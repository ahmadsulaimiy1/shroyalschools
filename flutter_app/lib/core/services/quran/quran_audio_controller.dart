import 'package:audio_service/audio_service.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../models/quran_verse.dart';
import '../tts/adhkar_audio_handler.dart';
import 'quran_audio_service.dart';

const _kQuranReciterPref = 'quran_reciter';

enum QuranPlaybackStatus { idle, loading, playing, paused, completed }

/// The Qur'an screens' single point of contact with recitation audio —
/// mirrors TtsController's shape (same shared handler, same playlist/
/// continuous-mode idea) but plays real Qari audio via [QuranAudioService]
/// instead of speaking text through flutter_tts.
class QuranAudioController extends ChangeNotifier {
  QuranAudioController(this._handler, this._audioService) {
    _handler.playbackState.listen(_onPlaybackStateChanged);
    _loadReciter();
  }

  Future<void> _loadReciter() async {
    final prefs = await SharedPreferences.getInstance();
    final name = prefs.getString(_kQuranReciterPref);
    final match = QuranReciter.values.where((r) => r.name == name);
    if (match.isNotEmpty) {
      _reciter = match.first;
      notifyListeners();
    }
  }

  final AdhkarAudioHandler _handler;
  final QuranAudioService _audioService;

  List<QuranVerse> _playlist = [];
  int _currentIndex = -1;
  double _speed = 1.0;
  RepeatMode _repeatMode = RepeatMode.off;
  QuranPlaybackStatus _status = QuranPlaybackStatus.idle;

  QuranVerse? get currentVerse => (_currentIndex >= 0 && _currentIndex < _playlist.length) ? _playlist[_currentIndex] : null;
  QuranPlaybackStatus get status => _status;
  double get speed => _speed;
  RepeatMode get repeatMode => _repeatMode;

  bool isCurrentlyPlaying(QuranVerse verse) =>
      currentVerse?.surah == verse.surah && currentVerse?.ayah == verse.ayah && _status == QuranPlaybackStatus.playing;

  QuranReciter _reciter = QuranReciter.alafasy;
  QuranReciter get reciter => _reciter;
  Future<void> setReciter(QuranReciter reciter) async {
    _reciter = reciter;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kQuranReciterPref, reciter.name);
  }

  /// Plays [verse] aloud. [playlist] + [index] enable continuous recitation:
  /// when this verse finishes and repeat mode is [RepeatMode.continuous],
  /// the next verse in [playlist] starts automatically.
  Future<void> playVerse(QuranVerse verse, {List<QuranVerse>? playlist, int? index}) async {
    _playlist = playlist ?? [verse];
    _currentIndex = index ?? _playlist.indexWhere((v) => v.surah == verse.surah && v.ayah == verse.ayah);
    if (_currentIndex < 0) _currentIndex = 0;

    _status = QuranPlaybackStatus.loading;
    notifyListeners();

    final source = await _audioService.audioSourceFor(verse.surah, verse.ayah, reciter: _reciter);
    await _handler.loadQuranAudio(
      id: verse.key,
      title: 'Surah ${verse.surah}, Ayah ${verse.ayah}',
      audioSource: source,
    );
    _handler.repeatMode = _repeatMode;
    // Shared with TtsController — reclaimed here so continuous mode always
    // advances whichever content (adhkar or Qur'an) is currently playing.
    _handler.onRequestNext = _playNextInPlaylist;
    await _handler.setAudioSpeed(_speed);
    await _handler.play();
  }

  Future<void> _playNextInPlaylist() async {
    if (_currentIndex + 1 < _playlist.length) {
      await playVerse(_playlist[_currentIndex + 1], playlist: _playlist, index: _currentIndex + 1);
    } else {
      _status = QuranPlaybackStatus.completed;
      notifyListeners();
    }
  }

  Future<void> pause() => _handler.pause();

  Future<void> resume() => _handler.play();

  Future<void> stop() => _handler.stop();

  Future<void> setSpeed(double speed) async {
    _speed = speed;
    await _handler.setAudioSpeed(speed);
    notifyListeners();
  }

  void setRepeatMode(RepeatMode mode) {
    _repeatMode = mode;
    _handler.repeatMode = mode;
    notifyListeners();
  }

  void _onPlaybackStateChanged(PlaybackState state) {
    // The handler is shared with TtsController — ignore state changes that
    // belong to the Adhkar TTS engine, not this Qur'an audio one.
    if (_handler.activeEngine == AudioEngineKind.tts) return;
    if (state.processingState == AudioProcessingState.completed) {
      _status = QuranPlaybackStatus.completed;
    } else if (state.processingState == AudioProcessingState.loading ||
        state.processingState == AudioProcessingState.buffering) {
      _status = QuranPlaybackStatus.loading;
    } else if (state.playing) {
      _status = QuranPlaybackStatus.playing;
    } else if (state.processingState == AudioProcessingState.idle) {
      _status = QuranPlaybackStatus.idle;
    } else {
      _status = QuranPlaybackStatus.paused;
    }
    notifyListeners();
  }
}
