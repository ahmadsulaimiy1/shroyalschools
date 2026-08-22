# Itqan Virtual Quran Academy — Web (V2)

Rebuild of the `itqan-quran.com` marketing site and registration router, built
to the specification in [`../docs`](../docs).

**Stack:** Next.js 15 (App Router) · React 19 · TypeScript · Tailwind v4 · RTL-first · 8 locales

```bash
npm install
npm run dev        # http://localhost:3000 → redirects to /ar
npm run build      # production build
npm run typecheck  # tsc --noEmit
```

---

## What this fixes

Every item below was a **verified defect** on the live V1 site, cross-referenced
to the audit document that recorded it.

| # | V1 defect | Fix | Ref |
|---|---|---|---|
| 1 | **61% of registration journeys dead-ended.** 22 of 36 entry points were full; nothing indicated which. | Every track carries an availability badge **before** the user leaves the site. Closed tracks route to a waitlist, never to the LMS. | `docs/08` §4.6 |
| 2 | **Waitlist captured no email** — the academy could not tell anyone a track had reopened. | `email` + explicit contact consent are required fields. | `docs/07` §4 |
| 3 | **Registration was JavaScript-only** (`onsubmit="return false;"`). JS off = no registration path at all. | Router is three plain **GET forms**, fully server-rendered. State lives in the URL. | `docs/03` §1 |
| 4 | FAQ "عرض كافة الأسئلة" CTA → **HTTP 404**. | `/[locale]/faq` exists, with 12 questions covering cost, schedule, tech requirements and certification. | `docs/01` §3 |
| 5 | `المصادر والمعرفة` was `href="#"` — dead nav item on all 14 pages. | `/[locale]/resources` hub → mind maps + study plans. | `docs/01` §3 |
| 6 | **No meta description, OG, or structured data** on any page. | Per-page metadata, Open Graph, `EducationalOrganization` + `FAQPage` JSON-LD, sitemap with `hreflang`. | `docs/00` #5 |
| 7 | English/French/Italian pages served as `dir="rtl" lang="ar"`. | Correct `dir` and `lang` per locale, set on `<html>`. | `docs/02` §2.7 |
| 8 | Gold `#d4af37` used for text at **1.9:1** contrast. | `--color-gold` is decorative-only; `--color-gold-text` (#7a6318) for text. | `docs/04` §1 |
| 9 | **No `prefers-reduced-motion`** anywhere, on a site with a ذوي الهمم track. | All motion gated; full reduce override. | `docs/04` §5 |
| 10 | Required fields errored with `*`; three had no `<label>`. | Specific localised messages, every field labelled, `role="alert"` + `aria-describedby`. | `docs/07` §3 |
| 11 | Marquee unpausable; mobile menu had no focus trap. | Marquee pauses on hover/focus with clones `aria-hidden`; nav uses native `<dialog>`. | `docs/03` §2, §10 |
| 12 | Headings were **empty in the DOM** until JS typed them. | Real text server-rendered. | `docs/03` §6 |
| 13 | Phone number collected purely to read a country code, then discarded. | Country + language asked directly — no PII collected to make a routing decision. | `docs/03` §1 |
| 14 | Internal `circleTypeId` leaked in closed-track URLs. | Only public GUID tokens appear in URLs and the API. | `docs/08` §3 |
| 15 | No login link anywhere for returning students. | Persistent sign-in link in header and footer. | `docs/09` §5 |
| 16 | Sitemap advertised a page that 404s. | Generated from real routes only. | `docs/01` §2 |
| 17 | 14-month study plan served over plain `http://`. | HTTPS; all four plans now state daily rate, starting point and file size. | `docs/05` §2 |
| 18 | Copy defects: `القرأن`→`القرآن`, `معلمين مؤهلين`→`معلمون مؤهلون`, `يسعد إدارة`→`تسعد إدارة`, goals merged into one string. | Corrected, each with a comment citing `docs/06` §17. | `docs/06` §17 |

## Deliberately not "fixed"

**The women's WhatsApp number.** V1 pointed both the men's and women's buttons at
the same number. We cannot invent a second one, and relabelling a single number as
two gendered channels would repeat the deception rather than fix it. Until
`NEXT_PUBLIC_WHATSAPP_WOMEN` is set, `/contact` shows **one honest general
channel**. Set the variable and the two gendered cards appear automatically.

## Verified

```
✓ Production build passes; all pages prerendered across 8 locales
✓ Men/KSA      → 7 open,  0 waitlist links, 7 LMS registration links
✓ Women/KSA    → 0 open,  7 waitlist links, 0 LMS registration links  ← the V1 dead-end
✓ Non-Arabic   → routes to the X11/G11 international halaqa
✓ Router works with JavaScript disabled (GET forms only)
✓ circleTypeId appears 0 times in HTML and 0 times in /api/tracks
✓ href="#" appears 0 times across all 8 pages
✓ Waitlist API rejects bad email / missing consent / unknown track (422)
✓ dir/lang correct on every locale
```

## Configuration

| Variable | Purpose | Without it |
|---|---|---|
| `NEXT_PUBLIC_WHATSAPP_MEN` | Men's / general WhatsApp | Falls back to the published number |
| `NEXT_PUBLIC_WHATSAPP_WOMEN` | Women's WhatsApp | One general channel shown instead of two |
| `WAITLIST_ENDPOINT` | In-Kingdom waitlist store | Validates and accepts; **does not persist** |
| `WAITLIST_TOKEN` | Bearer token for the above | — |

> **`WAITLIST_ENDPOINT` is intentionally unset.** Saudi PDPL expects children's
> personal data to remain inside the Kingdom, and this waitlist can carry a
> minor's details. Wiring a store before the hosting decision is made would
> recreate the exact cross-border exposure the audit flagged in V1, which routed
> registrations through Google Forms. See `docs/18` §3.

## Structure

```
src/
  app/[locale]/          layout (per-locale dir/lang), home, register, waitlist,
                         about, policies, faq, resources, contact, join
  app/api/tracks         public availability API (docs/11 §2)
  app/api/waitlist       waitlist intake with server-side validation
  lib/tracks.ts          all 36 verified tracks — GUIDs, codes, status
  lib/i18n.ts            8 locales with correct dir/lang
  lib/dictionary.ts      UI strings, fully translated per locale
  content/home.ts        verbatim Arabic copy, with docs/06 §17 corrections
```

## Not included

Assets (logo, licence badge, mushaf thumbnails) are **not** in this repo — they
belong to the academy. `docs/05` lists every original with its measured size and
the optimisation needed: the V1 logo was a **300 KB PNG** and should ship as SVG.
