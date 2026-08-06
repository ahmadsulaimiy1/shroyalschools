# Advanced Notifications & Worship Reminders — Architecture & Limitations

## Library

Scheduling uses **`flutter_local_notifications`** (MIT licensed, the
de-facto standard local-notification plugin for Flutter) together with the
**`timezone`** package (also used by `flutter_local_notifications`'s own
recommended pattern) for timezone-aware exact scheduling, and
**`flutter_timezone`** to resolve the device's actual IANA timezone name at
runtime (`timezone` itself has no way to detect this). All scheduling is
local -- no server, no push notifications, consistent with the rest of the
app's offline-first design.

## What was built (Phase 5 Part 3, Priority 1)

- **`core/services/notifications/notification_service.dart`** -- thin
  wrapper: plugin/timezone init, 14 Android notification channels (one per
  reminder *kind*, so a user can mute/re-tone one type from Android's own
  settings without affecting others), POST_NOTIFICATIONS + exact-alarm
  permission requests, and a small schedule/cancel API.
- **`core/services/notifications/reminder_settings_controller.dart`** --
  persisted preferences for every reminder category listed in the
  directive: Prayer (Adhan, early, Iqamah, missed), Tahajjud (smart/manual
  time, gentle/strong wake, escalating heads-up, multiple alarms,
  vibration pattern), Qur'an (reading, Khatm, memorisation), Adhkar
  (morning/evening/sleep/travel), Friday (Jumu'ah), plus global Quiet
  Hours and a Ramadan Mode toggle.
- **`core/services/notifications/reminder_scheduler.dart`** -- turns those
  preferences into concrete scheduled notifications:
  - Fixed-clock-time reminders (Adhkar, Qur'an reading/Khatm/memorisation)
    use the plugin's native daily/weekly repeat rules
    (`DateTimeComponents.time` / `.dayOfWeekAndTime`), so once scheduled
    they don't need re-arming.
  - Prayer-linked reminders (Adhan, early, Iqamah, missed) and Tahajjud
    can't use a fixed repeat rule -- prayer times shift by a few minutes
    every day. These are computed as one-off notifications for a rolling
    **10-day window**, recomputed (idempotently, via deterministic
    notification ids) on every app launch and whenever prayer or reminder
    settings change.
  - **Smart Tahajjud time** uses adhan_dart's `SunnahTimes.lastThirdOfTheNight`
    -- the classical last-third-of-the-night definition, computed from
    that night's actual Maghrib and the next day's Fajr for the user's
    location, not an arbitrary fixed clock time.
  - **Missed Prayer reminder** integrates with Masjid Mode's existing
    "Finished Praying" button: tapping it cancels that prayer's still-
    pending Iqamah/Missed reminders for today, so a reminder never fires
    for a prayer just prayed. This is the one place the app tracks
    "prayed" state at all -- there's no broader prayer-tracking log.
  - **Ramadan Mode** is auto-detected from the Hijri calendar (current
    Hijri month = Ramadan) via the already-shipped `HijriCalendarService`,
    not a separate dataset.

## Android manifest / build changes

- `RECEIVE_BOOT_COMPLETED`, `SCHEDULE_EXACT_ALARM`, `USE_FULL_SCREEN_INTENT`
  permissions; the plugin's scheduled-notification and boot-rescheduling
  receivers; `showWhenLocked`/`turnScreenOn` on the main activity (needed
  for Tahajjud's "Strong" wake style, a genuine full-screen alarm rather
  than an ordinary notification).
- Gradle: core-library desugaring + `multiDexEnabled` (required by the
  plugin for scheduled notifications on older API levels) and the
  `desugar_jdk_libs` dependency.
- Deliberately used `SCHEDULE_EXACT_ALARM` (requested from the user at
  runtime, with a graceful fallback to inexact scheduling if declined)
  rather than `USE_EXACT_ALARM`, which Android reserves for alarm-clock/
  calendar-category apps and carries its own store-review expectations
  this app doesn't need to take on for a reminder feature.
- The notification/exact-alarm permission is **only ever requested when
  the user turns a specific reminder on**, from the Notifications settings
  screen -- never pre-emptively on first launch.

## Known limitations (disclosed rather than glossed over)

- **Rolling-window prayer reminders**: if the app is not opened for more
  than 10 days, prayer-linked and Tahajjud reminders stop firing until
  the next launch re-primes the window. A true "always current" schedule
  would need a background daily trigger (e.g. `workmanager` or
  `android_alarm_manager_plus`), which was out of scope for this pass --
  the fixed-clock-time reminders (Adhkar, Qur'an) don't have this
  limitation since they use the plugin's native repeat rules.
- **Missed Prayer detection is not real tracking**: the app has no
  broader "did I pray this prayer" log. The reminder fires unconditionally
  after the configured delay unless the user has tapped Masjid Mode's
  "Finished Praying" for that specific prayer in the meantime.
- **OEM background restrictions**: some Android manufacturers (Xiaomi,
  Huawei, and others) aggressively kill background apps regardless of
  what this app requests -- a known, widely documented limitation of the
  underlying `AlarmManager` API itself, not something a Flutter plugin can
  work around. Users on affected devices may need to allow-list Misbaha in
  their device's battery-optimisation settings.
- **Not verified on a physical device**: like the rest of this app's
  sensor/notification-dependent features, exact-alarm delivery, full-
  screen-intent behaviour, and boot-rescheduling cannot be exercised in
  this build sandbox (no emulator or device available) and should be
  spot-checked on real hardware before release.
- **No deep-linking from a tapped notification** yet -- tapping any
  reminder opens the app to wherever it was left, not the specific
  relevant screen (e.g. the Tahajjud reader). Scoped out of this pass to
  keep it focused on getting the scheduling system itself right; a
  follow-up could wire `onDidReceiveNotificationResponse` payloads to
  specific routes.
