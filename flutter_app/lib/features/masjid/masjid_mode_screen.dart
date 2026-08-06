import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/models/adhkar_entry.dart';
import '../../core/services/notifications/reminder_scheduler.dart';
import '../../core/services/prayer_settings_controller.dart';
import '../../core/services/prayer_times_service.dart';
import '../../core/services/settings_controller.dart';
import '../adhkar/adhkar_category_screen.dart';

/// A calm, distraction-free screen to hold in hand (or leave running) while
/// praying: no menus, no counters, nothing competing for attention. Sets
/// [SettingsController.masjidMode] true for the duration -- a hook point a
/// future notification system (see docs/21) can check before showing
/// anything non-prayer-related. "Finished Praying" leads straight into the
/// after-Salah adhkar category that already exists in the Adhkar library.
class MasjidModeScreen extends StatefulWidget {
  const MasjidModeScreen({super.key});

  @override
  State<MasjidModeScreen> createState() => _MasjidModeScreenState();
}

class _MasjidModeScreenState extends State<MasjidModeScreen> {
  static const _bg = Color(0xFF0B2545);
  static const _gold = Color(0xFFC9A227);

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<SettingsController>().setMasjidMode(true);
    });
  }

  void _endMasjidMode(BuildContext context) {
    context.read<SettingsController>().setMasjidMode(false);
  }

  /// Best-effort: cancels today's still-pending Iqamah/Missed-Prayer
  /// reminders for whichever prayer most recently started, so tapping
  /// "Finished Praying" doesn't get followed by a reminder for a prayer
  /// the user just prayed. Silently does nothing if location/prayer
  /// settings aren't configured -- Masjid Mode itself doesn't depend on
  /// them, so this is a bonus, not a requirement.
  void _markCurrentPrayerCompleted(BuildContext context) {
    final prayerSettings = context.read<PrayerSettingsController>();
    if (!prayerSettings.hasLocation) return;
    const service = PrayerTimesService();
    final now = DateTime.now();
    final times = service.calculate(
      latitude: prayerSettings.latitude!,
      longitude: prayerSettings.longitude!,
      date: now,
      method: prayerSettings.method,
      madhab: prayerSettings.madhab,
      adjustmentsMinutes: prayerSettings.adjustments,
    );
    PrayerName? current;
    for (final p in [PrayerName.fajr, PrayerName.dhuhr, PrayerName.asr, PrayerName.maghrib, PrayerName.isha]) {
      if (!times.timeFor(p).isAfter(now)) current = p;
    }
    if (current != null) {
      final scheduler = ReminderScheduler(
        prayerSettings: prayerSettings,
        reminderSettings: context.read(),
        quranRepository: context.read(),
        loc: context.loc,
      );
      scheduler.markPrayerCompletedToday(current);
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    return PopScope(
      onPopInvokedWithResult: (didPop, _) {
        if (didPop) _endMasjidMode(context);
      },
      child: Scaffold(
        backgroundColor: _bg,
        body: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.mosque, size: 72, color: _gold),
                const SizedBox(height: 24),
                Text(
                  t('masjid_mode_active_title'),
                  style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.w600),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 12),
                Text(
                  t('masjid_mode_active_body'),
                  style: TextStyle(color: Colors.white.withOpacity(0.75), fontSize: 15),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 48),
                FilledButton.icon(
                  style: FilledButton.styleFrom(backgroundColor: _gold, foregroundColor: Colors.black, padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 16)),
                  icon: const Icon(Icons.check_circle_outline),
                  label: Text(t('masjid_mode_finished_praying')),
                  onPressed: () {
                    _markCurrentPrayerCompleted(context);
                    _endMasjidMode(context);
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(builder: (_) => const AdhkarCategoryScreen(category: AdhkarCategory.prayer)),
                    );
                  },
                ),
                const SizedBox(height: 16),
                TextButton(
                  onPressed: () {
                    _endMasjidMode(context);
                    Navigator.of(context).maybePop();
                  },
                  child: Text(t('masjid_mode_exit'), style: TextStyle(color: Colors.white.withOpacity(0.6))),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
