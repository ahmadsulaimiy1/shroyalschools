import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/counter_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/services/active_dhikr_controller.dart';
import '../../core/services/feedback_service.dart';
import '../../core/services/settings_controller.dart';
import '../../core/services/volume_button_service.dart';
import 'bead_ring_counter.dart';

class CounterScreen extends StatefulWidget {
  const CounterScreen({super.key});

  @override
  State<CounterScreen> createState() => _CounterScreenState();
}

class _CounterScreenState extends State<CounterScreen> {
  String? _sessionId;
  int _count = 0;
  int _target = 33;
  bool _completed = false;

  ActiveDhikrController? _activeDhikr;
  SettingsController? _settings;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();

    _activeDhikr?.removeListener(_onActiveDhikrChanged);
    _activeDhikr = context.watch<ActiveDhikrController>();
    _activeDhikr!.addListener(_onActiveDhikrChanged);

    _settings = context.watch<SettingsController>();
    // Cheap idempotent channel call — re-synced on every settings change so
    // toggling "Volume Button Counter" in Settings takes effect immediately,
    // even though this screen (kept alive by the shell's IndexedStack) was
    // already built before the toggle happened.
    VolumeButtonService.instance.setEnabled(_settings!.volumeButtonEnabled);
    VolumeButtonService.instance.onVolumeButtonPressed = _onCount;

    if (_sessionId == null) {
      _target = _activeDhikr!.target;
      _startSession();
    }
  }

  void _onActiveDhikrChanged() {
    setState(() {
      _target = _activeDhikr!.target;
    });
    _startSession();
  }

  Future<void> _startSession() async {
    final repo = context.read<CounterRepository>();
    final id = await repo.startSession(dhikrId: _activeDhikr?.dhikr?.id, targetCount: _target);
    if (!mounted) return;
    setState(() {
      _sessionId = id;
      _count = 0;
      _completed = false;
    });
  }

  Future<void> _onCount() async {
    if (_sessionId == null || _completed) return;
    final repo = context.read<CounterRepository>();
    final feedback = context.read<FeedbackService>();

    final newCount = _count + 1;
    final justCompleted = newCount >= _target;
    setState(() {
      _count = newCount;
      _completed = justCompleted;
    });

    await repo.recordTap(_sessionId!);
    if (justCompleted) {
      await repo.completeSession(_sessionId!);
      feedback.onComplete();
    } else {
      feedback.onCount();
    }
  }

  Future<void> _onReset() async {
    final t = context.loc.t;
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(t('counter_reset_confirm_title')),
        content: Text(t('counter_reset_confirm_body')),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: Text(t('counter_cancel'))),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: Text(t('counter_confirm'))),
        ],
      ),
    );
    if (confirmed == true) {
      await _startSession();
    }
  }

  Future<void> _onSelectTarget() async {
    final t = context.loc.t;
    final choice = await showModalBottomSheet<int>(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (context) {
        const options = [33, 99, 100, 1000];
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Padding(
                padding: const EdgeInsets.all(16),
                child: Text(t('counter_select_target'), style: Theme.of(context).textTheme.titleMedium),
              ),
              for (final o in options)
                ListTile(
                  title: Text('$o'),
                  onTap: () => Navigator.pop(context, o),
                ),
              const SizedBox(height: 8),
            ],
          ),
        );
      },
    );
    if (choice != null) {
      _activeDhikr!.clearToFreeform();
      _activeDhikr!.setCustomTarget(choice);
      setState(() => _target = choice);
      await _startSession();
    }
  }

  @override
  void dispose() {
    _activeDhikr?.removeListener(_onActiveDhikrChanged);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;
    final dhikr = context.watch<ActiveDhikrController>().dhikr;

    return Scaffold(
      appBar: AppBar(
        title: Text(t('nav_counter')),
        actions: [
          IconButton(
            tooltip: t('counter_select_target'),
            icon: const Icon(Icons.tune),
            onPressed: _onSelectTarget,
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 8),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                children: [
                  Text(
                    dhikr?.arabicText ?? t('counter_freeform'),
                    style: theme.textTheme.headlineMedium,
                    textAlign: TextAlign.center,
                  ),
                  if (dhikr != null) ...[
                    const SizedBox(height: 4),
                    Text(
                      '${dhikr.transliteration} • ${dhikr.translationEn}',
                      style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                      textAlign: TextAlign.center,
                    ),
                  ] else ...[
                    const SizedBox(height: 4),
                    Text(
                      t('counter_tap_hint'),
                      style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                    ),
                  ],
                ],
              ),
            ),
            Expanded(
              child: Center(
                child: BeadRingCounter(currentCount: _count, targetCount: _target, onTap: _onCount),
              ),
            ),
            Text(
              context.loc.tArgs('counter_progress_of', [_count, _target]),
              style: theme.textTheme.labelLarge,
            ),
            const SizedBox(height: 8),
            if (_completed)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
                child: Card(
                  color: theme.colorScheme.secondary.withOpacity(0.12),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        Text(t('counter_completed_title'), style: theme.textTheme.titleMedium),
                        const SizedBox(height: 4),
                        Text(t('counter_completed_body'), textAlign: TextAlign.center),
                      ],
                    ),
                  ),
                ),
              ),
            Padding(
              padding: const EdgeInsets.all(24),
              child: OutlinedButton.icon(
                icon: const Icon(Icons.refresh),
                label: Text(t('counter_reset')),
                onPressed: _onReset,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
