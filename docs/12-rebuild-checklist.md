# 12 — Rebuild Checklist

Ordered by **business impact per unit of effort**, not by technical tidiness.

> **The framing that matters:** the site's biggest problem is not its design. It is that
> **61% of registration journeys end in a dead end that cannot even collect an email
> address.** Phase 0 below is worth more than the entire visual rebuild, and most of it can
> ship in days on the existing WordPress site.

---

## Phase 0 — Fix the bleeding (days, on the current site)

Do these before any rebuild. None require the new stack.

| # | Task | Impact | Effort |
|---|---|---|---|
| 0.1 | **Add `email` + consent to the LMS waitlist form** | 🔴 Critical — recovers 61% of lost intent | S |
| 0.2 | **Mark closed tracks on the four registration pages** — badge each card open/full | 🔴 Critical — stops sending users into dead ends | S |
| 0.3 | **Warn on the women's path** before the 3-step flow, or route straight to the waitlist | 🔴 Critical | S |
| 0.4 | **Fix the FAQ 404** — build `/الأسئلة-الشائعة/` or remove the CTA | 🟠 High | S |
| 0.5 | **Fix or remove the dead `المصادر والمعرفة` nav item** (all 14 pages) | 🟠 High | S |
| 0.6 | **Correct the women's WhatsApp number** (currently identical to men's) | 🟠 High | XS |
| 0.7 | **Add analytics** (Plausible/Matomo) — establish a baseline | 🟠 High | S |
| 0.8 | **Add a login link** for returning students | 🟠 High | XS |
| 0.9 | Add meta descriptions + OG tags (WhatsApp shares are the main channel) | 🟠 High | S |
| 0.10 | Fix the `http://` study-plan PDF link | 🟠 High | XS |
| 0.11 | Delete the Sample Page, Hello World post, Uncategorised category | 🟡 Medium | XS |
| 0.12 | Fix `القرأن` → `القرآن` in the mind-maps title, nav, H1 and footer | 🟡 Medium | S |
| 0.13 | Compress `logo.png` (300 KB) and `license.jpg` (249 KB) | 🟡 Medium | XS |
| 0.14 | Add `prefers-reduced-motion` to the stylesheet | 🟡 Medium (a11y) | XS |
| 0.15 | Raise with the client: **.NET 5 is end-of-life** | 🔴 Critical (security) | — |
| 0.16 | Raise with the client: **no guardian consent for children aged 3+** | 🔴 Critical (legal) | — |

---

## Phase 1 — Foundation

- [ ] Next.js (App Router) + TypeScript; RTL-first
- [ ] Port design tokens from `04-design-system.md` verbatim
- [ ] **Add accessible gold** (`--color-gold-text: #7a6318`) — current gold is 1.9:1
- [ ] Self-host Amiri + Tajawal, subset per locale, `font-display: swap`
- [ ] Replace Font Awesome CDN with an inline SVG sprite (~25 icons)
- [ ] `prefers-reduced-motion` honoured across every animation
- [ ] Focus-visible rings on every interactive element
- [ ] i18n scaffolding for the 8-locale set (`09-user-flows.md` §6), per-locale `dir`/`lang`
- [ ] Component library per `03-components.md`
- [ ] CI: lint, typecheck, Lighthouse budget, axe-core

## Phase 2 — Content

- [ ] Migrate all copy from `06-copywriting.md` — **verify Arabic diacritics survive**
- [ ] Fix the 13 copy defects in `06-copywriting.md` §17
- [ ] Standardise on one brand spelling
- [ ] Home, About, Policies, Mind Maps, 4× Arabic registration, non-Arabic hub, 4× language
- [ ] ✚ `/faq` — expanded (see Phase 6)
- [ ] ✚ `/resources` — fixes the dead nav item
- [ ] ✚ `/contact` — a real page
- [ ] ✚ `/join` — staff recruitment hub
- [ ] Self-host the 4 study plans (compress from ~10 MB each) and 7 mind maps
- [ ] Add a "last updated" date and version to the policy page
- [ ] ✚ Privacy policy and cookie policy — **currently absent despite collecting PII**

## Phase 3 — The registration router

- [ ] Server-rendered `/register` — **works without JavaScript**
- [ ] Replace the phone step with Country + Language selects (IP-hinted, overridable)
- [ ] **Consume `GET /api/v1/tracks` for live availability** *(`11-api-inference.md` §2)*
- [ ] Availability badge on every track card: open / places left / full + reopening date
- [ ] Inline waitlist capture on closed tracks — name, **email**, WhatsApp, age, language
- [ ] ✚ Guardian branch for under-18 tracks
- [ ] Record consent with timestamp, IP and policy version
- [ ] Progress indicator, back navigation, `sessionStorage` persistence
- [ ] Modal a11y: `<dialog>`, focus trap, Escape, focus restoration
- [ ] Instrument every step

## Phase 4 — Forms

- [ ] Replace the 4 staff Google Forms with `/join/teacher` and `/join/supervisor`
- [ ] Replace the 3 non-Arabic Google Forms with the LMS flow *(honours terms clause 2)*
- [ ] Contact form with routing and confirmation
- [ ] ✚ Feedback form *(fulfils terms clause 7, which invites feedback with no mechanism)*
- [ ] ✚ "Notify me when registration reopens"
- [ ] Every field labelled; real localised error messages; `aria-live` on validation
- [ ] CSRF, rate limiting, spam protection, server-side validation
- [ ] Confirmation email on every submission

## Phase 5 — LMS integration

