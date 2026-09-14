# -*- coding: utf-8 -*-
"""Generate SUBJECT-LIFECYCLE.md — every registered subject, G1 through G12."""
import json,os,io,importlib.util
H=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location('ga',os.path.join(H,'gen-allocation.py'))
# reuse the data layer without re-running the renderer: read it directly instead
D=json.load(open(os.path.join(H,'allocation-v11.json'),encoding='utf-8'))
import curriculum_data as C
cl = C.display
NAMES={1:'الأول',2:'الثاني',3:'الثالث',4:'الرابع',5:'الخامس',6:'السادس',7:'السابع',
8:'الثامن',9:'التاسع',10:'العاشر',11:'الحادي عشر',12:'الثاني عشر'}
PROG={'القرآن':'الأول · القرآن وعلومه','اللغة':'الثاني · اللغة وعلومها',
      'الإسلامية':'الثالث · الدراسات الإسلامية','التتويج':'خدمة سنة التتويج'}
PORDER=['القرآن','اللغة','الإسلامية','التتويج']
STR={g:['التوحيد','الفقه','الحديث النبوي','السيرة النبوية'] for g in range(1,6)}
STR[6]=['التوحيد','الفقه','الحديث النبوي']
FORMS=['مدمج','مضمّن','وحدة','مسار','دوراني','مستقل']

life={}   # sub -> {g: dict}
prog={}
UNRES=[]
for g in range(1,13):
    corner,slots,hosted=D[str(g)]
    life.setdefault('حفظ القرآن الكريم',{})[g]=dict(f='مستقل',d='الساعة المحمية',h='—',n='خارج الخانات',s='')
    prog['حفظ القرآن الكريم']='القرآن'
    for name,p,n,note in corner:
        sub=cl(name)
        if sub.startswith('كتاب اللغة'): sub='اللغة العربية'
        if sub.startswith('كتاب الدراسات'): sub='التربية الإسلامية'
        life.setdefault(sub,{})[g]=dict(f='مستقل',d='سنة',h='—',n=note or '',s=str(n))
        prog[sub]=p
    for lab,cap,terms in slots:
        for term,nt,name,p,note in terms:
            sub=cl(name); sub='الفرائض' if sub=='الفرائض التطبيقية' else sub
            life.setdefault(sub,{})[g]=dict(f='مستقل',d=f'مقرر فصلي {term}',h='—',n=note or '',s=str(cap))
            prog.setdefault(sub,p)
    for name,p,host,note in hosted:
        sub=cl(name); nt=note.strip(); f=None
        for x in FORMS:
            if nt.startswith(x): f=x; nt=nt[len(x):].lstrip(' —·-').strip(); break
        if f is None: f='مضمّن'; UNRES.append((g,sub)); nt=(nt or '')+' ⚠️'
        life.setdefault(sub,{})[g]=dict(f=f,d='—',h=cl(host),n=nt,s='—')
        prog.setdefault(sub,p)
    for s in STR[g] if g<=6 else []:
        life.setdefault(s,{}).setdefault(g,dict(f='مسار',d='—',
            h='كتاب الدراسات الإسلامية',n='خيط داخل الكتاب',s='—'))
        prog.setdefault(s,'الإسلامية')

SYM={'مستقل':'●','مدمج':'◍','مضمّن':'◌','وحدة':'▣','مسار':'▷'}
def cell(e):
    if e is None: return '·'
    if e['f']=='مستقل' and e['d'].startswith('مقرر'): return '◐'
    if e['f']=='مستقل' and e['d']=='الساعة المحمية': return '◆'
    return SYM.get(e['f'],'?')

o=io.StringIO(); w=o.write
w('''# دورة حياة المادة · SUBJECT LIFECYCLE · G1 → G12
### متى تبدأ · متى تستقلّ · متى تُدمَج · متى تُضمَّن · متى تصير مقررًا فصليًّا · متى تنقطع · متى تعود أعلى

> **مولَّدة آليًّا** من `allocation-v11.json` بـ `gen-lifecycle.py`. **لا تُحرَّر باليد.**
> رفيقتها: `CLASS-BY-CLASS-SUBJECT-ALLOCATION.md`.

| الرمز | الصيغة | خانة | كتاب | ورقة | المعدل |
|---|---|---|---|---|---|
| **◆** | الساعة القرآنية المحمية | **خارج العدّ** | كتاب القرآن وعلومه | بوابة أداء | يدخل |
| **●** | **مستقل** سنةً كاملة | نعم | نعم | نعم | يدخل |
| **◐** | **مستقل** مقررًا فصليًّا | خانة مشتركة | كراسة المقررات | نعم | يدخل |
| **◍** | **مدمج** مع شريك مسمّى | يشترك | كتاب الشريك | قسم مسمّى · أرضية ٤٠٪ | يدخل مجموعًا |
| **◌** | **مضمّن** في مضيف مسمّى | لا | لا | داخل المضيف | عبر المضيف |
| **▣** | **وحدة** | لا | لا | تقدير إنجاز | **لا يدخل** |
| **▷** | **مسار** داخل كتاب | لا | لا | لا رقم | لا |
| **·** | لا تُدرَّس في هذا الصف | | | | |

''')
if UNRES:
    w(f'> ⚠️ **{len(UNRES)} مدخلًا** لا تُصرِّح ببنيتها في بيانات التوزيع، وعُرضت مؤقتًا كـ `◌ مضمّن`\n')
    w('> **وهو استنتاج لا قرار.** التفصيل والحسم في `CLASS-BY-CLASS-SUBJECT-ALLOCATION.md`.\n\n')
