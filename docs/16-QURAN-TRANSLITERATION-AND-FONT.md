# Qur'an Transliteration & Typography — Source Verification

## 1. Why this exists

Phase 3C (the "Premium Qur'an Experience" directive) required (a) a
professional Qur'anic Arabic typeface so the Mushaf reads like a real Mushaf,
and (b) Reading Mode C (Arabic + Translation + Transliteration). Both are
sourced/verified rather than invented, following the same discipline used for
the Qur'an text/translation/chapter/juz data (see `docs/15`).

## 2. Typeface: Amiri Quran

- **Source**: Google Fonts' GitHub mirror,
  `github.com/google/fonts/tree/main/ofl/amiriquran` (upstream project:
  `aliftype/amiri`).
- **License**: SIL Open Font License 1.1 (`assets/fonts/AmiriQuran-OFL.txt`) —
  free for commercial and non-commercial embedding.
- **Why this font**: Amiri Quran is a Naskh-style Qur'anic typeface derived
  from the "Amiri" typeface family, purpose-built for Qur'anic typesetting
  with correct tashkeel placement, ligatures, and Uthmani-script support — the
  same design lineage used by several published Qur'an apps and websites.
- **Integration**: registered in `pubspec.yaml` under `flutter: fonts:` as
  family `AmiriQuran`, applied to the Arabic verse `Text` in
  `QuranVerseCard` with `height: 2.3` line spacing and a modest size bump
  (1.05×) over the surrounding UI text, addressing the directive's specific
  complaint about cramped spacing.

## 3. Transliteration: Tanzil.net "quran-la" edition

- **Source**: `fawazahmed0/quran-api` (GitHub), edition `ara-quran-la`,
  fetched from
  `raw.githubusercontent.com/fawazahmed0/quran-api/1/editions/ara-quran-la.json`.
- **Upstream origin**: the aggregator's own edition metadata lists this
  edition's `source` as `http://tanzil.net` — i.e. it is Tanzil.net's own
  transliteration dataset, the same organisation that is the ultimate source
  of the Uthmani Arabic text used throughout this app (see `docs/15`), not a
  third-party or community-contributed romanization.
- **Verification performed**: confirmed exactly 6,236 entries, one per
  `(chapter, verse)` pair, matching 1:1 against the existing 6,236-verse
  Arabic/English dataset with zero missing keys. Spot-checked Ayat al-Kursi
  (2:255) and Surah al-Fatiha's opening verse — both read as standard
  Tanzil-style transliteration.
- **Known convention note**: this transliteration uses Tanzil's own plain
  Latin-alphabet convention (e.g. doubled vowels for length, `AA` for
  `ع`-adjacent sounds) rather than IJMES-style academic diacritics (macrons,
  underdots). This is disclosed here rather than silently accepted as
  "premium-equivalent" to the more heavily diacritised transliteration style
  used for the Adhkar library — no better-verified alternative transliteration
  edition of the full Qur'an was found through this aggregator or its listed
  sources, and Tanzil.net itself is unreachable from this build sandbox to
  cross-check directly (see `docs/15` §2 on the sandbox's network policy).

### 3.1 Known upstream anomaly (disclosed, not silently "fixed")

A scripted scan of all 6,236 transliteration entries for malformed word
endings found exactly one anomaly: surah An-Nas's closing verse (114:6) is
rendered `"Mina aljinnati wa alnnasm"`, where the final word breaks the
pattern used by the identical word (`alnnasi`) four lines earlier in the same
surah (114:1, 114:2, 114:3, 114:5). This is present verbatim in the upstream
Tanzil-sourced file — it was not introduced by this app's merge step. Rather
than silently "correct" a single character from memory (which would
reintroduce exactly the reconstruction risk this whole sourcing discipline
exists to avoid), the data is shipped as-is and the anomaly is disclosed
here. It is the only such anomaly found across the full corpus.

## 4. Reading Modes shipped

- **Mode A — Qur'an Only**: Arabic text alone (`QuranReadingMode.arabicOnly`).
- **Mode B — Qur'an + Translation** (default): Arabic + English
  (`QuranReadingMode.arabicTranslation`).
- **Mode C — Qur'an + Translation + Transliteration**: adds the
  transliteration line above the translation
  (`QuranReadingMode.arabicTranslationTransliteration`).

The mode is persisted (SharedPreferences, `SettingsController`) and
selectable from a text-format icon in the Qur'an reader's app bar — it
applies uniformly across surah reading, juz reading, search results,
bookmarks, and favourites, since all of those routes render through the same
`QuranReaderScreen`/`QuranVerseCard`.

Modes D (+Tafsir) and E (Study Mode: word-by-word, root words, notes) remain
future-expansion items, as scoped in the original directive.

## 5. Data footprint

`assets/quran/verses.json` grew from ~2.4 MB to ~3.0 MB with the added `tl`
(transliteration) field per verse — still a single bundled JSON asset loaded
once into memory, no schema or architecture change from `docs/15`.
