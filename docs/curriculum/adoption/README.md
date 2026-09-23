# سجل الاعتماد المؤقت للكتب الدراسية · Temporary Textbook Adoption Register

**SHRS/ACB/TTA-01 · 2026/2027 · للاعتماد — لم يُقرَّها المجلس بعد**

Generated, never hand-edited. `python3 gen-adoption-register.py && python3 topdf-reg.py $PWD/ADOPTION-REGISTER.html $PWD/SHRS-TEMPORARY-TEXTBOOK-ADOPTION-REGISTER.pdf`

| file | what it is |
|---|---|
| `submission.py` | the two lists **exactly as received**, plus the Board's proposed mapping of each line to an existing SHRS subject. The two are kept apart on purpose. |
| `reconcile.py` | tests that mapping against the curriculum register. A mapping naming a subject the class does not carry is **raised, not honoured**. Also finds gaps, host-carried subjects, book burden, one-book-two-functions, and attribution clashes. |
| `gen-adoption-register.py` | the Registrar-facing document. |

## What this register is not

It is a **temporary implementation layer**. It creates no subject, deletes
none, adds no programme, and settles no حصص. The curriculum register
(`../00-LOCKED-DECISIONS.md`) remains the controlling framework, and where the
book list and the framework disagree the disagreement is **recorded as a board
item**, not resolved here.

## The finding the whole thing turns on

The supplied heading «الصف الأول الابتدائي» is the school's **third** class,
not its first — الابتدائي runs 3–6. Three independent tests agree (نور البيان's
three classes, the تيسير النحو/الصرف volume sequence, and الإنشاء والتعبير's
span). Read literally, the same books would open النحو in class three and place
نور البيان in class one twice. **BD-TB-01** puts the reading to the Board.
