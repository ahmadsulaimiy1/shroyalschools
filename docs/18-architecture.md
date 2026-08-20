# 18 — Target Architecture

Sized for **100,000 active students** and **10,000 concurrent users**, multilingual,
multi-campus, multi-country, cloud-deployed, with mobile apps, APIs, analytics and AI.

All **[RECOMMENDED]** unless labelled otherwise.

---

## 1. Sizing — read this before designing anything

The concurrency requirement is far less alarming than it sounds, and getting this right
avoids massively over-engineering.

**[VERIFIED]** A halaqa is a small group — the academy's tracks are age-banded circles, and
**[RESEARCHED]** comparable Saudi platforms run circles of 1–4 hours daily. A Quran circle is
**5–15 students**, not a 10,000-person lecture.

So 10,000 concurrent users decomposes as:

| Segment | Estimate | Load profile |
|---|---:|---|
| In live halaqat | ~7,000 | ≈ **700 concurrent rooms of ~10** |
| Browsing/dashboards | ~2,500 | Ordinary web traffic |
| Uploading audio | ~500 | Bursty writes |

**[RESEARCHED]** "Below 100 participants, a single SFU node handles it." 700 rooms of 10 is a
**horizontally trivial SFU problem** — not the 1K–10K single-room cascade scenario that
demands regional cascading.

### Two real constraints, and they are not raw concurrency

1. **Peak spikes are extreme and predictable.** Sessions start on the hour. **[RESEARCHED]**
   circles run 1–4 hours daily, and much of the audience shares Gulf time. Expect ~60% of
   daily load inside a few hour-boundary minutes.
   → Design for **burst**, not average. Pre-warm before session boundaries.
2. **Ramadan.** Quran platform load multiplies during Ramadan and collapses afterwards.
   → **Elastic capacity is a hard requirement**, not an optimisation.

> Sizing for "10,000 concurrent" as though it were one room would waste a large amount of
> money. Size for **700 small rooms with violent hourly spikes and an annual 3–5× season.**

---

## 2. Architecture style

**[RECOMMENDED] Modular monolith + selectively extracted services.**

Not microservices. At this scale, with what **[INFERRED]** is likely a small team, a
distributed architecture would add far more operational cost than it removes. Extract only
what has genuinely different scaling or availability characteristics.

```
┌──────────────────────────────────────────────────────────────┐
│  Clients                                                     │
│  Web (Next.js, RTL, 8 locales) · iOS · Android               │
│  Student app · Teacher app (offline-first) · Parent app      │
└───────────────────────────┬──────────────────────────────────┘
                            │ HTTPS / WSS
┌───────────────────────────▼──────────────────────────────────┐
│  Edge — CDN, WAF, DDoS, rate limiting                        │
└───────────────────────────┬──────────────────────────────────┘
┌───────────────────────────▼──────────────────────────────────┐
│  API Gateway — authn, routing, quotas                        │
└───────────────────────────┬──────────────────────────────────┘
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ CORE         │  │ EXTRACTED        │  │ EXTRACTED        │
│ MONOLITH     │  │ SERVICES         │  │ ASYNC            │
│              │  │                  │  │                  │
│ Identity     │  │ Live Classes     │  │ Notifications    │
│ Admissions   │  │  (SFU cluster)   │  │ Reports (PDF)    │
│ Enrolment    │  │                  │  │ Revision sched.  │
│ Hifz/Tasmi'  │  │ Media Pipeline   │  │ Analytics ingest │
│ Attendance   │  │  (audio/video)   │  │ Email/WhatsApp   │
│ Assessment   │  │                  │  │                  │
│ Certificates │  │ AI Inference     │  │ ← queue-driven   │
│ Portals ×11  │  │  (pronunciation) │  │                  │
└──────┬───────┘  └────────┬─────────┘  └────────┬─────────┘
       └───────────────────┼─────────────────────┘
                           ▼
   PostgreSQL (primary + replicas) · Redis · Object storage
   ClickHouse (analytics) · Search
```

**Why these three are extracted:**
- **Live classes** — bursty, stateful, CPU/bandwidth-bound, and must scale independently
- **Media pipeline** — long-running transcode/transcription jobs must never block requests
- **AI inference** — GPU-bound, optional, and must degrade gracefully when unavailable

Everything else stays in one deployable unit until measurement proves otherwise.

---

## 3. 🚨 Hosting & data residency — the decisive constraint

**[RESEARCHED]** Saudi PDPL rules for children's data include **data sovereignty
requirements ensuring children's data remains within Saudi Arabia** and **restrictions on
cross-border transfers**. **[VERIFIED]** the academy enrols children **from age 3**.

This is not a preference. It **determines the cloud provider.**

### In-Kingdom options as of August 2026 **[RESEARCHED]**

