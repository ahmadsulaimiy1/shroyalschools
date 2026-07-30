# Phase 4 — Royal Mushaf & Intelligent Worship Platform: Progress Report

## 1. Scope decisions (confirmed with the product owner)

The full Phase 4 directive spans 15 sections plus a bonus feature -- several
of which are either separate builds in their own right or need a decision
only the owner can make. Before starting, three forks were confirmed:

1. **Madinah Mushaf page-accuracy**: research feasibility first, rather than
   committing straight to a full page-accurate rebuild. See §2 below.
2. **User Recitation Upload** (directive explicitly said to ask): deferred
   until the owner has the actual audio files ready to provide.
3. **Wear OS companion app** and **AI Worship Assistant**: both scoped in,
   but both are genuinely separate builds from the phone app (see §7).

## 2. Madinah Mushaf page-accuracy — feasibility: CONFIRMED, not yet imported

A real, standard King Fahd Complex Madinah Mushaf page/line-layout dataset
exists: **QUL (Quranic Universal Library)**, built by Tarteel, Inc. (the
company behind the Tarteel Qur'an app), publishes the exact 604-page,
15-line-per-page layout for both the 1405H and 1421H King Fahd Complex
print editions, specifically for third-party developers to build Mushaf
UIs from. A working GitHub mirror of this data
(`zonetecde/mushaf-layout`) was fetched and spot-checked directly: page 1's
JSON matches the real printed Mushaf's Al-Fatiha layout exactly (surah
header, basmala, 7 verses distributed across 8 lines).

Critically, each line/word carries **plain Unicode Arabic text** (`word`/
`text` fields) alongside optional QPC glyph-font codepoints (`qpcV1`/
`qpcV2`). This means genuine King Fahd Mushaf line-breaks are achievable
using the **existing AmiriQuran font already bundled in this app** --
no need to embed the QCF glyph fonts (which are typically large, often the
real reason "Mushaf mode" implementations bloat their app size). This
elegantly avoids trading APK size (this session's `docs/17` fix) against
Mushaf accuracy.

**Not yet imported**: QUL's own terms-of-use page (`qul.tarteel.ai`) is
behind bot-detection in this sandbox and could not be read to confirm the
data's redistribution terms. Rather than assume permissive terms from an
unofficial GitHub mirror lacking its own LICENSE file, this is tracked as
task #63 -- to be resolved from an environment with normal browser access
before importing all 604 pages and rebuilding the Mushaf renderer around
them.

## 3. Typography fixes — shipped

An audit of every Arabic-rendering code path found and fixed two real
defects (see `docs/20` for full detail):

- **`letterSpacing` on Arabic text**: removed everywhere. Non-zero
  letter-spacing inserts a gap after every shaped glyph cluster regardless
  of script, which visually breaks cursive letter-joining in Arabic --
  this is the mechanical cause of "detached letter" appearance.
- **`TextAlign.justify` on the Mushaf flow view**: changed to right-align.
  Flutter's justify only stretches inter-word spacing; a real Mushaf
  justifies via kashida/tatweel elongation, which requires the page-layout
  glyph data from §2 above. Word-spacing justification on cursive Arabic
  reads as unnaturally gappy, so right-alignment is the honest choice until
  that data is in.

No visual defect could be *observed* (no device/emulator in this sandbox)
-- this was a code-level audit for known anti-patterns, not a rendered
screenshot comparison.

## 4. Royal Mushaf Mode — shipped

The existing Madani Mushaf continuous-flow view now has:

- A restrained double gold border framing the whole reading surface,
  echoing a printed Mushaf page's ornamental border.
- A double-ring ayah-end marker (rosette) instead of a single ring.
- A bordered surah-header banner with a small diamond-and-dots flourish
  above and below the surah name -- simple geometric shapes, no image
  assets, deliberately avoiding "excessive decoration" per the directive's
  own instruction to aim for dignity over ornament.

## 5. Audio platform completions — shipped

- **Minshawi** added as a 6th reciter (`Minshawy_Murattal_128kbps`) --
  the strongest-evidence reciter verification yet, since a web search
  surfaced the exact live per-ayah URL directly (see `docs/18` update).
- **Play Surah/Juz**: a new "Playback options" menu in the reader toolbar
  starts continuous playback through the entire currently-open verse list
  (surah or juz), reusing the existing continuous-repeat-mode playlist
  logic that was already built for per-verse "play next."
- **Memorisation Mode**: repeats each verse a configurable number of times
  (default 3) before advancing to the next, implemented entirely in
  `QuranAudioController` (the shared audio handler is left untouched during
  memorisation so there's no race with its own built-in repeat-one/
  continuous timing).
- Verse-by-verse playback, repeat mode, speed adjustment, background
  playback, and lock-screen controls were already shipped in earlier
  phases (`docs/15`, Phase 3B) and needed no new work.

## 6. Masjid Mode — shipped

A calm, full-screen worship view (navy/gold, no menus) reachable from the
Home screen. Sets a new `SettingsController.masjidMode` flag for the
duration -- deliberately session-only (not persisted across app restarts,
since it represents "praying right now," not a durable preference) and
exposed as a hook point for the not-yet-built notification system (task
#70) to check before showing anything non-essential. "Finished Praying"
leads straight into the Adhkar library's existing `prayer` category (the
after-Salah adhkar already transcribed and shipped in Phase 2/3A) --
no new content needed.

## 7. What's next, and two constraints flagged before building them

Tracked as tasks #68-72, roughly in priority order:

- **Smart Salah Platform** (prayer times, Adhan notifications, missed-
  prayer tracking, statistics) and **Tahajjud alarm system** and
  **advanced notification system**: all standard, buildable features
  using well-established Flutter packages (prayer-time calculation
  libraries, `flutter_local_notifications` or similar for scheduling) --
  no blocking unknowns, just genuine build effort.
- **Wear OS companion app**: Flutter has no official Wear OS support.
  A real Wear OS app is built natively (Kotlin + Wear Compose) as its own
  Gradle module, optionally exchanging data with the phone app via the
  Wearable Data Layer. This is a second, separate app target, not a new
  screen inside the existing Flutter project -- flagged now so this isn't
  a surprise later, with a dedicated scoping pass still to come.
- **AI Worship Assistant**: an LLM-backed assistant cannot safely embed a
  raw API key inside a shipped APK (secrets are trivially extractable from
  any distributed Android app) -- it needs a backend proxy service, which
  is new infrastructure (hosting, cost model) beyond the Flutter app
  itself. This needs an explicit decision from the owner on backend
  approach before any implementation starts.
