# 05 — Database Schema

## 1. Overview

Two coordinated schemas: an **on-device Room (SQLite)** schema optimized for offline-first reads,
and a **cloud Postgres** schema (backing the sync/API tier) optimized for multi-tenant scale,
analytics, and content governance. Both share entity shapes to keep the sync mapping simple.

## 2. On-Device Schema (Room / SQLite)

```
User (local profile, may be anonymous pre-signup)
  id: UUID (PK)
  display_name: TEXT NULL
  locale: TEXT              -- 'ar', 'en', ...
  madhhab_preference: TEXT NULL
  created_at: INTEGER (epoch ms)
  is_synced_account: BOOLEAN

DhikrDefinition (cached from content service — read-only locally)
  id: UUID (PK)
  category: TEXT            -- 'post_salah','morning','evening','travel','ruqyah','sleep',...
  arabic_text: TEXT
  transliteration: TEXT
  translation_en: TEXT
  source_citation: TEXT
  authenticity_grade: TEXT  -- 'quran','sahih','hasan','da_if_reference_only'
  default_target_count: INTEGER
  audio_asset_ref: TEXT NULL
  content_version: INTEGER  -- governance revision number
  governance_signoff_id: TEXT

CounterSession
  id: UUID (PK)
  user_id: UUID (FK -> User.id)
  dhikr_definition_id: UUID (FK -> DhikrDefinition.id) NULL   -- NULL = freeform counter
  target_count: INTEGER
  started_at: INTEGER
  completed_at: INTEGER NULL
  context_tag: TEXT NULL    -- 'ramadan','hajj','post_salah', freeform

DhikrEvent (append-only ledger — source of truth for counts; never UPDATEd, only INSERTed)
  id: UUID (PK)
  session_id: UUID (FK -> CounterSession.id)
  increment: INTEGER        -- normally 1, supports batch corrections
  occurred_at: INTEGER
  source: TEXT              -- 'tap','ble_ring','voice','watch'
  synced_at: INTEGER NULL   -- NULL until acknowledged by server

JournalEntry
  id: UUID (PK)
  user_id: UUID (FK)
  date: TEXT (ISO date)
  note: TEXT NULL           -- private, device-encrypted
  dedication_note: TEXT NULL -- optional personal sadaqah-jariyah dedication label

CircleMembership (opt-in community)
  id: UUID (PK)
  user_id: UUID (FK)
  circle_id: UUID
  visibility: TEXT          -- 'aggregate_only','name_visible'
  joined_at: INTEGER

UserSettings
  user_id: UUID (PK, FK)
  theme: TEXT
  numeral_style: TEXT       -- 'eastern_arabic','western_arabic'
  reduce_motion: BOOLEAN
  high_contrast: BOOLEAN
  haptics_enabled: BOOLEAN
  prayer_calc_method: TEXT
  reminder_prefs_json: TEXT
```

Indices: `DhikrEvent(session_id, occurred_at)`, `DhikrEvent(synced_at)` for sync-worker queries,
`CounterSession(user_id, started_at)` for journal aggregation.

## 3. Cloud Schema (PostgreSQL — sync/content/governance tier)

```
users
  id UUID PK, email CITEXT UNIQUE NULL, auth_provider TEXT, locale TEXT,
  created_at TIMESTAMPTZ, deleted_at TIMESTAMPTZ NULL   -- soft delete for GDPR erasure workflow

dhikr_definitions
  id UUID PK, category TEXT, arabic_text TEXT, transliteration TEXT,
  translations JSONB,             -- { "en": "...", "ur": "...", "ms": "..." }
  source_citation TEXT, authenticity_grade TEXT,
  content_version INT, status TEXT,     -- 'draft','in_review','approved','deprecated'
  governance_signoff_id UUID FK -> governance_reviews.id,
  created_at TIMESTAMPTZ, updated_at TIMESTAMPTZ

governance_reviews
  id UUID PK, dhikr_definition_id UUID FK, reviewer_id UUID FK -> scholars.id,
  decision TEXT, notes TEXT, reviewed_at TIMESTAMPTZ

scholars
  id UUID PK, name TEXT, credentials TEXT, madhhab_affiliation TEXT, active BOOLEAN

dhikr_events (partitioned by month, append-only, high volume)
  id UUID PK, user_id UUID FK, session_id UUID, increment INT,
  occurred_at TIMESTAMPTZ, source TEXT, ingested_at TIMESTAMPTZ

counter_sessions
  id UUID PK, user_id UUID FK, dhikr_definition_id UUID NULL,
  target_count INT, started_at TIMESTAMPTZ, completed_at TIMESTAMPTZ NULL, context_tag TEXT

circles
  id UUID PK, name TEXT, type TEXT,   -- 'family','mosque','institution'
  owner_user_id UUID FK, institution_id UUID NULL FK -> institutions.id

institutions  -- white-label / B2B tenants, see Monetisation §4
  id UUID PK, name TEXT, plan_tier TEXT, branding_config JSONB, created_at TIMESTAMPTZ

subscriptions
  id UUID PK, user_id UUID FK NULL, institution_id UUID FK NULL,
  tier TEXT, status TEXT, renews_at TIMESTAMPTZ, payment_provider_ref TEXT

audit_log  -- security & governance traceability, see Security Framework §5
  id UUID PK, actor_id UUID, action TEXT, target_type TEXT, target_id UUID,
  metadata JSONB, occurred_at TIMESTAMPTZ
```

Content tables (`dhikr_definitions`, `governance_reviews`, `scholars`) are the authoritative
governance record described in the [Brand Identity Shariah Charter](03-BRAND-IDENTITY.md#6-shariah-content-governance-charter);
mobile clients only ever receive `status = 'approved'` rows through the content sync API.

## 4. Data Classification & Retention

| Data class | Examples | Retention |
|---|---|---|
| Worship/behavioral (sensitive) | dhikr_events, counter_sessions, journal notes | User-controlled; deleted on account erasure request within 30 days |
| Account | users, subscriptions | Retained per legal/tax requirement post-deletion where mandated, minimized otherwise |
| Content | dhikr_definitions, governance_reviews | Retained indefinitely as public content record |
| Telemetry | crash/perf events | Pseudonymized, 90-day rolling window |

Full handling detailed in [Security Framework §4](09-SECURITY-FRAMEWORK.md#4-data-classification--gdpr-compliance).
