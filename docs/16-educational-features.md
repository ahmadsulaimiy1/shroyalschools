# 16 — Educational Features

The pedagogy layer. This is where a Quran platform differs from a generic LMS, and where
**[VERIFIED]** V1 is entirely absent.

All designs are **[RECOMMENDED]** unless labelled otherwise.

---

## 1. Design principles

1. **The teacher is authoritative.** Software assists; it never certifies. No AI verdict
   overrides a qualified teacher, and no ijazah is ever issued on machine assessment.
2. **The word is the unit.** **[RESEARCHED]** leading tools mark errors at word level.
3. **Revision outranks new memorisation.** A student who memorises 5 pages a day and revises
   nothing has memorised nothing.
4. **The mushaf page is the interface.** Learners think in pages, lines and juz — not
   "modules" and "units". Generic LMS abstractions do not fit.
5. **Consistency beats intensity.** Track streaks and completion rates, not raw volume.

---

## 2. Quran memorisation (Hifz) ⭐ *the core system*

### 2.1 The three-tier model

**[RESEARCHED]** Every serious hifz institution runs Sabaq / Sabqi / Manzil.
**[VERIFIED]** V1 models none of them.

```
┌──────────── SABAQ (سبق) — new memorisation ────────────┐
│ Today's new portion. Small, precise, teacher-assigned. │
│ Graded in the daily tasmi'.                            │
└────────────────────────┬───────────────────────────────┘
                         ▼ once accepted
┌──────────── SABQI (سبقي) — recent revision ────────────┐
│ Roughly the last 7 days / current juz.                 │
│ Recited daily until stable.                            │
└────────────────────────┬───────────────────────────────┘
                         ▼ once stable
┌──────────── MANZIL (منزل) — consolidated revision ─────┐
│ Everything memorised, on a repeating cycle.            │
│ Scheduled by spaced repetition, weighted by weakness.  │
└────────────────────────────────────────────────────────┘
```

### 2.2 The revision scheduler

**[RESEARCHED]** Documented intervals: same day → 1 → 3 → 7 → 14 days, widening with strength.

**[RECOMMENDED]** Each memorised page carries a **strength score** (0–100) that:
- **rises** on a clean recitation
- **falls** sharply on errors, weighted by error type *(forgetting hurts more than hesitation)*
- **decays** with elapsed time since last recitation

The daily Manzil queue is simply *the lowest-strength pages due today*, capped at the
student's declared daily capacity — **[VERIFIED]** which V1 already collects as
`HefzDailyCount` (`ربع وجه` … `خمسة أوجه`) and then never uses. V2 finally puts that field to work.

**Ramadan mode:** an institution-wide schedule variant — reduced new memorisation, increased
revision — reflecting how these academies actually operate.

### 2.3 Progress representation
Juz map (30 cells, shaded by strength) · page-level heat map · % of Quran memorised ·
projected completion date from actual velocity vs the `HefzDuration` target declared at
signup · streak and consistency score.

---

## 3. Tajweed

**[RECOMMENDED]** A structured rule taxonomy — نون ساكنة وتنوين (إظهار، إدغام، إقلاب، إخفاء) ·
مدود · قلقلة · أحكام الراء واللام · مخارج الحروف · صفات الحروف · الوقف والابتداء.

Every error marked in tasmi' is tagged with its rule, producing a **per-student tajweed
profile**: "consistently weak on إخفاء; strong on مدود." That profile drives targeted drills
and gives the teacher something specific to teach.

Theory lessons with practical application, short rule-level assessments, and a tajweed
competency map per student.

---

## 4. Tilawah (recitation quality)

Distinct from memorisation — a student may recite from the mushaf without memorising.
Graded on **fluency · articulation (makhraj) · rhythm and pacing · voice control · waqf/ibtida**.

**[RECOMMENDED]** Reference-audio comparison: the student hears a qualified reciter for the
same range **[RESEARCHED]** (QUL provides audio with word-level timestamps), records their
own, and teacher and student can compare side by side.

---

## 5. Ijazah & sanad ⭐ *the institution's most valuable asset*

**[VERIFIED]** V1 advertises `منح الإجازات القرآنية بالسند المتصل` on track H11 and
Maknoon-accredited certificates — with no implementation.

**[RESEARCHED]** An ijazah's worth is its **sanad**: an unbroken chain of typically **28–32
named teachers** back to the Prophet ﷺ. **[RESEARCHED]** Typical pass mark 75%; typical
duration 6 months–2 years.

