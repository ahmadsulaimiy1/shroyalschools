import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/localization/app_localizations.dart';
import '../../../core/models/adhkar_entry.dart';
import '../../../core/services/tts/adhkar_audio_handler.dart';
import '../../../core/services/tts/tts_controller.dart';

/// Play/pause/stop/repeat/speed/voice controls for reading an [AdhkarEntry]
/// (or a whole category as a continuous-reading playlist) aloud via the
/// offline device TTS engine. See core/services/tts/ for the underlying
/// audio_service + flutter_tts integration this drives.
class TtsControlBar extends StatelessWidget {
  const TtsControlBar({
    super.key,
    required this.entry,
    this.playlist,
    this.index,
  });

  final AdhkarEntry entry;
  final List<AdhkarEntry>? playlist;
  final int? index;

  @override
  Widget build(BuildContext context) {
    final tts = context.watch<TtsController>();
    final t = context.loc.t;
    final theme = Theme.of(context);
    final isCurrent = tts.currentEntry?.id == entry.id;
    final isPlaying = isCurrent && tts.status == TtsPlaybackStatus.playing;
    final isPaused = isCurrent && tts.status == TtsPlaybackStatus.paused;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            if (!tts.hasArabicVoice)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: _MissingVoiceBanner(languageLabel: t('settings_language_arabic')),
              ),
            Row(
              children: [
                IconButton.filled(
                  iconSize: 32,
                  icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
                  tooltip: isPlaying ? t('tts_pause') : t('tts_play'),
                  onPressed: () {
                    if (isPlaying) {
                      tts.pause();
                    } else if (isPaused) {
                      tts.resume();
                    } else {
                      tts.playEntry(entry, playlist: playlist, index: index);
                    }
                  },
                ),
                IconButton(
                  icon: const Icon(Icons.stop),
                  tooltip: t('tts_stop'),
                  onPressed: isCurrent ? tts.stop : null,
                ),
                IconButton(
                  icon: const Icon(Icons.replay),
                  tooltip: t('tts_repeat_this'),
                  onPressed: () => tts.playEntry(entry, playlist: playlist, index: index),
                ),
                const Spacer(),
                PopupMenuButton<double>(
                  tooltip: t('tts_speed'),
                  initialValue: tts.speechRate,
                  onSelected: tts.setSpeed,
                  itemBuilder: (context) => const [0.3, 0.45, 0.6, 0.8]
                      .map((r) => PopupMenuItem(value: r, child: Text('${(r * 2).toStringAsFixed(1)}x')))
                      .toList(),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.speed),
                      const SizedBox(width: 4),
                      Text('${(tts.speechRate * 2).toStringAsFixed(1)}x'),
                    ],
                  ),
                ),
              ],
            ),
            Row(
              children: [
                Expanded(
                  child: SegmentedButton<RepeatMode>(
                    segments: [
                      ButtonSegment(value: RepeatMode.off, label: Text(t('tts_repeat_off'))),
                      ButtonSegment(value: RepeatMode.repeatOne, label: Text(t('tts_repeat_one'))),
                      ButtonSegment(value: RepeatMode.continuous, label: Text(t('tts_continuous'))),
                    ],
                    selected: {tts.repeatMode},
                    onSelectionChanged: (s) => tts.setRepeatMode(s.first),
                    style: const ButtonStyle(visualDensity: VisualDensity.compact),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _MissingVoiceBanner extends StatelessWidget {
  const _MissingVoiceBanner({required this.languageLabel});
  final String languageLabel;

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: theme.colorScheme.error.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Icon(Icons.warning_amber_rounded, color: theme.colorScheme.error, size: 20),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              context.loc.tArgs('tts_no_voice_installed', [languageLabel]),
              style: theme.textTheme.labelLarge,
            ),
          ),
        ],
      ),
    );
  }
}
