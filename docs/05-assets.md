# 05 — Asset Inventory

Every asset referenced by the public site. Sizes measured live 2026-08-20.

---

## 1. Images hosted on `itqan-quran.com`

| File | Size | Dimensions/Type | Used on | Note |
|---|---:|---|---|---|
| `uploads/2026/01/logo_itqan.png` | 39 KB | PNG | Header + footer, all pages | Primary logo |
| `uploads/2026/01/fav_itqan.png` | 11 KB | PNG 192×192 | Favicon / Apple touch | |
| `uploads/2026/01/fav_itqan-142x150.png` | — | PNG 32×32 | Favicon | Odd source ratio |
| `themes/itqan-theme/assets/images/logo.png` | **300 KB** | PNG | About section | ⚠ **Oversized** |
| `themes/itqan-theme/assets/images/license.jpg` | **249 KB** | JPEG | Hero licence badge | ⚠ **Oversized** |
| `…/open-mushaf-white.svg` | 1 KB | SVG | Hero icon | ✅ Well optimised |
| `…/part-30.jpg` | 34 KB | JPEG | Juz' Amma card | |
| `…/part-29.jpg` | 34 KB | JPEG | Juz' Tabarak card | |
| `…/part-28.jpg` | 35 KB | JPEG | Juz' Qad Sami'a card | |
| `…/part-27.jpg` | 35 KB | JPEG | Juz' Adh-Dhariyat card | |
| `…/part-1.jpg` | 35 KB | JPEG | Juz' 1 card | |
| `…/part-2.jpg` | 35 KB | JPEG | Juz' 2 card | |
| `…/part-all.jpg` | 70 KB | JPEG | Complete file card | |

**Total site images: ~878 KB**, of which **549 KB (63%) is two files** — `logo.png` and
`license.jpg`.

### ⚠ Defects

- **`logo.png` at 300 KB** is a logo. It should be an SVG (likely < 10 KB) or an optimised
  PNG under 30 KB. This is the single heaviest asset on the site.
- **`license.jpg` at 249 KB** is a small badge thumbnail. Should be ~30 KB WebP.
- **No modern formats.** Zero WebP or AVIF. Converting all JPEGs and PNGs would cut roughly
  60–70% of image weight.
- **No `srcset` / `sizes`.** Mobile downloads full-size desktop assets.
- **No lazy loading** attributes observed on below-the-fold thumbnails.
- Favicon derives from a `142x150` crop for a `32x32` slot — non-square source.

**Projected after optimisation: ~878 KB → ~150 KB (-83%).**

---

## 2. ⚠ PDFs hosted on a third-party domain

The four study plans are **not** on `itqan-quran.com`. They are served from
`quranlives.com`, an unrelated domain.

| Plan | Size | URL |
|---|---:|---|
| خطة حفظ القرآن خلال 5 أشهُر | **9.9 MB** | `https://quranlives.com/…/خمسة-أوجه-من-البقرة-5-أشهر.pdf` |
| خطة حفظ القرآن خلال 6 أشهُر | **10.0 MB** | `https://quranlives.com/…/ثلاثة-أوجه-وربع-من-الناس-6-أشهر.pdf` |
| خطة حفظ القرآن خلال 10 أشهُر | **10.2 MB** | `https://quranlives.com/…/وجهان-من-الناس-_-10-أشهر.pdf` |
| خطة حفظ القرآن خلال 14 أشهُر | **10.4 MB** | `http://quranlives.com/…/وجه-ونصف-يوميا-_-14-شهرا.pdf` ⚠ **`http://`** |

**Total: 40.5 MB on a domain the academy does not appear to control.**

Risks, in order of severity:
1. **One link is plain `http://`** — mixed content; browsers will warn or block, and the
   download is interceptable.
2. **No control over availability.** If `quranlives.com` moves, expires or reorganises its
   uploads folder, all four plans die silently.
3. **No control over content.** A third party can change what the academy's students receive.
4. **~10 MB each with no size warning** — punishing on mobile data, which matters directly
   for the international student base this site is trying to serve.

**Required fix:** obtain the source files, compress them (10 MB Arabic PDFs are almost
certainly uncompressed scans — expect 1–2 MB after optimisation), self-host, serve over
HTTPS from a CDN, and display file size and page count on the download button.

---

## 3. ⚠ Google Drive downloads

Seven mind maps, all as Drive `/view` links rather than files:

