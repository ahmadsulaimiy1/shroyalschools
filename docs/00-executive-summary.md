# Executive Summary — Itqan Virtual Quran Academy Rebuild

**Target:** https://itqan-quran.com/
**Audit date:** 2026-08-20
**Status:** Discovery complete. Full technical specification follows in `01`–`12`.

---

## 1. The single most important finding

The brief assumed this is one large website with an embedded LMS containing student,
teacher and admin dashboards, courses, quizzes and certificates.

**That is not the architecture.** This is **two separate systems on two hosts**, and the
public site contains no LMS at all:

| System | Host | Stack | Role |
|---|---|---|---|
| **Marketing site** | `itqan-quran.com` | WordPress 7.0.4 + custom theme `itqan-theme` (Tailwind v4) | Brochure + registration funnel. 14 pages. **Zero** LMS functionality. |
| **The actual LMS** | `register.itqan-quran.com` | **ASP.NET Core 5 MVC**, SignalR, Kendo UI, SB Admin 2 | Accounts, halaqa (circle) enrolment, notifications. Login-walled. |

The WordPress site's only job is to route a visitor to the correct entry point on the
ASP.NET application. Everything the brief describes as "the LMS" lives behind a login on a
different codebase, in a different language, that we cannot read from outside.

### What this means for the rebuild

Rebuilding `itqan-quran.com` from scratch is a **small, well-bounded project** (14 pages,
one interactive component). Rebuilding the LMS is a **completely separate and much larger
project** that cannot be specified from public crawling — it needs source access or
credentials. Section 8 documents everything observable about it and states plainly where
inference begins.

**Recommendation:** treat these as two workstreams. The marketing site can be rebuilt and
shipped independently and immediately; it is the higher-ROI half and is where every defect
listed below lives.

---

## 2. What the organisation actually is

**مِقْرَأَة إِتْقَان الِافْتِرَاضِيَّةُ** (Itqan Virtual Quran Academy) — an online Quran
memorisation and recitation academy operating under **جمعية مكنون لتحفيظ القرآن الكريم**
(Maknoon Association, Riyadh), with partner **جمعية إقرأ بالخرمة**. Saudi-based, Arabic-first
(RTL), serving students inside and outside the Kingdom, with multilingual outreach.

Teaching is gender-segregated, age-banded, delivered live over video, and priced as
"رمزية" (nominal/token pricing). It is **not** a self-paced course platform: there is no
cart, no checkout, no pricing table, and no payment gateway anywhere on the public site.

---

## 3. Defects found (all verified, not inferred)

