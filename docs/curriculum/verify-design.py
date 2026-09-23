# -*- coding: utf-8 -*-
"""قفلُ التصميم · THE DESIGN LOCK — mechanical enforcement of D-01 … D-16.

`verify.py` fails the build when a locked CURRICULUM item is broken. Until now
the locked DESIGN items lived only in prose, in
`CURRICULUM-EDITORIAL-BIBLE.md` §X-ter, which is exactly the condition under
which decisions in this project have always been lost: written down, then
rebuilt away by someone who did not read them.

This script reads the generator and the built PDF and **exits non-zero** if a
locked item is broken. It is run by `build-handbook.sh` before the PDF is
accepted. Every check names the item it enforces and the failure it prevents.

A check here must be able to FAIL. Each one below was tested by breaking the
thing it guards; a check that cannot fail is decoration, and decoration is how
the last set of checks passed green while the document carried ten red markers.
"""
import hashlib
import os
import re
import subprocess
import sys

H = os.path.dirname(os.path.abspath(__file__))
# The first pass runs BEFORE the generator, when the PDF on disk is still the
# previous build — judging this run by the last run's artefact. --source-only
# checks the source; the post-build pass checks the source AND the book.
SOURCE_ONLY = '--source-only' in sys.argv
GEN = open(os.path.join(H, 'gen-teacher-guide.py'), encoding='utf-8').read()
CSS = GEN[GEN.index('CSS = """'):GEN.index('\n"""\n\n\ndef ') if '\n"""\n\n\ndef ' in GEN
                                   else GEN.rindex('"""')]

FAIL, NOTE = [], []


def check(item, ok, what, prevents):
    (print if ok else FAIL.append)(f'  {"✓" if ok else "✗"}  {item} — {what}'
                                   + ('' if ok else f'\n        يمنع: {prevents}'))
    if ok:
        return True
    return False


def rule(sel):
    """The declaration block of the first rule whose selector list contains sel."""
    m = re.search(re.escape(sel) + r'[^{}]*\{([^}]*)\}', CSS)
    return m.group(1) if m else ''


print('قفلُ التصميم · THE DESIGN LOCK\n')

# ── D-01 · six faces, and no seventh ────────────────────────────────
TOKENS = ('--fa', '--fk', '--fn', '--fl', '--fd', '--fu')
declared = {t for t in TOKENS if re.search(re.escape(t) + r'\s*:', CSS)}
stray = set(re.findall(r"font-family:\s*'([^']+)'", CSS))
check('D-01', declared == set(TOKENS) and not stray,
      f'six faces declared, none applied outside a token'
      + (f' — STRAY: {sorted(stray)}' if stray else ''),
      'a seventh face creeping in, and the house voice becoming four voices')

# ── D-02 · Reem Kufi never sets vowelled Arabic ─────────────────────
# The forbidden selectors are the VOWELLED headings, matched EXACTLY — an
# earlier version matched them as substrings and flagged `.sot h3`, which is a
# short unvowelled section title and is Reem Kufi's proper work. A check that
# cries wolf gets switched off, so it is matched per comma-separated selector.
VOWELLED = {'h2', 'h3', '.alh', '.opener h2', '.xsec h4'}
vowelled = []
for m in re.finditer(r'([^{}]+)\{([^}]*var\(--fk\)[^}]*)\}', CSS):
    sels = [' '.join(x.split()) for x in re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S).split(',')]
    vowelled += [x for x in sels if x in VOWELLED]
check('D-02', not vowelled, 'Reem Kufi sets no vowelled heading',
      'the display kufi crowding the ḥarakāt at heading size, as it did')

# ── D-03 · Arabic is never letterspaced ─────────────────────────────
tracked = []
for m in re.finditer(r'([^{}]+)\{([^}]*)\}', CSS):
    sel, body = m.group(1), m.group(2)
    if re.search(r'var\(--f[akn]\)', body):
        ls = re.search(r'letter-spacing:\s*([^;]+)', body)
        if ls and ls.group(1).strip() not in ('0', '0em', 'normal'):
            tracked.append(sel.strip()[:40])
check('D-03', not tracked,
      'no Arabic-voice rule carries tracking'
      + (f' — TRACKED: {tracked}' if tracked else ''),
      'tracking a cursive script, which pulls the joins apart')

# ── D-04 · the six colours, at their exact values ───────────────────
PALETTE = {'--panel': '#2A1C10', '--gold': '#B08E4E', '--green': '#0F3F38',
           '--blue': '#082A66', '--ox': '#5E1B26', '--char': '#3A342C'}
