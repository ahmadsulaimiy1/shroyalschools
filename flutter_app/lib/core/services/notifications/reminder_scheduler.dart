import 'package:adhan_dart/adhan_dart.dart' show SunnahTimes, PrayerTimes, Coordinates, Madhab;
import 'package:flutter/material.dart' show BuildContext, TimeOfDay;
import 'package:provider/provider.dart';

import '../../database/quran_repository.dart';
import '../../localization/app_localizations.dart';
import '../hijri_calendar_service.dart';
import '../prayer_settings_controller.dart';
import '../prayer_times_service.dart';
import 'notification_channels.dart';
import 'notification_service.dart';
import 'reminder_settings_controller.dart';

/// How many days ahead prayer-linked (and Tahajjud smart-time) reminders are
/// scheduled. These shift by a few minutes daily so, unlike the fixed-clock
/// Adhkar/Qur'an reminders, they can't be expressed as a single repeating
/// rule -- they're re-generated as a rolling window instead. Known
/// limitation: if the app is not opened for longer than this window, prayer
/// reminders stop until the next launch re-primes them (see docs/27) --
/// there is no background daily trigger in this build without adding a
/// separate WorkManager-style plugin.
const int _rollingWindowDays = 10;

/// Orchestrates the worship reminder system: reads [PrayerSettingsController]
/// + [ReminderSettingsController] + [HijriCalendarService] and turns them
/// into concrete scheduled notifications via [NotificationService]. This is
/// the only class that decides *what* to schedule; [NotificationService]
/// only knows *how*.
class ReminderScheduler {
  const ReminderScheduler({
    required this.prayerSettings,
    required this.reminderSettings,
    required this.quranRepository,
    required this.loc,
  });

  final PrayerSettingsController prayerSettings;
  final ReminderSettingsController reminderSettings;
  final QuranRepository quranRepository;
  final AppLocalizations loc;

  static const _prayerTimesService = PrayerTimesService();
  static const _hijriService = HijriCalendarService();

  /// Recomputes and re-schedules every reminder from scratch. Idempotent --
  /// safe to call on every app launch, whenever prayer settings change,
  /// and whenever reminder settings change. Cancels nothing that isn't
  /// being replaced, so stale one-offs from a shortened window are simply
  /// overwritten by new schedule calls sharing the same deterministic id.
  Future<void> rescheduleAll() async {
    await _scheduleFixedReminders();
    if (prayerSettings.hasLocation) {
      await _schedulePrayerLinkedReminders();
    }
  }

  // ---------------------------------------------------------------------
  // Fixed-clock-time reminders (Adhkar, Qur'an reading/khatm/memorisation,
  // Friday) -- these don't depend on location/prayer times at all.
  // ---------------------------------------------------------------------

