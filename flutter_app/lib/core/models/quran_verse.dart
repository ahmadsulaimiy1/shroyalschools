class QuranVerse {
  const QuranVerse({
    required this.surah,
    required this.ayah,
    required this.arabicText,
    required this.translationEn,
    this.transliteration = '',
  });

  final int surah;
  final int ayah;
  final String arabicText;
  final String translationEn;

  /// Latin-script transliteration (Tanzil.net's standard "quran-la" edition),
  /// used by Reading Mode C. Empty string for the placeholder verse used
  /// internally by [QuranRepository._resolveRows]'s not-found fallback.
  final String transliteration;

  String get key => '$surah:$ayah';

  factory QuranVerse.fromJson(Map<String, dynamic> json) => QuranVerse(
        surah: json['surah'] as int,
        ayah: json['ayah'] as int,
        arabicText: json['ar'] as String,
        translationEn: json['en'] as String,
        transliteration: json['tl'] as String? ?? '',
      );
}
