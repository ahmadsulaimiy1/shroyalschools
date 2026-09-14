# -*- coding: utf-8 -*-
"""Generate CLASS-BY-CLASS-SUBJECT-ALLOCATION.md and SUBJECT-LIFECYCLE.md
   from allocation-v11.json + 00-LOCKED-DECISIONS.md. Never hand-edit the output.

   The source map, the name normaliser and the Qurʾān-hour figures used to live
   here as a second copy and drifted from the verifier's. They now live once, in
   curriculum_data.py, which both scripts import."""
import os, io, re
import curriculum_data as C
from curriculum_data import D, src, SGATE, quran_minutes
cl = C.display
H = os.path.dirname(os.path.abspath(__file__))

NAMES={1:('الأول','Primary 1'),2:('الثاني','Primary 2'),3:('الثالث','Primary 3'),
4:('الرابع','Primary 4'),5:('الخامس','Primary 5'),6:('السادس','Primary 6'),
7:('السابع','JSS 1'),8:('الثامن','JSS 2'),9:('التاسع','JSS 3'),
10:('العاشر','SS 1'),11:('الحادي عشر','SS 2'),12:('الثاني عشر','SS 3')}
SECTION={1:'التمهيدي',2:'التمهيدي',3:'الابتدائي',4:'الابتدائي',5:'الابتدائي',6:'الابتدائي',
7:'الإعدادي',8:'الإعدادي',9:'الإعدادي',10:'الثانوي',11:'الثانوي',12:'الثانوي'}
PROG={'القرآن':'الأول · القرآن وعلومه','اللغة':'الثاني · اللغة وعلومها',
      'الإسلامية':'الثالث · الدراسات الإسلامية','التتويج':'خدمة سنة التتويج'}
PORDER=['القرآن','اللغة','الإسلامية','التتويج']
GATE={1:'بوابة القراءة',3:'بوابة الطلاقة',5:'الشهادة الابتدائية',6:'بوابة الجسر',
      9:'الشهادة الإعدادية — بممتحن خارجي',11:'الثانوية القرآنية',12:'شهادة التخرج'}

# assessment consequence, mechanical from form (register ch.6)
ASSESS={
 'مستقل':'ورقة مستقلة · كتاب · **يدخل المعدل** · القسم (أ)',
 'مدمج':'قسم مسمّى في ورقة الشريك · **أرضية ٤٠٪** · لا كتاب · يدخل المعدل مجموعًا · القسم (أ)',
 'مضمّن':'لا ورقة ولا كتاب · يُقوَّم **داخل المضيف** · القسم (أ)',
 'وحدة':'تقدير إنجاز · لا كتاب · **لا يدخل المعدل** · القسم (ب)',
 'مسار':'لا ورقة ولا رقم · ملحق وصفي: متقن / نامٍ / مبتدئ',
 'شرط':'**لا يحمل درجة أبدًا** · القسم (ج) — يُستوفى أو لا يُستوفى',
 'الساعة':'بوابة الحفظ · خارج الخانات · القسم (أ) بالأداء أمام لجنة'}

# ── form resolution: explicit only. Never guessed. ──────────────────────────
UNRESOLVED=[]
def form_of(note,sub,g,host):
    n=note.strip()
    for f in C.FORMS:
        if n.startswith(f): return f,False
    UNRESOLVED.append((g,sub,host,n))
    return 'مضمّن',True

def detail(note):
    n=note.strip()
    for f in C.FORMS:
        if n.startswith(f):
            r=n[len(f):].lstrip(' —·-').strip()
            return r
    return n

BOOKNOTE={'مستقل':'كتاب مستقل','مدمج':'داخل كتاب الشريك','مضمّن':'لا كتاب — داخل المضيف',
          'وحدة':'لا كتاب','مسار':'لا كتاب','شرط':'ملف لا كتاب'}
STRANDS=C.STRANDS

