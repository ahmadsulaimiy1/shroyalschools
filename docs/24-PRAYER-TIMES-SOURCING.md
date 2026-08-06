# Prayer & Solar Times — Sourcing & Verification

## Library

Prayer-time calculation uses **`adhan_dart`** (`pub.dev/packages/adhan_dart`,
MIT licensed), a Dart port of the widely-used open-source
[batoulapps/Adhan](https://github.com/batoulapps/Adhan) library family
(the same calculation engine behind Adhan JS/Swift/Java/Kotlin, used across
many published prayer-time apps). All astronomical formulas are drawn from
Jean Meeus's *Astronomical Algorithms*, the reference text recommended by
the U.S. Naval Observatory's Astronomical Applications Department.

This was chosen over hand-rolling the astronomical calculations (feasible
but error-prone and hard to independently verify against known-correct
output) and over calling a prayer-times web API (would break offline
operation, the app's core design constraint). `adhan_dart` has **no
runtime dependencies** and does pure on-device computation from
coordinates + date, so prayer times are available offline the moment a
location fix is known -- consistent with every other offline-first part
of this app.

## What's implemented

- `core/services/prayer_times_service.dart`: thin wrapper computing the
  five daily prayers + sunrise for a given date/coordinates.
- `core/services/prayer_settings_controller.dart`: persists the user's
  chosen calculation method, Asr madhab, per-prayer manual minute
  offsets, and last-known location fix (SharedPreferences).
- `features/prayer/prayer_times_screen.dart`: today's five prayers +
  sunrise, a live countdown to the next prayer, calculation-method picker
  (12 commonly recognised regional conventions), Asr madhab picker
  (Hanafi vs Shafi'i/Maliki/Hanbali -- the two Asr shadow-length
  conventions Islamic jurisprudence actually differs on), and a
  long-press-to-adjust manual minute offset per prayer (for matching a
  specific local masjid's announced times, a real-world need since
  calculated times can differ by a minute or two from a masjid's own
  practice).
- Location is resolved once via the same `geolocator` permission flow
  already used for the Qiblah Compass (reusing already-granted
  permissions/UI patterns), then persisted -- so a location fix survives
  app restarts without needing GPS every time. A manual refresh action is
  available in the app bar.

## Not yet built (tracked separately)

Adhan notifications/alarms, quiet hours, and prayer-tracking (marking a
prayer performed) are tracked as their own tasks (#69/#70/#78) --
notifications need Android's separate exact-alarm/notification permission
model handled deliberately, not bundled into this first pass. This phase
delivers accurate, configurable, offline prayer *times* first; alerting
on them is the next layer.
