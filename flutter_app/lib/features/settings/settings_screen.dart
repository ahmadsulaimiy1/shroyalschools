import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/services/settings_controller.dart';
import '../about/about_screen.dart';
import '../prayer/prayer_times_screen.dart';
import 'appearance_settings_screen.dart';
import 'audio_settings_screen.dart';
import 'data_settings_screen.dart';
import 'notification_settings_screen.dart';
import 'quran_settings_screen.dart';

/// The premium Settings control centre: a hub of named sections (Appearance,
/// Qur'an, Audio, Prayer, Notifications, Downloads, Accessibility, Backup,
/// Privacy, Advanced), each either its own screen or, for the smallest
/// sections, expanded inline here. Prayer's own controls already live on
/// the Prayer Times screen (calculation method, madhab, offsets) -- this
/// links there rather than duplicating that UI. Downloads lives inside
/// Audio Settings since the only downloadable content today is cached
/// Qur'an recitation audio.
class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final settings = context.watch<SettingsController>();

    return Scaffold(
      appBar: AppBar(title: Text(t('settings_title'))),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 8),
        children: [
          _NavTile(
            icon: Icons.brightness_6_outlined,
            title: t('settings_appearance'),
            screen: const AppearanceSettingsScreen(),
          ),
          _NavTile(
            icon: Icons.menu_book_outlined,
            title: t('settings_quran'),
            screen: const QuranSettingsScreen(),
          ),
          _NavTile(
            icon: Icons.headphones_outlined,
            title: t('settings_audio'),
            screen: const AudioSettingsScreen(),
          ),
          _NavTile(
            icon: Icons.access_time_outlined,
            title: t('prayer_times_title'),
            screen: const PrayerTimesScreen(),
          ),
          _NavTile(
            icon: Icons.notifications_active_outlined,
            title: t('notif_settings_title'),
            screen: const NotificationSettingsScreen(),
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
          _NavTile(
            icon: Icons.folder_shared_outlined,
            title: t('settings_data_centre'),
            screen: const DataSettingsScreen(),
          ),
          const Divider(height: 24),
          _NavTile(
            icon: Icons.info_outline,
            title: t('settings_about'),
            screen: const AboutScreen(),
          ),
        ],
      ),
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
}

class _NavTile extends StatelessWidget {
  const _NavTile({required this.icon, required this.title, required this.screen});
  final IconData icon;
  final String title;
  final Widget screen;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      trailing: const Icon(Icons.chevron_right),
      onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => screen)),
    );
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
