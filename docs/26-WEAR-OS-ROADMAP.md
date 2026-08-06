# Wear OS Companion App — Architecture & Roadmap

## Why this is a document, not a build

Flutter has no official Wear OS support. A native Wear OS app is a
**second, separate application target** -- a standalone Kotlin + Jetpack
Wear Compose module with its own Gradle build, its own APK, and its own
install/update lifecycle on the Play Store, not a screen or a build flavor
inside the existing `flutter_app/` project. It optionally exchanges data
with a paired phone app over Android's **Wearable Data Layer API**, but
does not share Dart/Flutter code with this repository at all.

Phase 5 Part 2's own directive explicitly anticipates this: "If a full
Wear OS application is outside the current project scope, prepare the
architecture and roadmap first." That is what this document does. No
Wear OS code exists yet.

## Scope: four features, deliberately small

The directive names four planned features for a first Wear OS release --
this roadmap does not expand that scope:

1. **Tasbeeh** — a tap-to-count dhikr counter on the watch face/app,
   mirroring the phone app's core counter.
2. **Prayer alerts** — a watch notification/vibration when a prayer time
   arrives (consuming the phone's calculated times, not recalculating
   independently on-watch).
3. **Qiblah** — a simplified compass view using the watch's own
   magnetometer + the phone's last-known location.
4. **Quick adhkar** — a short list of the most-used adhkar (likely the
   already-designated "Featured Worship" set) for a glanceable read
   without unlocking the phone.

Everything else in the phone app (full Qur'an reading, Khatm tracking,
Tahajjud Mode, Masjid Mode, etc.) is deliberately **out of scope** for a
watch form factor -- these are reading/study features that need a phone
or tablet screen, not a 1-2 inch display.

## Proposed architecture

```
shroyalschools/
├── flutter_app/          (existing — phone app, unchanged)
└── wear_app/              (new — separate Android Gradle project)
    ├── app/                Kotlin + Jetpack Compose for Wear OS
    │   ├── ui/             Tasbeeh, Qiblah, Adhkar, Prayer-alert screens
    │   ├── data/            Local Room DB (own tiny counter/adhkar cache)
    │   └── sync/             Wearable Data Layer client
    └── build.gradle.kts
```

- **Phone → watch data flow**: the phone app (already a Flutter/Android
  app) would add a small native Kotlin bridge that publishes prayer
  times, the last-known Qiblah bearing, and the Featured Worship adhkar
  list to the **Wearable Data Layer** (`DataClient`/`MessageClient` from
  `com.google.android.gms:play-services-wearable`) whenever they change.
  This requires a native Android platform channel addition to the
  existing Flutter app (small, additive, does not touch existing Dart
  code) plus the new watch-side module to receive it.
- **Watch → phone data flow**: Tasbeeh counts logged on the watch sync
  back to the phone's existing `CounterRepository` (sqflite) the same
  way, so a count made on the watch shows up in the phone's statistics.
- **Offline-first stays true on the watch too**: once synced, prayer
  times/adhkar/Qiblah bearing are cached locally on the watch (a small
  Room database or even SharedPreferences-equivalent
  `DataStore`), so the watch works without the phone nearby for the rest
  of the day -- consistent with this app's offline-first design
  throughout.
- **No new licensing/content risk**: every data type crossing to the
  watch (prayer times, Qiblah bearing, the already-shipped adhkar text)
  is already computed/verified on the phone; the watch only displays it,
  so this introduces no new sourcing questions beyond what's already
  resolved for the phone app.

## Why this needs a dedicated scoping pass before implementation

- **New toolchain**: Kotlin + Jetpack Compose for Wear OS is a different
  skill/tooling surface from this Flutter codebase; realistically staffed
  as separate work, not an incremental Dart change.
- **New Play Store listing**: Wear OS apps are typically published as a
  second APK/AAB under the same Play Store listing (multi-APK) or as a
  standalone listing -- a store-publishing decision the owner needs to
  make, not an engineering default.
- **Device testing gap**: this sandbox has no physical or emulated Wear
  OS device available, the same constraint already disclosed for phone
  sensor/TTS testing (see task #62) -- Wear OS work would need real
  device verification before release, more so than the phone app since
  watch UI (tiny screen, rotary input, ambient mode) has failure modes a
  phone-sized emulator can't surface.

## Recommendation

Treat this as its own follow-up project once the phone app's remaining
Phase 5 Part 2 scope is settled, starting with Tasbeeh (the simplest,
most self-contained of the four) and the Wearable Data Layer bridge as
the first milestone, before adding Prayer alerts, Qiblah, and Quick
adhkar.
