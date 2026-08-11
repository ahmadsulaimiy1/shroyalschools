# Qur'an Audio Platform (Phase 5 Part 4, Priority 3)

Status of the "complete Qur'an audio experience" directive: what was already
built in earlier phases, what was added this pass, and a documented decision
on Android Auto.

## Already in place before this pass

- **Verse-by-verse, Surah, and Juz playback** — `QuranAudioController.playVerse()`
  takes an optional `playlist`/`index`; the reader screen's "Play Surah/Juz"
  action passes the full verse list for the open surah or juz range.
- **Memorisation Mode** — repeats each verse a configurable number of times
  before advancing, handled in `QuranAudioController` independently of the
  shared handler's own repeat modes.
- **Background playback, lock-screen controls, Bluetooth headset controls** —
  all three come from `audio_service`'s `BaseAudioHandler` /
  `AudioService.AudioService` foreground service, already wired for Adhkar
  TTS and shared with Qur'an audio (`AdhkarAudioHandler`). Android's
  MediaSession is what a Bluetooth headset's play/pause/next buttons and the
  lock screen's transport controls talk to — there is no separate
  "Bluetooth support" to add on top of a correctly implemented MediaSession,
  and this app already has one (see `AndroidManifest.xml`'s `AudioService`
  service + `MediaButtonReceiver`).
- **Resume within a session** — pausing (not stopping) preserves the exact
  playback position via `just_audio`'s `AudioPlayer`, so tapping play again
  resumes from where it left off. Resuming *across* an app restart (i.e.
  auto-resuming mid-verse after the app was fully closed) was not built —
  the existing "last read" tracking (`QuranRepository.setLastRead`) already
  takes a returning reader back to the right verse to *read*, and adding a
  second, audio-specific "resume playback" affordance on top of that was
  judged not to carry its weight for this pass.
- **Multi-reciter selection** — six verified reciters from everyayah.com
  (see `docs/18-QURAN-RECITER-VERIFICATION.md`).

## Added this pass

- **Reciter Centre** (`lib/features/quran/reciter_centre_screen.dart`,
  linked from Settings → Audio) — browse every reciter, download their full
  Qur'an recitation once for permanent offline playback, see per-reciter
  progress and storage size, pause and resume a download, and delete a
  downloaded pack. Downloads are never bundled in the APK: they're fetched
  on demand from the same verified everyayah.com CDN the app already streams
  from, via a new pure-Dart `http` dependency (no native Android code, so no
  Gradle/manifest risk).
  - Downloaded files live in a directory separate from the existing lazy
    per-play cache (`quran_audio_downloads/<reciter>/` vs
    `quran_audio_cache/`), and `QuranAudioService.audioSourceFor()` now
    checks the downloaded directory first. A verse a user deliberately
    downloaded is never silently re-fetched or treated as merely cached.
  - "Pause" stops issuing new download requests after the in-flight batch
    finishes; "resume" is just calling download again, since already-present
    files are skipped — no separate resume codepath to get wrong.
- **Repeat Range** — `QuranAudioController.loopPlaylist` lets any playlist
  loop back to its start instead of stopping when it reaches the end. The
  reader's playback-options menu exposes this as "Repeat Range" with a
  from/to ayah picker, for looping (say) one page while memorising.
- **Repeat one verse** — long-pressing a verse's play button repeats just
  that verse, as a one-gesture alternative to opening the Repeat Range sheet
  for a single ayah.

## Android Auto — researched, not implemented

Android Auto surfaces a `MediaBrowserService`'s browsable tree (`onGetRoot`/
`onLoadChildren`) inside its own car-safe UI; `audio_service`'s
`BaseAudioHandler` already implements the underlying `MediaBrowserService`
contract (the same one this app declares in `AndroidManifest.xml` for the
existing lock-screen/notification session), so the plumbing is not foreign
to this codebase.

Decision: **not implemented this pass**, for two reasons that are about
correctness, not effort:

1. Android Auto requires every browsable node the car surfaces to resolve to
   something drivable-and-safe — for a Qur'an app that means a curated
   browse tree (reciters → surahs, or continue-last-read), not the
   verse-by-verse/range-repeat/memorisation controls built above, none of
   which make sense as a glanceable in-car interaction. Exposing the full
   reader's audio surface to Android Auto as-is would be the wrong design,
   not a smaller version of the right one.
2. Google's Android Auto approval process reviews the *actual* browse tree
   and driving-safety behaviour on a real head unit or the Desktop Head Unit
   emulator — neither exists in this sandbox, so anything shipped here would
   be unverified against the one thing Android Auto review actually checks.

If Android Auto support is wanted for a future release, the right-sized
version is a minimal browse tree (reciters at the root, surahs one level
down, tapping a surah starts continuous playback) built and tested against
the Desktop Head Unit before submission — tracked as a v1.1+ candidate
rather than folded into this Gold Master pass.

## Ahmad Sulaimiy reciter pack — awaiting owner input

Per the standing directive, no reciter pack is added without the rights
holder's recordings and explicit confirmation of distribution rights. This
has not yet been requested of the owner in this session; the six reciters
in the Reciter Centre remain everyayah.com's independently verifiable
public catalogue only.
