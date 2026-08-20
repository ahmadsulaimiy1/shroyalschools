# 08 — LMS Specification

> **Scope warning.** This document mixes observed fact with inference and labels which is
> which on every claim.
>
> - **§1–§5 are observed** — extracted from live HTTP responses on `register.itqan-quran.com`.
>   Safe to build integrations against.
> - **§6–§8 are `[INFERRED]`** — the platform is login-walled. These sections are a *proposal*
>   informed by the observable surface and the published terms, **not** a description of what
>   exists. Do not hand them to a developer as a spec for the current system.
>
> Getting the rest requires credentials or source access. That should be the first ask.

---

## 1. The LMS is a separate application

The brief assumed an LMS embedded in the website. It is not. It is a **distinct ASP.NET Core
application on `register.itqan-quran.com`**, written in a different language from the
WordPress marketing site and sharing nothing with it but a brand.

`https://register.itqan-quran.com/` → `302` → `/Account/Login?ReturnUrl=%2F`

Everything except the login, registration, waitlist and reset endpoints is authenticated.

---

## 2. Observed technology stack

| Layer | Technology | Evidence |
|---|---|---|
| Framework | **ASP.NET Core MVC** | `/Account/Login`, `__RequestVerificationToken`, `data-val-*` |
| Version | **~.NET 5** | SignalR client `5.0.11` |
| Real-time | **SignalR 5.0.11** + `/js/notifications.js` | Script tags |
| UI kit | **Kendo UI (Telerik)** | `kendo.rtl.min.css` |
| Admin theme | **SB Admin 2** | `sb-admin-2.min.css`, `sb-admin-2.min.js` |
| CSS | Bootstrap + custom `site.min.css`, `rtl.css` | Script tags |
| JS | jQuery 2.2.1, jQuery UI | Script tags |
| Validation | `jquery.validate` + unobtrusive + `messages_ar` | Script tags |
| Notifications | **toastr** (RTL build) | `toastr-rtl.min.css` |
| Auth | **Passwordless — email + emailed code** | Login form fields |
| Bot protection | **Google reCAPTCHA v3** | Site key `6Le27zYiAAAAAHr4z3n51xKFVunKe02tJm-ByFaM` |
| Fonts | Google Fonts (Nunito) | ⚠ Latin font on an Arabic-first RTL app |
| CDN/WAF | Cloudflare | Response headers |
| Version | **v1.2.3.4**, `© 1448` (Hijri) | Footer |
| Custom | `/js/comboBox.min.js` | Script tag |

**Two independent signals confirm real LMS features exist:**
1. **SignalR + `notifications.js`** — a persistent real-time channel. This is not something
   you add to a registration form; it implies in-app notifications and/or messaging.
2. **Terms clause 4** requires students to *"رفع تقرير التسميع عبر المنصة"* (submit a
   recitation report via the platform) — confirming an attendance/assessment reporting loop.

---

## 3. Observed endpoints

| Endpoint | Method | Auth | Purpose |
|---|---|---|---|
| `/Account/Login` | GET, POST | Public | Email + code |
| `/Account/Login?l={ar,en,fr,id,SML,ur,ru}` | GET | Public | Locale switch |
| `/Account/Reset` | GET, POST | Public | Account recovery |
| `/Account/Register?i=<GUID>` | GET, POST | Public | Track registration |
| `/ClosedCircleType/CreateNeedToRegisterdUser?circleTypeId=<int>` | GET, POST | Public | Waitlist |
| `/Home/About` | GET | Public | Version info |
| `/` and all else | — | **Auth required** | Not observable |

### Two identifier schemes — an important design detail

- **Public:** an opaque **GUID** per track (`?i=8711e101-…`) — non-enumerable, safe to publish.
- **Internal:** a sequential **integer** `circleTypeId` (28, 30, 44, 79, 106 …).

The GUID scheme is good practice. **But the closed-track redirect leaks the internal integer
into the URL**, undoing that protection: the IDs are enumerable and reveal roughly how many
circle types exist. The waitlist route should also take the GUID.

---

## 4. Track catalogue — complete, verified

All 36 registration entry points, resolved by following each GUID and recording the outcome.