| Provider | Status |
|---|---|
| **Google Cloud — Dammam** | ✅ **Live since November 2023** |
| **Oracle Cloud — Riyadh** (`me-riyadh-1`) | ✅ **Live since October 2024** |
| **Oracle Cloud — Jeddah** (`me-jeddah-1`) | ✅ Live since 2020 |
| Microsoft Azure — Saudi Arabia East | ⏳ Announced for **Q4 2026** |
| AWS — Saudi region | ⏳ Committed ($5.3bn), **not yet GA** |
| Local sovereign providers (STC, SCCC) | ✅ Available |

**[RECOMMENDED]** **Google Cloud Dammam** or **Oracle Riyadh** as primary. Both are live
in-Kingdom today with multiple availability zones.

**[RECOMMENDED] Data classification and placement:**

| Class | Examples | Placement |
|---|---|---|
| **Minors' PII + recordings + voice** | Under-18 records, session recordings, audio submissions | **KSA only. Never leaves.** |
| Adult student PII | Adult records | KSA primary |
| Operational | Schedules, capacity, curriculum | KSA primary, may be cached at edge |
| Public content | Mushaf, marketing, mind maps | Global CDN |
| Analytics | Aggregated, pseudonymised | KSA; no raw minor PII |

> **[VERIFIED] A live problem to fix first:** V1 routes registrations — including children's —
> through **Google Forms**, and serves fonts from Google, meaning children's personal data
> already leaves the Kingdom. Migrating those seven forms in-platform (`15` §7) is a
> compliance action, not a UX improvement.

**Multi-country expansion:** as the academy expands, the model is **regional data residency
with a shared control plane** — KSA data in KSA, EU data in EU (GDPR), each region's minors'
data staying home. Design the tenancy model for this from day one; retrofitting residency is
extremely expensive.

---

## 4. Live classes

**[RESEARCHED]** SFU is the 2026 default; LiveKit is cloud-native, strictly separates
signalling from media, and runs as stateless horizontally-scalable pods on Kubernetes.

**[RECOMMENDED]** Self-hosted **LiveKit** (open source) on Kubernetes in-Kingdom.

Self-hosting rather than LiveKit Cloud is driven by **[RESEARCHED]** PDPL residency — minors'
audio and video must not traverse or rest outside KSA, which a global managed SFU cannot
guarantee.

**Sizing:** ~700 concurrent rooms × ~10 participants. **[RESEARCHED]** a single SFU node
handles sub-100-participant rooms comfortably; this is a horizontal-pod problem. Use
simulcast + SVC, audio-only fallback for poor connections (common and important for
international students), and autoscale on the hourly boundary pattern from §1.

**Recording:** server-side, stored in-Kingdom, 90-day retention, guardian consent enforced
before any minor is recorded (`16` §14).

---

## 5. Data layer

| Store | Use | Why |
|---|---|---|
| **PostgreSQL** | Primary OLTP | Relational integrity matters here — enrolment, sanad chains, consent records |
| Read replicas | Dashboards, reports | Keeps analytical reads off the primary |
| **Redis** | Sessions, revision queues, rate limits, presence | The daily revision queue is a natural cached-computation |
| **Object storage** | Audio submissions, recordings, certificates, mushaf assets | In-Kingdom bucket for minors' media |
| **ClickHouse** | Learning analytics, xAPI stream | Append-heavy event data; column store fits |
| **Search** (OpenSearch) | Students, content, mushaf | |

**Partitioning:** by academic year (**[VERIFIED]** V1 already carries an `fy` field) and by
tenant/campus. Attendance and tasmi' records are the high-volume tables — 100k students × ~250
sessions/year ≈ **25M attendance rows and 25M tasmi' records per year**. Partition both by
year from the start.

**[RECOMMENDED]** The revision scheduler (`16` §2.2) computes each student's daily queue.
Doing this on demand for 100k students is wasteful; compute nightly per timezone as a batch
job and cache in Redis, recomputing on the fly only when a tasmi' is graded.

---

## 6. Multi-tenancy & multi-campus

**[RECOMMENDED]** Single database, `tenant_id` on every table, row-level security enforced in
the database — not only in application code.

Hierarchy: **Association** (e.g. Maknoon) → **Campus/Academy** (e.g. Itqan) → **Track** →
**Circle**. Supports the academy's real situation **[VERIFIED]**: it operates under Maknoon
and partners with جمعية إقرأ بالخرمة.

Per-tenant configuration: branding, locales, track catalogue, academic calendar, capacity
rules, certificate templates.

---

## 7. Mobile

**[RESEARCHED]** Peer systems ship **three separate apps** (teacher, student, parent).

**[RECOMMENDED]** Three apps, one shared React Native / Expo codebase.

**Teacher app must be offline-first.** Teachers mark attendance and grade tasmi' in
conditions where connectivity is unreliable; losing a session's grading is unacceptable.
Local-first writes with sync-on-reconnect and conflict resolution.