| Mind map | Drive ID | `usp` param |
|---|---|---|
| جزء عم | `1YQ7KGkAfoCpoh4iyvbM517WqTbCap9Nr` | `sharing` |
| جزء تبارك | `1RX82zZlw-0N2IaJFYiGllbRqrhGDua8_` | `sharing` |
| جزء قد سمع | `1x6EGatntygV_nVBzkDndQtBm4alMJsI9` | `sharing` |
| جزء الذاريات | `1SS1hiDMigiTjlrcMdrmwiLG1xJ0lGNnk` | `share_link` |
| الجزء الأول | `1FQJOymTyZPwdsFkSAg1zwBqmecz_9y3E` | `sharing` |
| الجزء الثاني | `1I00pIibr2RpwKEX8I-LJufGqX3uGL074` | `drivesdk` |
| ملف شامل | `10hqQTtn3nGyu9qS3Q9w300Q7-P95vyJT` | `sharing` |

**Defects:** these are preview pages, not downloads — an extra step, and some users hit a
Google sign-in wall · no file size, format or page count shown · no download analytics · no
versioning · the three different `usp` values reveal ad-hoc manual link copying · Drive is
rate-limited on popular files.

**Fix:** self-host alongside the study plans; keep Drive only as a mirror.

---

## 4. Third-party origins

| Origin | Purpose | Blocking? | Recommendation |
|---|---|---|---|
| `cdnjs.cloudflare.com` | Font Awesome 7.0.0 (full CSS) | **Yes** | Inline used icons as SVG; drop |
| `fonts.googleapis.com` | Amiri + Tajawal via CSS `@import` | **Yes** | Self-host, subset, `font-display: swap` |
| `cdn.jsdelivr.net` | intl-tel-input 18.2.1 CSS + JS + `utils.js` | Partly | Removed if the phone step is replaced |
| `quranlives.com` | 4 study-plan PDFs (40 MB) | No | **Self-host — see §2** |
| `drive.google.com` | 7 mind maps | No | **Self-host — see §3** |
| `docs.google.com` / `forms.gle` / `goo.gl` | 7 registration/recruitment forms | No | Migrate into the platform |
| `register.itqan-quran.com` | The LMS | No | Keep |
| `wa.me` / `api.whatsapp.com` | Support | No | Keep |
| `youtube.com/@-Itqan-quran01` | Channel link | No | Keep |
| `s.w.org` | WP emoji sprites | No | **Disable** — unused, WP default |
| `www.google.com/recaptcha` | reCAPTCHA v3 (LMS only) | No | Keep on LMS |
| `linkedin.com/in/engamreldeeb` | Developer credit | No | Keep |
| `upload.wikimedia.org` | Flag/partner imagery | No | Self-host |

**Count: 14 external origins.** Each is a DNS + TLS round trip and, for European users, a
data-transfer disclosure obligation. Target: **4** (`register.` subdomain, WhatsApp,
YouTube, reCAPTCHA).

---

## 5. Code assets

| File | Size | Note |
|---|---:|---|
| `itqan-theme/style.css` | 86 KB | Compiled Tailwind v4 — not obviously purged |
| `itqan-theme/assets/js/main.js` | 18 KB | Unminified; ~60 lines are commented-out dead code |
| Font Awesome CSS | ~100 KB+ | Full build via CDN |
| intl-tel-input CSS + JS + utils | ~250 KB+ | `utils.js` alone is large |
| WordPress inline CSS | ~40 KB | Block library + global styles injected into every page |

**Homepage HTML is 187 KB uncompressed** — largely WordPress inlining its full block-library
and global-styles CSS on a page that uses no blocks.

**Fixes:** dequeue `wp-block-library`, `classic-theme-styles`, `global-styles` and emoji
scripts (this theme uses none of them) · purge and minify Tailwind · minify `main.js` and
delete the dead counter module · drop Font Awesome and intl-tel-input.

---

## 6. Missing assets

| Missing | Impact |
|---|---|
| **OG / social share image** | Every share on WhatsApp — the academy's primary channel — renders as a bare link |
| Logo as SVG | Forces the 300 KB PNG |
| `site.webmanifest` | No installable PWA / add-to-home-screen |
| `favicon.ico` | Legacy fallback absent |
| Teacher/staff photography | No human faces anywhere; weakens trust for an education brand |
| Screenshots of the LMS | Students register blind, never having seen the platform |
| Video (channel exists) | YouTube is linked but nothing is embedded |

---

## 7. Asset budget for the rebuild

| Category | Now | Target |
|---|---:|---:|
| Images | 878 KB | < 150 KB |
| CSS | ~230 KB | < 40 KB |
| JS | ~280 KB | < 50 KB |
| Fonts | ~200 KB (external) | < 120 KB (self-hosted, subset) |
| PDFs | 40 MB (third-party) | < 8 MB (self-hosted) |
| External origins | 14 | 4 |
| **Homepage transfer** | **~1.2 MB+** | **< 350 KB** |
