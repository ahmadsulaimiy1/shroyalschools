import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'notification_service.dart';

/// How a fixed-time reminder repeats across the week.
enum ReminderRepeatRule { daily, weekdays, weekends, custom }

enum TahajjudWakeStyle { gentle, strong }

/// A single fixed-time reminder (Adhkar morning/evening/sleep/travel,
/// Qur'an reading/memorisation) -- everything needed to (re)schedule it.
class TimeReminder {
  const TimeReminder({
    required this.enabled,
    required this.time,
    this.repeatRule = ReminderRepeatRule.daily,
    this.customDays = const {},
  });

  final bool enabled;
  final TimeOfDay time;
  final ReminderRepeatRule repeatRule;

  /// Only used when [repeatRule] is [ReminderRepeatRule.custom] --
  /// [DateTime.weekday] values (1 = Monday .. 7 = Sunday).
  final Set<int> customDays;

  TimeReminder copyWith({bool? enabled, TimeOfDay? time, ReminderRepeatRule? repeatRule, Set<int>? customDays}) =>
      TimeReminder(
        enabled: enabled ?? this.enabled,
        time: time ?? this.time,
        repeatRule: repeatRule ?? this.repeatRule,
        customDays: customDays ?? this.customDays,
      );

  Map<String, dynamic> toJson() => {
        'enabled': enabled,
        'hour': time.hour,
        'minute': time.minute,
        'repeatRule': repeatRule.name,
        'customDays': customDays.toList(),
      };

  factory TimeReminder.fromJson(Map<String, dynamic> json, TimeReminder fallback) => TimeReminder(
        enabled: json['enabled'] as bool? ?? fallback.enabled,
        time: TimeOfDay(hour: json['hour'] as int? ?? fallback.time.hour, minute: json['minute'] as int? ?? fallback.time.minute),
        repeatRule: ReminderRepeatRule.values.firstWhere(
          (r) => r.name == json['repeatRule'],
          orElse: () => fallback.repeatRule,
        ),
        customDays: (json['customDays'] as List?)?.cast<int>().toSet() ?? fallback.customDays,
      );
}

class TahajjudSettings {
  const TahajjudSettings({
    required this.enabled,
    required this.useSmartTime,
    required this.manualTime,
    required this.wakeStyle,
    required this.escalatingReminders,
    required this.headsUpMinutesBefore,
    required this.vibrationPattern,
    required this.alarmCount,
  });

  final bool enabled;

  /// When true, the wake time is computed as the last third of the night
  /// (classical Tahajjud timing) from that day's Maghrib/Fajr via
  /// adhan_dart's SunnahTimes -- see reminder_scheduler.dart. When false,
  /// [manualTime] is used verbatim every night.
  final bool useSmartTime;
  final TimeOfDay manualTime;
  final TahajjudWakeStyle wakeStyle;

  /// Whether a gentler "heads up" notification fires before the main alarm.
  final bool escalatingReminders;
  final int headsUpMinutesBefore;
  final VibrationPatternPreset vibrationPattern;

  /// Number of alarms to schedule (the primary time, plus this many extra
  /// alarms spaced 10 minutes apart) -- "multiple alarms" from the
  /// directive, for users who want a backup in case they sleep through
  /// the first.
  final int alarmCount;

  TahajjudSettings copyWith({
    bool? enabled,
    bool? useSmartTime,
    TimeOfDay? manualTime,
    TahajjudWakeStyle? wakeStyle,
    bool? escalatingReminders,
    int? headsUpMinutesBefore,
    VibrationPatternPreset? vibrationPattern,
    int? alarmCount,
  }) =>
      TahajjudSettings(
        enabled: enabled ?? this.enabled,
        useSmartTime: useSmartTime ?? this.useSmartTime,
        manualTime: manualTime ?? this.manualTime,
        wakeStyle: wakeStyle ?? this.wakeStyle,
        escalatingReminders: escalatingReminders ?? this.escalatingReminders,
        headsUpMinutesBefore: headsUpMinutesBefore ?? this.headsUpMinutesBefore,
        vibrationPattern: vibrationPattern ?? this.vibrationPattern,
        alarmCount: alarmCount ?? this.alarmCount,
      );

  Map<String, dynamic> toJson() => {
        'enabled': enabled,
        'useSmartTime': useSmartTime,
        'hour': manualTime.hour,
        'minute': manualTime.minute,
        'wakeStyle': wakeStyle.name,
        'escalatingReminders': escalatingReminders,
        'headsUpMinutesBefore': headsUpMinutesBefore,
        'vibrationPattern': vibrationPattern.name,
        'alarmCount': alarmCount,
      };