  Future<void> _scheduleFixedReminders() async {
    await _scheduleTimeReminder(
      reminder: reminderSettings.adhkarMorning,
      kind: _Kind.adhkarMorning,
      channel: NotificationChannels.adhkarMorning,
      titleKey: 'notif_title_adhkar_morning',
      bodyKey: 'notif_body_adhkar_morning',
    );
    await _scheduleTimeReminder(
      reminder: reminderSettings.adhkarEvening,
      kind: _Kind.adhkarEvening,
      channel: NotificationChannels.adhkarEvening,
      titleKey: 'notif_title_adhkar_evening',
      bodyKey: 'notif_body_adhkar_evening',
    );
    await _scheduleTimeReminder(
      reminder: reminderSettings.adhkarSleep,
      kind: _Kind.adhkarSleep,
      channel: NotificationChannels.adhkarSleep,
      titleKey: 'notif_title_adhkar_sleep',
      bodyKey: 'notif_body_adhkar_sleep',
    );
    await _scheduleTimeReminder(
      reminder: reminderSettings.adhkarTravel,
      kind: _Kind.adhkarTravel,
      channel: NotificationChannels.adhkarTravel,
      titleKey: 'notif_title_adhkar_travel',
      bodyKey: 'notif_body_adhkar_travel',
    );
    await _scheduleTimeReminder(
      reminder: reminderSettings.quranReading,
      kind: _Kind.quranReading,
      channel: NotificationChannels.quranReading,
      titleKey: 'notif_title_quran_reading',
      bodyKey: 'notif_body_quran_reading',
    );
    await _scheduleTimeReminder(
      reminder: reminderSettings.quranMemorisation,
      kind: _Kind.quranMemorisation,
      channel: NotificationChannels.quranMemorisation,
      titleKey: 'notif_title_quran_memorisation',
      bodyKey: 'notif_body_quran_memorisation',
    );

    if (reminderSettings.quranKhatm.enabled) {
      final plan = await quranRepository.khatmPlan();
      String body = loc.t('notif_body_quran_khatm');
      if (plan != null) {
        final today = DateTime.now();
        final versesSinceStart = await quranRepository.versesReadSince(plan.startDate);
        final versesRemaining = (totalQuranVerseCount - versesSinceStart).clamp(0, totalQuranVerseCount);
        final daysRemaining = plan.targetDate.difference(DateTime(today.year, today.month, today.day)).inDays.clamp(1, 999999);
        final dailyTarget = (versesRemaining / daysRemaining).ceil();
        body = loc.tArgs('notif_body_quran_khatm_target', [dailyTarget]);
      }
      await _scheduleTimeReminder(
        reminder: reminderSettings.quranKhatm,
        kind: _Kind.quranKhatm,
        channel: NotificationChannels.quranKhatm,
        titleKey: 'notif_title_quran_khatm',
        bodyKey: null,
        bodyOverride: body,
      );
    } else {
      await _cancelRepeatingSet(_Kind.quranKhatm, {1, 2, 3, 4, 5, 6, 7});
    }

    if (reminderSettings.fridayEnabled) {
      final fridayTime = _subtractMinutes(const TimeOfDay(hour: 13, minute: 0), reminderSettings.fridayMinutesBefore);
      await NotificationService.instance.scheduleWeeklyRepeat(
        id: _id(_Kind.fridayJumuah, weekday: DateTime.friday),
        channel: NotificationChannels.friday,
        title: loc.t('notif_title_friday'),
        body: loc.t('notif_body_friday'),
        weekday: DateTime.friday,
        time: fridayTime,
      );
    } else {
      await NotificationService.instance.cancel(_id(_Kind.fridayJumuah, weekday: DateTime.friday));
    }
  }

  Future<void> _scheduleTimeReminder({
    required TimeReminder reminder,
    required _Kind kind,
    required NotificationChannel channel,
    required String titleKey,
    String? bodyKey,
    String? bodyOverride,
  }) async {
    // Always clear every previous shape for this kind first (daily id +
    // all seven weekday ids) so switching repeat rules doesn't leave a
    // stale notification behind under the old id.
    await NotificationService.instance.cancel(_dailyId(kind));
    for (var wd = 1; wd <= 7; wd++) {
      await NotificationService.instance.cancel(_id(kind, weekday: wd));
    }
    if (!reminder.enabled) return;

    final title = loc.t(titleKey);
    final body = bodyOverride ?? loc.t(bodyKey!);

    switch (reminder.repeatRule) {
      case ReminderRepeatRule.daily:
        await NotificationService.instance.scheduleDailyRepeat(
          id: _dailyId(kind),
          channel: channel,
          title: title,
          body: body,
          time: reminder.time,
        );
      case ReminderRepeatRule.weekdays:
        for (var wd = DateTime.monday; wd <= DateTime.friday; wd++) {
          await NotificationService.instance.scheduleWeeklyRepeat(
            id: _id(kind, weekday: wd),
            channel: channel,
            title: title,
            body: body,
            weekday: wd,
            time: reminder.time,
          );
        }
      case ReminderRepeatRule.weekends:
        for (final wd in [DateTime.saturday, DateTime.sunday]) {
          await NotificationService.instance.scheduleWeeklyRepeat(
            id: _id(kind, weekday: wd),
            channel: channel,
            title: title,
            body: body,
            weekday: wd,
            time: reminder.time,
          );
        }
      case ReminderRepeatRule.custom:
        for (final wd in reminder.customDays) {
          await NotificationService.instance.scheduleWeeklyRepeat(
            id: _id(kind, weekday: wd),
            channel: channel,
            title: title,
            body: body,
            weekday: wd,
            time: reminder.time,
          );
        }
    }
  }

