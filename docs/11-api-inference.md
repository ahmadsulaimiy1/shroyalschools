# 11 — API Proposal

> ## ⚠ Read this first
>
> **This is a proposed API design, not documentation of an existing one.**
>
> The live LMS exposes no public API. Its authenticated surface is server-rendered ASP.NET
> MVC. The only **[OBSERVED]** endpoints are the public form routes in `08-lms.md` §3.
>
> This document specifies (a) the minimal integration contract the marketing site needs from
> the LMS, and (b) a fuller API if the platform is modernised.

---

## 1. Observed API surface

### `itqan-quran.com` (WordPress)
**[OBSERVED]** `/wp-json/` is open and unauthenticated. Namespaces: `wp/v2`,
`oembed/1.0`, `litespeed/v1`, `litespeed/v3`, `wordfence/v1`, `wp-site-health/v1`,
`wp-block-editor/v1`, `wp-abilities/v1`.

⚠ **Security note:** `/wp/v2/users` is reachable and enumerates usernames — standard
WordPress behaviour, and a standard hardening target. `xmlrpc.php` is also exposed.
Neither is used by this theme. Disable both.

**[OBSERVED]** Installed plugins inferred from namespaces: **LiteSpeed Cache** and
**Wordfence Security**. No LMS, e-commerce or form plugin exists.

### `register.itqan-quran.com` (ASP.NET)
**[OBSERVED]** — form endpoints only, all HTML responses:

| Endpoint | Method | Auth |
|---|---|---|
| `/Account/Login` | GET, POST | Public |
| `/Account/Reset` | GET, POST | Public |
| `/Account/Register?i=<GUID>` | GET, POST | Public |
| `/ClosedCircleType/CreateNeedToRegisterdUser?circleTypeId=<int>` | GET, POST | Public |
| `/Home/About` | GET | Public |

Plus a **[OBSERVED]** SignalR hub (client 5.0.11) driving `/js/notifications.js`.

---

## 2. The one integration that matters ⭐

Everything else in this document is optional. **This is not.**

The marketing site currently cannot tell whether a track is open. That single missing fact
causes the 61% dead-end documented in `08-lms.md` §4.6.

### `GET /api/v1/tracks`

```http
GET /api/v1/tracks?gender=female&residency=ksa&locale=ar
```
```json
{
  "data": [
    {
      "token": "11c3ac58-1473-42fc-9184-2ce1987411d9",
      "code": "A11",
      "name": { "ar": "قسم الروضة والتأسيس", "en": "Nursery & Foundation" },
      "gender": "female",
      "residency": "ksa",
      "age_range": { "min": 3, "max": 6 },
      "availability": {
        "status": "closed",
        "capacity": 40,
        "enrolled": 40,
        "places_left": 0,
        "waitlist_count": 27,
        "reopens_at": "1448-07-01",
        "reopens_at_gregorian": "2026-12-10"
      },
      "register_url": "https://register.itqan-quran.com/Account/Register?i=11c3ac58-…",
      "waitlist_url": "https://register.itqan-quran.com/waitlist/11c3ac58-…"
    }
  ],
  "meta": { "total": 7, "open": 0, "closed": 7, "generated_at": "2026-08-20T06:00:00Z" }
}
```

**Contract:** public, read-only, no PII, cacheable for 60–300 s.
**Enables:** live availability badges, honest "full — reopens in Rajab" messaging, inline
waitlist capture, and a router that never sends anyone to a dead end.

**If only one thing in this document is built, build this.**

---

## 3. Waitlist capture

### `POST /api/v1/waitlist`
```json
{
  "track_token": "11c3ac58-1473-42fc-9184-2ce1987411d9",
  "full_name": "أحمد بن محمد بن عبدالله",
  "email": "ahmad@example.com",
  "whatsapp": "+966501234567",
  "age": 8,
  "gender": "male",
  "country_code": "SA",
  "preferred_language": "ar",
  "consent_to_contact": true,
  "guardian": { "full_name": "محمد بن عبدالله", "email": "…", "relationship": "father" }
}
```
`201 Created` → `{ "id": "…", "position": 28, "estimated_reopening": "1448-07-01" }`

**vs today [OBSERVED]:** name + WhatsApp only, no email, no confirmation, no position.
`email` and `consent_to_contact` are the fields that turn this from a dead end into a
pipeline. `guardian` is required when `age < 18`.

---

## 4. Registration & auth

```
POST /api/v1/registrations          Enrol in a track
GET  /api/v1/registrations/{id}     Status
POST /api/v1/auth/request-code      [OBSERVED] passwordless — send code to email
POST /api/v1/auth/verify-code       [OBSERVED] exchange code for session/JWT
POST /api/v1/auth/logout
GET  /api/v1/me
```

`POST /api/v1/registrations` mirrors the **[OBSERVED]** 13-field form:
`track_token`, `full_name`, `gender`, `date_of_birth` *(not `age` — see `10`)*, `email`,
`country_code`, `mobile`, `preferred_language`, `hefz_daily_count`, `hefz_duration`,
`referral_source`, `circle_id?`, `guardian?`, `consent`.

**Error format** — replaces the **[OBSERVED]** `data-val-required="*"`:
```json
{ "error": { "code": "validation_failed",
  "fields": { "email": { "code": "invalid_format",
    "message": { "ar": "يرجى إدخال بريد إلكتروني صحيح", "en": "Please enter a valid email address" } } } } }
```
Localised, specific, machine-readable. An asterisk is not an error message.