  static const fallback = TahajjudSettings(
    enabled: false,
    useSmartTime: true,
    manualTime: TimeOfDay(hour: 3, minute: 30),
    wakeStyle: TahajjudWakeStyle.gentle,
    escalatingReminders: true,
    headsUpMinutesBefore: 15,
    vibrationPattern: VibrationPatternPreset.standard,
    alarmCount: 1,
  );

  factory TahajjudSettings.fromJson(Map<String, dynamic> json) => TahajjudSettings(
        enabled: json['enabled'] as bool? ?? fallback.enabled,
        useSmartTime: json['useSmartTime'] as bool? ?? fallback.useSmartTime,
        manualTime: TimeOfDay(
          hour: json['hour'] as int? ?? fallback.manualTime.hour,
          minute: json['minute'] as int? ?? fallback.manualTime.minute,
        ),
        wakeStyle: TahajjudWakeStyle.values.firstWhere(
          (w) => w.name == json['wakeStyle'],
          orElse: () => fallback.wakeStyle,
        ),
        escalatingReminders: json['escalatingReminders'] as bool? ?? fallback.escalatingReminders,
        headsUpMinutesBefore: json['headsUpMinutesBefore'] as int? ?? fallback.headsUpMinutesBefore,
        vibrationPattern: VibrationPatternPreset.values.firstWhere(
          (v) => v.name == json['vibrationPattern'],
          orElse: () => fallback.vibrationPattern,
        ),
        alarmCount: json['alarmCount'] as int? ?? fallback.alarmCount,
      );
}

class QuietHours {
  const QuietHours({required this.enabled, required this.start, required this.end});
  final bool enabled;
  final TimeOfDay start;
  final TimeOfDay end;

  static const fallback = QuietHours(enabled: false, start: TimeOfDay(hour: 22, minute: 0), end: TimeOfDay(hour: 6, minute: 0));

  /// Whether [time] falls within the quiet window, correctly handling a
  /// window that wraps past midnight (e.g. 22:00 -> 06:00).
  bool suppresses(TimeOfDay time) {
    if (!enabled) return false;
    final t = time.hour * 60 + time.minute;
    final s = start.hour * 60 + start.minute;
    final e = end.hour * 60 + end.minute;
    if (s == e) return false;
    return s < e ? (t >= s && t < e) : (t >= s || t < e);
  }

  QuietHours copyWith({bool? enabled, TimeOfDay? start, TimeOfDay? end}) =>
      QuietHours(enabled: enabled ?? this.enabled, start: start ?? this.start, end: end ?? this.end);
}

/// Persisted worship-reminder preferences: everything [ReminderScheduler]
/// needs to decide what to schedule. Kept as its own controller (matching
/// [PrayerSettingsController]/[QuranAudioController]'s pattern) since this
/// is a large, independently-growing settings surface.
class ReminderSettingsController extends ChangeNotifier {
  static const _kAdhanEnabled = 'reminder_adhan_enabled';
  static const _kEarlyReminderMinutes = 'reminder_early_minutes';
  static const _kIqamahReminderMinutes = 'reminder_iqamah_minutes';
  static const _kMissedPrayerEnabled = 'reminder_missed_prayer_enabled';
  static const _kMissedPrayerDelayMinutes = 'reminder_missed_prayer_delay_minutes';
  static const _kFridayEnabled = 'reminder_friday_enabled';
  static const _kFridayMinutesBefore = 'reminder_friday_minutes_before';
  static const _kRamadanModeEnabled = 'reminder_ramadan_mode_enabled';
  static const _kTahajjud = 'reminder_tahajjud';
  static const _kQuietHours = 'reminder_quiet_hours';
  static const _kQuranReading = 'reminder_quran_reading';
  static const _kQuranKhatm = 'reminder_quran_khatm';
  static const _kQuranMemorisation = 'reminder_quran_memorisation';
  static const _kAdhkarMorning = 'reminder_adhkar_morning';
  static const _kAdhkarEvening = 'reminder_adhkar_evening';
  static const _kAdhkarSleep = 'reminder_adhkar_sleep';
  static const _kAdhkarTravel = 'reminder_adhkar_travel';

