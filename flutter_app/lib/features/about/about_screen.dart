import 'package:flutter/material.dart';
import 'package:package_info_plus/package_info_plus.dart' as pkg;

import '../../core/localization/app_localizations.dart';

class AboutScreen extends StatefulWidget {
  const AboutScreen({super.key});

  @override
  State<AboutScreen> createState() => _AboutScreenState();
}

class _AboutScreenState extends State<AboutScreen> {
  String _version = '1.0.0';

  @override
  void initState() {
    super.initState();
    _loadVersion();
  }

  Future<void> _loadVersion() async {
    try {
      final info = await pkg.PackageInfo.fromPlatform();
      if (mounted) setState(() => _version = '${info.version} (${info.buildNumber})');
    } catch (_) {
      // Keep the fallback version string — non-critical.
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;

    return Scaffold(
      appBar: AppBar(title: Text(t('about_title'))),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          Center(
            child: Container(
              width: 88,
              height: 88,
              decoration: BoxDecoration(color: theme.colorScheme.primary, borderRadius: BorderRadius.circular(24)),
              child: Icon(Icons.fingerprint, color: theme.colorScheme.secondary, size: 48),
            ),
          ),
          const SizedBox(height: 16),
          Center(child: Text(t('about_app_name'), style: theme.textTheme.titleLarge, textAlign: TextAlign.center)),
          const SizedBox(height: 4),
          Center(
            child: Text(
              '${t('about_version')} $_version',
              style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
          ),
          const SizedBox(height: 24),
          Text(t('about_description'), style: theme.textTheme.bodyLarge, textAlign: TextAlign.center),
          const SizedBox(height: 24),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  _InfoRow(icon: Icons.wifi_off_outlined, text: t('about_offline_notice')),
                  const SizedBox(height: 12),
                  _InfoRow(icon: Icons.lock_outline, text: t('about_privacy')),
                  const SizedBox(height: 12),
                  _InfoRow(icon: Icons.flutter_dash_outlined, text: t('about_made_with')),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  const _InfoRow({required this.icon, required this.text});
  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Row(
      children: [
        Icon(icon, color: theme.colorScheme.secondary),
        const SizedBox(width: 12),
        Expanded(child: Text(text, style: theme.textTheme.bodyMedium)),
      ],
    );
  }
}
