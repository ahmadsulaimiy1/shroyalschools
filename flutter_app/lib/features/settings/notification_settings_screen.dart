import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/services/notifications/notification_service.dart';
import '../../core/services/notifications/reminder_scheduler.dart';
import '../../core/services/notifications/reminder_settings_controller.dart';
import '../../core/theme/app_colors.dart';

/// Premium control centre for the worship reminder system: Prayer, Tahajjud,
/// Qur'an, Adhkar, Friday, and global behaviour (Quiet Hours, Ramadan Mode).
/// Every change re-primes the actual scheduled notifications immediately via
/// [rescheduleReminders] -- there is no separate "Save" step.
class NotificationSettingsScreen extends StatefulWidget {
  const NotificationSettingsScreen({super.key});

  @override
  State<NotificationSettingsScreen> createState() => _NotificationSettingsScreenState();
}

class _NotificationSettingsScreenState extends State<NotificationSettingsScreen> {
  bool? _notificationsGranted;

  Future<void> _reschedule() => rescheduleReminders(context);

  Future<void> _requestPermissionIfNeeded() async {
    final granted = await NotificationService.instance.requestPermissions();
    if (mounted) setState(() => _notificationsGranted = granted);
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final reminders = context.watch<ReminderSettingsController>();

    return Scaffold(
      appBar: AppBar(title: Text(t('notif_settings_title'))),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 8),
        children: [
          if (_notificationsGranted == false)
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 8),
              child: Card(
                color: AppColors.navy,
                child: ListTile(
                  leading: const Icon(Icons.notifications_off_outlined, color: AppColors.gold),
                  title: Text(t('notif_permission_needed_title'), style: const TextStyle(color: Colors.white)),
                  subtitle: Text(t('notif_permission_needed_body'), style: const TextStyle(color: Colors.white70)),
                  trailing: TextButton(
                    onPressed: _requestPermissionIfNeeded,
                    child: Text(t('notif_permission_enable'), style: const TextStyle(color: AppColors.gold)),
                  ),
                ),
              ),
            ),

