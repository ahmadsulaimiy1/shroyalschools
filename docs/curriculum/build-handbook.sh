#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════
#  SHRS · GACAIS-CURRICULUM — build the handbook PDF from source
# ════════════════════════════════════════════════════════════════════
#  The handbook is HTML rendered by headless Chromium. It is built in
#  TWO passes, and the split is not cosmetic:
#
#    pass 1 — the cover, at margin 0 and with no running head or foot,
#             so the binding bleeds to the trim;
#    pass 2 — the body, at 29/23/19mm with the furniture templates.
#
#  A single pass cannot do both, and an earlier attempt to force it with
#  `@page{margin:0}` overrode the margins passed to the renderer and
#  printed the running head across the text on 1478 pages. That CSS rule
#  must never come back.
#
#  usage:  bash build-handbook.sh
# ════════════════════════════════════════════════════════════════════
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FONTDIR=/usr/share/fonts/truetype/shrs
TMP="${TMPDIR:-/tmp}/shrs-build"; mkdir -p "$TMP"

# ── 1 · the six faces the design system names ───────────────────────
#    Arabic:  Amiri (reading) · Reem Kufi (institutional) · Noto Kufi (clarity)
#    Latin :  EB Garamond (text) · Cormorant Garamond (display) · Archivo (furniture)
fetch() {  # fetch <css-family-spec> <installed-name>
  local css url
  css=$(curl -sS -L -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64)' \
        "https://fonts.googleapis.com/css2?family=$1&display=swap")
  url=$(printf '%s' "$css" | grep -o 'https://fonts.gstatic.com[^)]*' | head -1)
  [ -n "$url" ] || { echo "!! could not resolve $1" >&2; return 1; }
  curl -sS -L "$url" -o "$FONTDIR/$2.ttf"
}
mkdir -p "$FONTDIR"
for spec in "Amiri:wght@400|Amiri-Regular" "Amiri:wght@700|Amiri-Bold" \
            "Reem+Kufi:wght@400|ReemKufi-Regular" "Reem+Kufi:wght@600|ReemKufi-SemiBold" \
            "Noto+Kufi+Arabic:wght@400|NotoKufiArabic-Regular" \
            "Noto+Kufi+Arabic:wght@700|NotoKufiArabic-Bold" \
            "EB+Garamond:wght@400|EBGaramond-Regular" "EB+Garamond:wght@500|EBGaramond-Medium" \
            "Cormorant+Garamond:wght@600|CormorantGaramond-SemiBold" \
            "Cormorant+Garamond:wght@700|CormorantGaramond-Bold" \
            "Archivo:wght@500|Archivo-Medium" "Archivo:wght@600|Archivo-SemiBold" \
            "Archivo:wght@700|Archivo-Bold"; do
  f="${spec%%|*}"; n="${spec##*|}"
  [ -s "$FONTDIR/$n.ttf" ] || { echo "  fetching $n"; fetch "$f" "$n"; }
done
fc-cache -f >/dev/null 2>&1 || true

# ── 2 · generate the HTML from the register and the allocation ──────
python3 "$HERE/verify.py" || { echo "!! a locked item is broken — not building" >&2; exit 1; }
python3 "$HERE/gen-teacher-guide.py"

# ── 3 · render each board on its own terms, then join ───────────────
#  The two boards bleed to the trim, so they render at margin 0 with no
#  running furniture. The text block does not. The wraparound sheet is a
#  fourth render at the binder's trim — front · spine · back on one piece.
python3 "$HERE/topdf.py" "$HERE/HANDBOOK-cover.html" "$TMP/front.pdf" 1 NOFURN
python3 "$HERE/topdf.py" "$HERE/HANDBOOK-back.html"  "$TMP/back.pdf"  1 NOFURN
python3 "$HERE/topdf.py" "$HERE/HANDBOOK-body.html"  "$TMP/body.pdf"
pdfunite "$TMP/front.pdf" "$TMP/body.pdf" "$TMP/back.pdf" \
         "$HERE/SHRS-CURRICULUM-HANDBOOK.pdf"

WRAP_W=$(python3 -c "import re,io;src=open('$HERE/gen-teacher-guide.py',encoding='utf-8').read();\
import ast;print(2*210+int(re.search(r'SPINE_MM = (\\d+)',src).group(1)))")
python3 "$HERE/topdf.py" "$HERE/HANDBOOK-wrap.html" \
        "$HERE/SHRS-CURRICULUM-COVER-WRAP.pdf" 1 NOFURN "${WRAP_W}x297"

# ── 4 · the furniture must never print over the text ────────────────
NPAGES=$(pdfinfo "$HERE/SHRS-CURRICULUM-HANDBOOK.pdf" | awk '/^Pages:/{print $2}')
python3 "$HERE/audit-furniture.py" "$HERE/SHRS-CURRICULUM-HANDBOOK.pdf" \
        "--boards=1,$NPAGES"      # the front board and the back board
echo "built · $HERE/SHRS-CURRICULUM-HANDBOOK.pdf"
echo "built · $HERE/SHRS-CURRICULUM-COVER-WRAP.pdf  (${WRAP_W} x 297 mm, trim, no bleed)"
