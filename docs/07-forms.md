# 07 — Forms Specification

Every data-capture surface across both systems. Field names are the **real** `name`
attributes, so this doubles as the integration contract.

> **Key fact:** `itqan-quran.com` contains **no data-collecting form at all**. Its only
> `<form>` is `#smart-reg-form`, which has `onsubmit="return false;"` and exists purely to
> host the router UI. Every real submission happens on `register.itqan-quran.com` or in
> Google Forms.

---

## 1. Form landscape

| # | Form | Host | Method | Status |
|---|---|---|---|---|
| 1 | Smart registration router | WordPress | None — client-side redirect | Live |
| 2 | LMS student registration | ASP.NET | `POST` | Live, 14 of 36 tracks open |
| 3 | LMS waitlist (closed tracks) | ASP.NET | `POST` | Live, 22 tracks |
| 4 | LMS login (passwordless) | ASP.NET | `POST` | Live |
| 5 | LMS account recovery | ASP.NET | `POST` | Live (`/Account/Reset`) |
| 6–9 | Teacher / supervisor recruitment ×4 | Google Forms | External | Live |
| 10–12 | Non-Arabic registration ×3 | Google Forms | External | Live |

---

## 2. Smart registration router *(not a real form)*

`<form dir="ltr" id="smart-reg-form" class="space-y-6" onsubmit="return false;">`

| Control | ID | Type | Purpose |
|---|---|---|---|
| Gender buttons | `.gender-selector[data-gender]` | button | Sets `selectedGender` |
| Terms consent | `#terms-agree-check` | checkbox | Gates `#btn-agree-terms` |
| Continue | `#btn-agree-terms` | button | `disabled` until checked |
| Phone | `#phone` | tel (intl-tel-input) | Country detection only |
| Validate | `#btn-check-number` | button | `iti.isValidNumber()` |
| Error | `#phone-error` | div | `يرجى إدخال رقم صحيح` |
| Language | `#btn-speak-arabic` / `#btn-dont-speak-arabic` | button | Final branch |

**Validation:** exactly one rule — `intlTelInput.isValidNumber()`. On failure: unhide
`#phone-error`, add `!border-red-500`, halt. **No other validation exists.**

**Submission:** none. `window.location.href = redirectUrl`. **Nothing is stored, logged or
sent.** The phone number is discarded after reading its country code.

### Defects

| Severity | Issue |
|---|---|
| Critical | No `<noscript>` fallback — JS off means no registration path |
| High | Phone collected for country detection only, then discarded — unjustified data friction |
| High | No analytics on any step; funnel drop-off is invisible |
| Medium | Terms consent not recorded — users tick a box that leaves no audit trail, on a page that calls itself an `اتفاقية التسجيل` (registration agreement) |
| Medium | No `aria-live` on the error; screen readers are not told validation failed |
| Medium | No back navigation; closing a modal discards all progress |
| Low | Error text is hard-coded Arabic even in the non-Arabic flow |

---

## 3. LMS student registration ⭐

`GET|POST https://register.itqan-quran.com/Account/Register?i=<GUID>`
Form: `<form id="frm" method="post">` — ASP.NET MVC with unobtrusive validation.

### Fields (verbatim `name` attributes)

| # | `name` | Label | Type | Required | Notes |
|---|---|---|---|---|---|
| 1 | `fy` | — | hidden | — | Likely fiscal/academic year |
| 2 | `Name` | `الاسم:` | text | ✅ | Terms require a **three-part** name |
| 3 | `Gender` | `الجنس:` | select | ✅ | **Pre-filtered by GUID** — men's track offers only `رجل` |
| 4 | `Age` | `السن:` | number | ✅ | Must match the track's age band |
| 5 | `__Invariant` | — | hidden | — | ASP.NET culture-invariant marker |
| 6 | `Email` | `البريد:` | email | ✅ | Becomes the login identifier |
| 7 | `Country` | `الدولة:` | select | ✅ | Name + English name + dial code |
| 8 | `Mobile` | `الجوال:` | text | ✅ | |
| 9 | `Language` | `اللغة:` | select | ✅ | 8 options |
| 10 | `HefzDailyCount` | *(unlabelled)* | select | ✅ | Daily memorisation target |
| 11 | `HefzDuration` | *(unlabelled)* | select | ✅ | Target completion time |
| 12 | `AcademicAdvertiseWay` | *(unlabelled)* | text | ✅ | How they heard about the academy |
| 13 | `CircleNumber` | `اختر أي حلقة متاحة:` | select | — | Available halaqa |
| 14 | `__RequestVerificationToken` | — | hidden | — | CSRF anti-forgery |