  bool _adhanEnabled = true;
  int? _earlyReminderMinutes;
  int? _iqamahReminderMinutes = 15;
  bool _missedPrayerEnabled = false;
  int _missedPrayerDelayMinutes = 30;
  bool _fridayEnabled = false;
  int _fridayMinutesBefore = 30;
  bool _ramadanModeEnabled = false;
  TahajjudSettings _tahajjud = TahajjudSettings.fallback;
  QuietHours _quietHours = QuietHours.fallback;
  TimeReminder _quranReading = const TimeReminder(enabled: false, time: TimeOfDay(hour: 20, minute: 0));
  TimeReminder _quranKhatm = const TimeReminder(enabled: false, time: TimeOfDay(hour: 20, minute: 30));
  TimeReminder _quranMemorisation = const TimeReminder(enabled: false, time: TimeOfDay(hour: 6, minute: 0));
  TimeReminder _adhkarMorning = const TimeReminder(enabled: false, time: TimeOfDay(hour: 6, minute: 30));
  TimeReminder _adhkarEvening = const TimeReminder(enabled: false, time: TimeOfDay(hour: 17, minute: 30));
  TimeReminder _adhkarSleep = const TimeReminder(enabled: false, time: TimeOfDay(hour: 22, minute: 0));
  TimeReminder _adhkarTravel = const TimeReminder(enabled: false, time: TimeOfDay(hour: 8, minute: 0));

