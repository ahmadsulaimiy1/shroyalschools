# 02 — Page-by-Page Specification

One section per page: purpose, layout, sections, components, links, and defects.
Verbatim copy lives in `06-copywriting.md`; components in `03-components.md`.

**Global shell (all 14 pages):** `<html dir="rtl" lang="ar">`, sticky header that shrinks on
scroll, mobile slide-in menu, registration-portal dropdown, CTA band, footer, floating
WhatsApp button. Only the `<main>` content differs.

---

## 2.1 Home — `/` (ID 7, `front-page.php`)

The only page with meaningful interactivity. ~187 KB of HTML; 12 stacked sections.

| # | Section | Purpose | Key components |
|---|---|---|---|
| 1 | Hero | Identity + primary CTA | H1, subtitle, "ابدأ رحلتك الآن" → `#registration`, "تواصل معنا" → `#contact`, licence thumbnail (click to enlarge) |
| 2 | عن المقرأة (About) | Who we are | Logo, body copy, Maknoon supervision badge |
| 3 | الرؤية والرسالة والأهداف | Vision / Mission / Goals | 3-card grid |
| 4 | ماذا نقدم (What we offer) | Service catalogue | 6-card `stagger-grid`: memorisation, recitation correction, review, tajweed, beginners (Nooraniyah), learning tracks |
| 5 | مزايا (Advantages) | Trust building | 8 items with icons |
| 6 | تقسيم حلقات المقرأة | The 7 age/needs tracks | 7 cards, each with age band + 2–3 bullets |
| 7 | الجداول والخطط | 4 memorisation plans | 4 PDF download cards (5 / 6 / 10 / 14 months) |
| 8 | Partners marquee | Social proof | `animate-marquee`, Maknoon + Iqra Al-Khurmah |
| 9 | **`#registration`** | **The router** | Gender selector → terms modal → phone modal → language modal |
| 10 | شروط القبول والتسجيل | Terms (7 clauses) | Rendered inside the terms modal |
| 11 | الأسئلة الشائعة (FAQ) | 4 accordion Q&As | ⚠ "View all" → **404** |
| 12 | `#contact` | Contact channels | 2 WhatsApp cards ⚠ **same number**, phone, email |

**Section 9 — the smart registration router** is the site's single most important
component. Full behavioural spec in `03-components.md` §1 and `09-user-flows.md` §1.

Routing targets are held in a hidden `<div id="reg-config">` with nine `data-*` attributes
(`data-ksa-m`, `data-ksa-w`, `data-glb-m`, `data-glb-w`, `data-lang-en`, `data-lang-fr`,
`data-lang-it`, `data-lang-ur`, `data-na`) — a clean PHP→JS handoff worth preserving.

**Defects:** FAQ "view all" 404 · both WhatsApp cards use `966539065696` · registration is
JS-only · 4 plan PDFs are ~10 MB each on `quranlives.com`, one over `http://` · statistics
counter shipped but commented out.

---

## 2.2 About — `/عن-المنصة/` (ID 8, `page-about.php`)

Static narrative. Sections: hero (`منصة قرآنية إلكترونية`), رؤيتنا (Vision), رسالتنا
(Mission), 🏆 أهداف المقرأة (Goals), 🤍 لماذا مِقْرَأَة إتقان؟ (Why Itqan).

Substantially **duplicates homepage sections 2–5**. Two H3s use emoji as heading glyphs
(🏆, 🤍) — decorative, unlabelled to assistive tech.

**Defects:** content duplication with home (thin-content SEO risk, two pages competing for
the same query) · no meta description · emoji-in-heading.

---

## 2.3 Policies — `/السياسات-واللوائح/` (ID 9, `page-policy.php`)

H1 `اللوائح والسياسات`, then `شروط القبول والتسجيل (اتفاقية التسجيل)` — the registration
agreement in 7 numbered clauses (أولًا…سابعًا): mission scope, registration mechanism,
general rules, commitment, data accuracy, support, feedback.

This is the **same text** rendered inside the homepage terms modal. Single-source it.

**Defects:** duplicated verbatim on the homepage · no "last updated" date — a dated policy
is expected for an agreement users are asked to accept · no privacy policy or cookie policy
despite collecting name, email, phone and age, and running Cloudflare + reCAPTCHA + Google
Fonts. **This is a compliance gap, not a cosmetic one.**

---

## 2.4 Mind Maps — `/الخرائط-الذهنية-لتحفيظ-القرأن-الكريم/` (ID 10, `page-downloads.php`)

Seven download cards, each with a thumbnail and a "تحميل الملف" button:

