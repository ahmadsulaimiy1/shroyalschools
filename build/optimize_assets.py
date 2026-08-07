#!/usr/bin/env python3
"""Derive print-ready web assets from the originals in assets/source.

Two kinds of derivation happen here:

  * Logo marks (crest, award seal, stole) are gold/ink artwork sitting on a flat
    white studio background. Knocking that white out to alpha lets the same file
    sit on the royal-blue cover and on ivory interior pages without a halo.
  * Photographs are downscaled and re-encoded so the whole brochure can be
    inlined as base64 for the Adobe Express import without blowing past its
    size budget.

Run: python3 build/optimize_assets.py
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "source"
OUT = ROOT / "assets" / "web"

# Luminance window for the white knockout. Pixels at or above OPAQUE_BELOW stay
# fully opaque, pixels at or above TRANSPARENT_AT vanish, and the band between
# them feathers so the gold keeps its antialiased edge.
TRANSPARENT_AT = 246
OPAQUE_BELOW = 206

# Marks are cut out of white and kept as PNG; the tuple is (source, output, max edge).
MARKS = [
    ("crest-gold-on-white.jpg", "crest-gold.png", 1400),
    ("award-seal-annual-competition.jpg", "award-seal.png", 1200),
    ("graduation-stole.jpg", "graduation-stole.png", 900),
]

# Photographs keep their background; the tuple is (source, output, max edge, quality).
PHOTOS = [
    ("crest-star-badge.png", "crest-star-badge.jpg", 900, 88),
    ("campus-front-elevation.jpg", "campus-front-elevation.jpg", 1500, 82),
    ("campus-main-gate.jpg", "campus-main-gate.jpg", 1500, 82),
    ("lab-chemistry.jpg", "lab-chemistry.jpg", 1300, 80),
    ("lab-biology.jpg", "lab-biology.jpg", 1300, 80),
    ("lab-physics.jpg", "lab-physics.jpg", 1300, 80),
    ("vocational-workshop.jpg", "vocational-workshop.jpg", 1300, 80),
    ("boarding-dining.jpg", "boarding-dining.jpg", 1300, 80),
    ("sports-and-games.jpg", "sports-and-games.jpg", 1300, 80),
    ("classroom-session.jpg", "classroom-session.jpg", 1500, 82),
    ("spelling-medalists-a.jpg", "spelling-medalists-a.jpg", 1300, 82),
    ("spelling-medalists-b.jpg", "spelling-medalists-b.jpg", 1300, 82),
    ("graduands-name-cards.jpg", "graduands-name-cards.jpg", 1300, 82),
]


def fit(image: Image.Image, max_edge: int) -> Image.Image:
    """Downscale so the longest edge is at most max_edge. Never upscales."""
    longest = max(image.size)
    if longest <= max_edge:
        return image
    scale = max_edge / longest
    size = (round(image.width * scale), round(image.height * scale))
    return image.resize(size, Image.LANCZOS)


def knock_out_white(image: Image.Image) -> Image.Image:
    """Replace the flat white studio background with alpha, feathering the edge."""
    rgb = image.convert("RGB")
    luminance = rgb.convert("L")

    span = TRANSPARENT_AT - OPAQUE_BELOW
    # point() over the 0-255 lookup table is far cheaper than per-pixel Python.
    alpha = luminance.point(
        lambda v: 255 if v <= OPAQUE_BELOW else (0 if v >= TRANSPARENT_AT else round(255 * (TRANSPARENT_AT - v) / span))
    )

    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out


def crest_mark() -> None:
    """Crop the crest down to the shield and arabesque, dropping its wordmark.

    The full crest carries "Sultan Hanafi Royal Schools" beneath a rule. On the
    covers that name is already set in type directly below, so the lockup reads
    as a stutter. This variant is the mark alone, trimmed to its own ink.
    """
    with Image.open(OUT / "crest-gold.png") as img:
        # Rows 168-868 are the crest; the rule and wordmark start at 893.
        cropped = img.crop((0, 150, img.width, 880))
        bbox = cropped.getchannel("A").getbbox()
        mark = cropped.crop(bbox)

    target = OUT / "crest-mark.png"
    mark.save(target, "PNG", optimize=True)
    print(f"mark   {'crest-mark.png':<34} {mark.width}x{mark.height}  {target.stat().st_size // 1024} KB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    for source_name, out_name, max_edge in MARKS:
        with Image.open(SRC / source_name) as img:
            result = knock_out_white(fit(img, max_edge))
        target = OUT / out_name
        result.save(target, "PNG", optimize=True)
        print(f"mark   {out_name:<34} {result.width}x{result.height}  {target.stat().st_size // 1024} KB")

    crest_mark()

    for source_name, out_name, max_edge, quality in PHOTOS:
        with Image.open(SRC / source_name) as img:
            result = fit(img.convert("RGB"), max_edge)
        target = OUT / out_name
        result.save(target, "JPEG", quality=quality, optimize=True, progressive=True)
        print(f"photo  {out_name:<34} {result.width}x{result.height}  {target.stat().st_size // 1024} KB")

    total = sum(p.stat().st_size for p in OUT.iterdir())
    print(f"\ntotal web assets: {total // 1024} KB")


if __name__ == "__main__":
    main()
