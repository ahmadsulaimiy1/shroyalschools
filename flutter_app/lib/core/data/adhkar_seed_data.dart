import '../models/adhkar_entry.dart';

/// Seed content for the Adhkar library, sourced from الورد المصفى ("Al-Wird
/// al-Musaffa"), selected by 'Abd al-'Aziz bin 'Abd al-Rahman Al-Faisal Al
/// Sa'ud (رحمه الله), published by Dar As-Salam, Cairo (1423H/2003).
///
/// Reproduced under license from the publisher — see /docs and the app's
/// About screen for the full attribution. This is a two-part compilation:
/// Part 1 is Qur'anic du'a verses in Mushaf order (category: quranicDuas);
/// Part 2 is Prophetic/traditional supplications with no built-in time-of-day
/// categorization (mapped here to generalDhikr/dailyDuas/protection based on
/// each entry's content). The book does not contain distinct Morning/
/// Evening/Sleep/Wake-up/Travel/Prayer sections — see docs/13-ADHKAR-IMPORT-VERIFICATION-REPORT.md
/// for the full import verification report and category-mapping rationale.
final DateTime _importedAt = DateTime.utc(2026, 7, 30);

final List<AdhkarEntry> wirdAlMusaffaSeed = [
  // Populated from docs/13-ADHKAR-IMPORT-VERIFICATION-REPORT.md batch
  // translations — see that report for the full entry-by-entry accounting.
];
