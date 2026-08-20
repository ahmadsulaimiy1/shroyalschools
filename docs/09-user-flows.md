# 09 — User Flows

Current flows are **observed**. Proposed flows are marked and are recommendations.

---

## 1. Student registration — current (observed)

```
Homepage
   │
   ├─ "ابدأ رحلتك الآن" / "التسجيل الآن" / "سجّل الآن"  → #registration
   ▼
[STEP 1] Choose path:  مسار الرجال  |  مسار النساء
   │  sets selectedGender; resets consent
   ▼
[STEP 2] Terms modal — 7 clauses
   │  must tick "قرأت الشروط وأوافق عليها بالكامل"
   │  → enables "موافق ومتابعة"
   ▼
[STEP 3] Phone modal — intl-tel-input, default +966
   │  "التسجيل الآن" → iti.isValidNumber()
   │     invalid → "يرجى إدخال رقم صحيح", halt
   ▼
   Country code read from the number
   │
   ├─ SA ──────────────► KSA page (by gender)
   ├─ Arab country ────► International page (by gender)
   └─ elsewhere ───────► [STEP 4]
                            │
                            ├─ "نعم، أتحدث العربية" ──► International page (by gender)
                            └─ "No, I don't" ─────────► EN/FR/IT/UR page by country,
                                                        else non-Arabic hub
   ▼
Registration page — 7 track cards (or 2 on language pages)
   │  "تسجيل الآن"
   ▼
register.itqan-quran.com/Account/Register?i=<GUID>
   │
   ├─ OPEN (14 of 36) ──► 13-field form → account created
   └─ CLOSED (22 of 36) ► 🚨 waitlist: name + WhatsApp only
```

### Where this flow fails

| Step | Problem |
|---|---|
| 1 | Both paths look equally available. **Every women's track is closed.** |
| 2 | Consent is required but never recorded — no audit trail for an "agreement". |
| 3 | A phone number is demanded to derive a country code, then discarded. Highest-friction step, lowest value. |
| 3 | JS-only. No JS → the funnel simply does not exist. |
| 4 | Country is used as a proxy for language. Wrong for diasporas and multilingual countries. |
| 5 | **No availability shown.** The user picks a track blind. |
| 6 | 61% of the time the journey ends in a waitlist that cannot even email them back. |
| — | No step is instrumented. Drop-off is invisible. |

**Net effect:** a 6-step journey where more than half of all completions terminate in a dead
end, with no measurement anywhere.

---

## 2. Student registration — proposed

```
/register  (server-rendered — works without JS)
   │
[STEP 1] Who is registering?
   │  Myself (adult)  |  My child ✚  |  Learning as a family ✚
   │  → child selects guardian flow (fixes the safeguarding gap)
   ▼
[STEP 2] Gender + Country + Preferred language ✚
   │  Country pre-selected from an IP hint, fully overridable
   │  Language chosen independently of country  ← fixes the proxy problem
   ▼
[STEP 3] Available tracks — LIVE AVAILABILITY ✚✚
   │  ┌──────────────────────────────────────────┐
   │  │ B11 · Primary (7–12)                     │
   │  │ ✅ Open · 4 places left  → [Register]    │
   │  ├──────────────────────────────────────────┤
   │  │ D11 · Over 40                            │
   │  │ ⏳ Full · reopens Rajab 1448             │
   │  │    [Notify me] ← captures email + track  │
   │  └──────────────────────────────────────────┘
   │  Closed tracks are never hidden — they are shown honestly, with a date and a capture.
   ▼
[STEP 4] Terms — recorded with timestamp, IP and policy version ✚
   ▼
[STEP 5] Enrolment form — progressive, labelled, real error messages
   ▼
Confirmation page + email ✚ (what happens next, when the halaqa starts, how to join)
```

**Every step instrumented.** Funnel becomes measurable for the first time.

---

## 3. Waitlist flow — current vs proposed

