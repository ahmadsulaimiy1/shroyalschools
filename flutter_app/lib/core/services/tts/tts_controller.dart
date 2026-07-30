import 'package:audio_service/audio_service.dart';
import 'package:flutter/foundation.dart';

import '../../models/adhkar_entry.dart';
import 'adhkar_audio_handler.dart';

enum TtsPlaybackStatus { idle, playing, paused, completed }

/// The Adhkar screens' single point of contact with TTS/audio_service —
/// screens call [playEntry]/[pause]/[resume]/[stop]/[setSpeed]/[setRepeatMode]
/// and listen via ChangeNotifier rather than touching AudioHandler directly.
class TtsController extends ChangeNotifier {
  TtsController(this._handler) {
    _handler.playbackState.listen(_onPlaybackStateChanged);
  }

  final AdhkarAudioHandler _handler;

  List<AdhkarEntry> _playlist = [];
  int _currentIndex = -1;
  double _speechRate = 0.45;
  RepeatMode _repeatMode = RepeatMode.off;
  TtsPlaybackStatus _status = TtsPlaybackStatus.idle;
  List<Map<String, String>> _arabicVoices = [];
  List<Map<String, String>> _englishVoices = [];
  String? _selectedArabicVoice;
  String? _selectedEnglishVoice;

  AdhkarEntry? get currentEntry => (_currentIndex >= 0 && _currentIndex < _playlist.length) ? _playlist[_currentIndex] : null;
  TtsPlaybackStatus get status => _status;
  double get speechRate => _speechRate;
  RepeatMode get repeatMode => _repeatMode;
  List<Map<String, String>> get arabicVoices => _arabicVoices;
  List<Map<String, String>> get englishVoices => _englishVoices;
  String? get selectedArabicVoice => _selectedArabicVoice;
  String? get selectedEnglishVoice => _selectedEnglishVoice;

  Future<void> loadVoices() async {
    final voices = await _handler.availableVoices();
    _arabicVoices = voices.where((v) => (v['locale'] ?? '').toLowerCase().startsWith('ar')).toList();
    _englishVoices = voices.where((v) => (v['locale'] ?? '').toLowerCase().startsWith('en')).toList();
    notifyListeners();
  }

  bool get hasArabicVoice => _arabicVoices.isNotEmpty;
  bool get hasEnglishVoice => _englishVoices.isNotEmpty;

  void setArabicVoice(String? name) {
    _selectedArabicVoice = name;
    notifyListeners();
  }

  void setEnglishVoice(String? name) {
    _selectedEnglishVoice = name;
    notifyListeners();
  }

  /// Speak the Arabic text of [entry]. [playlist] + [index] enable
  /// "continuous reading mode": when this entry finishes and repeat mode is
  /// [RepeatMode.continuous], the next entry in [playlist] starts automatically.
  Future<void> playEntry(AdhkarEntry entry, {List<AdhkarEntry>? playlist, int? index, bool arabic = true}) async {
    _playlist = playlist ?? [entry];
    _currentIndex = index ?? _playlist.indexWhere((e) => e.id == entry.id);
    if (_currentIndex < 0) _currentIndex = 0;

    await _handler.loadItem(
      id: entry.id,
      title: entry.titleAr,
      text: arabic ? entry.arabicText : entry.translationEn,
      languageCode: arabic ? 'ar' : 'en-GB',
    );
    await _handler.configureVoice(
      languageCode: arabic ? 'ar' : 'en-GB',
      voiceName: arabic ? _selectedArabicVoice : _selectedEnglishVoice,
      speechRate: _speechRate,
    );
    _handler.repeatMode = _repeatMode;
    // The handler is shared with QuranAudioController (only one MediaSession
    // handler is allowed per app) — (re)claim onRequestNext here rather than
    // once in the constructor, so whichever controller last started playback
    // is the one "continuous mode" advances.
    _handler.onRequestNext = _playNextInPlaylist;
    await _handler.play();
  }

  Future<void> _playNextInPlaylist() async {
    if (_currentIndex + 1 < _playlist.length) {
      await playEntry(_playlist[_currentIndex + 1], playlist: _playlist, index: _currentIndex + 1);
    } else {
      _status = TtsPlaybackStatus.completed;
      notifyListeners();
    }
  }

  Future<void> pause() => _handler.pause();

  Future<void> resume() => _handler.play();

  Future<void> stop() => _handler.stop();

  Future<void> setSpeed(double rate) async {
    _speechRate = rate;
    await _handler.setSpeechRate(rate);
    notifyListeners();
  }

  void setRepeatMode(RepeatMode mode) {
    _repeatMode = mode;
    _handler.repeatMode = mode;
    notifyListeners();
  }

  void _onPlaybackStateChanged(PlaybackState state) {
    // The handler is shared with QuranAudioController — ignore state changes
    // that belong to the Qur'an audio engine, not this TTS one.
    if (_handler.activeEngine == AudioEngineKind.audio) return;
    if (state.processingState == AudioProcessingState.completed) {
      _status = TtsPlaybackStatus.completed;
    } else if (state.playing) {
      _status = TtsPlaybackStatus.playing;
    } else if (state.processingState == AudioProcessingState.idle) {
      _status = TtsPlaybackStatus.idle;
    } else {
      _status = TtsPlaybackStatus.paused;
    }
    notifyListeners();
  }
}
