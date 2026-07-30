import 'package:flutter/material.dart';
import 'translations_ar.dart';
import 'translations_en.dart';

/// Hand-rolled localization (no `flutter gen-l10n` build step required) so the
/// project compiles immediately with nothing but `flutter pub get`.
class AppLocalizations {
  AppLocalizations(this.locale);

  final Locale locale;

  static const supportedLocales = [Locale('en'), Locale('ar')];

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  static const LocalizationsDelegate<AppLocalizations> delegate = _AppLocalizationsDelegate();

  Map<String, String> get _values => locale.languageCode == 'ar' ? arTranslations : enTranslations;

  String t(String key) => _values[key] ?? enTranslations[key] ?? key;

  String tArgs(String key, List<Object> args) {
    var value = t(key);
    for (var i = 0; i < args.length; i++) {
      value = value.replaceAll('{$i}', args[i].toString());
    }
    return value;
  }

  bool get isRtl => locale.languageCode == 'ar';
}

class _AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) =>
      AppLocalizations.supportedLocales.any((l) => l.languageCode == locale.languageCode);

  @override
  Future<AppLocalizations> load(Locale locale) async => AppLocalizations(locale);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

/// Convenience extension: `context.t('home_greeting')`.
extension AppLocalizationsX on BuildContext {
  AppLocalizations get loc => AppLocalizations.of(this);
  String t(String key) => loc.t(key);
}
