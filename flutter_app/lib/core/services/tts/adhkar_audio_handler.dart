import 'package:audio_service/audio_service.dart';
import 'package:flutter_tts/flutter_tts.dart';

/// Splits an adhkar's text into speakable sentences. Android's native
/// TextToSpeech engine has no true pause/resume primitive — it can only
/// start or stop an utterance. To offer a real "Pause" button (not just a
/// fake one), we speak sentence-by-sentence and let pause/resume land on a
/// sentence boundary, which is the same compromise every production
/// TTS-reader app on Android makes.
List<String> splitIntoSentences(String text) {
  final raw = text.split(RegExp(r'(?<=[.؟!])\s+|\n+'));
  return raw.map((s) => s.trim()).where((s) => s.isNotEmpty).toList();
}

enum RepeatMode { off, repeatOne, continuous }

/// Bridges flutter_tts (the actual offline speech engine) to audio_service
/// (real Android MediaSession: lock-screen transport controls, notification,
/// and the foreground service that keeps speech going while the app is
/// backgrounded). Neither package alone gives you both offline TTS *and*
/// lock-screen controls — this handler is the glue between them.
class AdhkarAudioHandler extends BaseAudioHandler with SeekHandler {
  AdhkarAudioHandler() {
    _tts.setCompletionHandler(_onUtteranceComplete);
    _tts.setCancelHandler(() {});
    _tts.setErrorHandler((msg) {
      playbackState.add(playbackState.value.copyWith(processingState: AudioProcessingState.error));
    });
  }

  final FlutterTts _tts = FlutterTts();

  /// Called by the owning controller whenever the "next item" in a
  /// continuous-reading session should start (see [RepeatMode.continuous]).
  Future<void> Function()? onRequestNext;

  List<String> _sentences = [];
  int _sentenceIndex = 0;
  RepeatMode repeatMode = RepeatMode.off;
  bool _stoppedByUser = false;

  Future<void> configureVoice({required String languageCode, String? voiceName, double speechRate = 0.45}) async {
    await _tts.setLanguage(languageCode);
    await _tts.setSpeechRate(speechRate);
    if (voiceName != null) {
      await _tts.setVoice({'name': voiceName, 'locale': languageCode});
    }
  }

  Future<List<Map<String, String>>> availableVoices() async {
    final voices = await _tts.getVoices;
    return (voices as List)
        .map((v) => Map<String, dynamic>.from(v as Map))
        .map((v) => {'name': '${v['name']}', 'locale': '${v['locale']}'})
        .toList();
  }

  Future<void> loadItem({required String id, required String title, required String text, required String languageCode}) async {
    await stop();
    _sentences = splitIntoSentences(text);
    _sentenceIndex = 0;
    mediaItem.add(MediaItem(id: id, title: title, extras: {'languageCode': languageCode}));
  }

  @override
  Future<void> play() async {
    if (_sentences.isEmpty) return;
    _stoppedByUser = false;
    playbackState.add(playbackState.value.copyWith(
      controls: [MediaControl.pause, MediaControl.stop, MediaControl.skipToNext],
      playing: true,
      processingState: AudioProcessingState.ready,
    ));
    await _speakCurrentSentence();
  }

  Future<void> _speakCurrentSentence() async {
    if (_sentenceIndex >= _sentences.length) {
      await _onFinishedAllSentences();
      return;
    }
    await _tts.speak(_sentences[_sentenceIndex]);
  }

  Future<void> _onUtteranceComplete() async {
    if (_stoppedByUser) return;
    _sentenceIndex++;
    if (playbackState.value.playing) {
      await _speakCurrentSentence();
    }
  }

  Future<void> _onFinishedAllSentences() async {
    if (repeatMode == RepeatMode.repeatOne) {
      _sentenceIndex = 0;
      await _speakCurrentSentence();
      return;
    }
    playbackState.add(playbackState.value.copyWith(playing: false, processingState: AudioProcessingState.completed));
    if (repeatMode == RepeatMode.continuous) {
      await onRequestNext?.call();
    }
  }

  @override
  Future<void> pause() async {
    _stoppedByUser = true;
    await _tts.stop();
    playbackState.add(playbackState.value.copyWith(
      controls: [MediaControl.play, MediaControl.stop, MediaControl.skipToNext],
      playing: false,
    ));
  }

  @override
  Future<void> stop() async {
    _stoppedByUser = true;
    await _tts.stop();
    _sentenceIndex = 0;
    playbackState.add(playbackState.value.copyWith(
      playing: false,
      processingState: AudioProcessingState.idle,
    ));
    return super.stop();
  }

  @override
  Future<void> skipToNext() async {
    await onRequestNext?.call();
  }

  Future<void> setSpeechRate(double rate) => _tts.setSpeechRate(rate);
}
