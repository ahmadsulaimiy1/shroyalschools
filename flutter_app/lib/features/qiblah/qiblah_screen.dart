import 'dart:async';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter_compass/flutter_compass.dart';
import 'package:geolocator/geolocator.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/services/qiblah_service.dart';
import '../../core/theme/app_colors.dart';

enum _QiblahLoadState { locating, noPermission, noService, noSensor, ready, error }

/// Points toward the Kaaba using the device's magnetometer (compass heading)
/// combined with a great-circle bearing computed from the device's GPS
/// position -- see core/services/qiblah_service.dart. Sensor/location
/// behaviour cannot be exercised in a build sandbox with no physical
/// device; this should be spot-checked on a real phone before release
/// (heading calibration in particular is a known real-world quirk of
/// magnetometer-based compasses, addressed here by an explicit in-app
/// calibration guide rather than just a passive hint).
class QiblahScreen extends StatefulWidget {
  const QiblahScreen({super.key});

  @override
  State<QiblahScreen> createState() => _QiblahScreenState();
}

class _QiblahScreenState extends State<QiblahScreen> {
  _QiblahLoadState _state = _QiblahLoadState.locating;
  double? _qiblahBearing;
  double? _distanceKm;
  StreamSubscription<CompassEvent>? _compassSub;
  double? _heading;
  double? _headingAccuracy;

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    if (!await Geolocator.isLocationServiceEnabled()) {
      setState(() => _state = _QiblahLoadState.noService);
      return;
    }
    var permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    if (permission == LocationPermission.denied || permission == LocationPermission.deniedForever) {
      setState(() => _state = _QiblahLoadState.noPermission);
      return;
    }

    try {
      final position = await Geolocator.getCurrentPosition();
      final bearing = QiblahService.bearingTo(position.latitude, position.longitude);
      final distance = QiblahService.distanceKm(position.latitude, position.longitude);
      if (!mounted) return;
      setState(() {
        _qiblahBearing = bearing;
        _distanceKm = distance;
      });
      _listenToCompass();
    } catch (_) {
      if (mounted) setState(() => _state = _QiblahLoadState.error);
    }
  }

  void _listenToCompass() {
    final events = FlutterCompass.events;
    if (events == null) {
      setState(() => _state = _QiblahLoadState.noSensor);
      return;
    }
    _compassSub = events.listen((event) {
      if (event.heading == null) return;
      if (!mounted) return;
      setState(() {
        _heading = event.heading;
        _headingAccuracy = event.accuracy;
        _state = _QiblahLoadState.ready;
      });
    });
  }

  @override
  void dispose() {
    _compassSub?.cancel();
    super.dispose();
  }

  void _showCalibrationGuide() {
    final t = context.loc.t;
    showModalBottomSheet(
      context: context,
      backgroundColor: AppColors.navy,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) => Padding(
        padding: const EdgeInsets.fromLTRB(24, 28, 24, 36),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const _FigureEightAnimation(),
            const SizedBox(height: 20),
            Text(
              t('qiblah_calibrate_title'),
              style: const TextStyle(color: AppColors.gold, fontSize: 18, fontWeight: FontWeight.w700),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            Text(
              t('qiblah_calibrate_steps'),
              style: const TextStyle(color: Colors.white70, height: 1.5),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 20),
            FilledButton(
              style: FilledButton.styleFrom(backgroundColor: AppColors.gold, foregroundColor: Colors.black),
              onPressed: () => Navigator.of(context).pop(),
              child: Text(t('qiblah_calibrate_done')),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: theme.brightness == Brightness.dark ? AppColors.surfaceDark : AppColors.surfaceLight,
      appBar: AppBar(title: Text(t('qiblah_title'))),
      body: Center(
        child: switch (_state) {
          _QiblahLoadState.locating => const CircularProgressIndicator(),
          _QiblahLoadState.noService => _Message(icon: Icons.location_off_outlined, text: t('qiblah_no_location_service')),
          _QiblahLoadState.noPermission => _Message(icon: Icons.location_disabled_outlined, text: t('qiblah_no_permission')),
          _QiblahLoadState.noSensor => _Message(icon: Icons.explore_off_outlined, text: t('qiblah_no_sensor')),
          _QiblahLoadState.error => _Message(icon: Icons.error_outline, text: t('qiblah_error')),
          _QiblahLoadState.ready => _CompassDial(
              heading: _heading ?? 0,
              qiblahBearing: _qiblahBearing ?? 0,
              distanceKm: _distanceKm ?? 0,
              accuracy: _headingAccuracy,
              theme: theme,
              t: t,
              onCalibrate: _showCalibrationGuide,
            ),
        },
      ),
    );
  }
}

class _Message extends StatelessWidget {
  const _Message({required this.icon, required this.text});
  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 48, color: Theme.of(context).colorScheme.onSurfaceVariant),
          const SizedBox(height: 16),
          Text(text, textAlign: TextAlign.center),
        ],
      ),
    );
  }
}

/// A slowly rotating figure-8 path traced by a small dot, illustrating the
/// motion a magnetometer calibration gesture needs -- shown inside the
/// calibration guide sheet rather than only described in words.
class _FigureEightAnimation extends StatefulWidget {
  const _FigureEightAnimation();

  @override
  State<_FigureEightAnimation> createState() => _FigureEightAnimationState();
}

