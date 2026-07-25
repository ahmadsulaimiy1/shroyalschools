# Editorial typefaces

Three free, open-source (SIL Open Font License) families make up the type
system shared by both AMIU flagship publications — the Strategic
Implementation Blueprint and the Constitution. Each family has a distinct
typographic role, rather than three sizes of the same design (the earlier
Cinzel/Cormorant Garamond/EB Garamond system was replaced for exactly this
reason — a close read correctly flagged it as visually flat, since all
three were the same old-style-Garamond-descended serif at different
weights). Static weight instances were extracted from their source variable
fonts via `fonttools varLib.instancer`:

- **Fraunces** (Black, SemiBold, Regular, Italic) — display: covers,
  monumental numerals, chapter/article openers, headings, pull quotes. An
  ink-trap display serif with real range and a contemporary editorial
  identity (Google Fonts, OFL).
- **Source Serif 4** (Regular, Bold, Italic, Bold Italic) — reading: body
  text. Built for long-form reading; deliberately not a Garamond derivative,
  so it reads as a distinct second voice against Fraunces (Google Fonts,
  OFL).
- **Archivo** (Regular, SemiBold, Bold, Black) — structural: kickers,
  captions, headers/footers, table data, TOC rows, numbered-provision
  labels. Replaces Liberation Sans (the open-source Arial substitute)
  everywhere it appeared — that generic system-default sans was itself a
  significant contributor to a "Word document" rather than "flagship
  publication" feel, since it recurred on every page. (Google Fonts, OFL)

Source: https://github.com/google/fonts (`ofl/fraunces`, `ofl/sourceserif4`,
`ofl/archivo`)

## Install (required before running `build_reference.py` / `assemble.py`)

```
mkdir -p /usr/share/fonts/truetype/amiu-editorial
cp assets/fonts/*.ttf /usr/share/fonts/truetype/amiu-editorial/
fc-cache -f
```

Without this step, LibreOffice's headless PDF export will silently
substitute a fallback font for every Fraunces/Source Serif 4/Archivo
reference — no error, just wrong typography.
`fc-list | grep -iE "fraunces|source serif|archivo"` should list 12 faces
once installed correctly. Matplotlib figure generators
(`gen_figures.py`, `gen_constitution_figures.py`) also need these fonts
registered with `matplotlib.font_manager` and the matplotlib font cache
cleared (`rm -rf ~/.cache/matplotlib`) before regenerating any exhibit —
otherwise the exhibit-frame labels silently fall back to a default sans.