**Student app:** offline mushaf, offline audio, queued submissions.
**Parent app:** lightweight — progress, attendance, reports, notifications.

---

## 8. Analytics & AI

**Product analytics:** privacy-respecting (Plausible/Matomo, self-hosted in-Kingdom).
**[VERIFIED]** V1 has **none on either host** — this is the baseline gap.

**Learning analytics:** an xAPI-shaped event stream into ClickHouse (`17` §2), powering the
early-warning model (`16` §11) and the executive dashboard.

**AI services** — extracted, GPU-backed, and **always optional**:
- Pronunciation/error pre-screen (`16` §16)
- At-risk prediction from attendance, error trend and revision backlog
- Admissions placement support

**[RECOMMENDED]** Every AI path must degrade gracefully: if inference is unavailable, the
teacher grades exactly as before. **No workflow may depend on AI availability.** Minors' voice
data is processed in-Kingdom with guardian consent and strict retention.

---

## 9. Security

- MFA for all staff roles; passwordless email-code for students/parents **[VERIFIED]** *(keep — V1 got this right)*
- Codes hashed, 10-minute expiry, rate-limited issuance and verification
- Row-level security; every privileged read of a minor's record audit-logged
- Encryption at rest and in transit; field-level encryption for minors' PII
- Secrets in a managed vault; no long-lived credentials
- **Target NCA ECC** (KSA National Cybersecurity Authority) and ISO 27001
- Annual penetration test; dependency scanning in CI
- **[VERIFIED]** Immediate remediations carried over from V1: migrate off **end-of-life .NET 5**,
  disable `xmlrpc.php`, restrict `/wp-json/wp/v2/users`, remove the version `<meta generator>`

---

## 10. Reliability

| Target | Value |
|---|---|
| Availability | 99.9% (99.95% during session hours) |
| RPO | 15 minutes |
| RTO | 1 hour |
| Backups | Continuous WAL + daily snapshot, **restore tested quarterly** |

**Graceful degradation order** — shed in this sequence under load:
AI inference → recording → analytics ingest → reports → **live classes and tasmi' last**.
The daily halaqa is the product; everything else can wait.

---

## 11. Scaling path — do not build phase 4 on day one

| Stage | Students | Architecture |
|---|---:|---|
| Now **[VERIFIED]** | ~hundreds | Single ASP.NET app + WordPress |
| **Phase 1** | 5,000 | Modular monolith, managed Postgres, single region, LiveKit single cluster |
| **Phase 2** | 25,000 | Read replicas, Redis, extract media pipeline, mobile apps |
| **Phase 3** | 100,000 | Extract live classes + AI, ClickHouse, partitioning, multi-campus |
| **Phase 4** | 250,000+ | Multi-region residency, SFU cascading, per-region control plane |

**[INFERRED]** The academy is currently at low thousands at most. Building phase 4 now would
be a serious and expensive mistake. The architecture above is designed so each phase is a
natural extension of the last, not a rewrite.

---

## 12. Build vs buy

| Component | Decision | Why |
|---|---|---|
| Core platform | **Build** | The Quran-specific model is the product (`17` §1) |
| SFU / live classes | **Adopt** LiveKit self-hosted | Never write WebRTC infrastructure |
| Mushaf data & audio | **Adopt** QUL / quran-align | **[RESEARCHED]** already open and high quality |
| Speech/AI models | **Adopt then tune** | Building from scratch is unjustified |
| Notifications | **Adopt** (WhatsApp Business API, email provider) | Commodity |
| Analytics | **Adopt** self-hosted Plausible/Matomo + ClickHouse | Commodity |
| Payments *(if ever)* | **Adopt** Saudi rails (Mada, STC Pay) | Never build |
| Course authoring / SCORM | **Integrate via LTI if needed** | Do not compete (`17` §5) |

---

## 13. Assumptions register

Stated explicitly so they can be corrected rather than inherited silently.

| # | Assumption | Confidence | How to verify |
|---|---|---|---|
| 1 | Halaqat are 5–15 students | **[INFERRED]** High | Ask the academy |
| 2 | Peak load clusters on hour boundaries | **[INFERRED]** High | Server logs |
| 3 | Ramadan drives a 3–5× seasonal peak | **[INFERRED]** Medium | Historical data |
| 4 | Current scale is low thousands | **[INFERRED]** Medium | LMS admin figures |
| 5 | No payment processing is required | **[VERIFIED]** on public surface | Confirm with client |
| 6 | Live teaching runs on external video today | **[VERIFIED]** via FAQ text | Confirm which tool |
| 7 | Children's data must stay in KSA | **[RESEARCHED]** High | **Qualified legal review** |
| 8 | Maknoon requires institutional reporting | **[INFERRED]** Medium | Ask the association |

> Assumption 7 carries the largest architectural consequence — it selects the cloud provider
> and rules out several managed services. **It should be confirmed by a Saudi
> data-protection lawyer before procurement, not after.**
