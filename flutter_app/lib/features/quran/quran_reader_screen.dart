import 'package:flutter/material.dart' hide RepeatMode;
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
  final _pageController = PageController();
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

  /// Repeat Range: lets the reader pick a start/end ayah from the verses on
  /// screen and loops just that sub-range indefinitely (e.g. one page while
  /// memorising, or one ruku' during reflection) -- distinct from Memorisation
  /// Mode, which repeats each verse individually before advancing.
  void _showRepeatRangeSheet(BuildContext context) {
    if (widget.verses.isEmpty) return;
    final t = context.loc.t;
    var startIndex = 0;
    var endIndex = widget.verses.length - 1;

    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (sheetContext) => StatefulBuilder(
        builder: (sheetContext, setSheetState) {
          return SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(t('quran_repeat_range'), style: Theme.of(sheetContext).textTheme.titleMedium),
                  const SizedBox(height: 4),
                  Text(t('quran_repeat_range_hint'), style: Theme.of(sheetContext).textTheme.bodySmall),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: DropdownButtonFormField<int>(
                          initialValue: startIndex,
                          decoration: InputDecoration(labelText: t('quran_repeat_range_from')),
                          items: [
                            for (var i = 0; i < widget.verses.length; i++)
                              DropdownMenuItem(value: i, child: Text('${widget.verses[i].ayah}')),
                          ],
                          onChanged: (value) => setSheetState(() {
                            startIndex = value ?? startIndex;
                            if (startIndex > endIndex) endIndex = startIndex;
                          }),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: DropdownButtonFormField<int>(
                          initialValue: endIndex,
                          decoration: InputDecoration(labelText: t('quran_repeat_range_to')),
                          items: [
                            for (var i = 0; i < widget.verses.length; i++)
                              DropdownMenuItem(value: i, child: Text('${widget.verses[i].ayah}')),
                          ],
                          onChanged: (value) => setSheetState(() {
                            endIndex = value ?? endIndex;
                            if (endIndex < startIndex) startIndex = endIndex;
                          }),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    child: FilledButton(
                      onPressed: () {
                        final range = widget.verses.sublist(startIndex, endIndex + 1);
                        final audioController = context.read<QuranAudioController>();
                        audioController.setMemorizationMode(false);
                        audioController.setRepeatMode(RepeatMode.continuous);
                        audioController.setLoopPlaylist(true);
                        audioController.playVerse(range.first, playlist: range, index: 0);
                        Navigator.pop(sheetContext);
                      },
                      child: Text(t('quran_repeat_range_start')),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    _pageController.dispose();
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
                      audioController.setLoopPlaylist(false);
                      if (widget.verses.isNotEmpty) {
                        audioController.setRepeatMode(RepeatMode.continuous);
                        audioController.playVerse(widget.verses.first, playlist: widget.verses, index: 0);
                      }
                    } else if (action == 'toggle_memorization') {
                      final enabling = !audio.memorizationMode;
                      audioController.setLoopPlaylist(false);
                      audioController.setMemorizationMode(enabling);
                      if (enabling && widget.verses.isNotEmpty) {
                        audioController.playVerse(widget.verses.first, playlist: widget.verses, index: 0);
                      }
                    } else if (action == 'repeat_range') {
                      _showRepeatRangeSheet(context);
                    }
                  },
                  itemBuilder: (context) => [
                    PopupMenuItem(value: 'play_all', child: Text(t('quran_play_surah_juz'))),
                    CheckedPopupMenuItem(
                      value: 'toggle_memorization',
                      checked: audio.memorizationMode,
                      child: Text(t('quran_memorization_mode')),
                    ),
                    PopupMenuItem(value: 'repeat_range', child: Text(t('quran_repeat_range'))),
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
                  IconButton(
                    icon: Icon(settings.quranScrollMode == QuranScrollMode.horizontalSwipe
                        ? Icons.view_carousel_outlined
                        : Icons.view_agenda_outlined),
                    tooltip: t('quran_scroll_mode'),
                    onPressed: () => context.read<SettingsController>().setQuranScrollMode(
                          settings.quranScrollMode == QuranScrollMode.horizontalSwipe
                              ? QuranScrollMode.verticalList
                              : QuranScrollMode.horizontalSwipe,
                        ),
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
          : settings.quranScrollMode == QuranScrollMode.horizontalSwipe
              ? PageView.builder(
                  controller: _pageController,
                  itemCount: widget.verses.length,
                  itemBuilder: (context, i) => Padding(
                    padding: const EdgeInsets.all(16),
                    child: Center(
                      child: SingleChildScrollView(
                        child: QuranVerseCard(
                          verse: widget.verses[i],
                          playlist: widget.verses,
                          index: i,
                          fontScale: settings.effectiveTextScale,
                          readingMode: settings.quranReadingMode,
                        ),
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
