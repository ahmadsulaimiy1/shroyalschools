import 'dart:typed_data';
import 'dart:ui' show Locale;

import 'package:flutter/material.dart' show TimeOfDay;
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_timezone/flutter_timezone.dart';
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

import '../../localization/translations_ar.dart';
import '../../localization/translations_en.dart';
import 'notification_channels.dart';

/// Vibration pattern presets offered for Tahajjud's "strong wake" option
/// and (more subtly) for other reminder categories -- each is a sequence of
/// alternating pause/vibrate durations in milliseconds, starting with a
/// pause (Android's `VibrationEffect`/`Vibrator#vibrate(long[])` convention).
enum VibrationPatternPreset { standard, shortPulse, longPulse, escalating }

/// Thin, single-purpose wrapper around `flutter_local_notifications` +
/// `timezone`: plugin/timezone initialisation, Android notification-channel
/// creation, permission requests (POST_NOTIFICATIONS, exact alarms,
/// full-screen intent), and a small scheduling API used by
/// [ReminderScheduler]. Kept separate from scheduling *decisions* (what to
/// schedule and when) -- this class only knows how to schedule/cancel a
/// given notification, not why.
class NotificationService {
  NotificationService._();
  static final NotificationService instance = NotificationService._();

  final _plugin = FlutterLocalNotificationsPlugin();
  bool _initialized = false;
  Map<String, String> _strings = enTranslations;

  String _channelName(NotificationChannel channel) => _strings[channel.nameKey] ?? channel.nameKey;
  String? _channelDescription(NotificationChannel channel) => _strings[channel.descriptionKey];

  AndroidFlutterLocalNotificationsPlugin? get _android =>
      _plugin.resolvePlatformSpecificImplementation<AndroidFlutterLocalNotificationsPlugin>();

  /// [locale] resolves each channel's human-readable name/description at
  /// creation time (Android's channel settings UI shows these directly to
  /// the user, so they must be real text, not a translation key) -- taken
  /// from the persisted language preference since this runs before the
  /// widget tree (and therefore any `BuildContext`) exists. A channel's
  /// name only takes effect the first time it's created for a given id;
  /// switching language later does not retroactively rename channels
  /// already created on the device, a known limitation of Android's
  /// notification-channel API rather than something this app can override.
  Future<void> init({Locale locale = const Locale('en')}) async {
    if (_initialized) return;
    tz.initializeTimeZones();
    try {
      final timeZoneName = await FlutterTimezone.getLocalTimezone();
      tz.setLocalLocation(tz.getLocation(timeZoneName));
    } catch (_) {
      // Falls back to whatever default `timezone` ships with (UTC) --
      // reminders would then fire at the wrong clock time until the device's
      // timezone can be resolved, which is preferable to crashing.
    }

    await _plugin.initialize(
      settings: const InitializationSettings(
        android: AndroidInitializationSettings('@mipmap/ic_launcher'),
      ),
    );

    _strings = locale.languageCode == 'ar' ? arTranslations : enTranslations;
    for (final channel in NotificationChannels.all) {
      await _android?.createNotificationChannel(
        AndroidNotificationChannel(
          channel.id,
          _channelName(channel),
          description: _channelDescription(channel),
          importance: channel == NotificationChannels.tahajjudStrong
              ? Importance.max
              : channel == NotificationChannels.prayerAdhan
                  ? Importance.high
                  : Importance.defaultImportance,
        ),
      );
    }
    _initialized = true;
  }

  /// Requests POST_NOTIFICATIONS (Android 13+) and the exact-alarm
  /// permission (Android 12+). Returns whether notifications are permitted
  /// at all -- exact-alarm being declined is not fatal, callers should fall
  /// back to inexact scheduling (see [_scheduleModeFor]).
  Future<bool> requestPermissions() async {
    final notificationsGranted = await _android?.requestNotificationsPermission() ?? true;
    await _android?.requestExactAlarmsPermission();
    return notificationsGranted;
  }

  Future<bool> canScheduleExactAlarms() async => await _android?.canScheduleExactNotifications() ?? false;

  Future<AndroidScheduleMode> _scheduleModeFor({required bool exactRequested}) async {
    if (!exactRequested) return AndroidScheduleMode.inexactAllowWhileIdle;
    return await canScheduleExactAlarms() ? AndroidScheduleMode.exactAllowWhileIdle : AndroidScheduleMode.inexactAllowWhileIdle;
  }

