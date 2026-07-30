# 02 — UI/UX Design System

## 1. Design Principles

1. **Sakinah (Tranquility) over Stimulation.** No slot-machine gamification, no aggressive red
   badges, no push-notification spam. Motion and sound exist to calm, not to hook.
2. **Arabic-First, Not Arabic-Translated.** Layouts are authored in RTL first, then mirrored to
   LTR — never the reverse. Arabic typography gets equal or greater visual weight than Latin.
3. **Craftsmanship as Worship (Itqan).** Every pixel, easing curve, and haptic tap is treated as
   an act of care, echoing the Islamic principle of ihsan (excellence) in one's work.
4. **Radical Clarity.** One primary action per screen. The counter screen has exactly one
   dominant interactive element.
5. **Trust Made Visible.** Every piece of religious content visibly shows its source/citation —
   never a bare block of text with unclear provenance.

## 2. Information Architecture

```
Root
├── Home (Today) — greeting, prayer-time strip, "continue session", daily adhkar suggestion
├── Counter — the core tasbeeh screen (bottom-nav default tab)
├── Library — Adhkar collections / Qur'an / Asma-ul-Husna / Hadith
├── Journal — personal history, streaks, stats, Ramadan/Hajj modes
├── Circles — opt-in community/family/mosque groups
└── Profile & Settings — account, accessibility, language, privacy, subscription
```

## 3. Core Screens (Representative Set)

| Screen | Purpose | Key Elements |
|---|---|---|
| **Splash / Basmala Intro** | Brand moment, cold-start bridge | Animated geometric mark resolving from Islamic star pattern, < 1.2s |
| **Onboarding — Language & Madhhab** | First-run setup | Arabic/English toggle, calculation-method selection, no account required to start |
| **Home ("Today")** | Daily anchor screen | Hijri + Gregorian date, next-prayer countdown, "Recommended Dhikr" card, streak flame (subtle, not neon) |
| **Counter (core)** | Primary dhikr counting | Large bead-ring counter (radial progress), current dhikr text (AR large / EN small), target selector, lap history drawer, haptic toggle |
| **Multi-Counter Session** | Track several adhkar in one sitting | Horizontal swipe deck of counters, session summary on complete |
| **Library — Collection List** | Browse adhkar sets | Category cards (Morning, Evening, Post-Salah, Travel, Ruqyah, Sleep) with verified badge |
| **Library — Dhikr Detail** | Read/recite a single dhikr | Arabic (Uthmani-style calligraphic font), transliteration toggle, translation toggle, audio playback, source citation footer, "Start Counting" CTA |
| **Qur'an Reader** | Mushaf-style reading | Continuous Uthmani script, ayah-by-ayah audio sync highlight, bookmarking, tafsir drawer |
| **Journal / Stats** | Reflect on practice | Calendar heatmap (muted gold, not aggressive green), weekly/monthly totals, exportable |
| **Circles** | Community, opt-in | Aggregate counters only by default; per-circle settings for granular sharing |
| **Admin/Institution Console (web)** | See [Admin Dashboard](07-ADMIN-DASHBOARD.md) | Separate web surface, not on-device |
| **Settings — Accessibility** | Inclusive controls | Text scale, high-contrast, reduce-motion, screen-reader test mode, one-handed layout |
| **Paywall / Premium** | Value-first upsell | Never blocks core counting or the free Adhkar library; upsells audio packs, themes, cloud sync, family circles |

## 4. User Journeys (Key Flows)

### 4.1 First-Time Use (Zero Friction)
`Splash → Language select → (skip account) → Home → Tap Counter tab → Start counting immediately.`
No login wall. Account creation is deferred until the user opts into cloud sync/circles.

### 4.2 Daily Ritual Loop
`Prayer-time notification (optional, respectful tone) → Home shows suggested post-salah adhkar →
One tap into Counter pre-loaded with the triplet (SubhanAllah/Alhamdulillah/Allahu Akbar ×33) →
Completion animation (subtle, no confetti) → Journal auto-logs.`

