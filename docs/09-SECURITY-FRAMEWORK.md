# 09 — Security Framework

## 1. Threat Model Summary

Assets to protect: user worship/behavioral data (sensitive-by-nature even though not a legally
"special category" under GDPR in most interpretations, treated with special-category-equivalent
care), account credentials, institutional tenant data isolation, and content integrity (tampering
with religious text is a distinct, high-severity threat class unique to this product).

Primary threat actors considered: opportunistic credential-stuffing attackers, malicious insiders
with content-edit access, curious/negligent third-party SDK data leakage, and nation-state-level
mass surveillance risk in some deployment markets — the last of which specifically motivates the
anonymous-usage-by-default posture in §3.

## 2. Application Security (Android Client)

- No PII required for core functionality (anonymous session model, [API §2](06-API-DOCUMENTATION.md#2-authentication)).
- All local sensitive data (journal notes, dedication notes) encrypted at rest via Android
  Keystore-backed SQLCipher on the Room database; keys never leave hardware-backed keystore.
- Certificate pinning on all API traffic; TLS 1.3 minimum.
- No sensitive data in logs; structured logging framework enforces field-level redaction by type
  (compile-time annotation on data classes, not developer discipline alone).
- Root/tamper detection surfaces a non-blocking advisory (never locks out worship functionality —
  balances security posture against the "never block core use" product principle).
- Dependency supply-chain scanning (SCA) gated in CI; no unreviewed third-party SDK may access
  network or storage permissions without a security review sign-off.

## 3. Backend / Cloud Security

- Zero-trust service-to-service auth (mTLS) within the cloud environment; no implicit trust based
  on network location.
- Secrets management via a dedicated vault (no secrets in code, config, or CI logs).
- Least-privilege IAM per service; the content-governance service, for example, cannot write to
  the billing/subscriptions tables.
- Rate limiting and WAF at the edge (see [API §4](06-API-DOCUMENTATION.md#4-rate-limiting--abuse-protection)).
- Encryption at rest (AES-256) for all datastores; encryption in transit everywhere, including
  internal service mesh traffic.
- Regular third-party penetration testing (minimum annual, plus after any major architecture
  change) and a public responsible-disclosure program.

## 4. Data Classification & GDPR Compliance

Extends [Database Schema §4](05-DATABASE-SCHEMA.md#4-data-classification--retention):

- **Lawful basis:** legitimate interest / contract performance for core functionality; explicit
  opt-in consent for Circles sharing, analytics beyond essential telemetry, and marketing
  communications — consent is granular per purpose, not a single blanket toggle.
- **Data Subject Rights:** self-service export (Art. 20) and erasure (Art. 17) via
  `/v1/account/export` and `DELETE /v1/account` ([API §3](06-API-DOCUMENTATION.md)), executed
  within the statutory window and fanned out across all datastores including backups (via
  crypto-shredding of per-user encryption keys for backup data, avoiding costly backup rewrites
  while still rendering data unrecoverable).
- **Data minimization:** anonymous-by-default architecture means most installs never generate
  identifiable data at all.
- **Cross-border transfer:** regional data residency options for institutional/enterprise tenants
  (e.g., KSA-resident hosting option) to satisfy PDPL and similar regional frameworks alongside
  GDPR.
- **DPIA:** a Data Protection Impact Assessment is maintained and re-reviewed at each major
  feature addition touching behavioral or location (prayer-time) data.
- **Children's data:** the child/family-managed accounts described in the PRD's Aisha persona
  operate under parent-account custodianship with no independent data collection from the child
  profile beyond what the parent configures — aligned with GDPR Art. 8 and COPPA-equivalent
  practice for the US market.

## 5. Governance & Auditability

- Immutable `audit_log` ([Database Schema §3](05-DATABASE-SCHEMA.md)) covers all admin actions,
  especially content publish/deprecate and any PII access by support staff — a dual-purpose
  control satisfying both security forensics and Shariah content-integrity assurance.
- Content-signing: published `dhikr_definitions` carry a governance sign-off reference that
  clients can surface as the "Verified" badge from the Design System — tampering with content
  in transit or at rest is detectable via integrity hash comparison against the signed record.

## 6. Observability & Incident Response

- Privacy-scrubbed crash/perf telemetry only (no dhikr content, no journal text ever leaves the
  device in telemetry payloads — enforced via the same field-redaction framework as §2).
- Defined incident response runbook with severity tiers; user-notification commitments for any
  confirmed breach affecting personal data, meeting GDPR's 72-hour regulator notification
  requirement.
- Security championship model: each squad in the modular Android architecture
  ([Architecture §3](04-ANDROID-ARCHITECTURE.md#3-module-map)) has a designated security reviewer
  for PRs touching auth, storage, or network boundaries.
