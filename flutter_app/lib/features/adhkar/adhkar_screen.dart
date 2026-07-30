import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/adhkar_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/adhkar_entry.dart';
import 'adhkar_category_screen.dart';
import 'adhkar_favourites_screen.dart';
import 'adhkar_recently_read_screen.dart';

/// The Adhkar library home, grouped per the MISBAHA directive's structure:
/// Featured Worship (Morning/Evening, shown as premium cards) → Daily Du'as
/// → Daily Life → Additional (General Dhikr, Favourites, Recently Read).
/// Entry counts come straight from the database so a category the current
/// content pack doesn't cover would honestly show as empty rather than being
/// hidden or faked — see docs/13-ADHKAR-IMPORT-VERIFICATION-REPORT.md and
/// docs/14-HISN-AL-MUSLIM-IMPORT.md for what's populated and from where.
class AdhkarScreen extends StatefulWidget {
  const AdhkarScreen({super.key});

  @override
  State<AdhkarScreen> createState() => _AdhkarScreenState();
}

class _AdhkarScreenState extends State<AdhkarScreen> {
  static const _featured = [AdhkarCategory.morning, AdhkarCategory.evening];
  static const _dailyDuas = [AdhkarCategory.dailyDuas, AdhkarCategory.quranicDuas];
  static const _dailyLife = [
    AdhkarCategory.wakeUp,
    AdhkarCategory.sleep,
    AdhkarCategory.prayer,
    AdhkarCategory.travel,
    AdhkarCategory.protection,
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
      appBar: AppBar(title: Text(t('adhkar_title'))),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  _SectionLabel(t('adhkar_section_featured_worship')),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      for (final category in _featured) ...[
                        Expanded(child: _FeaturedCard(category: category, count: _counts[category] ?? 0)),
                        if (category != _featured.last) const SizedBox(width: 12),
                      ],
                    ],
                  ),
                  const SizedBox(height: 24),
                  _SectionLabel(t('adhkar_section_daily_duas')),
                  const SizedBox(height: 8),
                  for (final category in _dailyDuas)
                    _CategoryTile(
                      category: category,
                      count: _counts[category] ?? 0,
                      icon: _categoryIcon(category),
                      label: _categoryLabel(context, category),
                    ),
                  const SizedBox(height: 16),
                  _SectionLabel(t('adhkar_section_daily_life')),
                  const SizedBox(height: 8),
                  for (final category in _dailyLife)
                    _CategoryTile(
                      category: category,
                      count: _counts[category] ?? 0,
                      icon: _categoryIcon(category),
                      label: _categoryLabel(context, category),
                    ),
                  const SizedBox(height: 16),
                  _SectionLabel(t('adhkar_section_additional')),
                  const SizedBox(height: 8),
                  _CategoryTile(
                    category: AdhkarCategory.generalDhikr,
                    count: _counts[AdhkarCategory.generalDhikr] ?? 0,
                    icon: _categoryIcon(AdhkarCategory.generalDhikr),
                    label: _categoryLabel(context, AdhkarCategory.generalDhikr),
                  ),
                  _NavigationTile(
                    icon: Icons.star_outline,
                    label: t('adhkar_favourites'),
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const AdhkarFavouritesScreen()),
                    ),
                  ),
                  _NavigationTile(
                    icon: Icons.history,
                    label: t('adhkar_recently_read'),
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const AdhkarRecentlyReadScreen()),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}

class _SectionLabel extends StatelessWidget {
  const _SectionLabel(this.label);
  final String label;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Text(label, style: theme.textTheme.titleMedium?.copyWith(color: theme.colorScheme.secondary));
  }
}

/// Morning/Evening's premium "Featured Worship" card: a Deep Royal Navy
/// gradient tile with the category's gold icon, set apart from the plain
/// list tiles used everywhere else on this screen.
class _FeaturedCard extends StatelessWidget {
  const _FeaturedCard({required this.category, required this.count});
  final AdhkarCategory category;
  final int count;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;
    final icon = category == AdhkarCategory.morning ? Icons.wb_sunny_outlined : Icons.nights_stay_outlined;
    final label = t('adhkar_category_${category.id}');

    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: count == 0
            ? null
            : () => Navigator.of(context).push(
                  MaterialPageRoute(builder: (_) => AdhkarCategoryScreen(category: category)),
                ),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [theme.colorScheme.tertiary, theme.colorScheme.tertiary.withOpacity(0.75)],
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon, color: theme.colorScheme.secondary, size: 30),
              const SizedBox(height: 14),
              Text(
                label,
                style: theme.textTheme.titleMedium?.copyWith(color: Colors.white),
              ),
              const SizedBox(height: 4),
              Text(
                count == 0 ? t('adhkar_no_entries_category') : context.loc.tArgs('adhkar_entries_count', [count]),
                style: theme.textTheme.labelLarge?.copyWith(color: Colors.white.withOpacity(0.8)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _CategoryTile extends StatelessWidget {
  const _CategoryTile({required this.category, required this.count, required this.icon, required this.label});
  final AdhkarCategory category;
  final int count;
  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: CircleAvatar(
          backgroundColor: theme.colorScheme.secondary.withOpacity(0.15),
          child: Icon(icon, color: theme.colorScheme.secondary),
        ),
        title: Text(label, style: theme.textTheme.titleMedium),
        subtitle: Text(count == 0 ? t('adhkar_no_entries_category') : context.loc.tArgs('adhkar_entries_count', [count])),
        trailing: const Icon(Icons.chevron_right),
        onTap: count == 0
            ? null
            : () => Navigator.of(context).push(
                  MaterialPageRoute(builder: (_) => AdhkarCategoryScreen(category: category)),
                ),
      ),
    );
  }
}

class _NavigationTile extends StatelessWidget {
  const _NavigationTile({required this.icon, required this.label, required this.onTap});
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: CircleAvatar(
          backgroundColor: theme.colorScheme.secondary.withOpacity(0.15),
          child: Icon(icon, color: theme.colorScheme.secondary),
        ),
        title: Text(label, style: theme.textTheme.titleMedium),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}
