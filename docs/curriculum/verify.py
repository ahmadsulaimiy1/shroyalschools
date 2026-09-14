#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""فحص السجل المقفل · Verify the curriculum against 00-LOCKED-DECISIONS.md

Run from docs/curriculum:  python3 verify.py
Exits non-zero if any locked item is violated. Nothing is published on a failure.
"""
import re, sys
import curriculum_data as C
from curriculum_data import D, REG, GRADES, CEIL, clean

fails, notes, contradictions = [], [], []
def check(item, ok, detail):
    (notes if ok else fails).append(f'{"✓" if ok else "✗"} {item} — {detail}')

def contradiction(item, detail):
    """Not a script bug and not mine to settle: a clash between the data and a
    locked item, or a figure nobody declared. Reported, never silently fixed."""
    contradictions.append(f'⚠ {item} — {detail}')

# ── L-24/25 · the week balances in every class ──────────────────────────────
bad = [g for g in GRADES
       if sum(x[2] for x in D[g][0]) + sum(s[1] for s in D[g][1]) != CEIL[g]]
check('L-24/25', not bad, f'كل صف يوازن حصصه — {12 - len(bad)}/12')

# ── L-11 · every term slot carries exactly three terms ──────────────────────
bad = [(g, s[0]) for g in GRADES for s in D[g][1] if sum(t[1] for t in s[2]) != 3]
check('L-11', not bad, f'كل خانة فصلية تستوفي ثلاثة فصول — {bad or "36/36"}')

# ── L-03/04 · every subject under one of the three programmes ───────────────
PROGS = set(C.PROG_IN_DATA)   # three locked + التتويج, which L-03 does not admit
bad = set()
subs = {'حفظ القرآن الكريم': 'القرآن', 'التوحيد': 'الإسلامية', 'السيرة النبوية': 'الإسلامية'}
for g in GRADES:
    corner, slots, hosted = D[g]
    for x in corner:                        subs[clean(x[0])] = x[1]; bad |= {x[1]} - PROGS
    for s in slots:
        for t in s[2]:                      subs[clean(t[2])] = t[3]; bad |= {t[3]} - PROGS
    for x in hosted:                        subs[clean(x[0])] = x[1]; bad |= {x[1]} - PROGS
check('L-03/04', not bad, f'كل مادة تحت أحد البرامج — {len(subs)} مادة، ولا واحدة خارجها')
extra = sorted({p for g in GRADES for _, p, _, _ in D[g][0]} - set(C.PROGRAMMES))
if extra:
    who = sorted({clean(x[0]) for g in GRADES for x in D[g][0] if x[1] in extra})
    contradiction('L-03/04', f'برنامجٌ رابع في البيانات ({" · ".join(extra)}) يحمل '
                  f'{" · ".join(who)} — وL-03 يحصر البرامج في ثلاثة، وL-04 لا يقبل مادة خارجها')

# ── L-30 · every subject-grade resolves to a source the register carries ───
# The old check asked whether a subject NAME appeared anywhere in the register
# text. Nearly every name does, so it passed green while the published document
# printed [RED — لا مصدر مُسجَّل] in ten places. It now calls the SAME src()
# the generator calls, so the check and the document cannot disagree again.
red, flagged = [], []
for sub, gs in C.subject_grades().items():
    for g in gs:
        t = C.src(sub, g)
        if 'RED' in t:                     red.append(f'{sub} ({g})')
        elif 'لا مصدر مُسجَّل' in t:        flagged.append(f'{sub} ({g})')
check('L-30', not red, f'لكل مادة مصدر يُحلّه المولِّد — {red or "لا مادة بلا مصدر"}')
if flagged:
    contradiction('L-30', 'مواضعُ لا نصَّ لها في السجل، مُعلَنةً بسببها لا مستورة: '
                  + ' · '.join(flagged))

# ── L-30/provenance · no prescribed book that the register does not carry ──
# This catches the opposite failure: a title invented in the generator and
# never ruled. «مجلة الأحكام ١–٩٩» was one; the register spells it العدلية.
ghost = [f'{sub} {lo}–{hi}: {b}'
         for sub, ents in C.SRC.items() for lo, hi, t in ents
         for b in C.named_books(t) if b not in REG]
check('L-30/سند', not ghost,
      f'كل كتاب مقرَّر مذكور في السجل — {ghost or str(sum(len(C.named_books(t)) for e in C.SRC.values() for _,_,t in e)) + " عنوانًا، كلها مسندة"}')

# ── L-20 · the Qurʾānic hour is never drawn upon ───────────────────────────
# The old check asked only whether ḥifẓ had left the slot ledger. It never
# asked the question that matters: has another science moved INTO the hour?
bad = [g for g in GRADES
       if any(clean(x[0]) == 'حفظ القرآن الكريم' for x in D[g][0] + D[g][2])]
check('L-20', not bad, 'الساعة القرآنية خارج الخانات في كل صف — 12/12')

inside = [(g, clean(x[0])) for g in GRADES for x in D[g][2]
          if 'الساعة القرآنية' in x[2]]
if inside:
    contradiction('L-20', 'علومٌ تسكن الساعة القرآنية — والحمايةُ تمنع الاقتطاع '
                  'ولا تمنع الإسكان: '
                  + ' · '.join(f'{g}: {n}' for g, n in inside))

# ── L-32 · tajwīd independent 4–11, never folded into the hour there ───────
bad = []
for g in GRADES:
    ind = [x for x in D[g][0] if clean(x[0]) == 'التجويد']
    emb = [x for x in D[g][2] if clean(x[0]) == 'التجويد']
    if 4 <= int(g) <= 11 and not ind:                       bad.append(f'{g}: ليس مستقلًّا')
    if 4 <= int(g) <= 11 and emb:                           bad.append(f'{g}: مضمّن')
check('L-32', not bad, f'التجويد مستقل ٤–١١ — {bad or "8/8"}')

# ── L-33 · these are chapters of tajwīd, never courses ─────────────────────
# L-33 names الرسم العثماني and فرش رواية حفص and nothing else. علوم القرآن
# was in this list by my error, so a unit the register prescribes was banned.
FORBIDDEN = ['الرسم العثماني', 'أصول رواية حفص', 'رواية حفص', 'فرش رواية حفص']
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

# ── L-14/15/16/17 · the subjects the Director General weighted by hand ────
def terms(subject):
    n = 0
    for g in GRADES:
        corner, slots, _ = D[g]
        if any(clean(x[0]) == subject for x in corner): n += 3      # a full year
        for sl in slots:
            for t in sl[2]:
                if clean(t[2]) == subject: n += t[1]
    return n
def grades_present(subject):
    return [int(g) for g in GRADES
            if any(clean(x[0]) == subject for x in D[g][0] + D[g][2])
            or any(clean(t[2]) == subject for sl in D[g][1] for t in sl[2])]

check('L-14', terms('البلاغة') >= 6,       f'البلاغة ستة فصول فأكثر — {terms("البلاغة")} فصلًا')
check('L-15', terms('العروض وعلم القافية') > 1,
      f'العروض لا يُدرَّس في فصل واحد — {terms("العروض وعلم القافية")} فصلًا في {grades_present("العروض وعلم القافية")}')
check('L-16', terms('النقد والآداب') >= 3,
      f'النقد والآداب مادة لها وزنها — {terms("النقد والآداب")} فصلًا في {grades_present("النقد والآداب")}')
adv = [g for g in range(7, 13) if g not in grades_present('الصرف')]
check('L-17', not adv, f'الصرف حاضر في كل صف متقدم — {adv or "6/6"}')

# ── L-01/02 · twelve classes in four sections ─────────────────────────────
SECTIONS = {'التمهيدي': [1, 2], 'الابتدائي': [3, 4, 5, 6],
            'الإعدادي': [7, 8, 9], 'الثانوي': [10, 11, 12]}
flat = [g for gs in SECTIONS.values() for g in gs]
check('L-01/02', len(D) == 12 and sorted(flat) == list(range(1, 13)),
      f'١٢ صفًّا في ٤ أقسام — {" · ".join(f"{k} {len(v)}" for k, v in SECTIONS.items())}')

# ── L-05 · in the lower classes everything is embedded or merged ──────────
bad = []
for g in GRADES:
    if int(g) > 6: continue
    for x in D[g][0]:
        n = clean(x[0])
        if n not in ('اللغة العربية', 'التربية الإسلامية', 'التجويد'):
            bad.append(f'{g}: {n} مستقل')
check('L-05', not bad, f'التمهيدي والابتدائي: كل شيء مدمج أو مضمّن — {bad or "6/6"}')

# ── L-09 · the load rises with the class ──────────────────────────────────
sci = [sum(1 for sub in subs
           if any(clean(x[0]) == sub for x in D[g][0] + D[g][2])
           or any(clean(t[2]) == sub for sl in D[g][1] for t in sl[2]))
       for g in GRADES]
drops = [(i + 1, sci[i - 1], sci[i]) for i in range(1, 12) if sci[i] < sci[i - 1]]
check('L-09', not drops, f'الحمل يرتفع مع الصف — {drops or sci}')

# ── L-18 · translation is carried, not dropped ──────────────────────────
# The target language is NOT fixed: the Director General has ruled it may be
# English, Hausa, Urdu or Yoruba. This checks the subject is present, and says
# nothing about which tongue — the register's own wording still needs editing.
check('L-18', grades_present('الترجمة'),
      f'الترجمة حاضرة — {grades_present("الترجمة")} · واللغةُ الهدفُ غير مسمّاة')
if 'إلى اليوربا' in REG:
    contradiction('L-18/L-38', 'السجل ما زال يكتب «الترجمة إلى اليوربا» في '
                  f'{REG.count("إلى اليوربا")} موضعًا، وقد قُضي بأن اللغة غير مسمّاة')

# ── L-19 · farāʾiḍ is ring-fenced with its own paper ─────────────────────
fg = grades_present('الفرائض')
check('L-19', len(fg) >= 2 and terms('الفرائض') >= 3,
      f'الفرائض بابٌ مُصان — {terms("الفرائض")} فصلًا في {fg}')

# ── L-34 · no science before its instrument ───────────────────────────────
def first(subject):
    hits = []
    for g in GRADES:
        corner, slots, hosted = D[g]
        if any(clean(x[0]) == subject for x in corner):                 hits.append(int(g))
        elif any(clean(t[2]) == subject for sl in slots for t in sl[2]): hits.append(int(g))
    return min(hits) if hits else None

# (science, its instrument, the class the instrument closes in)
LADDER = [('البلاغة',        'النحو الأساس — قطر الندى', 9),
          ('أصول الفقه',     'الفقه',                    7),
          ('مصطلح الحديث',   'الحديث النبوي',            7),
          ('المنطق',         'النضج والعقيدة',          11)]
bad = [f'{sci} يُفتح في {first(sci)} وآلتُه ({tool}) تُختم في {close}'
       for sci, tool, close in LADDER
       if first(sci) is not None and first(sci) <= close]
check('L-34', not bad, f'لا يُقدَّم علمٌ على آلته — {bad or "4/4"}')

# ── L-37 · Arabic is the instrument: parity at JSS, a third at SS ─────────
def share(g):
    corner, slots, _ = D[g]
    T = {'القرآن':0,'اللغة':0,'الإسلامية':0,'التتويج':0}
    for name, p, n, _n in corner:            T[p] += n*3
    for lab, cap, terms in slots:
        for term, nt, name, p, _n in terms:  T[p] += cap*nt
    return T, sum(T.values())

bad = []
for g in GRADES:
    T, tot = share(g)
    if 7 <= int(g) <= 9 and T['اللغة'] < T['الإسلامية']:
        bad.append(f'{g}: لغة {T["اللغة"]} < شرعية {T["الإسلامية"]}')
    if int(g) >= 10 and T['اللغة']*3 < tot:
        bad.append(f'{g}: لغة دون الثلث ({T["اللغة"]}/{tot})')
check('L-37', not bad,
      'الإعدادي تكافؤ · الثانوي أرضية الثلث — ' + (str(bad) if bad else
      ' · '.join(f'{g}:{share(g)[0]["اللغة"]*100//share(g)[1]}%' for g in GRADES if int(g)>=7)))

# ── L-38 · the living language is carried, not only its instruments ───────
ins = grades_present('الإنشاء والتعبير')
bh  = grades_present('البحث والخطابة')
live = sorted(set(ins) | set(bh))
gap = [g for g in range(4, 13) if g not in live]
tr  = [g for g in range(7, 13) if g not in grades_present('الترجمة')]
check('L-38', not gap and not tr,
      f'اللغة الحية متصلة ٤–١٢ — {gap or "9/9"} · الترجمة ٧–١٢ — {tr or "6/6"}')

# ── L-39 · a stage's name is not imported into another stage ──────────────
bad = []
if [g for g in bh if g < 10]:   bad.append(f'البحث في {[g for g in bh if g<10]} — والبحث عملُ الثانوي')
if [g for g in ins if g > 9]:   bad.append(f'الإنشاء في {[g for g in ins if g>9]} — وقد نضج بحثًا')
check('L-39', not bad,
      f'الإنشاء {ins} ثم البحث {bh} — ' + (str(bad) if bad else 'لا إقحام'))

# ── L-36 · no tafsīr before class five ────────────────────────────────────
present=[int(g) for g in GRADES
         if any(clean(x[0])=='التفسير' for x in D[g][0]+D[g][2])
         or any(clean(t[2])=='التفسير' for sl in D[g][1] for t in sl[2])]
early=[g for g in present if g<5]
check('L-36', not early and present and min(present)==5,
      f'لا تفسير قبل الخامس — أوله {min(present) if present else "غائب"}، ومستمرٌّ إلى {max(present) if present else "—"}'
      + (f' · وُجد في {early}' if early else ''))

# ── L-35 · المعاني ← البيان ← البديع ──────────────────────────────────────
def balaghah(g):
    for x in D[g][0]:
        if clean(x[0]) == 'البلاغة': return x[3]
    return ''
order = [('10', 'المعاني'), ('11', 'البيان'), ('12', 'البديع')]
bad = [f'{g}: ليس فيه {br}' for g, br in order if br not in balaghah(g)]
check('L-35', not bad, f'ترتيب البلاغة: المعاني ← البيان ← البديع — {bad or "3/3"}')

# ── L-07 · no name without a lesson or a named host ───────────────────────
bad = [(g, x[0]) for g in GRADES for x in D[g][2] if not x[2].strip()]
check('L-07', not bad, f'لا اسمَ بلا دقيقة ولا مضيف — {bad or "لا واحد"}')

# ── L-08 · every hosted entry must declare one of the six forms ───────────
# The generator falls back to مضمّن when no form is declared. That fallback
# changes a child's mark — مدمج earns a named section with a 40% floor, مضمّن
# earns no paper at all — so a silent default is a decision taken by a script.
noform = [(g, clean(x[0]), clean(x[2]))
          for g in GRADES for x in D[g][2]
          if not any(x[3].strip().startswith(f) for f in C.FORMS)]
if noform:
    contradiction('L-08', f'{len(noform)} مدخلًا مستضافًا بلا صيغة مصرَّحة، '
                  'والمولِّد يفترض «مضمّن» — وهو فرقٌ في درجة الطالب لا في التحرير: '
                  + ' · '.join(f'{g}:{n}⊂{h}' for g, n, h in noform[:6])
                  + (f' … وسائرها في الوثيقة المولَّدة' if len(noform) > 6 else ''))

# ── الساعة القرآنية · the figures nobody declared ─────────────────────────
if not C.QURAN_HOUR_DECLARED:
    lo, up = C.QURAN_HOUR['lower'], C.QURAN_HOUR['upper']
    if str(lo) not in REG and str(up) not in REG:
        contradiction('L-20/L-25', f'مقدار الساعة القرآنية ({lo} و{up} دقيقة أسبوعيًّا) '
                      'ليس في السجل ولا في بيانات التوزيع — كان مكتوبًا في المولِّد وحده، '
                      'وهو الآن في موضع واحد ينتظر قرارًا يُدرجه في السجل')

# ── L-31 · Chapter Five is arithmetic, so it is recomputed and COMPARED ────
# The chapter declares its numbers computed from L-31. They were typed, and had
# gone stale: 12 sciences at G1–3 against a live 11, 13 at G7 against 15, and
# 10 books at G9 against 11. A number derived by a declared rule is now proved
# against the register on every run, so it can never drift again.
AR = '٠١٢٣٤٥٦٧٨٩'
def ar(n): return ''.join(AR[int(c)] for c in str(n))

written = {}
for line in REG.split('\n'):
    m = re.match(r'^\|\s*([٠-٩]+)\s*\|\s*([٠-٩]+)\s*\|\s*\*\*([٠-٩]+)\*\*'
                 r'\s*\+\s*المصحف\s*\|\s*([٠-٩]+)\s*\|\s*([^|]+)\|', line.strip())
    if m:
        g = str(int(''.join(str(AR.index(c)) for c in m.group(1))))
        written[g] = (m.group(2), m.group(3), m.group(4), m.group(5).strip())

bad = []
for g in GRADES:
    mins = CEIL[g] * 40 * 39 + C.quran_minutes(g) * 39
    h, mm = divmod(mins, 60)
    want = (ar(CEIL[g]), ar(C.books(g)), ar(len(C.sciences(g))),
            f'{ar(h)} س' + (f' {ar(mm)} د' if mm else ''))
    got = written.get(g)
    if got is None:
        bad.append(f'{g}: لا سطر له في الباب الخامس')
    elif got != want:
        bad.append(f'{g}: مكتوب {got} والمحسوب {want}')
check('L-31/ب٥', not bad,
      f'الباب الخامس يطابق الحساب — {bad or str(len(written)) + "/12 سطرًا، حصصًا وكتبًا وعلومًا وساعات"}')

# Locked items no script can judge — they are read by a person, not asserted here.
BY_HAND = {
    'L-08': 'الصيغ وحدها: مستقل · مدمج · مضمّن · وحدة · دوراني · مسار',
    'L-12': 'إن عادت المادة بعد انقطاع عادت أعلى، لا تكرارًا',
    'L-21': 'مذهب أهل السنة بلا التزام مذهب واحد — يُقاس بمِعيار عدم الحصر',
    'L-22': 'يجوز أن يختلف الإطار من باب إلى باب',
    'L-23': 'الرواية حفص عن عاصم · المصحف مطبعة الملك فهد',
    'L-26': 'لا يُختلق دليل مفقود',
    'L-27': 'لا يُخلط المستردّ بقرار المجلس الحالي',
    'L-28': 'لا يُقدَّم استنتاج على أنه نصٌّ مستردّ',
    'L-29': 'لا تُستنبط العقيدة ولا المذهب من قوائم الكتب',
}
COVERED = {'L-01','L-02','L-03','L-04','L-05','L-06','L-07','L-09','L-10','L-11',
           'L-13','L-14','L-15','L-16','L-17','L-18','L-19','L-20','L-24','L-25',
           'L-30','L-31','L-32','L-33','L-34','L-35','L-36','L-37','L-38','L-39'}

for line in notes + fails: print(line)
print()
if contradictions:
    print('── تناقضاتٌ تُرفَع ولا تُصلَح هنا ' + '─'*34)
    for line in contradictions: print(line)
    print('  هذه ليست أخطاءَ برمجة. كلُّ واحدٍ منها يصطدم ببندٍ مقفل أو برقمٍ لم '
          'يُعلنه أحد،\n  فلا يُغيَّر إلا بقرار صريح من المدير العام.')
    print()
print(f'مفحوص آليًّا: {len(COVERED)} بندًا من ٣٩.')
print(f'لا يفحصه إلا قارئ ({len(BY_HAND)} بندًا): ' + ' · '.join(sorted(BY_HAND)))
for k in sorted(BY_HAND): print(f'    {k} — {BY_HAND[k]}')
print()
if fails:
    print(f'✗ {len(fails)} بندًا مقفلًا مخروقًا. الوثيقة ليست جاهزة ولا تُنشر.')
    sys.exit(1)
print(f'✓ البنود الـ{len(COVERED)} المفحوصة آليًّا سليمة.')
print('  والتسعةُ الباقية تُقرأ ولا تُفحَص — فلا يُقال «تمّ التحقق» حتى تُقرأ.')
if contradictions:
    print(f'  ومع ذلك: {len(contradictions)} تناقضًا مرفوعًا أعلاه ينتظر قرارًا. '
          'السلامةُ الآلية ليست إجازةَ نشر.')
