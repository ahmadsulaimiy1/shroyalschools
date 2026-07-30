import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;
import 'package:sqflite/sqflite.dart';

import '../models/quran_chapter.dart';
import '../models/quran_juz.dart';
import '../models/quran_verse.dart';
import 'database_helper.dart';

/// Strips Qur'anic diacritics (tashkeel/harakat) for a more forgiving search
/// match — a search for "الرحمن" should still find "ٱلرَّحۡمَٰنِ".
String _stripDiacritics(String text) => text.replaceAll(RegExp(r'[ً-ٰٟۖ-ۭ]'), '');

class QuranReadingStats {
  const QuranReadingStats({required this.todayCount, required this.totalVersesRead, required this.streakDays});
  final int todayCount;
  final int totalVersesRead;
  final int streakDays;
}

/// The Qur'an text/translation/chapter/juz metadata is bundled as read-only
/// JSON assets (assets/quran/*.json) rather than shipped as generated Dart
/// source or a sqflite table — at ~6,236 verses that would bloat both the
/// compiled binary and the diff surface for something that never changes at
/// runtime. Only user-generated state (bookmarks, favourites, last-read
/// position, reading log) lives in sqflite — see database_helper.dart.
class QuranRepository {
  QuranRepository(this._db);
  final DatabaseHelper _db;

  List<QuranChapter>? _chapters;
  List<QuranVerse>? _verses;
  List<QuranJuz>? _juz;
  Map<int, List<QuranVerse>>? _versesBySurah;

  Future<void> _ensureLoaded() async {
    if (_chapters != null && _verses != null && _juz != null) return;

    final chaptersJson = await rootBundle.loadString('assets/quran/chapters.json');
    final versesJson = await rootBundle.loadString('assets/quran/verses.json');
    final juzJson = await rootBundle.loadString('assets/quran/juz.json');

    _chapters = (jsonDecode(chaptersJson) as List)
        .map((e) => QuranChapter.fromJson(e as Map<String, dynamic>))
        .toList(growable: false);
    _verses = (jsonDecode(versesJson) as List)
        .map((e) => QuranVerse.fromJson(e as Map<String, dynamic>))
        .toList(growable: false);
    _juz = (jsonDecode(juzJson) as List)
        .map((e) => QuranJuz.fromJson(e as Map<String, dynamic>))
        .toList(growable: false);

    final bySurah = <int, List<QuranVerse>>{};
    for (final v in _verses!) {
      bySurah.putIfAbsent(v.surah, () => []).add(v);
    }
    _versesBySurah = bySurah;
  }

  Future<List<QuranChapter>> chapters() async {
    await _ensureLoaded();
    return _chapters!;
  }

  Future<QuranChapter> chapter(int number) async {
    await _ensureLoaded();
    return _chapters!.firstWhere((c) => c.number == number);
  }

  Future<List<QuranVerse>> versesForChapter(int surah) async {
    await _ensureLoaded();
    return _versesBySurah![surah] ?? const [];
  }

  Future<QuranVerse?> verseAt(int surah, int ayah) async {
    await _ensureLoaded();
    final list = _versesBySurah![surah];
    if (list == null) return null;
    for (final v in list) {
      if (v.ayah == ayah) return v;
    }
    return null;
  }

  Future<List<QuranJuz>> juzList() async {
    await _ensureLoaded();
    return _juz!;
  }

  Future<List<QuranVerse>> versesForJuz(int juzNumber) async {
    await _ensureLoaded();
    final juz = _juz!.firstWhere((j) => j.number == juzNumber);
    return _verses!.where((v) {
      final afterStart = v.surah > juz.startSurah || (v.surah == juz.startSurah && v.ayah >= juz.startAyah);
      final beforeEnd = v.surah < juz.endSurah || (v.surah == juz.endSurah && v.ayah <= juz.endAyah);
      return afterStart && beforeEnd;
    }).toList(growable: false);
  }

  /// Case-insensitive English search plus diacritic-insensitive Arabic
  /// search, over the full 6,236-verse corpus. This is a linear scan, but
  /// the whole dataset is a couple of MB in memory — instant on any modern
  /// device, so no FTS index is needed.
  Future<List<QuranVerse>> search(String query) async {
    await _ensureLoaded();
    final trimmed = query.trim();
    if (trimmed.isEmpty) return const [];
    final lowerQuery = trimmed.toLowerCase();
    final normalizedArQuery = _stripDiacritics(trimmed);
    return _verses!.where((v) {
      if (v.translationEn.toLowerCase().contains(lowerQuery)) return true;
      if (normalizedArQuery.isNotEmpty && _stripDiacritics(v.arabicText).contains(normalizedArQuery)) return true;
      return false;
    }).toList(growable: false);
  }

