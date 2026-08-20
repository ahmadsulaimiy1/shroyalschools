# 17 — International Standards & Gap Analysis

Compares the proposed platform against mainstream LMS products and formal edtech standards,
then identifies what would make it genuinely world-class rather than merely adequate.

---

## 1. Against mainstream LMS products

| Capability | Moodle | Canvas | Google Classroom | **V1 [VERIFIED]** | **V2 [RECOMMENDED]** |
|---|:-:|:-:|:-:|:-:|:-:|
| Course/content management | ●●● | ●●● | ●● | ○ | ●● |
| Assignments & grading | ●●● | ●●● | ●●● | ✗ | ●●● |
| Gradebook | ●●● | ●●● | ●● | ✗ | ●●● |
| Quizzes | ●●● | ●●● | ●● | ✗ | ●● |
| Attendance | ●● | ●● | ○ | ✗ | ●●● |
| Parent portal | ● | ●● | ●● | **✗** | ●●● |
| Live classes | ● | ●● | ●● | ✗ *(external)* | ●●● |
| Mobile apps | ●● | ●●● | ●●● | ✗ | ●●● |
| Analytics | ●● | ●●● | ● | **✗** | ●●● |
| Standards (LTI/SCORM/xAPI) | ●●● | ●●● | ● | ✗ | ●● |
| Multi-tenant / multi-campus | ●● | ●●● | ● | ✗ | ●●● |
| RTL & Arabic | ●● | ●● | ●● | ●●● | ●●● |
| **Hifz tracking** | ✗ | ✗ | ✗ | ✗ | ●●● |
| **Spaced revision** | ✗ | ✗ | ✗ | ✗ | ●●● |
| **Digital mushaf** | ✗ | ✗ | ✗ | ✗ | ●●● |
| **Tajweed profiling** | ✗ | ✗ | ✗ | ✗ | ●●● |
| **Ijazah & sanad** | ✗ | ✗ | ✗ | ✗ | ●●● |
| **Gender segregation** | ✗ | ✗ | ✗ | ●●● | ●●● |

### The strategic conclusion

The bottom six rows are the whole argument. **No mainstream LMS models hifz, revision, the
mushaf, tajweed or sanad** — and none ever will, because these are not general education
concepts.

Conversely, V2 should **not** try to out-Moodle Moodle on quizzes, SCORM packages or course
authoring. Those are commodity capabilities where competing is expensive and pointless.

> **Recommendation:** be the best *Quran* platform in the world, not a mediocre general LMS.
> Adopt standards (§2) so the commodity parts can interoperate with tools that already do
> them well, and spend the engineering budget on the six rows nobody else has.

---

## 2. Formal standards

**[RESEARCHED]** The current landscape: SCORM 2004 remains the most widely deployed despite
being frozen since 2009; LTI 1.3 + Advantage is the production standard for tool integration
(OAuth 2.0 + JWT); xAPI is the modern learning-data standard; QTI covers assessment
interchange; OneRoster handles roster/SIS integration.

| Standard | Adopt? | Rationale |
|---|:-:|---|
| **xAPI (Tin Can)** | ✅ **Yes** | The natural fit. Statements like *"student recited Al-Baqarah 1–5 with 2 tajweed errors"* are exactly what xAPI expresses and no other standard can. Build the event stream xAPI-shaped from day one. |
| **LTI 1.3 + Advantage** | ✅ Yes *(consumer)* | Lets the academy embed third-party tools without rebuilding them. |
| **OneRoster** | ⚠ If integrating schools | Valuable only for multi-campus/partner-school expansion. Defer. |
| **QTI** | ⚠ Partial | Useful for tajweed theory quizzes. Not for tasmi', which QTI cannot express. |
| **SCORM / cmi5** | ❌ Import only | Legacy course packages. Do not author in it. |
| **WCAG 2.1 AA** | ✅ **Mandatory** | Non-negotiable — see §3. |
| **ISO 27001 / NCA ECC** | ✅ Target | KSA National Cybersecurity Authority controls apply to a Saudi entity handling children's data. |

### An honest caveat
**[INFERRED]** None of these standards were designed for oral transmission, sanad, or
memorisation strength. xAPI is the only one flexible enough to carry Quran-specific verbs,
and it will need a **custom vocabulary** (`recited`, `revised`, `memorized`, `examined`,
`granted-ijazah`). Publishing that vocabulary openly would be a genuine contribution to the
field and a credible claim to leadership.

---

## 3. Accessibility

**[VERIFIED]** V1 fails WCAG 2.1 AA in at least eight identified ways: gold at 1.9:1
contrast, `*` as the sole error message, three unlabelled required fields, no
`prefers-reduced-motion`, headings empty until JS runs, unpausable marquee, modals without
focus management, and `dir="rtl" lang="ar"` on English/French/Italian pages.

