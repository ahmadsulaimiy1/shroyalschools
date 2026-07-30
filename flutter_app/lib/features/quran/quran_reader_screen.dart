import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/quran_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/quran_chapter.dart';
import '../../core/models/quran_verse.dart';
import '../../core/services/quran/quran_audio_controller.dart';
import '../../core/services/quran/quran_audio_service.dart';
import '../../core/services/settings_controller.dart';
import '../../core/services/tts/adhkar_audio_handler.dart' show RepeatMode;
import '../../core/theme/app_colors.dart';
import 'tahajjud_screen.dart';
import 'widgets/mushaf_flow_text.dart';
import 'widgets/quran_verse_card.dart';

/// Generic verse-by-verse reader — used for a single surah, a juz range,
/// bookmarks, favourites, and search results alike, since they're all just
/// "a list of verses with a title" once resolved.
class QuranReaderScreen extends StatefulWidget {
  const QuranReaderScreen({super.key, required this.title, required this.verses, this.scrollToAyah});

  final String title;
  final List<QuranVerse> verses;

  /// If set, the reader scrolls to this ayah number on open (used when
  /// jumping into a surah from a search result or a bookmark).
  final int? scrollToAyah;

  @override
  State<QuranReaderScreen> createState() => _QuranReaderScreenState();
}

class _QuranReaderScreenState extends State<QuranReaderScreen> {
  final _scrollController = ScrollController();
  Map<int, QuranChapter> _chaptersById = const {};

  /// Reading Focus Mode: tapping the page hides the app bar/chrome so the
  /// text fills the screen; tapping again brings it back.
  bool _focusMode = false;