w('---\n\n## الخريطة الكاملة\n\n')
w('| المادة | البرنامج | ١ | ٢ | ٣ | ٤ | ٥ | ٦ | ٧ | ٨ | ٩ | ١٠ | ١١ | ١٢ |\n')
w('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
order=sorted(life,key=lambda s:(PORDER.index(prog[s]),min(life[s]),-len(life[s])))
for s in order:
    cells=' | '.join(cell(life[s].get(g)) for g in range(1,13))
    w(f'| **{s}** | {prog[s][:12]} | {cells} |\n')
w(f'\n**{len(life)} مادة وخدمة مسجَّلة.**\n\n---\n\n')

w('# المسار التفصيلي لكل مادة\n\n')
for p in PORDER:
    subs=[s for s in order if prog[s]==p]
    w(f'## البرنامج {PROG[p]} — {len(subs)} مادة\n\n')
    for s in subs:
        gs=sorted(life[s])
        w(f'### {s}\n\n')
        chain=[]
        for g in range(1,13):
            e=life[s].get(g)
            chain.append(f'**ص{g}** {cell(e)}' if e else f'ص{g} ·')
        w('> '+' → '.join(chain)+'\n\n')
        # narrative
        first=gs[0]; runs=[]; st=pv=gs[0]
        for x in gs[1:]:
            if x==pv+1: pv=x
            else: runs.append((st,pv)); st=pv=x
        runs.append((st,pv))
        facts=[f'**تبدأ في الصف {NAMES[first]}**']
        ind=[g for g in gs if life[s][g]['f']=='مستقل' and life[s][g]['d']=='سنة']
        trm=[g for g in gs if life[s][g]['d'].startswith('مقرر')]
        mrg=[g for g in gs if life[s][g]['f']=='مدمج']
        emb=[g for g in gs if life[s][g]['f']=='مضمّن']
        unt=[g for g in gs if life[s][g]['f']=='وحدة']
        stz=[g for g in gs if life[s][g]['f']=='مسار']
        if ind: facts.append(f'**مستقلة سنويًّا**: {"، ".join(NAMES[g] for g in ind)}')
        if trm: facts.append(f'**مقررًا فصليًّا**: '+"، ".join(f'{NAMES[g]} ({life[s][g]["d"].split()[-1]})' for g in trm))
        if mrg: facts.append('**مدمجة**: '+"، ".join(f'{NAMES[g]} مع {life[s][g]["h"]}' for g in mrg))
        if emb: facts.append('**مضمّنة**: '+"، ".join(f'{NAMES[g]} في {life[s][g]["h"]}' for g in emb))
        if unt: facts.append('**وحدة**: '+"، ".join(NAMES[g] for g in unt))
        if stz: facts.append(f'**مسارًا داخل كتاب الدراسات الإسلامية**: {NAMES[stz[0]]}–{NAMES[stz[-1]]}')
        if len(runs)>1:
            gaps=[f'{NAMES[runs[i][1]+1]}–{NAMES[runs[i+1][0]-1]}' if runs[i+1][0]-runs[i][1]>2
                  else NAMES[runs[i][1]+1] for i in range(len(runs)-1)]
            facts.append(f'**تنقطع** في: {"، ".join(gaps)} — **وتعود أعلى، لا تكرارًا (L-12)**')
        w('- '+'\n- '.join(facts)+'\n\n')
        w('| الصف | الصيغة | خانات | الموضع | المضيف / الشريك | البيان |\n|---|---|---|---|---|---|\n')
        for g in gs:
            e=life[s][g]
            nn=e["n"].replace("|","\\|") if e["n"] else "—"
            w(f'| {NAMES[g]} | **{e["f"]}** | {e["s"]} | {e["d"]} | {e["h"]} | {nn} |\n')
        w('\n')
open(os.path.join(H,'SUBJECT-LIFECYCLE.md'),'w',encoding='utf-8').write(o.getvalue())
print('SUBJECT-LIFECYCLE written —',len(o.getvalue().split(chr(10))),'lines,',len(life),'subjects')