  Int64List? _vibrationPattern(VibrationPatternPreset? preset) {
    switch (preset) {
      case null:
        return null;
      case VibrationPatternPreset.standard:
        return null; // Use the channel/system default.
      case VibrationPatternPreset.shortPulse:
        return Int64List.fromList([0, 150, 100, 150]);
      case VibrationPatternPreset.longPulse:
        return Int64List.fromList([0, 800]);
      case VibrationPatternPreset.escalating:
        return Int64List.fromList([0, 150, 150, 250, 150, 400, 150, 600]);
    }
  }

  /// Schedules a single one-off notification at [dateTime] (a specific
  /// calendar instant, not a repeating clock time) -- used for prayer-linked
  /// reminders, whose fire time shifts by a few minutes every day and so
  /// can't be expressed as a repeating "same time daily" rule.
  Future<void> scheduleOneOff({
    required int id,
    required NotificationChannel channel,
    required String title,
    required String body,
    required DateTime dateTime,
    bool exact = true,
    bool fullScreenIntent = false,
    VibrationPatternPreset? vibrationPattern,
    String? payload,
  }) async {
    final scheduled = tz.TZDateTime.from(dateTime, tz.local);
    if (scheduled.isBefore(tz.TZDateTime.now(tz.local))) return;
    await _plugin.zonedSchedule(
      id: id,
      title: title,
      body: body,
      scheduledDate: scheduled,
      payload: payload,
      androidScheduleMode: await _scheduleModeFor(exactRequested: exact),
      notificationDetails: NotificationDetails(
        android: AndroidNotificationDetails(
          channel.id,
          _channelName(channel),
          channelDescription: _channelDescription(channel),
          importance: fullScreenIntent ? Importance.max : Importance.high,
          priority: fullScreenIntent ? Priority.max : Priority.high,
          fullScreenIntent: fullScreenIntent,
          category: fullScreenIntent ? AndroidNotificationCategory.alarm : AndroidNotificationCategory.reminder,
          vibrationPattern: _vibrationPattern(vibrationPattern),
          autoCancel: !fullScreenIntent,
          ongoing: fullScreenIntent,
        ),
      ),
    );
  }

  /// Schedules (or re-arms) a notification that repeats every day at the
  /// same clock time [time] -- used for fixed-time reminders (Adhkar,
  /// Qur'an reading) whose schedule doesn't depend on prayer-time drift.
  Future<void> scheduleDailyRepeat({
    required int id,
    required NotificationChannel channel,
    required String title,
    required String body,
    required TimeOfDay time,
    String? payload,
  }) async {
    final next = _nextInstanceOfTime(time);
    await _plugin.zonedSchedule(
      id: id,
      title: title,
      body: body,
      scheduledDate: next,
      payload: payload,
      androidScheduleMode: await _scheduleModeFor(exactRequested: false),
      matchDateTimeComponents: DateTimeComponents.time,
      notificationDetails: NotificationDetails(
        android: AndroidNotificationDetails(
          channel.id,
          _channelName(channel),
          channelDescription: _channelDescription(channel),
          importance: Importance.defaultImportance,
          priority: Priority.defaultPriority,
        ),
      ),
    );
  }

  /// Schedules a notification that repeats weekly on [weekday]
  /// (1 = Monday .. 7 = Sunday, matching [DateTime.weekday]) at [time] --
  /// used for the Friday (Jumu'ah) reminder, and internally to build
  /// weekday-specific repeat rules (e.g. "weekdays only").
  Future<void> scheduleWeeklyRepeat({
    required int id,
    required NotificationChannel channel,
    required String title,
    required String body,
    required int weekday,
    required TimeOfDay time,
    String? payload,
  }) async {
    var next = _nextInstanceOfTime(time);
    while (next.weekday != weekday) {
      next = next.add(const Duration(days: 1));
    }
    await _plugin.zonedSchedule(
      id: id,
      title: title,
      body: body,
      scheduledDate: next,
      payload: payload,
      androidScheduleMode: await _scheduleModeFor(exactRequested: false),
      matchDateTimeComponents: DateTimeComponents.dayOfWeekAndTime,
      notificationDetails: NotificationDetails(
        android: AndroidNotificationDetails(
          channel.id,
          _channelName(channel),
          channelDescription: _channelDescription(channel),
          importance: Importance.defaultImportance,
          priority: Priority.defaultPriority,
        ),
      ),
    );
  }

  tz.TZDateTime _nextInstanceOfTime(TimeOfDay time) {
    final now = tz.TZDateTime.now(tz.local);
    var scheduled = tz.TZDateTime(tz.local, now.year, now.month, now.day, time.hour, time.minute);
    if (scheduled.isBefore(now)) scheduled = scheduled.add(const Duration(days: 1));
    return scheduled;
  }

  Future<void> cancel(int id) => _plugin.cancel(id: id);

  Future<void> cancelAll() => _plugin.cancelAll();
}
