# 15 — Portal Specifications

Eleven portals. Each specifies navigation, permissions, workflows, dashboards, reports,
notifications and integrations.

**Everything here is [RECOMMENDED]** — a V2 design. Where V1 has a counterpart it is marked
**[VERIFIED]**; otherwise the portal does not exist today.

---

## 0. Cross-portal foundations

### Role model

| Role | Scope | V1 status |
|---|---|---|
| Student | Own data | **[VERIFIED]** exists |
| Parent/Guardian | Linked children | ❌ **absent** |
| Teacher | Assigned circles | **[VERIFIED]** recruited via Google Form |
| Supervisor | Assigned teachers/circles | **[VERIFIED]** recruited via Google Form |
| QA Reviewer | Cross-cutting, read-mostly | ❌ absent |
| Admissions Officer | Applicants, waitlists | ❌ absent |
| Finance Officer | Donations, stipends | ❌ absent |
| Support Agent | Tickets, impersonation-with-consent | ❌ absent |
| Content Manager | Curriculum, CMS | ❌ absent |
| Executive | Read-only aggregates | ❌ absent |
| System Administrator | Platform config | **[VERIFIED]** SB Admin 2 |

### Permission model
RBAC + scope, enforced server-side. Format `resource:action:scope` —
e.g. `tasmi:grade:own_circles`, `student:read:linked_children`.

**Non-negotiable rules:**
1. **No adult↔minor direct channel.** All communication about a minor routes through their
   guardian and is logged. *(PDPL: prohibition of direct communication with minors.)*
2. **Gender segregation enforced at data level** — a male teacher cannot be assigned to, or
   view rosters of, a female circle.
3. **Every privileged read of a minor's record is audit-logged.**
4. **Support impersonation requires explicit, logged, time-boxed consent.**

### Shared conventions
RTL-first, 8 locales · Hijri + Gregorian dates everywhere · timezone-aware · WCAG 2.1 AA ·
mobile-first · offline-tolerant for teachers on poor connections.

---

## 1. Student Portal

**Navigation:** Today · My Hifz · Revision · Sessions · Progress · Achievements · Mushaf ·
Messages · Certificates · Profile

**Permissions:** `own:*` only. Minors get a reduced set: no free-text messaging, no profile
photo, no public visibility.

### Dashboard — "Today"
The single screen that answers *what do I do now?*
- **Sabaq** — today's new portion, with target
- **Sabqi** — recent revision due
- **Manzil** — consolidated revision due today
- Next live session + join button (with countdown)
- Streak, current juz, % of Quran memorised
- Outstanding homework / audio submission

### Key workflows
| Workflow | Steps |
|---|---|
| Daily tasmi' | See assignment → practise (optional AI pre-check) → join session → recite → receive word-level feedback → view updated revision queue |
| Audio submission | Record against a target range → submit → teacher grades asynchronously → feedback returned |
| Revision | Open queue (ordered by spaced-repetition priority) → recite → mark confidence → queue recomputes |
| Absence | Request excusal with reason → guardian and teacher notified |

**Reports:** weekly progress, monthly summary, error-pattern report, attendance record,
juz completion map.

**Notifications:** session starting (15 min / 5 min), tasmi' graded, revision overdue,
achievement unlocked, certificate issued, schedule change.

**Integrations:** live class (SFU), digital mushaf + recitation audio (QUL), calendar
(`.ics`), push (mobile), WhatsApp opt-in for reminders.

---

## 2. Teacher Portal

**Navigation:** Today · My Circles · Tasmi' · Attendance · Students · Assessments ·
Materials · Messages · Availability · My Performance

**Permissions:** `*:*:own_circles`. **Cannot** self-assign circles, alter capacity, issue
certificates, or view students outside their circles. Gender-matched circles only.

### Dashboard
Today's sessions with one-tap start · students awaiting grading · attendance not yet marked ·
at-risk students in my circles · pending audio submissions.

### The tasmi' grading screen ⭐ *the most important screen in the platform*
- Digital mushaf showing the student's assigned range
- **Tap any word to mark an error**; classify: tajweed / pronunciation (makhraj) /
  forgetting / hesitation / tashkeel / skipped
- Per-dimension rating: **accuracy · tajweed · fluency · recall**
- Voice note attachment for nuanced correction
- Auto-computed suggestion for the next Sabaq
- **AI pre-screen results shown as suggestions only — teacher confirms or overrides**

