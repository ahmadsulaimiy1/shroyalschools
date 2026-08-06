import 'dart:async';

import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/services/notifications/reminder_scheduler.dart';
import '../../core/services/prayer_settings_controller.dart';
import '../../core/services/prayer_times_service.dart';
import '../../core/theme/app_colors.dart';

enum _LoadState { locating, noPermission, noService, error, ready }

/// Prayer & Solar Times centre: today's five prayers plus sunrise, a live
/// countdown to the next prayer, and controls for calculation method, Asr
/// madhab, and manual per-prayer minute offsets. All computation happens
/// on-device via [PrayerTimesService] (astronomical formulas, no network),
/// so once a location fix is stored this screen works fully offline.
class PrayerTimesScreen extends StatefulWidget {
  const PrayerTimesScreen({super.key});

  @override
  State<PrayerTimesScreen> createState() => _PrayerTimesScreenState();
}

class _PrayerTimesScreenState extends State<PrayerTimesScreen> {
  static const _service = PrayerTimesService();

  _LoadState _state = _LoadState.locating;
  DailyPrayerTimes? _times;
  DateTime? _tomorrowFajr;
  Timer? _ticker;
  DateTime _now = DateTime.now();

  @override
  void initState() {
    super.initState();
    _ticker = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() => _now = DateTime.now());
    });
    _bootstrap();
  }

  @override
  void dispose() {
    _ticker?.cancel();
    super.dispose();
  }

  Future<void> _bootstrap() async {
    final prayerSettings = context.read<PrayerSettingsController>();
    if (prayerSettings.hasLocation) {
      _recompute();
    } else {
      await _refreshLocation();
    }
  }

  Future<void> _refreshLocation() async {
    setState(() => _state = _LoadState.locating);
    if (!await Geolocator.isLocationServiceEnabled()) {
      if (mounted) setState(() => _state = _LoadState.noService);
      return;
    }
    var permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    if (permission == LocationPermission.denied || permission == LocationPermission.deniedForever) {
      if (mounted) setState(() => _state = _LoadState.noPermission);
      return;
    }
    try {
      final position = await Geolocator.getCurrentPosition();
      if (!mounted) return;
      await context.read<PrayerSettingsController>().setLocation(
            latitude: position.latitude,
            longitude: position.longitude,
          );
      _recompute();
    } catch (_) {
      if (mounted) setState(() => _state = _LoadState.error);
    }
  }

  void _recompute() {
    final prayerSettings = context.read<PrayerSettingsController>();
    if (!prayerSettings.hasLocation) return;
    // Prayer-linked reminders (Adhan, early, iqamah, missed, Tahajjud) are
    // computed from these same settings, so any change here needs them
    // re-primed too -- fire-and-forget, this screen doesn't need to wait
    // on it to show updated times.
    rescheduleReminders(context);
    final today = DateTime.now();
    final times = _service.calculate(
      latitude: prayerSettings.latitude!,
      longitude: prayerSettings.longitude!,
      date: today,
      method: prayerSettings.method,
      madhab: prayerSettings.madhab,
      adjustmentsMinutes: prayerSettings.adjustments,
    );
    // Once today's Isha has passed, the countdown card needs a next target
    // to point at -- tomorrow's Fajr -- rather than disappearing until
    // midnight rolls over.
    final tomorrow = _service.calculate(
      latitude: prayerSettings.latitude!,
      longitude: prayerSettings.longitude!,
      date: today.add(const Duration(days: 1)),
      method: prayerSettings.method,
      madhab: prayerSettings.madhab,
      adjustmentsMinutes: prayerSettings.adjustments,
    );
    if (mounted) {
      setState(() {
        _times = times;
        _tomorrowFajr = tomorrow.fajr;
        _state = _LoadState.ready;
      });
    }
  }

  Future<void> _editOffset(PrayerName prayer) async {
    final prayerSettings = context.read<PrayerSettingsController>();
    final t = context.loc.t;
    var value = prayerSettings.adjustments[prayer] ?? 0;
    final result = await showDialog<int>(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: Text(t('prayer_adjust_time')),
          content: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(icon: const Icon(Icons.remove_circle_outline), onPressed: () => setDialogState(() => value--)),
              SizedBox(width: 64, child: Text('$value ${t('prayer_minutes_short')}', textAlign: TextAlign.center)),
              IconButton(icon: const Icon(Icons.add_circle_outline), onPressed: () => setDialogState(() => value++)),
            ],
          ),
          actions: [
            TextButton(onPressed: () => Navigator.of(context).pop(), child: Text(t('cancel'))),
            FilledButton(onPressed: () => Navigator.of(context).pop(value), child: Text(t('save'))),
          ],
        ),
      ),
    );
    if (result == null) return;
    await prayerSettings.setAdjustment(prayer, result);
    _recompute();
  }

  String _methodLabel(String Function(String) t, PrayerCalculationMethod m) => t('prayer_method_${m.name}');

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);
    final prayerSettings = context.watch<PrayerSettingsController>();

    return Scaffold(
      appBar: AppBar(
        title: Text(t('prayer_times_title')),
        actions: [
          IconButton(icon: const Icon(Icons.my_location), tooltip: t('prayer_refresh_location'), onPressed: _refreshLocation),
          PopupMenuButton<PrayerCalculationMethod>(
            icon: const Icon(Icons.tune),
            tooltip: t('prayer_calculation_method'),
            initialValue: prayerSettings.method,
            onSelected: (m) async {
              await prayerSettings.setMethod(m);
              _recompute();
            },
            itemBuilder: (context) => PrayerCalculationMethod.values
                .map((m) => CheckedPopupMenuItem(
                      value: m,
                      checked: prayerSettings.method == m,
                      child: Text(_methodLabel(t, m)),
                    ))
                .toList(),
          ),
          PopupMenuButton<PrayerAsrMadhab>(
            icon: const Icon(Icons.balance),
            tooltip: t('prayer_asr_madhab'),
            initialValue: prayerSettings.madhab,
            onSelected: (m) async {
              await prayerSettings.setMadhab(m);
              _recompute();
            },
            itemBuilder: (context) => [
              CheckedPopupMenuItem(
                value: PrayerAsrMadhab.hanafi,
                checked: prayerSettings.madhab == PrayerAsrMadhab.hanafi,
                child: Text(t('prayer_madhab_hanafi')),
              ),
              CheckedPopupMenuItem(
                value: PrayerAsrMadhab.shafi,
                checked: prayerSettings.madhab == PrayerAsrMadhab.shafi,
                child: Text(t('prayer_madhab_shafi')),
              ),
            ],
          ),
        ],
      ),
      body: switch (_state) {
        _LoadState.locating => const Center(child: CircularProgressIndicator()),
        _LoadState.noService => _Message(icon: Icons.location_off_outlined, text: t('qiblah_no_location_service'), onRetry: _refreshLocation),
        _LoadState.noPermission => _Message(icon: Icons.location_disabled_outlined, text: t('qiblah_no_permission'), onRetry: _refreshLocation),
        _LoadState.error => _Message(icon: Icons.error_outline, text: t('qiblah_error'), onRetry: _refreshLocation),
        _LoadState.ready => _times == null
            ? const Center(child: CircularProgressIndicator())
            : _PrayerList(times: _times!, tomorrowFajr: _tomorrowFajr, now: _now, theme: theme, t: t, onEditOffset: _editOffset),
      },
    );
  }
}

