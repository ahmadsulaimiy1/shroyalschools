import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/adhkar_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/adhkar_entry.dart';
import 'adhkar_detail_screen.dart';
import 'widgets/adhkar_list_tile.dart';

class AdhkarCategoryScreen extends StatefulWidget {
  const AdhkarCategoryScreen({super.key, required this.category});
  final AdhkarCategory category;

  @override
  State<AdhkarCategoryScreen> createState() => _AdhkarCategoryScreenState();
}

class _AdhkarCategoryScreenState extends State<AdhkarCategoryScreen> {
  List<AdhkarEntry> _entries = [];
  bool _loading = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final entries = await context.read<AdhkarRepository>().byCategory(widget.category);
    if (!mounted) return;
    setState(() {
      _entries = entries;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    return Scaffold(
      appBar: AppBar(title: Text(t('adhkar_category_${widget.category.id}'))),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _entries.length,
              itemBuilder: (context, i) {
                final entry = _entries[i];
                return AdhkarListTile(
                  entry: entry,
                  onFavouriteToggled: _load,
                  onTap: () => Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) => AdhkarDetailScreen(entry: entry, playlist: _entries, index: i),
                    ),
                  ),
                );
              },
            ),
    );
  }
}
