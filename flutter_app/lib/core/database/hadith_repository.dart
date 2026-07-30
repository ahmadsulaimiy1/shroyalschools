import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/hadith_entry.dart';

/// A 365-entry, evenly-sampled subset of Sahih al-Bukhari (English, Muhsin
/// Khan translation, public domain -- Unlicense) used for the "Daily
/// Hadith" home card. See docs/19-DAILY-HADITH-SOURCE.md for the full
/// source, license, and sampling-method disclosure: the 365 entries were
/// picked by deterministic even-stride sampling across the verified
/// 7,589-hadith collection (not hand-curated), specifically to keep the
/// bundled asset small (~200KB instead of ~4.6MB for the full collection)
/// while still being 100% verbatim, traceable source text.
class HadithRepository {
  List<HadithEntry>? _entries;

  Future<void> _ensureLoaded() async {
    if (_entries != null) return;
    final json = await rootBundle.loadString('assets/hadith/bukhari_en.json');
    _entries = (jsonDecode(json) as List).map((e) => HadithEntry.fromJson(e as Map<String, dynamic>)).toList(growable: false);
  }

  /// Deterministic "hadith of the day" -- the same calendar day always
  /// shows the same hadith, cycling through all 365 entries across the
  /// year.
  Future<HadithEntry> dailyHadith(DateTime date) async {
    await _ensureLoaded();
    final dayOfYear = DateTime(date.year, date.month, date.day).difference(DateTime(date.year, 1, 1)).inDays;
    final index = dayOfYear % _entries!.length;
    return _entries![index];
  }
}
