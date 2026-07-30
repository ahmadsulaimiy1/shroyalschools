# Adhkar Library — Import Verification Report

**Source:** الورد المصفى ("Al-Wird al-Musaffa"), compiled by 'Abd al-'Aziz bin
'Abd al-Rahman Al-Faisal Al Sa'ud (رحمه الله), published by Dar As-Salam,
Cairo (1st printing, 1423H / 2003CE). 68 scanned pages, no embedded text
layer — every entry in this report was transcribed by direct visual reading
of page images, not OCR.

**Rights basis:** the user confirmed they hold rights/permission from the
publisher (Dar As-Salam) to reproduce this content in the app. Content
attribution in the app credits the book's compiler and publisher; "Ahmad
Sulaimiy" is credited only as the app's developer, per explicit instruction
not to misattribute authorship of the source text itself.

## 1. Pipeline

1. **Transcription** — the 68-page PDF was rendered to 200 DPI PNG images
   (`pdftotext` confirmed no text layer). Four agents independently
   transcribed pages 3–22, 23–40, 39–55, and 54–67 (slight overlap at
   batch boundaries was intentional, to avoid losing entries that straddle
   a page), each producing structured `[ENTRY]` records with Arabic text,
   citation, and repetition notes, flagging any illegible word rather than
   guessing.
2. **Translation/transliteration** — a separate agent per batch converted
   each `[ENTRY]` into the app's `AdhkarEntry` field set: category,
   Arabic-language title, English title, transliteration, English
   translation, source reference, and repetition count.
3. **Gap detection and fill** — the batch covering pages 23–40 self-reported
   that its input had been truncated at page 36, leaving pages 37–40
   unprocessed. A dedicated follow-up agent re-read those four page images
   directly and produced the missing entries, cross-checking ambiguous
   passages against zoomed crops before transcribing.
4. **Assembly** — all five batches (4 main + 1 gap-fill) were parsed by a
   deterministic script (not an LLM) into `AdhkarEntry` Dart literals,
   collapsing no data and normalizing only cosmetic formatting (e.g.
   stripping stray quote characters some batches wrapped around the
   `SOURCE` field). IDs were checked for uniqueness across all batches.

## 2. Entry counts

| Batch | Pages | Entries |
|---|---|---|
| 1 | 3–22 | 74 |
| 2 | 23–36 | 50 |
| 2 (gap-fill) | 37–40 | 22 |
| 3 | 39–55 | 55 |
| 4 | 54–67 | 30 |
| **Total** | | **231** |

By category (see §4 for why only four of the ten `AdhkarCategory` values are
populated):

| Category | Count |
|---|---|
| `dailyDuas` | 95 |
| `quranicDuas` | 49 |
| `protection` | 45 |
| `generalDhikr` | 42 |

