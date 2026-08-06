import 'package:adhan_dart/adhan_dart.dart';

/// The calculation-method presets we surface in Settings, mapped onto
/// adhan_dart's [CalculationMethodParameters] factories. Not every preset
/// the library ships is exposed here -- these are the conventions users are
/// actually likely to recognise and choose between (mirrors the options
/// most mainstream prayer-time apps offer).
enum PrayerCalculationMethod {
  muslimWorldLeague,
  egyptian,
  karachi,
  ummAlQura,
  dubai,
  moonsightingCommittee,
  northAmerica,
  kuwait,
  qatar,
  singapore,
  tehran,
  turkiye,
}

extension PrayerCalculationMethodX on PrayerCalculationMethod {
  CalculationParameters build() {
    switch (this) {
      case PrayerCalculationMethod.muslimWorldLeague:
        return CalculationMethodParameters.muslimWorldLeague();
      case PrayerCalculationMethod.egyptian:
        return CalculationMethodParameters.egyptian();
      case PrayerCalculationMethod.karachi:
        return CalculationMethodParameters.karachi();
      case PrayerCalculationMethod.ummAlQura:
        return CalculationMethodParameters.ummAlQura();
      case PrayerCalculationMethod.dubai:
        return CalculationMethodParameters.dubai();
      case PrayerCalculationMethod.moonsightingCommittee:
        return CalculationMethodParameters.moonsightingCommittee();
      case PrayerCalculationMethod.northAmerica:
        return CalculationMethodParameters.northAmerica();
      case PrayerCalculationMethod.kuwait:
        return CalculationMethodParameters.kuwait();
      case PrayerCalculationMethod.qatar:
        return CalculationMethodParameters.qatar();
      case PrayerCalculationMethod.singapore:
        return CalculationMethodParameters.singapore();
      case PrayerCalculationMethod.tehran:
        return CalculationMethodParameters.tehran();
      case PrayerCalculationMethod.turkiye:
        return CalculationMethodParameters.turkiye();
    }
  }
}

enum PrayerAsrMadhab { shafi, hanafi }

/// The five obligatory prayers plus sunrise, in the order they occur in a
/// day -- used for both display order and "next prayer" lookups.
enum PrayerName { fajr, sunrise, dhuhr, asr, maghrib, isha }

class DailyPrayerTimes {
  const DailyPrayerTimes({
    required this.fajr,
    required this.sunrise,
    required this.dhuhr,
    required this.asr,
    required this.maghrib,
    required this.isha,
  });

  final DateTime fajr;
  final DateTime sunrise;
  final DateTime dhuhr;
  final DateTime asr;
  final DateTime maghrib;
  final DateTime isha;

  DateTime timeFor(PrayerName name) {
    switch (name) {
      case PrayerName.fajr:
        return fajr;
      case PrayerName.sunrise:
        return sunrise;
      case PrayerName.dhuhr:
        return dhuhr;
      case PrayerName.asr:
        return asr;
      case PrayerName.maghrib:
        return maghrib;
      case PrayerName.isha:
        return isha;
    }
  }

  /// The next upcoming prayer relative to [at] (defaults to now), and the
  /// prayer after that if [at] is already past Isha for today -- callers
  /// wanting "tomorrow's Fajr" should compute the next day's [DailyPrayerTimes]
  /// and take its [fajr] instead; this getter only reasons about today.
  PrayerName? nextPrayer({DateTime? at}) {
    final now = at ?? DateTime.now();
    for (final name in PrayerName.values) {
      if (timeFor(name).isAfter(now)) return name;
    }
    return null;
  }
}

/// Wraps adhan_dart's astronomical prayer-time calculation: pure offline
/// computation from coordinates + date + method, no network calls, so once
/// a location fix is known the whole Prayer Times centre works without
/// connectivity. See docs/24 for the library's sourcing/verification note.
class PrayerTimesService {
  const PrayerTimesService();

  DailyPrayerTimes calculate({
    required double latitude,
    required double longitude,
    required DateTime date,
    required PrayerCalculationMethod method,
    required PrayerAsrMadhab madhab,
    Map<PrayerName, int> adjustmentsMinutes = const {},
  }) {
    final coordinates = Coordinates(latitude, longitude);
    final params = method.build()
      ..madhab = madhab == PrayerAsrMadhab.hanafi ? Madhab.hanafi : Madhab.shafi;

    for (final entry in adjustmentsMinutes.entries) {
      final prayer = _toAdhanPrayer(entry.key);
      if (prayer != null) {
        params.adjustments[prayer] = entry.value;
      }
    }

    final times = PrayerTimes(
      coordinates: coordinates,
      date: DateTime(date.year, date.month, date.day),
      calculationParameters: params,
      precision: true,
    );

    return DailyPrayerTimes(
      fajr: times.fajr.toLocal(),
      sunrise: times.sunrise.toLocal(),
      dhuhr: times.dhuhr.toLocal(),
      asr: times.asr.toLocal(),
      maghrib: times.maghrib.toLocal(),
      isha: times.isha.toLocal(),
    );
  }

  Prayer? _toAdhanPrayer(PrayerName name) {
    switch (name) {
      case PrayerName.fajr:
        return Prayer.fajr;
      case PrayerName.sunrise:
        return null; // adhan_dart has no adjustable Sunrise prayer entry.
      case PrayerName.dhuhr:
        return Prayer.dhuhr;
      case PrayerName.asr:
        return Prayer.asr;
      case PrayerName.maghrib:
        return Prayer.maghrib;
      case PrayerName.isha:
        return Prayer.isha;
    }
  }
}
