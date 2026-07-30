# 03 — Brand Identity System

## 1. Naming

- **Brand name:** Misbaha (المسبحة) — the classical Arabic word for the prayer-bead string,
  chosen for authenticity, cross-market recognizability (understood in Arabic, Urdu, Turkish,
  Malay-Muslim contexts), and unmarked neutrality across madhāhib.
- **Full mark:** *Misbaha — Digital Sanctuary for Dhikr* (EN) / *المسبحة — واحتك الرقمية للذكر* (AR)
- **Institutional sub-brand:** *Misbaha for Institutions* — white-label offering for mosques,
  Islamic schools, and waqf organizations (see [Deployment §5](10-DEPLOYMENT-LAUNCH-PLAN.md)).

## 2. Brand Positioning

Positioned adjacent to premium Saudi digital experiences — Haramain services, STC Pay/premium
Islamic banking apps, and Vision 2030 flagship government platforms — rather than the existing
tasbeeh-app category, which reads as low-trust utility software. Brand perception target: *"This
feels like it was built with the same care as the Two Holy Mosques' own digital services."*

## 3. Color System

| Token | Light Theme | Dark (default/"Night Dhikr") Theme | Usage |
|---|---|---|---|
| `color.primary` | `#0B6E4F` (Emerald) | `#1C9A6E` | Primary actions, active states |
| `color.accent.gold` | `#B8912F` (Muted Royal Gold) | `#D4AF37` | Ornamentation, premium badges, streak glyph |
| `color.surface` | `#FBF9F4` (Warm Ivory) | `#0E1512` (Deep Ink-Green Black) | Backgrounds |
| `color.surface.elevated` | `#FFFFFF` | `#16211C` | Cards |
| `color.text.primary` | `#1A1F1D` | `#F3F1EA` | Body text |
| `color.text.secondary` | `#5C645F` | `#A9B3AC` | Captions, citations |
| `color.error` | `#B3261E` | `#E4635A` | Destructive/error only, never decorative |

Gold is **rationed**: used only for premium/verified markers and ornamental accents, never as a
large fill, to avoid a garish/kitsch reading and preserve luxury restraint. This is the single
biggest differentiator from existing "gold-and-green mosque clipart" competitor apps.

## 4. Typography

- **Arabic body/UI:** Licensed Naskh-style variable font family (weights 400/500/700).
- **Arabic display (wordmark, section titles only):** Thuluth-inspired calligraphic display face.
- **Latin body/UI:** A humanist sans (e.g., a licensed equivalent of Inter/SF Pro) matched for
  x-height and weight against the Arabic family so mixed AR/EN screens feel visually unified.
- **Numerals:** Configurable Eastern Arabic ↔ Western Arabic (see Design System §5).

## 5. Logo & Mark

Primary mark: an abstracted single prayer bead rendered as a minimal geometric dot integrated
into a crescent-arc, forming a negative-space number "1" — symbolizing tawhid (oneness) and the
first bead of the strand. Renders as a monoline glyph at favicon size and as a filled mark at app-
icon size. Full usage grid, clear-space rules, and forbidden-usage examples are maintained in the
brand asset repository (Figma/brand-kit source of truth, referenced by the design team; not
duplicated here to avoid drift between design tool and documentation).

## 6. Shariah Content Governance Charter

All religious content (adhkar, Qur'an text, hadith, translations, audio recitation) is subject to
a mandatory governance workflow before publication:

1. **Sourcing:** Content is only sourced from recognized classical compilations (e.g., Hisnul
   Muslim / al-Adhkar corpora), the Uthmani Mushaf standard for Qur'an text, and hadith databases
   with established chain-of-narration grading (sahih/hasan/da'if labeled transparently — da'if
   content is excluded from default recitation sets and, if shown for reference, explicitly
   labeled).
2. **Review Board:** A standing **Islamic Content Governance Board** (minimum 3 qualified
   scholars spanning at least two schools of jurisprudence for cross-madhhab balance) reviews and
   signs off on every content batch before it ships. No engineer or product manager may add or
   edit religious text unilaterally.
3. **Neutrality on Fiqh Differences:** Where valid scholarly difference exists (e.g., specific
   dhikr wording variants, counting conventions), the app presents the mainstream default and
   offers a settings toggle for alternate accepted variants, rather than adjudicating between
   schools.
4. **No Theological Overreach:** The product makes no claims about reward, acceptance, or
   spiritual efficacy beyond citing the source text itself. Marketing copy is reviewed by the
   Governance Board for the same standard.
5. **Correction Pipeline:** A visible in-app "Report a content concern" path routes directly to
   the Governance Board with SLA-tracked review (see [Admin Dashboard §3](07-ADMIN-DASHBOARD.md)).
6. **Auditability:** Every content record stores its source citation, reviewer sign-off identity,
   and revision history (see [Database Schema §3](05-DATABASE-SCHEMA.md)).

## 7. Voice & Tone

- Warm, respectful, unembellished. Never uses exclamation-heavy "gamified app" copy ("You crushed
  it! 🔥 7-day streak!!"). Instead: calm affirmation ("You have remembered Allah for 7 consecutive
  days.").
- Bilingual parity: Arabic copy is never a literal machine translation of English marketing copy;
  each locale's copy is authored/reviewed by a native speaker for register and idiom.
- No anthropomorphized mascot. The brand does not personify itself as a "coach" character —
  consistent with avoiding trivializing worship.

## 8. Brand Application Across Surfaces

Design tokens (color, type, spacing, motion) are defined once in a shared design-token source
(see [Android Architecture §3](04-ANDROID-ARCHITECTURE.md)) and consumed identically across
Android, and in the roadmap, iOS/Web/Wear/TV/Auto — guaranteeing the luxury identity is pixel-
and-motion consistent everywhere the brand appears.
