# Itqan Virtual Quran Academy — Rebuild Documentation

Technical specification for rebuilding **https://itqan-quran.com/**
(مِقْرَأَة إِتْقَان الِافْتِرَاضِيَّةُ).

**Audit date:** 2026-08-20 · **Method:** live crawl of all public pages, assets, CSS, JS and
HTTP responses across both hosts.

---

## Start here

**[00-executive-summary.md](00-executive-summary.md)** — the findings that change the plan.

Two things to know before reading anything else:

1. **This is two systems, not one.** `itqan-quran.com` is a 14-page WordPress marketing site
   with **no LMS**. The actual LMS is a separate **ASP.NET Core** application on
   `register.itqan-quran.com`, behind a login. Rebuilding the marketing site is small and
   well-bounded; rebuilding the LMS is a separate project that needs source access.

2. **61% of registration journeys dead-end.** 22 of 36 entry points are closed — every
   women's track and every men's international track — and the waitlist they land on does not
   collect an email address. This outweighs every design consideration in these documents.

---

## Contents

| Doc | Contents |
|---|---|
| [00-executive-summary.md](00-executive-summary.md) | Findings, defects, target architecture |
| [01-sitemap.md](01-sitemap.md) | Two-host topology, all 14 pages, broken links, proposed sitemap |
| [02-pages.md](02-pages.md) | Page-by-page: purpose, sections, components, defects |
| [03-components.md](03-components.md) | Component library; the smart registration router in depth |
| [04-design-system.md](04-design-system.md) | Colours, type, spacing, motion + contrast audit |
| [05-assets.md](05-assets.md) | Every asset with measured sizes; third-party dependencies |
| [06-copywriting.md](06-copywriting.md) | **Verbatim Arabic copy** + 13 copy defects |
| [07-forms.md](07-forms.md) | All 12 forms with real field names; validation; gaps |
| [08-lms.md](08-lms.md) | LMS stack, endpoints, **complete 36-track catalogue** |
| [09-user-flows.md](09-user-flows.md) | Current vs proposed journeys; locale consolidation |
| [10-database-inference.md](10-database-inference.md) | ⚠ Schema **proposal** |
| [11-api-inference.md](11-api-inference.md) | ⚠ API **proposal** + the one critical integration |
| [12-rebuild-checklist.md](12-rebuild-checklist.md) | Phased plan, budgets, open questions |

---

## Evidence status

| Documents | Status |
|---|---|
| `01`–`07`, `09` | **Observed** — extracted from live responses. Safe to build from. |
| `08` §1–§5 | **Observed** — the LMS public surface and full track catalogue. |
| `08` §6–§8, `10`, `11` | **Partly inferred** — tagged `[INFERRED]` inline. |

`10` and `11` describe a **proposed** database and API, **not** the existing ones. The live
LMS is login-walled. Do not hand them to a developer as documentation of what exists.

---

## The organisation

An online Quran memorisation and recitation academy under **جمعية مكنون لتحفيظ القرآن الكريم**
(Maknoon Association, Riyadh), partnered with **جمعية إقرأ بالخرمة**. Arabic-first (RTL),
gender-segregated, age-banded across 7 tracks from age 3 to over 40, including a dedicated
**ذوي الهمم** (special needs) track and a **قراءات وإجازات** track granting ijazah with
connected sanad. Teaching is live over external video; pricing is described as
**بأسعار رمزية** (nominal).

---

## Highest-priority actions

1. Add **email capture** to the LMS waitlist — recovers 61% of currently lost intent
2. Show **live availability** on registration pages — stop sending users to dead ends
3. Fix the **FAQ 404** and the dead **المصادر والمعرفة** nav item
4. Correct the **women's WhatsApp number** (currently identical to the men's)
5. Add **analytics** — there is none on either host, so nothing is currently measurable
6. Raise with the client: **.NET 5 is end-of-life**, and there is **no guardian consent
   mechanism for children aged 3+**

Items 5 and 6 are flagged for the client rather than actioned here: one needs an account
decision, the other a policy and legal answer.
