import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/quran_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/quran_verse.dart';
import 'quran_reader_screen.dart';

class QuranBookmarksScreen extends StatefulWidget {
  const QuranBookmarksScreen({super.key});

  @override
  State<QuranBookmarksScreen> createState() => _QuranBookmarksScreenState();
}

class _QuranBookmarksScreenState extends State<QuranBookmarksScreen> {
  List<QuranVerse> _verses = [];
  bool _loading = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final verses = await context.read<QuranRepository>().bookmarkedVerses();
    if (!mounted) return;
    setState(() {
      _verses = verses;
      _loading = false;
    });
  }

  Future<void> _openVerse(QuranVerse verse) async {
    final repo = context.read<QuranRepository>();
    final chapter = await repo.chapter(verse.surah);
    final verses = await repo.versesForChapter(verse.surah);
    if (!mounted) return;
    await Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuranReaderScreen(
          title: '${chapter.nameTransliteration} — ${chapter.nameTranslation}',
          verses: verses,
          scrollToAyah: verse.ayah,
        ),
      ),
    );
    _load();
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(t('quran_bookmarks'))),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _verses.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text(t('quran_no_bookmarks'), textAlign: TextAlign.center, style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _verses.length,
                  itemBuilder: (context, i) {
                    final v = _verses[i];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 10),
                      child: ListTile(
                        title: Text(v.arabicText, textDirection: TextDirection.rtl, textAlign: TextAlign.right, maxLines: 2, overflow: TextOverflow.ellipsis),
                        subtitle: Text('${v.surah}:${v.ayah} — ${v.translationEn}', maxLines: 2, overflow: TextOverflow.ellipsis),
                        onTap: () => _openVerse(v),
                      ),
                    );
                  },
                ),
    );
  }
}