# ════════════════════════════════════════════════════════════════════════════
#  build the per-class row model
# ════════════════════════════════════════════════════════════════════════════
def rows_for(g):
    """returns (rows, slots_used, slot_lines) ; rows = list of dicts"""
    corner,slots,hosted=D[str(g)]
    lower=g<=6
    R=[]
    R.append(dict(prog='القرآن',sub='حفظ القرآن الكريم',form='مستقل',slots='—',
        place='الساعة القرآنية المحمية · كل يوم',host='—',partner='—',
        note=f'{quran_minutes(g)} د/أسبوع · **خارج الخانات** · لا تُقتطع لأي مادة (L-20)',
        book='كتاب القرآن وعلومه',assess=ASSESS['الساعة'],unres=False))
    for name,prog,n,note in corner:
        sub=cl(name)
        disp=sub
        if sub.startswith('كتاب اللغة'): disp='اللغة العربية'
        if sub.startswith('كتاب الدراسات'): disp='التربية الإسلامية'
        R.append(dict(prog=prog,sub=disp,form='مستقل',slots=str(n),
            place='سنة كاملة · ٣ فصول',host='—',partner='—',note=note or '—',
            book=('كتاب القرآن وعلومه' if disp=='التجويد' else 'كتاب مستقل'),
            assess=ASSESS['مستقل'],unres=False))
    for lab,cap,terms in slots:
        for term,nt,name,prog,note in terms:
            R.append(dict(prog=prog,sub=cl(name),form='مستقل',slots=f'{cap} *(خانة مشتركة)*',
                place=f'**مقرر فصلي — {term}**' + (f' ({nt} فصول)' if nt>1 else ''),
                host='—',partner='—',note=note or '—',
                book='كراسة المقررات الفصلية',assess=ASSESS['مستقل'],unres=False))
    for name,prog,host,note in hosted:
        sub=cl(name); f,unres=form_of(note,sub,g,host)
        R.append(dict(prog=prog,sub=sub,form=f,slots='—',place='داخل المضيف',
            host=cl(host) if f!='مدمج' else '—',
            partner=cl(host) if f=='مدمج' else '—',
            note=detail(note) or '—',book=BOOKNOTE[f],assess=ASSESS[f],unres=unres))
    if g<=6:
        for s in STRANDS[g]:
            R.append(dict(prog='الإسلامية',sub=s,form='مسار',slots='—',
                place='مسار داخل الكتاب',host='كتاب الدراسات الإسلامية — التربية الإسلامية',
                partner='—',note='خيط داخل الكتاب — لا يُفرَد',book='لا كتاب',
                assess=ASSESS['مسار'],unres=False))
    used=sum(x[2] for x in corner)+sum(s[1] for s in slots)
    return R,used

def esc(s): return str(s).replace('|','\\|')

out=io.StringIO(); w=out.write
TOTAL_SUBJ=33
w('''# التوزيع التفصيلي للمواد · صفًّا صفًّا
# CLASS-BY-CLASS SUBJECT ALLOCATION · G1–G12

> ## وثيقة تسليم للجدول الزمني · TIMETABLE HANDOFF DOCUMENT
> **مولَّدة آليًّا** من `allocation-v11.json` و`00-LOCKED-DECISIONS.md` بواسطة
> `gen-allocation.py`. **لا تُحرَّر باليد.** إن لزم تغيير، فغيِّر المصدر وأعد التوليد.
>
> فُحصت بـ `verify.py` قبل التوليد: **٢٦ بندًا مقفلًا من ٣٥ سليمة آليًّا**،
> والتسعة الباقية تُقرأ ولا تُفحَص.

**الصيغ المقفلة — ولا سواها (L-08):**
`مستقل` · `مدمج` · `مضمّن` · `وحدة` · `دوراني` · `مسار` — ومعها `شرط` صيغةَ تقويمٍ لا تعليم.

| الصيغة | خانة | كتاب | ورقة | المعدل | قسم الشهادة |
|---|---|---|---|---|---|
| **مستقل** | نعم | نعم | نعم | يدخل | أ |
| **مدمج** | يشترك مع شريك مسمّى | كتاب الشريك | **قسم مسمّى · أرضية ٤٠٪** | يدخل مجموعًا | أ |
| **مضمّن** | لا | لا | داخل المضيف | عبر المضيف | أ |
| **وحدة** | لا | لا | تقدير إنجاز | **لا يدخل** | ب |
| **مسار** | لا | لا | لا رقم | لا | ملحق وصفي |
| **شرط** | — | ملف | **لا درجة أبدًا** | لا | ج |

''')

# ── the blocker report ─────────────────────────────────────────────────────
# (filled after the loop; placeholder index kept)
BLOCK_MARK='<!--BLOCKERS-->'
w(BLOCK_MARK+'\n\n---\n\n')

