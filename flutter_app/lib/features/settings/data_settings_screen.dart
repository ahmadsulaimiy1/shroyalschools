import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:package_info_plus/package_info_plus.dart' as pkg;
import 'package:path_provider/path_provider.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../core/database/counter_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/services/notifications/notification_service.dart';

/// Backup, Privacy, and Advanced -- grouped into one screen since all three
/// are "manage your data" concerns a user reaches for together, rather than
/// three near-empty screens. Local backup exports every persisted app
/// setting/preference to a JSON file in the app's own private storage
/// (survives app updates; cleared on uninstall, like any Android app's
/// private data). Cloud backup isn't offered -- like the AI Worship
/// Assistant explored earlier in this project, syncing user data off-device
/// needs a real backend (hosting, accounts, a data-retention policy) that's
/// an infrastructure decision for the owner, not something to add silently.
class DataSettingsScreen extends StatefulWidget {
  const DataSettingsScreen({super.key});

  @override
  State<DataSettingsScreen> createState() => _DataSettingsScreenState();
}

class _DataSettingsScreenState extends State<DataSettingsScreen> {
  String? _version;
  String? _lastBackupInfo;
  bool _busy = false;
  LocationPermission? _locationPermission;
  bool? _notificationsEnabled;

  @override
  void initState() {
    super.initState();
    _loadVersion();
    _loadBackupInfo();
    _loadPermissionStatus();
  }

  Future<void> _loadVersion() async {
    try {
      final info = await pkg.PackageInfo.fromPlatform();
      if (mounted) setState(() => _version = '${info.version} (${info.buildNumber})');
    } catch (_) {}
  }

  Future<Directory> _backupDir() async {
    final baseDir = await getApplicationDocumentsDirectory();
    final dir = Directory('${baseDir.path}/backups');
    if (!await dir.exists()) await dir.create(recursive: true);
    return dir;
  }

  Future<void> _loadBackupInfo() async {
    final dir = await _backupDir();
    final files = await dir.list().where((e) => e is File && e.path.endsWith('.json')).toList();
    if (files.isEmpty) {
      if (mounted) setState(() => _lastBackupInfo = null);
      return;
    }
    files.sort((a, b) => b.path.compareTo(a.path));
    final latest = File(files.first.path);
    final stat = await latest.stat();
    if (mounted) setState(() => _lastBackupInfo = stat.modified.toString());
  }

  Future<void> _loadPermissionStatus() async {
    final locationPermission = await Geolocator.checkPermission();
    final notificationsEnabled = await NotificationService.instance.areNotificationsEnabled();
    if (mounted) {
      setState(() {
        _locationPermission = locationPermission;
        _notificationsEnabled = notificationsEnabled;
      });
    }
  }

  Future<void> _createBackup() async {
    setState(() => _busy = true);
    final prefs = await SharedPreferences.getInstance();
    final data = {for (final key in prefs.getKeys()) key: prefs.get(key)};
    final dir = await _backupDir();
    final timestamp = DateTime.now().toIso8601String().replaceAll(':', '-');
    final file = File('${dir.path}/misbaha_backup_$timestamp.json');
    await file.writeAsString(jsonEncode(data));
    await _loadBackupInfo();
    if (mounted) {
      setState(() => _busy = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(context.loc.t('settings_backup_created'))));
    }
  }

  Future<void> _restoreLatestBackup() async {
    final dir = await _backupDir();
    final files = await dir.list().where((e) => e is File && e.path.endsWith('.json')).toList();
    if (files.isEmpty) return;
    files.sort((a, b) => b.path.compareTo(a.path));
    setState(() => _busy = true);
    final content = await File(files.first.path).readAsString();
    final data = jsonDecode(content) as Map<String, dynamic>;
    final prefs = await SharedPreferences.getInstance();
    for (final entry in data.entries) {
      final value = entry.value;
      if (value is bool) {
        await prefs.setBool(entry.key, value);
      } else if (value is int) {
        await prefs.setInt(entry.key, value);
      } else if (value is double) {
        await prefs.setDouble(entry.key, value);
      } else if (value is String) {
        await prefs.setString(entry.key, value);
      } else if (value is List) {
        await prefs.setStringList(entry.key, value.map((e) => '$e').toList());
      }
    }
    if (mounted) {
      setState(() => _busy = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(context.loc.t('settings_backup_restored'))));
    }
  }

  Future<void> _confirmResetData() async {
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
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(t('settings_reset_all_data_done'))));
      }
    }
  }

  String _locationPermissionLabel(String Function(String) t, LocationPermission? p) => switch (p) {
        null => t('settings_calculating'),
        LocationPermission.always || LocationPermission.whileInUse => t('settings_permission_granted'),
        LocationPermission.denied || LocationPermission.deniedForever => t('settings_permission_denied'),
        LocationPermission.unableToDetermine => t('settings_permission_unknown'),
      };

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(t('settings_data_centre'))),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 8),
        children: [
          _SectionHeader(t('settings_backup')),
          ListTile(
            leading: const Icon(Icons.save_outlined),
            title: Text(t('settings_local_backup')),
            subtitle: Text(_lastBackupInfo == null ? t('settings_no_backup_yet') : context.loc.tArgs('settings_last_backup', [_lastBackupInfo!])),
            trailing: FilledButton(
              onPressed: _busy ? null : _createBackup,
              child: Text(t('settings_backup_now')),
            ),
          ),
          if (_lastBackupInfo != null)
            ListTile(
              leading: const Icon(Icons.restore_outlined),
              title: Text(t('settings_restore_backup')),
              subtitle: Text(t('settings_restore_backup_subtitle')),
              trailing: OutlinedButton(
                onPressed: _busy ? null : _restoreLatestBackup,
                child: Text(t('settings_restore')),
              ),
            ),
          ListTile(
            leading: Icon(Icons.cloud_off_outlined, color: theme.colorScheme.onSurfaceVariant),
            title: Text(t('settings_cloud_backup')),
            subtitle: Text(t('settings_cloud_backup_subtitle')),
          ),
          const Divider(height: 24),
          _SectionHeader(t('settings_privacy')),
          ListTile(
            leading: const Icon(Icons.location_on_outlined),
            title: Text(t('settings_permission_location')),
            subtitle: Text(_locationPermissionLabel(t, _locationPermission)),
          ),
          ListTile(
            leading: const Icon(Icons.notifications_outlined),
            title: Text(t('settings_permission_notifications')),
            subtitle: Text(_notificationsEnabled == null
                ? t('settings_calculating')
                : (_notificationsEnabled! ? t('settings_permission_granted') : t('settings_permission_denied'))),
          ),
          const Divider(height: 24),
          _SectionHeader(t('settings_advanced')),
          ListTile(
            leading: const Icon(Icons.info_outline),
            title: Text(t('settings_app_version')),
            subtitle: Text(_version ?? t('settings_calculating')),
          ),
          ListTile(
            leading: Icon(Icons.delete_forever_outlined, color: theme.colorScheme.error),
            title: Text(t('settings_reset_all_data'), style: TextStyle(color: theme.colorScheme.error)),
            subtitle: Text(t('settings_reset_all_data_subtitle')),
            onTap: _confirmResetData,
          ),
        ],
      ),
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
      child: Text(label, style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.secondary)),
    );
  }
}
