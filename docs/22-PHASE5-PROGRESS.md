# Phase 5 — Royal Islamic Flagship Platform: Progress Report

## 1. About page attribution — updated per explicit confirmation

The directive named two new scholars for the About page's review/approval
chain, but its own text says to only assert this if the review/approval
actually happened -- something not verifiable from this sandbox. This was
confirmed directly with the product owner before adding anything (see the
question asked and its answer in the conversation). With that confirmation,
the About page now shows:

- Islamic Content Supervision: Imam Ahmad Sulaimiy (unchanged, already
  shipped in Phase 3A).
- **Reviewed by**: Shaykh Abdul-Fattah Muiz (Türkiye) -- new.
- **Approved by**: Shaykh Prof. Abdullah Turki (Madinah, Saudi Arabia) --
  new.
- A "shroyalschools.com" website link -- new, added above the existing
  contact email.

## 2. Royal Madinah Mushaf — still blocked on the same licensing check as Phase 4

`docs/21` §2 already found a real, usable King Fahd Complex Mushaf
page-layout dataset (QUL, by Tarteel Inc.) but could not confirm its
redistribution terms because `qul.tarteel.ai` is unreachable from this
sandbox. That remains true -- retried this phase via a different path
(the raw GitHub README for QUL's own code repository, which confirms the
*code* is MIT-licensed but says nothing about the *data*'s terms) and via
web search (which surfaced QUL's own guidance that licensing "varies by
resource" and must be checked per-resource) -- neither route reaches the
actual per-resource license badge needed to confirm the Mushaf-layout
dataset specifically is clear to redistribute. Task #63 remains open,
unchanged.

Hizb/Rub'/Sajdah markers and accurate line layout are all attributes of
this same withheld dataset -- they cannot be added independently of it
without either the same licensing gap or fabricating placement data, which
was never going to happen. Ayah numbers, however, are already correct and
shipped (`_AyahMarker` in `mushaf_flow_text.dart`).

## 3. Tafsir platform — real data found, same blocker as §2

Searched for Ibn Kathir / As-Saadi / Al-Mukhtasar specifically, per the
directive's own examples. Found `spa5k/tafsir_api` (GitHub, MIT-licensed
*redistribution* repository) carrying English **Ibn Kathir** (abridged) and
English **Al-Mukhtasar**, both verified by fetching and reading real
per-verse content directly (spot-checked Al-Fatiha's opening tafsir from
Ibn Kathir -- genuine, well-formatted, matches the known text). No English
**As-Saadi** was found through this source (only an Albanian edition
exists in its edition list) -- disclosed rather than substituted with
something else under the same name.

Both available editions' own metadata cites `qul.tarteel.ai/resources/
tafsir/{id}` as their source -- meaning this is the *same* underlying
per-resource licensing gap as the Mushaf layout in §2, not a separate
question. Tracked as task #73, blocked on the same QUL terms-of-use check.

**Recommendation for whoever performs that check**: since both the Mushaf
layout and the tafsir data live behind the same `qul.tarteel.ai` terms
page, confirming it once resolves both blockers (tasks #63 and #73)
together, not two separate checks.

## 4. Flexible scrolling — shipped (partial)

Two of the five requested scroll behaviours were already effectively
in place before this phase (the card view's vertical `ListView` *is*
"Vertical Scroll"; the Mushaf flow's `SingleChildScrollView` *is*
"Continuous Scroll") and Tahajjud's auto-scroll already existed. This phase
adds:

- **Horizontal Swipe**: a new `QuranScrollMode` setting, toggled from the
  reader toolbar, switches the card view from a vertical list to a
  `PageView` -- one verse per swipe.
- **Custom speed slider** for Tahajjud auto-scroll, alongside the existing
  four named presets (very slow/slow/medium/fast) -- the presets set the
  slider's position; the slider itself allows continuous fine-tuning from
  4 to 70 px/second.

**Not built**: true "Page Mode" (King Fahd Mushaf page-accurate
pagination) -- blocked on the same §2 dataset. Building a page mode that
merely paginates by an arbitrary verse count (not real Mushaf pages) was
considered and rejected as not matching what "Page Mode" means in the
directive -- it would look like a page but not *be* a real Mushaf page,
which is worse than not having it yet.

## 5. Not started this phase (unchanged from `docs/21`'s list)

Calendar Centre, expanded Settings Centre, Advanced Alarm System, Solar &
Prayer Times, the luxury Qiblah Centre redesign, Wear OS, and the AI
Worship Assistant are all still pending -- the same two hard constraints
flagged in `docs/21` §7 (no official Flutter Wear OS support; an AI
assistant needs a backend proxy, not a raw embedded API key) still apply
and haven't been resolved.
