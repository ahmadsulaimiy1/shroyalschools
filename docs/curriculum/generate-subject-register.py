# -*- coding: utf-8 -*-
import json,io
import os; SP=os.path.dirname(os.path.abspath(__file__))+'/'
D=json.load(open(SP+'allocation-v11.json'))
PROGS=[('القرآن','البرنامج الأول · القرآن وعلومه'),('اللغة','البرنامج الثاني · اللغة وعلومها'),
       ('الإسلامية','البرنامج الثالث · الدراسات الإسلامية'),('التتويج','خدمة سنة التتويج')]
import curriculum_data as C
clean = C.display
# build: subject -> prog -> {grade: mark}
M={}; P={}
for g in range(1,13):
    c,sl,h=D[str(g)]
    M.setdefault('حفظ القرآن الكريم',{})[g]='◆'; P['حفظ القرآن الكريم']='القرآن'
    for name,prog,n,note in c:
        nm=clean(name)
        if nm.startswith('كتاب اللغة'): nm='اللغة العربية'
        if nm.startswith('كتاب الدراسات'): nm='التربية الإسلامية'
        M.setdefault(nm,{})[g]='●'; P[nm]=prog
    for lab,cap,terms in sl:
        for term,nt,name,prog,note in terms:
            nm=clean(name)
            if nm=='الفرائض التطبيقية': nm='الفرائض'
            M.setdefault(nm,{})[g]='◐'; P.setdefault(nm,prog)
    for name,prog,host,note in h:
        nm=clean(name)
        mark='○' if note.startswith('مدمج') else ('▣' if note.startswith('وحدة') else '·')
        M.setdefault(nm,{})[g]=mark; P.setdefault(nm,prog)
# strands G1-G6
ST={g:['التوحيد','الفقه','الحديث النبوي','السيرة النبوية'] for g in range(1,6)}
ST[6]=['التوحيد','الفقه','الحديث النبوي']
for g,names in ST.items():
    for nm in names:
        M.setdefault(nm,{}).setdefault(g,'▷'); P.setdefault(nm,'الإسلامية')

o=io.StringIO(); w=o.write
w('# سجل المواد · THE SUBJECT REGISTER\n')
w('### كم مادة نُدرِّس · تحت أي برنامج · في أي صف\n\n')
w('> **مولَّد من نفس المصدر الذي وُلِّد منه `CLASS-BOOK.md`. متوافق مع `00-LOCKED-DECISIONS.md`.**\n\n')
w('| الرمز | المعنى | كتاب؟ | ورقة؟ |\n|---|---|---|---|\n')
w('| **◆** | الساعة القرآنية المحمية — خارج الخانات | كتاب القرآن وعلومه | بوابة |\n')
w('| **●** | **مستقل** سنةً كاملة — له خانة | **نعم** | **نعم** |\n')
w('| **◐** | **مستقل** مقررًا فصليًّا — خانة فصلية | كراسة المقررات | **نعم** |\n')
w('| **○** | **مدمج** في مادة شريكة | كتاب الشريك | قسم مسمّى · أرضية ٤٠٪ |\n')
w('| **▣** | **وحدة** — تُقوَّم ولا تدخل المعدل | لا | قسم (ب) |\n')
w('| **·** | **مضمّن** في مضيف مسمّى | لا | داخل المضيف |\n')
w('| **▷** | **مسار** داخل كتاب التربية الإسلامية | لا | ملحق وصفي بلا رقم |\n\n')
cnt={p:0 for p,_ in PROGS}
for nm in M: cnt[P[nm]]+=1
w('| البرنامج | عدد المواد |\n|---|---|\n')
for p,lab in PROGS: w(f'| **{lab}** | **{cnt[p]}** |\n')
w(f'| | **المجموع: {sum(cnt.values())} مادة** |\n\n---\n\n')
for p,lab in PROGS:
    names=[n for n in M if P[n]==p]
    # order by first appearance then breadth
    names.sort(key=lambda n:(min(M[n]),-len(M[n])))
    w(f'## {lab} — {len(names)} مادة\n\n')
    w('| المادة | ١ | ٢ | ٣ | ٤ | ٥ | ٦ | ٧ | ٨ | ٩ | ١٠ | ١١ | ١٢ | العدد · الصفوف |\n')
    w('|---|'+'---|'*13+'\n')
    for n in names:
        cells=''.join('| '+M[n].get(g,' ')+' ' for g in range(1,13))
        gs=sorted(M[n])
        runs=[];st=pv=gs[0]
        for x in gs[1:]:
            if x==pv+1: pv=x
            else: runs.append((st,pv)); st=pv=x
        runs.append((st,pv))
        span='، '.join(str(a) if a==b else f'{a}–{b}' for a,b in runs)
        w(f'| **{n}** {cells}| {len(gs)} · {span} |\n')
    w('\n')
w('---\n\n## عدد العلوم في كل صف\n\n')
w('| الصف | '+' | '.join(str(g) for g in range(1,13))+' |\n|---|'+'---|'*12+'\n')
per=[sum(1 for n in M if g in M[n]) for g in range(1,13)]
w('| **علوم** | '+' | '.join(f'**{x}**' for x in per)+' |\n')
hs=[sum(x[2] for x in D[str(g)][0])+sum(x[1] for x in D[str(g)][1]) for g in range(1,13)]
w('| **خانات** | '+' | '.join(str(x) for x in hs)+' |\n\n')
w('> **الحمل يرتفع مع الصف (L-09)، وصفُّ التخرج يحمل الأكثر (L-10).**\n\n')
w('---\n\n## ما ليس مادة\n\n')
w('| الاسم | ما هو |\n|---|---|\n')
w('| **الرسم العثماني** | بابٌ داخل منهج التجويد في التاسع — **لا مقرر ولا مادة** (L-33) |\n')
w('| **رواية حفص عن عاصم** | وصفُ المصحف الذي نقرأ به (L-23) — **لا مادة تُدرَّس**. وفرشُها بابٌ في ورقة التجويد |\n')
w('| **علوم القرآن** | مباحثُها موزَّعة: أصول التفسير داخل التفسير، والتجويد مادةٌ قائمة |\n')
w('| **المصحف** | أصلٌ لا يُعدّ في الكتب ولا في المواد |\n')
open(''+SP+'SUBJECT-REGISTER.md','w').write(o.getvalue())
print('total',sum(cnt.values()),cnt)
print('per-grade',per)
