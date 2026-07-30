import 'package:audio_service/audio_service.dart';
import 'package:flutter/material.dart';

import 'app.dart';
import 'core/services/tts/adhkar_audio_handler.dart';

late final AdhkarAudioHandler audioHandler;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Registers the app with Android's MediaSession so TTS playback gets a
  // real lock-screen/notification transport and a foreground service that
  // survives the app being backgrounded — see core/services/tts/. This binds
  // to a native service, which on some devices (OEM battery/foreground-
  // service restrictions, notification permission not yet granted) can be
  // slow or never resolve. A stuck native binding must never keep the whole
  // app on the launch screen forever, so it's bounded by a timeout with a
  // plain (non-MediaSession) fallback handler — the app still launches and
  // TTS still plays, just without lock-screen/background transport controls.
  try {
    audioHandler = await AudioService.init(
      builder: () => AdhkarAudioHandler(),
      config: const AudioServiceConfig(
        androidNotificationChannelId: 'com.misbaha.tasbeeh.audio',
        androidNotificationChannelName: 'Misbaha Adhkar Reading',
        androidNotificationOngoing: false,
        androidStopForegroundOnPause: true,
      ),
    ).timeout(const Duration(seconds: 5));
  } catch (_) {
    audioHandler = AdhkarAudioHandler();
  }

  runApp(const MisbahaApp());
}