### Key workflows
Mark attendance (bulk, one tap per student) · grade tasmi' · assign homework · grade audio
submissions · request substitute cover · escalate a struggling student to supervisor ·
recommend a student for juz examination.

**Reports:** circle progress, per-student trajectory, attendance summary, my grading turnaround.

**Notifications:** session reminder, student absent, new audio submission, supervisor
feedback, substitution request.

**Integrations:** live class, mushaf, offline-capable grading (syncs when reconnected).

---

## 3. Parent Portal 🔴 *entirely new — legally required*

> **[VERIFIED]** V1 has no parent role while enrolling children **from age 3**.
> **[RESEARCHED]** PDPL requires guardian consent for children's data.
> This portal is not a feature request; it is a compliance requirement.

**Navigation:** My Children · Progress · Attendance · Reports · Teacher Contact ·
Schedule · Consent & Privacy · Payments

**Permissions:** `read` on linked children + `consent:manage`. Cannot alter academic records.
Link established at enrolment and verified.

### Dashboard (per child)
Memorisation progress (juz map) · attendance this month · last teacher comment ·
next session · flags needing attention.

### Key workflows
| Workflow | Notes |
|---|---|
| Grant/withdraw consent | Versioned, timestamped, IP-logged — the PDPL basis for processing |
| Report absence | Before the session; teacher notified |
| Contact teacher | **The only sanctioned adult↔minor-adjacent channel — logged and auditable** |
| Review monthly report | Delivered by email + in-app |
| Approve level change | Guardian sign-off on track transfer |

**Reports:** monthly progress report (PDF, shareable), attendance record, certificates earned.

**Notifications:** child absent *(same day)*, monthly report ready, teacher comment,
certificate issued, schedule change, consent renewal due.

**Integrations:** email, WhatsApp Business API (opt-in), calendar, payments (if enabled).

---

## 4. Supervisor Portal

**Navigation:** Overview · My Teachers · Circles · Observations · Escalations ·
At-Risk Students · Reports

**Permissions:** `read:assigned_scope`, `observation:write`, `escalation:manage`.
Gender-matched. Cannot issue certificates or alter finance.

### Dashboard
Teacher performance grid (attendance-marking compliance, grading turnaround, student
progress velocity, parent satisfaction) · circles below target · overdue observations ·
open escalations · at-risk students across scope.

### Key workflows
Schedule and conduct lesson observation against a rubric **[RESEARCHED]** *(Danielson /
NIET / Quality Matters adapted for Quran instruction)* · review teacher grading consistency ·
handle escalations · approve substitutions · recommend teacher development · sign off juz
examinations.

**Reports:** teacher evaluation summary, circle health, observation history, intervention
outcomes.

**Notifications:** observation due, escalation raised, teacher below threshold, circle
at-risk.

---

## 5. Quality Assurance Portal

**Navigation:** QA Dashboard · Grading Calibration · Session Audits · Certificate Audit ·
Complaints · Standards · Reports

**Permissions:** `read:*` (broad, audited) + `qa:*`. **No write access to academic records** —
QA observes and reports, it does not grade.

### Dashboard
Grading consistency across teachers *(is Teacher A systematically more lenient than
Teacher B on the same material?)* · session recording audit sample · certificate issuance
audit · complaint themes · safeguarding flags.

### Key workflows
| Workflow | Purpose |
|---|---|
| Grading calibration | Multiple teachers grade the same recitation sample; variance measured and addressed |
| Session audit | Sample recordings reviewed against teaching standards |
| **Certificate/ijazah audit** | Verify sanad chain completeness and examiner qualification **before** issuance |
| Complaint investigation | Structured, with outcome tracking |
| **Safeguarding review** | Flagged interactions, policy adherence |

**Reports:** quality scorecard by teacher/circle/region, calibration variance, audit
findings, complaint trends, safeguarding incident log.

> The **certificate audit** matters most. **[VERIFIED]** the academy advertises
> Maknoon-accredited certificates and connected-sanad ijazah. If those are ever
> issued incorrectly, the institution's credibility — its entire asset — is damaged.

---

## 6. Finance Portal

> **[VERIFIED]** No payment gateway, cart, checkout or price list exists anywhere on V1.
> **[VERIFIED]** The only pricing statement on the site is `بأسعار رمزية` (nominal prices),
> inside a scrolling marquee. **[INFERRED]** the academy is free or funded charitably.
>
> **This portal is therefore specified as optional and must be confirmed with the client
> before any build.** Do not assume a fee model exists.

