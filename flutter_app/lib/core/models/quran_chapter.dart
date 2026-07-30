class QuranChapter {
  const QuranChapter({
    required this.number,
    required this.nameArabic,
    required this.nameTransliteration,
    required this.nameTranslation,
    required this.revelationType,
    required this.versesCount,
  });

  final int number;
  final String nameArabic;
  final String nameTransliteration;
  final String nameTranslation;

  /// "meccan" or "medinan", as printed in the source metadata.
  final String revelationType;
  final int versesCount;

  factory QuranChapter.fromJson(Map<String, dynamic> json) => QuranChapter(
        number: json['number'] as int,
        nameArabic: json['nameArabic'] as String,
        nameTransliteration: json['nameTransliteration'] as String,
        nameTranslation: json['nameTranslation'] as String,
        revelationType: json['revelationType'] as String,
        versesCount: json['versesCount'] as int,
      );
}
