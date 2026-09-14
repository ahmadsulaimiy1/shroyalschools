# The Curriculum — an editorial bible

**Sultan Hanafi Royal Schools · GACAIS**
**Version 1.0 — 14 September 2026. Governing standard for the curriculum corpus.**

*The companion to `docs/editorial-bible.md` in the `sultan-` repository, which
governs the school's visual and brand identity. That bible holds the school's
face. This one holds what it teaches. They answer to the same institution and
to the same discipline, and neither may contradict the other.*

---

## Why this document exists

Written because "build the curriculum" is not a brief anyone can execute twice
the same way, and because the same decision was lost eleven separate times in a
way that could have been predicted from a standard and was not.

Every loss followed one pattern. A document was rebuilt from whatever happened
to be in front of whoever was rebuilding it. Decisions settled weeks earlier
that did not appear *in that particular file* were silently dropped, and the
Director General had to restate them from memory. Nobody disagreed with the
lost decisions. Nobody argued them down. They simply were not written anywhere
that the next rebuild would look.

The register (`00-LOCKED-DECISIONS.md`) is the remedy. This bible is the
standard the register is held to, and the reasoning behind each rule — so that
the rules survive the person who wrote them.

**The eleven losses, named, because a standard that does not name its failures
gets argued with:**

| What was lost | How it came back |
|---|---|
| The three-programme structure and the four sections | Restated by the Director General |
| Two books, then three — one per programme, lower classes | Restated twice; L-06 corrected |
| Class 12 carrying the most | A board overruled it and had to be reversed |
| أصول التفسير · التاريخ والسيرة · الترجمة · مصطلح الحديث | Dropped from the matrix during an unrelated rebuild |
| The booklist of البرنامج الأول | Never written at all — discovered by audit |
| التجويد as an independent science | Ruled by the Qur'anic sciences board; the ruling was mislaid and the science folded back into the memorisation hour, leaving a discipline with a متن and no lesson |
| الرسم العثماني and رواية حفص counted as courses | A chapter of tajwīd and a description of the muṣḥaf, carried for months as two subjects |
| البلاغة opened before النحو | In term one of class 9, while قطر الندى was unfinished that same year |
| البيان before المعاني | The same error one layer down |
| التفسير taught from class one | Meaning given to a child still unlocking the letter |
| Arabic collapsing at the bridge | 61% of the week in class 6, 31% in class 7 — and البحث والخطابة, a stated priority, absent from classes 7, 8 and 9 entirely |

> **وما ليس في هذا السجل فليس بقرار.**
> What is not in the register is not a decision.

---

## I. What the curriculum corpus is for

The corpus is not a description of what the school intends. It is the
instrument by which a child's twelve years are allocated, and by which a
teacher is told what to open on a Monday. Three consequences follow, and every
rule in this bible descends from one of them.

**It is binding before it is persuasive.** A curriculum document that reads
beautifully and cannot be timetabled has failed. Prose that cannot be turned
into a slot, a book, a teacher and a mark is decoration.

**It is read by people who were not in the room.** The Director General will
not be present when a scheme of work is written in class 8 in three years.
Everything the corpus means must be *on the page*, not in the memory of whoever
ruled it.

**A silent failure is worse than a loud one.** A curriculum that is obviously
wrong gets fixed. A curriculum that reports itself sound while a science has
quietly evaporated does not. Most of this bible is written against the second
case.

---

## II. The constitutional order

Four tiers. Each governs the one below it, absolutely, and nothing governs
upward.

| Tier | What it is | Files |
|---|---|---|
| **1 · القرار** The register | The only record of settled decisions. Hand-authored. Changed only by an explicit new ruling. | `00-LOCKED-DECISIONS.md` |
| **2 · البيانات** The allocation | The single machine-readable statement of who is taught what, when. Hand-edited, but only to implement a tier-1 ruling. | `allocation-v11.json` |
| **3 · الأدوات** The instruments | The shared facts, the generators, the verifier. Code, not policy. | `curriculum_data.py` · `verify.py` · the four generators |
| **4 · المولَّد** The generated documents | Produced from tiers 1–3. **Never hand-edited.** Every one carries a banner saying so. | `CLASS-BOOK.md` · `SUBJECT-REGISTER.md` · `CLASS-BY-CLASS-SUBJECT-ALLOCATION.md` · `SUBJECT-LIFECYCLE.md` |

