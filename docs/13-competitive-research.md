# 13 — Competitive & Best-Practice Research

Research into leading Quran academies and Quran-tech products across Saudi Arabia, the GCC
and internationally, plus mainstream edtech, to establish what "best in class" means before
designing V2.

**Method:** desk research of live platforms and published documentation, August 2026.
No platform is copied; the goal is the *pattern shared by the strongest institutions*.

**Evidence labelling used throughout Phase 2:**
- **[VERIFIED]** — observed directly on a live system
- **[RESEARCHED]** — documented by a named third-party source
- **[INFERRED]** — reasoned conclusion, not observed
- **[RECOMMENDED]** — our design proposal

---

## 1. Platforms studied

### Saudi / GCC institutional

| Platform | Relevance |
|---|---|
| **جمعية مكنون** (`maknon.org.sa`) | **The client's own parent association.** Runs its own electronic maqra'at. |
| **الجمعية الخيرية الإلكترونية لتحفيظ القرآن** (`maqraa.sa`) | Self-described first electronic Quran charity, KSA licence #3298. The closest true peer. |
| **مقرأة الحرمين** (`maqraa.prh.gov.sa`) | Haramain circles; governance and QA framework for circle performance. |
| **نظام إدارة جمعيات تحفيظ القرآن** (Ministry of Islamic Affairs) | The official registry all KSA Quran associations report into. |
| **إنجازي** (`injaazy.com`) | Commercial circle-management system — separate teacher, student and parent apps. |
| **راصد**, **حلقات**, **تحفيظ** | KSA circle-management products; attendance and record keeping. |

### Quran-technology

| Product | Relevance |
|---|---|
| **Tarteel AI** | ~15M users. Real-time word-level error detection during recitation. |
| **Quranic Universal Library (QUL)** | Open Quran data: word-by-word text, audio, **timestamps**. |
| **QuranRecord**, **MyHifz**, **QuranTrack**, **Hifz Tracker**, **Hifz Focus** | Hifz-tracking apps — the pattern source for word-level marking and revision logs. |

### Mainstream edtech benchmarks
Moodle, Canvas, Google Classroom, Quality Matters, NIET/Danielson observation rubrics,
IMS Global standards (LTI 1.3, xAPI, QTI, OneRoster).

---

## 2. The single most important domain concept

> Every serious hifz institution organises memorisation around **three tiers**, not one.
> The existing platform models **none** of them. This is the central finding of Phase 2.

**[RESEARCHED]** The traditional structure:

| Tier | Arabic | What it is | Typical cadence |
|---|---|---|---|
| **Sabaq** | سبق | New memorisation | Today's new portion |
| **Sabqi** | سبقي | Recent revision | Last ~7 days / current juz |
| **Manzil** *(a.k.a. Dhor)* | منزل / دور | Consolidated revision | Everything memorised, on a cycle |

**[RESEARCHED]** This three-tier structure "maps almost perfectly onto what modern memory
science calls spaced repetition." Documented review intervals: same day → 1 day → 3 days →
7 days → 14 days, widening as strength grows.

**[RECOMMENDED]** V2 must treat Sabaq / Sabqi / Manzil as **first-class entities** with an
automated scheduler, not as free-text notes. This single change is the difference between a
booking system and a Quran learning platform. Full design in `16-educational-features.md` §2.

**[VERIFIED]** The existing platform captures `HefzDailyCount` and `HefzDuration` at
*registration only* — a stated intention, never tracked, never compared against actual
progress, and never used to schedule revision.

---

## 3. Best practices by domain

### 3.1 Student onboarding

**[RESEARCHED]** Strong institutions run **placement before enrolment** — a short recitation
assessment determines level rather than relying on self-declaration. `maqraa.sa`
**[VERIFIED]** publishes per-circle registration status (`تسجيل متاح` vs full) directly in its
catalogue, so a student never pursues a closed circle.

| Best practice | V1 status |
|---|---|
| Placement/level assessment before enrolment | ❌ Absent — self-declared only |
| Per-circle availability shown before commitment | ❌ Absent — **this is the 61% dead-end** |
| Trial session before commitment | ❌ Absent |
| Guardian onboarding alongside child | ❌ Absent |
| Orientation to the platform | ❌ Absent |
| Waitlist with reopening notification | ⚠ Waitlist exists but captures no email |

