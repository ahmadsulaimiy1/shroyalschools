import 'dart:io';

import 'package:just_audio/just_audio.dart';
import 'package:path_provider/path_provider.dart';

/// Resolves a Qur'an verse to a playable [AudioSource]: real Qari recitation
/// (Mishary Rashid Alafasy, 128kbps) from everyayah.com's long-standing
/// public per-ayah CDN — never synthesized TTS, see
/// docs/15-QURAN-DATA-SOURCE-VERIFICATION.md for why that distinction
/// matters for Qur'an recitation specifically.
///
/// [LockCachingAudioSource] streams from the network on first play while
/// simultaneously writing the response to [cacheFile]; every subsequent
/// play of the same verse reads straight from that local file with no
/// network request at all — this is what gives "online the first time,
/// offline after that" without any caching logic of our own to get wrong.
class QuranAudioService {
  static const _reciterFolder = 'Alafasy_128kbps';

  Future<AudioSource> audioSourceFor(int surah, int ayah) async {
    final url = Uri.parse(
      'https://everyayah.com/data/$_reciterFolder/'
      '${surah.toString().padLeft(3, '0')}${ayah.toString().padLeft(3, '0')}.mp3',
    );
    final cacheFile = await _cacheFileFor(surah, ayah);
    return LockCachingAudioSource(url, cacheFile: cacheFile);
  }

  Future<bool> isCached(int surah, int ayah) async {
    final file = await _cacheFileFor(surah, ayah);
    return file.exists();
  }

  Future<File> _cacheFileFor(int surah, int ayah) async {
    final baseDir = await getApplicationSupportDirectory();
    final cacheDir = Directory('${baseDir.path}/quran_audio_cache');
    if (!await cacheDir.exists()) {
      await cacheDir.create(recursive: true);
    }
    return File('${cacheDir.path}/${surah}_$ayah.mp3');
  }
}
