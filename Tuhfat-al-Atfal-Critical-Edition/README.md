# Tuḥfat al-Aṭfāl — A Critical English Edition

This folder contains the flagship-designed critical edition of "A Critical English Edition of Tuḥfat al-Aṭfāl wa-l-Ghilmān fī Tajwīd al-Qurʾān," Sulaymān al-Jamzūrī's 61-verse didactic poem on Tajwīd, translated and annotated by Ahmad Sulaimiy.

## What's in the file

`Tuhfat-al-Atfal-A-Critical-English-Edition.docx` / `.pdf` (identical layout, 263 pages, 7"×10" luxury scholarly trim) include:

- Half title, blank verso, series title page, title page (with the poem's opening line in Arabic), copyright page, dedication, Endorsements, Editorial Board, Advisory Council, About the Editor, About the University, Publisher's Note, Preface, Methodology, Transliteration System, Abbreviations, Editorial Principles, Acknowledgements, Table of Contents, List of Tables, Reading Guide, "A Note to the Reader," and Textual Notes
- Full-page illuminated Part openers for all eight parts — large Arabic and English titles, a rasterized rub al-ḥizb star medallion, inside a bordered ivory plate — plus a dynamic running head on every right-hand page showing the current Part title
- All eight parts of the poem exactly as the manuscript defines them, verse by verse: Arabic text, DMG transliteration, a three-column word-for-word gloss table, smooth prose translation, linguistic and rhetorical analysis, and Tajwīd/phonetic commentary
- Every expository rule-essay the manuscript contains between verses (rationale, comparison with Ibn al-Jazarī, common learner errors, worked examples), preserved in full
- 78 worked Qurʾānic examples in styled callout boxes, each with the āyah, transliteration, translation, and application
- Back matter: Afterword, Appendix A (Glossary of Tajwīd terms), Appendix B (Qurʾānic Index), Appendix C (Biography of al-Jamzūrī), Index of Arabic Terms, Index of Tajwīd Rules, General Index, Bibliography, About the Editor, Future Publications, Colophon
- Appendix D: a Companion Quick-Reference Guide — the shorter, simpler beginner's guide to the same poem found appended to the source manuscript, kept as a clearly labeled bonus section

## Design overhaul (second pass)

The first redesign (deep-oxblood/antique-gold, described further below) fixed the "flat and reddish" complaint but was, on its own terms, still an academic PDF rather than a flagship publication. This second pass rebuilt the production values from the ground up against an explicit brief targeting the caliber of Oxford University Press / Brill / major institutional Islamic-studies publishing:

- **Palette:** replaced the oxblood scheme with deep royal navy (`#082A66`), antique gold (`#C8A75D`), warm ivory (`#FAF8F3`), and dark espresso ink — a restrained two-hue-plus-gold system throughout, cover to colophon.
- **Typography:** Cormorant Garamond for display/headings, EB Garamond for body text, Source Serif 4 for tabular matter, Amiri for Arabic — Cormorant Garamond and Source Serif 4 are genuine open-source (SIL OFL) fonts fetched and installed for this build. Trajan Pro, Minion Pro, and Adobe Caslon, named in the brief, are commercial Adobe fonts not available in this environment; EB Garamond (already licensed and used throughout the earlier books in this series) stands in for the body-text family.
- **Cover, back cover, and colophon page:** a bordered navy panel inside a near-black outer frame, gold double rule, the rub al-ḥizb star as both divider and medallion, full title/subtitle/author/university hierarchy.
- **Running heads and footers:** true verso/recto pages (Word's even/odd header mechanism) — the book title on left-hand pages, a *live* field on right-hand pages that tracks the current Part automatically; outer-aligned page numbers with a publisher mark and section indicator, replacing the old centered page number.
- **Table of Contents, List of Tables, and all back-matter indices:** genuinely computed, not hand-typed guesses. Word's native TOC field doesn't get resolved by the LibreOffice pipeline used to render the PDF, so these are built by a small two-pass process (`gen_toc_pages.js`): render once, search the actual output for where each heading/term/table lands, feed real page numbers back into a second build. All entries print real page numbers except one Part VII heading long enough to wrap awkwardly across lines in the source text search — it shows "—" rather than a guess.
- **Tables and callout boxes:** navy/gold/ivory "Brill-style" table borders throughout; a differentiated callout system (Worked Example, Tajwīd Insight, Teacher's Note, Memorisation Note, Advanced Discussion, Historical Note, Common Student Errors) distinguished by border color and style — applied to content the manuscript already contains, not invented to fill out the taxonomy.
- **Footnotes:** real Word footnotes (not endnotes) are now supported and demonstrated on the Methodology page; the existing bracketed `[sūrah: āyah]` inline citation convention was kept for the 78 worked examples themselves, since that's the standard convention in Tajwīd texts and rewriting all 78 into footnotes would have been a cosmetic change with no accuracy benefit.
- **Print specification:** the interior is laid out to a 7"×10" trim as a design target for a matte-laminated hardback on cream stock — noted on the Colophon page. A separate print-ready wraparound cover (front + spine + back, with a computed spine width) needs a specific printer/POD vendor's template to build against; none was specified, so it wasn't attempted rather than guessing at one that might not match a real print run.

### Content the editor still needs to supply

Three sections are placeholders, not fabricated content — see them for what they are before printing:

- **Endorsements**, **Editorial Board**, and **Advisory Council** — the brief asked for these, but populating them with invented names or quotations would misrepresent who actually reviewed this work. Each page states plainly that it's awaiting real content.
- **About Al-Mulk International University** — kept to name, location, and a one-line description per your instruction; no institutional history, founding date, or accreditation claim was invented.
- Nothing in this edition claims endorsement, commissioning, or association with King Fahd Complex, King Salman Global Academy, Oxford University Press, Brill, or the Saudi Royal Court — the design targets that production caliber; it doesn't claim their institutional backing, which doesn't exist.

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