wrong = {k: v for k, v in PALETTE.items()
         if not re.search(re.escape(k) + r':\s*' + v + r'\s*;', CSS, re.I)}
check('D-04', not wrong, 'the six institutional colours hold their values'
      + (f' — MOVED: {sorted(wrong)}' if wrong else ''),
      'the palette drifting shade by shade until it means nothing')

# ── D-05 · burgundy flags, never fills ──────────────────────────────
filled = [m.group(0)[:60] for m in re.finditer(r'background[^;:]*:\s*[^;]*var\(--burg\)[^;]*;', CSS)]
check('D-05', not filled, 'burgundy is never a filled surface'
      + (f' — FILLED: {filled}' if filled else ''),
      'the flag colour becoming a surface and being read as programme three')

# ── D-06 · programme → colour, and the ramps that never cross ───────
# EVERY load-bearing declaration is named. Two weaker versions of this check
# passed a tamper: the first asked whether ANY family kept the colour, and the
# second matched the bare token, which `--blue` satisfies from inside
# `--bluetint`. Both were "somebody, somewhere, still mentions it" — which is
# what a broken lock looks like from the outside. The declarations are listed.
MAP = {'p1': '--green', 'p2': '--blue', 'p3': '--ox', 'p4': '--char'}
# .xp and .xreg carry the THREE programmes only: التتويج is not one of them,
# and its absence there is the design, not an omission.
DECLS = ([('.alt.{p} h4', 'border-color'), ('.alt.{p} .atab thead th', 'background'),
          ('.ccp.{p}:before', 'background'), ('.ccp.{p} h6', 'color'),
          ('.opener.{p}:before', 'background'), ('.xmap tr.mh.{p} td', 'border-top-color')],
         [('.xp.{p}:before', 'background'), ('.xreg.{p} h4', 'border-color')])
bad = []
for k, tok in MAP.items():
    pats = DECLS[0] + (DECLS[1] if k != 'p4' else [])
    for pat, prop in pats:
        sel = pat.format(p=k)
        m = re.search(re.escape(sel) + r'\s*\{([^}]*)\}', CSS)
        if not (m and re.search(prop + r':\s*var\(' + re.escape(tok) + r'\)', m.group(1))):
            bad.append(f'{sel}{{{prop}}}')
check('D-06', not bad,
      f'all {sum(len(DECLS[0]) + (len(DECLS[1]) if k != "p4" else 0) for k in MAP)} '
      'programme declarations hold' + (f' — BROKEN: {bad}' if bad else ''),
      'a programme quietly losing its colour in one view while keeping it in another')

# ── D-07 · the front board's geometry, and what was refused ─────────
pan = rule('.cover .panel')
w_m = re.search(r'width:(\d+)mm', pan)
# The asymmetry is the point, so it is MEASURED: the cloth must be held to the
# top and right edges, must not also be given a left edge (which would centre
# it), and must leave a cream margin between a fifth and a third of the page —
# the three-to-one split that was asked for.
w = int(w_m.group(1)) if w_m else 0
cream = 210 - w
check('D-07',
      re.search(r'(^|;)\s*top:0\s*;', ';' + pan) is not None
      and re.search(r'(^|;)\s*right:0\s*;', ';' + pan) is not None
      and 'left:' not in pan and 42 <= cream <= 70,
      f'the cloth is held to the top and right edges; cream margin {cream}mm',
      'the return of the centred, symmetrical composition that was refused')

# ── D-08 · the arch is cropped by the trim ──────────────────────────
arch = rule('.cover .arch')
check('D-08', re.search(r'right:\s*-\d', arch) is not None,
      'the arch runs off the trim — a fragment, not an emblem',
      'the arch being centred and turning back into a medallion')

# ── D-09 · one ornament, used exactly twice ─────────────────────────
n_lat = GEN.count("lat_svg('")
check('D-09', n_lat == 2, f'the lattice band appears exactly twice (found {n_lat})',
      'the one ornament multiplying into decoration')

# ── D-10 · gold is always a gradient ────────────────────────────────
foil = ['.cover .t2', '.cover .hrule', '.cover .lrule']
flat = [s for s in foil if 'linear-gradient' not in rule(s)]
check('D-10', not flat, 'every foil element is a gradient' + (f' — FLAT: {flat}' if flat else ''),
      'gold printing as yellow ink instead of reading as metal')

