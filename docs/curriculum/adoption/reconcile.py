# -*- coding: utf-8 -*-
"""THE BOARD'S RECONCILIATION — checked against the register, not asserted.

The mapping in submission.py is judgement. This is where it is TESTED:
every mapped subject must exist in the class the book is proposed for,
under the register's own treatment table. A mapping that names a subject
the class does not carry is not quietly honoured — it is raised.

It also finds what a book list cannot tell you by itself:
  · subjects the class carries for which NO book was submitted;
  · books whose proposed subject the class does not carry;
  · lower classes given more separate books than the architecture allows;
  · the same book serving two curricular functions;
  · titles and authors that disagree between the two submissions.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from submission import CLASSES, SUBMISSION                       # noqa: E402

CUR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CUR)      # the shared curriculum_data module lives there
_src = open(os.path.join(CUR, 'gen-teacher-guide.py'), encoding='utf-8').read()
_ns = {'__file__': os.path.join(CUR, 'gen-teacher-guide.py')}
exec(compile(_src.replace("\nif __name__", "\nif False and __name__"), 'gtg', 'exec'), _ns)
T, PROG_OF, SUBS_OF, PROGS = _ns['T'], _ns['PROG_OF'], _ns['SUBS_OF'], _ns['PROGS']

SECTION = {**{g: 'التمهيدي' for g in (1, 2)}, **{g: 'الابتدائي' for g in (3, 4, 5, 6)},
           **{g: 'الإعدادي' for g in (7, 8, 9)}, **{g: 'الثانوي' for g in (10, 11, 12)}}

DEC = {'ind': 'معتمد مؤقتًا — مادة مستقلة',
       'emb': 'معتمد مؤقتًا — داخل مضيفه',
       'split': 'معتمد مؤقتًا — كتابٌ لمسارين',
       'ask': 'قرار المجلس مطلوب'}


def rows():
    """Every submitted line, placed and judged."""
    out = []
    for div, head, g, copies in CLASSES:
        for supplied, book, shrs in SUBMISSION[(div, g)]:
            if shrs and '+' in shrs:                      # one book, two strands
                parts = shrs.split('+')
                ok = all(p in T[g] for p in parts)
                form = ' · '.join(T[g][p][0] or '—' for p in parts) if ok else '—'
                out.append(dict(div=div, head=head, g=g, copies=copies, supplied=supplied,
                                book=book, shrs=' + '.join(parts), prog=PROG_OF.get(parts[0], '—'),
                                form=form, dec=DEC['split'] if ok else DEC['ask'],
                                note='' if ok else 'المادة غير قائمة في هذا الصف'))
                continue
            if shrs is None:
                out.append(dict(div=div, head=head, g=g, copies=copies, supplied=supplied,
                                book=book, shrs='—', prog='—', form='—', dec=DEC['ask'],
                                note='لا تقابله مادةٌ في السجل لهذا الصف'))
                continue
            if shrs not in T[g]:
                out.append(dict(div=div, head=head, g=g, copies=copies, supplied=supplied,
                                book=book, shrs=shrs, prog=PROG_OF.get(shrs, '—'), form='—',
                                dec=DEC['ask'],
                                note=f'«{shrs}» لا تُدرَّس في الصف {g} بحسب السجل'))
                continue
            form, host = T[g][shrs][0], T[g][shrs][1]
            out.append(dict(div=div, head=head, g=g, copies=copies, supplied=supplied,
                            book=book, shrs=shrs, prog=PROG_OF[shrs], form=form or '—',
                            dec=DEC['ind'] if form == 'مستقل' else DEC['emb'],
                            note=('داخل: ' + host) if host else ''))
    return out


def gaps(rs):
    """Subjects a class carries for which no book was submitted.

    A first version called every one of these a gap and produced 37, most of
    them false: الخط والإملاء is مدمج inside اللغة العربية, which HAS a book,
    so the child is not without a text — the host carries it. The architecture
    says so explicitly. A gap is only real when the subject stands alone, or
    when its host has no book either. The Qur'anic hour is not a book and is
    never counted as a missing one.
    """
    have = {}
    for r in rs:
        for s_ in r['shrs'].split(' + '):
            have.setdefault((r['div'], r['g']), set()).add(s_.strip())
    real, carried = [], []
    for div, head, g, copies in CLASSES:
        got = have.get((div, g), set())
        for sub in T[g]:
            if sub in got:
                continue
            form, host = T[g][sub][0] or '—', T[g][sub][1] or ''
            rec = dict(div=div, head=head, g=g, sub=sub, prog=PROG_OF.get(sub, '—'),
                       form=form, host=host)
            if host and host in got:
                rec['by'] = host
                carried.append(rec)
            elif host == 'الساعة القرآنية':
                rec['by'] = 'الساعة القرآنية — لا كتابَ لها'
                carried.append(rec)
            elif host == 'كتاب الدراسات الإسلامية':
                rec['by'] = 'كتابُ البرنامج — وهو نفسُه غيرُ مقدَّم'
                real.append(rec)
            else:
                real.append(rec)
    return real, carried


def burden(rs):
    """L-05/L-06: the lower classes take ONE book per programme, not one per
    named science. Counting the separate volumes a child would carry."""
    out = []
    for div, head, g, copies in CLASSES:
        if g > 6:
            continue
        per = {}
        for r in rs:
            if r['div'] == div and r['g'] == g and r['prog'] != '—':
                per.setdefault(r['prog'], set()).add(r['book'])
        for prog, books in per.items():
            if len(books) > 1:
                out.append(dict(div=div, head=head, g=g, prog=prog,
                                n=len(books), books=sorted(books)))
    return out


def doubles(rs):
    """One book carrying two different curricular functions."""
    seen = {}
    for r in rs:
        seen.setdefault(r['book'], set()).add(r['shrs'])
    return {b: sorted(v) for b, v in seen.items() if len(v) > 1}


def clashes():
    """Where the two submissions disagree about the SAME work.

    A first version split on the dash and called «ج١ / ج٢ / ج٣» a
    disagreement, which is a volume sequence, not a contradiction. It now
    compares author against author for one and the same title.
    """
    import re as _re
    VOL = _re.compile(r'[،,]?\s*(?:ج\s*[١٢٣٤]|الجزء\s+\S+)\s*$')

    def split(b):
        t, _, a = b.partition('—')
        # the volume rides on whichever side it was typed; it is a sequence,
        # not a disagreement, and an earlier version reported all of them
        return VOL.sub('', t.strip()).strip(), VOL.sub('', a.strip()).strip()
    acc = {}
    for div, head, g, copies in CLASSES:
        for supplied, book, shrs in SUBMISSION[(div, g)]:
            t, a = split(book)
            acc.setdefault(t, {}).setdefault(a, set()).add(f'{div} ص{g}')
    out = {}
    for t, by in acc.items():
        named = {a: w for a, w in by.items() if a}
        if len(named) > 1 or (len(named) == 1 and '' in by):
            out[t] = {a or '«بلا نسبة»': sorted(w) for a, w in by.items()}
    return out


if __name__ == '__main__':
    rs = rows()
    print(f'lines submitted: {len(rs)}')
    for d in DEC.values():
        print(f'  {d}: {sum(1 for r in rs if r["dec"] == d)}')
    real, carried = gaps(rs)
    print(f'\nREAL GAPS — no book, and no host book either: {len(real)}')
    for x in real:
        print(f'   {x["div"]:<8} ص{x["g"]:<2} {x["sub"]:<24} {x["form"]:<8} {x["host"]}')
    print(f'\nCARRIED BY A HOST THAT HAS A BOOK (not a gap): {len(carried)}')
    print('\nBOOK BURDEN in classes 1–6 (architecture wants one book per programme):')
    for x in burden(rs):
        print(f'   {x["div"]:<8} ص{x["g"]} {x["prog"]:<18} {x["n"]} كتب')
    print('\nONE BOOK, TWO FUNCTIONS:')
    for b, v in doubles(rs).items():
        print(f'   {b}  →  {v}')
    print('\nTHE TWO SUBMISSIONS DISAGREE:')
    for k, v in clashes().items():
        print(f'   {k}:')
        for x in v: print(f'       {x}')