### The ijazah record
```
riwayah            e.g. حفص عن عاصم — or one of the عشر صغرى / عشر كبرى
type               full Quran · partial · tajweed · specific qira'ah
examiner           teacher, with their own verified ijazah on file
examination_date   Hijri + Gregorian
score              vs the institution's pass threshold
sanad_chain        ordered list of named teachers — the chain itself
verification_code  public, checkable at /verify/{code}
```

### Workflow
Teacher recommends → **supervisor verifies eligibility** → formal examination by a
**qualified examiner who is not the student's own teacher** → QA audits the sanad chain and
examiner credentials → certificate issued → publicly verifiable.

> Two rules to state plainly: **an examiner must hold their own ijazah in the same riwayah**,
> and **AI must play no part in ijazah assessment.** Oral transmission from a certified
> teacher *is* the sanad. Automating it would destroy the thing being certified.

---

## 6. Daily lesson tracking (تسميع)

The daily tasmi' is the heartbeat of a مقرأة.

**Teacher screen:** digital mushaf → student's assigned range → **tap any word to mark an
error** → classify (tajweed / makhraj / forgetting / hesitation / tashkeel / skipped) →
rate accuracy, tajweed, fluency, recall → optional voice note → accept or repeat the Sabaq.

**Every marked error persists**, feeding the tajweed profile (§3), the strength score (§2.2)
and the error-pattern report. **[RESEARCHED]** This word-level persistence is what
distinguishes the strongest tools from simple attendance logs.

---

## 7. Weekly assessment & monthly reports

**Weekly:** consolidation of the week's Sabaq, revision-queue health, attendance,
error trend vs previous week, teacher comment.

**Monthly:** a **parent-facing PDF** — juz map, pages memorised this month, attendance %,
tajweed profile, teacher's narrative comment, next month's target.
**[RESEARCHED]** Peer platforms send parents structured periodic reports; **[VERIFIED]**
V1's advantage #5 promises `متابعة وتقارير دورية` (regular follow-up and reports) with no
mechanism to produce them. This closes an existing promise.

---

## 8. Parent follow-up

Covered in `15` §3. Educationally, the parent needs three things: *is my child attending?*,
*is my child progressing?*, *what should I do at home?* — the last being the one most
platforms omit and the one that changes outcomes for young children.

**[RECOMMENDED]** Each monthly report ends with a concrete "how to help at home this month"
section written by the teacher.

---

## 9. Teacher evaluation

**[RESEARCHED]** Best practice pairs lesson observation with multiple evidence sources —
artefacts of practice, student/family feedback, and evidence of student learning.

**Composite teacher index:**
| Dimension | Source |
|---|---|
| Observation score | Supervisor rubric |
| Student progress velocity | Pages/juz per student per month |
| Grading consistency | QA calibration variance |
| Attendance-marking compliance | System |
| Grading turnaround | System |
| Parent satisfaction | Survey |
| Retention in their circles | System |

Used for development first, performance management second — and never published to students.

---

## 10. Student achievements

Juz completion badges · streak milestones · full-Quran completion (ختمة) · tajweed mastery ·
perfect-attendance months · revision consistency.
**[RESEARCHED]** `maqraa.sa` already runs a medals/badges system recognising hafiz achievement.

**Age-appropriate:** heavy gamification for the 3–12 tracks; restrained, dignified recognition
for adult and ijazah tracks. **[RECOMMENDED]** No competitive leaderboards between students —
inappropriate to the subject matter and demotivating for slower memorisers.

---

## 11. Attendance

Per-session status: present · late · absent excused · absent unexcused, with minutes attended.
Automatic guardian notification on absence *(same day)*.
**[VERIFIED]** V1's terms clause 4 already mandates *"إبلاغ المعلم أو إدارة المقرأة عند التغيب
بعذر مناسب"* — V2 implements the policy that already exists on paper.

Attendance is a **leading indicator**: **[RESEARCHED]** early-warning systems combining
attendance, performance and engagement cut dropout by up to ~35%.

---

## 12. Homework & audio submissions

Asynchronous practice between live sessions — **[RESEARCHED]** the pattern used by Hifz Focus
("asynchronous audio feedback").

Student records against a target range → uploads → teacher grades with the same word-level
tool → feedback returns with a voice note. Optional AI pre-screen (§16) highlights likely
errors first, so the teacher's time goes to judgement rather than detection.

**Critical for:** students in awkward timezones, missed sessions, and the over-40 and
special-needs tracks where pace varies widely.

---

## 13. Live online classes

**[VERIFIED]** V1's FAQ states teaching depends on `برامج الاتصال المرئي والصوتي` — external
video tools. The LMS administers; it does not host the classroom.

