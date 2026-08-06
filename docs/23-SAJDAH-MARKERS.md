# Sajdah (Prostration) Markers — Sourcing & Verification

## What was added

The 15 verses of Qur'anic prostration (sajdah al-tilawah) are now marked
with a small ۩ rosette next to the ayah number in Mushaf Mode, and a
"Sajdah" chip on the verse card in list/swipe views.

## Sourcing method

Rather than typing out a hand-maintained list of (surah, ayah) pairs from
an external site, the marker is read directly off the app's own already-
bundled, already-verified Uthmani Arabic text (`assets/quran/verses.json`,
sourced and verified in `docs/08`/earlier Qur'an data-sourcing work). That
text already carries the traditional printed-Mushaf sajdah glyph (۩,
U+06E9 ARABIC PLACE OF SAJDAH) embedded at the end of each prostration
verse, matching standard Tanzil/Uthmani typesetting. `QuranVerse.fromJson`
checks for that mark once, records it as `isSajdah`, and strips the raw
glyph out of the stored `arabicText` — the shipped Amiri Quran font has no
guaranteed coverage for this rare annotation codepoint, so rendering code
draws its own themed marker widget instead of trusting the font to shape
an unfamiliar character correctly. No separate list to drift out of sync
with the shipped text.

Scanning the full bundled dataset for this mark returns exactly 15 verses:

| # | Surah:Ayah | Surah name |
|---|---|---|
| 1 | 7:206 | Al-A'raf |
| 2 | 13:15 | Ar-Ra'd |
| 3 | 16:50 | An-Nahl |
| 4 | 17:109 | Al-Isra |
| 5 | 19:58 | Maryam |
| 6 | 22:18 | Al-Hajj |
| 7 | 22:77 | Al-Hajj |
| 8 | 25:60 | Al-Furqan |
| 9 | 27:26 | An-Naml |
| 10 | 32:15 | As-Sajdah |
| 11 | 38:24 | Sad |
| 12 | 41:38 | Fussilat |
| 13 | 53:62 | An-Najm |
| 14 | 84:21 | Al-Inshiqaq |
| 15 | 96:19 | Al-Alaq |

This was cross-checked verse-by-verse against the bundled English
translation and Arabic text for every ambiguous candidate (several
external sources disagree by ±1 ayah, e.g. 16:49 vs 16:50, 17:107 vs
17:109, 27:25 vs 27:26, 41:37 vs 41:38) — in each case the exact ayah
carrying the ۩ mark in the bundled text is the one whose Arabic contains
the actual prostration clause (e.g. 41:38 is "…they glorify Him night and
day, and tire not۩", not 41:37's "…but prostrate to Allah" clause, which
introduces the instruction but is not itself the marked ayah in this
edition's verse-numbering convention).

## Note on madhhab differences

Islamic scholarship differs on the exact status of two of these 15: the
Hanafi school treats all 15 as marked, including Surah Sad (38:24) as an
obligatory (wajib) sajdah; the Shafi'i/Hanbali schools generally count 14,
treating 38:24 as a sujud ash-shukr (thanksgiving prostration prompted by
its narrative content) rather than a sajdah al-tilawah, and grade
Al-Hajj's second sajdah (22:77) as mustahab (recommended) rather than
obligatory. The 15-location marker set used here matches the standard
printed-Mushaf convention (and this app's own bundled Tanzil-derived
text) — it marks *where* the tradition places a sajdah, without itself
asserting a wajib/mustahab ruling for either verse, so it works correctly
for a reader following either school. Given the app's own "Sultan Hanafi
Community" branding, all 15 are shown identically; a future refinement
could add a per-madhhab toggle if requested, but nothing here contradicts
either school's practice.

## What was not built

Line-accurate Hizb/Rub' al-Hizb boundary markers were considered together
with this task, since they're visually similar small in-text markers. They
were **not** added: unlike sajdah locations (independently well-known
public religious knowledge, confirmed directly from the app's own bundled
text), accurate Hizb/Rub' boundaries are typically distributed as part of
a specific Mushaf's page-layout dataset and were not independently
re-derivable from data already in this app. They remain tracked under the
same King Fahd Mushaf page-layout blocker as `docs/21`/`docs/22` (task
#63), rather than approximated.
