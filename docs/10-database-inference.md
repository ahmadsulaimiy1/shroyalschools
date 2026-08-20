# 10 — Database Proposal

> ## ⚠ Read this first
>
> **This is a proposal for a new database, not documentation of the existing one.**
>
> The live LMS database is not observable — the application is login-walled. What follows is
> a schema *designed* from the evidence in `07-forms.md` and `08-lms.md`. Anchors in observed
> reality are marked **[OBSERVED]**; everything else is design.
>
> Do not hand this to a developer as "the current schema". Request the real one — see
> `08-lms.md` §9.

### Observed anchors

| Evidence | Implication |
|---|---|
| **[OBSERVED]** Form fields: `Name`, `Gender`, `Age`, `Email`, `Country`, `Mobile`, `Language`, `HefzDailyCount`, `HefzDuration`, `AcademicAdvertiseWay`, `CircleNumber`, `fy` | Student attributes |
| **[OBSERVED]** `circleTypeId` integers: 28,30,32,34,36,38,44–51,57,58,79,92,93,94,106 | A `CircleType` table with sequential integer PKs, ≥106 rows |
| **[OBSERVED]** GUID per track alongside the integer | Dual key: internal PK + public token |
| **[OBSERVED]** `CircleNumber` = `حلقة استقبال طلاب الجدد` | `Circle` is distinct from `CircleType` |
| **[OBSERVED]** Closed → `CreateNeedToRegisterdUser` | A waitlist table exists |
| **[OBSERVED]** Login = email + code | No password hash; a short-lived code table |
| **[OBSERVED]** 7 UI locales, 8 form languages | A locale reference table |
| **[OBSERVED]** SignalR + `notifications.js` | A notifications table |
| **[OBSERVED]** Terms clause 4: recitation reports via the platform | A reporting/assessment table |
| **[OBSERVED]** `fy` hidden field | Academic/fiscal year scoping |

---

## 1. Entity overview

```
AcademicYear ──┬── CircleType ──── Circle ──── Enrollment ──── User
               │       │              │             │            │
               │       └── Waitlist   ├─ Session ───┼── Attendance
               │                      │             │
               │                      └─ TeacherAssignment
               │
               └── RecitationReport ── ProgressSnapshot ── Certificate
                                          Notification · Message
                                          StaffApplication · ConsentRecord
                                          Guardian ✚
```

---

## 2. Core tables

### `users`
```sql
id                 UUID PK
email              CITEXT UNIQUE NOT NULL   -- [OBSERVED] login identifier
full_name          TEXT NOT NULL            -- [OBSERVED] terms require 3 parts
gender             ENUM('male','female')    -- [OBSERVED]
date_of_birth      DATE                     -- replaces raw Age (see §5)
country_code       CHAR(2)                  -- [OBSERVED]
mobile_e164        TEXT                     -- [OBSERVED]
preferred_language CHAR(3)                  -- [OBSERVED] 8 options
role               ENUM('student','teacher','supervisor','admin','guardian')
status             ENUM('pending','active','suspended','graduated','withdrawn')
guardian_id        UUID FK → users(id)      -- ✚ required when age < 18
timezone           TEXT                     -- ✚ absent today; essential for live halaqat
created_at, updated_at, last_login_at
```
**Change from observed:** store `date_of_birth`, not `Age`. The live form captures a
**static integer** that silently becomes wrong — a 7-year-old in an age-banded 7–12 track is
misfiled within a year. This is a real data-integrity bug, not a stylistic preference.

### `login_codes` — **[OBSERVED]** passwordless auth
```sql
id UUID PK · user_id FK · code_hash TEXT NOT NULL   -- hash, never plaintext
expires_at TIMESTAMPTZ NOT NULL                     -- recommend 10 min
consumed_at TIMESTAMPTZ · attempt_count INT DEFAULT 0
ip_address INET · user_agent TEXT
INDEX (user_id, expires_at)
```
Rate-limit issuance and verification; lock after N failures.

