import 'package:flutter/services.dart';

import 'settings_controller.dart';

/// Tap feedback: a soft system click (no bundled audio asset needed) plus
/// haptic feedback — both individually toggleable from Settings.
class FeedbackService {
  FeedbackService(this._settings);
  final SettingsController _settings;

  void onCount() {
    if (_settings.soundEnabled) {
      SystemSound.play(SystemSoundType.click);
    }
    if (_settings.vibrationEnabled) {
      HapticFeedback.mediumImpact();
    }
  }

  void onComplete() {
    if (_settings.soundEnabled) {
      SystemSound.play(SystemSoundType.alert);
    }
    if (_settings.vibrationEnabled) {
      HapticFeedback.heavyImpact();
    }
  }
}