class _FigureEightAnimationState extends State<_FigureEightAnimation> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(seconds: 2))..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 120,
      height: 70,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, _) {
          final t = _controller.value * 2 * math.pi;
          final x = 50 * math.sin(t);
          final y = 25 * math.sin(t) * math.cos(t);
          return Stack(
            children: [
              Center(
                child: Icon(Icons.explore_outlined, size: 40, color: AppColors.gold.withOpacity(0.35)),
              ),
              Positioned(
                left: 60 + x - 6,
                top: 35 + y - 6,
                child: Container(
                  width: 12,
                  height: 12,
                  decoration: const BoxDecoration(shape: BoxShape.circle, color: AppColors.gold),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

class _CompassDial extends StatelessWidget {
  const _CompassDial({
    required this.heading,
    required this.qiblahBearing,
    required this.distanceKm,
    required this.accuracy,
    required this.theme,
    required this.t,
    required this.onCalibrate,
  });

  final double heading;
  final double qiblahBearing;
  final double distanceKm;
  final double? accuracy;
  final ThemeData theme;
  final String Function(String) t;
  final VoidCallback onCalibrate;

  @override
  Widget build(BuildContext context) {
    // Rotate the needle by (qiblahBearing - deviceHeading): when the phone
    // is pointed exactly at the Qiblah, this is 0 and the needle points
    // straight up. Normalised to (-180, 180] and expressed in turns (not
    // radians) so TweenAnimationBuilder eases between readings smoothly
    // instead of snapping with every raw magnetometer sample.
    var delta = qiblahBearing - heading;
    delta = ((delta + 180) % 360 + 360) % 360 - 180;
    final needleTurns = delta / 360.0;
    final isAligned = delta.abs() < 3;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(
          width: 300,
          height: 300,
          child: Stack(
            alignment: Alignment.center,
            children: [
              // Outer metallic ring: a radial gold gradient gives a
              // brushed-metal impression without any image asset.
              Container(
                width: 300,
                height: 300,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: SweepGradient(
                    colors: [AppColors.goldDark, AppColors.gold, AppColors.navyLight, AppColors.gold, AppColors.goldDark],
                    stops: const [0.0, 0.25, 0.5, 0.75, 1.0],
                  ),
                  boxShadow: [BoxShadow(color: AppColors.gold.withOpacity(0.35), blurRadius: 24, spreadRadius: 2)],
                ),
              ),
              Container(
                width: 284,
                height: 284,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: theme.brightness == Brightness.dark ? AppColors.surfaceDark : AppColors.surfaceElevatedLight,
                ),
              ),
              CustomPaint(size: const Size(284, 284), painter: _DialTicksPainter(color: AppColors.gold.withOpacity(0.7))),
              Container(
                width: 8,
                height: 8,
                decoration: BoxDecoration(shape: BoxShape.circle, color: isAligned ? AppColors.primaryLight : AppColors.gold),
              ),
              TweenAnimationBuilder<double>(
                tween: Tween(begin: 0, end: needleTurns),
                duration: const Duration(milliseconds: 260),
                curve: Curves.easeOut,
                builder: (context, turns, child) => Transform.rotate(angle: turns * 2 * math.pi, child: child),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.mosque, color: isAligned ? AppColors.primaryLight : AppColors.gold, size: 42),
                    Container(
                      width: 3,
                      height: 100,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [isAligned ? AppColors.primaryLight : AppColors.gold, Colors.transparent],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),
        AnimatedOpacity(
          opacity: isAligned ? 1 : 0.7,
          duration: const Duration(milliseconds: 200),
          child: Text(
            isAligned ? t('qiblah_aligned') : t('qiblah_instruction'),
            style: theme.textTheme.titleMedium?.copyWith(
              color: isAligned ? AppColors.primaryLight : null,
              fontWeight: isAligned ? FontWeight.w700 : null,
            ),
            textAlign: TextAlign.center,
          ),
        ),
        const SizedBox(height: 8),
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.place_outlined, size: 16, color: theme.colorScheme.onSurfaceVariant),
            const SizedBox(width: 4),
            Text(
              context.loc.tArgs('qiblah_distance', [distanceKm.round()]),
              style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
          ],
        ),
        const SizedBox(height: 12),
        TextButton.icon(
          onPressed: onCalibrate,
          icon: const Icon(Icons.explore_outlined, size: 18),
          label: Text(t('qiblah_calibrate_action')),
        ),
        if (accuracy != null && accuracy! > 15) ...[
          const SizedBox(height: 4),
          Text(t('qiblah_calibrate_hint'), style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.error)),
        ],
      ],
    );
  }
}

/// Draws 36 tick marks (one per 10°) around the dial, with the four
/// cardinal ticks slightly longer -- a restrained, image-free way to give
/// the compass face real instrument detail.
class _DialTicksPainter extends CustomPainter {
  const _DialTicksPainter({required this.color});
  final Color color;

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;
    final paint = Paint()..color = color;
    for (var i = 0; i < 36; i++) {
      final angle = (i * 10) * math.pi / 180;
      final isCardinal = i % 9 == 0;
      final tickLength = isCardinal ? 14.0 : 7.0;
      final strokeWidth = isCardinal ? 2.0 : 1.0;
      final outer = Offset(center.dx + radius * math.sin(angle), center.dy - radius * math.cos(angle));
      final inner = Offset(
        center.dx + (radius - tickLength) * math.sin(angle),
        center.dy - (radius - tickLength) * math.cos(angle),
      );
      canvas.drawLine(outer, inner, paint..strokeWidth = strokeWidth);
    }
  }

  @override
  bool shouldRepaint(covariant _DialTicksPainter oldDelegate) => oldDelegate.color != color;
}
