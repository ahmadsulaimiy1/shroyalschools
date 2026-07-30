class HadithEntry {
  const HadithEntry({required this.number, required this.text, required this.book, required this.hadithInBook});

  /// Sequential number within Sahih al-Bukhari's standard English numbering.
  final int number;
  final String text;

  /// Book (chapter) number, per Sahih al-Bukhari's traditional book division.
  final int book;

  /// Hadith number within that book.
  final int hadithInBook;

  factory HadithEntry.fromJson(Map<String, dynamic> json) => HadithEntry(
        number: json['n'] as int,
        text: json['text'] as String,
        book: json['book'] as int,
        hadithInBook: json['hadith'] as int,
      );
}
