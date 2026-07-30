# 07 — Admin Dashboard Design

## 1. Purpose & Users

A web console (not on-device) serving three distinct operator roles with role-based access
control:

| Role | Primary Use |
|---|---|
| **Content Governance Reviewer** (scholar) | Review/approve/reject content submissions |
| **Platform Operator** (internal team) | Monitor system health, manage content pipeline, support |
| **Institution Admin** (mosque/school/waqf customer) | Manage their branded deployment, view circle analytics |

## 2. Information Architecture

```
Admin Console
├── Overview          — platform health, DAU/MAU, sync success rate, error budget
├── Content Governance — submission queue, review workflow, publish/deprecate
├── Scholars           — manage reviewer roster, credentials, madhhab tagging
├── Institutions        — tenant management, branding config, plan tier, seats
├── Users & Support     — support ticket-linked lookup (privacy-gated), GDPR request queue
├── Analytics           — aggregate engagement, retention cohorts, content trust score
└── Audit Log            — immutable record of every admin action
```

## 3. Content Governance Workflow (Screen Detail)

1. **Submission Queue** — new/edited `dhikr_definitions` land as `status='draft'`; queue shows
   source citation, diff-against-previous-version, and assigned reviewer(s).
2. **Review Screen** — side-by-side Arabic source text + proposed translations, citation
   verification checklist, authenticity-grade selector, comment thread between reviewers.
3. **Sign-off** — requires minimum quorum (configurable, default 2 of 3 assigned scholars) before
   `status` transitions to `approved`; a single reviewer cannot unilaterally publish (matches the
   Shariah Governance Charter in [Brand Identity §6](03-BRAND-IDENTITY.md#6-shariah-content-governance-charter)).
4. **Deprecation/Correction** — the in-app "Report a content concern" pipeline
   ([PRD §5.2](01-PRD.md#52-content-library-shariah-governed)) surfaces here as a triaged queue
   with SLA timers (target: acknowledged in 48h, resolved in 14 days).

## 4. Institution Console (Multi-Tenant)

- **Branding config:** logo, primary color override within luxury palette guardrails (cannot
  violate accessibility contrast minimums — enforced by validation, not just guidance), custom
  circle naming.
- **Circle analytics:** aggregate-only dashboards (total dhikr count this week, active members,
  streak distribution) — never per-member drill-down unless every member has explicitly opted
  into `visibility=name_visible` (see [API §3](06-API-DOCUMENTATION.md#core-endpoints)).
- **Seat/license management:** bulk invite via email/QR code for congregation onboarding.
- **k-anonymity floor:** any aggregate breakdown suppresses cells below 5 users to prevent
  re-identification in small circles — enforced server-side, not a UI-only guard.

## 5. Platform Operations Screens

- Real-time sync health (event ingestion lag, error rates by region — surfaces connectivity-
  constrained markets like the PRD's Hajj/rural persona).
- Feature flag / staged rollout control (ties into [Deployment Plan §3](10-DEPLOYMENT-LAUNCH-PLAN.md)).
- GDPR request queue: export/erasure requests with countdown timers to the legal SLA, and
  one-click execution that fans out deletion across Postgres, object storage (audio/journal
  attachments), and analytics pipelines.

## 6. Access Control & Audit

- RBAC scoped by role × institution (an Institution Admin can only see their own tenant's data —
  enforced at the query layer, not just UI hiding).
- Every mutating action writes to the immutable `audit_log` table
  ([Database Schema §3](05-DATABASE-SCHEMA.md#3-cloud-schema-postgresql--syncontentgovernance-tier))
  with actor, action, target, and timestamp — reviewable in the Audit Log screen, exportable for
  compliance review.
- Admin console authentication requires MFA for all roles handling content publish or PII access.
