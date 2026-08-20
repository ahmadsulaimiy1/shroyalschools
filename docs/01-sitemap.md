# 01 — Sitemap & Site Architecture

All URLs verified live on 2026-08-20. HTTP status is from a direct request.

---

## 1. Two-host topology

```
                        ┌──────────────────────────────────────┐
   Visitor ───────────► │  itqan-quran.com                     │
                        │  WordPress 7.0.4 + itqan-theme       │
                        │  14 pages · marketing + routing only │
                        └───────────────┬──────────────────────┘
                                        │  smart router (client-side JS)
                                        │  gender → terms → phone → country
                                        ▼
                        ┌──────────────────────────────────────┐
                        │  register.itqan-quran.com            │
                        │  ASP.NET Core 5 MVC · v1.2.3.4       │
                        │  THE ACTUAL LMS — login-walled       │
                        └──────────────────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
          /Account/Register?i=<GUID>            /ClosedCircleType/…?circleTypeId=<int>
          (open track → real form)              (closed track → waitlist form)
```

Additionally, several flows leave both systems entirely:

- **Staff recruitment** → Google Forms (4 distinct forms)
- **Non-Arabic student registration** → Google Forms (3 distinct forms)
- **Study plan PDFs** → `quranlives.com` (third-party domain)
- **Mind maps** → Google Drive (7 files)
- **Support** → WhatsApp `wa.me/966539065696`

---

## 2. Complete page inventory — `itqan-quran.com`

Source: `wp-sitemap.xml` + REST API `/wp/v2/pages` + link crawl. WordPress page ID and PHP
template are included because they define the rebuild's route table.

| ID | Title (AR) | English | URL path | Template | HTTP |
|---:|---|---|---|---|---|
| 7 | الرئيسية | Home | `/` | `front-page.php` | 200 |
| 8 | عن المنصة | About the Platform | `/عن-المنصة/` | `page-about.php` | 200 |
| 9 | السياسات واللوائح | Policies & Regulations | `/السياسات-واللوائح/` | `page-policy.php` | 200 |
| 10 | الخرائط الذهنية لتحفيظ القرأن الكريم | Mind Maps for Memorisation | `/الخرائط-الذهنية-لتحفيظ-القرأن-الكريم/` | `page-downloads.php` | 200 |
| 11 | تسجيل الرجال داخل المملكة | Men's Registration — KSA | `/تسجيل-الرجال-داخل-المملكة/` | `page-men-registration.php` | 200 |
| 12 | تسجيل النساء داخل المملكة | Women's Registration — KSA | `/تسجيل-النساء-داخل-المملكة/` | `page-women-registration.php` | 200 |
| 13 | تسجيل الرجال خارج المملكة | Men's Registration — International | `/تسجيل-الرجال-خارج-المملكة/` | `page-men-global-registration.php` | 200 |
| 14 | تسجيل النساء خارج المملكة | Women's Registration — International | `/تسجيل-النساء-خارج-المملكة/` | `page-women-global-registration.php` | 200 |
| 15 | التسجيل لغير الناطقين بالعربية | Registration — Non-Arabic Speakers | `/التسجيل-لغير-الناطقين-بالعربية/` | `page-non-arabic-registration.php` | 200 |
| 16 | Registration (English) | — | `/registration-english/` | `page-english-registration.php` | 200 |
| 17 | Registration (French) | — | `/registration-french/` | `page-french-registration.php` | 200 |
| 18 | Registration (Italian) | — | `/registration-italian/` | `page-italian-registration.php` | 200 |
| 19 | Registration (Urdu) | — | `/registration-urdu/` | `page-urdu-registration.php` | 200 |
| 2 | مثال على صفحة | Sample Page | `/مثال-على-صفحة/` | default | **404** ⚠ |

**Posts (1):** `أهلا-بالعالم/` — the default WordPress "Hello World" post. ⚠ Should be deleted.
**Taxonomy (1):** `/category/غير-مصنف/` (Uncategorised) — 200, indexable, no real content. ⚠

### ⚠ Defects in the sitemap itself

- **Page 2 (`مثال على صفحة`) is listed in `wp-sitemap.xml` but returns 404.** WordPress is
  advertising a broken URL to search engines.
- The default "Hello World" post and "Uncategorised" category are live and indexable —
  standard install debris that signals an unmaintained site to crawlers.

---

## 3. Broken and dead internal links

| Link text | `href` | Status | Appears on |
|---|---|---|---|
| عرض كافة الأسئلة (View all questions) | `/الأسئلة-الشائعة/` | **404** | Homepage FAQ |
| المصادر والمعرفة (Resources & Knowledge) | `#` | **Dead** | All 14 pages (main nav) |
| الخرائط الذهنية | `/الخرائط-الذهنية/` | 301 → canonical | Homepage |

The first two are user-facing failures on the highest-traffic page.

---

## 4. Navigation structure

