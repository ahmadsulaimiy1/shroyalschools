import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';

import 'core/database/counter_repository.dart';
import 'core/database/database_helper.dart';
import 'core/localization/app_localizations.dart';
import 'core/services/active_dhikr_controller.dart';
import 'core/services/feedback_service.dart';
import 'core/services/settings_controller.dart';
import 'core/theme/app_theme.dart';
import 'features/splash/splash_screen.dart';

class MisbahaApp extends StatelessWidget {
  const MisbahaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<SettingsController>(create: (_) => SettingsController()..load()),
        Provider<CounterRepository>(create: (_) => CounterRepository(DatabaseHelper.instance)),
        ChangeNotifierProvider<ActiveDhikrController>(create: (_) => ActiveDhikrController()),
        ProxyProvider<SettingsController, FeedbackService>(
          update: (_, settings, __) => FeedbackService(settings),
        ),
      ],
      child: Consumer<SettingsController>(
        builder: (context, settings, _) {
          return MaterialApp(
            title: 'Misbaha',
            debugShowCheckedModeBanner: false,
            theme: AppTheme.light,
            darkTheme: AppTheme.dark,
            themeMode: settings.flutterThemeMode,
            locale: settings.locale,
            supportedLocales: AppLocalizations.supportedLocales,
            localizationsDelegates: const [
              AppLocalizations.delegate,
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],
            builder: (context, child) {
              final isRtl = settings.locale.languageCode == 'ar';
              return Directionality(
                textDirection: isRtl ? TextDirection.rtl : TextDirection.ltr,
                child: child ?? const SizedBox.shrink(),
              );
            },
            home: const SplashScreen(),
          );
        },
      ),
    );
  }
}
