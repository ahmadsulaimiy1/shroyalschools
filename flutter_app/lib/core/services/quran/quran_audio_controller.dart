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

  /// Memorisation Mode: repeat each verse [memorizationTargetRepeats] times
  /// before moving on to the next one in the playlist -- handled entirely
  /// in this controller (the shared handler's own repeat modes are left at
  /// [RepeatMode.off] while this is active) so it never races with the
  /// handler's internal repeatOne/continuous timing.
  bool _memorizationMode = false;
  int memorizationTargetRepeats = 3;
  int _memorizationRepeatsLeft = 0;
  bool get memorizationMode => _memorizationMode;

  /// Repeat Range: when the current playlist reaches its last verse, start
  /// over from its first verse instead of stopping -- used for looping a
  /// user-selected verse range indefinitely (see quran_reader_screen.dart's
  /// "Repeat Range" action). Requires [repeatMode] to be [RepeatMode.continuous]
  /// as well, since that's what makes the shared handler call back into this
  /// controller when a verse finishes at all; this flag only changes what
  /// happens once the playlist itself runs out.
  bool _loopPlaylist = false;
  bool get loopPlaylist => _loopPlaylist;
  void setLoopPlaylist(bool value) {
    _loopPlaylist = value;
    notifyListeners();
  }

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

  /// Set to true immediately before an internal same-verse replay so
  /// [playVerse] knows not to reset the memorisation repeat counter.
  bool _isMemorizationReplay = false;

  void setMemorizationMode(bool enabled) {
    _memorizationMode = enabled;
    notifyListeners();
  }

  /// Plays [verse] aloud. [playlist] + [index] enable continuous recitation:
  /// when this verse finishes and repeat mode is [RepeatMode.continuous],
  /// the next verse in [playlist] starts automatically. When
  /// [memorizationMode] is on, each verse instead repeats
  /// [memorizationTargetRepeats] times before advancing.
  Future<void> playVerse(QuranVerse verse, {List<QuranVerse>? playlist, int? index}) async {
    _playlist = playlist ?? [verse];
    _currentIndex = index ?? _playlist.indexWhere((v) => v.surah == verse.surah && v.ayah == verse.ayah);
    if (_currentIndex < 0) _currentIndex = 0;

    if (!_isMemorizationReplay) {
      _memorizationRepeatsLeft = memorizationTargetRepeats;
    }
    _isMemorizationReplay = false;

    _status = QuranPlaybackStatus.loading;
    notifyListeners();

    final source = await _audioService.audioSourceFor(verse.surah, verse.ayah, reciter: _reciter);
    await _handler.loadQuranAudio(
      id: verse.key,
      title: 'Surah ${verse.surah}, Ayah ${verse.ayah}',
      audioSource: source,
    );
    // Memorisation Mode drives its own repeat/advance logic from
    // _onPlaybackStateChanged below, so the shared handler is told not to
    // do anything special on completion while it's active.
    _handler.repeatMode = _memorizationMode ? RepeatMode.off : _repeatMode;
    // Shared with TtsController — reclaimed here so continuous mode always
    // advances whichever content (adhkar or Qur'an) is currently playing.
    _handler.onRequestNext = _playNextInPlaylist;
    await _handler.setAudioSpeed(_speed);
    await _handler.play();
  }

  Future<void> _playNextInPlaylist() async {
    if (_currentIndex + 1 < _playlist.length) {
      await playVerse(_playlist[_currentIndex + 1], playlist: _playlist, index: _currentIndex + 1);
    } else if (_loopPlaylist && _playlist.isNotEmpty) {
      await playVerse(_playlist[0], playlist: _playlist, index: 0);
    } else {
      _status = QuranPlaybackStatus.completed;
      notifyListeners();
    }
  }

  Future<void> _replayCurrentVerse() async {
    final verse = currentVerse;
    if (verse == null) return;
    _isMemorizationReplay = true;
    await playVerse(verse, playlist: _playlist, index: _currentIndex);
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
      if (_memorizationMode) {
        _memorizationRepeatsLeft--;
        if (_memorizationRepeatsLeft > 0) {
          _replayCurrentVerse();
        } else {
          _memorizationRepeatsLeft = memorizationTargetRepeats;
          _playNextInPlaylist();
        }
      }
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