**Current (observed):**
```
Closed track → generic apology → [ Name ] [ WhatsApp ] → حفظ → (nothing)
```
No email. No track preference beyond an integer. No confirmation. No reopening notification.
**61% of registration intent lands here and effectively evaporates.**

**Proposed:**
```
Closed track → "B11 Primary is full — reopening ~Rajab 1448"
   → [ Name ] [ Email ] [ WhatsApp ] [ Age ] [ Language ] [ ☑ Contact me when it reopens ]
   → Confirmation: "You are #12 on the list. We will email and message you."
   → Automatic notification on reopening, with a time-limited priority window
```

---

## 4. Staff recruitment — current vs proposed

**Current (observed):** header dropdown or footer → one of four **Google Forms** →
spreadsheet. Applicants never enter the LMS. Two links still use the retired `goo.gl`
shortener. This contradicts terms clause 2, which states registrations outside the platform
are not recognised.

**Proposed:** `/join` hub → role (teacher/supervisor) → in-platform application with
qualifications, ijazah details, availability and CV upload → applicant record in the LMS →
status tracking and interview scheduling.

---

## 5. Other flows

**Resource download (observed):** nav → mind maps page → 7 cards → Google Drive `/view` →
extra click, possible sign-in wall, no analytics.
**Proposed:** self-hosted direct download with size and page count shown; optional email
capture for the complete bundle.

**Support (observed):** WhatsApp float / contact section / footer → `wa.me/966539065696` —
⚠ the *same number* for both "رجال" and "نساء", defeating the gender segregation the site is
built around. No async channel, no ticket, no record.
**Proposed:** correct per-gender numbers, plus a real `/contact` form with routing and
confirmation.

**Returning student (observed):** ⚠ **there is no login link anywhere on the marketing
site.** An enrolled student cannot reach `register.itqan-quran.com` from
`itqan-quran.com` — they must know the URL. This is a significant omission.
**Proposed:** persistent "تسجيل الدخول" in the header.

---

## 6. Locale consolidation

| Locale | Marketing site | LMS UI | LMS form option |
|---|---|---|---|
| Arabic | ✅ | ✅ | ✅ |
| English | ✅ | ✅ | ✅ |
| French | ✅ | ✅ | ✅ |
| Urdu | ✅ | ✅ | ✅ |
| **Italian** | ✅ | ❌ | ✅ |
| **Indonesian** | ❌ | ✅ | ✅ |
| **Somali** | ❌ | ✅ | ✅ |
| **Russian** | ❌ | ✅ | ✅ |

Three inconsistent language sets across three surfaces. An Italian speaker gets a marketing
page and a form option but **no interface they can read**. Indonesian, Somali and Russian
speakers are supported by the LMS but invisible to marketing.

**Proposed:** one canonical set — **ar, en, fr, ur, id, so, ru, it** — applied identically to
the marketing site, the LMS UI and the form options, with `hreflang` and per-locale `dir`/`lang`.

---

## 7. Flow defect summary

| # | Severity | Defect |
|---|---|---|
| 1 | **Critical** | Women's path leads to 7 closed tracks with no warning |
| 2 | **Critical** | Registration is JS-only; no fallback |
| 3 | **Critical** | Waitlist captures no email — 61% of intent is unrecoverable |
| 4 | **High** | No availability shown before the user leaves the site |
| 5 | **High** | No login entry point for returning students |
| 6 | **High** | No guardian flow despite enrolling children from age 3 |
| 7 | **High** | No analytics on any funnel step |
| 8 | Medium | Phone collected then discarded |
| 9 | Medium | Country used as a proxy for language |
| 10 | Medium | Consent not recorded |
| 11 | Medium | Same WhatsApp number for both genders |
| 12 | Medium | Staff applications bypass the LMS |
| 13 | Medium | Three inconsistent locale sets |
| 14 | Low | No back navigation between steps |
| 15 | Low | No confirmation email after registration |
