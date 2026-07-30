import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/quran_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/quran_verse.dart';
import '../../core/services/settings_controller.dart';
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

  @override
  void initState() {
    super.initState();
    if (widget.verses.isNotEmpty) {
      final last = widget.verses.last;
      context.read<QuranRepository>().setLastRead(last.surah, last.ayah);
    }
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

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final settings = context.watch<SettingsController>();
    final t = context.loc.t;
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions: [
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
      body: ListView.builder(
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
  }
}