> `maqraa.sa` — a directly comparable Saudi charity — already does the availability display
> the client is missing. This is table stakes among peers, not an advanced feature.

### 3.2 Teacher onboarding

**[RESEARCHED]** Mature academies verify **ijazah and sanad** before hiring, run a
demo/probation lesson, and require child-protection training where minors are taught.

| Best practice | V1 status |
|---|---|
| Ijazah/sanad verification with documentation | ❌ Google Form only |
| Demo lesson / teaching assessment | ❌ Absent |
| Safeguarding training + acknowledgement | ❌ Absent |
| Probation period with supervisor review | ❌ Absent |
| Teacher profile visible to students/parents | ❌ No teacher profiles exist anywhere |

### 3.3 Memorisation tracking

**[RESEARCHED]** The strongest tools mark errors at **word level**, not lesson level.
QuranTrack lets teachers "mark mistakes at the word level to track improvement over time";
Hifz Focus offers "word-level error marking and asynchronous audio feedback"; Tarteel
"flags word-level errors, skipped words, or incorrect tashkeel."

**[RESEARCHED]** QuranRecord tracks recitation "in such detail that even a single missing
ayah triggers an alert to school management."

| Best practice | V1 status |
|---|---|
| Word-level error capture | ❌ Absent |
| Error-pattern analysis over time | ❌ Absent |
| Structured rating (tajweed / fluency / accuracy / recall) | ❌ Absent |
| Progress by juz / page / surah | ❌ Absent |
| Quarter-page granularity | ⚠ Offered at registration (`ربع وجه`), never tracked |

### 3.4 Revision systems
Covered in §2. **[RESEARCHED]** Best practice is an **automatic revision queue** generated
from what the student has memorised and when they last recited it. V1 has no revision
concept at all.

### 3.5 Attendance
**[RESEARCHED]** Per-session marking with excused/unexcused distinction, automatic guardian
notification on absence, and attendance feeding an at-risk score.

**[VERIFIED]** V1's terms clause 4 *requires* attendance discipline and absence notification
— so the policy exists, but no system implements it. Policy without mechanism.

### 3.6 Scheduling
**[RESEARCHED]** `maqraa.sa` runs circles of 1–4 hours daily segmented by gender and age.
Best practice: timezone-aware scheduling, teacher availability windows, substitute cover,
Hijri + Gregorian calendars, and Ramadan/Eid schedule variants.

**[VERIFIED]** V1 stores no timezone anywhere, despite serving students across KSA, Europe,
Africa and South Asia.

### 3.7 Assessment
**[RESEARCHED]** Layered: daily tasmi' → weekly consolidation → monthly/juz examination by a
second examiner → final ijazah test. **[RESEARCHED]** Typical ijazah pass mark is **75%**.

### 3.8 Certificates & ijazah
**[RESEARCHED]** An ijazah's value *is* its **sanad** — an unbroken chain of typically
**28–32 named teachers** back to the Prophet ﷺ. Best practice records the full chain, the
riwayah (e.g. Hafs 'an 'Asim), the examiner, and issues a **publicly verifiable** certificate.

**[VERIFIED]** V1 advertises Maknoon-accredited certificates and ijazah with connected sanad
(track H11) but exposes no issuance, storage or verification mechanism.

### 3.9 Communication
**[RESEARCHED]** Announcements, teacher↔guardian threads, and automated notifications —
**with all messaging logged and auditable** where minors are involved.

**[VERIFIED]** V1 terms clause 3 explicitly forbids private non-educational contact between
members. **[RECOMMENDED]** V2 must *enforce* this in software: no unlogged private channels,
and — per PDPL, §5 below — no direct adult↔minor channel at all.

### 3.10 Dashboards & reporting
**[RESEARCHED]** Role-specific dashboards (`injaazy` ships **separate teacher, student and
parent apps**); institution-level reporting for the parent association.

**[VERIFIED]** V1 uses SB Admin 2 and Kendo UI, so an admin dashboard exists — but no
student, teacher or parent dashboard is reachable, and **no analytics exist on either host**.

