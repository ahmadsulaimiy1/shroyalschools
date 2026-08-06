import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/services/settings_controller.dart';

/// Qur'an reading preferences. Font/font size already follow the app-wide
/// text-size setting (Settings > Accessibility) rather than a separate
/// Qur'an-only font size, to avoid two competing "how big is my text"
/// controls. Tafsir mode, Tajweed colours, and page-turn animation are not
/// offered here yet -- Tafsir content and Tajweed-colour data are both
/// blocked on the same licensing/sourcing questions tracked as tasks
/// #56/#63/#73, and a fabricated toggle for content that isn't there would
/// be worse than not showing it.
class QuranSettingsScreen extends StatelessWidget {
  const QuranSettingsScreen({super.key});

  String _readingModeLabel(String Function(String) t, QuranReadingMode mode) => switch (mode) {
        QuranReadingMode.arabicOnly => t('quran_mode_arabic_only'),
        QuranReadingMode.arabicTranslation => t('quran_mode_arabic_translation'),
        QuranReadingMode.arabicTranslationTransliteration => t('quran_mode_arabic_translation_transliteration'),
      };

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final settings = context.watch<SettingsController>();

    return Scaffold(
      appBar: AppBar(title: Text(t('settings_quran'))),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 8),
        children: [
          SwitchListTile(
            secondary: const Icon(Icons.menu_book_outlined),
            title: Text(t('quran_mushaf_mode')),
            subtitle: Text(t('settings_quran_mushaf_mode_subtitle')),
            value: settings.quranMushafMode,
            onChanged: settings.setQuranMushafMode,
          ),
          if (!settings.quranMushafMode) ...[
            ListTile(
              leading: const Icon(Icons.text_fields),
              title: Text(t('quran_reading_mode')),
              subtitle: Text(_readingModeLabel(t, settings.quranReadingMode)),
              onTap: () => _showReadingModeSheet(context, settings),
            ),
            SwitchListTile(
              secondary: const Icon(Icons.view_carousel_outlined),
              title: Text(t('quran_scroll_mode')),
              subtitle: Text(settings.quranScrollMode == QuranScrollMode.horizontalSwipe
                  ? t('settings_quran_scroll_swipe')
                  : t('settings_quran_scroll_list')),
              value: settings.quranScrollMode == QuranScrollMode.horizontalSwipe,
              onChanged: (v) => settings.setQuranScrollMode(v ? QuranScrollMode.horizontalSwipe : QuranScrollMode.verticalList),
            ),
          ],
          const Divider(height: 24),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Text(
              t('settings_quran_footnote'),
              style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Theme.of(context).colorScheme.onSurfaceVariant),
            ),
          ),
        ],
      ),
    );
  }

  void _showReadingModeSheet(BuildContext context, SettingsController settings) {
    final t = context.loc.t;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            for (final mode in QuranReadingMode.values)
              RadioListTile<QuranReadingMode>(
                value: mode,
                groupValue: settings.quranReadingMode,
                title: Text(_readingModeLabel(t, mode)),
                onChanged: (value) {
                  if (value != null) settings.setQuranReadingMode(value);
                  Navigator.pop(context);
                },
              ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }
}