          _SectionHeader(t('notif_section_prayer')),
          SwitchListTile(
            secondary: const Icon(Icons.volume_up_outlined),
            title: Text(t('notif_prayer_adhan')),
            subtitle: Text(t('notif_prayer_adhan_subtitle')),
            value: reminders.adhanEnabled,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v);
              await reminders.setAdhanEnabled(v);
              await _reschedule();
            },
          ),
          ListTile(
            leading: const Icon(Icons.alarm_outlined),
            title: Text(t('notif_prayer_early')),
            subtitle: Text(_minutesLabel(t, reminders.earlyReminderMinutes)),
            onTap: () => _pickMinutes(
              title: t('notif_prayer_early'),
              current: reminders.earlyReminderMinutes,
              options: const [null, 5, 10, 15, 20, 30],
              onPicked: (v) async {
                if (v != null) await _requestPermissionIfNeededOnEnable(true);
                await reminders.setEarlyReminderMinutes(v);
                await _reschedule();
              },
            ),
          ),
          ListTile(
            leading: const Icon(Icons.groups_outlined),
            title: Text(t('notif_prayer_iqamah')),
            subtitle: Text(_minutesLabel(t, reminders.iqamahReminderMinutes)),
            onTap: () => _pickMinutes(
              title: t('notif_prayer_iqamah'),
              current: reminders.iqamahReminderMinutes,
              options: const [null, 5, 10, 15, 20, 30],
              onPicked: (v) async {
                if (v != null) await _requestPermissionIfNeededOnEnable(true);
                await reminders.setIqamahReminderMinutes(v);
                await _reschedule();
              },
            ),
          ),
          SwitchListTile(
            secondary: const Icon(Icons.history_toggle_off),
            title: Text(t('notif_prayer_missed')),
            subtitle: Text(t('notif_prayer_missed_subtitle')),
            value: reminders.missedPrayerEnabled,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v);
              await reminders.setMissedPrayerEnabled(v);
              await _reschedule();
            },
          ),

          const Divider(height: 24),
          _SectionHeader(t('notif_section_tahajjud')),
          SwitchListTile(
            secondary: const Icon(Icons.bedtime_outlined),
            title: Text(t('notif_tahajjud_enable')),
            subtitle: Text(t('notif_tahajjud_enable_subtitle')),
            value: reminders.tahajjud.enabled,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v);
              await reminders.setTahajjud(reminders.tahajjud.copyWith(enabled: v));
              await _reschedule();
            },
          ),
          if (reminders.tahajjud.enabled) ...[
            SwitchListTile(
              secondary: const Icon(Icons.auto_awesome_outlined),
              title: Text(t('notif_tahajjud_smart_time')),
              subtitle: Text(t('notif_tahajjud_smart_time_subtitle')),
              value: reminders.tahajjud.useSmartTime,
              onChanged: (v) async {
                await reminders.setTahajjud(reminders.tahajjud.copyWith(useSmartTime: v));
                await _reschedule();
              },
            ),
            if (!reminders.tahajjud.useSmartTime)
              ListTile(
                leading: const Icon(Icons.access_time),
                title: Text(t('notif_tahajjud_manual_time')),
                subtitle: Text(reminders.tahajjud.manualTime.format(context)),
                onTap: () async {
                  final picked = await showTimePicker(context: context, initialTime: reminders.tahajjud.manualTime);
                  if (picked == null) return;
                  await reminders.setTahajjud(reminders.tahajjud.copyWith(manualTime: picked));
                  await _reschedule();
                },
              ),
            ListTile(
              leading: const Icon(Icons.nightlight_round),
              title: Text(t('notif_tahajjud_wake_style')),
              subtitle: Text(reminders.tahajjud.wakeStyle == TahajjudWakeStyle.strong
                  ? t('notif_tahajjud_wake_strong')
                  : t('notif_tahajjud_wake_gentle')),
              onTap: () => _pickWakeStyle(reminders),
            ),
            SwitchListTile(
              secondary: const Icon(Icons.trending_up),
              title: Text(t('notif_tahajjud_escalating')),
              subtitle: Text(context.loc.tArgs('notif_tahajjud_escalating_subtitle', [reminders.tahajjud.headsUpMinutesBefore])),
              value: reminders.tahajjud.escalatingReminders,
              onChanged: (v) async {
                await reminders.setTahajjud(reminders.tahajjud.copyWith(escalatingReminders: v));
                await _reschedule();
              },
            ),
            ListTile(
              leading: const Icon(Icons.filter_9_plus_outlined),
              title: Text(t('notif_tahajjud_alarm_count')),
              subtitle: Text(context.loc.tArgs('notif_tahajjud_alarm_count_subtitle', [reminders.tahajjud.alarmCount])),
              trailing: SizedBox(
                width: 120,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    IconButton(
                      icon: const Icon(Icons.remove_circle_outline),
                      onPressed: reminders.tahajjud.alarmCount <= 1
                          ? null
                          : () async {
                              await reminders.setTahajjud(reminders.tahajjud.copyWith(alarmCount: reminders.tahajjud.alarmCount - 1));
                              await _reschedule();
                            },
                    ),
                    IconButton(
                      icon: const Icon(Icons.add_circle_outline),
                      onPressed: reminders.tahajjud.alarmCount >= 4
                          ? null
                          : () async {
                              await reminders.setTahajjud(reminders.tahajjud.copyWith(alarmCount: reminders.tahajjud.alarmCount + 1));
                              await _reschedule();
                            },
                    ),
                  ],
                ),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.vibration),
              title: Text(t('notif_tahajjud_vibration')),
              subtitle: Text(_vibrationLabel(t, reminders.tahajjud.vibrationPattern)),
              onTap: () => _pickVibrationPattern(reminders),
            ),
          ],

          const Divider(height: 24),
          _SectionHeader(t('notif_section_quran')),
          _TimeReminderTile(
            icon: Icons.menu_book_outlined,
            title: t('notif_quran_reading'),
            reminder: reminders.quranReading,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v.enabled);
              await reminders.setQuranReading(v);
              await _reschedule();
            },
          ),
          _TimeReminderTile(
            icon: Icons.flag_outlined,
            title: t('notif_quran_khatm'),
            reminder: reminders.quranKhatm,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v.enabled);
              await reminders.setQuranKhatm(v);
              await _reschedule();
            },
          ),
          _TimeReminderTile(
            icon: Icons.psychology_outlined,
            title: t('notif_quran_memorisation'),
            reminder: reminders.quranMemorisation,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v.enabled);
              await reminders.setQuranMemorisation(v);
              await _reschedule();
            },
          ),

          const Divider(height: 24),
          _SectionHeader(t('notif_section_adhkar')),
          _TimeReminderTile(
            icon: Icons.wb_sunny_outlined,
            title: t('notif_adhkar_morning'),
            reminder: reminders.adhkarMorning,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v.enabled);
              await reminders.setAdhkarMorning(v);
              await _reschedule();
            },
          ),
          _TimeReminderTile(
            icon: Icons.wb_twilight_outlined,
            title: t('notif_adhkar_evening'),
            reminder: reminders.adhkarEvening,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v.enabled);
              await reminders.setAdhkarEvening(v);
              await _reschedule();
            },
          ),
          _TimeReminderTile(
            icon: Icons.bedtime_outlined,
            title: t('notif_adhkar_sleep'),
            reminder: reminders.adhkarSleep,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v.enabled);
              await reminders.setAdhkarSleep(v);
              await _reschedule();
            },
          ),
          _TimeReminderTile(
            icon: Icons.luggage_outlined,
            title: t('notif_adhkar_travel'),
            reminder: reminders.adhkarTravel,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v.enabled);
              await reminders.setAdhkarTravel(v);
              await _reschedule();
            },
          ),

          const Divider(height: 24),
          _SectionHeader(t('notif_section_friday')),
          SwitchListTile(
            secondary: const Icon(Icons.mosque_outlined),
            title: Text(t('notif_friday_enable')),
            subtitle: Text(context.loc.tArgs('notif_friday_subtitle', [reminders.fridayMinutesBefore])),
            value: reminders.fridayEnabled,
            onChanged: (v) async {
              await _requestPermissionIfNeededOnEnable(v);
              await reminders.setFridayEnabled(v);
              await _reschedule();
            },
          ),

          const Divider(height: 24),
          _SectionHeader(t('notif_section_behaviour')),
          SwitchListTile(
            secondary: const Icon(Icons.do_not_disturb_on_outlined),
            title: Text(t('notif_quiet_hours')),
            subtitle: Text(reminders.quietHours.enabled
                ? context.loc.tArgs('notif_quiet_hours_subtitle', [reminders.quietHours.start.format(context), reminders.quietHours.end.format(context)])
                : t('notif_quiet_hours_off')),
            value: reminders.quietHours.enabled,
            onChanged: (v) async {
              await reminders.setQuietHours(reminders.quietHours.copyWith(enabled: v));
              await _reschedule();
            },
          ),
          if (reminders.quietHours.enabled)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () async {
                        final picked = await showTimePicker(context: context, initialTime: reminders.quietHours.start);
                        if (picked == null) return;
                        await reminders.setQuietHours(reminders.quietHours.copyWith(start: picked));
                        await _reschedule();
                      },
                      child: Text('${t('notif_quiet_hours_start')}: ${reminders.quietHours.start.format(context)}'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () async {
                        final picked = await showTimePicker(context: context, initialTime: reminders.quietHours.end);
                        if (picked == null) return;
                        await reminders.setQuietHours(reminders.quietHours.copyWith(end: picked));
                        await _reschedule();
                      },
                      child: Text('${t('notif_quiet_hours_end')}: ${reminders.quietHours.end.format(context)}'),
                    ),
                  ),
                ],
              ),
            ),
          SwitchListTile(
            secondary: const Icon(Icons.nights_stay_outlined),
            title: Text(t('notif_ramadan_mode')),
            subtitle: Text(t('notif_ramadan_mode_subtitle')),
            value: reminders.ramadanModeEnabled,
            onChanged: (v) => reminders.setRamadanModeEnabled(v),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(
              t('notif_settings_footnote'),
              style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Theme.of(context).colorScheme.onSurfaceVariant),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _requestPermissionIfNeededOnEnable(bool enabling) async {
    if (!enabling) return;
    final granted = await NotificationService.instance.requestPermissions();
    if (mounted) setState(() => _notificationsGranted = granted);
  }

  String _minutesLabel(String Function(String) t, int? minutes) =>
      minutes == null ? t('notif_off') : context.loc.tArgs('notif_minutes_before', [minutes]);

  String _vibrationLabel(String Function(String) t, VibrationPatternPreset preset) => switch (preset) {
        VibrationPatternPreset.standard => t('notif_vibration_standard'),
        VibrationPatternPreset.shortPulse => t('notif_vibration_short_pulse'),
        VibrationPatternPreset.longPulse => t('notif_vibration_long_pulse'),
        VibrationPatternPreset.escalating => t('notif_vibration_escalating'),
      };

  void _pickMinutes({
    required String title,
    required int? current,
    required List<int?> options,
    required ValueChanged<int?> onPicked,
  }) {
    final t = context.loc.t;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (sheetContext) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Padding(padding: const EdgeInsets.fromLTRB(20, 16, 20, 4), child: Align(alignment: Alignment.centerLeft, child: Text(title, style: Theme.of(sheetContext).textTheme.titleMedium))),
            for (final option in options)
              RadioListTile<int?>(
                value: option,
                groupValue: current,
                title: Text(_minutesLabel(t, option)),
                onChanged: (v) {
                  onPicked(v);
                  Navigator.pop(sheetContext);
                },
              ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }

  void _pickWakeStyle(ReminderSettingsController reminders) {
    final t = context.loc.t;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (sheetContext) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            RadioListTile<TahajjudWakeStyle>(
              value: TahajjudWakeStyle.gentle,
              groupValue: reminders.tahajjud.wakeStyle,
              title: Text(t('notif_tahajjud_wake_gentle')),
              subtitle: Text(t('notif_tahajjud_wake_gentle_subtitle')),
              onChanged: (v) async {
                Navigator.pop(sheetContext);
                await reminders.setTahajjud(reminders.tahajjud.copyWith(wakeStyle: v));
                await _reschedule();
              },
            ),
            RadioListTile<TahajjudWakeStyle>(
              value: TahajjudWakeStyle.strong,
              groupValue: reminders.tahajjud.wakeStyle,
              title: Text(t('notif_tahajjud_wake_strong')),
              subtitle: Text(t('notif_tahajjud_wake_strong_subtitle')),
              onChanged: (v) async {
                Navigator.pop(sheetContext);
                if (v != null) await NotificationService.instance.requestPermissions();
                await reminders.setTahajjud(reminders.tahajjud.copyWith(wakeStyle: v));
                await _reschedule();
              },
            ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }

  void _pickVibrationPattern(ReminderSettingsController reminders) {
    final t = context.loc.t;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (sheetContext) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            for (final preset in VibrationPatternPreset.values)
              RadioListTile<VibrationPatternPreset>(
                value: preset,
                groupValue: reminders.tahajjud.vibrationPattern,
                title: Text(_vibrationLabel(t, preset)),
                onChanged: (v) async {
                  Navigator.pop(sheetContext);
                  if (v == null) return;
                  await reminders.setTahajjud(reminders.tahajjud.copyWith(vibrationPattern: v));
                  await _reschedule();
                },
              ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  const _SectionHeader(this.label);
  final String label;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
      child: Text(label, style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.secondary)),
    );
  }
}

/// A switch + tap-to-configure row for a [TimeReminder]: toggling shows/
/// hides a time + repeat-rule row beneath it.
class _TimeReminderTile extends StatelessWidget {
  const _TimeReminderTile({required this.icon, required this.title, required this.reminder, required this.onChanged});

  final IconData icon;
  final String title;
  final TimeReminder reminder;
  final ValueChanged<TimeReminder> onChanged;

  String _repeatLabel(String Function(String) t, ReminderRepeatRule rule) => switch (rule) {
        ReminderRepeatRule.daily => t('notif_repeat_daily'),
        ReminderRepeatRule.weekdays => t('notif_repeat_weekdays'),
        ReminderRepeatRule.weekends => t('notif_repeat_weekends'),
        ReminderRepeatRule.custom => t('notif_repeat_custom'),
      };

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    return Column(
      children: [
        SwitchListTile(
          secondary: Icon(icon),
          title: Text(title),
          subtitle: Text(reminder.enabled ? reminder.time.format(context) : t('notif_off')),
          value: reminder.enabled,
          onChanged: (v) => onChanged(reminder.copyWith(enabled: v)),
        ),
        if (reminder.enabled)
          Padding(
            padding: const EdgeInsets.only(left: 56, right: 16, bottom: 8),
            child: Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    icon: const Icon(Icons.access_time, size: 18),
                    label: Text(reminder.time.format(context)),
                    onPressed: () async {
                      final picked = await showTimePicker(context: context, initialTime: reminder.time);
                      if (picked == null) return;
                      onChanged(reminder.copyWith(time: picked));
                    },
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: OutlinedButton(
                    onPressed: () => _pickRepeatRule(context),
                    child: Text(_repeatLabel(t, reminder.repeatRule)),
                  ),
                ),
              ],
            ),
          ),
      ],
    );
  }

  void _pickRepeatRule(BuildContext context) {
    final t = context.loc.t;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (sheetContext) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            for (final rule in ReminderRepeatRule.values)
              RadioListTile<ReminderRepeatRule>(
                value: rule,
                groupValue: reminder.repeatRule,
                title: Text(_repeatLabel(t, rule)),
                onChanged: (v) {
                  Navigator.pop(sheetContext);
                  if (v == null) return;
                  if (v == ReminderRepeatRule.custom) {
                    _pickCustomDays(context);
                  } else {
                    onChanged(reminder.copyWith(repeatRule: v));
                  }
                },
              ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }

  void _pickCustomDays(BuildContext context) {
    final t = context.loc.t;
    var selected = {...reminder.customDays};
    if (selected.isEmpty) selected = {1, 2, 3, 4, 5, 6, 7};
    const dayKeys = ['notif_day_mon', 'notif_day_tue', 'notif_day_wed', 'notif_day_thu', 'notif_day_fri', 'notif_day_sat', 'notif_day_sun'];
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (sheetContext) => StatefulBuilder(
        builder: (sheetContext, setSheetState) => SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              for (var i = 0; i < 7; i++)
                CheckboxListTile(
                  value: selected.contains(i + 1),
                  title: Text(t(dayKeys[i])),
                  onChanged: (checked) => setSheetState(() {
                    if (checked == true) {
                      selected.add(i + 1);
                    } else {
                      selected.remove(i + 1);
                    }
                  }),
                ),
              Padding(
                padding: const EdgeInsets.all(16),
                child: FilledButton(
                  onPressed: () {
                    Navigator.pop(sheetContext);
                    onChanged(reminder.copyWith(repeatRule: ReminderRepeatRule.custom, customDays: selected));
                  },
                  child: Text(t('save')),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
