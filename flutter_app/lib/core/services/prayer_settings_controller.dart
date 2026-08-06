import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'prayer_times_service.dart';

/// Persisted Prayer Times preferences: calculation method, Asr madhab,
/// per-prayer manual minute offsets, and the last-known location fix.
/// Kept separate from [SettingsController] the same way Qur'an audio has
/// its own controller -- this is a distinct worship subsystem with its own
/// growing settings surface (notifications/alarms build on top of it next).
class PrayerSettingsController extends ChangeNotifier {
  static const _kMethod = 'prayer_calculation_method';
  static const _kMadhab = 'prayer_asr_madhab';
  static const _kLat = 'prayer_location_lat';
  static const _kLon = 'prayer_location_lon';
  static const _kLocationLabel = 'prayer_location_label';
  static const _kAdjustmentPrefix = 'prayer_adjustment_';

  PrayerCalculationMethod _method = PrayerCalculationMethod.ummAlQura;
  PrayerAsrMadhab _madhab = PrayerAsrMadhab.hanafi;
  double? _latitude;
  double? _longitude;
  String? _locationLabel;
  Map<PrayerName, int> _adjustments = const {};

  PrayerCalculationMethod get method => _method;
  PrayerAsrMadhab get madhab => _madhab;
  double? get latitude => _latitude;
  double? get longitude => _longitude;
  String? get locationLabel => _locationLabel;
  Map<PrayerName, int> get adjustments => _adjustments;
  bool get hasLocation => _latitude != null && _longitude != null;

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _method = PrayerCalculationMethod.values.firstWhere(
      (e) => e.name == prefs.getString(_kMethod),
      orElse: () => PrayerCalculationMethod.ummAlQura,
    );
    _madhab = PrayerAsrMadhab.values.firstWhere(
      (e) => e.name == prefs.getString(_kMadhab),
      orElse: () => PrayerAsrMadhab.hanafi,
    );
    _latitude = prefs.getDouble(_kLat);
    _longitude = prefs.getDouble(_kLon);
    _locationLabel = prefs.getString(_kLocationLabel);
    _adjustments = {
      for (final p in PrayerName.values)
        if (prefs.containsKey('$_kAdjustmentPrefix${p.name}')) p: prefs.getInt('$_kAdjustmentPrefix${p.name}')!,
    };
    notifyListeners();
  }

  Future<void> setMethod(PrayerCalculationMethod method) async {
    _method = method;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kMethod, method.name);
  }

  Future<void> setMadhab(PrayerAsrMadhab madhab) async {
    _madhab = madhab;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kMadhab, madhab.name);
  }

  Future<void> setLocation({required double latitude, required double longitude, String? label}) async {
    _latitude = latitude;
    _longitude = longitude;
    _locationLabel = label;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble(_kLat, latitude);
    await prefs.setDouble(_kLon, longitude);
    if (label != null) {
      await prefs.setString(_kLocationLabel, label);
    } else {
      await prefs.remove(_kLocationLabel);
    }
  }

  Future<void> setAdjustment(PrayerName prayer, int minutes) async {
    _adjustments = {..._adjustments, prayer: minutes};
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('$_kAdjustmentPrefix${prayer.name}', minutes);
  }
}
