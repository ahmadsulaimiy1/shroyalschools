import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/database/adhkar_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/models/adhkar_entry.dart';
import '../../core/models/dhikr.dart' as legacy;
import '../../core/services/active_dhikr_controller.dart';
import '../../core/widgets/app_shell.dart';
import 'widgets/tts_control_bar.dart';

class AdhkarDetailScreen extends StatefulWidget {
  const AdhkarDetailScreen({super.key, required this.entry, this.playlist, this.index});

  final AdhkarEntry entry;
  final List<AdhkarEntry>? playlist;
  final int? index;

  @override
  State<AdhkarDetailScreen> createState() => _AdhkarDetailScreenState();
}

class _AdhkarDetailScreenState extends State<AdhkarDetailScreen> {
  late AdhkarEntry _entry = widget.entry;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = context.loc.t;

    return Scaffold(
      appBar: AppBar(
        title: Text(_entry.titleEn),
        actions: [
          IconButton(
            icon: Icon(_entry.favourite ? Icons.star : Icons.star_border),
            tooltip: _entry.favourite ? t('adhkar_remove_favourite') : t('adhkar_add_favourite'),
            onPressed: () async {
              final newValue = !_entry.favourite;
              await context.read<AdhkarRepository>().setFavourite(_entry.id, newValue);
              setState(() => _entry = _entry.copyWith(favourite: newValue));
            },
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    _entry.arabicText,
                    style: theme.textTheme.headlineMedium?.copyWith(height: 1.9),
                    textAlign: TextAlign.right,
                    textDirection: TextDirection.rtl,
                  ),
                  const Divider(height: 32),
                  Text(_entry.transliteration, style: theme.textTheme.bodyLarge?.copyWith(fontStyle: FontStyle.italic)),
                  const SizedBox(height: 12),
                  Text(_entry.translationEn, style: theme.textTheme.bodyLarge),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          TtsControlBar(entry: _entry, playlist: widget.playlist, index: widget.index),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.repeat, size: 18, color: theme.colorScheme.secondary),
                      const SizedBox(width: 8),
                      Text(
                        _entry.repetitionCount > 1
                            ? context.loc.tArgs('adhkar_repetition_label', [_entry.repetitionCount])
                            : t('adhkar_repetition_once'),
                        style: theme.textTheme.bodyMedium,
                      ),
                    ],
                  ),
                  if (_entry.repetitionNote != null && _entry.repetitionNote!.isNotEmpty) ...[
                    const SizedBox(height: 4),
                    Text(
                      _entry.repetitionNote!,
                      style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                    ),
                  ],
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Icon(Icons.menu_book, size: 18, color: theme.colorScheme.secondary),
                      const SizedBox(width: 8),
                      Expanded(child: Text(_entry.sourceReference, style: theme.textTheme.bodyMedium)),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: FilledButton.icon(
              icon: const Icon(Icons.fingerprint),
              label: Text(t('adhkar_start_counting')),
              onPressed: () {
                context.read<ActiveDhikrController>().select(
                      legacy.Dhikr(
                        id: _entry.id,
                        category: legacy.DhikrCategory.general,
                        arabicText: _entry.arabicText,
                        transliteration: _entry.transliteration,
                        translationEn: _entry.translationEn,
                        translationAr: _entry.titleAr,
                        sourceCitation: _entry.sourceReference,
                        defaultTarget: _entry.repetitionCount,
                      ),
                    );
                AppShellScope.maybeOf(context)?.goToCounter();
                Navigator.of(context).popUntil((route) => route.isFirst);
              },
            ),
          ),
        ],
      ),
    );
  }
}