**[RECOMMENDED]** Bring sessions in-platform so attendance, tasmi' and recording are one flow:
in-app join · shared digital mushaf synchronised to the reciter · raise hand / recitation
queue · teacher mutes and calls students in turn *(exactly how a physical halaqa runs)* ·
low-bandwidth audio-only fallback · automatic attendance from join/leave events.

**Scale note:** a halaqa is **5–15 students**, not a lecture hall. See `18` §4 — this makes
the concurrency problem far easier than it first appears.

---

## 14. Recorded sessions

Recording is valuable for revision, QA sampling and dispute resolution — **and sensitive
because minors are on camera.**

**[RESEARCHED]** Safeguarding guidance: recording protocols must be proportionate to risk;
one-to-one unmonitored interactions should be eliminated.

**[RECOMMENDED] Rules:**
- Guardian consent required before any recording involving a minor
- Retention limited (e.g. 90 days) and enforced automatically
- **In-Kingdom storage** for minors' recordings (PDPL — see `18` §3)
- Access logged; QA sampling permitted; download restricted
- **No unrecorded one-to-one adult↔minor session** — either a second adult is present or the
  session is recorded

---

## 15. Digital Mushaf

The shared surface across student, teacher and live class.

**[RESEARCHED]** Open infrastructure exists: **QUL** provides word-by-word text, Uthmani and
IndoPak scripts, translations, tafsir, audio and **timestamp data usable to highlight words
as recitation plays**; `quran-align` provides word-accurate timestamps.

**Requirements:** Madinah Mushaf page layout (students memorise by page position — this is not
cosmetic) · word-level tap targets for error marking · synchronised audio highlighting ·
multiple reciters · tajweed colour-coding · adjustable size and high contrast *(the over-40
and special-needs tracks depend on this)* · **offline capability** · translations for the
non-Arabic tracks.

---

## 16. AI-assisted pronunciation feedback *(future-ready)*

**[RESEARCHED]** Tarteel (~15M users) does real-time word-level error flagging, skipped-word
and tashkeel detection, with visual highlighting and a reviewable error log.

### Phased, honest adoption

| Phase | Capability | Authority |
|---|---|---|
| 1 | **Practice pre-screen** — student self-checks before tasmi' | Advisory to student only |
| 2 | **Teacher assist** — likely errors pre-flagged on the grading screen | Teacher confirms/overrides |
| 3 | **Revision intelligence** — error patterns weight the revision queue | Suggestion only |
| 4 | **Placement support** — assist admissions level assessment | Human confirms |

### Guardrails — state these to the client
- AI output is **never** shown as a grade, and never reaches a parent as an assessment
- **No certificate or ijazah may involve AI assessment** (§5)
- Tajweed has legitimate scholarly variation; a model's confidence is not a fatwa
- Accuracy varies by age, accent and audio quality — **children and non-Arabic speakers,
  precisely this academy's growth segments, are the hardest cases**
- Voice data from minors is sensitive personal data: guardian consent, in-Kingdom processing,
  strict retention
- Ship it as clearly labelled assistance, or not at all

---

## 17. Feature summary

| # | Feature | V1 **[VERIFIED]** | V2 | Priority |
|---|---|:-:|:-:|:-:|
| 1 | Hifz three-tier model | ❌ | ⭐ Core | 🔴 |
| 2 | Revision scheduler | ❌ | ⭐ Core | 🔴 |
| 3 | Daily tasmi' + word-level marking | ❌ | ⭐ Core | 🔴 |
| 4 | Attendance | ❌ *(policy only)* | ✅ | 🔴 |
| 5 | Digital mushaf | ❌ | ⭐ Core | 🔴 |
| 6 | Parent reports | ❌ *(promised)* | ✅ | 🔴 |
| 7 | Tajweed rule tracking | ❌ | ✅ | 🟠 |
| 8 | Weekly/monthly assessment | ❌ | ✅ | 🟠 |
| 9 | Certificates + sanad | ❌ *(advertised)* | ✅ | 🟠 |
| 10 | Homework / audio submission | ❌ | ✅ | 🟠 |
| 11 | Teacher evaluation | ❌ | ✅ | 🟠 |
| 12 | Achievements | ❌ | ✅ | 🟡 |
| 13 | Live classes in-platform | ❌ *(external)* | ✅ | 🟡 |
| 14 | Recorded sessions | ❌ | ✅ | 🟡 |
| 15 | Tilawah assessment | ❌ | ✅ | 🟡 |
| 16 | AI pronunciation assist | ❌ | ✅ | 🟢 Later |
