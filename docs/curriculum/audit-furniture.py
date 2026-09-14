import subprocess, sys, re, html
from collections import Counter
PDF = sys.argv[1]
# The full-bleed boards are named by the build, not guessed. Guessing them
# from 'this page has no furniture' fails: the covers carry their own
# letterspaced GACAIS line, and pdftotext splits letterspaced Latin into
# single letters, so the cover's own type matches the running foot's tokens.
BOARDS = set()
for _a in sys.argv[2:]:
    if _a.startswith('--boards='):
        BOARDS = {int(v) for v in _a.split('=',1)[1].split(',') if v.strip()}
PT = 72/25.4
TOP = 29.0*PT      # content must not start above this
BOT = 23.0*PT      # nor end below (H - this)
xml = subprocess.run(['pdftotext','-bbox','-enc','UTF-8',PDF,'-'],
                     capture_output=True, text=True).stdout
pages = re.findall(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', xml, re.S)
W = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
# words appearing in the same band on nearly every page are the furniture
band_top, band_bot = Counter(), Counter()
for w,h,body in pages:
    H=float(h)
    for m in W.finditer(body):
        y0,y1,t = float(m.group(2)), float(m.group(4)), html.unescape(m.group(5)).strip()
        if not t: continue
        if y1 < 60: band_top[t]+=1
        if y0 > H-60: band_bot[t]+=1
N=len(pages)
furn = {t for t,c in band_top.items() if c > N*0.5} | {t for t,c in band_bot.items() if c > N*0.5}
# where the furniture actually sits, measured from the rendered file
tops, bots = [], []
for w,h,body in pages:
    H=float(h)
    for m in W.finditer(body):
        y0,y1,t = float(m.group(2)), float(m.group(4)), html.unescape(m.group(5)).strip()
        if t in furn:
            if y1 < 60: tops.append(y1)
            if y0 > H-60: bots.append(y0)
hdr_bot = max(tops) if tops else 0
ftr_top = min(bots) if bots else float(pages[0][1])
print(f'furniture band: header ends y={hdr_bot:.1f} · footer starts y={ftr_top:.1f}')
bad=[]; boards=set()
for pno,(w,h,body) in enumerate(pages,1):
    H=float(h)
    # the furniture's real position ON THIS PAGE, not a global minimum
    pt_, pb_ = [], []
    for m in W.finditer(body):
        y0,y1,t = float(m.group(2)), float(m.group(4)), html.unescape(m.group(5)).strip()
        if t in furn:
            if y1 < 60: pt_.append(y1)
            if y0 > H-60: pb_.append(y0)
    hdr_bot = max(pt_) if pt_ else 0
    ftr_top = min(pb_) if pb_ else H
    for m in W.finditer(body):
        x0,y0,x1,y1 = map(float, m.group(1,2,3,4))
        t = html.unescape(m.group(5)).strip()
        if not t or t in furn: continue
        if pno in BOARDS:
            boards.add(pno); continue          # a board bleeds; nothing to collide with
        if y1 < 22 or y0 > H-34: continue         # inside the furniture band = furniture
        # a collision is content intruding on the furniture band (or within 8pt)
        if y0 < hdr_bot + 8:  bad.append((pno,'HEADER',round(y0,1),t[:30]))
        elif y1 > ftr_top - 8: bad.append((pno,'FOOTER',round(y1,1),t[:30]))
print(f'pages={N}   furniture tokens ignored: {len(furn)}')
print('full-bleed boards skipped: ' + (', '.join(f'p{n}' for n in sorted(BOARDS)) or 'none'))
_missing = BOARDS - set(range(1, N+1))
if _missing: print(f'!! declared boards outside the file: {sorted(_missing)}')
print(f'REAL COLLISIONS: {len(bad)}')
seen=set()
for pno,zone,y,t in bad:
    if (pno,zone) in seen: continue
    seen.add((pno,zone)); print(f'  p{pno:>3}  {zone}  y={y}  "{t}"')