### 3.11 Parent experience
**[RESEARCHED]** Parents get progress visibility, absence alerts, teacher contact and
monthly reports. QuranRecord gives "each teacher, parent and management their own login."

**[VERIFIED]** V1 has **no parent role at all**, while enrolling children **from age 3**.
This is the most serious structural gap identified across both phases.

### 3.12 Retention & early warning
**[RESEARCHED]** Predictive early-warning systems combining attendance, performance and
engagement reduce dropout by up to ~35%, flagging risk up to 12 weeks before disengagement.
**[RECOMMENDED]** For hifz the leading indicators are missed tasmi' sessions, rising error
counts, and a growing revision backlog.

---

## 4. AI in Quran learning — the state of the art

**[RESEARCHED]** Tarteel AI (~15M users) provides real-time recitation feedback: word-level
error flagging, skipped-word and tashkeel detection, visual highlighting on the Quranic text,
a reviewable error log, and voice search.

**[RESEARCHED]** Open infrastructure exists to build on: **QUL** (word-by-word text, audio,
timestamps) and `quran-align` (word-accurate timestamps for Quranic audio).

**[RECOMMENDED]** Position AI as **teacher augmentation, never replacement**:
- Pre-screen a student's practice recitation so the live tasmi' focuses on real weaknesses
- Suggest — never assign — an error-informed revision queue
- Flag likely errors for teacher confirmation; **the teacher's judgement is authoritative**

> **A caution to state to the client:** tajweed correctness is a religious matter with
> scholarly nuance. An AI verdict must never be presented as authoritative, and no
> certificate or ijazah may ever be issued on AI assessment. Ijazah requires oral
> transmission from a certified teacher — that is the entire point of a sanad, and no
> technology substitutes for it.

---

## 5. 🚨 Regulatory findings — Saudi PDPL

**[RESEARCHED]** Saudi Arabia's Personal Data Protection Law (in force 14 Sep 2023, full
compliance required by 14 Sep 2024) imposes specific obligations for children's data:

- **Guardian consent is mandatory** for processing a child's personal data
- **Data sovereignty** — children's data is expected to remain **inside Saudi Arabia**
- **Restrictions on cross-border transfer**
- **Prohibition of direct communication with minors**
- **Data minimisation** — collection limited to what is essential
- **Penalties** — fines up to **SAR 5 million**, and imprisonment for malicious disclosure

### How V1 measures up

| PDPL requirement | V1 status **[VERIFIED]** |
|---|---|
| Guardian consent for children | ❌ **No guardian field on any form.** Enrols from age 3. |
| Children's data kept in KSA | ⚠ **Registrations flow through Google Forms** — data leaves the Kingdom |
| Cross-border transfer restricted | ⚠ Google Forms, Google Drive, Google Fonts, Cloudflare |
| No direct communication with minors | ⚠ No enforcement mechanism observed |
| Data minimisation | ❌ Router collects a phone number it never uses |
| Privacy policy published | ❌ **None exists on the site** |

**[INFERRED]** On the face of the public evidence, the current arrangement appears to sit
outside several PDPL requirements. **We are not lawyers and this is not legal advice** — but
the gap is wide enough that the client should obtain a qualified Saudi data-protection review
before, not after, the rebuild. It also directly constrains the architecture: see
`18-architecture.md` §3 on in-Kingdom hosting.

---

## 6. Cross-cutting patterns among the strongest institutions

1. **Three-tier memorisation is the data model** — not an afterthought.
2. **Word-level granularity** — the unit of feedback is the word, not the lesson.
3. **Availability is published honestly** — peers show open/full before you commit.
4. **Parents are first-class users** — not an afterthought, and legally required for minors.
5. **The sanad is the product** for ijazah tracks — record and verify the chain.
6. **Separate apps per role** — students, teachers and parents need different tools.
7. **Attendance drives intervention** — it is a leading indicator, not just a register.
8. **Teachers are quality-assured** — observation rubrics, not just recruitment.
9. **AI augments the teacher** — and never certifies.
10. **Institutional reporting** — the parent association needs its own view.