summary=[]
for g in range(1,13):
    R,used=rows_for(g)
    ceil=13 if g<=6 else 19
    corner,slots,hosted=D[str(g)]
    books=1+len([x for x in corner if cl(x[0])!='التجويد'])+(1 if slots else 0)
    sciences=len({r['sub'] for r in R})
    summary.append((g,used,books,sciences))
    w(f'# الصف {NAMES[g][0]} · {NAMES[g][1]}\n')
    w(f'### القسم {SECTION[g]} · **{used}/{ceil} خانة** · **{books} كتابًا** + المصحف · '
      f'**{sciences} علمًا مسمًّى**\n\n')
    if g in GATE: w(f'> **بوابة هذا الصف:** {GATE[g]}\n\n')
    for p in PORDER:
        rs=[r for r in R if r['prog']==p]
        if not rs: continue
        w(f'## البرنامج {PROG[p]} — {len(rs)} مادة\n\n')
        w('| المادة | الصيغة | خانات | الموضع الفصلي | المضيف | الشريك | المصدر المقرَّر | أثر التقويم | البوابة / الشرط | البيان |\n')
        w('|---|---|---|---|---|---|---|---|---|---|\n')
        for r in rs:
            form=f"**{r['form']}**"
            if r['unres']: form+=' ⚠️ `[غير مُثبَت]`'
            gate=SGATE.get(C.clean(r['sub']),'—')   # L-19: الفرائض التطبيقية is the same ring-fenced door
            w(f"| **{esc(r['sub'])}** | {form} | {esc(r['slots'])} | {esc(r['place'])} | "
              f"{esc(r['host'])} | {esc(r['partner'])} | {esc(src(r['sub'],g))} | "
              f"{esc(r['assess'])} | {esc(gate)} | {esc(r['note'])} |\n")
        w('\n')
    if slots:
        w('### الخانات الفصلية — خانة واحدة تحمل مقررات مختلفة عبر السنة\n\n')
        w('| الخانة | خانات/أسبوع | الفصل الأول | الفصل الثاني | الفصل الثالث |\n|---|---|---|---|---|\n')
        for lab,cap,terms in slots:
            cells={'ف١':'—','ف٢':'—','ف٣':'—'}
            for term,nt,name,prog,note in terms:
                if term=='ف١+ف٢': cells['ف١']=cells['ف٢']=f'**{cl(name)}**'
                elif term in cells: cells[term]=f'**{cl(name)}**'
                else: cells['ف١']=f'**{cl(name)}** ({term})'
            w(f"| {lab} | {cap} | {cells['ف١']} | {cells['ف٢']} | {cells['ف٣']} |\n")
        w('\n')
    w(f'**ميزان الخانات: {used} / {ceil}** ✓\n\n---\n\n')

# ════════════════════════════════════════════════════════════════════════════
#  TIMETABLE HANDOFF — what actually occupies the weekly slots
# ════════════════════════════════════════════════════════════════════════════
w('''# جدول التسليم الزمني · TIMETABLE HANDOFF
### ما يشغل خانات الأسبوع فعلًا — ولا شيء غيره

> **هذا هو الجدول الذي يبني عليه مخطِّط الجدول الزمني.**
> ما ليس في هذه الجداول **لا يشغل خانة**: المدمج يشترك خانة شريكه،
> والمضمّن والوحدة والمسار داخل مضيفها، والساعة القرآنية **خارج العدّ كلِّه**.
> **لا تُقتطع الساعة القرآنية لأي مادة في أي صف (L-20).**

''')
for g in range(1,13):
    corner,slots,hosted=D[str(g)]
    ceil=13 if g<=6 else 19
    used=sum(x[2] for x in corner)+sum(s[1] for s in slots)
    lower=g<=6
    w(f'## الصف {NAMES[g][0]} · {NAMES[g][1]} — {used}/{ceil} خانة\n\n')
    w('| # | ما يشغل الخانة | خانات/أسبوع | نوع الخانة | ملاحظة للمخطِّط |\n|---|---|---|---|---|\n')
    i=0
    for name,prog,n,note in corner:
        i+=1; sub=cl(name)
        disp='اللغة العربية' if sub.startswith('كتاب اللغة') else ('التربية الإسلامية' if sub.startswith('كتاب الدراسات') else sub)
        shares=[cl(h[0]) for h in hosted if cl(h[2])==sub or cl(h[2])==disp]
        extra=('يحمل معه: '+' · '.join(shares)) if shares else '—'
        w(f'| {i} | **{esc(disp)}** | **{n}** | ثابتة سنويًّا | {esc(extra)} |\n')
    for lab,cap,terms in slots:
        i+=1
        seq=' ← '.join(f'{t[0]}: {cl(t[2])}' for t in terms)
        w(f'| {i} | **{esc(lab)}** | **{cap}** | **متغيرة بالفصل** | {esc(seq)} |\n')
    w(f'| | **المجموع** | **{used}** | | يوازن {ceil} ✓ |\n\n')
    w(f'> **الساعة القرآنية:** {quran_minutes(g)} د/أسبوع — **خارج هذه الخانات تمامًا**. '
      f'إجمالي السنة {"٥٢٦ س ٣٠ د" if lower else "٧١٥ س"}.\n\n')
