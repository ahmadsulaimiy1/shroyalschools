# Hijri & Gregorian Calendar — Sourcing & Verification

## Library

Date conversion uses **`hijri`** (`pub.dev/packages/hijri`, BSD-2-Clause
licensed, no runtime dependencies), which implements the **Umm al-Qura
tabular calendar** -- the same convention used officially by the Kingdom
of Saudi Arabia. This was chosen over hand-deriving the conversion
algorithm (error-prone, hard to independently verify) and matches the
"computable from the calendar itself, not a separate licensed dataset"
approach used for this app's other unblocked features: the conversion is
pure on-device arithmetic, so it works fully offline and required no
licensing review.

## Islamic events shown

`core/services/hijri_calendar_service.dart` lists a standard set of Hijri
calendar dates: Islamic New Year, Ashura, Mawlid al-Nabi, start of
Ramadan, an estimated Laylat al-Qadr night, Eid al-Fitr, Day of Arafah,
and Eid al-Adha. These are fixed points on the Hijri calendar itself
(month + day), not a separately sourced dataset -- each event's Gregorian
date is computed on-device via the same conversion.

Two of these carry a genuine disclosed caveat, shown directly in the
calendar screen (`calendar_disclaimer`):

- **Mawlid al-Nabi** (12 Rabi' al-Awwal) is observed by many communities
  but treated as an innovation (bid'ah) to avoid by others -- the app
  lists it only as a calendar *date*, taking no position on whether or
  how to mark it.
- **Laylat al-Qadr** is traditionally understood to fall on one of the
  odd nights in the last ten nights of Ramadan, with its exact night
  deliberately unknown; 27 Ramadan is the most commonly cited estimate in
  general calendars, shown here labelled explicitly as an estimate, not
  a claimed certainty.

## Known limitation

Hijri dates calculated by a tabular algorithm can differ by a day from a
given local community's moon-sighting-based announcement (the two
methods are genuinely different ways of determining a Hijri month's
start, not a bug in either) -- disclosed directly in-app rather than
presented as unqualified fact.
