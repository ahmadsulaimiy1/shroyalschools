# قفل المنهاج · CURRICULUM LOCK

## Read this before touching anything in `docs/curriculum/`

> **The standard behind these rules is `CURRICULUM-EDITORIAL-BIBLE.md`** — what
> the corpus is for, the constitutional order, the closed vocabulary, each law
> with the failure it prevents, the house tone, and the list of gaps that must
> never be filled by invention. This file is the enforcement; that one is the
> reasoning. Read it once before your first change, and again whenever a rule
> here looks arbitrary — it will explain which loss it was written against.
>
> Its companion in the `sultan-` repository, `docs/editorial-bible.md`, governs
> the school's brand and visual identity. Neither bible may contradict the other.
>
> **And read Part II of it before you assume this register is supreme.** It is
> not. Under Article 12.1 of the Constitution of SHRS, `00-LOCKED-DECISIONS.md`
> is a **Register** — the bottom tier — beneath Policies, Regulations, Statutes,
> the Governance Charter and the Constitution, all of which live in the
> `sultan-` repository and **outrank it**. Curriculum changes are approved by
> the **Academic Council** (Charter Art. 68(b)), reviewed by the **Curriculum
> Review Panel** (Art. 71), and on ʿaqīdah content are subject to a binding
> **Religious Determination** of the Shariah Council (Art. 80D). «وما ليس في
> هذا السجل فليس بقرار» is true of this corpus. It was never true of the
> Institution.

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
- **التفسير taught from class one** — the meaning given to a child still
  unlocking the letter, before he could read the words. The same fault again
- **Arabic collapsing at the bridge** — 61% of the week in class 6, 31% in
  class 7, while Islamic studies took 53%. And **البحث والخطابة, the priority
  subject, was absent from classes 7, 8 and 9 entirely**, with الترجمة absent
  until class 10. The language is the instrument of every sharʿī science; it
  was being given less time than the sciences that depend on it

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
| Translation carried, not dropped — **the target language is not fixed** | L-18 |
| Farāʾiḍ ring-fenced | L-19 |
| The Qur'anic hour untouched | L-20 |
| Every class balances its weekly lessons | L-24/25 |
| Every subject-grade RESOLVES to a source text | **L-30** |
| Every prescribed book title is one the register carries | **L-30/سند** |
| Chapter Five's counts recompute and match | **L-31/ب٥** |
| Tajwīd independent in classes 4–11, not folded into the hour | **L-32** |
| Rasm ʿUthmānī / riwāyat Ḥafṣ never counted as courses | **L-33** |
| No science opened before its instrument | **L-34** |
| Balāghah runs maʿānī → bayān → badīʿ | **L-35** |
| No tafsīr before class five | **L-36** |
| Arabic ≥ Islamic studies at Ideadi; ≥ one third at Thanawi | **L-37** |
| The living language runs unbroken 4–12, الترجمة 7–12 | **L-38** |
| الإنشاء والتعبير 4–9, البحث والخطابة 10–12 — never swapped | **L-39** |

**That is 30 of the 39**, now with three checks where there was one. The script prints the other nine every run and does not
claim them. They are matters of judgement, not arithmetic — the forms vocabulary
(L-08), a subject returning higher rather than repeating (L-12), the madhhab
rules (L-21/22/23) and the rules of evidence (L-26–L-29). **A green run is not a
verification until a person has read those nine.** The script says so itself.

If you change the allocation, change **`allocation-v11.json`** and regenerate —
never hand-edit `CLASS-BOOK.md` or `SUBJECT-REGISTER.md`. They are generated
files. Hand-editing them is what let the counts drift apart.

**And never add a second copy of a fact.** The source map, the name normaliser,
the forms vocabulary, the strand lists and the Qurʾān-hour minutes live once, in
`curriculum_data.py`, which every script imports. They used to live twice — in
the verifier and in the generator — and the copies drifted. That drift is
precisely what let `verify.py` report a clean run while the published document
carried ten `[RED — لا مصدر مُسجَّل]` markers, and what dropped الفرائض from the
certificate line while its check reported sound. If a fact needs to be known in
two places, it belongs in that module, not in both.

### The script now reports contradictions as well as breaches

A breach fails the run. A **contradiction** is different: the data clashes with a
locked item, or a load-bearing figure was never declared by anyone. The script
prints these under `تناقضاتٌ تُرفَع ولا تُصلَح هنا` and **does not fix them**,
because fixing them would be deciding them. They go to the Director General,
item by item. A green exit with contradictions listed is **not** clearance to
publish, and the script says so on its last line.

## Working language

Subject names, text titles and instructional forms are written **in Arabic**.
English may gloss a rule, never replace a name. «العروض وعلم القافية» is not
"prosody"; «البحث والخطابة» is not "research and oratory".
