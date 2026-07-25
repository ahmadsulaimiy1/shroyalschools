# Editorial typefaces

Three free, open-source (SIL Open Font License) families make up the
Blueprint's typography — a single Garamond-family system top to bottom,
extracted as static weight instances from their source variable fonts via
`fonttools varLib.instancer`:

- **Cinzel** (Regular, Bold) — monumental chapter numerals and kicker labels.
  A free, purpose-built alternative to Trajan Pro (Google Fonts, OFL).
- **Cormorant Garamond** (Regular, Medium, SemiBold, Bold, Italic, Medium
  Italic) — chapter titles, section headings, and pull quotes (Google Fonts,
  OFL).
- **EB Garamond** (Regular, Bold, Italic, Bold Italic) — body text. A free
  equivalent of Adobe Garamond Pro, the requested body face, which cannot be
  licensed here; pairs with Cormorant Garamond as one Garamond-derived
  system rather than mixing unrelated serif designs (Google Fonts, OFL).

Source: https://github.com/google/fonts (`ofl/cinzel`, `ofl/cormorantgaramond`,
`ofl/ebgaramond`)

## Install (required before running `build_reference.py` / `assemble.py`)

```
mkdir -p /usr/share/fonts/truetype/amiu-editorial
cp assets/fonts/*.ttf /usr/share/fonts/truetype/amiu-editorial/
fc-cache -f
```

Without this step, LibreOffice's headless PDF export will silently substitute
a fallback font for every Cinzel/Cormorant Garamond/EB Garamond reference —
no error, just wrong typography. `fc-list | grep -iE "cinzel|cormorant|garamond"`
should list 12 faces once installed correctly.
