import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/models/dhikr.dart';
import '../../core/services/active_dhikr_controller.dart';
import '../../core/widgets/app_shell.dart';

class AdhkarScreen extends StatelessWidget {
  const AdhkarScreen({super.key});

  static const _categoryOrder = [
    DhikrCategory.postSalah,
    DhikrCategory.morning,
    DhikrCategory.evening,
    DhikrCategory.general,
  ];

  String _categoryLabel(BuildContext context, DhikrCategory category) {
    final t = context.loc.t;
    switch (category) {
      case DhikrCategory.postSalah:
        return t('adhkar_category_post_salah');
      case DhikrCategory.morning:
        return t('adhkar_category_morning');
      case DhikrCategory.evening:
        return t('adhkar_category_evening');
      case DhikrCategory.general:
        return t('adhkar_category_general');
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(t('adhkar_title'))),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          for (final category in _categoryOrder) ...[
            Padding(
              padding: const EdgeInsets.only(bottom: 12, top: 8),
              child: Text(_categoryLabel(context, category), style: theme.textTheme.titleMedium),
            ),
            ...seedAdhkar.where((d) => d.category == category).map(
                  (dhikr) => _AdhkarCard(dhikr: dhikr),
                ),
            const SizedBox(height: 12),
          ],
        ],
      ),
    );
  }
}

class _AdhkarCard extends StatelessWidget {
  const _AdhkarCard({required this.dhikr});
  final Dhikr dhikr;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(dhikr.arabicText, style: theme.textTheme.titleLarge, textAlign: TextAlign.right),
            const SizedBox(height: 6),
            Text(dhikr.transliteration, style: theme.textTheme.bodyMedium),
            Text(
              dhikr.translationEn,
              style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
            const SizedBox(height: 10),
            Text(
              '${t('adhkar_source')}: ${dhikr.sourceCitation}',
              style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.secondary),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Text('${t('adhkar_target')}: ${dhikr.defaultTarget}', style: theme.textTheme.labelLarge),
                const Spacer(),
                FilledButton(
                  onPressed: () {
                    context.read<ActiveDhikrController>().select(dhikr);
                    AppShellScope.maybeOf(context)?.goToCounter();
                  },
                  child: Text(t('adhkar_start_counting')),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