class _Message extends StatelessWidget {
  const _Message({required this.icon, required this.text, required this.onRetry});
  final IconData icon;
  final String text;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 48, color: Theme.of(context).colorScheme.onSurfaceVariant),
            const SizedBox(height: 16),
            Text(text, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            FilledButton(onPressed: onRetry, child: Text(t('prayer_retry'))),
          ],
        ),
      ),
    );
  }
}

class _PrayerList extends StatelessWidget {
  const _PrayerList({
    required this.times,
    required this.tomorrowFajr,
    required this.now,
    required this.theme,
    required this.t,
    required this.onEditOffset,
  });

  final DailyPrayerTimes times;
  final DateTime? tomorrowFajr;
  final DateTime now;
  final ThemeData theme;
  final String Function(String) t;
  final ValueChanged<PrayerName> onEditOffset;

  String _nameFor(PrayerName p) => switch (p) {
        PrayerName.fajr => t('prayer_fajr'),
        PrayerName.sunrise => t('prayer_sunrise'),
        PrayerName.dhuhr => t('prayer_dhuhr'),
        PrayerName.asr => t('prayer_asr'),
        PrayerName.maghrib => t('prayer_maghrib'),
        PrayerName.isha => t('prayer_isha'),
      };

  @override
  Widget build(BuildContext context) {
    final next = times.nextPrayer(at: now);
    // After today's Isha, next is null -- fall back to tomorrow's Fajr so
    // the countdown card keeps a target instead of vanishing until midnight.
    final nextLabel = next != null ? _nameFor(next) : (tomorrowFajr != null ? t('prayer_fajr') : null);
    final nextTime = next != null ? times.timeFor(next) : tomorrowFajr;
    final countdown = nextTime?.difference(now);

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        if (nextLabel != null && countdown != null)
          Card(
            color: AppColors.navy,
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Text(t('prayer_next_in'), style: const TextStyle(color: Colors.white70)),
                  const SizedBox(height: 4),
                  Text(
                    nextLabel,
                    style: const TextStyle(color: AppColors.gold, fontSize: 24, fontWeight: FontWeight.w700),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _formatDuration(countdown),
                    style: const TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.w300, fontFeatures: [FontFeature.tabularFigures()]),
                  ),
                ],
              ),
            ),
          ),
        const SizedBox(height: 16),
        for (final p in PrayerName.values)
          Card(
            child: ListTile(
              leading: Icon(
                p == PrayerName.sunrise ? Icons.wb_twilight : Icons.mosque_outlined,
                color: p == next ? AppColors.gold : theme.colorScheme.onSurfaceVariant,
              ),
              title: Text(_nameFor(p), style: p == next ? const TextStyle(fontWeight: FontWeight.w700) : null),
              trailing: Text(
                DateFormat.jm().format(times.timeFor(p)),
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: p == next ? FontWeight.w700 : FontWeight.w400,
                  color: p == next ? AppColors.gold : null,
                ),
              ),
              onLongPress: p == PrayerName.sunrise ? null : () => onEditOffset(p),
            ),
          ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          child: Text(t('prayer_offset_hint'), style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
        ),
      ],
    );
  }

  String _formatDuration(Duration d) {
    final h = d.inHours;
    final m = d.inMinutes % 60;
    final s = d.inSeconds % 60;
    final hh = h.toString().padLeft(2, '0');
    final mm = m.toString().padLeft(2, '0');
    final ss = s.toString().padLeft(2, '0');
    return '$hh:$mm:$ss';
  }
}
