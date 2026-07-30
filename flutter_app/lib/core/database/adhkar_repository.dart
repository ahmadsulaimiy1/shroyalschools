import 'package:sqflite/sqflite.dart';

import '../models/adhkar_entry.dart';
import 'database_helper.dart';

class AdhkarRepository {
  AdhkarRepository(this._db);
  final DatabaseHelper _db;

  Future<int> count() async {
    final db = await _db.database;
    final result = await db.rawQuery('SELECT COUNT(*) as c FROM adhkar');
    return Sqflite.firstIntValue(result) ?? 0;
  }

  /// Seeds the adhkar table on first run (or after an app update ships new
  /// entries) without duplicating rows or clobbering the user's favourites —
  /// existing ids are left untouched, only missing ones are inserted.
  Future<void> seedIfNeeded(List<AdhkarEntry> seedEntries) async {
    final db = await _db.database;
    final batch = db.batch();
    for (final entry in seedEntries) {
      batch.insert(
        'adhkar',
        _toRow(entry),
        conflictAlgorithm: ConflictAlgorithm.ignore,
      );
    }
    await batch.commit(noResult: true);
  }

  Future<List<AdhkarEntry>> byCategory(AdhkarCategory category) async {
    final db = await _db.database;
    final rows = await db.query(
      'adhkar',
      where: 'category = ?',
      whereArgs: [category.id],
      orderBy: 'created_at ASC',
    );
    return rows.map(_fromRow).toList();
  }

  Future<List<AdhkarEntry>> favourites() async {
    final db = await _db.database;
    final rows = await db.query('adhkar', where: 'favourite = 1', orderBy: 'created_at ASC');
    return rows.map(_fromRow).toList();
  }

  Future<Map<AdhkarCategory, int>> countsByCategory() async {
    final db = await _db.database;
    final rows = await db.rawQuery('SELECT category, COUNT(*) as c FROM adhkar GROUP BY category');
    return {
      for (final row in rows) AdhkarCategoryX.fromId(row['category'] as String): row['c'] as int,
    };
  }

  Future<void> setFavourite(String id, bool favourite) async {
    final db = await _db.database;
    await db.update(
      'adhkar',
      {'favourite': favourite ? 1 : 0},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Map<String, Object?> _toRow(AdhkarEntry e) => {
        'id': e.id,
        'category': e.category.id,
        'title_ar': e.titleAr,
        'title_en': e.titleEn,
        'arabic_text': e.arabicText,
        'transliteration': e.transliteration,
        'translation_en': e.translationEn,
        'source_reference': e.sourceReference,
        'repetition_count': e.repetitionCount,
        'repetition_note': e.repetitionNote,
        'audio_available': e.audioAvailable ? 1 : 0,
        'favourite': e.favourite ? 1 : 0,
        'created_at': e.createdAt.millisecondsSinceEpoch,
      };

  AdhkarEntry _fromRow(Map<String, Object?> row) => AdhkarEntry(
        id: row['id'] as String,
        category: AdhkarCategoryX.fromId(row['category'] as String),
        titleAr: row['title_ar'] as String,
        titleEn: row['title_en'] as String,
        arabicText: row['arabic_text'] as String,
        transliteration: row['transliteration'] as String,
        translationEn: row['translation_en'] as String,
        sourceReference: row['source_reference'] as String,
        repetitionCount: row['repetition_count'] as int,
        repetitionNote: row['repetition_note'] as String?,
        audioAvailable: (row['audio_available'] as int) == 1,
        favourite: (row['favourite'] as int) == 1,
        createdAt: DateTime.fromMillisecondsSinceEpoch(row['created_at'] as int),
      );
}
