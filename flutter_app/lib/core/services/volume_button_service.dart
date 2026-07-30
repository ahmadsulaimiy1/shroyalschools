import 'package:flutter/services.dart';

/// Bridges to the custom Android host (see android/app/.../MainActivity.kt) which
/// intercepts hardware volume-up/down key events and forwards them here, so the
/// Counter screen can count taps without the user touching the screen at all.
class VolumeButtonService {
  VolumeButtonService._();
  static final instance = VolumeButtonService._();

  static const MethodChannel _channel = MethodChannel('com.misbaha.tasbeeh/volume_buttons');

  void Function()? onVolumeButtonPressed;

  bool _listening = false;

  void _ensureListening() {
    if (_listening) return;
    _listening = true;
    _channel.setMethodCallHandler((call) async {
      if (call.method == 'onVolumeButtonPressed') {
        onVolumeButtonPressed?.call();
      }
    });
  }

  Future<void> setEnabled(bool enabled) async {
    _ensureListening();
    try {
      await _channel.invokeMethod('setEnabled', {'enabled': enabled});
    } on MissingPluginException {
      // Running on a platform/host without the native handler (e.g. tests) — no-op.
    }
  }
}
