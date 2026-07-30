# Hisn al-Muslim Import — Verification Report

**Source:** Hisn al-Muslim ("Fortress of the Muslim"), Sa'id bin Ali bin Wahf
Al-Qahtani. This is one of the most widely republished Islamic manuals in
print, organized by daily-life occasion (waking, sleeping, prayer, travel,
etc.) rather than by Qur'anic/Prophetic origin — the structure this app's
Phase 3 directive asked for, and which الورد المصفى (the Phase 2 source) does
not have.

## 1. Why a second source

docs/13-ADHKAR-IMPORT-VERIFICATION-REPORT.md documented that six of the ten
`AdhkarCategory` values (`morning`, `evening`, `sleep`, `wakeUp`, `prayer`,
`travel`) were intentionally left empty after Phase 2, because الورد المصفى
does not contain that taxonomy and fabricating content to fill it would have
misrepresented invented text as authentic. This import adds a second,
independently-sourced compilation that does use this taxonomy, rather than
inventing content to force the first source into a shape it doesn't have.

## 2. Sourcing method

No PDF of Hisn al-Muslim was supplied for this phase, unlike الورد المصفى in
Phase 2. Three research agents compiled the six categories by searching for
and cross-referencing the book's Arabic text, English translation, and
transliteration against multiple independent, well-established Islamic
reference sources (hadith encyclopedias, verse-by-verse Hisn al-Muslim
commentary sites, and established English-translation mirrors), rather than
relying on a single source or on unverified memory. Direct WebFetch access to
several primary hosting sites (sunnah.com, hisnmuslim.com, islamhouse.com,
etc.) returned HTTP 403 in this environment; agents fell back to WebSearch
snippets and GitHub-hosted structured mirrors of the same published material,
cross-checking Arabic wording word-for-word across at least two sources per
entry before finalizing it. Entries were dropped rather than guessed at
wherever sources disagreed or a fixed wording doesn't exist in the source
(e.g. the free-form supplication between adhan and iqamah).

## 3. Entry counts

| Category | New entries |
|---|---|
| `morning` | 26 |
| `evening` | 23 |
| `prayer` | 32 |
| `travel` | 15 |
| `sleep` | 13 |
| `wakeUp` | 3 |
| **Total added** | **112** |

Combined with the 231 entries from Phase 2, the Adhkar library now totals
**343 entries** across all ten categories — no category is empty:

| Category | Count | Source |
|---|---|---|
| `dailyDuas` | 95 | الورد المصفى |
| `quranicDuas` | 49 | الورد المصفى |
| `protection` | 45 | الورد المصفى |
| `generalDhikr` | 42 | الورد المصفى |
| `prayer` | 32 | Hisn al-Muslim |
| `morning` | 26 | Hisn al-Muslim |
| `evening` | 23 | Hisn al-Muslim |
| `travel` | 15 | Hisn al-Muslim |
| `sleep` | 13 | Hisn al-Muslim |
| `wakeUp` | 3 | Hisn al-Muslim |

## 4. Notes on specific entries

- The morning/evening chapters share many identical du'as differing only in
  a "morning"/"evening" wording variant (e.g. "أصبحنا" vs "أمسينا") — both
  variants were kept as separate entries since the book itself treats them
  as distinct recitations for their respective times.
- Repetition counts were preserved exactly as the source specifies,
  including entries recited 3×, 4×, 7×, 10×, 33×, and 100× — these are not
  simplified to a default of 1.
- One entry present in an initial source draft (Al-Baqarah 2:285-286 in the
  morning/evening chapter) was excluded after a second source confirmed it
  belongs to the "before sleeping" chapter, not morning/evening — it is
  correctly included once, under `sleep`, instead.
- "Turning over during the night" and "fear/distress during sleep" (short
  related chapters) were folded into `sleep` rather than kept as separate
  categories, since the app's schema has no dedicated slot for them and they
  are thematically continuous with going-to-sleep remembrance.

## 5. Known limitations

- As with Phase 2, no automated emulator/device testing was performed in
  this sandbox (no Android runtime available). The entries above should be
  spot-checked against a printed copy of Hisn al-Muslim or a device before
  release, same as recommended for the Phase 2 content.
- Sourcing relied on WebSearch-retrieved text rather than direct visual
  transcription (no source PDF was provided for this phase), which is a
  materially different verification method than Phase 2's page-image
  transcription. Cross-referencing multiple independent sources per entry is
  the mitigation, but this is disclosed here rather than left implicit.