  Future<void> _cancelRepeatingSet(_Kind kind, Set<int> weekdays) async {
    await NotificationService.instance.cancel(_dailyId(kind));
    for (final wd in weekdays) {
      await NotificationService.instance.cancel(_id(kind, weekday: wd));
    }
  }

  // ---------------------------------------------------------------------
  // Prayer-linked reminders (Adhan, early, iqamah, missed) + Tahajjud --
  // computed per-day for a rolling window since prayer times drift daily.
  // ---------------------------------------------------------------------

  Future<void> _schedulePrayerLinkedReminders() async {
    final today = DateTime.now();
    final currentHijriMonth = _hijriService.toHijri(today).month;
    final isRamadan = currentHijriMonth == 9;

    for (var offset = 0; offset < _rollingWindowDays; offset++) {
      final date = DateTime(today.year, today.month, today.day + offset);
      final times = _prayerTimesService.calculate(
        latitude: prayerSettings.latitude!,
        longitude: prayerSettings.longitude!,
        date: date,
        method: prayerSettings.method,
        madhab: prayerSettings.madhab,
        adjustmentsMinutes: prayerSettings.adjustments,
      );

      for (final prayer in [PrayerName.fajr, PrayerName.dhuhr, PrayerName.asr, PrayerName.maghrib, PrayerName.isha]) {
        final prayerTime = times.timeFor(prayer);
        final dayOfYear = _dayOfYear(date);

        if (reminderSettings.adhanEnabled) {
          await NotificationService.instance.scheduleOneOff(
            id: _id(_kindForAdhan(prayer), dayOfYear: dayOfYear),
            channel: NotificationChannels.prayerAdhan,
            title: loc.tArgs('notif_title_prayer_adhan', [_prayerLabel(prayer)]),
            body: loc.t('notif_body_prayer_adhan'),
            dateTime: prayerTime,
          );
        } else {
          await NotificationService.instance.cancel(_id(_kindForAdhan(prayer), dayOfYear: dayOfYear));
        }

        if (reminderSettings.earlyReminderMinutes != null) {
          await NotificationService.instance.scheduleOneOff(
            id: _id(_kindForEarly(prayer), dayOfYear: dayOfYear),
            channel: NotificationChannels.prayerEarly,
            title: loc.tArgs('notif_title_prayer_early', [_prayerLabel(prayer)]),
            body: loc.tArgs('notif_body_prayer_early', [reminderSettings.earlyReminderMinutes!]),
            dateTime: prayerTime.subtract(Duration(minutes: reminderSettings.earlyReminderMinutes!)),
            exact: false,
          );
        } else {
          await NotificationService.instance.cancel(_id(_kindForEarly(prayer), dayOfYear: dayOfYear));
        }

        if (reminderSettings.iqamahReminderMinutes != null) {
          await NotificationService.instance.scheduleOneOff(
            id: _id(_kindForIqamah(prayer), dayOfYear: dayOfYear),
            channel: NotificationChannels.prayerIqamah,
            title: loc.tArgs('notif_title_prayer_iqamah', [_prayerLabel(prayer)]),
            body: loc.t('notif_body_prayer_iqamah'),
            dateTime: prayerTime.add(Duration(minutes: reminderSettings.iqamahReminderMinutes!)),
            exact: false,
          );
        } else {
          await NotificationService.instance.cancel(_id(_kindForIqamah(prayer), dayOfYear: dayOfYear));
        }

        if (reminderSettings.missedPrayerEnabled) {
          await NotificationService.instance.scheduleOneOff(
            id: _id(_kindForMissed(prayer), dayOfYear: dayOfYear),
            channel: NotificationChannels.prayerMissed,
            title: loc.tArgs('notif_title_prayer_missed', [_prayerLabel(prayer)]),
            body: loc.t('notif_body_prayer_missed'),
            dateTime: prayerTime.add(Duration(minutes: reminderSettings.missedPrayerDelayMinutes)),
            exact: false,
          );
        } else {
          await NotificationService.instance.cancel(_id(_kindForMissed(prayer), dayOfYear: dayOfYear));
        }
      }

      await _scheduleTahajjudForNight(date, times, isRamadan: isRamadan);
    }
  }