### `circle_types` — **[OBSERVED]**
```sql
id            SERIAL PK          -- [OBSERVED] 28…106
public_token  UUID UNIQUE        -- [OBSERVED] the ?i= GUID
code          TEXT               -- [OBSERVED] A11, B11, C11, C21, D11, E11, H11, G11, X11
name_ar, name_en TEXT
gender        ENUM('male','female')      -- [OBSERVED] pre-filters the form
residency     ENUM('ksa','international')-- [OBSERVED]
age_min, age_max SMALLINT                -- [OBSERVED] 3–6, 7–12, 13–18, 19–40, 40+
is_special_needs BOOLEAN                 -- [OBSERVED] E11
is_ijazah        BOOLEAN                 -- [OBSERVED] H11
language_scope   TEXT[]                  -- [OBSERVED] G11/X11 serve all non-Arabic
registration_status ENUM('open','closed','waitlist_only')  -- [OBSERVED]
capacity, enrolled_count INT
reopens_at    DATE                       -- ✚ powers "reopens Rajab 1448"
academic_year_id FK
```
> **`public_token` must be the only identifier in any URL.** The live system exposes the
> integer `id` on the closed-track redirect — see `08-lms.md` §3.

### `circles` — **[OBSERVED]** distinct from `circle_types`
```sql
id UUID PK · circle_type_id FK · name TEXT   -- [OBSERVED] "حلقة استقبال طلاب الجدد"
teacher_id FK → users · supervisor_id FK → users
schedule JSONB          -- days, start time, duration
timezone TEXT · capacity INT · current_enrollment INT
meeting_url TEXT · meeting_platform TEXT   -- external video (see 08-lms.md §5)
status ENUM('forming','active','paused','completed')
```

### `enrollments`
```sql
id UUID PK · user_id FK · circle_id FK · circle_type_id FK
hefz_daily_count ENUM  -- [OBSERVED] quarter/half/1/2/3/4/5 pages
hefz_duration    ENUM  -- [OBSERVED] <1mo, 2mo, 6mo, 1y, 1.5y, 2y, 3y
referral_source  TEXT  -- [OBSERVED] AcademicAdvertiseWay
status ENUM('pending','active','completed','withdrawn','transferred')
enrolled_at · completed_at · academic_year_id FK
UNIQUE (user_id, circle_id)
```

### `waitlist_entries` — **[OBSERVED]**, substantially extended
```sql
id UUID PK
circle_type_id FK NOT NULL      -- [OBSERVED]
full_name TEXT NOT NULL         -- [OBSERVED]
whatsapp  TEXT NOT NULL         -- [OBSERVED]
email     CITEXT                -- ✚✚ NOT captured today — the critical gap
age SMALLINT · gender ENUM · country_code CHAR(2) · preferred_language CHAR(3)  -- ✚
consent_to_contact BOOLEAN NOT NULL DEFAULT FALSE                              -- ✚
position INT · notified_at TIMESTAMPTZ · converted_enrollment_id FK             -- ✚
created_at
INDEX (circle_type_id, created_at)
```
> **The `email` column is the single most valuable addition in this schema.** Without it the
> academy cannot contact the 61% of prospects who reach the waitlist. Everything else here
> is refinement; this is the difference between a dead end and a pipeline.

---

## 3. Learning tables

### `recitation_reports` — **[OBSERVED]** via terms clause 4
```sql
id UUID PK · enrollment_id FK · session_id FK
report_type ENUM('hefz','muraja','tilawa')   -- memorisation / review / recitation
from_surah, from_ayah, to_surah, to_ayah INT
pages_completed NUMERIC(4,2)                 -- supports quarter-page granularity
teacher_rating ENUM('excellent','very_good','good','needs_review')
teacher_notes TEXT · errors_count INT
submitted_at · reviewed_at · reviewed_by FK
```
Quarter-page granularity is required by the **[OBSERVED]** `ربع وجه` option.

### `sessions`, `attendance`
```sql
sessions:   id · circle_id FK · scheduled_start/end TIMESTAMPTZ · actual_* · status · meeting_url · notes
attendance: id · session_id FK · user_id FK
            status ENUM('present','absent_excused','absent_unexcused','late')  -- [OBSERVED] terms clause 4
            minutes_attended INT · excuse_note TEXT · recorded_by FK
            UNIQUE (session_id, user_id)
```

### `progress_snapshots`, `certificates`
```sql
progress_snapshots: id · enrollment_id FK · as_of DATE
                    total_pages_memorized NUMERIC · juz_completed INT
                    current_surah INT · attendance_rate NUMERIC(5,2)
                    consistency_score NUMERIC(5,2)

certificates:       id · user_id FK · enrollment_id FK
                    type ENUM('completion','juz','full_quran','ijazah','tajweed')
                    -- [OBSERVED] advantage #1 claims Maknoon-accredited certificates
                    -- [OBSERVED] H11 track grants إجازات بالسند المتصل
                    issued_by_org TEXT DEFAULT 'جمعية مكنون'
                    sanad_chain TEXT          -- isnad for ijazah
                    verification_code TEXT UNIQUE · pdf_url TEXT
                    issued_at · revoked_at
```
`sanad_chain` supports the **[OBSERVED]** `منح الإجازات القرآنية بالسند المتصل` claim — an
ijazah's value *is* its chain of transmission, so it must be a first-class field.

