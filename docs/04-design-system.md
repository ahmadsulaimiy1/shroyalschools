# 04 — Design System

Extracted from `wp-content/themes/itqan-theme/style.css` (86 KB, Tailwind v4 compiled).
Values are verbatim from the compiled `@theme` layer.

---

## 1. Colour

### Brand tokens (as shipped)

| Token | Hex | Role |
|---|---|---|
| `--color-primary` | `#027043` | Islamic green — headings, primary buttons, brand |
| `--color-primary-dark` | `#0d352d` | Deep green — footer, dark surfaces |
| `--color-primary-light` | `#1a5c52` | Mid green — hover, gradients |
| `--color-gold` | `#d4af37` | Accent — dividers, emphasis CTAs |
| `--color-gold-dark` | `#aa8c2c` | Gold hover |
| `--color-surface-warm` | `#fdfbf7` | Default page background (warm off-white) |
| `--color-surface-alt` | `#f9fafb` | Alternating section background |
| `--color-white` | `#fff` | Cards |
| `--color-black` | `#000` | — |

Plus the default Tailwind palette (grays for body text: `text-gray-800`).

**Assessment:** an appropriate, well-chosen palette. Green + gold on warm off-white is
idiomatic for Islamic educational identity and should be preserved without change.

### ⚠ Contrast audit

| Pair | Ratio | WCAG AA | Verdict |
|---|---|---|---|
| `#027043` on `#fdfbf7` | ~5.9:1 | ✅ Pass | Body and headings safe |
| `#0d352d` on `#fdfbf7` | ~13.5:1 | ✅ Pass | Excellent |
| White on `#027043` | ~5.7:1 | ✅ Pass | Primary buttons safe |
| **`#d4af37` on `#fff`** | **~1.9:1** | ❌ **Fail** | **Gold text/icons on light are unreadable** |
| **`#d4af37` on `#fdfbf7`** | **~1.8:1** | ❌ **Fail** | Same |
| White on `#d4af37` | ~2.2:1 | ❌ Fail | Gold buttons with white labels fail |

**This is the design system's one real flaw.** Gold is used decoratively (dividers, glows,
large icons) where it is acceptable, but anywhere it carries text or a meaningful icon it
fails AA by a wide margin.

**Fix — add an accessible gold for text, keep the original for decoration:**

```css
--color-gold:        #d4af37;  /* decorative only: dividers, glows, large ornament */
--color-gold-text:   #7a6318;  /* ~5.6:1 on #fdfbf7 — use for any gold-coloured text */
--color-gold-on-dark:#e8c860;  /* ~8.9:1 on #0d352d — gold text on dark surfaces */
```
Rule: `--color-gold` must never be used for text, icons conveying meaning, or focus rings.

---

## 2. Typography

| Token | Stack | Role |
|---|---|---|
| `--font-amiri` | `"Amiri", serif` | Display — H1/H2, Quranic and formal headings |
| `--font-tajawal` | `"Tajawal", sans-serif` | Body — all UI text (`<body class="font-tajawal">`) |
| `--font-sans` | `ui-sans-serif, system-ui, …` | Fallback |
| `--font-mono` | `ui-monospace, SFMono-Regular, …` | Unused |

Loaded via `@import` from Google Fonts inside `style.css`.

**Weights:** `medium 500`, `bold 700`, `extrabold 800`.

**Type scale** (Tailwind default, `rem`, with paired line-heights):
`xs .75` · `sm .875` · `base 1` · `lg 1.125` · `xl 1.25` · `2xl 1.5` · `3xl 1.875` ·
`4xl 2.25` · `5xl 3` · `6xl 3.75` · `7xl 4.5`

Headings typically `text-3xl lg:text-5xl font-amiri font-bold text-primary`.

**Assessment:** Amiri (a high-quality Naskh) for display + Tajawal for UI is an excellent
Arabic pairing — traditional authority in headings, clean legibility in body.

### ⚠ Defects

- **`@import` inside CSS blocks rendering.** The font request cannot start until `style.css`
  has downloaded and parsed — a serialised round-trip on the critical path.
  **Fix:** `<link rel="preconnect">` + `<link rel="preload">`, or self-host.
- **No `font-display: swap`** → FOIT; text is invisible while fonts load.
- **No Latin/Urdu subsetting.** Arabic Amiri + Tajawal are large; the English, French and
  Italian pages load full Arabic fonts they never render.
- **Self-hosting is recommended** — it removes a third-party dependency, a privacy concern
  (Google Fonts logs IPs, relevant to GDPR for the European locales), and a render-blocking
  origin.

---

## 3. Spacing & Layout

Tailwind 4 px base scale (`--spacing-*`). Sections use `py-24` (6 rem);
containers `container mx-auto px-4`, constrained variously to `max-w-4xl` … `max-w-7xl`.