| Card | Thumbnail | Destination |
|---|---|---|
| جزء عم (Juz' Amma) | `part-30.jpg` | Drive `1YQ7KGkAfoCpoh4iyvbM517WqTbCap9Nr` |
| جزء تبارك (Juz' Tabarak) | `part-29.jpg` | Drive `1RX82zZlw-0N2IaJFYiGllbRqrhGDua8_` |
| جزء قد سمع | `part-28.jpg` | Drive `1x6EGatntygV_nVBzkDndQtBm4alMJsI9` |
| جزء الذاريات | `part-27.jpg` | Drive `1SS1hiDMigiTjlrcMdrmwiLG1xJ0lGNnk` |
| الجزء الأول (Juz' 1) | `part-1.jpg` | Drive `1FQJOymTyZPwdsFkSAg1zwBqmecz_9y3E` |
| الجزء الثاني (Juz' 2) | `part-2.jpg` | Drive `1I00pIibr2RpwKEX8I-LJufGqX3uGL074` |
| ملف شامل (Complete file) | `part-all.jpg` | Drive `10hqQTtn3nGyu9qS3Q9w300Q7-P95vyJT` |

**Defects:** all 7 are Google Drive `/view` links, not direct downloads — an extra click,
a possible Google account wall, no file size or page count shown, no version control, and
zero download analytics · mixed `usp=` params (`sharing`, `share_link`, `drivesdk`) show
ad-hoc copy-pasting · thumbnails are unoptimised JPEGs.

---

## 2.5 Arabic registration pages (IDs 11–14)

Four structurally identical pages — the router's Arabic destinations.

| Page | H2 | Register links |
|---|---|---|
| Men KSA (11) | اختر المسار المناسب لك | 7 |
| Women KSA (12) | اختاري المسار المناسب لَكِ | 7 |
| Men International (13) | اختر المسار المناسب لك (دولي) | 7 |
| Women International (14) | اختاري المسار المناسب لَكِ (دولي) | 7 |

Each renders the same 7 track cards, differing only by the target GUID. Headings are
correctly gender-inflected in Arabic (`لك` vs `لَكِ`) — good localisation detail.

Cards: قسم الروضة والتأسيس · قسم المرحلة الابتدائية · قسم المرحلة المتوسطة والثانوية ·
قسم المرحلة الجامعية والشباب/والفتيات · قسم ما فوق الأربعين · قسم ذوي الهمم ·
قسم القراءات والإجازات.

Each card: title, age band, 2–3 bullets, "تسجيل الآن" →
`register.itqan-quran.com/Account/Register?i=<GUID>`. Also "عرض الشروط" → policies page.

### ⚠ Critical defect

**21 of these 28 links are closed.** All 7 women's KSA, all 7 women's international, and all
7 men's international tracks redirect to a waitlist. Only men's KSA (7/7) is open.

The pages give **no indication** which tracks are open. A user picks a track, leaves the
site, and only then discovers it is full. Per-card availability state is the single highest-
value fix on the site. Full catalogue: `08-lms.md`.

---

## 2.6 Non-Arabic hub — `/التسجيل-لغير-الناطقين-بالعربية/` (ID 15)

Four language blocks — English Speakers · Francophones · Parlanti italiano ·
اردو بولنے والے — each offering Students / Teachers (Men, Women) / Supervisors (Men, Women).

**Inconsistent with every other registration path:** these route to **Google Forms**, not
the LMS, while `/registration-english/` etc. route to the LMS. Two different systems for
the same task.

Distinct Google Forms observed: `1FAIpQLSciSGOLuEMxbLaEydBBEX_c0iN5bPdTw2ywpVsBhIXQtk5FVA`,
`1FAIpQLSdlaWJ-zteKtdgMIKzIYzg7ahf3zXOJjwXpf1iYnxVTVOrvTw`,
`1FAIpQLSdt77dBTf_C80iQMG-cOwAHtw4Uti_sspv_w_4kjT4wA1VbsQ`.

**Defects:** ⚠ **"Register", "Men", "Women", "Supervisors" are left in English inside the
French, Italian and Urdu blocks** — the localisation is incomplete · Google Forms bypasses
the LMS entirely, so these students exist in a spreadsheet, not the system · four languages
on one page with no anchor navigation.

---

## 2.7 Language registration pages (IDs 16–19)

`/registration-english/`, `/registration-french/`, `/registration-italian/`,
`/registration-urdu/` — minimal two-card pages (Men / Women → Register Now).

**All four pages link to the identical pair of GUIDs:**
- Men → `5c24212d-35b4-4996-8748-55422740a8b4` — **G11 Male International Halaqas**
- Women → `0118c82d-03e8-4ea1-a475-ee9be52aa23a` — **X11 Female International Halaqas**

So the four "language" pages are **presentational only** — every non-Arabic student lands in
the same two halaqas regardless of language. Both are **OPEN** (the only open international
tracks on the site).

**Defects:** page chrome remains `dir="rtl" lang="ar"` on the English, French and Italian
pages — LTR content inside an RTL document with the wrong `lang`, which is both a rendering
and a screen-reader defect · content is only ~10 words (thin content) · Italian has a
marketing page but **no Italian locale in the LMS login**.

---

## 2.8 Sample Page — `/مثال-على-صفحة/` (ID 2)

Default WordPress sample page. **Returns 404 but is still listed in `wp-sitemap.xml`.**
Delete the page and let the sitemap regenerate.

## 2.9 Hello World post + Uncategorised category

`أهلا-بالعالم/` (default post) and `/category/غير-مصنف/` are both live and indexable.
Install debris. Delete both; the blog is otherwise unused.

---

## 2.10 Cross-page summary

| Property | Status |
|---|---|
| Pages returning 200 | 13 of 14 |
| Pages with a meta description | **0** |
| Pages with Open Graph / Twitter Card | **0** |
| Pages with structured data (JSON-LD) | **0** |
| Pages with a canonical URL | Only via WP default |
| Pages with a dead nav item | **14 of 14** (`المصادر والمعرفة`) |
| Pages usable with JavaScript disabled | Content yes; **registration no** |
