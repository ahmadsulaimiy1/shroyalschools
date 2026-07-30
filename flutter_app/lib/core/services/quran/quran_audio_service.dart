import 'dart:io';

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
  Future<AudioSource> audioSourceFor(int surah, int ayah, {QuranReciter reciter = QuranReciter.alafasy}) async {
    final url = Uri.parse(
      'https://everyayah.com/data/${reciter.folder}/'
      '${surah.toString().padLeft(3, '0')}${ayah.toString().padLeft(3, '0')}.mp3',
    );
    final cacheFile = await _cacheFileFor(surah, ayah, reciter);
    return LockCachingAudioSource(url, cacheFile: cacheFile);
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
}