**Navigation:** Overview · Donations · Sponsorships · Teacher Stipends · Fees *(if enabled)* ·
Invoices · Reconciliation · Reports

**Permissions:** `finance:*`. Strictly segregated from academic data — finance sees
identities and amounts, not memorisation records.

### Dashboard
Donations this period vs target · active sponsorships · stipends due · cost per student ·
outstanding fees *(if enabled)*.

### Key workflows
Record and receipt donations *(terms clause 6 **[VERIFIED]** references a Maknoon store but
provides **no link** — wire this properly)* · **student sponsorship** (a donor funds a named
student or circle — a natural fit for a charitable Quran academy) · teacher stipend runs ·
Zakat-eligible fund tracking · reconciliation.

**Reports:** income/expenditure, donor statements, sponsorship impact reports, stipend
register, association-facing financial summary.

**Integrations:** Saudi payment rails (Mada, STC Pay, Apple Pay), bank reconciliation,
accounting export, Maknoon store.

---

## 7. Admissions Portal

**Navigation:** Applications · Placement · Waitlists · Capacity · Cohorts · Intake Reports

**Permissions:** `admission:*`, `student:create`, `waitlist:*`. Cannot grade or issue
certificates.

### Dashboard ⭐ *directly addresses the 61% dead-end*
Open vs closed tracks with places remaining · **waitlist depth per track** ·
conversion funnel by stage · demand heat map by country/language/age ·
**demand for closed tracks** *(the signal that tells the academy which circle to open next)*.

### Key workflows
| Workflow | Notes |
|---|---|
| Process application | Review → placement assessment → offer → enrol |
| **Placement assessment** | **[RESEARCHED]** short recitation assessment sets level — replaces V1's self-declaration |
| **Waitlist management** | Notify on reopening with a **time-boxed priority window** |
| Capacity planning | Open new circles where waitlist depth justifies a teacher |
| Cohort formation | Group by level, timezone and age |
| Transfer | Move a student between circles/tracks with guardian approval |

**Reports:** intake funnel, waitlist ageing, source attribution *(fixes V1's free-text
`AcademicAdvertiseWay`)*, demand-vs-capacity gap, conversion by locale.

**Notifications:** new application, **track reopened → notify waitlist**, capacity threshold
reached, placement assessment due.

> **[VERIFIED]** V1's waitlist captures only name + WhatsApp. This portal is useless without
> the email field added in `10-database-inference.md` §2.

---

## 8. Customer Support Portal

**Navigation:** Tickets · Live Chat · Knowledge Base · User Lookup · Escalations · SLA

**Permissions:** `ticket:*`, `user:read:limited`, `impersonate:with_consent`.
**Impersonation is time-boxed, consented and fully audit-logged.** No access to grading.

### Dashboard
Open tickets by priority/SLA · first-response and resolution times · CSAT ·
common issue themes · channel mix.

