import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/counter_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/services/settings_controller.dart';
import '../about/about_screen.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final settings = context.watch<SettingsController>();
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(t('settings_title'))),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 8),
        children: [
          _SectionHeader(t('settings_appearance')),
          ListTile(
            title: Text(t('settings_theme')),
            subtitle: Text(_themeLabel(context, settings.themeMode)),
            leading: const Icon(Icons.brightness_6_outlined),
            onTap: () => _showThemeSheet(context, settings),
          ),
          ListTile(
            title: Text(t('settings_language')),
            subtitle: Text(settings.locale.languageCode == 'ar' ? t('settings_language_arabic') : t('settings_language_english')),
            leading: const Icon(Icons.language_outlined),
            onTap: () => _showLanguageSheet(context, settings),
          ),
          const Divider(height: 24),
          _SectionHeader(t('settings_feedback')),
          SwitchListTile(
            secondary: const Icon(Icons.volume_up_outlined),
            title: Text(t('settings_sound')),
            value: settings.soundEnabled,
            onChanged: settings.setSoundEnabled,
          ),
          SwitchListTile(
            secondary: const Icon(Icons.vibration_outlined),
            title: Text(t('settings_vibration')),
            value: settings.vibrationEnabled,
            onChanged: settings.setVibrationEnabled,
          ),
          SwitchListTile(
            secondary: const Icon(Icons.tune_outlined),
            title: Text(t('settings_volume_button_counter')),
            subtitle: Text(t('settings_volume_button_counter_subtitle')),
            value: settings.volumeButtonEnabled,
            onChanged: settings.setVolumeButtonEnabled,
          ),
          const Divider(height: 24),
          _SectionHeader(t('settings_accessibility')),
          ListTile(
            leading: const Icon(Icons.format_size),
            title: Text(t('settings_text_size')),
            subtitle: Text(_textSizeLabel(context, settings.textSizePreset)),
            onTap: () => _showTextSizeSheet(context, settings),
          ),
          SwitchListTile(
            secondary: const Icon(Icons.elderly_outlined),
            title: Text(t('settings_elderly_mode')),
            subtitle: Text(t('settings_elderly_mode_subtitle')),
            value: settings.elderlyFriendlyMode,
            onChanged: settings.setElderlyFriendlyMode,
          ),
          const Divider(height: 24),
          _SectionHeader(t('settings_data')),
          ListTile(
            leading: Icon(Icons.delete_outline, color: theme.colorScheme.error),
            title: Text(t('settings_reset_all_data'), style: TextStyle(color: theme.colorScheme.error)),
            onTap: () => _confirmResetData(context),
          ),
          const Divider(height: 24),
          ListTile(
            leading: const Icon(Icons.info_outline),
            title: Text(t('settings_about')),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => const AboutScreen()),
            ),
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

  String _textSizeLabel(BuildContext context, TextSizePreset preset) {
    final t = context.loc.t;
    switch (preset) {
      case TextSizePreset.standard:
        return t('settings_text_size_standard');
      case TextSizePreset.large:
        return t('settings_text_size_large');
      case TextSizePreset.extraLarge:
        return t('settings_text_size_extra_large');
    }
  }

  void _showTextSizeSheet(BuildContext context, SettingsController settings) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (context) {
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              for (final preset in TextSizePreset.values)
                RadioListTile<TextSizePreset>(
                  value: preset,
                  groupValue: settings.textSizePreset,
                  title: Text(_textSizeLabel(context, preset)),
                  onChanged: (value) {
                    if (value != null) settings.setTextSizePreset(value);
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

  Future<void> _confirmResetData(BuildContext context) async {
    final t = context.loc.t;
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(t('settings_reset_all_data')),
        content: Text(t('settings_reset_all_data_confirm')),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: Text(t('common_cancel'))),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: Theme.of(context).colorScheme.error),
            onPressed: () => Navigator.pop(context, true),
            child: Text(t('common_delete')),
          ),
        ],
      ),
    );
    if (confirmed == true && context.mounted) {
      await context.read<CounterRepository>().resetAllData();
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(t('settings_reset_all_data_done'))),
        );
      }
    }
  }
}

class _SectionHeader extends StatelessWidget {
  const _SectionHeader(this.label);
  final String label;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
      child: Text(
        label,
        style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.secondary),
      ),
    );
  }
}
