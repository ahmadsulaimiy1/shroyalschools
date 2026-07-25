# AMIU official seal

Source: official university seal artwork provided by the user (globe, crown,
open book, and geometric medallion motif, with Arabic and English wordmark),
extracted from a white-background master file.

- `amiu_full_lockup.png` — full lockup (seal + Arabic calligraphy + English
  wordmark), background removed. Reference only; not currently placed in
  either publication.
- `amiu_seal.png` — seal mark only, background removed. Tested directly on
  the navy cover background and rejected: the source artwork's anti-aliased
  edges leave a visible light halo around the globe/crown linework when
  matted straight onto a dark fill.
- `amiu_seal_medallion.png` — **the one actually used.** The seal mark
  presented on its own cream disc with a thin gold ring, the standard
  real-world convention for an institutional seal on a dark-background
  cover. Placed at the top of both publications' front covers via
  `_insert_cover_seal()` in `assemble.py` (shared by both build pipelines).
