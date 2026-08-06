import 'package:hijri/hijri_calendar.dart';

/// Hijri month names (Gregorian-transliteration spellings), used for display
/// rather than the `hijri` package's own locale strings so this app's
/// spelling stays consistent with the rest of its UI copy.
const List<String> hijriMonthNamesEn = [
  'Muharram',
  'Safar',
  "Rabi' al-Awwal",
  "Rabi' al-Thani",
  'Jumada al-Awwal',
  'Jumada al-Thani',
  'Rajab',
  "Sha'ban",
  'Ramadan',
  'Shawwal',
  "Dhul Qi'dah",
  'Dhul Hijjah',
];

const List<String> hijriMonthNamesAr = [
  'محرم',
  'صفر',
  'ربيع الأول',
  'ربيع الآخر',
  'جمادى الأولى',
  'جمادى الآخرة',
  'رجب',
  'شعبان',
  'رمضان',
  'شوال',
  'ذو القعدة',
  'ذو الحجة',
];

/// One fixed point in the Hijri calendar that this app surfaces as an
/// "Islamic event" -- date only, computed on-device (never a separately
/// licensed dataset), since these are the Hijri calendar's own well-known
/// calendar dates, not scholarly content requiring separate sourcing.
class IslamicEvent {
  const IslamicEvent({required this.key, required this.hijriMonth, required this.hijriDay});

  /// Localisation key for the event name, e.g. 'calendar_event_ashura'.
  final String key;
  final int hijriMonth;
  final int hijriDay;
}

/// The standard set of dates most Islamic calendars mark. A couple of these
/// (Mawlid al-Nabi's observance, and Laylat al-Qadr's exact night within
/// the last ten nights of Ramadan) are subjects of differing scholarly and
/// community practice; they're included here as calendar *dates* only --
/// this list makes no claim about how, or whether, to observe them.
const List<IslamicEvent> islamicEvents = [
  IslamicEvent(key: 'islamic_new_year', hijriMonth: 1, hijriDay: 1),
  IslamicEvent(key: 'ashura', hijriMonth: 1, hijriDay: 10),
  IslamicEvent(key: 'mawlid_al_nabi', hijriMonth: 3, hijriDay: 12),
  IslamicEvent(key: 'start_of_ramadan', hijriMonth: 9, hijriDay: 1),
  IslamicEvent(key: 'laylat_al_qadr_estimated', hijriMonth: 9, hijriDay: 27),
  IslamicEvent(key: 'eid_al_fitr', hijriMonth: 10, hijriDay: 1),
  IslamicEvent(key: 'day_of_arafah', hijriMonth: 12, hijriDay: 9),
  IslamicEvent(key: 'eid_al_adha', hijriMonth: 12, hijriDay: 10),
];

class HijriDate {
  const HijriDate({required this.year, required this.month, required this.day});
  final int year;
  final int month;
  final int day;
}

class UpcomingIslamicEvent {
  const UpcomingIslamicEvent({required this.event, required this.gregorianDate, required this.hijriYear});
  final IslamicEvent event;
  final DateTime gregorianDate;
  final int hijriYear;
}

/// Wraps the `hijri` package's Umm al-Qura tabular calendar conversion --
/// the same convention used officially in Saudi Arabia -- for both
/// Gregorian-to-Hijri day lookups (month-view calendar cells) and computing
/// upcoming Islamic dates (agenda view). Pure on-device calculation, no
/// network calls, so this works fully offline. Dates computed this way can
/// differ by a day from local moon-sighting-based community announcements,
/// which this app cannot know in advance -- see docs/25.
class HijriCalendarService {
  const HijriCalendarService();

  HijriDate toHijri(DateTime gregorianDate) {
    final h = HijriCalendar.fromDate(gregorianDate);
    return HijriDate(year: h.hYear, month: h.hMonth, day: h.hDay);
  }

  DateTime toGregorian(int hijriYear, int hijriMonth, int hijriDay) {
    return HijriCalendar().hijriToGregorian(hijriYear, hijriMonth, hijriDay);
  }

  /// The next occurrence of every event in [islamicEvents] on/after [from],
  /// sorted chronologically -- checks the current Hijri year first and
  /// rolls over to the next if an event's date this year has already passed.
  List<UpcomingIslamicEvent> upcomingEvents(DateTime from) {
    final currentHijriYear = toHijri(from).year;
    final results = <UpcomingIslamicEvent>[];
    for (final event in islamicEvents) {
      var year = currentHijriYear;
      var date = toGregorian(year, event.hijriMonth, event.hijriDay);
      if (date.isBefore(DateTime(from.year, from.month, from.day))) {
        year += 1;
        date = toGregorian(year, event.hijriMonth, event.hijriDay);
      }
      results.add(UpcomingIslamicEvent(event: event, gregorianDate: date, hijriYear: year));
    }
    results.sort((a, b) => a.gregorianDate.compareTo(b.gregorianDate));
    return results;
  }
}