### Option sets (verbatim)

**`HefzDailyCount`** — `ربع وجه` (¼ page) · `نصف وجه` (½) · `وجه كامل` (1) · `وجهين` (2) ·
`ثلاثة أوجه` (3) · `أربعة أوجه` (4) · `خمسة أوجه` (5)

**`HefzDuration`** — `أقل من شهر` · `شهرين` · `ستة أشهر` · `سنة` · `سنة ونصف` · `سنتين` ·
`3 سنوات`

**`Language`** — `عربي` · `إنجليزي - English` · `فرنسي - Français` · `أوردو - اوردو` ·
`إندونيسي - bahasa Indonesi` · `الصومالية - Soomaali` · `Italiano` · `الروسية - Русский`

**`Country`** — `السعودية - Saudi Arabia (+966)` · `مصر - Egypt (+20)` ·
`الأردن - Jordan (+962)` · `الإمارات - United Arab Emirates (+971)` ·
`البحرين - Bahrain (+973)` · `الجزائر - Algeria (+213)` · `السنغال - Senegal (+221)` ·
`السودان - Sudan (+249)` · `الصومال - Somalia (+252)` · `العراق - Iraq (+964)` ·
`الكويت - Kuwait (+965)` … *(truncated in capture; full list is longer)*

**`CircleNumber`** — e.g. `حلقة استقبال طلاب الجدد 💡` (New-student intake circle)

### Validation

Client: `jquery.validate` + `jquery.validate.unobtrusive` with `messages_ar.min.js`.
Required fields carry `data-val-required="*"` — **the error message for every required
field is literally an asterisk.** Server: ASP.NET model binding + `__RequestVerificationToken`.

### ⚠ Defects

| Severity | Issue |
|---|---|
| High | **`data-val-required="*"`** — an asterisk is not an error message. Screen-reader users hear "star"; sighted users get no guidance on what is wrong. **13 required fields, 13 asterisks.** |
| High | Three fields (`HefzDailyCount`, `HefzDuration`, `AcademicAdvertiseWay`) have **no `<label>`** — unlabelled required inputs are a direct WCAG 1.3.1 / 4.1.2 failure |
| Medium | `AcademicAdvertiseWay` is free text where a select would give usable attribution data |
| Medium | `Language` offers 8 options but the LMS UI ships only 7 locales — **Italian has no interface** |
| Medium | No inline "no availability" state; capacity is only discovered by redirect |
| Low | `Age` is a free number with no range enforcement tied to the track's band |

### Rebuild recommendation

Real per-field messages in the user's language · `<label>` on every input ·
`aria-describedby` for errors · `Age` bounded by the track band with an explanatory message ·
`AcademicAdvertiseWay` → select + "other" · progressive disclosure across 2–3 steps rather
than 13 fields at once · show live capacity before submit.

---

## 4. LMS waitlist form *(closed tracks)*

`POST /ClosedCircleType/CreateNeedToRegisterdUser?circleTypeId=<int>`

| Field | Label | Type |
|---|---|---|
| Name | `الأسم` ⚠ *(misspelled)* | text |
| WhatsApp | `رقم واتساب` | text |
| Submit | `حفظ` | button |

Message shown: `نعقذر عن إغلاق التسجيل حاليًا لاكتمال العدد…` *(see `06-copywriting.md` §16
for the verbatim text)*.

**This form receives the traffic from 22 of 36 entry points — 61% of all registration
intent lands here.** Yet it captures only a name and a phone number.

### ⚠ Defects

| Severity | Issue |
|---|---|
| High | **No email captured** — the academy cannot email a waitlisted user when the track reopens; it must rely on manual WhatsApp outreach |
| High | **No track preference stored beyond `circleTypeId`** — no age, gender or language, so reopening cannot be targeted |
| High | **No confirmation of position or expected timeframe** — the user gets no feedback loop |
| Medium | The internal integer `circleTypeId` is exposed in the URL — enumerable, and leaks catalogue size |
| Medium | `الأسم` misspelling on the highest-traffic form on the platform |
| Low | No consent checkbox for being contacted later |

**This is the highest-leverage fix in the entire audit.** A waitlist that captures email +
track + age + language, sends an immediate confirmation, and auto-notifies on reopening
would convert a 61% dead end into a pipeline.

---

## 5. LMS login *(passwordless)*

`POST /Account/Login`

