import 'package:flutter/material.dart' hide RepeatMode;
import 'package:provider/provider.dart';

import '../../../core/database/quran_repository.dart';
import '../../../core/localization/app_localizations.dart';
import '../../../core/models/quran_verse.dart';
import '../../../core/services/quran/quran_audio_controller.dart';
import '../../../core/services/settings_controller.dart';
import '../../../core/services/tts/adhkar_audio_handler.dart' show RepeatMode;

class QuranVerseCard extends StatefulWidget {
  const QuranVerseCard({
    super.key,
    required this.verse,
    required this.playlist,
    required this.index,
    this.fontScale = 1.0,
    this.readingMode = QuranReadingMode.arabicTranslation,
  });

  final QuranVerse verse;
  final List<QuranVerse> playlist;
  final int index;
  final double fontScale;
  final QuranReadingMode readingMode;

  @override
  State<QuranVerseCard> createState() => _QuranVerseCardState();
}

class _QuranVerseCardState extends State<QuranVerseCard> {
  bool _bookmarked = false;
  bool _favourite = false;
  String? _bookmarkLabel;
  String? _note;

  @override
  void initState() {
    super.initState();
    _loadState();
  }

  Future<void> _loadState() async {
    final repo = context.read<QuranRepository>();
    final bookmarked = await repo.isBookmarked(widget.verse.surah, widget.verse.ayah);
    final favourite = await repo.isFavourite(widget.verse.surah, widget.verse.ayah);
    final label = await repo.bookmarkLabel(widget.verse.surah, widget.verse.ayah);
    final note = await repo.verseNote(widget.verse.surah, widget.verse.ayah);
    if (!mounted) return;
    setState(() {
      _bookmarked = bookmarked;
      _favourite = favourite;
      _bookmarkLabel = label;
      _note = note;
    });
  }

