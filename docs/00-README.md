# Misbaha — Global Islamic Luxury Tasbeeh Platform

**Codename:** Misbaha (المسبحة) — "The Digital Prayer Bead"
**Tagline (EN):** *Every Bead, A Remembrance.*
**Tagline (AR):** كل حبة ذكر، كل ذكرٍ نور

This directory contains the complete product, design, engineering, governance, and go-to-market
documentation set for Misbaha — a luxury Islamic Tasbeeh & Dhikr spiritual engagement platform,
built Android-first with a roadmap to iOS, Web, Wear OS/watchOS, Android TV/tvOS, and automotive
(Android Auto/CarPlay) surfaces.

## Document Index

| # | Document | Contents |
|---|----------|----------|
| 01 | [Product Requirements Document](01-PRD.md) | Vision, personas, JTBD, feature scope, success metrics |
| 02 | [UI/UX Design System](02-DESIGN-SYSTEM.md) | Screens, user journeys, component library, RTL rules, motion |
| 03 | [Brand Identity System](03-BRAND-IDENTITY.md) | Naming, logo, color, type, voice, Shariah governance charter |
| 04 | [Android Source Architecture](04-ANDROID-ARCHITECTURE.md) | Module map, Clean Architecture, tech stack, offline sync |
| 05 | [Database Schema](05-DATABASE-SCHEMA.md) | Local Room schema + cloud Postgres schema, ERDs |
| 06 | [API Documentation](06-API-DOCUMENTATION.md) | REST/GraphQL contracts, auth, sync protocol, rate limits |
| 07 | [Admin Dashboard Design](07-ADMIN-DASHBOARD.md) | Content governance console, moderation, analytics |
| 08 | [Monetisation Strategy](08-MONETIZATION-STRATEGY.md) | Halal revenue model, subscription tiers, waqf/sadaqah engine |
| 09 | [Security Framework](09-SECURITY-FRAMEWORK.md) | Enterprise security architecture, GDPR, threat model |
| 10 | [Deployment & Launch Plan](10-DEPLOYMENT-LAUNCH-PLAN.md) | Cloud infra, CI/CD, phased rollout, market launch |
| 11 | [Five-Year Product Roadmap](11-FIVE-YEAR-ROADMAP.md) | Y1–Y5 platform, market, and capability expansion |
| 12 | [Store Publishing Package](12-STORE-PUBLISHING-PACKAGE.md) | Play Store/App Store listing kit, compliance, ASO |

## Companion Implementation

`/android` contains a working Android application scaffold (Kotlin, Jetpack Compose, Room,
Hilt, Clean Architecture / MVVM) implementing the core Tasbeeh Counter experience described in
these documents — the seed from which the full platform in the roadmap is built out.

## Board of Record

This documentation set was produced under a joint governance review spanning product, Shariah
compliance, platform engineering, HCI/design, security, and go-to-market disciplines, per the
governing brief. It is the authoritative reference for all downstream engineering and design work
on Misbaha.
