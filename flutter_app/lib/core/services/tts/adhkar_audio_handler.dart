import 'package:audio_service/audio_service.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:just_audio/just_audio.dart';

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

/// Which playback engine currently owns the shared handler — TtsController
/// and QuranAudioController both listen to the same [AdhkarAudioHandler.playbackState]
/// stream, and each needs to ignore state changes that belong to the other.
enum AudioEngineKind { none, tts, audio }

/// The app's single shared audio_service handler — Android only allows one
/// MediaSession-backed BaseAudioHandler per process, so both playback modes
/// live here rather than as two competing handlers:
///
///  - Adhkar reading: flutter_tts speaking sentence-by-sentence (genuinely
///    offline, no network involved).
///  - Qur'an recitation: real Qari audio via just_audio's caching source,
///    which streams from the network on first play and transparently reads
///    from the local cache file on every play after that — Qur'an
///    recitation is never synthesized speech, see docs/15-QURAN-DATA-SOURCE-VERIFICATION.md
///    for why.
///
/// Whichever engine is active drives the shared `playbackState`/`mediaItem`
/// streams, so lock-screen/notification transport controls work the same
/// way regardless of which one is playing.
class AdhkarAudioHandler extends BaseAudioHandler with SeekHandler {
  AdhkarAudioHandler() {
    _tts.setCompletionHandler(_onUtteranceComplete);
    _tts.setCancelHandler(() {});
    _tts.setErrorHandler((msg) {
      playbackState.add(playbackState.value.copyWith(processingState: AudioProcessingState.error));
    });

    _audioPlayer.playerStateStream.listen(_onAudioPlayerStateChanged);
  }

  final FlutterTts _tts = FlutterTts();
  final AudioPlayer _audioPlayer = AudioPlayer();
  AudioEngineKind _engine = AudioEngineKind.none;

  /// Lets TtsController/QuranAudioController tell apart a playbackState
  /// event meant for them from one meant for the other engine, since both
  /// listen to the same shared stream.
  AudioEngineKind get activeEngine => _engine;

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
    _engine = AudioEngineKind.tts;
    _sentences = splitIntoSentences(text);
    _sentenceIndex = 0;
    mediaItem.add(MediaItem(id: id, title: title, extras: {'languageCode': languageCode}));
  }

  /// Loads a Qur'an verse's recitation audio, backed by [audioSource] (a
  /// [LockCachingAudioSource] so the caller controls exactly where the
  /// cached file lives — see QuranAudioService).
  Future<void> loadQuranAudio({
    required String id,
    required String title,
    required AudioSource audioSource,
  }) async {
    await stop();
    _engine = AudioEngineKind.audio;
    await _audioPlayer.setAudioSource(audioSource);
    mediaItem.add(MediaItem(id: id, title: title));
  }

  @override
  Future<void> play() async {
    if (_engine == AudioEngineKind.audio) {
      _stoppedByUser = false;
      await _audioPlayer.play();
      return;
    }
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
    if (_stoppedByUser || _engine != AudioEngineKind.tts) return;
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

  void _onAudioPlayerStateChanged(PlayerState state) {
    if (_engine != AudioEngineKind.audio) return;
    final processingState = switch (state.processingState) {
      ProcessingState.idle => AudioProcessingState.idle,
      ProcessingState.loading => AudioProcessingState.loading,
      ProcessingState.buffering => AudioProcessingState.buffering,
      ProcessingState.ready => AudioProcessingState.ready,
      ProcessingState.completed => AudioProcessingState.completed,
    };
    playbackState.add(playbackState.value.copyWith(
      controls: [
        state.playing ? MediaControl.pause : MediaControl.play,
        MediaControl.stop,
        MediaControl.skipToNext,
      ],
      playing: state.playing,
      processingState: processingState,
    ));
    if (state.processingState == ProcessingState.completed && !_stoppedByUser) {
      if (repeatMode == RepeatMode.repeatOne) {
        _audioPlayer.seek(Duration.zero);
        _audioPlayer.play();
      } else if (repeatMode == RepeatMode.continuous) {
        onRequestNext?.call();
      }
    }
  }

  @override
  Future<void> pause() async {
    _stoppedByUser = true;
    if (_engine == AudioEngineKind.audio) {
      await _audioPlayer.pause();
      return;
    }
    await _tts.stop();
    playbackState.add(playbackState.value.copyWith(
      controls: [MediaControl.play, MediaControl.stop, MediaControl.skipToNext],
      playing: false,
    ));
  }

  @override
  Future<void> stop() async {
    _stoppedByUser = true;
    if (_engine == AudioEngineKind.audio) {
      await _audioPlayer.stop();
    } else {
      await _tts.stop();
    }
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

  Future<void> setAudioSpeed(double speed) => _audioPlayer.setSpeed(speed);
}