  Future<void> _editBookmarkLabel() async {
    final t = context.loc.t;
    final controller = TextEditingController(text: _bookmarkLabel ?? '');
    final result = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(t('quran_bookmark_label_title')),
        content: TextField(
          controller: controller,
          autofocus: true,
          decoration: InputDecoration(hintText: t('quran_bookmark_label_hint')),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.of(context).pop(), child: Text(t('cancel'))),
          FilledButton(onPressed: () => Navigator.of(context).pop(controller.text), child: Text(t('save'))),
        ],
      ),
    );
    if (result == null) return;
    final repo = context.read<QuranRepository>();
    final label = result.trim().isEmpty ? null : result.trim();
    if (!_bookmarked) {
      await repo.addBookmark(widget.verse.surah, widget.verse.ayah, label: label);
    } else {
      await repo.setBookmarkLabel(widget.verse.surah, widget.verse.ayah, label);
    }
    if (mounted) setState(() { _bookmarked = true; _bookmarkLabel = label; });
  }

  Future<void> _editNote() async {
    final t = context.loc.t;
    final controller = TextEditingController(text: _note ?? '');
    final result = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(t('quran_reflection_note_title')),
        content: TextField(
          controller: controller,
          autofocus: true,
          maxLines: 5,
          decoration: InputDecoration(hintText: t('quran_reflection_note_hint')),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.of(context).pop(), child: Text(t('cancel'))),
          FilledButton(onPressed: () => Navigator.of(context).pop(controller.text), child: Text(t('save'))),
        ],
      ),
    );
    if (result == null) return;
    final repo = context.read<QuranRepository>();
    await repo.setVerseNote(widget.verse.surah, widget.verse.ayah, result.trim());
    if (mounted) setState(() => _note = result.trim().isEmpty ? null : result.trim());
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;
    final v = widget.verse;
    final audio = context.watch<QuranAudioController>();
    final isPlaying = audio.isCurrentlyPlaying(v);

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                CircleAvatar(
                  radius: 14,
                  backgroundColor: theme.colorScheme.secondary.withOpacity(0.15),
                  child: Text('${v.ayah}', style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.secondary)),
                ),
                if (v.isSajdah) ...[
                  const SizedBox(width: 8),
                  Tooltip(
                    message: t('quran_sajdah_verse'),
                    child: Chip(
                      avatar: Icon(Icons.self_improvement, size: 16, color: theme.colorScheme.secondary),
                      label: Text(t('quran_sajdah_short'), style: theme.textTheme.labelSmall),
                      visualDensity: VisualDensity.compact,
                      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                    ),
                  ),
                ],
                const Spacer(),
                GestureDetector(
                  onLongPress: () {
                    // Long-press: repeat just this verse in a loop, ignoring
                    // whatever playlist/repeat state the surah-level toolbar
                    // had set -- a quick way to repeat a single ayah without
                    // opening the Repeat Range sheet.
                    audio.setMemorizationMode(false);
                    audio.setRepeatMode(RepeatMode.repeatOne);
                    audio.setLoopPlaylist(false);
                    audio.playVerse(v, playlist: [v], index: 0);
                  },
                  child: IconButton(
                    icon: Icon(isPlaying ? Icons.pause_circle_outline : Icons.play_circle_outline),
                    tooltip: isPlaying
                        ? t('quran_pause_recitation')
                        : '${t('quran_play_recitation')} (${t('quran_repeat_this_verse_hint')})',
                    onPressed: () {
                      if (isPlaying) {
                        audio.pause();
                      } else {
                        audio.playVerse(v, playlist: widget.playlist, index: widget.index);
                      }
                    },
                  ),
                ),
                GestureDetector(
                  onLongPress: _editBookmarkLabel,
                  child: IconButton(
                    icon: Icon(_bookmarked ? Icons.bookmark : Icons.bookmark_border, color: theme.colorScheme.secondary),
                    tooltip: _bookmarked ? t('quran_remove_bookmark') : t('quran_add_bookmark'),
                    onPressed: () async {
                      final repo = context.read<QuranRepository>();
                      if (_bookmarked) {
                        await repo.removeBookmark(v.surah, v.ayah);
                      } else {
                        await repo.addBookmark(v.surah, v.ayah);
                      }
                      if (mounted) setState(() { _bookmarked = !_bookmarked; if (!_bookmarked) _bookmarkLabel = null; });
                    },
                  ),
                ),
                IconButton(
                  icon: Icon(_note != null ? Icons.edit_note : Icons.note_add_outlined, color: theme.colorScheme.secondary),
                  tooltip: t('quran_reflection_note_title'),
                  onPressed: _editNote,
                ),
                IconButton(
                  icon: Icon(_favourite ? Icons.star : Icons.star_border, color: theme.colorScheme.secondary),
                  tooltip: _favourite ? t('quran_remove_favourite') : t('quran_add_favourite'),
                  onPressed: () async {
                    await context.read<QuranRepository>().setFavourite(v.surah, v.ayah, !_favourite);
                    if (mounted) setState(() => _favourite = !_favourite);
                  },
                ),
              ],
            ),
            if (_bookmarkLabel != null && _bookmarkLabel!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Align(
                  alignment: AlignmentDirectional.centerEnd,
                  child: Chip(
                    label: Text(_bookmarkLabel!, style: theme.textTheme.labelSmall),
                    visualDensity: VisualDensity.compact,
                    materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  ),
                ),
              ),
            Text(
              v.arabicText,
              style: theme.textTheme.headlineSmall?.copyWith(
                fontFamily: 'AmiriQuran',
                height: 2.3,
                // Arabic is a cursive/joining script -- any non-zero
                // letterSpacing inserts a gap after every shaped glyph
                // cluster, which visually breaks letter joining (looks like
                // detached/disconnected letters). Never apply letterSpacing
                // to Arabic text.
                letterSpacing: 0.0,
                fontSize: (theme.textTheme.headlineSmall?.fontSize ?? 24) * 1.05 * widget.fontScale,
              ),
              textAlign: TextAlign.right,
              textDirection: TextDirection.rtl,
            ),
            if (widget.readingMode != QuranReadingMode.arabicOnly) ...[
              const Divider(height: 24),
              if (widget.readingMode == QuranReadingMode.arabicTranslationTransliteration && v.transliteration.isNotEmpty) ...[
                Text(
                  v.transliteration,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    fontStyle: FontStyle.italic,
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                ),
                const SizedBox(height: 8),
              ],
              Text(v.translationEn, style: theme.textTheme.bodyMedium),
            ],
            if (_note != null && _note!.isNotEmpty) ...[
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: theme.colorScheme.secondaryContainer.withOpacity(0.3),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(Icons.edit_note, size: 18, color: theme.colorScheme.secondary),
                    const SizedBox(width: 8),
                    Expanded(child: Text(_note!, style: theme.textTheme.bodySmall)),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
