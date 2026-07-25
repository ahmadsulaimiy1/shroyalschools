# Editorial typefaces

Two free, open-source (SIL Open Font License) families used for the Blueprint's
display typography, extracted as static weight instances from their source
variable fonts via `fonttools varLib.instancer`:

- **Cinzel** (Regular, Bold) — monumental chapter numerals and kicker labels.
  A free, purpose-built alternative to Trajan Pro (Google Fonts, OFL).
- **Cormorant Garamond** (Regular, Medium, SemiBold, Bold, Italic, Medium
  Italic) — chapter titles, section headings, and pull quotes (Google Fonts,
  OFL).

Source: https://github.com/google/fonts (`ofl/cinzel`, `ofl/cormorantgaramond`)

Body text remains on Bitstream Charter, a distinct serif face, deliberately —
see the comment in `assets/build_reference.py`.

## Install (required before running `build_reference.py` / `assemble.py`)

```
mkdir -p /usr/share/fonts/truetype/amiu-editorial
cp assets/fonts/*.ttf /usr/share/fonts/truetype/amiu-editorial/
fc-cache -f
```

Without this step, LibreOffice's headless PDF export will silently substitute
a fallback font for every Cinzel/Cormorant Garamond reference — no error, just
wrong typography. `fc-list | grep -iE "cinzel|cormorant"` should list 8 faces
once installed correctly.