# ── D-11 · the title is typography ──────────────────────────────────
t1, t2, tl = rule('.cover .t1'), rule('.cover .t2'), rule('.cover .titleL')
check('D-11',
      '43pt' in t1 and '43pt' in t2 and 'var(--fa)' in t1
      and 'var(--fd)' in tl and 'letter-spacing:.2em' in tl,
      'the title holds its scale, its two voices and its Latin setting',
      'the title sliding back to being an ordinary line of text')

# ── D-12 · front, spine and back are one object ─────────────────────
fp, bp = rule('.cover .panel'), rule('.back .bpanel')
f_h = re.search(r'height:(\d+)mm', fp)
b_h = re.search(r'height:(\d+)mm', bp)
f_band = re.search(r'top:(\d+)mm', rule('.cover .band'))
b_band = re.search(r'top:(\d+)mm', rule('.back .bband'))
check('D-12',
      all([f_h, b_h, f_band, b_band])
      and int(b_h.group(1)) < int(f_h.group(1))
      and f_band.group(1) != b_band.group(1)
      and 'scaleX(-1)' in rule('.back .barch'),
      'the back is quieter, its arch mirrored, its band at another station',
      'the back becoming blank, or a copy of the front')

# ── D-13 · Arabic spines read top to bottom ─────────────────────────
sp = rule('.bspine .sp')
m_spine = re.search(r'^SPINE_MM = (\d+)', GEN, re.M)
check('D-13', 'vertical-rl' in sp and 'rotate' not in sp and m_spine is not None,
      f'the spine is set vertically, not rotated by hand · SPINE_MM='
      f'{m_spine.group(1) if m_spine else "?"}mm',
      'a spine that reads bottom-to-top, which no Arabic book does')

# ── D-14 · the Institution's marks, used as given ───────────────────
LOCKED = {'shrs-crest.png': '9050ea9fe7cc4c2c1d6ff8c4a9cb26f488c85bed878032df695d00aca45b4ceb',
          'gacais-mark.png': '9d573297d0998e684789b3be15dc4ecbafd267c0d24de61da4c1a66e41d260ad'}
moved = []
for name, want in LOCKED.items():
    fp = os.path.join(H, 'assets', name)
    got = hashlib.sha256(open(fp, 'rb').read()).hexdigest() if os.path.exists(fp) else 'MISSING'
    if got != want:
        moved.append(f'{name}:{got[:12]}')
check('D-14', not moved, 'the crest and the emblem are byte-for-byte as supplied'
      + (f' — ALTERED: {moved}' if moved else ''),
      'the Institution\'s crest being redrawn, recoloured or replaced')

# ── D-15 · no approval is claimed ───────────────────────────────────
claims = 'واعتماد' in GEN
pending = GEN.count('ولم تُعتمد بعد')
check('D-15', (not claims) and pending >= 2,
      f'no approval claimed; the pending line stands in {pending} places',
      'the book asserting an approval the Board has not given (PUB-006 art. 4)')

# ── D-16 · the furniture never prints over the text ─────────────────
check('D-16', not re.search(r'@page\{[^}]*margin:\s*0', CSS),
      'no @page margin override in the stylesheet',
      'the running head printing across the text, as it did on 1478 pages')

# ── the artefact itself ────────────────────────────────────────────
# This asked whether the book was exactly 80 pages, which is not a design
# decision — it is a page count. It duly refused a build whose only change
# was the executive register fitting on one page instead of two. A lock that
# blocks legitimate work gets deleted, so it now asserts what it MEANT: the
# outer two pages are the boards, identified by marks only the boards carry.
pdf = os.path.join(H, 'SHRS-CURRICULUM-HANDBOOK.pdf')
if SOURCE_ONLY:
    NOTE.append('source-only pass — the board check runs after the build')
elif os.path.exists(pdf):
    def page_text(n):
        return ' '.join(subprocess.run(
            ['pdftotext', '-f', str(n), '-l', str(n), pdf, '-'],
            capture_output=True, text=True).stdout.split())
    info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    n = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
    first, last = page_text(1), page_text(n)
    check('BOARDS',
          n >= 3
          and 'MMXXVI' in first and 'FIRST EDITION' in first
          and 'One curriculum across twelve classes' in last,
          f'the outer pages are the front and back boards (book is {n} pages)',
          'a board going missing from the published file')
else:
    NOTE.append('the PDF was not built, so the board check did not run')

