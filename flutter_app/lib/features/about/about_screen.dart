import 'package:flutter/material.dart';
import 'package:package_info_plus/package_info_plus.dart' as pkg;
import 'package:url_launcher/url_launcher.dart';

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

  Future<void> _openUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  Future<void> _openEmail() async {
    final uri = Uri(scheme: 'mailto', path: 'support@misbaha.app');
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;
    final year = DateTime.now().year;

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

          const SizedBox(height: 24),
          _SectionLabel(t('about_developer_section')),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const CircleAvatar(
                        radius: 36,
                        backgroundImage: AssetImage('assets/images/developer.jpg'),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(t('about_developer_name'), style: theme.textTheme.titleMedium),
                            const SizedBox(height: 2),
                            Text(
                              t('about_developer_role'),
                              style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const Divider(height: 28),
                  _InfoRow(icon: Icons.verified_user_outlined, text: '${t('about_islamic_supervision_title')}: ${t('about_islamic_supervision_body')}'),
                  const SizedBox(height: 10),
                  _InfoRow(icon: Icons.fact_check_outlined, text: '${t('about_reviewed_by_title')}: ${t('about_reviewed_by_body')}'),
                  const SizedBox(height: 10),
                  _InfoRow(icon: Icons.workspace_premium_outlined, text: '${t('about_approved_by_title')}: ${t('about_approved_by_body')}'),
                  const SizedBox(height: 10),
                  _InfoRow(icon: Icons.location_on_outlined, text: t('about_location')),
                ],
              ),
            ),
          ),

          const SizedBox(height: 24),
          _SectionLabel(t('about_mission_title')),
          const SizedBox(height: 12),
          Text(t('about_mission_body'), style: theme.textTheme.bodyMedium),

          const SizedBox(height: 24),
          _SectionLabel(t('about_content_source_title')),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(t('about_content_source_body'), style: theme.textTheme.bodyMedium),
            ),
          ),

          const SizedBox(height: 24),
          _SectionLabel(t('about_quran_source_title')),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(t('about_quran_source_body'), style: theme.textTheme.bodyMedium),
            ),
          ),

          const SizedBox(height: 24),
          _SectionLabel(t('about_contact_title')),
          const SizedBox(height: 4),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.language_outlined),
            title: Text(t('about_website')),
            trailing: const Icon(Icons.open_in_new, size: 18),
            onTap: () => _openUrl('https://shroyalschools.com'),
          ),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.email_outlined),
            title: Text(t('about_contact_email')),
            subtitle: const Text('support@misbaha.app'),
            onTap: _openEmail,
          ),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.privacy_tip_outlined),
            title: Text(t('about_privacy_policy')),
            trailing: const Icon(Icons.open_in_new, size: 18),
            onTap: () => _openUrl('https://misbaha.app/privacy'),
          ),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.description_outlined),
            title: Text(t('about_terms_of_service')),
            trailing: const Icon(Icons.open_in_new, size: 18),
            onTap: () => _openUrl('https://misbaha.app/terms'),
          ),

          const SizedBox(height: 24),
          Center(
            child: Text(
              context.loc.tArgs('about_copyright', [year]),
              style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant),
              textAlign: TextAlign.center,
            ),
          ),
        ],
      ),
    );
  }
}

class _SectionLabel extends StatelessWidget {
  const _SectionLabel(this.label);
  final String label;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Text(label, style: theme.textTheme.titleMedium?.copyWith(color: theme.colorScheme.secondary));
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