Identical header and footer on all 14 pages.

**Header — main menu**
```
الرئيسية (Home)                    → /
عن المنصة (About)                  → /عن-المنصة/
المصادر والمعرفة (Resources)       → #            ⚠ DEAD
الخرائط الذهنية… (Mind Maps)       → /الخرائط-الذهنية-لتحفيظ-القرأن-الكريم/
السياسات واللوائح (Policies)       → /السياسات-واللوائح/
```

**Header — "بوابة التسجيل" (Registration Portal) dropdown**
```
الطلاب والطالبات (Students)
  └ التسجيل الآن                   → /#registration   (triggers smart router)
الكادر التعليمي (Teaching staff)
  ├ تسجيل المعلمين  (Male teachers)   → goo.gl/forms/FO4dBRij0buhezgF3
  └ تسجيل المعلمات  (Female teachers) → goo.gl/forms/artmNJBAb9yE9OJ42
الإشراف (Supervision)
  ├ تسجيل المشرفين  (Male supervisors)   → docs.google.com/forms/d/e/1FAIpQLSeNrT2BJ2…
  └ تسجيل المشرفات  (Female supervisors) → forms.gle/xUm7QUnc37q1HpHD7
```

Mobile uses the same tree in a slide-in panel (`#mobile-panel`, translate-X transition).

**Footer — روابط هامة (Important links)**
Policies · About · Mind Maps · the 4 staff Google Forms

**Footer — تواصل معنا (Contact)**
`966539065696` (tel) · `info@itqan-quran.com` (Cloudflare-obfuscated) ·
المملكة العربية السعودية، الرياض (Riyadh, Saudi Arabia)

**Persistent** — floating WhatsApp button (`wa.me/966539065696`) and a
"ابدأ حفظ القرآن اليوم / سجّل الآن" CTA band above the footer on every page.

---

## 5. Authenticated / hidden surface

| Path | Result | Note |
|---|---|---|
| `/wp-login.php` | 200 | Standard WP login — exposed |
| `/wp-admin/` | 302 → `wp-login.php` | Standard WP admin |
| `/dashboard`, `/admin`, `/login` | 302 → `wp-admin` | WP convenience redirects, **not an LMS** |
| `/xmlrpc.php` | Exposed | ⚠ Should be disabled |
| `/wp-json/` | Open | REST API readable unauthenticated |

**Probed and confirmed absent (404):** `/student`, `/teacher`, `/instructor`, `/register`,
`/my-account`, `/courses`, `/course`, `/lessons`, `/lms`, `/portal`, `/profile`, `/quiz`,
`/certificate`, `/signin`, `/sign-up`, `/account`, `/members`, `/membership`, `/enroll`,
`/payment`, `/checkout`, `/cart`.

**There is no LMS, no e-commerce and no member area on `itqan-quran.com`.**

---

## 6. LMS surface — `register.itqan-quran.com`

Publicly reachable without credentials:

| Path | Purpose |
|---|---|
| `/Account/Login` | Passwordless login (email + emailed code) |
| `/Account/Login?l={ar,en,fr,id,SML,ur,ru}` | Locale switch — 7 locales |
| `/Account/Reset` | Account recovery |
| `/Account/Register?i=<GUID>` | Track-specific registration (36 GUIDs mapped) |
| `/ClosedCircleType/CreateNeedToRegisterdUser?circleTypeId=<int>` | Waitlist capture for closed tracks |
| `/Home/About` | Version footer — `© 1448 - v1.2.3.4` |
| `/` | 302 → `/Account/Login?ReturnUrl=%2F` — everything else is login-walled |

Full track catalogue with GUIDs, internal IDs and open/closed status: `08-lms.md`.

---

## 7. Proposed sitemap for the rebuild

Adds what is missing, fixes what is broken, and introduces locale routing.

```
/                                   Home (router entry)
/about                              About
/policies                           Policies & Regulations
/faq                        ✚ NEW   Full FAQ — fixes the 404
/resources                  ✚ NEW   Resources hub — fixes the dead nav item
  /resources/mind-maps              Mind maps (7 downloads, self-hosted)
  /resources/study-plans    ✚ NEW   4 memorisation plans (self-hosted, off quranlives.com)
/register                   ✚ NEW   Server-rendered router — works without JS
  /register/men-ksa                 Men — inside KSA
  /register/women-ksa               Women — inside KSA
  /register/men-international       Men — outside KSA
  /register/women-international     Women — outside KSA
  /register/non-arabic              Non-Arabic speakers hub
/join                       ✚ NEW   Staff recruitment hub (replaces 4 loose Google Forms)
  /join/teachers  ·  /join/supervisors
/contact                    ✚ NEW   Real contact page (currently only an anchor)
```

With locale prefixes `/[locale]/…` for the agreed language set — see `09-user-flows.md` §6
for the locale consolidation proposal.

**Removed:** Sample Page, Hello World post, Uncategorised category.
