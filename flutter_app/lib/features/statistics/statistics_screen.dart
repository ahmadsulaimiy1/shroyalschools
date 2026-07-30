import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../../core/database/counter_repository.dart';
import '../../core/localization/app_localizations.dart';

class StatisticsScreen extends StatefulWidget {
  const StatisticsScreen({super.key});

  @override
  State<StatisticsScreen> createState() => _StatisticsScreenState();
}

class _StatisticsScreenState extends State<StatisticsScreen> {
  int _today = 0;
  int _week = 0;
  int _lifetime = 0;
  int _sessions = 0;
  List<DailyCount> _daily = const [];
  bool _loading = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final repo = context.read<CounterRepository>();
    final now = DateTime.now();
    final startOfDay = DateTime(now.year, now.month, now.day);
    final startOfWeek = startOfDay.subtract(Duration(days: now.weekday - 1));

    final results = await Future.wait([
      repo.countSince(startOfDay),
      repo.countSince(startOfWeek),
      repo.lifetimeCount(),
      repo.sessionCount(),
      repo.dailyCounts(7),
    ]);

    if (!mounted) return;
    setState(() {
      _today = results[0] as int;
      _week = results[1] as int;
      _lifetime = results[2] as int;
      _sessions = results[3] as int;
      _daily = results[4] as List<DailyCount>;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;
    final isRtl = context.loc.isRtl;

    return Scaffold(
      appBar: AppBar(title: Text(t('statistics_title'))),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(20),
                children: [
                  Row(
                    children: [
                      Expanded(child: _MetricCard(label: t('statistics_today'), value: _today)),
                      const SizedBox(width: 12),
                      Expanded(child: _MetricCard(label: t('statistics_this_week'), value: _week)),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(child: _MetricCard(label: t('statistics_lifetime'), value: _lifetime)),
                      const SizedBox(width: 12),
                      Expanded(child: _MetricCard(label: t('statistics_sessions'), value: _sessions)),
                    ],
                  ),
                  const SizedBox(height: 28),
                  Text(t('statistics_history'), style: theme.textTheme.titleMedium),
                  const SizedBox(height: 16),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(16, 24, 16, 16),
                      child: _WeeklyBarChart(daily: _daily, isRtl: isRtl),
                    ),
                  ),
                  if (_lifetime == 0) ...[
                    const SizedBox(height: 24),
                    Center(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Text(
                          t('statistics_no_data'),
                          textAlign: TextAlign.center,
                          style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  const _MetricCard({required this.label, required this.value});
  final String label;
  final int value;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('$value', style: theme.textTheme.headlineMedium),
            const SizedBox(height: 4),
            Text(label, style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
          ],
        ),
      ),
    );
  }
}

class _WeeklyBarChart extends StatelessWidget {
  const _WeeklyBarChart({required this.daily, required this.isRtl});

  final List<DailyCount> daily;
  final bool isRtl;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final maxValue = daily.fold<int>(1, (max, d) => d.count > max ? d.count : max);
    final ordered = isRtl ? daily.reversed.toList() : daily;

    return SizedBox(
      height: 140,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: ordered.map((d) {
          final heightFactor = d.count / maxValue;
          return Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Text('${d.count}', style: theme.textTheme.labelLarge),
              const SizedBox(height: 6),
              Container(
                width: 22,
                height: 80 * (heightFactor.clamp(0.04, 1.0)),
                decoration: BoxDecoration(
                  color: theme.colorScheme.primary,
                  borderRadius: BorderRadius.circular(6),
                ),
              ),
              const SizedBox(height: 8),
              Text(DateFormat.E().format(d.date), style: theme.textTheme.labelLarge),
            ],
          );
        }).toList(),
      ),
    );
  }
}
