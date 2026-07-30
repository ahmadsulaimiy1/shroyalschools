import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/counter_repository.dart';
import '../../core/database/quran_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/dhikr.dart';
import '../../core/models/quran_chapter.dart';
import '../../core/models/quran_verse.dart';
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
  QuranVerse? _lastReadVerse;
  QuranChapter? _lastReadChapter;
  bool _loading = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final repo = context.read<CounterRepository>();
    final quranRepo = context.read<QuranRepository>();
    final startOfDay = DateTime.now();
    final today = DateTime(startOfDay.year, startOfDay.month, startOfDay.day);
    final results = await Future.wait([
      repo.countSince(today),
      repo.lifetimeCount(),
    ]);
    final lastRead = await quranRepo.lastRead();
    final lastReadChapter = lastRead == null ? null : await quranRepo.chapter(lastRead.surah);
    if (!mounted) return;
    setState(() {
      _today = results[0];
      _lifetime = results[1];
      _lastReadVerse = lastRead;
      _lastReadChapter = lastReadChapter;
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
            if (_lastReadVerse != null && _lastReadChapter != null) ...[
              const SizedBox(height: 24),
              Text(t('quran_continue_reading'), style: theme.textTheme.titleMedium),
              const SizedBox(height: 12),
              Card(
                color: theme.colorScheme.tertiary,
                child: ListTile(
                  contentPadding: const EdgeInsets.all(16),
                  leading: Icon(Icons.auto_stories_outlined, color: theme.colorScheme.secondary),
                  title: Text(
                    '${_lastReadChapter!.nameTransliteration} — ${_lastReadChapter!.nameTranslation}',
                    style: theme.textTheme.titleMedium?.copyWith(color: Colors.white),
                  ),
                  subtitle: Text(
                    '${_lastReadVerse!.surah}:${_lastReadVerse!.ayah}',
                    style: theme.textTheme.bodyMedium?.copyWith(color: Colors.white.withOpacity(0.85)),
                  ),
                  trailing: Icon(Icons.chevron_right, color: Colors.white),
                  onTap: () => AppShellScope.maybeOf(context)?.goToQuran(),
                ),
              ),
            ],
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