  Future<void> _scheduleTahajjudForNight(DateTime date, DailyPrayerTimes times, {required bool isRamadan}) async {
    final t = reminderSettings.tahajjud;
    final dayOfYear = _dayOfYear(date);

    final ids = [
      _id(_Kind.tahajjudHeadsUp, dayOfYear: dayOfYear),
      for (var i = 0; i < 4; i++) _id(_Kind.tahajjudAlarm, dayOfYear: dayOfYear, extra: i),
    ];
    if (!t.enabled) {
      for (final id in ids) {
        await NotificationService.instance.cancel(id);
      }
      return;
    }

    DateTime wakeTime;
    if (t.useSmartTime) {
      final coordinates = Coordinates(prayerSettings.latitude!, prayerSettings.longitude!);
      final params = prayerSettings.method.build()..madhab = prayerSettings.madhab == PrayerAsrMadhab.hanafi ? Madhab.hanafi : Madhab.shafi;
      final adhanPrayerTimes = PrayerTimes(coordinates: coordinates, date: date, calculationParameters: params, precision: true);
      wakeTime = SunnahTimes(adhanPrayerTimes).lastThirdOfTheNight.toLocal();
    } else {
      wakeTime = DateTime(date.year, date.month, date.day, t.manualTime.hour, t.manualTime.minute);
      // A manual Tahajjud time is virtually always meant for "the small
      // hours of the *next* calendar day" (e.g. 3:30 AM) relative to the
      // night that starts on [date]'s evening.
      wakeTime = wakeTime.add(const Duration(days: 1));
    }

    final channel = t.wakeStyle == TahajjudWakeStyle.strong ? NotificationChannels.tahajjudStrong : NotificationChannels.tahajjudGentle;
    final isRamadanSuffix = isRamadan ? loc.t('notif_body_tahajjud_ramadan_suffix') : '';

    if (t.escalatingReminders) {
      await NotificationService.instance.scheduleOneOff(
        id: _id(_Kind.tahajjudHeadsUp, dayOfYear: dayOfYear),
        channel: NotificationChannels.tahajjudGentle,
        title: loc.t('notif_title_tahajjud_heads_up'),
        body: loc.t('notif_body_tahajjud_heads_up'),
        dateTime: wakeTime.subtract(Duration(minutes: t.headsUpMinutesBefore)),
        exact: false,
      );
    } else {
      await NotificationService.instance.cancel(_id(_Kind.tahajjudHeadsUp, dayOfYear: dayOfYear));
    }

    for (var i = 0; i < 4; i++) {
      final id = _id(_Kind.tahajjudAlarm, dayOfYear: dayOfYear, extra: i);
      if (i < t.alarmCount) {
        await NotificationService.instance.scheduleOneOff(
          id: id,
          channel: channel,
          title: loc.t('notif_title_tahajjud'),
          body: '${loc.t('notif_body_tahajjud')}$isRamadanSuffix',
          dateTime: wakeTime.add(Duration(minutes: 10 * i)),
          fullScreenIntent: t.wakeStyle == TahajjudWakeStyle.strong,
          vibrationPattern: t.vibrationPattern,
        );
      } else {
        await NotificationService.instance.cancel(id);
      }
    }
  }

  /// Cancels today's still-pending Iqamah and Missed-Prayer reminders for
  /// [prayer] -- called when the user marks a prayer as completed (Masjid
  /// Mode's "Finished Praying"), so a reminder never fires for a prayer the
  /// user has already prayed. Deliberately does not cancel the Adhan itself
  /// (that already happened) or Early reminder (already served its purpose).
  Future<void> markPrayerCompletedToday(PrayerName prayer) async {
    final dayOfYear = _dayOfYear(DateTime.now());
    await NotificationService.instance.cancel(_id(_kindForIqamah(prayer), dayOfYear: dayOfYear));
    await NotificationService.instance.cancel(_id(_kindForMissed(prayer), dayOfYear: dayOfYear));
  }

  String _prayerLabel(PrayerName p) => switch (p) {
        PrayerName.fajr => loc.t('prayer_fajr'),
        PrayerName.sunrise => loc.t('prayer_sunrise'),
        PrayerName.dhuhr => loc.t('prayer_dhuhr'),
        PrayerName.asr => loc.t('prayer_asr'),
        PrayerName.maghrib => loc.t('prayer_maghrib'),
        PrayerName.isha => loc.t('prayer_isha'),
      };