  bool get adhanEnabled => _adhanEnabled;
  int? get earlyReminderMinutes => _earlyReminderMinutes;
  int? get iqamahReminderMinutes => _iqamahReminderMinutes;
  bool get missedPrayerEnabled => _missedPrayerEnabled;
  int get missedPrayerDelayMinutes => _missedPrayerDelayMinutes;
  bool get fridayEnabled => _fridayEnabled;
  int get fridayMinutesBefore => _fridayMinutesBefore;
  bool get ramadanModeEnabled => _ramadanModeEnabled;
  TahajjudSettings get tahajjud => _tahajjud;
  QuietHours get quietHours => _quietHours;
  TimeReminder get quranReading => _quranReading;
  TimeReminder get quranKhatm => _quranKhatm;
  TimeReminder get quranMemorisation => _quranMemorisation;
  TimeReminder get adhkarMorning => _adhkarMorning;
  TimeReminder get adhkarEvening => _adhkarEvening;
  TimeReminder get adhkarSleep => _adhkarSleep;
  TimeReminder get adhkarTravel => _adhkarTravel;

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _adhanEnabled = prefs.getBool(_kAdhanEnabled) ?? true;
    _earlyReminderMinutes = prefs.getInt(_kEarlyReminderMinutes);
    _iqamahReminderMinutes = prefs.containsKey(_kIqamahReminderMinutes) ? prefs.getInt(_kIqamahReminderMinutes) : 15;
    _missedPrayerEnabled = prefs.getBool(_kMissedPrayerEnabled) ?? false;
    _missedPrayerDelayMinutes = prefs.getInt(_kMissedPrayerDelayMinutes) ?? 30;
    _fridayEnabled = prefs.getBool(_kFridayEnabled) ?? false;
    _fridayMinutesBefore = prefs.getInt(_kFridayMinutesBefore) ?? 30;
    _ramadanModeEnabled = prefs.getBool(_kRamadanModeEnabled) ?? false;
    _tahajjud = _loadTahajjud(prefs);
    _quietHours = _loadQuietHours(prefs);
    _quranReading = _loadReminder(prefs, _kQuranReading, _quranReading);
    _quranKhatm = _loadReminder(prefs, _kQuranKhatm, _quranKhatm);
    _quranMemorisation = _loadReminder(prefs, _kQuranMemorisation, _quranMemorisation);
    _adhkarMorning = _loadReminder(prefs, _kAdhkarMorning, _adhkarMorning);
    _adhkarEvening = _loadReminder(prefs, _kAdhkarEvening, _adhkarEvening);
    _adhkarSleep = _loadReminder(prefs, _kAdhkarSleep, _adhkarSleep);
    _adhkarTravel = _loadReminder(prefs, _kAdhkarTravel, _adhkarTravel);
    notifyListeners();
  }

  TimeReminder _loadReminder(SharedPreferences prefs, String key, TimeReminder fallback) {
    final raw = prefs.getString(key);
    if (raw == null) return fallback;
    try {
      return TimeReminder.fromJson(_decodeMap(raw), fallback);
    } catch (_) {
      return fallback;
    }
  }

  TahajjudSettings _loadTahajjud(SharedPreferences prefs) {
    final raw = prefs.getString(_kTahajjud);
    if (raw == null) return TahajjudSettings.fallback;
    try {
      return TahajjudSettings.fromJson(_decodeMap(raw));
    } catch (_) {
      return TahajjudSettings.fallback;
    }
  }

  QuietHours _loadQuietHours(SharedPreferences prefs) {
    final raw = prefs.getString(_kQuietHours);
    if (raw == null) return QuietHours.fallback;
    try {
      final json = _decodeMap(raw);
      return QuietHours(
        enabled: json['enabled'] as bool? ?? false,
        start: TimeOfDay(hour: json['startHour'] as int, minute: json['startMinute'] as int),
        end: TimeOfDay(hour: json['endHour'] as int, minute: json['endMinute'] as int),
      );
    } catch (_) {
      return QuietHours.fallback;
    }
  }

  Future<void> _save(String key, Map<String, dynamic> json) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(key, _encodeMap(json));
  }

  Future<void> setAdhanEnabled(bool value) async {
    _adhanEnabled = value;
    notifyListeners();
    await (await SharedPreferences.getInstance()).setBool(_kAdhanEnabled, value);
  }

  Future<void> setEarlyReminderMinutes(int? minutes) async {
    _earlyReminderMinutes = minutes;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    if (minutes == null) {
      await prefs.remove(_kEarlyReminderMinutes);
    } else {
      await prefs.setInt(_kEarlyReminderMinutes, minutes);
    }
  }

  Future<void> setIqamahReminderMinutes(int? minutes) async {
    _iqamahReminderMinutes = minutes;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    if (minutes == null) {
      await prefs.remove(_kIqamahReminderMinutes);
    } else {
      await prefs.setInt(_kIqamahReminderMinutes, minutes);
    }
  }

  Future<void> setMissedPrayerEnabled(bool value) async {
    _missedPrayerEnabled = value;
    notifyListeners();
    await (await SharedPreferences.getInstance()).setBool(_kMissedPrayerEnabled, value);
  }

  Future<void> setMissedPrayerDelayMinutes(int minutes) async {
    _missedPrayerDelayMinutes = minutes;
    notifyListeners();
    await (await SharedPreferences.getInstance()).setInt(_kMissedPrayerDelayMinutes, minutes);
  }

  Future<void> setFridayEnabled(bool value) async {
    _fridayEnabled = value;
    notifyListeners();
    await (await SharedPreferences.getInstance()).setBool(_kFridayEnabled, value);
  }

  Future<void> setFridayMinutesBefore(int minutes) async {
    _fridayMinutesBefore = minutes;
    notifyListeners();
    await (await SharedPreferences.getInstance()).setInt(_kFridayMinutesBefore, minutes);
  }

  Future<void> setRamadanModeEnabled(bool value) async {
    _ramadanModeEnabled = value;
    notifyListeners();
    await (await SharedPreferences.getInstance()).setBool(_kRamadanModeEnabled, value);
  }

  Future<void> setTahajjud(TahajjudSettings value) async {
    _tahajjud = value;
    notifyListeners();
    await _save(_kTahajjud, value.toJson());
  }

  Future<void> setQuietHours(QuietHours value) async {
    _quietHours = value;
    notifyListeners();
    await _save(_kQuietHours, {
      'enabled': value.enabled,
      'startHour': value.start.hour,
      'startMinute': value.start.minute,
      'endHour': value.end.hour,
      'endMinute': value.end.minute,
    });
  }

  Future<void> setQuranReading(TimeReminder value) async {
    _quranReading = value;
    notifyListeners();
    await _save(_kQuranReading, value.toJson());
  }

  Future<void> setQuranKhatm(TimeReminder value) async {
    _quranKhatm = value;
    notifyListeners();
    await _save(_kQuranKhatm, value.toJson());
  }

  Future<void> setQuranMemorisation(TimeReminder value) async {
    _quranMemorisation = value;
    notifyListeners();
    await _save(_kQuranMemorisation, value.toJson());
  }

  Future<void> setAdhkarMorning(TimeReminder value) async {
    _adhkarMorning = value;
    notifyListeners();
    await _save(_kAdhkarMorning, value.toJson());
  }

  Future<void> setAdhkarEvening(TimeReminder value) async {
    _adhkarEvening = value;
    notifyListeners();
    await _save(_kAdhkarEvening, value.toJson());
  }

  Future<void> setAdhkarSleep(TimeReminder value) async {
    _adhkarSleep = value;
    notifyListeners();
    await _save(_kAdhkarSleep, value.toJson());
  }

  Future<void> setAdhkarTravel(TimeReminder value) async {
    _adhkarTravel = value;
    notifyListeners();
    await _save(_kAdhkarTravel, value.toJson());
  }
}

Map<String, dynamic> _decodeMap(String raw) => Map<String, dynamic>.from(jsonDecode(raw) as Map);
String _encodeMap(Map<String, dynamic> json) => jsonEncode(json);