This matters more here than for a typical platform for a specific reason: **[VERIFIED]** the
academy runs a dedicated **قسم ذوي الهمم** (special needs) track *and* a **قسم ما فوق الأربعين**
(over-40) track. Two of its seven segments are populated by exactly the users these defects
exclude.

**[RECOMMENDED]** WCAG 2.1 AA as a release gate, plus Quran-specific accessibility:
adjustable mushaf text size, high-contrast mushaf, screen-reader-correct Arabic with
diacritics, audio-first pathways for visually impaired students, and captioning for
deaf students in tajweed *theory* lessons.

---

## 4. Missing capabilities — what would make this world-class

Ranked by differentiation.

### Tier 1 — nobody does these well

| # | Capability | Why it wins |
|---|---|---|
| 1 | **Strength-scored revision engine** | Existing hifz apps log revision; none *schedule* it from a decaying per-page strength model tied to a teacher's error marks. |
| 2 | **Verifiable sanad registry** | A public `/verify/{code}` endpoint showing the full 28–32-teacher chain. **[RESEARCHED]** No platform offers this. It would make the academy's ijazahs the most credible online. |
| 3 | **Tajweed profile per student** | Errors tagged by rule, aggregated into a competency map that drives targeted drills. |
| 4 | **Teacher grading calibration** | QA measures whether teachers grade the same recitation the same way. Standard in serious assessment; absent from Quran platforms. |
| 5 | **Demand-driven capacity planning** | Waitlist depth tells the academy which circle to open next — **[VERIFIED]** exactly the intelligence V1 discards today. |

### Tier 2 — expected of a leading platform

| # | Capability |
|---|---|
| 6 | Native mobile apps (student, teacher, parent) — **[RESEARCHED]** peers ship three |
| 7 | Offline-first teacher grading |
| 8 | In-platform live classes with a synchronised shared mushaf |
| 9 | Automated monthly parent reports |
| 10 | Early-warning/at-risk detection |
| 11 | Multi-campus / multi-tenant operation |
| 12 | Public API for partner associations |

### Tier 3 — differentiators worth considering

| # | Capability | Note |
|---|---|---|
| 13 | **Sponsorship marketplace** | A donor funds a named student's place. Natural for a charitable academy; **[VERIFIED]** V1 references a Maknoon store but never links it. |
| 14 | **Alumni/hafiz registry** | Public, opt-in register of graduates — institutional credibility compounding over time. |
| 15 | **Teacher marketplace across associations** | Shared teacher pool between Quran associations — a network effect no single academy has. |
| 16 | **Ministry reporting automation** | **[RESEARCHED]** KSA Quran associations report into a national system; automating it is real operational value. |
| 17 | **Open Quran-education data standard** | Publish the xAPI vocabulary (§2) and let other academies adopt it. Leadership by contribution. |

---

## 5. What to deliberately *not* build

Saying no is part of the specification.

| Don't build | Why |
|---|---|
| A general course-authoring system | Moodle/Canvas do it better. Integrate via LTI if ever needed. |
| SCORM authoring | Obsolete for this use case. |
| A video conferencing platform | **[RESEARCHED]** use an SFU (LiveKit/mediasoup). Never write WebRTC infrastructure from scratch. |
| A payment platform | **[VERIFIED]** no evidence fees exist. Confirm the model first (`15` §6). |
| AI tajweed *certification* | Religiously and reputationally indefensible (`16` §16). |
| Social/community features | **[VERIFIED]** terms clause 3 explicitly forbids non-educational contact between members. Building a social layer would contradict the institution's own policy. |
| A custom mushaf renderer from scratch | **[RESEARCHED]** QUL and quran-align already provide text, audio and word timings. |

---

## 6. Scorecard — V2 against "world-class"

| Dimension | V1 | V2 target | Basis |
|---|:-:|:-:|---|
| Quran-specific pedagogy | 0/10 | **9/10** | Tiers 1–2 above; nothing comparable exists |
| General LMS capability | 1/10 | 6/10 | Deliberately capped — integrate rather than compete |
| Accessibility | 2/10 | 9/10 | WCAG 2.1 AA + Quran-specific provisions |
| Compliance (PDPL) | 0/10 | 9/10 | Guardian consent, in-Kingdom residency, minimisation |
| Scale readiness | 3/10 | 9/10 | `18-architecture.md` |
| Analytics | 0/10 | 8/10 | xAPI stream + product analytics |
| Mobile | 0/10 | 8/10 | Three native apps |
| Institutional credibility | 4/10 | 9/10 | Verifiable sanad registry |

**[INFERRED]** The realistic path to "one of the strongest online Quran academies in the
world" is not breadth — it is depth in the six capabilities no general LMS will ever build,
combined with compliance and accessibility rigour that most Quran platforms currently lack.