Everything else in this directory — twenty-six of thirty-two markdown files —
is **⚠ مشتقة · derived**: an earlier snapshot, superseded, kept for the record
and for nothing else. A derived document is evidence of what was once thought.
It is never evidence of what is true.

**The order of work, and it has no shortcut:**

```
ruling → register (with its reason, in the change log)
       → allocation-v11.json
       → regenerate
       → verify.py
       → publish
```

Skipping a step is how every one of the eleven losses happened. A ruling
implemented in the allocation but never written into the register survives
until the next rebuild and then dies.

---

## III. The vocabulary

Closed lists. A word outside them is not a synonym; it is an unrecorded
decision wearing a familiar coat.

### The three programmes (L-03)
القرآن وعلومه · **اللغة وعلومها** · الدراسات الإسلامية

Note the second: **اللغة وعلومها**, never «اللغة العربية وعلومها». The longer
form has crept in repeatedly and is wrong.

### The four sections (L-01/02)
التمهيدي (١–٢) · الابتدائي (٣–٦) · الإعدادي (٧–٩) · الثانوي (١٠–١٢)

A section's name belongs to its own classes. **لا يُقحَم اسمُ مرحلةٍ في غيرها**
(L-39) — البحث is the work of الثانوي and has no business in الإعدادي, where
the same ladder is called الإنشاء والتعبير.

### The six instructional forms (L-08)
`مستقل` · `مدمج` · `مضمّن` · `وحدة` · `دوراني` · `مسار`

and with them `شرط` — an assessment category, not a teaching form. **الشرط لا
يحمل درجةً أبدًا.**

A form is not a description of how a lesson feels. It is a binding statement
about a book, a paper, a mark and a transcript section. مدمج earns a named
section with a 40% floor; مضمّن earns no paper at all. **The difference between
them is a difference in a child's result, not in wording** — which is why a
hosted entry with no declared form is a decision taken by a script, and why the
verifier now reports all twenty-five of them.

### Words that are forbidden outright
- **«حصة صغيرة» · «نصف مادة» · «تقريبًا مستقل»** — there is no seventh form.
- **«رواية حفص» as a subject** — a riwāyah describes the muṣḥaf. It is not
  taught (L-33).
- **«الرسم العثماني» as a course** — a chapter of the class-9 tajwīd syllabus.
- **«راسب» on a report to a child** — the scale says «لم يبلغ المستوى بعدُ».
  The word exists for the record, not for the child.

---

## IV. The laws, and the failure each one prevents

Every law below is in the register with a number. They are restated here with
their *reason*, because a rule whose reason is lost is a rule that gets argued
away by the next person with a deadline.

### 1 · لا اسمَ بلا دقيقة (L-07)
No subject appears anywhere without either lessons of its own or a named host.

*Prevents:* the register of a school that teaches twenty-four subjects and
timetables fourteen. A name with no minute is a promise to a parent that no
teacher has been asked to keep.

*Its inverse is equally forbidden, and was found live:* **درجةٌ بلا دقيقة** —
وحدة الفرائض carries 14% of the class-9 certificate paper, and الفرائض is not
taught before class 11.

### 2 · لا يُقدَّم علمٌ على آلته (L-34)
No science is opened before the instrument it depends on is closed.

*Prevents:* البلاغة in term one of class 9 while قطر الندى is unfinished.
A student meeting metaphor before he can parse the sentence carrying it is
being taught a vocabulary, not a science. The same law orders البلاغة itself:
**المعاني ← البيان ← البديع** (L-35).

### 3 · الساعة القرآنية محمية (L-20)
The daily Qur'an hour sits outside the slot ledger and is never drawn upon.

*Prevents:* the one resource every other subject would like to borrow.
**And the protection as originally written was insufficient** — it forbade
taking time *out* of the hour and said nothing about moving a science *into*
it. Six classes house another discipline inside the hour. The verifier now
names them; the register has not yet ruled on them.

### 4 · اللغة آلةُ كل علم (L-37/38)
Arabic is not one subject among the Islamic sciences. It is the instrument of
all of them. At الإعدادي the language must not fall below the Islamic sciences;
at الثانوي it holds a floor of one third.

