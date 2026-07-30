import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/adhkar_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/adhkar_entry.dart';
import 'adhkar_category_screen.dart';
import 'adhkar_favourites_screen.dart';

/// The Adhkar library home: browse by category or jump to Favourites.
/// Category order follows the Phase 2 directive's required taxonomy; entry
/// counts come straight from the database so categories the current content
/// pack doesn't cover (see docs/13-ADHKAR-IMPORT-VERIFICATION-REPORT.md)
/// honestly show as empty rather than being hidden or faked.
class AdhkarScreen extends StatefulWidget {
  const AdhkarScreen({super.key});

  @override
  State<AdhkarScreen> createState() => _AdhkarScreenState();
}

class _AdhkarScreenState extends State<AdhkarScreen> {
  static const _categoryOrder = [
    AdhkarCategory.morning,
    AdhkarCategory.evening,
    AdhkarCategory.sleep,
    AdhkarCategory.wakeUp,
    AdhkarCategory.prayer,
    AdhkarCategory.travel,
    AdhkarCategory.protection,
    AdhkarCategory.quranicDuas,
    AdhkarCategory.dailyDuas,
    AdhkarCategory.generalDhikr,
  ];

  Map<AdhkarCategory, int> _counts = {};
  bool _loading = true;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final counts = await context.read<AdhkarRepository>().countsByCategory();
    if (!mounted) return;
    setState(() {
      _counts = counts;
      _loading = false;
    });
  }

  String _categoryLabel(BuildContext context, AdhkarCategory category) {
    final t = context.loc.t;
    return t('adhkar_category_${category.id}');
  }

  IconData _categoryIcon(AdhkarCategory category) {
    switch (category) {
      case AdhkarCategory.morning:
        return Icons.wb_sunny_outlined;
      case AdhkarCategory.evening:
        return Icons.nights_stay_outlined;
      case AdhkarCategory.sleep:
        return Icons.bedtime_outlined;
      case AdhkarCategory.wakeUp:
        return Icons.alarm;
      case AdhkarCategory.prayer:
        return Icons.mosque_outlined;
      case AdhkarCategory.travel:
        return Icons.flight_takeoff;
      case AdhkarCategory.protection:
        return Icons.shield_outlined;
      case AdhkarCategory.quranicDuas:
        return Icons.menu_book_outlined;
      case AdhkarCategory.dailyDuas:
        return Icons.today_outlined;
      case AdhkarCategory.generalDhikr:
        return Icons.favorite_border;
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(t('adhkar_title')),
        actions: [
          IconButton(
            icon: const Icon(Icons.star_outline),
            tooltip: t('adhkar_favourites'),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => const AdhkarFavouritesScreen()),
            ),
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _categoryOrder.length,
                itemBuilder: (context, i) {
                  final category = _categoryOrder[i];
                  final count = _counts[category] ?? 0;
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    child: ListTile(
                      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      leading: CircleAvatar(
                        backgroundColor: theme.colorScheme.secondary.withOpacity(0.15),
                        child: Icon(_categoryIcon(category), color: theme.colorScheme.secondary),
                      ),
                      title: Text(_categoryLabel(context, category), style: theme.textTheme.titleMedium),
                      subtitle: Text(
                        count == 0
                            ? t('adhkar_no_entries_category')
                            : context.loc.tArgs('adhkar_entries_count', [count]),
                      ),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: count == 0
                          ? null
                          : () => Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (_) => AdhkarCategoryScreen(category: category),
                                ),
                              ),
                    ),
                  );
                },
              ),
            ),
    );
  }
}
