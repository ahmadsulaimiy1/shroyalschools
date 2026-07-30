# Daily Hadith — Source, License, and Sampling Method

## 1. Source

Full collection fetched from `fawazahmed0/hadith-api` (GitHub), edition
`eng-bukhari` — Sahih al-Bukhari, English translation by Muhsin Khan,
`https://raw.githubusercontent.com/fawazahmed0/hadith-api/1/editions/eng-bukhari.min.json`.
This is the same aggregator (and, per its README, the same author) already
used and verified for `docs/15`'s Qur'an data and cross-corroborated
independently in `docs/18` via `Prince77-7/quranMCP`'s published data-source
list, which cites this exact repo for its own hadith feature.

**Why Sahih al-Bukhari specifically**: it is universally regarded across
Sunni Islamic scholarship as the most rigorously authenticated hadith
collection (the name itself, "Sahih," means "authentic") — choosing it
avoids any need to filter by an individual-hadith grading field, unlike
weaker collections where authenticity varies hadith-by-hadith.

**License**: Unlicense (public domain) — confirmed by fetching
`https://raw.githubusercontent.com/fawazahmed0/hadith-api/1/LICENSE`
directly.

**Verification performed**: fetched the full edition (7,589 hadiths),
confirmed the JSON structure (`hadithnumber`, `text`, `reference.book`,
`reference.hadith`, plus a `metadata.sections` table mapping book numbers
to their traditional chapter titles), and spot-checked hadith #1 (the
well-known "actions are judged by intentions" hadith) against its
standard English rendering.

## 2. Why only 365 of the 7,589 hadiths are bundled

The full `eng-bukhari.min.json` is 4.6 MB. This app's "Daily Hadith" home
card only ever needs to show one hadith per calendar day, so bundling the
entire collection for that purpose would be the same kind of unnecessary
size cost this session's APK audit (`docs/17`) was specifically about
avoiding.

Rather than hand-picking 365 hadiths (which would reintroduce a
content-reconstruction/curation-quality risk this project's whole sourcing
discipline exists to avoid), the 365 entries were selected by **deterministic
even-stride sampling** across the full, verified 7,589-hadith collection: a
small Python script computed evenly-spaced indices
(`round(i * (n-1) / 364)` for `i` in `0..364`) so the 365 entries span the
entire collection front-to-back — every one of Sahih al-Bukhari's ~97 books
is represented somewhere in the sample — rather than being a hand-curated
"greatest hits" selection. Each entry is stored verbatim (hadith number,
full English text, book/hadith reference) with no paraphrasing or
alteration.

Bundled asset: `assets/hadith/bukhari_en.json`, ~200 KB (365 entries, down
from 4.6 MB for the full collection).

## 3. How "hadith of the day" is chosen

`HadithRepository.dailyHadith(date)` picks `dayOfYear % 365` from the
365-entry array — deterministic (the same calendar date always shows the
same hadith), cycling through the full sampled set across the year. This
mirrors the existing "verse of the day" pattern added to `QuranRepository`
for the same home-screen feature, which uses `dayOfYear % 6236` over the
full (already-bundled) Qur'an corpus — no new data needed for the Daily
Ayah card.

## 4. Known limitation

Because only 1-in-~21 hadiths were sampled, related hadiths that are
traditionally read together (e.g. multiple narrations of the same event)
may not all appear — this is a deliberate size/completeness tradeoff for a
"daily reflection card," not a hadith study/browsing tool. A future Hifz/
Islamic-Knowledge-Centre phase that wants full-collection browsing would
need to reconsider bundling the complete edition (or fetching on demand,
matching the Qur'an audio's stream-and-cache pattern) rather than this
sampled subset.