---

## 4. Supporting tables

```sql
notifications:      id · user_id FK · type · title · body · locale
                    channel ENUM('in_app','email','whatsapp','sms')
                    read_at · sent_at · payload JSONB          -- [OBSERVED] SignalR

messages:           id · thread_id · sender_id FK · recipient_id FK
                    body TEXT · sent_at · read_at
                    -- terms clause 3 forbids non-educational private contact:
                    -- messaging must be teacher↔student within a circle, and auditable

staff_applications: id · role ENUM('teacher','supervisor') · gender
                    full_name · email · mobile · country_code
                    qualifications TEXT · ijazah_details TEXT · has_ijazah BOOLEAN
                    availability JSONB · cv_url · years_experience INT
                    status ENUM('submitted','screening','interview','accepted','rejected')
                    -- ✚ replaces the 4 Google Forms

consent_records:    id · user_id FK · policy_version TEXT · policy_type
                    consented_at · ip_address INET · user_agent TEXT
                    -- ✚ the live site requires consent but records nothing

guardians:          id · guardian_user_id FK · child_user_id FK
                    relationship ENUM('father','mother','guardian')
                    consent_given_at · can_view_progress BOOLEAN
                    -- ✚✚ REQUIRED: the platform enrols children from age 3
                    UNIQUE (guardian_user_id, child_user_id)

academic_years:     id · name -- [OBSERVED] the `fy` field; note © 1448 (Hijri)
                    hijri_year · gregorian_start/end · is_current
                    -- store BOTH calendars: the org operates in Hijri, systems in Gregorian

audit_log:          id · actor_id FK · action · entity_type · entity_id
                    before JSONB · after JSONB · ip_address · created_at
                    -- required for a platform handling minors' data
```

---

## 5. Design decisions worth defending

| Decision | Rationale |
|---|---|
| `date_of_birth` not `Age` | **[OBSERVED]** the form stores a static integer that decays. Age bands are the platform's core taxonomy; storing a stale number corrupts them. |
| Dual key (`id` + `public_token`) | **[OBSERVED]** the system already does this — but leaks the integer. Enforce token-only URLs. |
| `email` on waitlist | **[OBSERVED]** absent today; the direct cause of an unrecoverable 61% drop-off. |
| `guardians` table | Enrolling 3-year-olds without a guardian record is a safeguarding and legal gap. |
| `consent_records` | Consent is demanded but not stored; an "اتفاقية" with no record is unenforceable. |
| Hijri + Gregorian | **[OBSERVED]** `© 1448`. Storing only Gregorian loses the organisation's working calendar. |
| Quarter-page `NUMERIC` | **[OBSERVED]** `ربع وجه`. Integer pages cannot represent the smallest unit the academy teaches in. |
| `sanad_chain` | **[OBSERVED]** ijazah with connected chain is an advertised product. |
| `timezone` on users and circles | Live halaqat across KSA, Europe, Africa and South Asia — absent today. |
| `audit_log` | Minors' data plus multiple staff roles. |

---

## 6. Indexing and integrity

```sql
CREATE INDEX idx_enroll_user     ON enrollments(user_id, status);
CREATE INDEX idx_enroll_circle   ON enrollments(circle_id, status);
CREATE INDEX idx_ct_availability ON circle_types(registration_status, gender, residency);
CREATE INDEX idx_waitlist_type   ON waitlist_entries(circle_type_id, created_at);
CREATE INDEX idx_attend_session  ON attendance(session_id);
CREATE INDEX idx_reports_enroll  ON recitation_reports(enrollment_id, submitted_at DESC);
CREATE INDEX idx_notif_unread    ON notifications(user_id) WHERE read_at IS NULL;
```

**Constraints:** `age_min <= age_max` · `enrolled_count <= capacity` · a user's gender must
match their circle type's gender · `guardian_id` required when age < 18 ·
`UNIQUE(user_id, circle_id)` · soft-delete rather than hard-delete student records.

**Encoding:** UTF-8 (`utf8mb4` on MySQL) end-to-end. Arabic diacritics
(`مِقْرَأَةُ إِتْقَانَ`) and Urdu/Russian text must survive storage, indexing and collation —
verify collation explicitly, as the marketing copy depends on exact diacritics.
