import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/services/quran/quran_audio_controller.dart';
import '../../core/services/quran/quran_audio_service.dart';
import '../../core/services/tts/tts_controller.dart';
import '../../core/theme/app_colors.dart';
import '../quran/reciter_centre_screen.dart';

/// Audio: Qari reciter + Qur'an playback speed, Adhkar TTS voice + speed,
/// a sleep timer that pauses whichever engine is currently playing, and
/// downloaded-recitation cache management (the directive's "Downloads"
/// section -- TTS voices themselves are installed at the OS level via
/// Android Settings, not something this app can download directly, so
/// only cached Qur'an audio appears here).
class AudioSettingsScreen extends StatefulWidget {
  const AudioSettingsScreen({super.key});

  @override
  State<AudioSettingsScreen> createState() => _AudioSettingsScreenState();
}

class _AudioSettingsScreenState extends State<AudioSettingsScreen> {
  int? _cacheBytes;
  bool _clearingCache = false;
  Duration? _sleepTimerRemaining;
  Timer? _sleepTimerTicker;

  @override
  void initState() {
    super.initState();
    _loadCacheSize();
  }

  @override
  void dispose() {
    _sleepTimerTicker?.cancel();
    super.dispose();
  }

  Future<void> _loadCacheSize() async {
    final bytes = await context.read<QuranAudioService>().cacheSizeBytes();
    if (mounted) setState(() => _cacheBytes = bytes);
  }

  Future<void> _clearCache() async {
    setState(() => _clearingCache = true);
    await context.read<QuranAudioService>().clearCache();
    if (mounted) setState(() => _clearingCache = false);
    await _loadCacheSize();
  }

