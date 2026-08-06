import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum AppThemeMode { system, light, dark }

/// Text scale presets for the accessibility "Large Text" / "Elderly-Friendly"
/// modes. Elderly-friendly goes beyond a simple font bump — it also widens
/// touch targets and spacing app-wide (applied by screens reading
/// [elderlyFriendlyMode], not by this enum alone).
enum TextSizePreset { standard, large, extraLarge }

/// Qur'an Reading Modes (A/B/C from the Premium Qur'an Experience directive).
/// D (Tafsir) and E (word-by-word Study Mode) are future-expansion items and
/// deliberately not represented here yet.
enum QuranReadingMode { arabicOnly, arabicTranslation, arabicTranslationTransliteration }

/// Card-view scrolling behaviour (Mushaf mode always uses a single
/// continuous flow regardless of this setting, since that's the whole
/// point of a Mushaf page). "Page Mode" in the Phase 5 directive would mean
/// exact King Fahd Mushaf pagination -- not yet available, see docs/21/22
/// -- so this offers the two modes buildable without that data today.
enum QuranScrollMode { verticalList, horizontalSwipe }

extension TextSizePresetX on TextSizePreset {
  double get scaleFactor {
    switch (this) {
      case TextSizePreset.standard:
        return 1.0;
      case TextSizePreset.large:
        return 1.25;
      case TextSizePreset.extraLarge:
        return 1.5;
    }
  }
}

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
  static const _kTextSizePreset = 'text_size_preset';
  static const _kElderlyFriendlyMode = 'elderly_friendly_mode';
  static const _kQuranReadingMode = 'quran_reading_mode';
  static const _kQuranMushafMode = 'quran_mushaf_mode';
  static const _kQuranScrollMode = 'quran_scroll_mode';

  AppThemeMode _themeMode = AppThemeMode.system;
  Locale _locale = const Locale('en');
  bool _soundEnabled = true;
  bool _vibrationEnabled = true;
  bool _volumeButtonEnabled = false;
  TextSizePreset _textSizePreset = TextSizePreset.standard;
  bool _elderlyFriendlyMode = false;
  QuranReadingMode _quranReadingMode = QuranReadingMode.arabicTranslation;
  bool _quranMushafMode = false;
  QuranScrollMode _quranScrollMode = QuranScrollMode.verticalList;

  /// True while Masjid Mode is active: distraction-free worship, and a hook
  /// point for a future notification system to check before showing any
  /// non-essential (non-prayer-related) notification -- see docs/21.
  bool _masjidMode = false;

  AppThemeMode get themeMode => _themeMode;
  Locale get locale => _locale;
  bool get soundEnabled => _soundEnabled;
  bool get vibrationEnabled => _vibrationEnabled;
  bool get volumeButtonEnabled => _volumeButtonEnabled;
  TextSizePreset get textSizePreset => _textSizePreset;
  bool get elderlyFriendlyMode => _elderlyFriendlyMode;
  QuranReadingMode get quranReadingMode => _quranReadingMode;
  bool get quranMushafMode => _quranMushafMode;
  bool get masjidMode => _masjidMode;
  QuranScrollMode get quranScrollMode => _quranScrollMode;

  /// Elderly-friendly mode implies at least the "large" text preset, even if
  /// the user hasn't separately bumped text size — the two settings compose
  /// rather than conflict.
  double get effectiveTextScale =>
      _elderlyFriendlyMode ? _textSizePreset.scaleFactor.clamp(1.25, 1.5) : _textSizePreset.scaleFactor;

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
    final presetName = prefs.getString(_kTextSizePreset);
    _textSizePreset = TextSizePreset.values.firstWhere(
      (e) => e.name == presetName,
      orElse: () => TextSizePreset.standard,
    );
    _elderlyFriendlyMode = prefs.getBool(_kElderlyFriendlyMode) ?? false;
    final readingModeName = prefs.getString(_kQuranReadingMode);
    _quranReadingMode = QuranReadingMode.values.firstWhere(
      (e) => e.name == readingModeName,
      orElse: () => QuranReadingMode.arabicTranslation,
    );
    _quranMushafMode = prefs.getBool(_kQuranMushafMode) ?? false;
    final scrollModeName = prefs.getString(_kQuranScrollMode);
    _quranScrollMode = QuranScrollMode.values.firstWhere(
      (e) => e.name == scrollModeName,
      orElse: () => QuranScrollMode.verticalList,
    );
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

  Future<void> setTextSizePreset(TextSizePreset preset) async {
    _textSizePreset = preset;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kTextSizePreset, preset.name);
  }

  Future<void> setElderlyFriendlyMode(bool value) async {
    _elderlyFriendlyMode = value;
    if (value && _textSizePreset == TextSizePreset.standard) {
      _textSizePreset = TextSizePreset.large;
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_kTextSizePreset, _textSizePreset.name);
    }
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_kElderlyFriendlyMode, value);
  }

  Future<void> setQuranReadingMode(QuranReadingMode mode) async {
    _quranReadingMode = mode;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kQuranReadingMode, mode.name);
  }

  Future<void> setQuranMushafMode(bool value) async {
    _quranMushafMode = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_kQuranMushafMode, value);
  }

  Future<void> setQuranScrollMode(QuranScrollMode mode) async {
    _quranScrollMode = mode;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kQuranScrollMode, mode.name);
  }

  /// Deliberately session-only (not persisted): Masjid Mode represents
  /// "currently praying right now," not a durable preference, so it should
  /// never carry over to the next app launch.
  void setMasjidMode(bool value) {
    _masjidMode = value;
    notifyListeners();
  }
}