- [ ] **Obtain source access and role credentials** *(`08-lms.md` §9)* — blocks the rest
- [ ] Build/expose `GET /api/v1/tracks`
- [ ] Build `POST /api/v1/waitlist` with email capture
- [ ] Automated reopening notifications to waitlisted users
- [ ] Admin capacity dashboard
- [ ] Unify locales across site and LMS
- [ ] Replace Nunito with Tajawal/Amiri in the LMS
- [ ] Use GUIDs on the waitlist route — stop leaking integer `circleTypeId`
- [ ] Replace `data-val-required="*"` with real messages
- [ ] Add `<label>` to `HefzDailyCount`, `HefzDuration`, `AcademicAdvertiseWay`
- [ ] **Migrate .NET 5 → current LTS**

## Phase 6 — Content gaps

- [ ] **Expanded FAQ** answering what prospects actually ask:
      cost · session length and frequency · weekly schedule · technical requirements ·
      certificate details and recognition · minimum commitment · what happens if you miss a
      session · how children are supervised · how teachers are vetted · what "nominal
      pricing" means in practice
- [ ] **A pricing/support page** — `بأسعار رمزية` currently appears only inside a marquee
- [ ] Link the Maknoon store referenced in terms clause 6
- [ ] Teacher profiles — no human faces appear anywhere today
- [ ] LMS screenshots — students currently register having never seen the platform
- [ ] Testimonials — none exist
- [ ] Embed video from the linked YouTube channel
- [ ] Standardise study-plan descriptions: duration · daily rate · starting point · file size

---

## Accessibility checklist

- [ ] **`prefers-reduced-motion`** on all 11 animation classes *(none today)*
- [ ] **Gold contrast** — never use `#d4af37` for text (1.9:1)
- [ ] Typewriter headings render real text in the DOM *(currently empty until JS)*
- [ ] Marquee pausable *(WCAG 2.2.2)*, clones `aria-hidden`
- [ ] Modals: focus trap, `role="dialog"`, `aria-modal`, Escape, focus restoration
- [ ] Accordion: `aria-expanded`, `aria-controls`
- [ ] Every form field labelled; errors linked via `aria-describedby`
- [ ] Correct `dir` and `lang` per locale *(EN/FR/IT pages are currently `dir="rtl" lang="ar"`)*
- [ ] Full keyboard operability; visible focus throughout
- [ ] Target: **WCAG 2.1 AA** — appropriate for a platform with a ذوي الهمم track

## Performance budget

| Metric | Now | Target |
|---|---:|---:|
| Homepage HTML | 187 KB | < 50 KB |
| Images | 878 KB | < 150 KB |
| CSS | ~230 KB | < 40 KB |
| JS | ~280 KB | < 50 KB |
| External origins | 14 | 4 |
| LCP | — | < 2.0 s |
| CLS | — | < 0.1 |
| Lighthouse a11y | — | ≥ 95 |

- [ ] Dequeue unused WordPress inline CSS (block library, global styles, emoji)
- [ ] AVIF/WebP + `srcset` + lazy loading
- [ ] Self-host and subset fonts

## SEO

- [ ] Meta description on every page *(0 of 14 today)*
- [ ] Open Graph + Twitter Card + share image *(0 of 14 — WhatsApp is the main channel)*
- [ ] JSON-LD: `EducationalOrganization`, `Course`, `FAQPage`, `BreadcrumbList` *(none today)*
- [ ] `hreflang` across the locale set
- [ ] Canonical URLs; regenerate the sitemap after deleting the 404'd Sample Page
- [ ] Resolve About/Home content duplication
- [ ] Remove `<meta name="generator">`

## Security

- [ ] Disable `xmlrpc.php`; restrict `/wp-json/wp/v2/users`
- [ ] CSP, HSTS, `X-Frame-Options`, `Referrer-Policy`
- [ ] **Migrate off end-of-life .NET 5**
- [ ] Rate-limit login-code issuance; hash codes; 10-minute expiry
- [ ] Audit-log admin mutations
- [ ] Define retention and deletion for minors' data

## Launch

- [ ] 301 map for all 14 Arabic-slug URLs — **percent-encoded Arabic slugs must be preserved**
- [ ] Verify every one of the 36 track GUIDs still resolves
- [ ] Test all 8 locales for `dir`, fonts and diacritics
- [ ] Verify registration with **JavaScript disabled**
- [ ] Real-device test: low-end Android, iOS Safari, slow 3G
- [ ] Screen-reader pass in Arabic (NVDA/VoiceOver)
- [ ] Confirm analytics fires on every funnel step
- [ ] Rollback plan

---

## Open questions for the client

These block real work and should be asked now:

1. **Why are all women's tracks closed?** Capacity, teacher shortage, or a policy decision?
   The answer changes whether the fix is technical or operational.
2. **When do tracks reopen?** Even an approximate Hijri month makes the waitlist far more
   effective than "full".
3. **Is the platform free?** No pricing or gateway exists; `بأسعار رمزية` suggests nominal
   fees. Is payment planned?
4. **What consent is obtained for children aged 3–17?** There is no guardian field anywhere.
   This is the most urgent question in this list.
5. **Can we get LMS source access and role credentials?** Blocks Phase 5 and would replace
   the inference in `10` and `11` with fact.
6. **Which video platform hosts the live halaqat?** Integration may be valuable.
7. **Who controls `quranlives.com`?** 40 MB of study plans depend on it.
8. **Which locales actually matter commercially?** Three inconsistent sets exist today.
9. **Are the Maknoon certificates formally accredited,** and can they be verified publicly?
10. **Is there an existing analytics account** we have not detected?