### Naming scheme

`<LETTER><NUMBER>` where the letter encodes the age/needs band and the number the cohort:
**A** nursery · **B** primary · **C** intermediate/secondary & university · **D** over-40 ·
**E** special needs · **H** qira'at & ijazah · **G** international male · **X** international
female. The 🇸🇦 flag marks KSA-resident tracks.

### 4.1 Men — inside KSA — **ALL 7 OPEN** ✅

| Code | Track | Age | GUID | Status |
|---|---|---|---|---|
| A11 | قسم الروضة والتأسيس | 3–6 | `8711e101-1ca7-4751-8afc-9b3094b74b3c` | ✅ OPEN |
| B11 | قسم المرحلة الابتدائية | 7–12 | `9fb0852e-38d9-4531-9580-e81e71619d74` | ✅ OPEN |
| C11 | قسم المرحلة المتوسطة والثانوية | 13–18 | `59ffe975-2fb1-4e86-bd09-24f657467eb8` | ✅ OPEN |
| C21 | قسم المرحلة الجامعية والشباب | 19–40 | `54817afe-2638-44d9-b3a4-b84859d71379` | ✅ OPEN |
| D11 | قسم فوق الأربعين | 40+ | `c221ab1b-2f61-42a0-9437-b2960aea9cc3` | ✅ OPEN |
| E11 | قسم ذوي الهمم | — | `ea5c2438-8b0a-4737-bd1d-dac1e0385763` | ✅ OPEN |
| H11 | قسم القراءات والإجازات | — | `f541eb5f-a1e4-4d58-8093-af35a0b10381` | ✅ OPEN |

### 4.2 Women — inside KSA — **ALL 7 CLOSED** ❌

| Track (page order) | GUID | `circleTypeId` | Status |
|---|---|---:|---|
| الروضة والتأسيس | `11c3ac58-1473-42fc-9184-2ce1987411d9` | 44 | ❌ CLOSED |
| المرحلة الابتدائية | `181f9ee7-d33a-4990-b9fc-cc3aab19141d` | 46 | ❌ CLOSED |
| المتوسطة والثانوية | `f0b427f3-e7a0-46a0-9a83-a10dbcc46109` | 48 | ❌ CLOSED |
| الجامعية والفتيات | `18e139aa-a7b0-4b2b-b857-f3797c105e27` | 94 | ❌ CLOSED |
| ما فوق الأربعين | `2c622c8b-4b40-41fd-9d8f-26f17a67b69e` | 50 | ❌ CLOSED |
| ذوي الهمم | `0d651942-c053-4e7f-baae-8969ea64ee34` | 79 | ❌ CLOSED |
| القراءات والإجازات | `d60c5774-abad-4e93-80b8-5eaac2c5c912` | 57 | ❌ CLOSED |

### 4.3 Men — outside KSA — **ALL 7 CLOSED** ❌

| Track (page order) | GUID | `circleTypeId` | Status |
|---|---|---:|---|
| الروضة والتأسيس | `e413d393-fd9e-47b5-9cc8-da96fc5f37bb` | 28 | ❌ CLOSED |
| المرحلة الابتدائية | `5799e1e3-d08b-4472-8863-d7e8e5bbf668` | 30 | ❌ CLOSED |
| المتوسطة والثانوية | `b3872b54-c575-4bf2-84c5-c1cf27b01925` | 32 | ❌ CLOSED |
| الجامعية والشباب | `b0dcf35a-9cac-4acd-b048-c8b384c0a071` | 93 | ❌ CLOSED |
| ما فوق الأربعين | `a3240f5e-4fed-4ff7-b347-0b1dba31a20e` | 34 | ❌ CLOSED |
| ذوي الهمم | `8c1d160a-071e-4651-8953-1adf4647ec9c` | 36 | ❌ CLOSED |
| القراءات والإجازات | `c1112a77-b6ad-4e93-afbb-8e23fdb3bade` | 38 | ❌ CLOSED |

### 4.4 Women — outside KSA — **ALL 7 CLOSED** ❌

