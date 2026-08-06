import 'package:flutter/material.dart';
import 'app_colors.dart';

class AppTheme {
  AppTheme._();

  static ThemeData get light => _build(
        brightness: Brightness.light,
        primary: AppColors.primaryLight,
        secondary: AppColors.gold,
        tertiary: AppColors.navy,
        background: AppColors.surfaceLight,
        surface: AppColors.surfaceElevatedLight,
        onSurface: AppColors.textPrimaryLight,
        onSurfaceVariant: AppColors.textSecondaryLight,
        error: AppColors.errorLight,
      );

  static ThemeData get dark => _build(
        brightness: Brightness.dark,
        primary: AppColors.primaryDark,
        secondary: AppColors.goldDark,
        tertiary: AppColors.navyLight,
        background: AppColors.surfaceDark,
        surface: AppColors.surfaceElevatedDark,
        onSurface: AppColors.textPrimaryDark,
        onSurfaceVariant: AppColors.textSecondaryDark,
        error: AppColors.errorDark,
      );

  /// True-black variant of [dark] for AMOLED screens: every pixel that
  /// would otherwise be the dark palette's near-black background becomes
  /// pure black (`#000000`), which AMOLED panels render by turning those
  /// pixels off entirely -- lower battery draw and, for many users,
  /// higher contrast/less eye strain in a dark room. Everything else
  /// (gold accent, text colours) stays identical to [dark].
  static ThemeData get amoled => _build(
        brightness: Brightness.dark,
        primary: AppColors.primaryDark,
        secondary: AppColors.goldDark,
        tertiary: AppColors.navyLight,
        background: Colors.black,
        surface: Colors.black,
        onSurface: AppColors.textPrimaryDark,
        onSurfaceVariant: AppColors.textSecondaryDark,
        error: AppColors.errorDark,
      );

  static ThemeData _build({
    required Brightness brightness,
    required Color primary,
    required Color secondary,
    required Color tertiary,
    required Color background,
    required Color surface,
    required Color onSurface,
    required Color onSurfaceVariant,
    required Color error,
  }) {
    final colorScheme = ColorScheme(
      brightness: brightness,
      primary: primary,
      onPrimary: brightness == Brightness.light ? Colors.white : AppColors.surfaceDark,
      secondary: secondary,
      onSecondary: brightness == Brightness.light ? Colors.white : AppColors.surfaceDark,
      tertiary: tertiary,
      onTertiary: Colors.white,
      error: error,
      onError: Colors.white,
      surface: surface,
      onSurface: onSurface,
      onSurfaceVariant: onSurfaceVariant,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: brightness,
      colorScheme: colorScheme,
      scaffoldBackgroundColor: background,
      appBarTheme: AppBarTheme(
        backgroundColor: background,
        foregroundColor: onSurface,
        elevation: 0,
        centerTitle: true,
      ),
      cardTheme: CardThemeData(
        color: surface,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        margin: EdgeInsets.zero,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          textStyle: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: primary,
          side: BorderSide(color: primary),
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        ),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: surface,
        indicatorColor: secondary.withOpacity(0.22),
        labelTextStyle: WidgetStateProperty.all(
          TextStyle(fontSize: 12, color: onSurface, fontWeight: FontWeight.w500),
        ),
      ),
      listTileTheme: ListTileThemeData(
        iconColor: secondary,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
      switchTheme: SwitchThemeData(
        thumbColor: WidgetStateProperty.resolveWith(
          (states) => states.contains(WidgetState.selected) ? secondary : null,
        ),
        trackColor: WidgetStateProperty.resolveWith(
          (states) => states.contains(WidgetState.selected) ? secondary.withOpacity(0.5) : null,
        ),
      ),
      dividerTheme: DividerThemeData(color: onSurfaceVariant.withOpacity(0.15)),
      textTheme: _textTheme(onSurface),
    );
  }

  static TextTheme _textTheme(Color onSurface) {
    return TextTheme(
      headlineLarge: TextStyle(fontWeight: FontWeight.bold, fontSize: 32, height: 1.25, color: onSurface),
      headlineMedium: TextStyle(fontWeight: FontWeight.bold, fontSize: 26, height: 1.3, color: onSurface),
      titleLarge: TextStyle(fontWeight: FontWeight.w600, fontSize: 22, height: 1.35, color: onSurface),
      titleMedium: TextStyle(fontWeight: FontWeight.w600, fontSize: 18, height: 1.4, color: onSurface),
      bodyLarge: TextStyle(fontWeight: FontWeight.normal, fontSize: 18, height: 1.6, color: onSurface),
      bodyMedium: TextStyle(fontWeight: FontWeight.normal, fontSize: 16, height: 1.5, color: onSurface),
      labelLarge: TextStyle(fontWeight: FontWeight.w500, fontSize: 14, height: 1.3, color: onSurface),
    );
  }
}