### 4.3 Learning Journey (New Muslim Persona)
`Library → filter "For Beginners" → Dhikr Detail with transliteration + audio + meaning →
"Learn Mode" quiz (optional, spaced repetition) → graduates to full Arabic display.`

### 4.4 Offline-to-Online Reconciliation
`User counts fully offline for days → connectivity returns → background sync merges local
event log with cloud via last-write-wins + append-only event journal (see Architecture §4) →
no data loss, no user-visible merge conflicts.`

## 5. RTL & Arabic Typography Rules

- Mirror layout direction, iconography with directional meaning (back arrows, progress), and
  swipe gestures; **do not** mirror numerals, logos, or the Kaaba/qibla icon.
- Primary Arabic typeface: a licensed Naskh-style variable font (e.g., a Noto Naskh Arabic /
  premium equivalent) for body text; a Thuluth-inspired display face reserved for the wordmark
  and section headers only, never body copy (legibility).
- Minimum Arabic body size: 18sp (Arabic script requires larger minimum size than Latin for
  equivalent legibility).
- Line height: 1.6× for Arabic paragraphs (diacritics/tashkeel require more vertical room).
- Numerals: Eastern Arabic numerals (٠١٢٣...) as default in AR locale, with a settings toggle to
  Western Arabic numerals — many Gulf users prefer the latter in-app despite AR locale.

## 6. Visual Language

- **Grid:** 8pt base grid, 4pt for micro-spacing (icon padding, badges).
- **Corner radius:** Large, soft radii (16–28dp) evoking dome/arch geometry rather than sharp
  Material default corners — a signature Misbaha silhouette.
- **Ornamentation:** Geometric Islamic star-and-polygon patterns (8-fold, 12-fold) used sparingly
  as background watermarks at ≤5% opacity — never as busy decoration competing with content.
- **Iconography:** Custom line-icon set with consistent 2dp stroke, rounded joins, echoing mosque
  architectural motifs (crescent, arch, minaret silhouette) used only where meaningful, not as
  generic decoration.

## 7. Motion & Haptics

- Counter tap: 40–60ms critically-damped spring scale (0.96→1.0), paired with a soft "click" haptic
  (Android `HapticFeedbackConstants.CONFIRM`-equivalent) — never a jarring buzz.
- Milestone completion (reaching target count): a slow 600ms radial-fill completion with a gentle
  chime (user-toggleable, respects silent/masjid mode) — explicitly *not* confetti or badges-pop.
- Page transitions: shared-element transitions between Library list → Detail → Counter, 250–300ms
  ease-out, respecting system "reduce motion" accessibility setting (falls back to instant cut).
- Reduce-motion and reduce-haptics are first-class settings, not buried.

## 8. Component Library (Summary)

`MisbahaButton` (primary/secondary/ghost), `BeadRingCounter`, `DhikrCard`, `SourceCitationChip`,
`PrayerTimeStrip`, `StreakIndicator` (flame glyph, muted gold, caps at a dignified icon rather
than escalating numbers-as-status), `VerifiedContentBadge`, `LanguageToggle`, `AudioPlayerBar`,
`CalendarHeatmap`, `BottomNavBar` (5-tab, RTL-aware), `EmptyState`, `OfflineBanner`.
Full component specs (states, tokens, Figma-equivalent handoff) live in the design tooling
repository referenced from the Brand Identity system (§5).

## 9. Accessibility Specification

- Contrast ratio ≥ 4.5:1 body text, ≥ 3:1 large text/icons, verified against both Light and Dark
  luxury themes (see Brand Identity §3 palette).
- All touch targets ≥ 48×48dp.
- Full semantic labeling for TalkBack in both Arabic and English; content descriptions are
  authored, not auto-generated from visible text, so audio phrasing is natural.
- Reduced-motion, reduced-transparency, and high-contrast theme variants ship at v1, not deferred.