---

## Sources

- [Tarteel AI — Quran memorisation](https://apps.apple.com/us/app/tarteel-ai-quran-memorization/id1391009396) · [Spaced repetition for hifz](https://tarteel.ai/blog/unlocking-quran-memorization-with-spaced-repetition-a-powerful-tool-for-lasting-retention/)
- [Quranic Universal Library (QUL)](https://qul.tarteel.ai/) · [quran-align](https://github.com/cpfair/quran-align) · [Quran.com developers](https://quran.com/developers)
- [Muraja'ah: the complete Quran revision guide](https://ilmify.app/blog/what-is-murajaah-quran-revision/) · [Ijazah and Sanad explained](https://ilmify.app/blog/ijazah-and-sanad-the-quranic-certification-system-explained/)
- [Quran Ijazah online: process, cost & timeline](https://rahmanschool.com/quran-ijazah-online/) · [Sanad/Isnaad certification](https://www.maturidi.co.uk/certification-isnaad)
- [الجمعية الخيرية الإلكترونية لتحفيظ القرآن (maqraa.sa)](https://maqraa.sa/) · [جمعية مكنون](https://maknon.org.sa/) · [مقرأة الحرمين](https://maqraa.prh.gov.sa/ar)
- [نظام إدارة جمعيات تحفيظ القرآن — وزارة الشؤون الإسلامية](https://moia.gov.sa/Systems/QuranAssociations/Pages/default.aspx) · [إنجازي](https://injaazy.com/) · [راصد](https://rased.qz.org.sa/) · [حلقات](https://halqaat.com/)
- [QuranRecord](https://www.quranrecord.com/en/) · [MyHifz](https://myhifz.com/) · [QuranTrack](https://hamzas.world/apps/quran-track/index.html) · [Hifz Tracker](https://hifztracker.com/) · [Hifz Focus](https://hifz.iqs.org.in/)
- [Saudi PDPL overview](https://usercentrics.com/knowledge-hub/saudi-arabia-personal-data-protection-law-pdpl/) · [Data processing rules for children](https://www.lexismiddleeast.com/pn/SaudiArabia/Personal_Data_Processing_Rules_for_Children_and_Incapacitated_Individuals/en) · [DLA Piper — Saudi Arabia](https://www.dlapiperdataprotection.com/?c=SA)
- [Safeguarding for digital & online schools (CIS)](https://www.cois.org/about-cis/perspectives-blog/blog-post/~board/perspectives-blog/post/12-safeguarding-considerations-for-digital-online-schools) · [Safeguarding for online teaching](https://schoolsweek.co.uk/what-schools-need-to-know-about-safeguarding-while-teaching-remotely/)
- [eLearning standards: SCORM, xAPI, cmi5, LTI, OneRoster](https://aristeksystems.com/blog/elearning-standards/) · [OneRoster vs Ed-Fi vs LTI Advantage](https://notixit.com/blog/edtech-oneroster-edfi-lti-interoperability)
- [Quality Matters rubrics & standards](https://www.qualitymatters.org/qa-resources/rubric-standards) · [NIET rubric and observation systems](https://www.niet.org/our-work/our-services/show/rubric-and-observation-systems) · [Peer observation tool for online teaching](https://link.springer.com/article/10.1007/s11423-024-10428-z)
- [Early warning system for online dropout](https://link.springer.com/article/10.1186/s41239-022-00371-5) · [AI student retention analytics](https://www.questionpro.com/blog/ai-student-retention-analytics-2026)
- [WebRTC architecture guide 2026](https://www.forasoft.com/blog/webrtc-architecture-guide-for-business-2026) · [SFU comparison](https://www.forasoft.com/learn/video-streaming/articles-streaming/sfu-comparison-mediasoup-janus-livekit-pion) · [LiveKit SFU](https://docs.livekit.io/reference/internals/livekit-sfu/)
- [Saudi cloud regions](https://vision2030.ai/sectors/technology/saudi-arabia-cloud-regions/) · [Azure Saudi Arabia East Q4 2026](https://www.datacenterdynamics.com/en/news/microsoft-to-launch-saudi-arabia-east-region-in-q4-2026/)
