import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import '../../database/quran_repository.dart';
import 'quran_audio_service.dart';

/// Drives the Reciter Centre: downloading a reciter's entire Qur'an
/// recitation (all [totalQuranVerseCount] verses) for permanent offline
/// playback, with per-reciter progress, pause, resume, and delete.
///
/// Downloads run in small concurrent batches (a handful of requests at a
/// time) rather than one-by-one, so a full pack finishes in a reasonable
/// time without hammering everyayah.com's public server with thousands of
/// simultaneous connections. "Pause" stops issuing new batches after the
/// current one finishes; "resume" is simply calling [download] again --
/// verses already on disk are skipped by [QuranAudioService.downloadVerse],
/// so progress naturally continues from wherever it left off.
class ReciterDownloadController extends ChangeNotifier {
  ReciterDownloadController(this._service, this._repository);

  static const _batchSize = 4;

  final QuranAudioService _service;
  final QuranRepository _repository;
  final http.Client _client = http.Client();

  final Map<QuranReciter, int> _downloadedCounts = {};
  final Set<QuranReciter> _activeDownloads = {};
  final Set<QuranReciter> _cancelFlags = {};

  int downloadedCount(QuranReciter reciter) => _downloadedCounts[reciter] ?? 0;
  bool isDownloading(QuranReciter reciter) => _activeDownloads.contains(reciter);
  bool isComplete(QuranReciter reciter) => downloadedCount(reciter) >= totalQuranVerseCount;

  Future<void> refreshCount(QuranReciter reciter) async {
    _downloadedCounts[reciter] = await _service.downloadedVerseCount(reciter);
    notifyListeners();
  }

  Future<void> refreshAllCounts() async {
    for (final reciter in QuranReciter.values) {
      _downloadedCounts[reciter] = await _service.downloadedVerseCount(reciter);
    }
    notifyListeners();
  }

  Future<int> downloadedBytes(QuranReciter reciter) => _service.downloadedBytesFor(reciter);

  Future<void> download(QuranReciter reciter) async {
    if (_activeDownloads.contains(reciter)) return;
    _activeDownloads.add(reciter);
    _cancelFlags.remove(reciter);
    notifyListeners();

    try {
      final chapters = await _repository.chapters();
      final verses = <({int surah, int ayah})>[];
      for (final chapter in chapters) {
        for (final verse in await _repository.versesForChapter(chapter.number)) {
          verses.add((surah: verse.surah, ayah: verse.ayah));
        }
      }

      _downloadedCounts[reciter] = await _service.downloadedVerseCount(reciter);
      notifyListeners();

      for (var i = 0; i < verses.length; i += _batchSize) {
        if (_cancelFlags.contains(reciter)) break;
        final batch = verses.skip(i).take(_batchSize).toList();
        await Future.wait(batch.map((v) async {
          try {
            await _service.downloadVerse(v.surah, v.ayah, reciter, client: _client);
          } catch (_) {
            // One verse failing (network hiccup) shouldn't abort the whole
            // pack -- it stays missing and is retried the next time the
            // user resumes this reciter's download.
          }
        }));
        final present = await Future.wait(batch.map((v) => _service.isDownloaded(v.surah, v.ayah, reciter)));
        _downloadedCounts[reciter] = (_downloadedCounts[reciter] ?? 0) + present.where((ok) => ok).length;
        notifyListeners();
      }
    } finally {
      _activeDownloads.remove(reciter);
      _cancelFlags.remove(reciter);
      notifyListeners();
    }
  }

  void pause(QuranReciter reciter) {
    _cancelFlags.add(reciter);
  }

  Future<void> delete(QuranReciter reciter) async {
    await _service.deleteDownloadsFor(reciter);
    _downloadedCounts[reciter] = 0;
    notifyListeners();
  }

  @override
  void dispose() {
    _client.close();
    super.dispose();
  }
}
