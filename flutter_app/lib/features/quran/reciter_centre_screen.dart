import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/quran_repository.dart' show totalQuranVerseCount;
import '../../core/localization/app_localizations.dart';
import '../../core/services/quran/quran_audio_controller.dart';
import '../../core/services/quran/quran_audio_service.dart';
import '../../core/services/quran/reciter_download_controller.dart';

/// The Reciter Centre: browse every verified reciter, download their full
/// Qur'an recitation once for permanent offline playback, and manage that
/// storage (pause/resume/delete). Separate from the quick reciter picker in
/// Audio Settings / the reader toolbar, which only chooses which reciter
/// plays -- this screen is about what's actually stored on the device.
///
/// Downloaded recitation is never bundled inside the APK: every reciter
/// pack here is fetched on demand from everyayah.com's public per-ayah CDN
/// (the same verified source the app already streams from), so the app
/// stays small until a user deliberately chooses to go fully offline with a
/// given reciter.
class ReciterCentreScreen extends StatefulWidget {
  const ReciterCentreScreen({super.key});

  @override
  State<ReciterCentreScreen> createState() => _ReciterCentreScreenState();
}

class _ReciterCentreScreenState extends State<ReciterCentreScreen> {
  final Map<QuranReciter, int> _bytes = {};

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      final controller = context.read<ReciterDownloadController>();
      await controller.refreshAllCounts();
      for (final reciter in QuranReciter.values) {
        final bytes = await controller.downloadedBytes(reciter);
        if (mounted) setState(() => _bytes[reciter] = bytes);
      }
    });
  }

  String _formatBytes(int bytes) {
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(0)} KB';
    return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
  }

  Future<void> _confirmDelete(BuildContext context, QuranReciter reciter) async {
    final t = context.loc.t;
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(t('reciter_delete_confirm_title')),
        content: Text(context.loc.tArgs('reciter_delete_confirm_body', [reciter.displayName])),
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
      await context.read<ReciterDownloadController>().delete(reciter);
      if (mounted) setState(() => _bytes[reciter] = 0);
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);
    final downloads = context.watch<ReciterDownloadController>();
    final activeReciter = context.watch<QuranAudioController>().reciter;

    return Scaffold(
      appBar: AppBar(title: Text(t('reciter_centre_title'))),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(t('reciter_centre_subtitle'), style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
          const SizedBox(height: 16),
          for (final reciter in QuranReciter.values) ...[
            _ReciterTile(
              reciter: reciter,
              isActive: reciter == activeReciter,
              downloadedCount: downloads.downloadedCount(reciter),
              downloading: downloads.isDownloading(reciter),
              complete: downloads.isComplete(reciter),
              bytes: _bytes[reciter],
              onSetActive: () => context.read<QuranAudioController>().setReciter(reciter),
              onDownload: () => downloads.download(reciter),
              onPause: () => downloads.pause(reciter),
              onDelete: () => _confirmDelete(context, reciter),
              formatBytes: _formatBytes,
            ),
            const SizedBox(height: 12),
          ],
        ],
      ),
    );
  }
}

class _ReciterTile extends StatelessWidget {
  const _ReciterTile({
    required this.reciter,
    required this.isActive,
    required this.downloadedCount,
    required this.downloading,
    required this.complete,
    required this.bytes,
    required this.onSetActive,
    required this.onDownload,
    required this.onPause,
    required this.onDelete,
    required this.formatBytes,
  });

  final QuranReciter reciter;
  final bool isActive;
  final int downloadedCount;
  final bool downloading;
  final bool complete;
  final int? bytes;
  final VoidCallback onSetActive;
  final VoidCallback onDownload;
  final VoidCallback onPause;
  final VoidCallback onDelete;
  final String Function(int) formatBytes;

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);
    final progress = downloadedCount / totalQuranVerseCount;
    final started = downloadedCount > 0;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Row(
                    children: [
                      Flexible(child: Text(reciter.displayName, style: theme.textTheme.titleMedium)),
                      if (isActive) ...[
                        const SizedBox(width: 8),
                        Chip(
                          label: Text(t('reciter_active_badge'), style: theme.textTheme.labelSmall),
                          visualDensity: VisualDensity.compact,
                          materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                        ),
                      ],
                    ],
                  ),
                ),
                if (!isActive)
                  TextButton(onPressed: onSetActive, child: Text(t('reciter_set_active'))),
              ],
            ),
            const SizedBox(height: 8),
            if (complete)
              Text(
                context.loc.tArgs('reciter_downloaded_complete', [bytes == null ? '…' : formatBytes(bytes!)]),
                style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.secondary),
              )
            else ...[
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(value: downloading && !started ? null : progress, minHeight: 6),
              ),
              const SizedBox(height: 6),
              Text(
                context.loc.tArgs('reciter_centre_progress', [downloadedCount, totalQuranVerseCount]),
                style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
              ),
            ],
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                if (started) TextButton(onPressed: onDelete, child: Text(t('reciter_delete'))),
                const SizedBox(width: 4),
                if (downloading)
                  OutlinedButton(onPressed: onPause, child: Text(t('reciter_pause')))
                else if (!complete)
                  FilledButton(onPressed: onDownload, child: Text(started ? t('reciter_resume') : t('reciter_download'))),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
