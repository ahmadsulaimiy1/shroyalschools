import 'dart:async';

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
/// magnetometer-based compasses, addressed here only by prompting the
/// user to calibrate if accuracy looks poor).
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

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final theme = Theme.of(context);

    return Scaffold(
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

class _CompassDial extends StatelessWidget {
  const _CompassDial({
    required this.heading,
    required this.qiblahBearing,
    required this.distanceKm,
    required this.accuracy,
    required this.theme,
    required this.t,
  });

  final double heading;
  final double qiblahBearing;
  final double distanceKm;
  final double? accuracy;
  final ThemeData theme;
  final String Function(String) t;

  @override
  Widget build(BuildContext context) {
    // Rotate the needle by (qiblahBearing - deviceHeading): when the phone
    // is pointed exactly at the Qiblah, this is 0 and the needle points
    // straight up.
    final needleAngle = (qiblahBearing - heading) * (3.14159265 / 180.0);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(
          width: 260,
          height: 260,
          child: Stack(
            alignment: Alignment.center,
            children: [
              Container(
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: AppColors.gold, width: 2),
                ),
              ),
              Transform.rotate(
                angle: needleAngle,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.mosque, color: AppColors.gold, size: 40),
                    Container(width: 4, height: 90, color: AppColors.gold),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        Text(t('qiblah_instruction'), style: theme.textTheme.titleMedium, textAlign: TextAlign.center),
        const SizedBox(height: 8),
        Text(
          context.loc.tArgs('qiblah_distance', [distanceKm.round()]),
          style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
        ),
        if (accuracy != null && accuracy! > 15) ...[
          const SizedBox(height: 16),
          Text(t('qiblah_calibrate_hint'), style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.error)),
        ],
      ],
    );
  }
}