| Track (page order) | GUID | `circleTypeId` | Status |
|---|---|---:|---|
| الروضة والتأسيس | `e924156d-ffea-4e87-837b-6f492fc1cadb` | 45 | ❌ CLOSED |
| المرحلة الابتدائية | `8a4c8295-8e57-4e9a-9d8e-85d4c6464608` | 47 | ❌ CLOSED |
| المتوسطة والثانوية | `086abb57-1fc9-4425-869e-e165ac10ed74` | 49 | ❌ CLOSED |
| الجامعية والفتيات | `9d36c55b-bffe-4af2-8501-90a37d419f93` | 92 | ❌ CLOSED |
| ما فوق الأربعين | `ae3a9345-e0f9-4496-8077-0a07590b4ec5` | 51 | ❌ CLOSED |
| ذوي الهمم | `4fae1c36-3e4f-4f2a-bd19-52f851e8ba7d` | 106 | ❌ CLOSED |
| القراءات والإجازات | `de027861-cd2c-4002-a754-789cfd3bb0d2` | 58 | ❌ CLOSED |

### 4.5 International language tracks — **BOTH OPEN** ✅

| Code | Track | GUID | Status |
|---|---|---|---|
| G11 | Male International Halaqas | `5c24212d-35b4-4996-8748-55422740a8b4` | ✅ OPEN |
| X11 | Female International Halaqas | `0118c82d-03e8-4ea1-a475-ee9be52aa23a` | ✅ OPEN |

⚠ **All four language pages (EN, FR, IT, UR) link to these same two GUIDs.** The four pages
are presentational only; every non-Arabic student lands in the same two halaqas.

### 4.6 Availability summary

| Segment | Open | Closed |
|---|---:|---:|
| Men — KSA | **7** | 0 |
| Women — KSA | 0 | **7** |
| Men — International | 0 | **7** |
| Women — International | 0 | **7** |
| International language (G11/X11) | **2** | 0 |
| **Total** | **9** | **28** |

Counting the 36 *page-level entry points* (G11/X11 are each linked from 4 language pages):
**14 of 36 open, 22 closed (61%)**.

### 🚨 The business consequence

The homepage router presents two equal choices — `مسار الرجال` and `مسار النساء`. A woman
who chooses her path completes three steps (gender → terms → phone) and arrives at a page
where **every one of the seven options is full**. There is no advance warning at any point.

Read together with the international closures, the practical position is:
**the only Arabic students the platform can currently enrol are men inside Saudi Arabia.**

This is not a UX nitpick — it is the dominant fact about the site's current performance, and
no visual redesign will matter next to fixing it.

---

## 5. Observed capabilities

| Capability | Status | Evidence |
|---|---|---|
| Passwordless auth | ✅ Confirmed | Login form |
| Account recovery | ✅ Confirmed | `/Account/Reset` |
| Multi-locale UI (7) | ✅ Confirmed | `?l=` switcher |
| Track-based enrolment | ✅ Confirmed | 36 GUIDs |
| Capacity management | ✅ Confirmed | Closed-track redirect |
| Waitlist capture | ✅ Confirmed | `CreateNeedToRegisterdUser` |
| Real-time notifications | ✅ Confirmed | SignalR + `notifications.js` |
| Toast alerts | ✅ Confirmed | toastr |
| Data grids | ✅ Strongly implied | Kendo UI |
| Admin dashboard | ✅ Strongly implied | SB Admin 2 |
| Recitation reporting | ✅ Implied by policy | Terms clause 4 |
| Attendance | ✅ Implied by policy | Terms clause 4 |
| Certificates | ⚠ Claimed, unverified | Advantage #1 |
| Quizzes / assignments | ❓ No evidence | — |
| Payments | ❌ No evidence | No gateway anywhere |
| Video delivery | ❌ External | FAQ cites external video tools |

**Note on video:** the FAQ states teaching depends on *"برامج الاتصال المرئي والصوتي"*
(audio/video communication programs) — i.e. sessions run on **external tools (likely Zoom or
similar), not inside the LMS.** The LMS administers; it does not host the classroom.

**Note on payments:** there is no cart, checkout, price list or gateway anywhere on either
host. Combined with `بأسعار رمزية` (nominal pricing) and the charitable-association
structure, the platform is either free or collects fees out-of-band. **Do not build a
payment system without confirming this with the client.**

