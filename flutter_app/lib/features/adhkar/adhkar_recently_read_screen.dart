import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/adhkar_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/adhkar_entry.dart';
import '../../core/services/recently_read_service.dart';
import 'adhkar_detail_screen.dart';
import 'widgets/adhkar_list_tile.dart';

class AdhkarRecentlyReadScreen extends StatefulWidget {
  const AdhkarRecentlyReadScreen({super.key});

  @override
  State<AdhkarRecentlyReadScreen> createState() => _AdhkarRecentlyReadScreenState();
}

class _AdhkarRecentlyReadScreenState extends State<AdhkarRecentlyReadScreen> {
  List<AdhkarEntry> _entries = [];
  bool _loading = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final ids = await context.read<RecentlyReadService>().getRecentIds();
    final entries = await context.read<AdhkarRepository>().byIds(ids);
    if (!mounted) return;
    setState(() {
      _entries = entries;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(t('adhkar_recently_read'))),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _entries.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text(
                      t('adhkar_no_recently_read'),
                      textAlign: TextAlign.center,
                      style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                    ),
                  ),
                )
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
