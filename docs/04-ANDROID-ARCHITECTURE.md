# 04 — Android Source Code Architecture

## 1. Guiding Constraints

- 100% offline-capable core loop (counting, library reading, journaling).
- Clean separation so the same domain/data layers can eventually back a KMP (Kotlin Multiplatform)
  push into iOS, sharing business logic — de-risking the Year-2 iOS expansion in the
  [Roadmap](11-FIVE-YEAR-ROADMAP.md) without a rewrite.
- Enterprise scale: modularized so 10s of feature teams can work without merge contention.

## 2. Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | Kotlin | Standard, coroutines/Flow for reactive offline-first data |
| UI | Jetpack Compose + Material 3 (heavily re-themed, not stock Material look) | Modern declarative UI, first-class RTL & accessibility support |
| DI | Hilt | Standard Android DI, testable module graph |
| Local persistence | Room (SQLite) + DataStore (preferences) | Structured relational data + lightweight settings |
| Async/reactive | Kotlin Coroutines + Flow | Structured concurrency, backpressure-safe streams |
| Networking (sync/cloud) | Retrofit + OkHttp + kotlinx.serialization | REST sync per [API doc](06-API-DOCUMENTATION.md) |
| Background work | WorkManager | Deferred sync, reminder scheduling, resilient to Doze/App Standby |
| Dependency graph target | Kotlin Multiplatform-ready `:core` modules | Future iOS/Web code share |
| Testing | JUnit5, Turbine (Flow testing), Compose UI Test, Robolectric | Full pyramid coverage |
| Crash/observability | Structured logging + crash reporting SDK (privacy-scrubbed) | See [Security §6](09-SECURITY-FRAMEWORK.md) |

## 3. Module Map

```
misbaha/
├── app/                          # Application shell, nav graph, DI wiring, splash
├── core/
│   ├── core-designsystem/        # Compose theme, tokens, shared components (BeadRingCounter, etc.)
│   ├── core-data/                # Repository interfaces + implementations, sync engine
│   ├── core-database/            # Room entities/DAOs (see Database Schema doc)
│   ├── core-datastore/           # User preferences, settings
│   ├── core-network/             # Retrofit services, DTOs, auth interceptors
│   ├── core-domain/               # Use cases (pure Kotlin, platform-agnostic — KMP-ready)
│   ├── core-model/                # Shared domain models (pure Kotlin)
│   ├── core-common/                # Result wrappers, dispatchers, utilities
│   └── core-analytics/            # Privacy-scrubbed event tracking abstraction
├── feature/
│   ├── feature-counter/          # Tasbeeh counting engine + UI
│   ├── feature-library/          # Adhkar/Qur'an/Asma-ul-Husna content browsing
│   ├── feature-journal/          # Stats, streaks, history, Ramadan/Hajj modes
│   ├── feature-circles/          # Opt-in community/family features
│   ├── feature-onboarding/       # First-run flow
│   └── feature-settings/         # Accessibility, language, subscription, privacy controls
└── sync/
    └── sync-worker/               # WorkManager jobs: background sync, prayer-time refresh, reminders
```

Each `feature-*` module depends only on `core-*` modules, never on another `feature-*` module
directly — cross-feature navigation goes through the `app` module's nav graph using route
contracts, keeping the dependency graph acyclic and buildable in isolation (parallel CI, faster
incremental builds at scale).

## 4. Architecture Pattern — Clean Architecture + MVVM/MVI

```
UI (Compose) → ViewModel (UDF: State + Intent) → UseCase (core-domain) → Repository (core-data)
                                                                              ↓            ↓
                                                                    Room (local)   Retrofit (remote)
```

- **Unidirectional Data Flow:** each screen exposes a single immutable `UiState` via
  `StateFlow`, mutated only through `ViewModel.onIntent(Intent)` — no ad-hoc mutable state in
  Composables, which keeps the counter screen correct under process death/rotation.
- **Offline-first repository pattern:** Repositories are the single source of truth backed by
  Room; network sync only writes into Room, UI never reads network responses directly. This
  guarantees identical behavior whether the device is online or fully offline.
- **Sync strategy:** Append-only local event log (`DhikrEventEntity`) is the durable source of
  truth for counts; a background `SyncWorker` uploads unsynced events in batches and reconciles
  server-acknowledged state, using event UUIDs for idempotency — safe against duplicate delivery
  and offline-for-weeks scenarios (Hajj/rural use case from the PRD).

## 5. Performance Engineering

- Compose `Stable`/`Immutable` annotations audited on all UI state classes to prevent
  recomposition storms on the high-frequency counter screen.
- Counter tap path avoids any disk I/O on the UI thread; the tap is written to an in-memory
  buffer and flushed to Room on a debounce/lifecycle boundary, so tap latency is bound only by
  Compose recomposition, not storage I/O.
- Baseline Profiles + macrobenchmarking (Jetpack Macrobenchmark) enforced in CI to guard the
  <800ms cold-start budget from the PRD.
- App size budget enforced via Play Feature Delivery: large asset packs (extra reciter audio,
  premium themes) are dynamic feature modules, not bundled into the base APK/AAB.

## 6. Multi-Form-Factor Readiness (from day one)

- Compose layouts built with `WindowSizeClass` from the start (phone/foldable/tablet), not
  retrofitted later — directly serves the Roadmap's tablet and eventual TV ambitions.
- Wear OS companion planned as a separate `wear/` module sharing `core-domain`/`core-model`
  (Kotlin Multiplatform boundary already respected by module design in §3).

## 7. CI/CD Hooks (summary — full detail in [Deployment Plan](10-DEPLOYMENT-LAUNCH-PLAN.md))

Static analysis (ktlint, detekt), unit + instrumented test gates, Baseline Profile regression
check, and accessibility lint (Compose a11y checks) run on every PR; merge to `main` triggers
signed internal-track AAB build for QA per the Deployment Plan.
