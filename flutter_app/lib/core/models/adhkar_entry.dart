/// Matches the required Adhkar database schema from the Phase 2 directive.
enum AdhkarCategory {
  morning,
  evening,
  sleep,
  wakeUp,
  prayer,
  travel,
  protection,
  quranicDuas,
  dailyDuas,
  generalDhikr,
}

extension AdhkarCategoryX on AdhkarCategory {
  /// Stable string stored in the database — never rename these once shipped.
  String get id {
    switch (this) {
      case AdhkarCategory.morning:
        return 'morning';
      case AdhkarCategory.evening:
        return 'evening';
      case AdhkarCategory.sleep:
        return 'sleep';
      case AdhkarCategory.wakeUp:
        return 'wake_up';
      case AdhkarCategory.prayer:
        return 'prayer';
      case AdhkarCategory.travel:
        return 'travel';
      case AdhkarCategory.protection:
        return 'protection';
      case AdhkarCategory.quranicDuas:
        return 'quranic_duas';
      case AdhkarCategory.dailyDuas:
        return 'daily_duas';
      case AdhkarCategory.generalDhikr:
        return 'general_dhikr';
    }
  }

  static AdhkarCategory fromId(String id) =>
      AdhkarCategory.values.firstWhere((c) => c.id == id, orElse: () => AdhkarCategory.generalDhikr);
}

class AdhkarEntry {
  const AdhkarEntry({
    required this.id,
    required this.category,
    required this.titleAr,
    required this.titleEn,
    required this.arabicText,
    required this.transliteration,
    required this.translationEn,
    required this.sourceReference,
    required this.repetitionCount,
    this.repetitionNote,
    required this.audioAvailable,
    this.favourite = false,
    required this.createdAt,
  });

  final String id;
  final AdhkarCategory category;
  final String titleAr;
  final String titleEn;
  final String arabicText;
  final String transliteration;
  final String translationEn;
  final String sourceReference;
  final int repetitionCount;

  /// Free-text repetition instruction as it actually appears in the source
  /// (e.g. "قالها ثلاثاً" / "said three times") — kept alongside the numeric
  /// [repetitionCount] rather than replacing it, since some source passages
  /// describe repetition in a way a bare integer can't fully capture.
  final String? repetitionNote;

  final bool audioAvailable;
  final bool favourite;
  final DateTime createdAt;

  AdhkarEntry copyWith({bool? favourite}) => AdhkarEntry(
        id: id,
        category: category,
        titleAr: titleAr,
        titleEn: titleEn,
        arabicText: arabicText,
        transliteration: transliteration,
        translationEn: translationEn,
        sourceReference: sourceReference,
        repetitionCount: repetitionCount,
        repetitionNote: repetitionNote,
        audioAvailable: audioAvailable,
        favourite: favourite ?? this.favourite,
        createdAt: createdAt,
      );
}
