# 06 — API Documentation

## 1. API Style & Principles

REST/JSON over HTTPS for v1 (broad client compatibility, simple caching), with a GraphQL gateway
under evaluation for v2 institutional/admin use cases with heterogeneous query shapes. All
endpoints versioned via URL prefix `/v1/`. All timestamps ISO-8601 UTC. All list endpoints
cursor-paginated (`?cursor=`, `?limit=`, response includes `next_cursor`).

Base URL: `https://api.misbaha.app/v1`

## 2. Authentication

- `POST /v1/auth/anonymous` — issues a device-bound anonymous session (no PII), enabling sync
  without account creation, matching the zero-friction onboarding journey in the Design System.
- `POST /v1/auth/signup`, `POST /v1/auth/login` — email/password or OAuth (Google/Apple/Microsoft),
  returns short-lived JWT access token (15 min) + rotating refresh token (30 days, single-use,
  reuse-detection revokes the token family).
- `POST /v1/auth/upgrade-anonymous` — links an anonymous device session to a newly created
  account, preserving local history.
- All authenticated requests: `Authorization: Bearer <access_token>`.

## 3. Core Endpoints

### Content Sync (read-mostly, heavily cached/CDN'd)
```
GET  /v1/content/dhikr?category=post_salah&locale=ar&since=<content_version>
GET  /v1/content/quran/{surah}?locale=en
GET  /v1/content/asma-ul-husna
GET  /v1/content/audio/{asset_ref}         -> signed CDN URL, short expiry
```
Only `status='approved'` governance-reviewed content is ever exposed here (§3 in Database Schema).
`since=<content_version>` enables delta sync — clients only download changed records.

### Dhikr Events (write-heavy, append-only, idempotent)
```
POST /v1/sync/events
  Body: { "events": [ { "id": "<client-uuid>", "session_id": "...", "increment": 1,
                          "occurred_at": "...", "source": "tap" }, ... ] }
  -> 200 { "accepted": ["<uuid>", ...], "duplicates": ["<uuid>", ...] }
```
Client-generated UUIDs make retries safe (idempotent upsert on primary key) — critical for the
offline-for-weeks Hajj scenario where a device syncs a large backlog at once.

```
GET  /v1/sync/sessions?since=<cursor>
POST /v1/sync/sessions          -- create/update session metadata (target, context_tag, completion)
```

### Journal & Stats
```
GET  /v1/journal/summary?range=weekly|monthly|yearly
GET  /v1/journal/streak
```
Aggregation is computed server-side from `dhikr_events` for the authoritative cross-device view;
the on-device Room copy remains the source of truth for the single-device offline UI.

### Circles / Community
```
POST /v1/circles                          -- create family/mosque circle
POST /v1/circles/{id}/join
GET  /v1/circles/{id}/aggregate            -- aggregate-only counters, no per-member breakdown
                                               unless visibility=name_visible was explicitly set
```

### Account & Privacy (GDPR rights)
```
GET    /v1/account/export       -- full data export (JSON), Art. 20 portability
DELETE /v1/account               -- initiates erasure workflow, Art. 17
GET    /v1/account/consents
PATCH  /v1/account/consents
```

### Institutional / Admin (separate scoped tokens, see Admin Dashboard doc)
```
POST /v1/institutions
PATCH /v1/institutions/{id}/branding
GET  /v1/institutions/{id}/analytics       -- aggregate, privacy-preserving (k-anonymity floor)
```

## 4. Rate Limiting & Abuse Protection

- Per-token sliding-window limits: 120 req/min standard, 20 req/min for `/auth/*`.
- `/v1/sync/events` accepts batches (up to 500 events/request) specifically so high-frequency
  taps are never sent as individual requests — client-side batching is required by contract, not
  just an optimization.
- 429 responses include `Retry-After`; clients back off exponentially and persist unsent events
  locally (never dropped).

## 5. Error Model

```json
{ "error": { "code": "CONTENT_VERSION_STALE", "message": "...", "request_id": "..." } }
```
Consistent error envelope; `request_id` ties client bug reports to server-side traces.

## 6. Webhooks (Institutional tier)

`institution.subscription.updated`, `institution.analytics.weekly_ready` — signed (HMAC-SHA256)
payloads for institutional customers integrating with their own systems.

## 7. SDK & Client Contract

The Android `core-network` module (see [Architecture §2](04-ANDROID-ARCHITECTURE.md)) generates
typed Retrofit interfaces from this contract, kept in sync via an OpenAPI 3.1 spec maintained
alongside the backend and validated in CI against contract tests.
