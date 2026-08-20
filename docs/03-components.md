# 03 — Component Library

Every interactive and structural component on the public site, documented as observed and
respecified for the rebuild. Class names are the live ones from `itqan-theme/style.css`.

---

## 1. Smart Registration Router ⭐ *the critical component*

The site's core interaction. A 4-step wizard that determines which of 36 registration
endpoints a visitor belongs to, without ever asking them "are you inside Saudi Arabia?".

### Observed implementation

`assets/js/main.js`, ~150 lines. Markup: `<form id="smart-reg-form" onsubmit="return false;">`
plus three modals and a hidden `<div id="reg-config">` carrying nine `data-*` URLs.

### State machine

```
[Gender selector]  .gender-selector[data-gender="men"|"women"]
        │  sets selectedGender; resets terms checkbox; disables continue
        ▼
[#terms-modal]     full 7-clause agreement
        │  #terms-agree-check must be ticked → enables #btn-agree-terms
        ▼
[#phone-modal]     intl-tel-input, initialCountry "sa", separateDialCode
        │  #btn-check-number → iti.isValidNumber()
        │     invalid → show #phone-error, add !border-red-500, halt
        │     valid   → read iso2 country code
        ▼
   ┌────┴─────────────────────────────────────────┐
   │ iso2 === "sa"        → KSA form (by gender)  │
   │ iso2 ∈ arabCountries → Intl form (by gender) │
   │ otherwise            → [#lang-check-modal]   │
   └──────────────────────┬───────────────────────┘
                          ▼
        "نعم، أتحدث العربية"  → Intl form (by gender)
        "No, I don't"        → route by country to en/fr/it/ur, else non-Arabic hub
```

### Country tables (verbatim from source)

- **Arab (21):** `eg ae kw qa bh om ye lb jo ps iq dz ma tn ly sd mr so dj km sy`
- **English (10):** `us gb ca au nz ie za ng ph sg`
- **French (16):** `fr be ch mc sn ci cm ne bf ml gn bj tg ga cg cd`
- **Italian (3):** `it sm va`
- **Urdu (2):** `pk in`
- Anything else → `data-na` (non-Arabic hub)

### Defects

| Severity | Issue |
|---|---|
| **Critical** | **JS-only.** `onsubmit="return false;"` with no server fallback. JS off or failed = no registration path at all. |
| **Critical** | Women's routes lead to pages where **all 7 tracks are closed**. The router faithfully delivers users to a dead end. |
| High | Country → language is a **crude proxy for language**. A Pakistani in Germany gets the non-Arabic hub; `in` (India) → Urdu ignores Hindi, Tamil, Bengali and ~20 other languages; `za` (South Africa) → English ignores Afrikaans and Zulu. |
| High | **Phone number is collected but never used.** It is validated purely to read the country code, then discarded — a real privacy and UX cost (users hesitate to give a number) for information a country `<select>` or IP hint would provide. |
| Medium | No back navigation between steps; closing a modal loses all progress. |
| Medium | Loading state overwrites the button's `innerHTML` via `document.activeElement` — fragile and destroys any icon markup. |
| Medium | Failure path is `alert()` — untranslated, unstyled, non-accessible. |
| Medium | No focus trap in modals, no `aria-modal`, no Escape handler, focus not restored on close. |
| Low | `preferredCountries` omits `pk`/`in` despite an explicit Urdu route. |

### Respecification

**Keep the concept, invert the mechanics.**

1. **Server-render the whole flow** as `/register` with real form `POST`s. Progressive
   enhancement upgrades it to modals client-side.
2. **Replace the phone step with an explicit two-field step:** Country (searchable select,
   pre-selected from an IP hint) + Preferred language (independent of country). This is
   faster, more accurate, more private, and removes the intl-tel-input dependency.
3. **Query live availability before routing.** Never send a user to a closed track — show
   open tracks, and offer the waitlist inline for closed ones.
4. Add a progress indicator ("Step 2 of 3"), a back button, and persist state in
   `sessionStorage`.
5. Full modal a11y: focus trap, `role="dialog"`, `aria-modal="true"`, Escape to close,
   focus restoration.

---

## 2. Modal / Dialog

`openModal()` / `closeModal()` locate children by `id$="-overlay"` and `id$="-panel"`,
toggling `opacity-0` and `scale-95 → scale-100` with a 300 ms exit delay.

Instances: `#terms-modal`, `#phone-modal`, `#lang-check-modal`.

**Defects:** no focus management, no `aria-modal`/`role="dialog"`, no Escape key, no scroll
lock on `<body>`, timing coupled to a hard-coded 300 ms `setTimeout` that can desync from CSS.

**Rebuild:** native `<dialog>` with `showModal()` — focus trap, Escape and backdrop come free.

---

## 3. Sticky Header

Scroll past 50 px → adds `shadow-md bg-white/95`, container `py-4 → py-2`, logos
`transform: scale(0.85)`.