  TimeOfDay _subtractMinutes(TimeOfDay time, int minutes) {
    final total = (time.hour * 60 + time.minute - minutes) % (24 * 60);
    final normalised = total < 0 ? total + 24 * 60 : total;
    return TimeOfDay(hour: normalised ~/ 60, minute: normalised % 60);
  }

  int _dayOfYear(DateTime date) => date.difference(DateTime(date.year, 1, 1)).inDays + 1;

  _Kind _kindForAdhan(PrayerName p) => switch (p) {
        PrayerName.fajr => _Kind.fajrAdhan,
        PrayerName.dhuhr => _Kind.dhuhrAdhan,
        PrayerName.asr => _Kind.asrAdhan,
        PrayerName.maghrib => _Kind.maghribAdhan,
        PrayerName.isha => _Kind.ishaAdhan,
        PrayerName.sunrise => throw ArgumentError('Sunrise has no Adhan'),
      };

  _Kind _kindForEarly(PrayerName p) => switch (p) {
        PrayerName.fajr => _Kind.fajrEarly,
        PrayerName.dhuhr => _Kind.dhuhrEarly,
        PrayerName.asr => _Kind.asrEarly,
        PrayerName.maghrib => _Kind.maghribEarly,
        PrayerName.isha => _Kind.ishaEarly,
        PrayerName.sunrise => throw ArgumentError('Sunrise has no early reminder'),
      };

  _Kind _kindForIqamah(PrayerName p) => switch (p) {
        PrayerName.fajr => _Kind.fajrIqamah,
        PrayerName.dhuhr => _Kind.dhuhrIqamah,
        PrayerName.asr => _Kind.asrIqamah,
        PrayerName.maghrib => _Kind.maghribIqamah,
        PrayerName.isha => _Kind.ishaIqamah,
        PrayerName.sunrise => throw ArgumentError('Sunrise has no Iqamah'),
      };

  _Kind _kindForMissed(PrayerName p) => switch (p) {
        PrayerName.fajr => _Kind.fajrMissed,
        PrayerName.dhuhr => _Kind.dhuhrMissed,
        PrayerName.asr => _Kind.asrMissed,
        PrayerName.maghrib => _Kind.maghribMissed,
        PrayerName.isha => _Kind.ishaMissed,
        PrayerName.sunrise => throw ArgumentError('Sunrise has no missed-prayer reminder'),
      };

  /// Deterministic notification id for a date-scoped one-off: distinct per
  /// (kind, day-of-year, extra-alarm-index), stable across reschedule runs
  /// so re-scheduling the same day overwrites rather than duplicates.
  int _id(_Kind kind, {int? dayOfYear, int? weekday, int extra = 0}) {
    final slot = dayOfYear ?? (weekday != null ? 900 + weekday : 0);
    return kind.index * 10000 + slot * 10 + extra;
  }

  int _dailyId(_Kind kind) => 800000 + kind.index;
}

enum _Kind {
  fajrAdhan,
  dhuhrAdhan,
  asrAdhan,
  maghribAdhan,
  ishaAdhan,
  fajrEarly,
  dhuhrEarly,
  asrEarly,
  maghribEarly,
  ishaEarly,
  fajrIqamah,
  dhuhrIqamah,
  asrIqamah,
  maghribIqamah,
  ishaIqamah,
  fajrMissed,
  dhuhrMissed,
  asrMissed,
  maghribMissed,
  ishaMissed,
  fridayJumuah,
  tahajjudHeadsUp,
  tahajjudAlarm,
  quranReading,
  quranKhatm,
  quranMemorisation,
  adhkarMorning,
  adhkarEvening,
  adhkarSleep,
  adhkarTravel,
}

/// Builds a [ReminderScheduler] from whatever's registered on [context] and
/// recomputes every scheduled reminder. Called after app launch and after
/// any change to prayer or reminder settings -- see notification_service.dart
/// and docs/27 for why this rolling-recompute approach was chosen over a
/// true background daily trigger.
Future<void> rescheduleReminders(BuildContext context) async {
  final scheduler = ReminderScheduler(
    prayerSettings: context.read<PrayerSettingsController>(),
    reminderSettings: context.read<ReminderSettingsController>(),
    quranRepository: context.read<QuranRepository>(),
    loc: AppLocalizations.of(context),
  );
  await scheduler.rescheduleAll();
}
