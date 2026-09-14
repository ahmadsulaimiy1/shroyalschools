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
| Every class balances its weekly lessons | L-24/25 |
| Every term slot carries exactly three terms | L-11 |
| Every subject under one of the three programmes | L-03/04 |
| Every subject has a named source text | **L-30** |
| The Qur'anic hour untouched | L-20 |
| Tajwīd independent in classes 4–11, not folded into the hour | **L-32** |
| Rasm ʿUthmānī / riwāyat Ḥafṣ never counted as courses | **L-33** |
| Three books minimum, one per programme, classes 1–6 | L-06/31 |
| The graduating class carries the most | L-10 |
| The cornerstones never pause | L-13 |
| No name without a lesson or a named host | L-07 |

If you change the allocation, change **`allocation-v11.json`** and regenerate —
never hand-edit `CLASS-BOOK.md` or `SUBJECT-REGISTER.md`. They are generated
files. Hand-editing them is what let the counts drift apart.

## Working language

Subject names, text titles and instructional forms are written **in Arabic**.
English may gloss a rule, never replace a name. «العروض وعلم القافية» is not
"prosody"; «البحث والخطابة» is not "research and oratory".