**Grids:** 6-service and 8-advantage grids are `stagger-grid` with `.anim-child`;
tracks render as a responsive 1 → 2 → 3 column grid.

---

## 4. Radius, Shadow, Effects

| Token | Value |
|---|---|
| `--radius-lg` | `.5rem` |
| `--radius-xl` | `.75rem` |
| `--radius-2xl` | `1rem` |
| `--radius-3xl` | `1.5rem` |
| `--radius-4xl` | `2rem` |
| `--shadow-glow` | `0 0 20px #d4af374d` (gold glow) |

Plus Tailwind default shadows (`shadow-md` on scrolled header).
Decorative: `.pattern-islamic-bg` (geometric pattern, `opacity-5`, `mix-blend-multiply`),
oversized Font Awesome glyphs at `text-[400px] text-gold/5` as section ornament.

---

## 5. Motion

| Class | Effect |
|---|---|
| `.anim-blur-in` | Blur + fade in |
| `.anim-slide-right` / `.anim-slide-left` | Directional slide |
| `.anim-pop-in` | Scale up |
| `.stagger-grid` / `.anim-child` | Cascading reveal (50 ms mobile / 100 ms desktop) |
| `.reveal-item` | Generic reveal |
| `.typewriter-text` | 70 ms/char typing |
| `.animate-marquee` | Infinite partner scroll |
| `.animate-float`, `.animate-float-y`, `.animate-spin-slow`, `.animate-bounce`, `.animate-ping` | Ambient |

### ⚠ Critical accessibility defect

**No `prefers-reduced-motion` media query exists anywhere in the 86 KB stylesheet.** Every
animation above runs unconditionally. For a platform explicitly serving ذوي الهمم (people
with disabilities) and users over 40, shipping unstoppable motion is both an accessibility
failure (WCAG 2.3.3) and a contradiction of the product's own stated mission.

**Required fix:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
    scroll-behavior: auto !important;
  }
}
```
…and gate the typewriter and marquee JS on `matchMedia('(prefers-reduced-motion: reduce)')`.

---

## 6. RTL

`<html dir="rtl" lang="ar">` with `class="rtl"` on `<body>`; Tailwind logical properties
handle mirroring. Font Awesome 7.0.0 via cdnjs.

**Defect:** the English, French and Italian registration pages inherit `dir="rtl" lang="ar"`
— LTR content in an RTL document declared as Arabic. Breaks punctuation placement, list
markers and screen-reader language selection. Each locale must set its own `dir` and `lang`.

---

## 7. Iconography

Font Awesome 7.0.0 (full CDN build) + one local SVG (`open-mushaf-white.svg`, 1 KB).

**Defect:** the **entire** Font Awesome CSS is loaded from `cdnjs` for a handful of icons —
a large render-blocking third-party request.
**Fix:** inline the ~25 used icons as SVG sprites. Removes a third-party origin and most of
the icon payload.

---

## 8. Responsive

Tailwind defaults: `sm 640` · `md 768` · `lg 1024` · `xl 1280` · `2xl 1536`.
Mobile menu below `lg`; typography steps at `lg`; animation delays branch at 768 px in JS.

---

## 9. Design tokens for the rebuild

```css
@theme {
  /* Brand — unchanged */
  --color-primary:       #027043;
  --color-primary-dark:  #0d352d;
  --color-primary-light: #1a5c52;
  --color-gold:          #d4af37;   /* decorative only */
  --color-gold-dark:     #aa8c2c;

  /* ✚ Accessible gold for text */
  --color-gold-text:     #7a6318;
  --color-gold-on-dark:  #e8c860;

  /* Surfaces — unchanged */
  --color-surface-warm:  #fdfbf7;
  --color-surface-alt:   #f9fafb;

  /* ✚ Semantic states — absent today, required for availability + form feedback */
  --color-success:       #027043;
  --color-warning:       #b45309;
  --color-danger:        #b91c1c;
  --color-info:          #1a5c52;

  /* Type — unchanged, self-hosted, subset, font-display: swap */
  --font-amiri:  "Amiri", serif;
  --font-tajawal:"Tajawal", sans-serif;

  /* Radius & shadow — unchanged */
  --radius-lg: .5rem;  --radius-xl: .75rem;  --radius-2xl: 1rem;
  --radius-3xl: 1.5rem; --radius-4xl: 2rem;
  --shadow-glow: 0 0 20px #d4af374d;

  /* ✚ Focus ring — none defined today */
  --ring-focus: 0 0 0 3px #02704340;
}
```

**Summary of changes:** the palette, typography and shape language are kept intact. The
additions are strictly corrective — an accessible gold, semantic state colours, a focus
ring, and a reduced-motion contract.
