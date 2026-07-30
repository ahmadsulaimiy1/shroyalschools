# Qur'an Data Source Verification Report

## 1. Why this exists

The Qur'an's Arabic text, translation, chapter metadata, and juz boundaries
are not something an LLM should reconstruct from memory at this scale (6,236
verses) — fidelity has to be perfect. Every dataset shipped in this app was
mechanically downloaded from an established, verifiable public source and
spot-checked against known reference verses, not retyped or paraphrased.

## 2. Sources

| Data | Source | License |
|---|---|---|
| Arabic Qur'an text (Uthmani Hafs script) | `fawazahmed0/quran-api` (GitHub), edition `ara-quranuthmanihaf` | Public aggregator of the standard Uthmani text; redistributed for app/website use |
| English translation | `fawazahmed0/quran-api`, edition `eng-mohammedmarmadu` (Muhammad Marmaduke Pickthall) | Public domain |
| Chapter metadata (Arabic name, transliteration, English meaning, revelation type, verse count) | `risan/quran-json` (GitHub), `dist/chapters/en/index.json` | MIT |
| Juz (para) boundaries | `semarketir/quranjson` (GitHub), `source/juz.json` | MIT |
| Recitation audio | everyayah.com per-ayah CDN, reciter Mishary Rashid Alafasy (`Alafasy_128kbps`) | Long-standing public Qur'an audio CDN used by numerous open-source Qur'an apps |

Tanzil.net itself (the corpus this ecosystem descends from) was unreachable
directly from this build sandbox (network policy blocks most non-GitHub
hosts here) — the GitHub-hosted mirrors above were used instead and
verified independently rather than assumed correct.

## 3. Verification performed

- **Verse count**: confirmed exactly 6,236 verses in both the Arabic and
  English datasets, and that they align key-for-key (every `(surah, ayah)`
  pair present in one is present in the other).
- **Chapter count**: confirmed exactly 114 chapters, and that
  `sum(versesCount)` across all chapters equals 6,236.
- **Juz count**: confirmed exactly 30 juz, that juz 1 starts at 1:1 and juz
  30 ends at 114:6 (the full Qur'an), and that consecutive juz boundaries
  are contiguous (no gap or overlap between the end of one juz and the
  start of the next).
- **Spot checks** against well-known verses:
  - Surah al-Fatiha 1:1 — matches the standard opening verse.
  - Ayat al-Kursi (2:255) — Arabic text matches the standard Uthmani
    rendering (wasla alifs, waqf marks); English matches Pickthall's
    well-known rendering ("Allah! There is no deity save Him...").
  - Surah an-Nas's closing verse (114:6) — matches "مِنَ الْجِنَّةِ وَالنَّاسِ" /
    "Of the jinn and of mankind".
  - Chapter metadata spot-checked for Al-Fatihah ("The Opener"), Al-Baqarah
    ("The Cow"), and An-Nas ("Mankind").
  - Juz boundaries spot-checked against the standard divisions (Juz 1 =
    Fatiha 1 – Baqarah 141; Juz 2 = Baqarah 142 – 252; Juz 3 = Baqarah 253 –
    Aal-Imran 92), which match every published Mushaf.

## 4. Why Pickthall over other translations

The aggregator used hosts 40+ English translations. Pickthall was chosen
because it is unambiguously public domain (published 1930, translator died
1936), avoiding any licensing ambiguity, while still being one of the most
respected and widely used English Qur'an translations historically. Saheeh
International (the most common modern default in Qur'an apps) was not
available through this particular aggregator and was not substituted with
an unverified alternative.

## 5. Why recitation audio is real Qari audio, not TTS

Adhkar reading in this app uses on-device text-to-speech, because reading a
translation or supplication aloud is not subject to Tajweed (the rules
governing correct Qur'anic recitation). The Qur'an is different: incorrect
application of madd, ghunnah, qalqalah, etc. is a real correctness problem,
and no synthesized TTS engine reproduces Tajweed reliably. Every legitimate
Qur'an app uses real reciter (Qari) audio for this reason, and this app does
the same — Mishary Rashid Alafasy's recitation, streamed from
everyayah.com's public per-ayah CDN on first play, then cached to local
storage (`LockCachingAudioSource`) so replay is instant and fully offline
afterward. No other feature in this app requires network access; the
Qur'an audio player is the one exception, and this is disclosed on the
About screen.

## 6. Architecture notes

- The 6,236-verse corpus is shipped as bundled JSON assets
  (`assets/quran/{chapters,verses,juz}.json`, ~2.4 MB total) loaded into
  memory once at runtime, rather than as generated Dart source or a
  pre-seeded sqflite table — this keeps the compiled binary and the app's
  diff surface reasonable for reference data that never changes at
  runtime. Only user-generated state (bookmarks, favourites, last-read
  position, reading log) lives in sqflite (`quran_bookmarks`,
  `quran_favourites`, `quran_last_read`, `quran_reads` — schema v3, see
  `core/database/database_helper.dart`).
- Search is a linear scan over the in-memory verse list (case-insensitive
  English, diacritic-insensitive Arabic) — the full dataset is a couple of
  MB, so this is effectively instant on any modern device; no FTS index
  was needed at this scale.
- Qur'an audio and Adhkar TTS share a single `audio_service` MediaSession
  handler (Android only allows one BaseAudioHandler per process) — see the
  updated doc comment in `core/services/tts/adhkar_audio_handler.dart` for
  how the two engines coexist under one set of lock-screen controls.

## 7. Known limitations

- No automated device/emulator testing was performed in this sandbox (no
  Android runtime available, as with every prior phase). The audio
  streaming/caching path in particular should be exercised on a real
  device before release.
- Transliteration and Tafsir are not included this phase (Tafsir was
  explicitly scoped as "Future Expansion" in the original directive;
  transliteration was not requested for the Qur'an specifically, unlike
  the Adhkar library).
- Word-by-word study, root-word analysis, and Tajweed color-highlighting
  remain future expansion items, as originally scoped.
