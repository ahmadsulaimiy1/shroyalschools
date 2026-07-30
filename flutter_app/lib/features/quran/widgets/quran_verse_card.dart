import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/database/quran_repository.dart';
import '../../../core/localization/app_localizations.dart';
import '../../../core/models/quran_verse.dart';
import '../../../core/services/quran/quran_audio_controller.dart';

class QuranVerseCard extends StatefulWidget {
  const QuranVerseCard({
    super.key,
    required this.verse,
    required this.playlist,
    required this.index,
    this.fontScale = 1.0,
  });

  final QuranVerse verse;
  final List<QuranVerse> playlist;
  final int index;
  final double fontScale;

  @override
  State<QuranVerseCard> createState() => _QuranVerseCardState();
}

class _QuranVerseCardState extends State<QuranVerseCard> {
  bool _bookmarked = false;
  bool _favourite = false;

  @override
  void initState() {
    super.initState();
    _loadState();
  }

  Future<void> _loadState() async {
    final repo = context.read<QuranRepository>();
    final bookmarked = await repo.isBookmarked(widget.verse.surah, widget.verse.ayah);
    final favourite = await repo.isFavourite(widget.verse.surah, widget.verse.ayah);
    if (!mounted) return;
    setState(() {
      _bookmarked = bookmarked;
      _favourite = favourite;
    });
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
                const Spacer(),
                IconButton(
                  icon: Icon(isPlaying ? Icons.pause_circle_outline : Icons.play_circle_outline),
                  tooltip: isPlaying ? t('quran_pause_recitation') : t('quran_play_recitation'),
                  onPressed: () {
                    if (isPlaying) {
                      audio.pause();
                    } else {
                      audio.playVerse(v, playlist: widget.playlist, index: widget.index);
                    }
                  },
                ),
                IconButton(
                  icon: Icon(_bookmarked ? Icons.bookmark : Icons.bookmark_border, color: theme.colorScheme.secondary),
                  tooltip: _bookmarked ? t('quran_remove_bookmark') : t('quran_add_bookmark'),
                  onPressed: () async {
                    final repo = context.read<QuranRepository>();
                    if (_bookmarked) {
                      await repo.removeBookmark(v.surah, v.ayah);
                    } else {
                      await repo.addBookmark(v.surah, v.ayah);
                    }
                    if (mounted) setState(() => _bookmarked = !_bookmarked);
                  },
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
            Text(
              v.arabicText,
              style: theme.textTheme.headlineSmall?.copyWith(height: 2.0, fontSize: (theme.textTheme.headlineSmall?.fontSize ?? 24) * widget.fontScale),
              textAlign: TextAlign.right,
              textDirection: TextDirection.rtl,
            ),
            const Divider(height: 24),
            Text(v.translationEn, style: theme.textTheme.bodyMedium),
          ],
        ),
      ),
    );
  }
}
