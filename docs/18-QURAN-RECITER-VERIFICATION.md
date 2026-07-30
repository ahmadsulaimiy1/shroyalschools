# Qur'an Multi-Reciter Verification

## 1. Why this exists

The Premium Qur'an Experience directive asked for Alafasy, Abdul Basit,
Maher Al-Muaiqly, Sudais, and Hudhaify as selectable reciters on
everyayah.com, with an explicit instruction to verify each has a working
folder before exposing it as a picker option -- not to guess folder names
from memory.

## 2. Why this couldn't be checked by directly browsing everyayah.com

This build sandbox's network policy returns `403`/`CONNECT tunnel failed`
for direct requests to `everyayah.com` (the same constraint already
documented in `docs/15` §2 for tanzil.net/mp3quran.net/cdn.jsdelivr.net --
only `raw.githubusercontent.com`-style GitHub hosts and web search are
reachable here). The existing Alafasy folder (`Alafasy_128kbps`) was
already shipped in Phase 3B and works on real devices; the same due
diligence was applied to the four new reciters via independent
corroboration instead of a direct browse.

## 3. Verification method and sources

- **Mishary Rashid Alafasy** -- `Alafasy_128kbps` (already shipped,
  independently re-confirmed via a Zekr Qur'an-player configuration file
  quoting the exact URL `everyayah.com/data/Alafasy_128kbps/001025.mp3`).
- **Abdul Basit** -- `Abdul_Basit_Murattal_192kbps`.
- **Maher Al-Muaiqly** -- `Maher_AlMuaiqly_64kbps`.
- **Abdurrahman As-Sudais** -- `Abdurrahmaan_As-Sudais_192kbps`.

  These three folder names were cross-checked against
  `Prince77-7/quranMCP`'s published `API.md`, a real, independently
  published production tool whose documented Qur'an-audio endpoint lists
  these exact identifiers as "Available Reciters" alongside Alafasy and
  Husary, and whose own README separately cites everyayah.com and
  `fawazahmed0/quran-api`/`fawazahmed0/hadith-api` as its data sources --
  the same two aggregators this app already uses, which is corroborating
  rather than coincidental.
- **Ali Al-Hudhaify** -- `Hudhaify_128kbps`. Confirmed via web search
  results describing everyayah.com's recitations listing page as offering
  `Hudhaify_32kbps`, `Hudhaify_64kbps`, and `Hudhaify_128kbps` folders, plus
  an Internet Archive mirror item named `quran_Hudhaify_64kbps_045`
  confirming the `Hudhaify_{bitrate}kbps` naming convention is real and
  already in third-party circulation.
- **Muhammad Siddiq Al-Minshawi** (added Phase 4) -- `Minshawy_Murattal_128kbps`.
  This one has the strongest evidence of all six: a web search directly
  surfaced the exact live URL
  `https://www.everyayah.com/data/Minshawy_Murattal_128kbps/021089.mp3`
  (surah 21, ayah 89) as a search-indexed page, not just a name mentioned
  in a third party's docs -- i.e. this specific per-ayah file's URL has
  been crawled from the live site.

All six reciters use the same per-ayah filename convention already
verified for Alafasy (`{surah:03d}{ayah:03d}.mp3`), since this is a
site-wide convention on everyayah.com, not something reciter-specific.

## 4. What remains unverified

The exact byte-for-byte existence of every one of the four new reciters'
6,236 individual per-ayah files was not (and cannot be, from this sandbox)
checked file-by-file. If any single verse file is missing for a given
reciter, playback for that specific verse would fail gracefully (the
existing `LockCachingAudioSource`/`just_audio` error handling applies) but
wouldn't crash the app. This should be spot-checked on a real device with
normal internet access before wide release, the same disclosed limitation
already noted for the original Alafasy integration in `docs/15`.

## 5. Implementation

- `QuranReciter` enum (`core/services/quran/quran_audio_service.dart`)
  carries each reciter's folder + display name.
- `QuranAudioService.audioSourceFor`/`isCached` take an optional `reciter`
  parameter (default Alafasy, preserving old call sites' behaviour).
- Cache files are now keyed per-reciter
  (`quran_audio_cache/{reciter}_{surah}_{ayah}.mp3`) so switching reciters
  never serves another Qari's cached audio for the same verse.
- `QuranAudioController` owns the selected reciter as persisted state
  (SharedPreferences, `quran_reciter` key), selectable from a
  "Reciter" icon in the reader toolbar.
