import 'package:flutter_test/flutter_test.dart';
import 'package:misbaha_tasbeeh/core/localization/translations_ar.dart';
import 'package:misbaha_tasbeeh/core/localization/translations_en.dart';
import 'package:misbaha_tasbeeh/core/models/dhikr.dart';

void main() {
  group('Localization key parity', () {
    test('every English key has an Arabic translation', () {
      for (final key in enTranslations.keys) {
        expect(arTranslations.containsKey(key), isTrue, reason: 'Missing Arabic translation for "$key"');
      }
    });

    test('every Arabic key has an English translation', () {
      for (final key in arTranslations.keys) {
        expect(enTranslations.containsKey(key), isTrue, reason: 'Missing English translation for "$key"');
      }
    });

    test('no translation value is empty', () {
      for (final entry in enTranslations.entries) {
        expect(entry.value.trim(), isNotEmpty, reason: 'Empty English value for "${entry.key}"');
      }
      for (final entry in arTranslations.entries) {
        expect(entry.value.trim(), isNotEmpty, reason: 'Empty Arabic value for "${entry.key}"');
      }
    });
  });

  group('Seed adhkar content', () {
    test('every dhikr has non-empty Arabic text and a positive target', () {
      expect(seedAdhkar, isNotEmpty);
      for (final dhikr in seedAdhkar) {
        expect(dhikr.arabicText.trim(), isNotEmpty, reason: 'Missing Arabic text for "${dhikr.id}"');
        expect(dhikr.defaultTarget, greaterThan(0), reason: 'Non-positive target for "${dhikr.id}"');
      }
    });

    test('dhikr ids are unique', () {
      final ids = seedAdhkar.map((d) => d.id).toList();
      expect(ids.toSet().length, ids.length, reason: 'Duplicate dhikr ids found');
    });
  });
}
