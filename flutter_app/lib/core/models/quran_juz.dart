class QuranJuz {
  const QuranJuz({
    required this.number,
    required this.startSurah,
    required this.startAyah,
    required this.endSurah,
    required this.endAyah,
  });

  final int number;
  final int startSurah;
  final int startAyah;
  final int endSurah;
  final int endAyah;

  factory QuranJuz.fromJson(Map<String, dynamic> json) => QuranJuz(
        number: json['number'] as int,
        startSurah: json['startSurah'] as int,
        startAyah: json['startAyah'] as int,
        endSurah: json['endSurah'] as int,
        endAyah: json['endAyah'] as int,
      );
}