  // --- Bookmarks ---

  Future<void> addBookmark(int surah, int ayah) async {
    final db = await _db.database;
    await db.insert(
      'quran_bookmarks',
      {'surah': surah, 'ayah': ayah, 'created_at': DateTime.now().millisecondsSinceEpoch},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<void> removeBookmark(int surah, int ayah) async {
    final db = await _db.database;
    await db.delete('quran_bookmarks', where: 'surah = ? AND ayah = ?', whereArgs: [surah, ayah]);
  }

  Future<bool> isBookmarked(int surah, int ayah) async {
    final db = await _db.database;
    final rows = await db.query('quran_bookmarks', where: 'surah = ? AND ayah = ?', whereArgs: [surah, ayah]);
    return rows.isNotEmpty;
  }

  Future<List<QuranVerse>> bookmarkedVerses() async {
    await _ensureLoaded();
    final db = await _db.database;
    final rows = await db.query('quran_bookmarks', orderBy: 'created_at DESC');
    return _resolveRows(rows);
  }

  // --- Favourites ---

  Future<void> setFavourite(int surah, int ayah, bool favourite) async {
    final db = await _db.database;
    if (favourite) {
      await db.insert(
        'quran_favourites',
        {'surah': surah, 'ayah': ayah, 'created_at': DateTime.now().millisecondsSinceEpoch},
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    } else {
      await db.delete('quran_favourites', where: 'surah = ? AND ayah = ?', whereArgs: [surah, ayah]);
    }
  }

  Future<bool> isFavourite(int surah, int ayah) async {
    final db = await _db.database;
    final rows = await db.query('quran_favourites', where: 'surah = ? AND ayah = ?', whereArgs: [surah, ayah]);
    return rows.isNotEmpty;
  }

  Future<List<QuranVerse>> favouriteVerses() async {
    await _ensureLoaded();
    final db = await _db.database;
    final rows = await db.query('quran_favourites', orderBy: 'created_at DESC');
    return _resolveRows(rows);
  }

  List<QuranVerse> _resolveRows(List<Map<String, Object?>> rows) {
    final result = <QuranVerse>[];
    for (final row in rows) {
      final v = _versesBySurah![row['surah'] as int]?.firstWhere(
        (v) => v.ayah == row['ayah'] as int,
        orElse: () => const QuranVerse(surah: 0, ayah: 0, arabicText: '', translationEn: ''),
      );
      if (v != null && v.surah != 0) result.add(v);
    }
    return result;
  }

  // --- Last read ---

  Future<void> setLastRead(int surah, int ayah) async {
    final db = await _db.database;
    await db.insert(
      'quran_last_read',
      {'id': 1, 'surah': surah, 'ayah': ayah, 'updated_at': DateTime.now().millisecondsSinceEpoch},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
    await db.insert('quran_reads', {'surah': surah, 'ayah': ayah, 'read_at': DateTime.now().millisecondsSinceEpoch});
  }

  Future<QuranVerse?> lastRead() async {
    await _ensureLoaded();
    final db = await _db.database;
    final rows = await db.query('quran_last_read', where: 'id = 1');
    if (rows.isEmpty) return null;
    final row = rows.first;
    return verseAt(row['surah'] as int, row['ayah'] as int);
  }

  // --- Reading statistics ---

  Future<QuranReadingStats> readingStats() async {
    final db = await _db.database;
    final now = DateTime.now();
    final startOfToday = DateTime(now.year, now.month, now.day).millisecondsSinceEpoch;

    final todayRows = await db.rawQuery(
      'SELECT COUNT(DISTINCT surah || ":" || ayah) as c FROM quran_reads WHERE read_at >= ?',
      [startOfToday],
    );
    final totalRows = await db.rawQuery('SELECT COUNT(DISTINCT surah || ":" || ayah) as c FROM quran_reads');
    final dayRows = await db.rawQuery('SELECT DISTINCT read_at FROM quran_reads ORDER BY read_at DESC');

    final readDays = <String>{};
    for (final row in dayRows) {
      final d = DateTime.fromMillisecondsSinceEpoch(row['read_at'] as int);
      readDays.add('${d.year}-${d.month}-${d.day}');
    }
    var streak = 0;
    var cursor = DateTime(now.year, now.month, now.day);
    while (readDays.contains('${cursor.year}-${cursor.month}-${cursor.day}')) {
      streak++;
      cursor = cursor.subtract(const Duration(days: 1));
    }

    return QuranReadingStats(
      todayCount: Sqflite.firstIntValue(todayRows) ?? 0,
      totalVersesRead: Sqflite.firstIntValue(totalRows) ?? 0,
      streakDays: streak,
    );
  }
}
