#!/usr/bin/env python3
"""Produce self-contained copies of the documents in dist/.

Two bundles, because the two destinations want opposite things:

  --mode express   Keeps the Adobe Fonts <link> exactly as the fontkit returned
                   it (the Express importer fetches it server-side and needs it
                   verbatim) and inlines only the images.

  --mode print     For rendering a PDF here, where the network policy blocks
                   use.typekit.net. Substitutes the Adobe families for their
                   closest openly-licensed equivalents and embeds the font files
                   in the document, so the PDF carries its own typography:

                     adobe-caslon-pro  ->  EB Garamond    (old-style, same colour)
                     source-serif-4    ->  Source Serif 4 (the same typeface)
                     source-sans-3     ->  Source Sans 3  (the same typeface)
                     adobe-arabic      ->  Amiri          (classical Naskh)

Run: python3 build/bundle.py --mode print
"""

import argparse
import base64
import mimetypes
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "prospectus"
DIST = ROOT / "dist"
CACHE = ROOT / "build" / ".fontcache"

TYPEKIT_LINK_RE = re.compile(r'<link rel="stylesheet" href="https://use\.typekit\.net/[^"]+">')

GOOGLE_CSS = (
    "https://fonts.googleapis.com/css2"
    "?family=EB+Garamond:ital,wght@0,600;1,600"
    "&family=Source+Serif+4:wght@400"
    "&family=Source+Sans+3:wght@400;600"
    "&family=Amiri:wght@700"
)

# An old User-Agent makes Google Fonts serve one unsubsetted TTF per style
# instead of dozens of unicode-range woff2 slices — far easier to embed.
LEGACY_UA = "Mozilla/4.0"

FAMILY_SUBSTITUTIONS = {
    '"adobe-caslon-pro", serif': "'EB Garamond', serif",
    '"source-serif-4", serif': "'Source Serif 4', serif",
    '"source-sans-3", sans-serif': "'Source Sans 3', sans-serif",
    '"adobe-arabic", sans-serif': "'Amiri', serif",
}


def fetch(url: str, ua: str = LEGACY_UA) -> bytes:
    CACHE.mkdir(parents=True, exist_ok=True)
    key = CACHE / (base64.urlsafe_b64encode(url.encode()).decode()[:120] + ".bin")
    if key.exists():
        return key.read_bytes()
    request = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    key.write_bytes(payload)
    return payload


def google_font_style() -> str:
    """Fetch the Google Fonts CSS and rewrite every src url() as an embedded font."""
    css = fetch(GOOGLE_CSS).decode("utf-8")

    def embed(match: re.Match) -> str:
        url = match.group(1)
        data = base64.b64encode(fetch(url)).decode("ascii")
        return f"url(data:font/ttf;base64,{data}) format('truetype')"

    css = re.sub(r"url\((https://fonts\.gstatic\.com[^)]+)\)\s*format\('truetype'\)", embed, css)
    return f"<style>{css}</style>"


def inline_images(html: str) -> str:
    """Replace every ../assets/web/... reference with a data URI."""

    def embed(match: re.Match) -> str:
        filename = match.group(1)
        path = ROOT / "assets" / "web" / filename
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f'src="data:{mime};base64,{data}"'

    return re.sub(r'src="\.\./assets/web/([^"]+)"', embed, html)


def build(mode: str) -> list:
    DIST.mkdir(parents=True, exist_ok=True)
    written = []

    style_block = google_font_style() if mode == "print" else None

    for source in sorted(SRC.glob("*.html")):
        html = source.read_text(encoding="utf-8")

        if mode == "print":
            html = TYPEKIT_LINK_RE.sub(style_block, html)
            for adobe, replacement in FAMILY_SUBSTITUTIONS.items():
                html = html.replace(adobe, replacement)

        html = inline_images(html)

        target = DIST / f"{source.stem}.{mode}.html"
        target.write_text(html, encoding="utf-8")
        written.append(target)
        print(f"{target.relative_to(ROOT)}  {target.stat().st_size // 1024} KB")

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["print", "express"], default="print")
    build(parser.parse_args().mode)


if __name__ == "__main__":
    main()
