#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""فحص السجل المقفل · Verify the curriculum against 00-LOCKED-DECISIONS.md

Run from docs/curriculum:  python3 verify.py
Exits non-zero if any locked item is violated. Nothing is published on a failure.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'allocation-v11.json'), encoding='utf-8'))
REG = open(os.path.join(HERE, '00-LOCKED-DECISIONS.md'), encoding='utf-8').read()

fails, notes = [], []
def check(item, ok, detail):
    (notes if ok else fails).append(f'{"✓" if ok else "✗"} {item} — {detail}')

def clean(n):
    n = n.replace('*', '').strip()
    if n.startswith('كتاب اللغة'):      return 'اللغة العربية'
    if n.startswith('كتاب الدراسات'):   return 'التربية الإسلامية'
    if n == 'الفرائض التطبيقية':        return 'الفرائض'
    return n

GRADES = [str(g) for g in range(1, 13)]
CEIL   = {g: (13 if int(g) <= 6 else 19) for g in GRADES}

# ── L-24/25 · the week balances in every class ──────────────────────────────
bad = [g for g in GRADES
       if sum(x[2] for x in D[g][0]) + sum(s[1] for s in D[g][1]) != CEIL[g]]
check('L-24/25', not bad, f'كل صف يوازن حصصه — {12 - len(bad)}/12')

# ── L-11 · every term slot carries exactly three terms ──────────────────────
bad = [(g, s[0]) for g in GRADES for s in D[g][1] if sum(t[1] for t in s[2]) != 3]
check('L-11', not bad, f'كل خانة فصلية تستوفي ثلاثة فصول — {bad or "36/36"}')

# ── L-03/04 · every subject under one of the three programmes ───────────────
PROGS = {'القرآن', 'اللغة', 'الإسلامية', 'التتويج'}
bad = set()
subs = {'حفظ القرآن الكريم': 'القرآن', 'التوحيد': 'الإسلامية', 'السيرة النبوية': 'الإسلامية'}
for g in GRADES:
    corner, slots, hosted = D[g]
    for x in corner:                        subs[clean(x[0])] = x[1]; bad |= {x[1]} - PROGS
    for s in slots:
        for t in s[2]:                      subs[clean(t[2])] = t[3]; bad |= {t[3]} - PROGS
    for x in hosted:                        subs[clean(x[0])] = x[1]; bad |= {x[1]} - PROGS
check('L-03/04', not bad, f'كل مادة تحت أحد البرامج — {len(subs)} مادة، ولا واحدة خارجها')

# ── L-30 · every subject has a named source ────────────────────────────────
INDEX = {  # subjects whose texts sit under a combined heading in the register
    'الحديث النبوي': 'الحديث ومصطلحه', 'مصطلح الحديث': 'الحديث ومصطلحه',
    'السيرة النبوية': 'السيرة والتاريخ', 'التاريخ والسيرة': 'السيرة والتاريخ',
}
missing = [s for s in subs if s not in REG and INDEX.get(s, '') not in REG]
check('L-30', not missing, f'لكل مادة مصدر — {missing or "لا مادة بلا مصدر"}')

# ── L-20 · the Qurʾānic hour is never drawn upon ───────────────────────────
bad = [g for g in GRADES
       if any(clean(x[0]) == 'حفظ القرآن الكريم' for x in D[g][0] + D[g][2])]
check('L-20', not bad, 'الساعة القرآنية خارج الخانات في كل صف — 12/12')

# ── L-32 · tajwīd independent 4–11, never folded into the hour there ───────
bad = []
for g in GRADES:
    ind = [x for x in D[g][0] if clean(x[0]) == 'التجويد']
    emb = [x for x in D[g][2] if clean(x[0]) == 'التجويد']
    if 4 <= int(g) <= 11 and not ind:                       bad.append(f'{g}: ليس مستقلًّا')
    if 4 <= int(g) <= 11 and emb:                           bad.append(f'{g}: مضمّن')
check('L-32', not bad, f'التجويد مستقل ٤–١١ — {bad or "8/8"}')

# ── L-33 · these are chapters of tajwīd, never courses ─────────────────────
FORBIDDEN = ['الرسم العثماني', 'أصول رواية حفص', 'رواية حفص', 'علوم القرآن']
bad = [(g, n) for g in GRADES for n in FORBIDDEN
       for x in D[g][0] + D[g][2] if clean(x[0]) == n]
bad += [(g, t[2]) for g in GRADES for s in D[g][1] for t in s[2] if clean(t[2]) in FORBIDDEN]
check('L-33', not bad, f'ليست موادَّ ولا مقررات — {bad or "لا واحد منها مادة"}')

# ── L-31/L-06 · three books minimum, one per programme, in classes 1–6 ─────
def books(g):
    corner, slots, _ = D[g]
    return 1 + len([x for x in corner if clean(x[0]) != 'التجويد']) + (1 if slots else 0)
bad = [g for g in GRADES if int(g) <= 6 and books(g) != 3]
check('L-06/31', not bad, f'ثلاثة كتب في التمهيدي والابتدائي — {bad or "6/6"}')

# ── L-10 · the graduating class carries the most ──────────────────────────
mx = max(GRADES, key=lambda g: (books(g), len(D[g][0])))
check('L-10', mx == '12', f'صف التخرج يحمل الأكثر — {books("12")} كتابًا، وأكثر من كل صف')

# ── L-13 · the cornerstones never pause ───────────────────────────────────
CORNERS = ['النحو', 'اللغة العربية', 'الفقه', 'العقيدة', 'الحديث النبوي', 'التفسير']
bad = []
for s in CORNERS:
    gaps = [g for g in GRADES if int(g) >= 7
            and not any(clean(x[0]) == s for x in D[g][0])]
    if gaps: bad.append((s, gaps))
check('L-13', not bad, f'مواد الأساس لا تنقطع من السابع — {bad or "6/6"}')

# ── L-07 · no name without a lesson or a named host ───────────────────────
bad = [(g, x[0]) for g in GRADES for x in D[g][2] if not x[2].strip()]
check('L-07', not bad, f'لا اسمَ بلا دقيقة ولا مضيف — {bad or "لا واحد"}')

for line in notes + fails: print(line)
print()
if fails:
    print(f'✗ {len(fails)} بندًا مقفلًا مخروقًا. الوثيقة ليست جاهزة ولا تُنشر.')
    sys.exit(1)
print('✓ كل البنود المقفلة سليمة. جاهزة للنشر.')
