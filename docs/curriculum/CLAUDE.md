# قفل المنهاج · CURRICULUM LOCK

## Read this before touching anything in `docs/curriculum/`

**`00-LOCKED-DECISIONS.md` is the only source of settled decisions.**
Read it in full before any change to any curriculum file. Not the other
documents — they are derived and may be stale. **The register governs.**

---

## The three rules

**1 · A locked item changes only by an explicit new ruling from the Director
General.** Not by forgetting. Not by rebuilding a document from scratch. Not by
a board's own judgement. A board may refer a locked item back; it may not
overrule one.

**2 · If a change would break a locked item, stop.** Do not make the change and
explain afterwards. Bring the locked item to the Director General and ask,
before editing.

**3 · A new ruling is written into the register FIRST**, in the change log with
its reason, and only then implemented in the derived documents.

> **وما ليس في هذا السجل فليس بقرار.**
> What is not in the register is not a decision.

---

## The failure this exists to prevent

Every document in this directory was at some point rebuilt from whatever was in
front of it. Each time, decisions settled earlier that did not happen to appear
in *that file* were silently dropped, and the Director General had to restate
them. It happened to:

- the **three-programme** structure and the **four sections**
- **two books, then three** — one per programme, for the lower classes
- **G12 carrying the most** — a board overruled it and had to be reversed
- **أصول التفسير · التاريخ والسيرة · الترجمة · مصطلح الحديث** — dropped from the
  matrix during an unrelated rebuild
- **البرنامج الأول's booklist** — never written at all
- **التجويد as an independent science** — the Qur'anic sciences board ruled it
  and the ruling was mislaid; the science was folded back into the memorisation
  hour, leaving a discipline with a matn and no lesson
- **الرسم العثماني and رواية حفص counted as courses** — a chapter of tajwīd and a
  description of the muṣḥaf, carried for months as two subjects on the register
- **البلاغة opened before النحو** — in the first term of class 9, while قطر الندى
  was still unfinished that same year; and **البيان before المعاني**, which is the
  same error one layer down. A science was being taught before its instrument

None of these were disagreements. They were losses. The register is the remedy,
and it only works if it is read first.

---

## Before publishing or reporting anything

```
cd docs/curriculum && python3 verify.py
```

It checks the allocation against the register mechanically and **exits
non-zero** if any locked item is broken. A non-zero exit means the document is
not ready and is not published. Do not read the checks off by eye — that is how
they were missed before.

| | Locked item |
|---|---|
| Twelve classes in four sections | L-01/02 |
| Every subject under one of the three programmes | L-03/04 |
| Lower classes: everything embedded or merged | L-05 |
| Three books minimum, one per programme, classes 1–6 | L-06/31 |
| No name without a lesson or a named host | **L-07** |
| The load rises with the class | L-09 |
| The graduating class carries the most | L-10 |
| Every term slot carries exactly three terms | L-11 |
| The cornerstones never pause | L-13 |
| The hand-weighted subjects keep their weight | L-14/15/16/17 |
| Translation into Yoruba carried, not dropped | L-18 |
| Farāʾiḍ ring-fenced | L-19 |
| The Qur'anic hour untouched | L-20 |
| Every class balances its weekly lessons | L-24/25 |
| Every subject has a named source text | **L-30** |
| Tajwīd independent in classes 4–11, not folded into the hour | **L-32** |
| Rasm ʿUthmānī / riwāyat Ḥafṣ never counted as courses | **L-33** |
| No science opened before its instrument | **L-34** |
| Balāghah runs maʿānī → bayān → badīʿ | **L-35** |

**That is 26 of the 35.** The script prints the other nine every run and does not
claim them. They are matters of judgement, not arithmetic — the forms vocabulary
(L-08), a subject returning higher rather than repeating (L-12), the madhhab
rules (L-21/22/23) and the rules of evidence (L-26–L-29). **A green run is not a
verification until a person has read those nine.** The script says so itself.

If you change the allocation, change **`allocation-v11.json`** and regenerate —
never hand-edit `CLASS-BOOK.md` or `SUBJECT-REGISTER.md`. They are generated
files. Hand-editing them is what let the counts drift apart.

## Working language

Subject names, text titles and instructional forms are written **in Arabic**.
English may gloss a rule, never replace a name. «العروض وعلم القافية» is not
"prosody"; «البحث والخطابة» is not "research and oratory".