  String _formatBytes(int bytes) {
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(0)} KB';
    return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
  }

  void _startSleepTimer(Duration duration) {
    _sleepTimerTicker?.cancel();
    setState(() => _sleepTimerRemaining = duration);
    _sleepTimerTicker = Timer.periodic(const Duration(seconds: 1), (timer) {
      final remaining = _sleepTimerRemaining;
      if (remaining == null || remaining.inSeconds <= 1) {
        timer.cancel();
        context.read<TtsController>().pause();
        context.read<QuranAudioController>().pause();
        if (mounted) setState(() => _sleepTimerRemaining = null);
        return;
      }
      if (mounted) setState(() => _sleepTimerRemaining = remaining - const Duration(seconds: 1));
    });
  }

  void _cancelSleepTimer() {
    _sleepTimerTicker?.cancel();
    setState(() => _sleepTimerRemaining = null);
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);
    final quranAudio = context.watch<QuranAudioController>();
    final tts = context.watch<TtsController>();

    return Scaffold(
      appBar: AppBar(title: Text(t('settings_audio'))),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 8),
        children: [
          _SectionHeader(t('settings_audio_quran')),
          ListTile(
            leading: const Icon(Icons.record_voice_over_outlined),
            title: Text(t('quran_reciter')),
            subtitle: Text(quranAudio.reciter.displayName),
            onTap: () => _pickReciter(context, quranAudio),
          ),
          ListTile(
            leading: const Icon(Icons.library_music_outlined),
            title: Text(t('settings_reciter_centre')),
            subtitle: Text(t('settings_reciter_centre_subtitle')),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const ReciterCentreScreen())),
          ),
          ListTile(
            leading: const Icon(Icons.speed_outlined),
            title: Text(t('settings_playback_speed')),
            subtitle: Slider(
              value: quranAudio.speed.clamp(0.5, 2.0),
              min: 0.5,
              max: 2.0,
              divisions: 6,
              label: '${quranAudio.speed.toStringAsFixed(2)}x',
              onChanged: (v) => context.read<QuranAudioController>().setSpeed(v),
            ),
          ),
          const Divider(height: 24),
          _SectionHeader(t('settings_audio_adhkar')),
          if (tts.hasArabicVoice)
            ListTile(
              leading: const Icon(Icons.record_voice_over_outlined),
              title: Text(t('settings_tts_arabic_voice')),
              subtitle: Text(tts.selectedArabicVoice ?? t('settings_tts_voice_default')),
              onTap: () => _pickVoice(context, tts, arabic: true),
            ),
          if (tts.hasEnglishVoice)
            ListTile(
              leading: const Icon(Icons.record_voice_over_outlined),
              title: Text(t('settings_tts_english_voice')),
              subtitle: Text(tts.selectedEnglishVoice ?? t('settings_tts_voice_default')),
              onTap: () => _pickVoice(context, tts, arabic: false),
            ),
          if (!tts.hasArabicVoice && !tts.hasEnglishVoice)
            ListTile(
              leading: Icon(Icons.warning_amber_outlined, color: theme.colorScheme.error),
              title: Text(t('settings_tts_no_voices')),
              subtitle: Text(t('settings_tts_no_voices_subtitle')),
            ),
          ListTile(
            leading: const Icon(Icons.speed_outlined),
            title: Text(t('settings_playback_speed')),
            subtitle: Slider(
              value: tts.speechRate.clamp(0.1, 1.0),
              min: 0.1,
              max: 1.0,
              divisions: 9,
              label: tts.speechRate.toStringAsFixed(2),
              onChanged: (v) => context.read<TtsController>().setSpeed(v),
            ),
          ),
          const Divider(height: 24),
          _SectionHeader(t('settings_sleep_timer')),
          if (_sleepTimerRemaining != null)
            Card(
              color: AppColors.navy,
              child: ListTile(
                leading: const Icon(Icons.bedtime_outlined, color: AppColors.gold),
                title: Text(
                  context.loc.tArgs('settings_sleep_timer_active', [_formatDuration(_sleepTimerRemaining!)]),
                  style: const TextStyle(color: Colors.white),
                ),
                trailing: TextButton(
                  onPressed: _cancelSleepTimer,
                  child: Text(t('settings_sleep_timer_cancel'), style: const TextStyle(color: AppColors.gold)),
                ),
              ),
            )
          else
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  for (final minutes in [5, 10, 15, 30, 45, 60])
                    OutlinedButton(
                      onPressed: () => _startSleepTimer(Duration(minutes: minutes)),
                      child: Text(context.loc.tArgs('settings_sleep_timer_minutes', [minutes])),
                    ),
                ],
              ),
            ),
          const Divider(height: 24),
          _SectionHeader(t('settings_downloads')),
          ListTile(
            leading: const Icon(Icons.storage_outlined),
            title: Text(t('settings_cached_audio')),
            subtitle: Text(_cacheBytes == null ? t('settings_calculating') : _formatBytes(_cacheBytes!)),
            trailing: _clearingCache
                ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                : TextButton(
                    onPressed: (_cacheBytes ?? 0) > 0 ? _clearCache : null,
                    child: Text(t('settings_clear_cache')),
                  ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Text(
              t('settings_downloads_footnote'),
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
          ),
        ],
      ),
    );
  }

  String _formatDuration(Duration d) {
    final m = d.inMinutes.toString().padLeft(2, '0');
    final s = (d.inSeconds % 60).toString().padLeft(2, '0');
    return '$m:$s';
  }

  void _pickReciter(BuildContext context, QuranAudioController controller) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (sheetContext) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            for (final reciter in QuranReciter.values)
              RadioListTile<QuranReciter>(
                value: reciter,
                groupValue: controller.reciter,
                title: Text(reciter.displayName),
                onChanged: (v) {
                  if (v != null) controller.setReciter(v);
                  Navigator.pop(sheetContext);
                },
              ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }

  void _pickVoice(BuildContext context, TtsController tts, {required bool arabic}) {
    final t = context.loc.t;
    final voices = arabic ? tts.arabicVoices : tts.englishVoices;
    final current = arabic ? tts.selectedArabicVoice : tts.selectedEnglishVoice;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (sheetContext) => SafeArea(
        child: ConstrainedBox(
          constraints: BoxConstraints(maxHeight: MediaQuery.of(sheetContext).size.height * 0.6),
          child: ListView(
            shrinkWrap: true,
            children: [
              RadioListTile<String?>(
                value: null,
                groupValue: current,
                title: Text(t('settings_tts_voice_default')),
                onChanged: (v) {
                  if (arabic) {
                    tts.setArabicVoice(null);
                  } else {
                    tts.setEnglishVoice(null);
                  }
                  Navigator.pop(sheetContext);
                },
              ),
              for (final voice in voices)
                RadioListTile<String?>(
                  value: voice['name'],
                  groupValue: current,
                  title: Text(voice['name'] ?? ''),
                  subtitle: Text(voice['locale'] ?? ''),
                  onChanged: (v) {
                    if (arabic) {
                      tts.setArabicVoice(v);
                    } else {
                      tts.setEnglishVoice(v);
                    }
                    Navigator.pop(sheetContext);
                  },
                ),
              const SizedBox(height: 8),
            ],
          ),
        ),
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
