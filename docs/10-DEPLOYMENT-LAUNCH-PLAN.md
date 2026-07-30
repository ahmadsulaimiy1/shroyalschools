# 10 — Deployment & Launch Plan

## 1. Cloud Infrastructure

- Managed Kubernetes for the API/sync tier, horizontally autoscaled by region, front by a global
  CDN/edge network for content and audio asset delivery (heaviest bandwidth consumer — reciter
  audio packs).
- Multi-region active-active for the content-sync API (read-heavy, cacheable); the write path
  (dhikr event ingestion, §3 of the [API doc](06-API-DOCUMENTATION.md)) uses regional primaries
  with async replication, since event data is append-only and idempotent by client UUID —
  tolerant of eventual consistency without correctness loss.
- Regional data residency option (KSA/GCC hosting) for institutional customers per
  [Security Framework §4](09-SECURITY-FRAMEWORK.md#4-data-classification--gdpr-compliance).

## 2. CI/CD Pipeline

```
PR opened → static analysis (ktlint/detekt) + unit tests + Compose UI tests
          → Baseline Profile / macrobenchmark regression gate
          → accessibility lint gate
          → security SCA scan
Merge to main → signed internal-track AAB build → automated smoke test on device farm
              → deploy to internal QA track (Play Console internal testing)
Release branch cut → closed beta track (opt-in testers, target markets) → staged rollout
```

- Backend: trunk-based development, feature-flagged; blue/green deploys with automated rollback
  on error-rate/latency SLO breach.
- Mobile staged rollout: 1% → 5% → 25% → 100% over 7–10 days per release, gated on crash-free
  session rate ≥ 99.9% and no P0/P1 regressions.

## 3. Feature Flagging & Progressive Delivery

Server-driven feature flags (via the Admin Console, [Admin Dashboard §5](07-ADMIN-DASHBOARD.md#5-platform-operations-screens))
allow decoupling deploy from release — e.g., shipping the Circles feature to app binaries ahead
of its market-by-market enablement as institutional partnerships come online.

## 4. Phased Market Launch

| Phase | Markets | Focus |
|---|---|---|
| Phase 0 — Closed Beta | Saudi Arabia, UAE (internal + invited testers) | Core loop validation, Arabic UX polish, content QA with Governance Board |
| Phase 1 — GCC Public Launch | KSA, UAE, Qatar, Kuwait, Bahrain, Oman | Full AR/EN, luxury brand campaign aligned with Vision 2030 partners |
| Phase 2 — MENA + South Asia | Egypt, Jordan, Pakistan, India (Muslim-majority regions) | Urdu localization, budget-device performance tuning |
| Phase 3 — Southeast Asia | Malaysia, Indonesia, Brunei | Malay/Indonesian localization, largest global Muslim population addressable market |
| Phase 4 — Western Diaspora | UK, US, Canada, France, Germany | English-first framing, convert/new-Muslim onboarding emphasis, GDPR-first messaging in EU |

Each phase gates on: content Governance Board sign-off for that locale's translations, local
App/Play Store compliance review ([Store Publishing Package](12-STORE-PUBLISHING-PACKAGE.md)),
and infra capacity headroom confirmed via load testing at 3x projected peak.

## 5. Institutional Rollout Track

Parallel, slower-moving track: pilot with 3–5 flagship mosques/Islamic organizations per launch
region before opening self-serve institutional sign-up, ensuring the Admin Dashboard's
multi-tenant model ([Admin Dashboard §4](07-ADMIN-DASHBOARD.md#4-institution-console-multi-tenant))
is validated against real congregation-scale usage before broad B2B marketing.

## 6. Launch Readiness Checklist (gate before Phase 1)

- [ ] Crash-free sessions ≥ 99.9% in closed beta
- [ ] All Phase 0/1 content fully Governance-Board-approved
- [ ] Accessibility audit passed (WCAG 2.2 AA) with independent auditor sign-off
- [ ] Security penetration test completed, all Critical/High findings remediated
- [ ] GDPR DPIA finalized and legal sign-off obtained
- [ ] Store listings, screenshots, and compliance declarations finalized (§ [Store Publishing Package](12-STORE-PUBLISHING-PACKAGE.md))
- [ ] On-call/incident response runbook rehearsed

## 7. Post-Launch Operations

24/7 on-call rotation for the sync/content API during the first 90 days post each phase launch;
weekly Governance Board content review cadence transitioning to bi-weekly once the core Adhkar
library reaches steady state.
