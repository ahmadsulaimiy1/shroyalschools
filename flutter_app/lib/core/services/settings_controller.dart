import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum AppThemeMode { system, light, dark }

/// Single source of truth for user-configurable settings, persisted locally via
/// SharedPreferences (fully offline). Exposed as a ChangeNotifier so the whole
/// widget tree (theme, locale, feedback toggles) reacts live to changes made in
/// the Settings screen.
class SettingsController extends ChangeNotifier {
  static const _kThemeMode = 'theme_mode';
  static const _kLanguage = 'language_code';
  static const _kSoundEnabled = 'sound_enabled';
  static const _kVibrationEnabled = 'vibration_enabled';
  static const _kVolumeButtonEnabled = 'volume_button_enabled';

  AppThemeMode _themeMode = AppThemeMode.system;
  Locale _locale = const Locale('en');
  bool _soundEnabled = true;
  bool _vibrationEnabled = true;
  bool _volumeButtonEnabled = false;

  AppThemeMode get themeMode => _themeMode;
  Locale get locale => _locale;
  bool get soundEnabled => _soundEnabled;
  bool get vibrationEnabled => _vibrationEnabled;
  bool get volumeButtonEnabled => _volumeButtonEnabled;

  ThemeMode get flutterThemeMode {
    switch (_themeMode) {
      case AppThemeMode.light:
        return ThemeMode.light;
      case AppThemeMode.dark:
        return ThemeMode.dark;
      case AppThemeMode.system:
        return ThemeMode.system;
    }
  }

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    final themeName = prefs.getString(_kThemeMode);
    _themeMode = AppThemeMode.values.firstWhere(
      (e) => e.name == themeName,
      orElse: () => AppThemeMode.system,
    );
    _locale = Locale(prefs.getString(_kLanguage) ?? 'en');
    _soundEnabled = prefs.getBool(_kSoundEnabled) ?? true;
    _vibrationEnabled = prefs.getBool(_kVibrationEnabled) ?? true;
    _volumeButtonEnabled = prefs.getBool(_kVolumeButtonEnabled) ?? false;
    notifyListeners();
  }

  Future<void> setThemeMode(AppThemeMode mode) async {
    _themeMode = mode;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kThemeMode, mode.name);
  }

  Future<void> setLocale(Locale locale) async {
    _locale = locale;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kLanguage, locale.languageCode);
  }

  Future<void> setSoundEnabled(bool value) async {
    _soundEnabled = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_kSoundEnabled, value);
  }

  Future<void> setVibrationEnabled(bool value) async {
    _vibrationEnabled = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_kVibrationEnabled, value);
  }

  Future<void> setVolumeButtonEnabled(bool value) async {
    _volumeButtonEnabled = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_kVolumeButtonEnabled, value);
  }
}
