import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:just_audio/just_audio.dart';
import 'package:path_provider/path_provider.dart';

/// A selectable Qari (reciter) for Qur'an audio, each a verified folder on
/// everyayah.com's long-standing public per-ayah CDN. See
/// docs/18-QURAN-RECITER-VERIFICATION.md for how each folder name was
/// cross-checked (this sandbox's network policy blocks everyayah.com
/// directly, so folder names were verified against an independent
/// production tool's published API documentation plus web search
/// corroboration, rather than assumed from memory).
enum QuranReciter {
  alafasy('Alafasy_128kbps', 'Mishary Rashid Alafasy'),
  abdulBasit('Abdul_Basit_Murattal_192kbps', 'Abdul Basit Abdus-Samad'),
  maherAlMuaiqly('Maher_AlMuaiqly_64kbps', 'Maher Al-Muaiqly'),
  sudais('Abdurrahmaan_As-Sudais_192kbps', 'Abdurrahman As-Sudais'),
  hudhaify('Hudhaify_128kbps', 'Ali Al-Hudhaify'),
  minshawi('Minshawy_Murattal_128kbps', 'Muhammad Siddiq Al-Minshawi');

  const QuranReciter(this.folder, this.displayName);
  final String folder;
  final String displayName;
}

/// Resolves a Qur'an verse to a playable [AudioSource]: real Qari recitation
/// from everyayah.com's long-standing public per-ayah CDN -- never
/// synthesized TTS, see docs/15-QURAN-DATA-SOURCE-VERIFICATION.md for why
/// that distinction matters for Qur'an recitation specifically.
///
/// [LockCachingAudioSource] streams from the network on first play while
/// simultaneously writing the response to [cacheFile]; every subsequent
/// play of the same verse reads straight from that local file with no
/// network request at all -- this is what gives "online the first time,
/// offline after that" without any caching logic of our own to get wrong.
/// Each reciter gets its own cache file per verse so switching reciters
/// never serves another Qari's cached audio.
class QuranAudioService {
  Uri _remoteUrlFor(int surah, int ayah, QuranReciter reciter) => Uri.parse(
        'https://everyayah.com/data/${reciter.folder}/'
        '${surah.toString().padLeft(3, '0')}${ayah.toString().padLeft(3, '0')}.mp3',
      );

  /// Prefers a permanently-downloaded file (see [downloadVerse]/the Reciter
  /// Centre) over the lazy per-play cache -- a verse a user deliberately
  /// downloaded should never be re-fetched or re-cached by the lazy path.
  Future<AudioSource> audioSourceFor(int surah, int ayah, {QuranReciter reciter = QuranReciter.alafasy}) async {
    final downloaded = await _downloadedFileFor(surah, ayah, reciter);
    if (await downloaded.exists()) {
      return AudioSource.uri(Uri.file(downloaded.path));
    }
    final cacheFile = await _cacheFileFor(surah, ayah, reciter);
    return LockCachingAudioSource(_remoteUrlFor(surah, ayah, reciter), cacheFile: cacheFile);
  }

  Future<bool> isCached(int surah, int ayah, {QuranReciter reciter = QuranReciter.alafasy}) async {
    final file = await _cacheFileFor(surah, ayah, reciter);
    return file.exists();
  }

  Future<File> _cacheFileFor(int surah, int ayah, QuranReciter reciter) async {
    final baseDir = await getApplicationSupportDirectory();
    final cacheDir = Directory('${baseDir.path}/quran_audio_cache');
    if (!await cacheDir.exists()) {
      await cacheDir.create(recursive: true);
    }
    return File('${cacheDir.path}/${reciter.name}_${surah}_$ayah.mp3');
  }

  Future<Directory> _downloadDirFor(QuranReciter reciter) async {
    final baseDir = await getApplicationSupportDirectory();
    final dir = Directory('${baseDir.path}/quran_audio_downloads/${reciter.name}');
    if (!await dir.exists()) {
      await dir.create(recursive: true);
    }
    return dir;
  }

  Future<File> _downloadedFileFor(int surah, int ayah, QuranReciter reciter) async {
    final dir = await _downloadDirFor(reciter);
    return File('${dir.path}/${surah}_$ayah.mp3');
  }

  Future<bool> isDownloaded(int surah, int ayah, QuranReciter reciter) async {
    final file = await _downloadedFileFor(surah, ayah, reciter);
    return file.exists();
  }

  /// Permanently stores [surah]:[ayah]'s recitation for [reciter] -- the
  /// Reciter Centre's "download this reciter's whole Qur'an for offline use"
  /// feature, distinct from the lazy per-play cache above. A no-op if the
  /// file is already downloaded, which is what makes pausing and resuming a
  /// pack download safe: resuming is just calling this again for every verse,
  /// and already-downloaded ones are skipped.
  Future<void> downloadVerse(int surah, int ayah, QuranReciter reciter, {required http.Client client}) async {
    final file = await _downloadedFileFor(surah, ayah, reciter);
    if (await file.exists()) return;
    final response = await client.get(_remoteUrlFor(surah, ayah, reciter));
    if (response.statusCode != 200) {
      throw Exception('Failed to download ${reciter.displayName} $surah:$ayah (HTTP ${response.statusCode})');
    }
    await file.writeAsBytes(response.bodyBytes, flush: true);
  }

  Future<int> downloadedVerseCount(QuranReciter reciter) async {
    final dir = await _downloadDirFor(reciter);
    var count = 0;
    await for (final entity in dir.list()) {
      if (entity is File) count++;
    }
    return count;
  }

  Future<int> downloadedBytesFor(QuranReciter reciter) async {
    final dir = await _downloadDirFor(reciter);
    var total = 0;
    await for (final entity in dir.list()) {
      if (entity is File) total += await entity.length();
    }
    return total;
  }

  Future<void> deleteDownloadsFor(QuranReciter reciter) async {
    final dir = await _downloadDirFor(reciter);
    if (await dir.exists()) {
      await dir.delete(recursive: true);
    }
  }

  /// Total bytes of every cached recitation file across every reciter --
  /// backs the Downloads section of Settings, which shows this figure
  /// rather than a per-reciter breakdown (cache files aren't tracked with
  /// enough metadata to attribute cheaply without adding a manifest).
  Future<int> cacheSizeBytes() async {
    final baseDir = await getApplicationSupportDirectory();
    final cacheDir = Directory('${baseDir.path}/quran_audio_cache');
    if (!await cacheDir.exists()) return 0;
    var total = 0;
    await for (final entity in cacheDir.list()) {
      if (entity is File) total += await entity.length();
    }
    return total;
  }

  /// Deletes every cached recitation file. Verses already read stay in the
  /// Qur'an database (bookmarks, notes, last-read); only the downloaded
  /// audio itself is removed, and will simply re-download on next play.
  Future<void> clearCache() async {
    final baseDir = await getApplicationSupportDirectory();
    final cacheDir = Directory('${baseDir.path}/quran_audio_cache');
    if (await cacheDir.exists()) {
      await cacheDir.delete(recursive: true);
    }
  }
}
