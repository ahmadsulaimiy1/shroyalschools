import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/services/settings_controller.dart';

/// Appearance: theme (Light/Dark/System + an AMOLED true-black variant of
/// Dark), and language. Accent colour and per-surah Tajweed colours are not
/// here yet -- see docs/28 for why (a single accent swap touches the whole
/// brand palette derived from it app-wide, and Tajweed colours need a
/// verified Tajweed-annotated text, tracked separately as task #56).
class AppearanceSettingsScreen extends StatelessWidget {
  const AppearanceSettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final settings = context.watch<SettingsController>();

    return Scaffold(
      appBar: AppBar(title: Text(t('settings_appearance'))),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 8),
        children: [
          ListTile(
            leading: const Icon(Icons.brightness_6_outlined),
            title: Text(t('settings_theme')),
            subtitle: Text(_themeLabel(context, settings.themeMode)),
            onTap: () => _showThemeSheet(context, settings),
          ),
          if (settings.themeMode != AppThemeMode.light)
            SwitchListTile(
              secondary: const Icon(Icons.dark_mode_outlined),
              title: Text(t('settings_amoled_black')),
              subtitle: Text(t('settings_amoled_black_subtitle')),
              value: settings.amoledBlackEnabled,
              onChanged: settings.setAmoledBlackEnabled,
            ),
          const Divider(height: 24),
          ListTile(
            leading: const Icon(Icons.language_outlined),
            title: Text(t('settings_language')),
            subtitle: Text(settings.locale.languageCode == 'ar' ? t('settings_language_arabic') : t('settings_language_english')),
            onTap: () => _showLanguageSheet(context, settings),
          ),
        ],
      ),
    );
  }

  String _themeLabel(BuildContext context, AppThemeMode mode) {
    final t = context.loc.t;
    switch (mode) {
      case AppThemeMode.system:
        return t('settings_theme_system');
      case AppThemeMode.light:
        return t('settings_theme_light');
      case AppThemeMode.dark:
        return t('settings_theme_dark');
    }
  }

  void _showThemeSheet(BuildContext context, SettingsController settings) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (context) {
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              for (final mode in AppThemeMode.values)
                RadioListTile<AppThemeMode>(
                  value: mode,
                  groupValue: settings.themeMode,
                  title: Text(_themeLabel(context, mode)),
                  onChanged: (value) {
                    if (value != null) settings.setThemeMode(value);
                    Navigator.pop(context);
                  },
                ),
              const SizedBox(height: 8),
            ],
          ),
        );
      },
    );
  }

  void _showLanguageSheet(BuildContext context, SettingsController settings) {
    final t = context.loc.t;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (context) {
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              RadioListTile<String>(
                value: 'en',
                groupValue: settings.locale.languageCode,
                title: Text(t('settings_language_english')),
                onChanged: (value) {
                  settings.setLocale(const Locale('en'));
                  Navigator.pop(context);
                },
              ),
              RadioListTile<String>(
                value: 'ar',
                groupValue: settings.locale.languageCode,
                title: Text(t('settings_language_arabic')),
                onChanged: (value) {
                  settings.setLocale(const Locale('ar'));
                  Navigator.pop(context);
                },
              ),
              const SizedBox(height: 8),
            ],
          ),
        );
      },
    );
  }
}
