import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/database/adhkar_repository.dart';
import '../../../core/localization/app_localizations.dart';
import '../../../core/models/adhkar_entry.dart';

class AdhkarListTile extends StatelessWidget {
  const AdhkarListTile({
    super.key,
    required this.entry,
    required this.onTap,
    this.onFavouriteToggled,
  });

  final AdhkarEntry entry;
  final VoidCallback onTap;
  final VoidCallback? onFavouriteToggled;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
        title: Text(entry.titleAr, style: theme.textTheme.titleMedium, textAlign: TextAlign.right),
        subtitle: Text(entry.titleEn, style: theme.textTheme.bodyMedium),
        trailing: IconButton(
          icon: Icon(entry.favourite ? Icons.star : Icons.star_border, color: theme.colorScheme.secondary),
          tooltip: entry.favourite ? t('adhkar_remove_favourite') : t('adhkar_add_favourite'),
          onPressed: () async {
            await context.read<AdhkarRepository>().setFavourite(entry.id, !entry.favourite);
            onFavouriteToggled?.call();
          },
        ),
        onTap: onTap,
      ),
    );
  }
}
