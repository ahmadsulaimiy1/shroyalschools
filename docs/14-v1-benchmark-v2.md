# 14 — V1 Benchmark & V2 Design

Treats the existing platform as **Version 1**, scores it against the best practice in `13`,
and specifies **Version 2**.

**Evidence labels:** **[VERIFIED]** observed · **[INFERRED]** reasoned · **[RECOMMENDED]** proposed.

---

## 1. What V1 actually is

**[VERIFIED]** V1 is a competent **enrolment and circle-administration system**:
passwordless auth, 36 GUID-addressed tracks, capacity management with waitlist overflow,
7 UI locales, real-time notification plumbing (SignalR), and an admin console (SB Admin 2 +
Kendo UI).

**[VERIFIED]** What it is **not** is a *learning* platform. Nothing observable models
memorisation, revision, attendance, assessment or certification — the actual work of a
مقرأة. It gets students into circles and then stops.

**[INFERRED]** Some of this may exist behind the login. But two things are certain from the
public surface: the **registration form is the only place hifz intent is captured**
(`HefzDailyCount`, `HefzDuration`), and it is captured **once, at signup, and never revisited**.
A system that tracked memorisation would not need to ask.

---

## 2. Benchmark scorecard

Scored against the best practice established in `13`. **0** = absent · **1** = partial ·
**2** = adequate · **3** = best-in-class.

| # | Capability | V1 | Evidence | V2 target |
|---|---|:--:|---|:--:|
| 1 | Student onboarding | 1 | **[VERIFIED]** 13-field form, no placement, no trial | 3 |
| 2 | Teacher onboarding | 0 | **[VERIFIED]** Google Form → spreadsheet | 3 |
| 3 | Admin workflows | 2 | **[INFERRED]** SB Admin 2 console exists | 3 |
| 4 | **Parent experience** | **0** | **[VERIFIED]** No parent role. Enrols from age 3 | 3 |
| 5 | **Memorisation tracking** | **0** | **[VERIFIED]** No Sabaq/Sabqi/Manzil model | 3 |
| 6 | **Revision system** | **0** | **[VERIFIED]** No revision concept | 3 |
| 7 | Attendance | 0 | **[VERIFIED]** Required by terms, not implemented | 3 |
| 8 | Scheduling | 1 | **[VERIFIED]** Circles exist; **no timezone stored** | 3 |
| 9 | Assessment | 0 | **[VERIFIED]** No mechanism | 3 |
| 10 | Certificates / ijazah | 0 | **[VERIFIED]** Advertised, not implemented | 3 |
| 11 | Communication | 1 | **[VERIFIED]** SignalR exists; WhatsApp is the real channel | 3 |
| 12 | Dashboards | 1 | **[INFERRED]** Admin only | 3 |
| 13 | Reporting | 1 | **[INFERRED]** Kendo grids | 3 |
| 14 | **Analytics** | **0** | **[VERIFIED]** None on either host | 3 |
| 15 | Availability transparency | 0 | **[VERIFIED]** 61% dead-end | 3 |
| 16 | Accessibility | 1 | **[VERIFIED]** `*` errors, unlabelled fields, no reduced-motion | 3 |
| 17 | **PDPL compliance** | **0** | **[VERIFIED]** No guardian consent, no privacy policy, Google Forms | 3 |
| 18 | Security currency | 0 | **[VERIFIED]** **.NET 5 — end of life** | 3 |
| 19 | Mobile apps | 0 | **[VERIFIED]** None; peers ship three | 3 |
| 20 | AI assistance | 0 | **[VERIFIED]** None | 2 |

**Total: 11 / 60 (18%).**

The distribution matters more than the score. V1 scores reasonably on **administration**
(items 3, 8, 12, 13) and near-zero on **education** (5, 6, 7, 9, 10) — precisely the half
that makes it a Quran academy rather than a booking system.

---

## 3. The ten defining V1→V2 changes

### 3.1 Introduce the memorisation model 🔴
**V1 [VERIFIED]:** no representation of memorisation anywhere. `HefzDailyCount` is a
registration preference.
**Why:** **[RESEARCHED]** every serious institution runs Sabaq/Sabqi/Manzil.
**V2 [RECOMMENDED]:** first-class `MemorizationRecord`, `RevisionQueue` and `TasmiSession`
entities driving an automatic revision scheduler.
**Better because:** it turns a stated intention into a tracked, coachable, reportable
learning process — the reason the institution exists.

### 3.2 Add the parent/guardian role 🔴
**V1 [VERIFIED]:** none, while enrolling children from age 3.
**Why:** **[RESEARCHED]** PDPL requires guardian consent; peers give parents their own login.
**V2 [RECOMMENDED]:** full Parent Portal (`15` §3), guardian consent capture, guardian-
mediated communication.
**Better because:** it closes a legal exposure and activates the person who actually drives
a child's consistency.

