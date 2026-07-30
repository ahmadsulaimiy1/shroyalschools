# Misbaha — Android App Scaffold

Kotlin + Jetpack Compose implementation of the architecture described in
[`/docs/04-ANDROID-ARCHITECTURE.md`](../docs/04-ANDROID-ARCHITECTURE.md).

## What's implemented in this scaffold

- Gradle project structure (Android Gradle Plugin 8.5.2, Kotlin 1.9.24, KSP, Hilt)
- Luxury design tokens (color/type/shape) matching
  [`/docs/03-BRAND-IDENTITY.md`](../docs/03-BRAND-IDENTITY.md) §3–4, with a light theme and a
  "Night Dhikr" dark theme
- Full bilingual Arabic/English resources (`values/` + `values-ar/`) with RTL enabled
  (`android:supportsRtl="true"`) — Arabic is not a translated afterthought
- Room offline-first local database (`dhikr_definitions`, `counter_sessions`, `dhikr_events`)
  matching [`/docs/05-DATABASE-SCHEMA.md`](../docs/05-DATABASE-SCHEMA.md) §2, with an append-only
  event ledger for the counting engine
- The core **Tasbeeh Counter** screen end-to-end: `BeadRingCounter` composable (radial progress,
  spring animation, haptic feedback), `CounterViewModel` (unidirectional data flow), and
  `CounterRepository` (offline-first repository pattern) — wired together via Hilt

## What's intentionally not in this scaffold yet

This is the seed implementation the [Five-Year Roadmap](../docs/11-FIVE-YEAR-ROADMAP.md) builds
out from, not a finished production app. Not yet implemented: bottom navigation across all five
tabs, the content-sync API client, WorkManager background sync, the Library/Journal/Circles
features, authentication, and the admin/institutional surfaces (those are separate web
deliverables per [`/docs/07-ADMIN-DASHBOARD.md`](../docs/07-ADMIN-DASHBOARD.md)).

## Building

This scaffold was authored in an environment without the Android SDK/Gradle wrapper installed, so
it has **not** been compiled in this session. To build:

```bash
cd android
# Generate the Gradle wrapper once (requires a local Gradle install or Android Studio):
gradle wrapper --gradle-version 8.7
./gradlew assembleDebug
```

Open the `android/` directory directly in Android Studio (Koala+) for the smoothest first run —
it will fetch the AGP/Kotlin/KSP versions pinned in `build.gradle.kts` automatically.