# ── D-18 · the executive register drops nothing ─────────────────────
# Ruled by the Chairman: «34 is correct — keep the register as built.»
# A directive had named a 26-subject universe; building from it would have
# dropped الفرائض (ring-fenced by L-19, and lost once already), الإنشاء
# والتعبير (L-39), قواعد اللغة الوظيفية, فقه اللغة والمعاجم, خدمة التتويج and
# علم الكلام, merged المنطق with علم الكلام, and renamed four more.
#
# So the register is checked against the corpus itself, not against a list:
# every subject the allocation carries must appear on that page, under its own
# programme, spelled as the corpus spells it. This is the one failure mode the
# whole project exists to prevent — a name quietly not making it into a rebuild.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location('_gtg', os.path.join(H, 'gen-teacher-guide.py'))
_g = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_g)                       # safe: build() is under __main__
_page = _g.exec_register()
_blocks = re.split(r'(?=<div class="erp )', _page)
_missing, _total = [], 0
for _k, _pn, _pt, _pen, _cls, _num, _blurb in _g.PROGS:
    _subs = _g.SUBS_OF[_k]
    _total += len(_subs)
    if _k == 'التتويج':                            # carried as a note, not a block
        _where = _page
    else:
        _where = next((b for b in _blocks if f'class="erp {_cls}"' in b), '')
        if not _where:
            _missing.append(f'{_pt}: whole programme absent')
            continue
    for _sub in _subs:
        if _g.e(_sub) not in _where:
            _missing.append(f'{_pt} / {_sub}')
_rows = len(re.findall(r'<tr><th>', _page))
check('D-18', not _missing and _rows == sum(len(_g.SUBS_OF[k]) for k, *_ in _g.PROGS
                                            if k != 'التتويج'),
      f'the register carries all {_total} subjects of the corpus, '
      f'{_rows} in table rows' + (f' — MISSING: {_missing}' if _missing else ''),
      'a subject being dropped or renamed in a rebuild — the failure this '
      'whole corpus exists to prevent')

# ── a reported defect, not a failing one ────────────────────────────
# Isolated Arabic marks print in the last millimetre of the text block on a
# handful of pages: ḥarakāt with no base letter under them. They are inside
# the safe area and clear of the running foot — the furniture audit is right
# to pass them — but they are orphans, and the cause is in Chromium's paged
# rendering, not in this stylesheet: the count does not move when the fonts,
# the padding or the page contents change.
#
# It is REPORTED and not failed, for the same reason verify.py reports
# contradictions instead of fixing them: failing the build on a defect nobody
# can currently fix would only teach the next person to switch the check off.
# If this number GROWS, something new is wrong.
ORPHAN_BASELINE = 29
if not SOURCE_ONLY and os.path.exists(pdf):
    xml = subprocess.run(['pdftotext', '-bbox', '-enc', 'UTF-8', pdf, '-'],
                         capture_output=True, text=True).stdout
    pgs = re.findall(r'<page width="[\d.]+" height="[\d.]+">(.*?)</page>', xml, re.S)
    wx = re.compile(r'<word xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">'
                    r'(.*?)</word>')
    edge = 274.0 * 72 / 25.4          # the foot of the text block
    orph = [(i + 1, m.group(3)) for i, b in enumerate(pgs) if i not in (0, len(pgs) - 1)
            for m in wx.finditer(b)
            if m.group(3).strip() and float(m.group(1)) < edge < float(m.group(2))]
    pages_hit = sorted({p for p, _ in orph})
    NOTE.append(f'orphaned marks at the foot of the text block: {len(orph)} on '
                f'{len(pages_hit)} pages {pages_hit} '
                f'(recorded baseline {ORPHAN_BASELINE} — REPORTED, not failed)')
    if len(orph) > ORPHAN_BASELINE:
        FAIL.append(f'  ✗  ORPHANS — {len(orph)} orphaned marks, above the recorded '
                    f'baseline of {ORPHAN_BASELINE}\n        يمنع: a new clipping fault '
                    f'hiding behind a known one')

print()
for line in FAIL:
    print(line)
for line in NOTE:
    print(f'  · {line}')
if FAIL:
    print(f'\n✗ {len(FAIL)} من بنود القفل مكسورة — لا يُنشر.')
    print('  A locked design item is broken. It changes only by an explicit ruling')
    print('  written into CURRICULUM-EDITORIAL-BIBLE.md §X-ter FIRST, with its reason.')
    sys.exit(1)
print('\n✓ بنودُ القفل سليمة · D-01 … D-18 hold.')