| Field | Label | Type |
|---|---|---|
| `ReturnURL` | — | hidden |
| `Email` | `البريد` | email |
| `Code` | `كود: الدخول` | text |
| `__RequestVerificationToken` | — | hidden |

Links: `طلب كود` (Request code — `href="#"`, JS-driven) · `استعادة الحساب` (`/Account/Reset`).
Protected by **Google reCAPTCHA v3** (site key `6Le27zYiAAAAAHr4z3n51xKFVunKe02tJm-ByFaM`).

**Assessment:** passwordless email-code auth is a **good choice** here — no password reset
burden, no credential reuse, and it suits a user base spanning children, older adults and
low-digital-literacy learners. Keep it.

### Defects

- `طلب كود` is `href="#"` — the primary way to obtain a login code depends entirely on JS
  with no fallback.
- No stated code expiry or rate-limit feedback.
- No visible "check your email" confirmation state in the static markup.

---

## 6. Google Forms *(7 external forms)*

| # | Purpose | ID / URL |
|---|---|---|
| 1 | تسجيل المعلمين (Male teachers) | `goo.gl/forms/FO4dBRij0buhezgF3` |
| 2 | تسجيل المعلمات (Female teachers) | `goo.gl/forms/artmNJBAb9yE9OJ42` |
| 3 | تسجيل المشرفين (Male supervisors) | `docs.google.com/forms/d/e/1FAIpQLSeNrT2BJ2M3WDlUK_AzRwbgewlmeTDp-m1Po71Bn0V1FYKahw` |
| 4 | تسجيل المشرفات (Female supervisors) | `forms.gle/xUm7QUnc37q1HpHD7` |
| 5–7 | Non-Arabic student registration | `1FAIpQLSciSGOLuEMxbLaEydBBEX…`, `1FAIpQLSdlaWJ-zteKtdgMIKzIYzg7ahf3zX…`, `1FAIpQLSdt77dBTf_C80iQMG-cOwAHtw4Uti…` |

### ⚠ Defects

| Severity | Issue |
|---|---|
| High | **Staff applications live in spreadsheets, not the LMS.** Teacher and supervisor records are disconnected from the system they will teach in — no single source of truth. |
| High | **Two forms still use `goo.gl` short links.** Google shut down the `goo.gl` shortener for general use; these are legacy links that are a live availability risk. |
| Medium | Non-Arabic students registering here **never enter the LMS** — they exist only in a spreadsheet, contradicting terms clause 2 (`لا يُعتد بأي تسجيل يتم من خارج المنصة` — "no registration outside the platform is recognised"). The site violates its own policy. |
| Medium | Google Forms cannot be styled, localised consistently, or made to match the brand |
| Medium | Data leaves the organisation's control; no DPA, unclear retention |
| Low | Three different link formats (`goo.gl`, `forms.gle`, `docs.google.com`) show ad-hoc creation |

**Recommendation:** migrate all seven into the platform as first-class forms.

---

## 7. Missing forms

| Missing | Why it matters |
|---|---|
| **Contact form** | `تواصل معنا` is only an anchor to WhatsApp/phone. No async channel; no record. |
| **Newsletter / reopening alerts** | The single highest-value capture given 22 closed tracks. |
| **Feedback / suggestions** | Terms clause 7 *invites* feedback but provides no mechanism. |
| **Donation** | Terms clause 6 names the Maknoon store but gives no link. |
| **Complaint / safeguarding** | Required for a platform teaching minors. |
| **Parent/guardian consent** | The 3–6 and 7–12 tracks enrol children with **no guardian field anywhere** — a significant safeguarding and data-protection gap. |

---

## 8. Consolidated form specification for the rebuild

```
/register                 Router — server-rendered, 3 steps, no-JS fallback
/register/[track]         Enrolment — labelled fields, real messages, live capacity
/waitlist/[track]         Waitlist — name, email, WhatsApp, age, language, consent
/join/teacher             Teacher application (replaces 2 Google Forms)
/join/supervisor          Supervisor application (replaces 2 Google Forms)
/contact                  Contact — subject, message, preferred channel
/feedback                 Suggestions (fulfils terms clause 7)
/alerts                   "Notify me when registration reopens"
```

**Cross-cutting requirements:** every field labelled · specific error messages in the user's
locale · `aria-live` on validation · CSRF on every POST · rate limiting · spam protection ·
server-side validation mirroring client rules · consent recorded with **timestamp, IP and
policy version** · guardian fields for under-18 tracks · confirmation email on every
submission · full keyboard operability.
