# Tuḥfat al-Aṭfāl — A Critical English Edition

This folder contains the flagship-designed critical edition of "A Critical English Edition of Tuḥfat al-Aṭfāl wa-l-Ghilmān fī Tajwīd al-Qurʾān," Sulaymān al-Jamzūrī's 61-verse didactic poem on Tajwīd, translated and annotated by Ahmad Sulaimiy.

## What's in the file

`Tuhfat-al-Atfal-A-Critical-English-Edition.docx` / `.pdf` (identical layout, 234 pages, ~6.14"×9.21" academic trim) include:

- Half title, title page (with the poem's opening line in Arabic), copyright page, dedication, "A Note to the Reader," and Textual Notes (newly written for this edition — see below)
- All eight parts of the poem exactly as the manuscript defines them, verse by verse: Arabic text, DMG transliteration, a three-column word-for-word gloss table, smooth prose translation, linguistic and rhetorical analysis, and Tajwīd/phonetic commentary
- Every expository rule-essay the manuscript contains between verses (rationale, comparison with Ibn al-Jazarī, common learner errors, worked examples), preserved in full
- 78 worked Qurʾānic examples in styled callout boxes, each with the āyah, transliteration, translation, and application
- Back matter: Appendix A (Glossary of Tajwīd terms), Appendix B (Qurʾānic Index — every citation indexed by sūrah in canonical order), Appendix C (Biography of al-Jamzūrī), Bibliography, Afterword, About the Editor
- Appendix D: a Companion Quick-Reference Guide — the shorter, simpler beginner's guide to the same poem found appended to the source manuscript, kept as a clearly labeled bonus section
- A redesigned cover and back cover: a near-black frame around a deep-oxblood inset panel with a double gold rule border, a rasterized gold rub al-ḥizb star (rendered as a proper vector ornament, not a font glyph) used as a divider and a colophon medallion, and the same ornament reused consistently at every Part heading throughout the body — replacing the original flat, single-color cover

## Editorial notes

- **Structural gap in the source:** the manuscript's own Table of Contents promised a Textual Notes section and four appendices (Glossary, Qurʾānic Index, Biography, Bibliography) that were never actually written in the body — the critical edition simply ended after Verse 61's commentary. Per your confirmation, this edition **authors those missing sections**, grounded in facts already established in the manuscript's own Introduction (editions of al-Ḍabbāʿ and Qamḥāwī, al-Jamzūrī's known works, his teacher al-Mayhī, etc.) and standard, real Tajwīd/Qurʾānic-sciences reference works.
- **The appended "Simple Guide":** a second, unrelated beginner's document was appended after the critical edition's own ending, uncredited in the TOC. Per your confirmation, it's kept as **Appendix D**, clearly separated and labeled as a companion rather than folded into the critical edition itself.
- **Qurʾānic Index:** built mechanically from the 78 worked examples actually present in the manuscript — every sūrah name, āyah reference, and rule was extracted programmatically from the source text, not invented.
- **Fidelity of the verse commentary:** the entire verse-by-verse and rule-essay content is the source manuscript's own scholarship, preserved in full; nothing in the critical edition's main body was rewritten or condensed.

## Scholarly review pass

The first version of this edition typeset the source manuscript's Tajwīd and Qurʾānic-sciences content faithfully, but without independently verifying it. Because this is a text whose entire purpose is teaching correct Qurʾānic recitation, that was the wrong priority — content accuracy has to come before formatting. Before this revision shipped, the full 61-verse commentary was split into 15 sections and each was independently reviewed by a subject-matter pass acting as a Tajwīd/ʿulūm al-Qurʾān scholar, checking every Qurʾānic citation against the actual muṣḥaf text, every attribution to Ibn al-Jazarī/al-Shāṭibī/al-Ḍabbāʿ, and every phonetic and grammatical claim.

That review surfaced roughly 100 genuine issues, since corrected in the text. The most consequential:

- **Two reversed Tajwīd rulings** — the manuscript said Ḥafṣ reads *iẓhār* (clear pronunciation) for "qul rabbi" and "nakhluqkum" when Ḥafṣ actually performs *idghām* (assimilation) in both — the kind of error that would directly mis-teach recitation.
- **A vocalization that changed a word's meaning** — أَلْفٍ ("a thousand") appeared where أَلِفٍ ("an alif," the letter) was meant, reproduced wrong in the Arabic, the transliteration, and the gloss table alike.
- **Roughly 20 fabricated or mismatched Qurʾānic citations** — verses that didn't exist at the cited sūrah:āyah, or that didn't actually contain the phrase being quoted.
- **Misattributed and fabricated quotations**, including a passage cited as "Ibn al-Jazarī states" that was word-for-word al-Jamzūrī's own verse, and a classical commentary by Abū Shāmah al-Maqdisī (13th century) wrongly listed among al-Jamzūrī's own works.
- **Systematic errors in the rāʾ tafkhīm/tarqīq rule** (light vs. heavy pronunciation), repeated across multiple sections.
- **Unedited AI drafting artifacts** — several passages still contained visible "wait, that's not a good example, let me find another" scratch reasoning that had never been cleaned up before this edition's source manuscript was written.

One correction from that pass was itself wrong and was caught and reverted during a second verification step: the review had flagged "our shaykh, al-Mayhī, possessor of perfection" as a fabricated quotation, but it is in fact genuine — verse 5 of the poem itself, confirmed against the published Arabic text. That case is a useful reminder that this kind of review, however careful, is not infallible and its own findings were spot-checked before being applied.

All corrections and the reasoning behind them are in the edit history of this branch; nothing was changed silently.

## Formatting note

Validated against the DOCX schema (passed) and visually proofed page-by-page as a rendered PDF. One real bug surfaced and was fixed during the original proofing pass: EB Garamond's bold and italic faces are missing the hamza (ʾ) and ʿayn (ʿ) transliteration glyphs used throughout a text about Tajwīd — words like "Qurʾān" were rendering with a gap. Fixed by routing those specific characters through Amiri (which has full coverage at every weight) wherever they appear, even mid-word inside ordinary English sentences.