*Prevents:* the bridge collapse — 61% in class 6, 31% in class 7. The sciences
were eating their own instrument.

*And its corollary:* **اللغة العربية ليست النحو** (L-38). A child who can
parse and cannot speak has not been taught the language. الإنشاء والتعبير
carries the living tongue at ٤–٩ and matures into البحث والخطابة at ١٠–١٢.

### 5 · الترتيب قبل الكثرة (L-09/L-12)
The load rises with the class, and a subject returning after a gap returns
**higher**, never as a repeat.

*Prevents:* the curriculum that looks generous because it lists everything
early, and teaches the same chapter three times under three names.

### 6 · لا يُختلق دليل مفقود (L-26/27/28)
A missing source is recorded as missing. A recovered document is never blended
with a present-day ruling. An inference is never presented as a text.

*Prevents:* the most expensive failure available to this project. A fabricated
source is indistinguishable from a real one six months later, and the school
would be teaching from it. **Where a text does not exist, the document says so
in the same register as everything else** — never in a lighter, apologetic
tone, and never by quietly supplying something plausible.

This is the curriculum's form of the brand bible's rule: **silence over
invention.** The two bibles agree on this word for word, and it is not a
coincidence — it is the same institution's character in two domains.

### 7 · عدٌّ بقاعدة معلنة (L-31)
Books and sciences are counted by one declared rule, stated in the open, and
recomputed — never tallied by hand.

*Prevents:* what was found live. Chapter Five declared its numbers computed and
they had been typed: 12 sciences at ١–٣ against a live 11, 13 at ٧ against 15,
10 books at ٩ against 11. **A number that can be derived must never be typed.**

### 8 · الحقيقةُ تُكتب مرّةً (the instruments' own law)
A fact known in two places will drift. The source map, the name normaliser, the
forms vocabulary, the strand lists and the Qur'an-hour minutes live once, in
`curriculum_data.py`.

*Prevents:* what was found live and is the subtlest failure in the corpus. The
verifier and the generator each held their own copy. They drifted. The verifier
reported a clean run while the published document carried ten
`[RED — لا مصدر مُسجَّل]` markers, and L-19's certificate line vanished while
its check reported sound. **A green check that is checking a different copy is
worse than no check**, because it buys confidence with nothing behind it.

---

## V. Naming, numbering and language

**Arabic is the working language of the corpus.** Subject names, text titles
and instructional forms are written in Arabic. English may gloss a rule; it may
never replace a name. «العروض وعلم القافية» is not "prosody". «البحث والخطابة»
is not "research and oratory". A translated subject name is a different subject
by the time it reaches a scheme of work.

**The target language of الترجمة is not fixed.** Ruled by the Director General,
14 September 2026: it may be English, Hausa, Urdu or Yoruba. The subject is the
skill of carrying meaning into the tongue of the listener, taught by its
principles; the section chooses its tongue. *(L-18 and L-38 still read «إلى
اليوربا» and need editing — see §VIII.)*

**Locked items are `L-nn`** and are cited by number, never paraphrased. A board
may refer a locked item back by its number. **A board may not overrule one.**

**Every generated document carries its banner** — «مولَّدة آليًّا … لا تُحرَّر
باليد» — naming the script that made it and the source it came from. A
generated file without a banner is an invitation to hand-edit it, which is how
the counts drifted apart the first time.

**Every superseded document carries ⚠ مشتقة** at the head. No figure is ever
quoted from a file bearing that mark. The ten reviewers were each held to this
and each confirmed it in writing before reporting.

---

## VI. Tone and register

The curriculum documents are written in the same voice as the school's
policies, and for the same reason: **a document that reads as reviewed and
approved is a stronger claim than any amount of assertion.**

- **Numbers with precision, never superlatives.** «ثلاثةَ عشرَ أسبوعًا» ·
  «٤٠ دقيقة» · «أرضية ٤٠٪». Specificity is the prestige signal. "Rigorous",
  "world-class" and "comprehensive" are the vocabulary of a document that has
  not done the arithmetic.
- **A ruling carries its reason.** The change log records *why*, not only
  *what*. A rule whose reason is unrecorded will be overturned by someone who
  cannot see the failure it prevents — which is exactly how class 12 was
  stripped and had to be restored.
