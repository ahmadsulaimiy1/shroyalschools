import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/counter_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/dhikr.dart';
import '../../core/services/active_dhikr_controller.dart';
import '../../core/widgets/app_shell.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _today = 0;
  int _lifetime = 0;
  bool _loading = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final repo = context.read<CounterRepository>();
    final startOfDay = DateTime.now();
    final today = DateTime(startOfDay.year, startOfDay.month, startOfDay.day);
    final results = await Future.wait([
      repo.countSince(today),
      repo.lifetimeCount(),
    ]);
    if (!mounted) return;
    setState(() {
      _today = results[0];
      _lifetime = results[1];
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;
    final suggested = seedAdhkar.first;

    return Scaffold(
      appBar: AppBar(title: Text(t('app_name'))),
      body: RefreshIndicator(
        onRefresh: _load,
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Text(t('home_greeting'), style: theme.textTheme.headlineMedium),
            const SizedBox(height: 4),
            Text(t('home_subtitle'), style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: _StatCard(
                    label: t('home_todays_count'),
                    value: _loading ? '—' : '$_today',
                    icon: Icons.today_outlined,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: _StatCard(
                    label: t('home_lifetime_count'),
                    value: _loading ? '—' : '$_lifetime',
                    icon: Icons.auto_awesome_outlined,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            Text(t('home_suggested_dhikr'), style: theme.textTheme.titleMedium),
            const SizedBox(height: 12),
            Card(
              child: ListTile(
                contentPadding: const EdgeInsets.all(16),
                title: Text(suggested.arabicText, style: theme.textTheme.headlineMedium, textAlign: TextAlign.right),
                subtitle: Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Text('${suggested.transliteration} • ${suggested.translationEn}'),
                ),
                trailing: FilledButton(
                  onPressed: () {
                    context.read<ActiveDhikrController>().select(suggested);
                    AppShellScope.maybeOf(context)?.goToCounter();
                  },
                  child: Text(t('home_quick_start')),
                ),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.fingerprint),
                label: Text(t('home_quick_start')),
                onPressed: () {
                  context.read<ActiveDhikrController>().clearToFreeform();
                  AppShellScope.maybeOf(context)?.goToCounter();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  const _StatCard({required this.label, required this.value, required this.icon});

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
