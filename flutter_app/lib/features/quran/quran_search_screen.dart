import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/quran_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/quran_verse.dart';
import 'quran_reader_screen.dart';

class QuranSearchScreen extends StatefulWidget {
  const QuranSearchScreen({super.key});

  @override
  State<QuranSearchScreen> createState() => _QuranSearchScreenState();
}

class _QuranSearchScreenState extends State<QuranSearchScreen> {
  final _controller = TextEditingController();
  List<QuranVerse> _results = [];
  bool _searched = false;

  Future<void> _search(String query) async {
    final results = await context.read<QuranRepository>().search(query);
    if (!mounted) return;
    setState(() {
      _results = results;
      _searched = query.trim().isNotEmpty;
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _openVerse(QuranVerse verse) async {
    final repo = context.read<QuranRepository>();
    final chapter = await repo.chapter(verse.surah);
    final verses = await repo.versesForChapter(verse.surah);
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuranReaderScreen(
          title: '${chapter.nameTransliteration} — ${chapter.nameTranslation}',
          verses: verses,
          scrollToAyah: verse.ayah,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: _controller,
          autofocus: true,
          textDirection: TextDirection.rtl,
          decoration: InputDecoration(hintText: t('quran_search_hint'), border: InputBorder.none),
          onSubmitted: _search,
          onChanged: (value) {
            if (value.trim().length >= 3) _search(value);
          },
        ),
      ),
      body: !_searched
          ? const SizedBox.shrink()
          : _results.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text(t('quran_search_empty'), style: theme.textTheme.bodyMedium),
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _results.length,
                  itemBuilder: (context, i) {
                    final v = _results[i];
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
