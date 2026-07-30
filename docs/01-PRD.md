# 01 — Product Requirements Document (PRD)

## 1. Vision Statement

Misbaha is the world's most advanced digital Tasbeeh and Dhikr platform — a spiritual companion
that treats remembrance of Allah (dhikr) as a lifelong practice worthy of the same craftsmanship,
trust, and polish as premium Islamic finance, Haramain digital services, and Saudi Vision 2030
flagship applications. It is not a "counter with a button." It is an ecosystem: counting engine,
knowledge library, habit-formation coach, community of remembrance, and Shariah-governed content
authority, unified under a single luxury experience across every device a Muslim owns.

## 2. Problem Statement

Existing tasbeeh apps are functionally interchangeable commodity utilities: a tap counter, a
generic UI, intrusive ads, unverified content, and no habit design. They fail to:

- Reflect the dignity of the ritual (i'tikaf-grade calm, not gamified noise)
- Guarantee scholarly-verified content (duas, adhkar, Qur'an text/audio, hadith attribution)
- Work reliably offline in low-connectivity regions (rural Muslim-majority markets)
- Support Arabic as a first-class, not translated-afterthought, language
- Scale technically or organizationally beyond a single-developer utility app
- Meet enterprise privacy/security bars expected of a platform handling worship data at scale

## 3. Target Users & Personas

| Persona | Description | Core Need |
|---|---|---|
| **Umm Fahad, 34, Riyadh** | Practicing professional, uses tasbeeh during commute and after Fajr/Isha | Fast, elegant counting; automatic Bluetooth-ring pairing; streaks |
| **Br. Yusuf, 22, London (convert)** | New Muslim, learning adhkar | Guided learning mode, transliteration, audio, English explanations |
| **Sheikh Abdullah, 58, Jeddah (content authority)** | Scholar reviewing content | Admin governance tools, source citation, edit workflows |
| **Aisha, 12, Kuala Lumpur (child, parental account)** | Learning Islamic habits | Gamified but dignified progress, parental controls |
| **Hajj/Umrah Pilgrim** | Uses app during pilgrimage, poor connectivity | 100% offline core function, low battery mode, multilingual |
| **Institutional customer (mosque, Islamic school, waqf org)** | Deploys to congregation | Bulk licensing, branded white-label, community leaderboards (opt-in) |

## 4. Jobs To Be Done

1. "When I finish a prayer, help me count my adhkar accurately without thinking about the app."
2. "Help me build a lasting daily dhikr habit, not just log one session."
3. "Give me confidence every dua/hadith shown to me is authentic and correctly attributed."
5. "Let me use this the same way in Riyadh, London, or with no signal at all in the desert."
6. "Let me privately track my spiritual growth without my data being sold or leaked."
7. "As an institution, let me deploy this to my community and see aggregate engagement."

## 5. Product Scope — Core Feature Pillars

### 5.1 Tasbeeh & Dhikr Engine
- Digital bead counter with haptic + audio feedback, configurable target counts (33/99/100/1000/custom)
- Multi-counter sessions (track several adhkar in parallel, e.g., after-salah triplet)
- Physical ring/Bluetooth counter pairing (BLE), smartwatch tap support
- Voice-activated counting (on-device speech detection of "SubhanAllah" etc., privacy-preserving, opt-in)
- Vibration-only "silent masjid mode"
- Auto-reset, lap history, daily/weekly/yearly aggregate stats

### 5.2 Content Library (Shariah-Governed)
- Verified Adhkar collections (Morning/Evening, Post-Salah, Sleep, Travel, Ruqyah) sourced from
  Hisnul Muslim and scholar-reviewed corpora, each entry carrying Arabic text, transliteration,
  translation (multi-language), and full source citation (book, hadith grading where applicable)
- Full Qur'an (Uthmani script) with word-by-word translation, multiple reciters, offline audio packs
- 99 Names of Allah (Asma-ul-Husna) module with meaning, dhikr counters per name
- Hadith reference layer with authenticity grading displayed transparently
- All content passes through the Islamic Content Governance Board workflow (see §9)

### 5.3 Habit Formation & Personal Growth
- Streaks, gentle reminders (not gamified badges that trivialize worship — see Design Ethics)
- Prayer-time-aware smart reminders (adhan integration, calculation-method configurable)
- Personal dhikr journal (private, encrypted, exportable)
- Ramadan mode (Qur'an khatm tracker, taraweeh dhikr sets, Laylatul Qadr focus)
- Hajj/Umrah companion mode (talbiyah counter, ritual-specific adhkar, offline map-independent)

### 5.4 Community (Opt-In, Privacy-First)
- Anonymous collective dhikr counters (e.g., global Ramadan tasbeeh total) — aggregate only, no
  individual leaderboard by default
- Mosque/institution circles: opt-in group challenges, family circles for children's progress
- Sadaqah Jariyah dedication: dedicate a dhikr session's reward-intent to a deceased relative
  (recorded locally as a personal note; the platform makes no theological claims about transfer
  of reward — see Shariah Governance Charter)

### 5.5 Accessibility & Inclusion
- Full Arabic-first RTL layout mirrored correctly (not just text-flipped)
- Screen reader (TalkBack/VoiceOver) labels on every interactive element in Arabic and English
- Dynamic type scaling, high-contrast and low-vision themes, colorblind-safe palettes
- One-handed reachability mode, large-target mode for elderly/motor-impaired users
- Support for Qur'an audio-only mode for visually impaired users

## 6. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Offline | 100% of counting, content library, and journal features work with zero connectivity; sync is background/best-effort |
| Performance | Cold start < 800ms on mid-tier Android (Snapdragon 6-series); counter tap-to-feedback latency < 16ms (one frame) |
| Localization | Arabic (primary), English (primary), phased: Urdu, Malay/Indonesian, Turkish, French, Farsi |
| Accessibility | WCAG 2.2 AA minimum across all screens |
| Availability | 99.95% for cloud sync/backend services |
| Security | See [Security Framework](09-SECURITY-FRAMEWORK.md) — enterprise-grade, zero-trust backend |
| Privacy | GDPR-compliant by design; PDPL (Saudi) and PDPA (Malaysia/Indonesia) aligned |
| Scale | Architecture supports 10M+ MAU, 100M+ daily counter events, horizontally scalable |

## 7. Out of Scope (v1)

- Live scholar Q&A / fatwa services (legal/compliance risk — future partnership consideration)
- Zakat calculation and payment processing (separate regulated product line)
- Social media-style public profiles/feeds (conflicts with humility-in-worship design ethic)

## 8. Success Metrics (North Star + Supporting)

- **North Star:** 7-day habit retention rate (% of new users who log dhikr on 5+ of first 7 days)
- D1/D7/D30 retention, DAU/MAU ratio ≥ 45%
- Average sessions/day per active user
- % of sessions completed fully offline
- Content trust score (in-app survey: "Do you trust the content in this app?") ≥ 95% agreement
- Play Store rating ≥ 4.8, crash-free sessions ≥ 99.9%
- Institutional deployments (mosques/schools) count, YoY growth

## 9. Governance Dependency

All content decisions route through the **Islamic Content Governance Board** (see
[Brand Identity §6](03-BRAND-IDENTITY.md#6-shariah-content-governance-charter)) before shipping.
Product cannot unilaterally add adhkar, hadith, or ritual content without sign-off.

## 10. Release Milestones (summary — detail in [Roadmap](11-FIVE-YEAR-ROADMAP.md))

| Milestone | Target |
|---|---|
| M0 — Architecture & Design System lock | Complete (this document set) |
| M1 — Android MVP (counter, adhkar library, offline, AR/EN) | Q4 2026 |
| M2 — Android v1.0 public launch (KSA, UAE, Egypt, Malaysia, Indonesia, UK, US) | Q1 2027 |
| M3 — Institutional/white-label + Admin Dashboard GA | Q3 2027 |
| M4 — iOS + Web launch | Q1 2028 |
| M5 — Wear/TV/Auto expansion | 2028–2029 |
