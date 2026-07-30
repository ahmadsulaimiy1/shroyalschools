# 12 — App Store & Play Store Publishing Package

## 1. Listing Copy (EN)

- **App name:** Misbaha — Tasbeeh & Dhikr
- **Short description (80 char):** Luxury digital tasbeeh, verified adhkar, and Qur'an — offline, ad-free.
- **Full description (structure):** Opens with the brand promise (dignity, verified content,
  offline reliability), followed by a feature list mapped to the [PRD §5](01-PRD.md#5-product-scope--core-feature-pillars)
  pillars, a note on the Islamic Content Governance Board for trust-building, and closing with
  accessibility/privacy commitments (no ads, GDPR-compliant, anonymous-by-default).

## 2. Listing Copy (AR) — الوصف بالعربية

- **اسم التطبيق:** المسبحة — تسبيح وذكر
- **الوصف المختصر:** مسبحة رقمية فاخرة، أذكار موثقة، والقرآن الكريم — دون اتصال، وبلا إعلانات.
- Full Arabic description authored natively by a qualified reviewer per the
  [Brand Identity §7 voice guidance](03-BRAND-IDENTITY.md#7-voice--tone) — never machine-translated
  from the English listing.

## 3. Visual Assets Required

| Asset | Spec |
|---|---|
| App icon | 512×512 (Play), 1024×1024 (App Store), adaptive icon layers for Android |
| Feature graphic (Play) | 1024×500 |
| Screenshots | Phone (min 4, max 8) + tablet, both in Arabic (RTL) and English locales — never
  reuse mirrored screenshots without verifying actual RTL rendering |
| Preview video | 15–30s, shows the Counter core loop and the luxury motion language from the
  [Design System §7](02-DESIGN-SYSTEM.md#7-motion--haptics) |

## 4. Store Categorization & Metadata

- Category: Lifestyle / Health & Fitness sub-category where available (avoid "Entertainment" —
  mismatched tone); Play Store additionally tagged under Religion/Spirituality where supported.
- Content rating: All ages / Everyone, with the religious-content declaration completed accurately
  on both stores.
- Keywords (ASO): tasbeeh, dhikr, adhkar, misbaha, tesbih, Qur'an offline, Islamic prayer beads,
  99 names of Allah — localized keyword sets per target locale, not a single global list.

## 5. Compliance Declarations

- **Data safety section (Play) / Privacy Nutrition Label (App Store):** Must accurately reflect
  the anonymous-by-default model and granular consent design from
  [Security Framework §4](09-SECURITY-FRAMEWORK.md#4-data-classification--gdpr-compliance) —
  declared data collection kept to the documented minimum, not padded defensively.
- **Target API level / platform version compliance:** tracked release-over-release against each
  store's minimum requirement, owned by the release engineering function in
  [Deployment Plan §2](10-DEPLOYMENT-LAUNCH-PLAN.md#2-cicd-pipeline).
- **Export compliance (encryption declaration):** required given at-rest/in-transit encryption
  use ([Security Framework §2–3](09-SECURITY-FRAMEWORK.md)); standard exemption for the
  encryption use case applies but must be filed correctly per store per market.
- **Religious content review:** proactively supply the Governance Board's review process
  documentation to store reviewers if requested, reducing risk of manual-review delay for
  sensitive-content classification.

## 6. Localization Rollout for Store Listings

Store listing localization ships in lockstep with the [Deployment Plan's phased market launch](10-DEPLOYMENT-LAUNCH-PLAN.md#4-phased-market-launch) —
a market is never opened without its store listing localized and reviewed by a native speaker
first.

## 7. Post-Submission Monitoring

Dedicated dashboard (Admin Console, [Admin Dashboard §5](07-ADMIN-DASHBOARD.md#5-platform-operations-screens))
tracks store review status, rejection reasons if any, and review-to-publish latency per market to
continuously tune future submissions.