  @override
  void initState() {
    super.initState();
    if (widget.verses.isNotEmpty) {
      final last = widget.verses.last;
      context.read<QuranRepository>().setLastRead(last.surah, last.ayah);
    }
    _loadChapters();
    if (widget.scrollToAyah != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        final index = widget.verses.indexWhere((v) => v.ayah == widget.scrollToAyah);
        if (index > 0 && _scrollController.hasClients) {
          _scrollController.animateTo(
            index * 280.0,
            duration: const Duration(milliseconds: 400),
            curve: Curves.easeOut,
          );
        }
      });
    }
  }

  Future<void> _loadChapters() async {
    final chapters = await context.read<QuranRepository>().chapters();
    if (!mounted) return;
    setState(() => _chaptersById = {for (final c in chapters) c.number: c});
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final settings = context.watch<SettingsController>();
    final audio = context.watch<QuranAudioController>();
    final t = context.loc.t;
    final isMushaf = settings.quranMushafMode;

    final toolbar = ClipRect(
      child: AnimatedAlign(
        alignment: Alignment.topCenter,
        heightFactor: _focusMode ? 0.0 : 1.0,
        duration: const Duration(milliseconds: 220),
        curve: Curves.easeOut,
        child: SafeArea(
          bottom: false,
          child: Material(
            elevation: 2,
            color: isMushaf ? AppColors.navy : Theme.of(context).appBarTheme.backgroundColor,
            child: Row(
              children: [
                IconButton(
                  icon: Icon(Icons.arrow_back, color: isMushaf ? Colors.white : null),
                  onPressed: () => Navigator.of(context).maybePop(),
                ),
                Expanded(
                  child: Text(
                    widget.title,
                    overflow: TextOverflow.ellipsis,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(color: isMushaf ? Colors.white : null),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.bedtime_outlined, color: isMushaf ? AppColors.gold : null),
                  tooltip: t('quran_tahajjud_mode'),
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute(builder: (_) => TahajjudScreen(title: widget.title, verses: widget.verses)),
                  ),
                ),
                IconButton(
                  icon: Icon(isMushaf ? Icons.menu_book : Icons.menu_book_outlined, color: isMushaf ? AppColors.gold : null),
                  tooltip: t('quran_mushaf_mode'),
                  onPressed: () => context.read<SettingsController>().setQuranMushafMode(!isMushaf),
                ),
                PopupMenuButton<String>(
                  icon: Icon(Icons.playlist_play, color: isMushaf ? AppColors.gold : null),
                  tooltip: t('quran_playback_options'),
                  onSelected: (action) {
                    final audioController = context.read<QuranAudioController>();
                    if (action == 'play_all') {
                      audioController.setMemorizationMode(false);
                      if (widget.verses.isNotEmpty) {
                        audioController.setRepeatMode(RepeatMode.continuous);
                        audioController.playVerse(widget.verses.first, playlist: widget.verses, index: 0);
                      }
                    } else if (action == 'toggle_memorization') {
                      final enabling = !audio.memorizationMode;
                      audioController.setMemorizationMode(enabling);
                      if (enabling && widget.verses.isNotEmpty) {
                        audioController.playVerse(widget.verses.first, playlist: widget.verses, index: 0);
                      }
                    }
                  },
                  itemBuilder: (context) => [
                    PopupMenuItem(value: 'play_all', child: Text(t('quran_play_surah_juz'))),
                    CheckedPopupMenuItem(
                      value: 'toggle_memorization',
                      checked: audio.memorizationMode,
                      child: Text(t('quran_memorization_mode')),
                    ),
                  ],
                ),
                PopupMenuButton<QuranReciter>(
                  icon: Icon(Icons.record_voice_over_outlined, color: isMushaf ? AppColors.gold : null),
                  tooltip: t('quran_reciter'),
                  initialValue: audio.reciter,
                  onSelected: (r) => context.read<QuranAudioController>().setReciter(r),
                  itemBuilder: (context) => QuranReciter.values
                      .map((r) => CheckedPopupMenuItem(value: r, checked: audio.reciter == r, child: Text(r.displayName)))
                      .toList(),
                ),
                if (!isMushaf)
                  PopupMenuButton<QuranReadingMode>(
                    icon: const Icon(Icons.text_fields),
                    tooltip: t('quran_reading_mode'),
                    initialValue: settings.quranReadingMode,
                    onSelected: (mode) => context.read<SettingsController>().setQuranReadingMode(mode),
                    itemBuilder: (context) => [
                      CheckedPopupMenuItem(
                        value: QuranReadingMode.arabicOnly,
                        checked: settings.quranReadingMode == QuranReadingMode.arabicOnly,
                        child: Text(t('quran_mode_arabic_only')),
                      ),
                      CheckedPopupMenuItem(
                        value: QuranReadingMode.arabicTranslation,
                        checked: settings.quranReadingMode == QuranReadingMode.arabicTranslation,
                        child: Text(t('quran_mode_arabic_translation')),
                      ),
                      CheckedPopupMenuItem(
                        value: QuranReadingMode.arabicTranslationTransliteration,
                        checked: settings.quranReadingMode == QuranReadingMode.arabicTranslationTransliteration,
                        child: Text(t('quran_mode_arabic_translation_transliteration')),
                      ),
                    ],
                  ),
              ],
            ),
          ),
        ),
      ),
    );

    final body = GestureDetector(
      behavior: HitTestBehavior.translucent,
      onTap: () => setState(() => _focusMode = !_focusMode),
      child: isMushaf
          ? Container(
              padding: const EdgeInsets.all(8),
              // Royal Mushaf page frame: a restrained double gold border
              // around the whole reading surface, echoing the ornamental
              // border printed on a real Mushaf page without competing
              // with the text itself.
              decoration: BoxDecoration(
                color: AppColors.surfaceLight,
                border: Border.all(color: AppColors.gold.withOpacity(0.5), width: 1),
              ),
              child: Container(
                decoration: BoxDecoration(border: Border.all(color: AppColors.gold, width: 2)),
                child: SingleChildScrollView(
                  controller: _scrollController,
                  padding: const EdgeInsets.fromLTRB(20, 16, 20, 40),
                  child: MushafFlowText(
                    verses: widget.verses,
                    chapters: _chaptersById,
                    textColor: AppColors.textPrimaryLight,
                    accentColor: AppColors.gold,
                    fontScale: settings.effectiveTextScale,
                  ),
                ),
              ),
            )
          : ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: widget.verses.length,
              itemBuilder: (context, i) => QuranVerseCard(
                verse: widget.verses[i],
                playlist: widget.verses,
                index: i,
                fontScale: settings.effectiveTextScale,
                readingMode: settings.quranReadingMode,
              ),
            ),
    );

    return Scaffold(
      body: Column(
        children: [
          toolbar,
          Expanded(child: body),
        ],
      ),
    );
  }
}