- **Stated limits, not hedges.** «هذا لم يُفحَص» is a sentence this corpus
  uses. «يبدو أنه سليم» is not. The verifier prints its nine unchecked items on
  every run and closes with **«والتسعةُ الباقية تُقرأ ولا تُفحَص — فلا يُقال
  ‹تمّ التحقق› حتى تُقرأ.»** That sentence is the house tone in one line.
- **A contradiction is raised, not resolved.** Where the data clashes with a
  locked item, the instrument reports it and stops. Fixing it would be deciding
  it, and the instruments decide nothing.
- **No praise in review.** The panel's ten briefs each carried the condition:
  no commendation, no summary of what is good. A reviewer's value is the
  finding, and praise is the first thing that dilutes it.

---

## VII. The mechanical guarantee

```
cd docs/curriculum && python3 verify.py
```

Thirty of the thirty-nine locked items are proved mechanically. **Nine are not,
and the script says so every run rather than letting a green exit imply
otherwise** — the forms vocabulary (L-08), a subject returning higher (L-12),
the madhhab rules (L-21/22/23) and the rules of evidence (L-26–L-29). These are
matters of judgement, not arithmetic.

The script distinguishes two things, and the distinction is the point:

- **خرق · a breach** — a locked item is violated. The run **fails**, exit
  non-zero, and nothing is published.
- **تناقض · a contradiction** — the data clashes with a locked item, or a
  load-bearing figure was never declared by anyone. It is **reported and not
  fixed**, because fixing it would be deciding it. It goes to the Director
  General, item by item.

**A green run with contradictions listed is not clearance to publish**, and the
script's last line says so. Every guard in it has been tested by deliberately
breaking the thing it guards and confirming the run fails.

---

## VIII. What does not exist yet — do not fabricate

The brand bible carries this section and so does this one, for the same reason.
Each item below is a real gap. **None may be filled by inference, by a
reviewer, or by a script.** They are the Director General's to close.

| Gap | Why it matters |
|---|---|
| **Nine of the ten competencies have no text** | The graduation certificate is defined as «الكفايات العشر + المناقشة + إثبات الجلوس». Only the tenth (الخدمة والأمانة) has recorded wording, and that is `[RECOVERED]`. Nine are named and unwritten. **This is the most serious gap in the corpus.** |
| **No gate has a failure rule** | Seven gates. Two carry thresholds (بوابة القرآن ٨/١٠ · الثانوية القرآنية). None states what happens to the child who does not pass. بوابة الجسر (٦) has no criteria at all. |
| **الترجمة has no source text, ٧–١٢** | A stated priority (L-18) with no text in the register — and now no fixed target language either. |
| **«كتاب اللغة وعلومها» is unregistered** | البرنامج الأول and الثالث each have a named school-authored core book in the register. البرنامج الثاني's book at ٤–٦ exists in the allocation and nowhere in the text chapters. |
| **٢٩٠ / ٣٤٠ دقيقة** | The weekly size of the protected Qur'an hour. Load-bearing in every hours figure in Chapter Five, and declared in no register and no data file. It was typed into a generator. |
| **Twenty-five hosted entries carry no form** | Each is a mark a child either earns or does not. |
| **The assessment policy predates four locked items** | It was written before L-32, L-34, L-36 and L-39 and has not been notified of any of them. It governs every certificate. |

**Where any of these is needed and absent, the document says so in the same
design language as everything else.** It does not switch to an apologetic
voice, and it does not supply something plausible.

---

## IX. Open decisions for the Director General

Twelve locked items and six contradictions stand referred. They are listed in
full, with the reviewer who raised each, in
`review/BOARD-01-CONSOLIDATED.md` §IV, and the six machine-detected ones print
on every `verify.py` run. They are not restated here, because a decision list
that exists in two places is the drift this bible was written to prevent.

**Nothing touching a locked item is implemented without an explicit ruling,
item by item.**

---

## X. How this bible is amended

This bible is tier 1 material: it is authority, not derivation. It changes the
way the register changes — by an explicit ruling from the Director General,
written down with its reason, and never by a rebuild.

When a rule here is found to have failed — as L-20's protection did, as
Chapter Five's arithmetic did — **the failure is added to §IV with the rule**,
not quietly patched. A standard that hides its own near-misses teaches nothing
to the person who inherits it.

*Extended as decisions are made and as the gaps in §VIII are closed.*