---

## 6. `[INFERRED]` Roles

Derived from the four registration audiences (student, teacher, supervisor, admin) and the
SB Admin 2 template — **not observed**.

| Role | Basis |
|---|---|
| **Student / طالب** | Registration forms |
| **Teacher / معلم·ة** | Dedicated recruitment forms |
| **Supervisor / مشرف·ة** | Dedicated recruitment forms — a distinct layer above teachers |
| **Administrator** | SB Admin 2 admin theme |
| **Guardian / ولي أمر** | ⚠ **Does not appear to exist** — see below |

### ⚠ The guardian gap

The academy enrols children from **age 3**. Yet:
- no guardian field exists on any registration form,
- no guardian role is evident,
- there is no parent-facing surface anywhere on either host.

A 3-year-old cannot supply an email address, consent to terms, or file recitation reports.
**A guardian role is not a feature request — it is a safeguarding and data-protection
requirement.** This is the most serious structural gap found in the audit and should be
raised with the client directly.

---

## 7. `[INFERRED]` Proposed dashboards

**None of this is observed.** Offered as a design proposal consistent with the platform's
evident purpose.

**Student:** next session (with join link) · today's memorisation assignment ·
recitation-report submission (fulfils terms clause 4) · progress by juz'/page ·
attendance record · teacher messages · certificates · schedule.

**Teacher:** today's halaqat · roster with per-student progress · attendance marking ·
recitation-report review and grading · student notes · leave/substitution requests.

**Supervisor:** assigned teachers and halaqat · attendance and completion rates ·
quality review of teacher reports · escalations · capacity monitoring.

**Admin:** enrolment funnel by track/gender/country · **capacity and waitlist depth per
track** (directly addresses §4.6) · teacher and supervisor management · circle scheduling ·
certificate issuance · broadcast announcements · Maknoon-facing reporting.

**Guardian ✚:** child's schedule, attendance, progress; teacher contact; consent management.

---

## 8. `[INFERRED]` Priority improvements

| # | Improvement | Rationale |
|---|---|---|
| 1 | **Live availability on the marketing site** | Fixes the 61% dead end. Highest ROI change available. |
| 2 | **Waitlist that captures email + track + demographics, with auto-notify on reopen** | Converts 22 dead ends into a pipeline. |
| 3 | **Guardian accounts for under-18 tracks** | Safeguarding and data-protection requirement. |
| 4 | **Publish capacity/opening dates** | "Opens in Rajab" beats "full" with no date. |
| 5 | Real validation messages (replace `*`) | Accessibility and completion rate. |
| 6 | Unify locales across site and LMS | Ends the ar/en/fr/it/ur vs ar/en/fr/id/SML/ur/ru split. |
| 7 | Migrate the 7 Google Forms into the LMS | Single source of truth; honours terms clause 2. |
| 8 | Use GUIDs on the waitlist route | Stops leaking internal integer IDs. |
| 9 | Replace Nunito with Tajawal/Amiri in the LMS | Brand consistency; Nunito has no Arabic. |
| 10 | Modernise .NET 5 → current LTS | **.NET 5 is end-of-life and unsupported** — a live security exposure. |

> **Flag for the client:** .NET 5 reached end of support in May 2022. Running an
> unsupported framework that processes children's personal data is the most significant
> technical risk identified in this audit, independent of any redesign.

---

## 9. What we still need

To specify the LMS properly, request in this order:

1. **Source code access** (or a walkthrough) for `register.itqan-quran.com`
2. **Test credentials** for each role — student, teacher, supervisor, admin
3. **Database schema** — replaces the inference in `10-database-inference.md`
4. **Confirmation of the payment model** — free, out-of-band, or planned
5. **Certificate process** — who issues, what triggers, what the artefact is
6. **Video platform** — which tool, and whether integration is wanted
7. **Capacity policy** — how and when tracks reopen
8. **Guardian/minor policy** — what consent is currently obtained, and how

Items 1–3 unblock the largest amount of downstream work; item 8 is the most urgent.
