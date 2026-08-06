import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/data/adhkar_seed_data.dart';
import '../../core/database/adhkar_repository.dart';
import '../../core/localization/app_localizations.dart';
import '../../core/services/notifications/reminder_scheduler.dart';
import '../../core/widgets/app_shell.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
  late final AnimationController _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 700),
  )..forward();
  late final Animation<double> _scale = CurvedAnimation(parent: _controller, curve: Curves.easeOutBack);
  late final Animation<double> _fade = CurvedAnimation(parent: _controller, curve: Curves.easeIn);

  @override
  void initState() {
    super.initState();
    // Fire-and-forget: seeds the offline adhkar library on first run without
    // blocking the splash animation. Safe to call every launch — insertion
    // is idempotent (existing ids are skipped, favourites untouched).
    context.read<AdhkarRepository>().seedIfNeeded(wirdAlMusaffaSeed);
    // Re-primes the worship reminder system on every launch -- covers both
    // "a reminder was enabled last session, extend its rolling window" and
    // "prayer times shifted since yesterday". Scheduling without the
    // notification/exact-alarm permission granted is harmless (Android
    // simply won't surface anything); the permission itself is only ever
    // requested when the user actually turns a reminder on, from the
    // Notifications settings screen -- never uninvited here.
    rescheduleReminders(context);
    Timer(const Duration(milliseconds: 1400), _goToShell);
  }

  void _goToShell() {
    if (!mounted) return;
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const AppShell()),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: Center(
        child: FadeTransition(
          opacity: _fade,
          child: ScaleTransition(
            scale: _scale,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 120,
                  height: 120,
                  decoration: BoxDecoration(
                    color: theme.colorScheme.primary,
                    borderRadius: BorderRadius.circular(32),
                  ),
                  child: Icon(Icons.fingerprint, color: theme.colorScheme.secondary, size: 64),
                ),
                const SizedBox(height: 24),
                Text(context.t('app_name'), style: theme.textTheme.headlineLarge),
                const SizedBox(height: 8),
                Text(
                  context.t('tagline'),
                  style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
