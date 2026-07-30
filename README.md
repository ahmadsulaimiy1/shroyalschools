# Misbaha — Global Islamic Luxury Tasbeeh Platform

Misbaha is a luxury Islamic Tasbeeh & Dhikr spiritual engagement platform, built cross-platform
with Flutter, with a roadmap to iOS, Web, Wear OS/watchOS, TV, and automotive surfaces.

- **[/flutter_app](flutter_app)** — **the working Flutter/Android MVP.** Complete Dart source
  (Splash, Home, Counter, Statistics, Daily Adhkar, Settings, About), offline sqflite storage,
  Arabic/English with full RTL, dark mode, tap/volume-button/haptic/sound counting. See
  [`flutter_app/BUILD.md`](flutter_app/BUILD.md) for building an APK/AAB and publishing to Google
  Play — or just push to this branch and let `.github/workflows/build-flutter-apk.yml` build a
  real installable APK for you automatically (see the repo's GitHub Releases, tag `latest-apk`).
- **[/docs](docs/00-README.md)** — the full product, design, engineering, governance, and
  go-to-market documentation set (PRD, UI/UX design system, brand identity, architecture, database
  schema, API docs, admin dashboard, monetisation, security, deployment, five-year roadmap, store
  publishing package).
- **[/android](android)** — an earlier native Kotlin/Jetpack Compose scaffold, kept for reference;
  the Flutter app in `/flutter_app` is the actively developed MVP.