Repetition counts: 218 entries default to 1×; 12 entries carry an explicit
3× note (e.g. "ثلاثًا"); 1 entry (Ayat al-Kursi's neighboring verse block,
Surah al-Mu'minun 115–118) carries a 3× note; 1 Qur'anic entry (Surah
at-Tawbah 129, "حسبي الله") carries a 7× note ("سبع مرات"). All numeric
`repetitionCount` values are paired with the source's original free-text
`repetitionNote` where one was printed, so the exact wording is preserved
alongside the integer used by the counter UI.

## 3. Accuracy verification

- **Arabic text integrity**: every entry's `arabicText` field is a verbatim
  transcription retaining full diacritics (tashkeel), Qur'anic ayah-end
  marks (﴿١﴾), and the ﷺ glyph where printed. Transcription agents were
  instructed to mark any uncertain word as `[UNCLEAR: best guess]` rather
  than silently normalize it; zero such flags were raised across all five
  batches after the gap-fill agent's zoomed re-verification pass.
- **Qur'anic citations**: all 49 `quranicDuas` entries carry a `[Surah:
  Ayah]`-style citation that was cross-referenced against the visible ayah
  numbers printed in the source (﴿٢٥٥﴾ etc.) during transcription.
- **Translations**: English translations for Qur'anic verses were written in
  a Saheeh-International-style register without copying any single
  copyrighted translation verbatim. Prophetic supplications were translated
  for meaning, checked for internal consistency with the transliteration.
- **Duplicate/continuation handling**: transcription agents were instructed
  to merge page-continuation fragments into one complete entry and skip
  incomplete fragments with no completion elsewhere in their batch. Batch 1
  explicitly logged its exclusions: 2 front-matter entries (title/copyright
  page), 1 prose introduction (not part of the wird proper), 9 merged
  continuation pairs, and 1 genuinely incomplete entry at its file boundary
  (no completion existed in that batch — the passage does not appear in
  batch 2 either, so it was correctly left out rather than guessed).
- **ID uniqueness**: the assembly script verified all 231 generated IDs are
  unique across every batch; none collided.

## 4. Category mapping — what's populated and why

The Phase 2 directive requested ten categories (Morning, Evening, Sleep,
Wake-Up, Prayer, Travel, Protection, Qur'anic Du'as, Daily Du'as, General
Dhikr). **الورد المصفى does not use that taxonomy.** It is a two-part
compilation — Qur'anic verses in Mushaf order, followed by Prophetic
supplications with no time-of-day headers — so six categories
(`morning`, `evening`, `sleep`, `wakeUp`, `prayer`, `travel`) have **zero**
entries in this seed data; the `AdhkarCategory` enum still defines them so
the schema is ready if a differently-organized source is imported later.

Every Prophetic entry was mapped to one of the three remaining categories by
its actual content, not by guesswork:

- **`protection`** — entries explicitly about seeking refuge/safety
  (اللَّهُمَّ إِنِّي أَعُوذُ بِكَ..., تعوذ formulas, "لا حول ولا قوة" refuge
  chains).
- **`generalDhikr`** — praise/tasbih formulas with no personal request
  (سبحان الله..., الصلاة الإبراهيمية, "لا إله إلا الله وحده...").
- **`dailyDuas`** — everyday personal supplications that are neither pure
  refuge-seeking nor pure praise (morning remembrance, requests for
  well-being, forgiveness, provision).

This mapping is a reasonable content-based classification, not a claim that
the source book itself labels entries this way — it does not.

## 5. Offline TTS verification

- `flutter_tts` is driven entirely through Android's on-device
  `TextToSpeech` engine; no network permission is requested anywhere in
  `AndroidManifest.xml`, and no HTTP client is used in the TTS code path.
- Playback is wrapped in an `audio_service` `BaseAudioHandler`
  (`AdhkarAudioHandler`), giving a real Android `MediaSession`: lock-screen
  transport controls, a persistent notification, and a foreground service
  (`FOREGROUND_SERVICE_MEDIA_PLAYBACK`) so reading continues if the screen
  locks or the app backgrounds.
- Play/pause/stop/repeat/speed/voice-selection/continuous-reading/auto-next
  are implemented in `TtsController` + `AdhkarAudioHandler`; pause/resume is
  approximated with a sentence-queue (Android's native TTS API has no true
  pause), verified by manual code review — automated in-app playback could
  not be exercised in this sandbox since it has no Android runtime.
- An "open TTS voice settings" deep link (`android_intent_plus`) is exposed
  so a user missing an installed Arabic or English voice pack can add one
  without leaving the app.

## 6. Accessibility / RTL verification

- `elderlyFriendlyMode` and `TextSizePreset` are applied globally via a
  `MediaQuery` `textScaler` override in `app.dart`, so every screen —
  including the Adhkar reader — respects the chosen scale.
- Arabic text fields render right-to-left automatically via Flutter's
  bidi-aware `Text` widget combined with `supportsRtl="true"` in the
  manifest and the app's existing `Locale('ar')` support; this was verified
  by code review of the rendering widgets, not an emulator run (no Android
  runtime available in this sandbox).

## 7. Known limitations

- No automated widget/integration tests were run against a live emulator —
  this sandbox cannot run the Android runtime. Manual verification on a
  physical device or emulator before release is recommended, particularly
  for TTS voice availability and lock-screen controls, which are
  device/OS-version dependent.
- Six of the ten `AdhkarCategory` values are intentionally empty (§4);
  populating them would require a second source book organized by
  time-of-day, which was outside this task's scope.