**Defect:** unthrottled `scroll` listener writing inline styles on every event — layout
thrash on low-end mobile.
**Rebuild:** `IntersectionObserver` on a sentinel, or a CSS-only `position: sticky` +
`animation-timeline: scroll()`. No scroll handler.

---

## 4. Mobile Menu

`#mobile-menu-btn` → `#mobile-menu-wrapper` / `#mobile-overlay` / `#mobile-panel`,
`-translate-x-full → translate-x-0`, 50 ms open / 300 ms close stagger.

**Defects:** no focus trap · no Escape · `<body>` still scrolls behind the panel · nested
`setTimeout`s duplicating CSS timing.

---

## 5. Animation Engine

`IntersectionObserver` (threshold 0.1, `rootMargin: 0px 0px -50px 0px`) adding `.active` to
`.anim-blur-in`, `.anim-slide-right`, `.anim-slide-left`, `.anim-pop-in`, `.stagger-grid`,
`.reveal-item`. `.stagger-grid` cascades `.anim-child` at 50 ms (mobile) / 100 ms (desktop).
A 100 ms failsafe force-activates anything already in viewport.

**Assessment:** the failsafe is a thoughtful fix for the classic "content invisible on fast
load" bug — keep the idea.

**Defect:** ⚠ **no `prefers-reduced-motion` support anywhere in the theme.** Users who have
asked their OS to reduce motion still get blur-ins, pop-ins, staggers, marquee and
typewriter. This is a WCAG 2.3.3 / vestibular-safety failure and the most important
accessibility fix in the component layer.

**Rebuild:** wrap all animation in `@media (prefers-reduced-motion: no-preference)`.

---

## 6. Typewriter Headings

`.typewriter-text[data-text]` types at 70 ms/char on 50% intersection, then `.typed-done`.

**Defects:** ⚠ **the heading is empty in the DOM until JS runs** — `<h2 data-text="…">`
starts blank, so crawlers and screen readers may see an empty heading; it is also the site's
main section-title mechanism, so this affects most H2s. · character-by-character mutation is
announced repeatedly by some screen readers · no reduced-motion opt-out.

**Rebuild:** render the real text in the DOM; animate with CSS only, `aria-hidden` on the
effect layer. Never let a heading depend on JS to have content.

---

## 7. Buttons

| Class | Style | Use |
|---|---|---|
| `.btn-primary` | Solid `#027043`, white text, rounded | Main CTAs |
| `.btn-gold` | Solid `#d4af37`, `shadow-glow` on hover | High-emphasis ("سجّل الآن") |
| `.btn-outline` | Transparent, primary border | Secondary ("عرض الشروط") |

**Defects:** no `:focus-visible` ring defined — keyboard users cannot see focus · no
disabled styling beyond the native attribute · gold `#d4af37` on white is **1.9:1 contrast**,
far below the 4.5:1 minimum, so gold text on light backgrounds fails WCAG AA.

---

## 8. Cards

Service (icon + title + text) · Track (title + age band + bullets + CTA) · Plan (PDF badge +
title + download) · Download (thumbnail + title + button) · Vision/Mission/Goal.

**Rebuild:** one `<Card>` with `variant` and `media` slots — five near-identical
implementations currently exist.

---

## 9. FAQ Accordion

Four `<button>`-triggered disclosures on the homepage.

**Defects:** no `aria-expanded` / `aria-controls` · "View all" → **404** · only 4 of an
unknown total exposed.

---

## 10. Partners Marquee

`.animate-marquee`, infinite horizontal scroll, content duplicated 4× in markup.

**Defects:** no pause on hover/focus · no reduced-motion opt-out · duplicated text read 4×
by screen readers (needs `aria-hidden` on the clones) · WCAG 2.2.2 (moving content must be
pausable) not met.

---

## 11. Gold Checkbox

`.gold-checkbox` — custom-styled terms consent. Gates `#btn-agree-terms`.
**Defect:** custom appearance with no visible `:focus-visible` state.

---

## 12. Floating WhatsApp Button

Fixed-position CTA on all pages → `wa.me/966539065696`.
**Defect:** same number for men and women despite gender-segregated support; no
`aria-label`; overlaps content at small viewports.

---

## 13. Component inventory for the rebuild

```
Layout      Header · MobileNav · Footer · CTABand · Container · Section
Navigation  MainMenu · RegistrationDropdown · Breadcrumb ✚ · LocaleSwitcher ✚
Content     Card(service|track|plan|download|value) · Accordion · Marquee
            SectionHeading · StatBadge · PartnerLogo
Forms       Button(primary|gold|outline) · Checkbox · Select · PhoneInput
            FormField · ErrorMessage ✚ · SuccessMessage ✚
Feedback    Dialog · Toast ✚ · LoadingSpinner · EmptyState ✚
            AvailabilityBadge ✚✚  ← open / closed / waitlist per track
Motion      Reveal · Stagger · Typewriter   (all reduced-motion aware)
```

`✚` = missing today. `✚✚` = the highest-value new component: it is what prevents users
walking into the 22 closed tracks.