`409 track_full` must return the waitlist URL so the client can recover in place rather than
redirecting to a dead end.

---

## 5. Student, teacher, supervisor, admin

```
# Student
GET  /api/v1/me/enrollments
GET  /api/v1/me/sessions?from&to
GET  /api/v1/me/progress
POST /api/v1/me/recitation-reports     # [OBSERVED] required by terms clause 4
GET  /api/v1/me/attendance
GET  /api/v1/me/certificates
GET  /api/v1/me/notifications

# Teacher
GET   /api/v1/teacher/circles
GET   /api/v1/teacher/circles/{id}/students
POST  /api/v1/teacher/sessions/{id}/attendance
GET   /api/v1/teacher/recitation-reports?status=pending
PATCH /api/v1/teacher/recitation-reports/{id}   # grade + notes

# Supervisor
GET /api/v1/supervisor/teachers
GET /api/v1/supervisor/quality-reviews
GET /api/v1/supervisor/circles/{id}/metrics

# Admin
GET   /api/v1/admin/enrollment-funnel?from&to&group_by=track,gender,country
GET   /api/v1/admin/capacity              # ⭐ drives the availability API
PATCH /api/v1/admin/tracks/{token}        # open/close, set reopens_at
GET   /api/v1/admin/waitlist?track&status
POST  /api/v1/admin/waitlist/notify       # ⭐ notify on reopening
POST  /api/v1/admin/certificates/issue
GET   /api/v1/admin/staff-applications

# Public
GET /api/v1/certificates/verify/{code}    # ✚ third-party verification of Maknoon certs
```

`GET /api/v1/admin/capacity` and `POST /api/v1/admin/waitlist/notify` are the operational
pair that close the loop opened by the 22 closed tracks.

---

## 6. Real-time (SignalR — **[OBSERVED]**)

A SignalR hub already exists. Proposed event contract:

| Event | Payload | Recipients |
|---|---|---|
| `session.starting` | circle, session, join URL | Enrolled students |
| `report.reviewed` | report id, rating | Student |
| `attendance.recorded` | session, status | Student, guardian |
| `track.reopened` | track token, name | ⭐ Waitlisted users |
| `message.received` | thread, sender, preview | Recipient |
| `certificate.issued` | certificate id | Student, guardian |

`track.reopened` is the event that makes the waitlist worth having.

---

## 7. Cross-cutting requirements

**Auth** — Bearer JWT, short-lived access + rotating refresh; passwordless codes hashed,
10-minute expiry, rate-limited issuance and verification.

**Rate limits** — `auth/request-code` 3/hour/email · `waitlist` 5/hour/IP ·
`registrations` 3/hour/IP · public reads 60/min/IP.

**Errors** — consistent envelope; localised messages; never leak stack traces.
**Pagination** — cursor-based; `{ data, meta: { next_cursor, total } }`.
**Versioning** — `/api/v1/`; additive changes only within a major version.
**i18n** — `Accept-Language` honoured; all user-facing strings localised to the 8-locale set
in `09-user-flows.md` §6.
**Security** — HTTPS only; HSTS; CSRF on cookie-authenticated routes
*(**[OBSERVED]** `__RequestVerificationToken` already in use — good)*; CORS restricted to
known origins; reCAPTCHA retained on public writes; **no PII in URLs**; audit-log every
admin mutation.
**Privacy** — minors' data is in scope: minimise fields, define retention, honour deletion,
require guardian consent for under-18s. Note the **[OBSERVED]** live form collects a phone
number the site never uses — a good example of the minimisation to apply.

---

## 8. Third-party integrations

| Service | Status | Purpose |
|---|---|---|
| Cloudflare | **[OBSERVED]** both hosts | CDN, WAF, email obfuscation |
| Google reCAPTCHA v3 | **[OBSERVED]** LMS | Bot protection |
| Google Fonts | **[OBSERVED]** both | ⚠ Self-host — privacy + performance |
| Google Forms | **[OBSERVED]** ×7 | ⚠ Migrate into the platform |
| Google Drive | **[OBSERVED]** ×7 | ⚠ Self-host |
| WhatsApp (`wa.me`) | **[OBSERVED]** | Support — consider Business API for waitlist notices |
| YouTube | **[OBSERVED]** | Channel `@-Itqan-quran01` |
| LiteSpeed Cache | **[OBSERVED]** | WP caching |
| Wordfence | **[OBSERVED]** | WP security |
| intl-tel-input | **[OBSERVED]** | Phone input — removable with the router redesign |
| Video conferencing | **Implied**, not identified | Live halaqat run on an external tool |
| Email provider | **Implied** | Login codes must be sent by something |
| Analytics | ❌ **None found on either host** | ⚠ See below |
| Payment gateway | ❌ **None found** | Consistent with nominal/charitable pricing |

### ⚠ No analytics anywhere

No Google Analytics, GTM, Plausible, Matomo or any other tag was found on either host. The
organisation currently has **no visibility** into traffic, funnel drop-off, or the impact of
the 22 closed tracks. Every recommendation in this documentation set is therefore currently
unmeasurable.

Add privacy-respecting analytics (Plausible or Matomo — no cookie banner required, and
appropriate for a platform serving minors) **before** the rebuild, so there is a baseline to
compare against.
