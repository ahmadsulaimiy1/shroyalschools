const _sajdahMark = '۩';

class QuranVerse {
  const QuranVerse({
    required this.surah,
    required this.ayah,
    required this.arabicText,
    required this.translationEn,
    this.transliteration = '',
    this.isSajdah = false,
  });

  final int surah;
  final int ayah;
  final String arabicText;
  final String translationEn;

  /// Latin-script transliteration (Tanzil.net's standard "quran-la" edition),
  /// used by Reading Mode C. Empty string for the placeholder verse used
  /// internally by [QuranRepository._resolveRows]'s not-found fallback.
  final String transliteration;

  /// Whether this is one of the 15 verses of prostration (sajdah al-tilawah).
  /// Derived directly from the bundled Uthmani text itself -- the verified
  /// Tanzil-sourced Arabic carries the traditional printed-Mushaf sajdah
  /// mark (۩, U+06E9) at these exact 15 locations; [fromJson] reads that
  /// mark once and strips it out of [arabicText] so rendering code always
  /// gets clean verse text and draws its own marker widget instead of
  /// relying on font glyph coverage for this rarely-supported codepoint.
  /// See docs/23 for the verification method and the note on madhhab
  /// differences in how these verses are graded.
  final bool isSajdah;

  String get key => '$surah:$ayah';

  factory QuranVerse.fromJson(Map<String, dynamic> json) {
    final rawArabic = json['ar'] as String;
    final sajdah = rawArabic.contains(_sajdahMark);
    final arabic = sajdah ? rawArabic.replaceAll(_sajdahMark, '').trimRight() : rawArabic;
    return QuranVerse(
      surah: json['surah'] as int,
      ayah: json['ayah'] as int,
      arabicText: arabic,
      translationEn: json['en'] as String,
      transliteration: json['tl'] as String? ?? '',
      isSajdah: sajdah,
    );
  }
}
