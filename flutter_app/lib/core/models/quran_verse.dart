class QuranVerse {
  const QuranVerse({
    required this.surah,
    required this.ayah,
    required this.arabicText,
    required this.translationEn,
  });

  final int surah;
  final int ayah;
  final String arabicText;
  final String translationEn;

  String get key => '$surah:$ayah';

  factory QuranVerse.fromJson(Map<String, dynamic> json) => QuranVerse(
        surah: json['surah'] as int,
        ayah: json['ayah'] as int,
        arabicText: json['ar'] as String,
        translationEn: json['en'] as String,
      );
}
