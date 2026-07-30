import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/quran_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/quran_chapter.dart';
import '../../core/models/quran_juz.dart';
import '../../core/models/quran_verse.dart';
import 'quran_bookmarks_screen.dart';
import 'quran_favourites_screen.dart';
import 'quran_reader_screen.dart';
import 'quran_search_screen.dart';

class QuranScreen extends StatefulWidget {
  const QuranScreen({super.key});

  @override
  State<QuranScreen> createState() => _QuranScreenState();
}

class _QuranScreenState extends State<QuranScreen> with SingleTickerProviderStateMixin {
  late final TabController _tabController = TabController(length: 2, vsync: this);

  List<QuranChapter> _chapters = [];
  List<QuranJuz> _juz = [];
  QuranVerse? _lastRead;
  bool _loading = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final repo = context.read<QuranRepository>();
    final chapters = await repo.chapters();
    final juz = await repo.juzList();
    final lastRead = await repo.lastRead();
    if (!mounted) return;
    setState(() {
      _chapters = chapters;
      _juz = juz;
      _lastRead = lastRead;
      _loading = false;
    });
  }

  Future<void> _openChapter(QuranChapter chapter) async {
    final repo = context.read<QuranRepository>();
    final verses = await repo.versesForChapter(chapter.number);
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuranReaderScreen(title: '${chapter.nameTransliteration} — ${chapter.nameTranslation}', verses: verses),
      ),
    );
  }

  Future<void> _openJuz(QuranJuz juz) async {
    final repo = context.read<QuranRepository>();
    final verses = await repo.versesForJuz(juz.number);
    final title = context.loc.tArgs('quran_juz_label', [juz.number]);
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(builder: (_) => QuranReaderScreen(title: title, verses: verses)),
    );
  }

  Future<void> _openLastRead() async {
    if (_lastRead == null) return;
    final repo = context.read<QuranRepository>();
    final chapter = await repo.chapter(_lastRead!.surah);
    final verses = await repo.versesForChapter(_lastRead!.surah);
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuranReaderScreen(
          title: '${chapter.nameTransliteration} — ${chapter.nameTranslation}',
          verses: verses,
          scrollToAyah: _lastRead!.ayah,
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
        title: Text(t('quran_title')),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            tooltip: t('quran_search_title'),
            onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const QuranSearchScreen())),
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          tabs: [Tab(text: t('quran_tab_surahs')), Tab(text: t('quran_tab_juz'))],
        ),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
                  child: Row(
                    children: [
                      Expanded(
                        child: OutlinedButton.icon(
                          icon: const Icon(Icons.bookmark_outline, size: 18),
                          label: Text(t('quran_bookmarks')),
                          onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const QuranBookmarksScreen())),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: OutlinedButton.icon(
                          icon: const Icon(Icons.star_outline, size: 18),
                          label: Text(t('quran_favourites')),
                          onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const QuranFavouritesScreen())),
                        ),
                      ),
                    ],
                  ),
                ),
                if (_lastRead != null)
                  Padding(
                    padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
                    child: Card(
                      color: theme.colorScheme.tertiary,
                      child: ListTile(
                        leading: Icon(Icons.auto_stories_outlined, color: theme.colorScheme.secondary),
                        title: Text(t('quran_continue_reading'), style: theme.textTheme.titleMedium?.copyWith(color: Colors.white)),
                        subtitle: Text(
                          '${_lastRead!.surah}:${_lastRead!.ayah}',
                          style: theme.textTheme.bodyMedium?.copyWith(color: Colors.white.withOpacity(0.85)),
                        ),
                        trailing: const Icon(Icons.chevron_right, color: Colors.white),
                        onTap: _openLastRead,
                      ),
                    ),
                  ),
                Expanded(
                  child: TabBarView(
                    controller: _tabController,
                    children: [
                      ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: _chapters.length,
                        itemBuilder: (context, i) {
                          final c = _chapters[i];
                          return Card(
                            margin: const EdgeInsets.only(bottom: 10),
                            child: ListTile(
                              leading: CircleAvatar(
                                backgroundColor: theme.colorScheme.secondary.withOpacity(0.15),
                                child: Text('${c.number}', style: TextStyle(color: theme.colorScheme.secondary, fontSize: 13)),
                              ),
                              title: Text('${c.nameTransliteration} — ${c.nameTranslation}', style: theme.textTheme.titleMedium),
                              subtitle: Text(
                                '${c.revelationType == 'meccan' ? t('quran_meccan') : t('quran_medinan')} · ${context.loc.tArgs('quran_verses_count', [c.versesCount])}',
                              ),
                              trailing: Text(c.nameArabic, style: theme.textTheme.titleMedium, textDirection: TextDirection.rtl),
                              onTap: () => _openChapter(c),
                            ),
                          );
                        },
                      ),
                      ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: _juz.length,
                        itemBuilder: (context, i) {
                          final j = _juz[i];
                          return Card(
                            margin: const EdgeInsets.only(bottom: 10),
                            child: ListTile(
                              leading: CircleAvatar(
                                backgroundColor: theme.colorScheme.secondary.withOpacity(0.15),
                                child: Text('${j.number}', style: TextStyle(color: theme.colorScheme.secondary, fontSize: 13)),
                              ),
                              title: Text(context.loc.tArgs('quran_juz_label', [j.number]), style: theme.textTheme.titleMedium),
                              subtitle: Text('${j.startSurah}:${j.startAyah} – ${j.endSurah}:${j.endAyah}'),
                              onTap: () => _openJuz(j),
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                ),
              ],
            ),
    );
  }
}
