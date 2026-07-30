import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';

import 'core/database/adhkar_repository.dart';
import 'core/database/counter_repository.dart';
import 'core/database/database_helper.dart';
import 'core/localization/app_localizations.dart';
import 'core/services/active_dhikr_controller.dart';
import 'core/services/feedback_service.dart';
import 'core/services/recently_read_service.dart';
import 'core/services/settings_controller.dart';
import 'core/services/tts/tts_controller.dart';
import 'core/theme/app_theme.dart';
import 'features/splash/splash_screen.dart';
import 'main.dart' show audioHandler;

class MisbahaApp extends StatelessWidget {
  const MisbahaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<SettingsController>(create: (_) => SettingsController()..load()),
        Provider<CounterRepository>(create: (_) => CounterRepository(DatabaseHelper.instance)),
        Provider<AdhkarRepository>(create: (_) => AdhkarRepository(DatabaseHelper.instance)),
        Provider<RecentlyReadService>(create: (_) => RecentlyReadService()),
        ChangeNotifierProvider<ActiveDhikrController>(create: (_) => ActiveDhikrController()),
        ChangeNotifierProvider<TtsController>(create: (_) => TtsController(audioHandler)..loadVoices()),
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
                child: MediaQuery(
                  data: MediaQuery.of(context).copyWith(
                    textScaler: TextScaler.linear(settings.effectiveTextScale),
                  ),
                  child: child ?? const SizedBox.shrink(),
                ),
              );
            },
            home: const SplashScreen(),
          );
        },
      ),
    );
  }
}