### 3.3 Publish live availability 🔴
**V1 [VERIFIED]:** 22 of 36 entry points closed, none marked.
**Why:** **[VERIFIED]** `maqraa.sa` already does this.
**V2 [RECOMMENDED]:** availability API + per-track badges + inline waitlist with email.
**Better because:** it recovers the 61% of demand currently discarded.

### 3.4 Word-level tasmi' capture 🔴
**V1 [VERIFIED]:** no assessment capture.
**Why:** **[RESEARCHED]** QuranTrack, Hifz Focus and Tarteel all mark at word level.
**V2 [RECOMMENDED]:** teacher taps the erroneous word in a digital mushaf; error type
classified; patterns aggregate over time.
**Better because:** "you made 4 mistakes" is a grade; "you consistently miss madd at
these 7 words" is teaching.

### 3.5 Attendance that triggers action 🔴
**V1 [VERIFIED]:** terms clause 4 mandates it; nothing implements it.
**V2 [RECOMMENDED]:** per-session marking, automatic guardian notification, attendance
feeding an at-risk score.
**Better because:** **[RESEARCHED]** early-warning systems cut dropout by up to ~35%.

### 3.6 Real certificates with verifiable sanad 🟠
**V1 [VERIFIED]:** Maknoon-accredited certificates and connected-sanad ijazah are
advertised; no issuance or verification exists.
**Why:** **[RESEARCHED]** an ijazah's value is its chain of 28–32 named teachers.
**V2 [RECOMMENDED]:** certificate records storing riwayah, examiner and full sanad, with a
public verification URL.
**Better because:** an unverifiable ijazah is worth little; a verifiable one is the
institution's most durable asset.

### 3.7 Replace `*` with real validation 🟠
**V1 [VERIFIED]:** every required field errors with `data-val-required="*"`; three required
fields have **no label at all**.
**V2 [RECOMMENDED]:** specific localised messages, labels on every field, `aria-describedby`.
**Better because:** it is simultaneously a completion-rate fix and a WCAG 1.3.1/4.1.2 fix.

### 3.8 Consolidate every entry point 🟠
**V1 [VERIFIED]:** 7 Google Forms outside the platform — contradicting the platform's own
terms clause 2 (*"no registration outside the platform is recognised"*), and sending
children's data offshore against PDPL expectations.
**V2 [RECOMMENDED]:** all registration and recruitment in-platform.

### 3.9 Instrument everything 🟠
**V1 [VERIFIED]:** no analytics on either host. Nothing is measurable.
**V2 [RECOMMENDED]:** privacy-respecting product analytics + a learning-analytics event
stream (xAPI-shaped).
**Better because:** without it, none of the above can be proven to have worked.

### 3.10 Modernise the runtime 🔴
**V1 [VERIFIED]:** .NET 5 — **end of support since May 2022**.
**V2 [RECOMMENDED]:** current .NET LTS, in-Kingdom hosting (`18` §3).
**Better because:** unsupported software processing children's data is an unacceptable
standing risk regardless of features.

---

## 4. What V2 must keep

Not everything needs replacing. These V1 decisions are **[VERIFIED]** sound:

| Keep | Why |
|---|---|
| **Passwordless email+code auth** | Excellent fit for 3-year-olds' guardians, 60-year-old beginners, and low-digital-literacy users. No password resets, no credential reuse. |
| **GUID-addressed tracks** | Non-enumerable public identifiers — good practice. *(Fix the closed-track route that leaks the integer.)* |
| **Capacity + waitlist overflow** | The mechanism is right; only the data captured is wrong. |
| **The age/gender track taxonomy** | 7 bands from 3 to 40+, plus special-needs and ijazah tracks. This is the academy's core IP. |
| **Gender segregation** | A product requirement, correctly modelled at the track level. |
| **Real-time infrastructure (SignalR)** | Already present; V2 has far more to send through it. |
| **Multi-locale from the start** | 7 locales is ahead of most peers. |
| **The smart registration router concept** | Genuinely good UX thinking. Rebuild the mechanics, keep the idea. |

---

## 5. V2 in one paragraph

**[RECOMMENDED]** V2 keeps V1's enrolment engine and adds the learning platform that was
never built: a Sabaq/Sabqi/Manzil memorisation model with an automatic revision scheduler;
word-level tasmi' capture on a digital mushaf; attendance that triggers guardian notification
and at-risk intervention; layered assessment ending in a verifiable ijazah with recorded
sanad; eleven role-specific portals including the parent portal V1 lacks entirely; honest
published availability; in-Kingdom hosting with guardian consent to meet PDPL; and AI that
pre-screens practice recitation to make the teacher's time count for more — while never
certifying anything itself.