### Key workflows
Ticket triage → resolution · **WhatsApp integration** *(**[VERIFIED]** WhatsApp is already
the academy's real support channel — formalise it rather than fight it)* · account recovery ·
technical troubleshooting for live sessions · **safeguarding escalation with a defined path**.

**Reports:** volume and themes, SLA compliance, deflection rate, satisfaction.

**Integrations:** WhatsApp Business API, email, knowledge base, status page.

> **[VERIFIED]** V1 routes both `واتساب (رجال)` and `واتساب (نساء)` to the **same number** —
> defeating the gender segregation the institution is built on. Fix at the routing layer.

---

## 9. Content Management Portal

**Navigation:** Curriculum · Study Plans · Mind Maps · Pages · FAQ · Announcements ·
Translations · Media

**Permissions:** `content:*`, `publish:request`. Publishing to production requires approval.

### Key workflows
Manage curriculum and level definitions · **manage study plans** *(**[VERIFIED]** V1's four
plans are ~10 MB PDFs on a **third-party domain**, one over plain `http://` — bring these
in-house)* · manage the 7 mind-map downloads *(**[VERIFIED]** currently Google Drive links)* ·
edit marketing pages · **manage the FAQ** *(**[VERIFIED]** V1's "view all" CTA 404s)* ·
**manage translations across all 8 locales** *(**[VERIFIED]** V1 leaves "Register", "Men",
"Women", "Supervisors" untranslated in French, Italian and Urdu)*.

**Reports:** content freshness, translation coverage per locale, download counts, FAQ search
misses *(what users looked for and did not find)*.

> **[VERIFIED]** All V1 copy is hard-coded in PHP templates. Staff cannot change a word
> without a developer. This portal is what makes the institution self-sufficient.

---

## 10. Executive Dashboard

**Navigation:** Overview · Growth · Academic Outcomes · Quality · Operations · Association
Reporting

**Permissions:** `read:aggregate` only. **No PII.** Executives see cohorts, not children.

### Dashboard — the numbers that matter
| Metric | Why |
|---|---|
| Active students, by track/gender/country | Scale and reach |
| **Enrolment funnel + demand lost to closed tracks** | **[VERIFIED]** the 61% problem, quantified |
| **Juz completed per period** | The real output of a مقرأة |
| Certificates and ijazahs issued | Institutional credibility |
| Retention / dropout by cohort | Health |
| Teacher utilisation and quality index | Capacity constraint |
| Cost per student *(if finance enabled)* | Sustainability |
| Waitlist depth | The growth opportunity |

**Reports:** board pack, **Maknoon association reporting** *(the academy operates under
جمعية مكنون and reports to it)*, Ministry of Islamic Affairs returns *(**[RESEARCHED]** KSA
Quran associations report into a national system)*, annual impact report.

---

## 11. System Administration Portal

**Navigation:** Users & Roles · Tracks & Circles · Locales · Integrations · Feature Flags ·
Audit Log · Security · Jobs · Health

**Permissions:** `system:*`. **Two-person approval for destructive actions.** MFA mandatory.

### Key workflows
Role and permission management · **track/circle configuration** *(open, close, set capacity,
**set reopening date** — the control the Admissions dashboard surfaces)* · locale management ·
integration credentials · feature flags · **audit log review** · data retention and deletion
*(PDPL right to erasure)* · backup verification.

**Reports:** audit trail, permission matrix, integration health, job failures, security
events, uptime.

> **[VERIFIED]** V1 exposes `xmlrpc.php`, advertises its WordPress version, leaves
> `/wp-json/wp/v2/users` enumerable, and runs **end-of-life .NET 5**. Hardening belongs here.

---

## 12. Portal × capability matrix

| Capability | Std | Par | Tch | Sup | QA | Fin | Adm | Sup* | CMS | Exec | Sys |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| View own progress | ● | ○ | ○ | ○ | ○ | – | – | – | – | – | – |
| Grade tasmi' | – | – | ● | ○ | ○ | – | – | – | – | – | – |
| Mark attendance | – | – | ● | ○ | ○ | – | – | – | – | – | – |
| Manage consent | – | ● | – | – | ○ | – | ○ | – | – | – | ○ |
| Observe teachers | – | – | – | ● | ● | – | – | – | – | – | – |
| Issue certificates | – | – | – | ○ | ● | – | – | – | – | – | – |
| Manage capacity | – | – | – | ○ | – | – | ● | – | – | ○ | ● |
| Notify waitlist | – | – | – | – | – | – | ● | ○ | – | – | – |
| Handle payments | – | ○ | – | – | – | ● | ○ | – | – | ○ | – |
| Impersonate (consented) | – | – | – | – | – | – | – | ● | – | – | ● |
| Edit content | – | – | ○ | – | – | – | – | – | ● | – | ● |
| View aggregates | – | – | – | ○ | ● | ● | ● | ○ | – | ● | ● |
| Configure system | – | – | – | – | – | – | – | – | – | – | ● |

● full · ○ read/limited · – none · *Sup\* = Support*

---

## 13. Notification matrix

| Event | Student | Parent | Teacher | Supervisor | Admissions |
|---|:-:|:-:|:-:|:-:|:-:|
| Session starting | ● | ○ | ● | – | – |
| Absence recorded | ● | ● | ● | ○ | – |
| Tasmi' graded | ● | ● | – | – | – |
| Revision overdue | ● | ○ | ● | – | – |
| At-risk threshold | ○ | ● | ● | ● | – |
| Certificate issued | ● | ● | ○ | ○ | – |
| **Track reopened** | – | – | – | – | ● |
| **Waitlist → offer** | ● | ● | – | – | ● |
| Observation scheduled | – | – | ● | ● | – |
| Safeguarding flag | – | – | – | ● | – |

**Channels:** in-app (SignalR — **[VERIFIED]** already present), email, push, WhatsApp
(opt-in). Per-user, per-category preferences; quiet hours honoured in the user's timezone.
