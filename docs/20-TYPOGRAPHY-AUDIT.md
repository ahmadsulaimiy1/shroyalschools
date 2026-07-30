# Arabic Typography Audit — Phase 4

## 1. Why this exists

Phase 4's directive flagged generic Arabic-rendering defects ("detached
alif," "incorrect ligatures," "broken word shaping") as unacceptable for a
flagship Mushaf reader. This sandbox has no Android device or emulator, so
these defects cannot be visually confirmed the way a real screenshot would
allow -- this audit instead reviewed every code path that renders Arabic
text for known, verifiable anti-patterns, and fixed what it found.

## 2. Bugs found and fixed

- **`letterSpacing` applied to Arabic text** (`QuranVerseCard`'s card-view
  verse text, `MushafFlowText`'s continuous-flow verse text). Arabic is a
  cursive, joining script -- Flutter (like essentially all text-shaping
  engines) applies `letterSpacing` by inserting a fixed gap *after every
  shaped glyph cluster*, regardless of script. For a joining script this
  visually breaks the connection between adjacent letters even though the
  underlying Unicode joining behavior is untouched -- exactly the kind of
  defect described as "detached" letters. Both instances had a non-zero
  `letterSpacing` (0.3-0.5) and have been set to `0.0`. **Arabic text
  should never carry manual letter-spacing.**
- **`TextAlign.justify` on the continuous Mushaf flow**
  (`MushafFlowText`). Flutter's justify implementation stretches
  inter-word spacing only -- it has no concept of kashida/tatweel
  elongation, which is how a real printed Mushaf actually justifies
  Arabic lines (letters are visually stretched via calligraphic elongation
  glyphs, not by widening the gaps between words). Naive word-spacing
  justification on a cursive script reads as unnaturally gappy and is not
  "how a real Mushaf looks." Changed to right-alignment, which is the
  honest choice given this app doesn't yet have kashida-aware,
  page-specific glyph data (see `docs/21`'s Mushaf-layout task) -- true
  kashida justification requires exactly the King Fahd Mushaf page-layout
  dataset that task is scoped to import.

## 3. Checked and found correct (no change needed)

- **Font**: Amiri Quran is a proper OpenType font with its own GSUB/GPOS
  tables for Arabic joining and ligatures; Flutter's text layout (Skia's
  Minikin-based shaper) performs full complex-script shaping automatically
  for any font with correct joining tables. No custom shaping code is
  needed or present that could interfere with this.
- **No manual text-splitting inside a verse**: every verse's Arabic text
  is rendered as a single unbroken string within one `TextSpan`/`Text`
  widget. The only place a verse's Arabic run is adjacent to something else
  (a `WidgetSpan` ayah-end marker in `MushafFlowText`) is *between* two
  different verses -- a real, intentional visual break at an ayah boundary,
  not a mid-word split that could cause a joining defect.
- **Wasla alif (`ٱ`, U+0671)**: appears throughout the bundled Arabic text
  (e.g. "بِسْمِ ٱللَّهِ") as standard Uthmani orthography carried over
  verbatim from the Tanzil-sourced data (`docs/15`) -- this is the correct,
  intentional Qur'anic spelling convention, not a rendering defect, even
  though its raised hamza-less form can look unfamiliar to someone
  expecting a plain alif.
- **Ayah-marker numerals**: rendered with an explicit
  `textDirection: TextDirection.rtl` on their own isolated `Text` widget
  (`_AyahMarker` in `mushaf_flow_text.dart`), so Arabic-Indic digit runs
  never inherit an ambiguous bidi context from surrounding content.

## 4. What remains unverifiable from this sandbox

No visual rendering was performed (no device/emulator available in this
environment). If a specific defect was observed on a real device
(screenshot, description of what looked wrong and where), that would let a
future pass target the actual bug directly rather than auditing by code
inspection alone.
