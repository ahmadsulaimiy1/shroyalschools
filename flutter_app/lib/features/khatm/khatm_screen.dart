import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/quran_repository.dart';
import '../../core/localization/app_localizations.dart';

/// Khatm Centre: lets the user set a target completion date for reading the
/// whole Qur'an and shows a daily verse target + progress, computed from
/// the existing quran_reads log (no new tracking mechanism -- this is a
/// view over data the app already collects every time a surah/juz is
/// opened, see QuranReaderScreen.setLastRead).
class KhatmScreen extends StatefulWidget {
  const KhatmScreen({super.key});

  @override
  State<KhatmScreen> createState() => _KhatmScreenState();
}

class _KhatmScreenState extends State<KhatmScreen> {
  bool _loading = true;
  KhatmPlan? _plan;
  int _versesRead = 0;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final repo = context.read<QuranRepository>();
    final plan = await repo.khatmPlan();
    final read = plan == null ? 0 : await repo.versesReadSince(plan.startDate);
    if (!mounted) return;
    setState(() {
      _plan = plan;
      _versesRead = read;
      _loading = false;
    });
  }

  Future<void> _pickTargetDate() async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: now.add(const Duration(days: 30)),
      firstDate: now.add(const Duration(days: 1)),
      lastDate: now.add(const Duration(days: 365 * 3)),
    );
    if (picked == null) return;
    await context.read<QuranRepository>().setKhatmPlan(picked);
    _load();
  }

  Future<void> _cancelPlan() async {
    await context.read<QuranRepository>().clearKhatmPlan();
    _load();
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(t('khatm_title'))),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _plan == null
              ? _NoPlanView(onSetTarget: _pickTargetDate, t: t, theme: theme)
              : _PlanView(plan: _plan!, versesRead: _versesRead, onCancel: _cancelPlan, t: t, theme: theme),
    );
  }
}

class _NoPlanView extends StatelessWidget {
  const _NoPlanView({required this.onSetTarget, required this.t, required this.theme});
  final VoidCallback onSetTarget;
  final String Function(String) t;
  final ThemeData theme;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.flag_outlined, size: 56, color: theme.colorScheme.secondary),
          const SizedBox(height: 16),
          Text(t('khatm_intro'), textAlign: TextAlign.center, style: theme.textTheme.bodyLarge),
          const SizedBox(height: 24),
          FilledButton.icon(
            icon: const Icon(Icons.calendar_month_outlined),
            label: Text(t('khatm_set_target')),
            onPressed: onSetTarget,
          ),
        ],
      ),
    );
  }
}

class _PlanView extends StatelessWidget {
  const _PlanView({required this.plan, required this.versesRead, required this.onCancel, required this.t, required this.theme});
  final KhatmPlan plan;
  final int versesRead;
  final VoidCallback onCancel;
  final String Function(String) t;
  final ThemeData theme;

  @override
  Widget build(BuildContext context) {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final daysRemaining = plan.targetDate.difference(today).inDays.clamp(1, 999999);
    final versesRemaining = (totalQuranVerseCount - versesRead).clamp(0, totalQuranVerseCount);
    final dailyTarget = (versesRemaining / daysRemaining).ceil();
    final progress = (versesRead / totalQuranVerseCount).clamp(0.0, 1.0);

    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        LinearProgressIndicator(value: progress, minHeight: 10, borderRadius: BorderRadius.circular(6)),
        const SizedBox(height: 8),
        Text(
          context.loc.tArgs('khatm_progress', [versesRead, totalQuranVerseCount]),
          style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
        ),
        const SizedBox(height: 24),
        Row(
          children: [
            Expanded(child: _StatTile(label: t('khatm_days_remaining'), value: '$daysRemaining', icon: Icons.calendar_today_outlined)),
            const SizedBox(width: 16),
            Expanded(child: _StatTile(label: t('khatm_daily_target'), value: '$dailyTarget', icon: Icons.flag_outlined)),
          ],
        ),
        const SizedBox(height: 24),
        Text(context.loc.tArgs('khatm_target_date', [_formatDate(plan.targetDate)]), style: theme.textTheme.bodyMedium),
        const SizedBox(height: 24),
        OutlinedButton(onPressed: onCancel, child: Text(t('khatm_cancel_plan'))),
      ],
    );
  }

  String _formatDate(DateTime d) => '${d.day}/${d.month}/${d.year}';
}

class _StatTile extends StatelessWidget {
  const _StatTile({required this.label, required this.value, required this.icon});
  final String label;
  final String value;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: theme.colorScheme.secondary),
            const SizedBox(height: 12),
            Text(value, style: theme.textTheme.headlineMedium),
            const SizedBox(height: 4),
            Text(label, style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
          ],
        ),
      ),
    );
  }
}