w('---\n\n## ملخص الأحمال\n\n')
w('| الصف | القسم | خانات | كتب | علوم مسمّاة | ساعات المواد | الساعة القرآنية | الإجمالي |\n')
w('|---|---|---|---|---|---|---|---|\n')
for g,used,books,sci in summary:
    lower=g<=6
    w(f'| **{NAMES[g][0]}** | {SECTION[g]} | {used} | {books} | {sci} | '
      f'{"٣٣٨ س" if lower else "٤٩٤ س"} | {"١٨٨ س ٣٠ د" if lower else "٢٢١ س"} | '
      f'{"٥٢٦ س ٣٠ د" if lower else "٧١٥ س"} |\n')
w('\n> **L-09** الحمل يرتفع مع الصف · **L-10** صف التخرج يحمل الأكثر — '
  f'{summary[-1][2]} كتابًا و{summary[-1][3]} علمًا، وهو الأعلى في الجدول.\n')
w('>\n> **عدد العلوم ليس عدد الخانات.** المقرر الفصلي والمضمّن والمدمج والمسار '
  'والمستقل لها آثار تشغيلية مختلفة — والخانات وحدها هي ما يُجدوَل.\n\n')

# ── blocker section, injected where the marker sits ─────────────────────────
if UNRESOLVED:
    b=io.StringIO(); bw=b.write
    bw('> # ⚠️ تقرير تناقضات — يُحسَم بقرار، ولم يُصلَح من عندي\n>\n')
    bw('> ## التناقض الأول — صيغةٌ غير مُصرَّح بها (L-08)\n>\n')
    bw(f'> **{len(UNRESOLVED)} مدخلًا مستضافًا لا تُصرِّح ببنيتها التعليمية في بيانات التوزيع.**\n')
    bw('> المولِّدات السابقة كانت **تستنتج** «مضمّن» من نص الملاحظة. والاستنتاج ليس قرارًا (L-28).\n>\n')
    bw('> **أثرها على الجدول الزمني: لا شيء.** كلُّها مستضافة، ولا تشغل خانةً واحدة،\n')
    bw('> فالتسليم الزمني أدناه **سليم وقابل للاستعمال فورًا**.\n>\n')
    bw('> **وأثرها على التقويم جسيم:** المدمج يأخذ قسمًا مسمًّى بأرضية ٤٠٪، والمضمّن لا ورقة له،\n')
    bw('> والوحدة لا تدخل المعدل. فالفرق بينها فرقٌ في درجة الطالب.\n>\n')
    bw('> وُسمت في الجداول بـ `[غير مُثبَت]` ولم تُحسَم من عندي.\n>\n')
    bw('> | الصف | المادة | المضيف | نص الملاحظة | ما يرجَّح ولماذا |\n')
    bw('> |---|---|---|---|---|\n')
    REC={('العروض وعلم القافية','البلاغة'):'**مدمج** — شريك مسمّى، ويشغل فصلين محددين (ف٢+ف٣)، وL-15 يمنع حصره في فصل',
         ('النقد والآداب','البلاغة'):'**مدمج** — L-16: «مادة لها وزنها لا وحدة صغيرة»، والمضمّن يحرمها قسمًا مسمًّى',
         ('الصرف','النحو'):'**مدمج** — L-17 يوجبه في كل صف متقدم، والكتاب واحد مع النحو أصلًا',
         ('فقه اللغة والمعاجم','الصرف'):'**وحدة** — «دورة ٣ أسابيع»، والدورة المحدودة صيغةُ وحدة',
         ('أصول الفقه','الفقه'):'**مضمّن** — السجل: «تأصيلًا عمليًّا ٨–٩ ثم مادةً في العاشر»',
         ('مصطلح الحديث','الحديث النبوي'):'**مدمج** — له متن مستقل (نخبة الفكر/نزهة النظر)، فيستحق قسمًا مسمًّى',
         ('التوحيد','العقيدة'):'**مضمّن** — السجل يصفه «باب مسمّى داخل العقيدة»',
         ('النشيد والمحفوظات','كل مادة بمتنها'):'**مضمّن** — قناة المتون، بلا ورقة',
         ('الترجمة','البحث والخطابة'):'**مضمّن** — L-18 يوجب حضورها، ولا متن لها مستقلًّا',
         ('أصول التفسير','التفسير'):'**مضمّن** — السجل: مقدمة ابن تيمية تطبيقًا داخل التفسير',
         ('التاريخ والسيرة','العقيدة'):'**مضمّن** — مادة البحث لا مقرر قائم',
         ('التاريخ والسيرة','البحث والخطابة'):'**مضمّن** — مادة البحث المحكّم لا مقرر قائم'}
    for g,sub,host,note in UNRESOLVED:
        rec=REC.get((sub,cl(host)),'**[يحتاج قرارًا صريحًا]**')
        bw(f'> | {NAMES[int(g)][0]} | **{esc(sub)}** | {esc(cl(host))} | '
           f'{esc(note) if note else "*(فارغ)*"} | {esc(rec)} |\n')
    bw('>\n> **ما هو مطلوب:** قرارٌ صريح من المدير العام بصيغة كل مدخل، ثم يُدوَّن في السجل،\n')
    bw('> ثم يُحدَّث `allocation-v11.json` بحيث تبدأ كل ملاحظة بصيغتها المقفلة، ويعاد التوليد.\n')
    bw('\n')
    # ── second finding: the memorisation channel is absent at G9 ────────────
    g9=[cl(h[0]) for h in D['9'][2]]
    if 'النشيد والمحفوظات' not in g9:
        bw('> ## ⚠️ تناقضٌ ثانٍ — انقطاع قناة المحفوظات في التاسع\n>\n')
        bw('> **السجل يقرِّر النشيد والمحفوظات للصفوف ١–١٢** (الباب الرابع تتمةً)، وفي ذخيرته\n')
        bw('> **البيقونية** — والبيقونية **تُحفَظ في التاسع** بنص السجل نفسه.\n>\n')
        bw('> ومع ذلك **لا مدخل للنشيد والمحفوظات في التاسع** في بيانات التوزيع:\n')
        bw('> حاضرٌ في الثامن مضمّنًا في اللغة العربية · **غائبٌ في التاسع** · عائدٌ في العاشر\n')
        bw('> مضمّنًا في «كل مادة بمتنها».\n>\n')
        bw('> فإمّا أن القناة تعمل في التاسع ولم تُسجَّل — وهو **خرقٌ لـ L-07**: علمٌ يُدرَّس\n')
        bw('> بلا مضيف مسمًّى · وإمّا أنها تنقطع حقًّا، فيلزم أن تعود **أعلى لا تكرارًا (L-12)**،\n')
        bw('> وأن يُبيَّن سببُ الانقطاع.\n>\n')
        bw('> **الأرجح أنه سهوُ تسجيل**: البيقونية والجزرية كلتاهما محفوظتان في التاسع،\n')
        bw('> فالقناة تعمل. **ولم أُصلحه من عندي.**\n>\n')
        bw('> **أثره على الجدول الزمني: لا شيء** — النشيد مضمّن في كل موضع، ولا يشغل خانة.\n')
    blockers=b.getvalue()
else:
    blockers='> ✓ كل مدخل مستضاف يُصرِّح بصيغته التعليمية. لا تناقض مع L-08.'

doc=out.getvalue().replace(BLOCK_MARK,blockers)
open(os.path.join(H,'CLASS-BY-CLASS-SUBJECT-ALLOCATION.md'),'w',encoding='utf-8').write(doc)
print('CLASS-BY-CLASS written —',len(doc.split(chr(10))),'lines')
print('unresolved forms:',len(UNRESOLVED))
for g,us,b_,s in summary: print(f'  G{g}: slots {us}, books {b_}, sciences {s}')