These are ranked by business impact. Full detail and proposed fixes in `12-rebuild-checklist.md`.

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | **Critical** | **22 of 36 registration entry points (61%) are closed.** Every women's track — KSA *and* international — and every men's international track dead-ends in a waitlist form. | See `08-lms.md` catalog |
| 2 | **Critical** | The homepage "مسار النساء" (Women's path) router sends women through a 3-step flow to a page where **all 7 options are closed**. The funnel's primary CTA leads to a dead end. | `main.js` routing + catalog |
| 3 | **High** | FAQ "عرض كافة الأسئلة" (View all questions) CTA → **HTTP 404**. | `/الأسئلة-الشائعة/` returns 404 |
| 4 | **High** | Nav item "المصادر والمعرفة" (Resources & Knowledge) is `href="#"` — a dead top-level menu item on every page. | All 14 pages |
| 5 | **High** | **No meta description, no Open Graph, no Twitter Card, no structured data on any page.** Shares render as bare URLs; SERP snippets are auto-generated. | All 14 pages |
| 6 | **High** | Men's and women's WhatsApp buttons point to the **same number** (`966539065696`), defeating the gender-segregation the whole site is built around. | Homepage contact section |
| 7 | **Medium** | Four study-plan PDFs (~10 MB each, 40 MB total) are hosted on an **unrelated third-party domain** (`quranlives.com`); **one is served over plain `http://`**. | Homepage plans section |
| 8 | **Medium** | Seven mind-map downloads are Google Drive `/view` links — not direct downloads, require a Google account prompt for some users, and are unversioned. | Downloads page |
| 9 | **Medium** | **Locale mismatch.** Marketing site offers ar/en/fr/it/ur. LMS login offers ar/en/fr/id/Somali/ur/ru. Italian has no LMS login; Indonesian, Somali and Russian have no marketing page. | Login page vs site |
| 10 | **Medium** | Untranslated UI in localised blocks: "Register", "Men", "Women", "Supervisors" remain in English inside the French, Italian and Urdu sections. | Non-Arabic page |
| 11 | **Medium** | `logo.png` is **300 KB** and `license.jpg` **249 KB** — unoptimised, no WebP/AVIF, no `srcset`. Homepage HTML is **187 KB** uncompressed. | Measured |
| 12 | **Medium** | Registration is **JavaScript-only**. With JS disabled or failed, the site has no registration path whatsoever — `<form onsubmit="return false;">` with no fallback. | `main.js` |
| 13 | **Low** | Default WordPress content still published: "مثال على صفحة" (Sample Page, 404s but in sitemap) and "أهلا بالعالم" (Hello World post) are live and indexed. | Sitemap |
| 14 | **Low** | Dead code shipped: the entire statistics-counter module in `main.js` is commented out but still downloaded by every visitor. | `main.js` |
| 15 | **Low** | `xmlrpc.php` is exposed; WordPress version is publicly advertised via `<meta name="generator">`. | Homepage `<head>` |

---

## 4. What is genuinely good and must be preserved

Not everything needs changing. These are deliberate, well-executed decisions:

- **The smart registration router.** Gender → terms → phone → country detection → correct
  destination is a genuinely thoughtful piece of UX that removes a hard routing problem
  from the user. The *logic* should be kept and rebuilt server-side; only its brittleness
  needs fixing.
- **Forced terms acknowledgement.** The continue button is disabled until the checkbox is
  ticked. For an organisation with religious and safeguarding obligations, this is correct.
- **Age-banded, gender-segregated tracks** (nursery 3–6 → primary → intermediate/secondary →
  university/youth → over-40 → special needs → qira'at/ijazah). This taxonomy is the
  academy's core IP and is well designed.
- **Visual identity.** Islamic green `#027043` with gold `#d4af37` on a warm off-white
  `#fdfbf7`, Amiri for display and Tajawal for body — a coherent, appropriate, RTL-native
  system. Keep it wholesale.
- **Accessibility of intent.** A dedicated ذوي الهمم (special needs) track with individual
  plans is a real commitment, not a checkbox.

---

## 5. Recommended target architecture

| Layer | Recommendation | Why |
|---|---|---|
| Framework | **Next.js (App Router) + TypeScript** | Static-render 13 of 14 pages; RTL and i18n are first-class; the router becomes a server component with a working no-JS fallback. |
| Styling | **Tailwind v4** — port existing tokens verbatim | Already the theme's system. Zero design risk, immediate familiarity. |
| Content | **MDX or a headless CMS** (Sanity/Payload) | Copy is currently hard-coded in PHP templates; staff cannot edit anything without a developer. |
| Forms | **Server-side handler + progressive enhancement** | Removes the JS-only single point of failure. |
| Assets | Self-host, AVIF/WebP, `srcset`, CDN | Kills the 300 KB logo and the third-party PDF dependency. |
| i18n | `next-intl`, one locale set shared with the LMS | Ends the ar/en/fr/it/ur vs ar/en/fr/id/SML/ur/ru split. |
| LMS | **Leave in place; integrate via a documented API** | Rewriting a working ASP.NET system is out of scope and unjustified without source access. |

**Explicitly not recommended:** rebuilding the ASP.NET LMS as part of this project. There is
no public evidence of what it does after login, and guessing would produce a specification
that is confidently wrong.

---

## 6. Scope boundary — read this before using these documents

Everything in `01`–`07` and `09` is **observed fact**, extracted from live HTML, CSS, JS and
HTTP responses, and is safe to build from.

`08-lms.md`, `10-database-inference.md` and `11-api-inference.md` are **partly inference**.
Every inferred claim is tagged `[INFERRED]`. The public surface of the LMS —
login, registration and waitlist forms, field names, tech stack, track catalogue — is
observed and reliable. What happens *after* login is not visible from outside and is
proposed as a design, not documented as a fact.

**Do not hand `10` or `11` to a developer as a description of the existing database.**
They are a proposal for a new one.
