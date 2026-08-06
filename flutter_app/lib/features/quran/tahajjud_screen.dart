import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:provider/provider.dart';
import 'package:wakelock_plus/wakelock_plus.dart';

import '../../core/database/quran_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/quran_chapter.dart';
import '../../core/models/quran_verse.dart';
import 'widgets/mushaf_flow_text.dart';

enum TahajjudSpeed { verySlow, slow, medium, fast, custom }

const _tahajjudSpeedPxPerSecond = {
  TahajjudSpeed.verySlow: 8.0,
  TahajjudSpeed.slow: 16.0,
  TahajjudSpeed.medium: 30.0,
  TahajjudSpeed.fast: 48.0,
};

const _minCustomSpeed = 4.0;
const _maxCustomSpeed = 70.0;

/// Hands-free auto-scrolling reciter view for Tahajjud/Qiyam al-Layl: dark,
/// warm, low-glare colours; smooth continuous scroll driven by a frame
/// Ticker (not repeated animateTo calls, which would visibly stutter); the
/// screen stays awake for the whole session via wakelock_plus.
class TahajjudScreen extends StatefulWidget {
  const TahajjudScreen({super.key, required this.title, required this.verses});

  final String title;
  final List<QuranVerse> verses;

  @override
  State<TahajjudScreen> createState() => _TahajjudScreenState();
}

class _TahajjudScreenState extends State<TahajjudScreen> with SingleTickerProviderStateMixin {
  late final Ticker _ticker;
  final _scrollController = ScrollController();
  Duration _lastTick = Duration.zero;
  bool _playing = false;
  double _pxPerSecond = _tahajjudSpeedPxPerSecond[TahajjudSpeed.slow]!;
  Map<int, QuranChapter> _chaptersById = const {};

  static const _bg = Color(0xFF0B0F14);
  static const _text = Color(0xFFE9D9A8);
  static const _accent = Color(0xFFC9A227);

  @override
  void initState() {
    super.initState();
    _ticker = createTicker(_onTick);
    _loadChapters();
  }

  Future<void> _loadChapters() async {
    final chapters = await context.read<QuranRepository>().chapters();
    if (!mounted) return;
    setState(() => _chaptersById = {for (final c in chapters) c.number: c});
  }

  void _onTick(Duration elapsed) {
    if (!_scrollController.hasClients) return;
    final dt = (elapsed - _lastTick).inMicroseconds / 1e6;
    _lastTick = elapsed;
    final maxExtent = _scrollController.position.maxScrollExtent;
    final next = (_scrollController.offset + _pxPerSecond * dt).clamp(0.0, maxExtent).toDouble();
    _scrollController.jumpTo(next);
    if (next >= maxExtent && maxExtent > 0) {
      _pause();
    }
  }

  void _play() {
    WakelockPlus.enable();
    _lastTick = Duration.zero;
    _ticker.start();
    setState(() => _playing = true);
  }

  void _pause() {
    _ticker.stop();
    WakelockPlus.disable();
    if (mounted) setState(() => _playing = false);
  }

  @override
  void dispose() {
    _ticker.dispose();
    WakelockPlus.disable();
    _scrollController.dispose();
    super.dispose();
  }

  String _speedLabel(String Function(String) t, TahajjudSpeed s) => switch (s) {
        TahajjudSpeed.verySlow => t('tahajjud_speed_very_slow'),
        TahajjudSpeed.slow => t('tahajjud_speed_slow'),
        TahajjudSpeed.medium => t('tahajjud_speed_medium'),
        TahajjudSpeed.fast => t('tahajjud_speed_fast'),
        TahajjudSpeed.custom => t('tahajjud_speed_custom'),
      };

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    return Scaffold(
      backgroundColor: _bg,
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 4),
              child: Row(
                children: [
                  IconButton(icon: const Icon(Icons.close, color: _text), onPressed: () => Navigator.of(context).maybePop()),
                  Expanded(
                    child: Text(
                      t('quran_tahajjud_mode'),
                      style: const TextStyle(color: _text, fontWeight: FontWeight.w600),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  PopupMenuButton<TahajjudSpeed>(
                    icon: const Icon(Icons.speed, color: _accent),
                    tooltip: t('tahajjud_speed'),
                    onSelected: (s) => setState(() => _pxPerSecond = _tahajjudSpeedPxPerSecond[s]!),
                    itemBuilder: (context) => TahajjudSpeed.values
                        .where((s) => s != TahajjudSpeed.custom)
                        .map((s) => PopupMenuItem(value: s, child: Text(_speedLabel(t, s))))
                        .toList(),
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Row(
                children: [
                  Icon(Icons.slow_motion_video, size: 18, color: _text.withOpacity(0.6)),
                  Expanded(
                    child: SliderTheme(
                      data: SliderTheme.of(context).copyWith(activeTrackColor: _accent, thumbColor: _accent),
                      child: Slider(
                        value: _pxPerSecond.clamp(_minCustomSpeed, _maxCustomSpeed).toDouble(),
                        min: _minCustomSpeed,
                        max: _maxCustomSpeed,
                        onChanged: (v) => setState(() => _pxPerSecond = v),
                      ),
                    ),
                  ),
                  Icon(Icons.fast_forward, size: 18, color: _text.withOpacity(0.6)),
                ],
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                controller: _scrollController,
                padding: const EdgeInsets.fromLTRB(20, 12, 20, 120),
                child: MushafFlowText(
                  verses: widget.verses,
                  chapters: _chaptersById,
                  textColor: _text,
                  accentColor: _accent,
                ),
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: _accent,
        foregroundColor: Colors.black,
        onPressed: _playing ? _pause : _play,
        icon: Icon(_playing ? Icons.pause : Icons.play_arrow),
        label: Text(_playing ? t('quran_pause_recitation') : t('tahajjud_start')),
      ),
    );
  }
}
