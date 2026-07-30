import 'package:audio_service/audio_service.dart';
import 'package:flutter/material.dart';

import 'app.dart';
import 'core/services/tts/adhkar_audio_handler.dart';

late final AdhkarAudioHandler audioHandler;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Registers the app with Android's MediaSession so TTS playback gets a
  // real lock-screen/notification transport and a foreground service that
  // survives the app being backgrounded — see core/services/tts/.
  audioHandler = await AudioService.init(
    builder: () => AdhkarAudioHandler(),
    config: const AudioServiceConfig(
      androidNotificationChannelId: 'com.misbaha.tasbeeh.audio',
      androidNotificationChannelName: 'Misbaha Adhkar Reading',
      androidNotificationOngoing: false,
      androidStopForegroundOnPause: true,
    ),
  );

  runApp(const MisbahaApp());
}
