#!/usr/bin/env python3
"""Render the print bundles in dist/ to A4 PDFs using headless Chromium.

Expects `python3 build/bundle.py --mode print` to have run first, so the input
carries its own embedded fonts and images and needs no network at render time.

Run: python3 build/render_pdf.py
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

CHROME_CANDIDATES = [
    Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome"),
    Path("/opt/pw-browsers/chromium-1194/chrome-linux/headless_shell"),
]


def find_chrome() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    for name in ("chromium", "chromium-browser", "google-chrome"):
        found = shutil.which(name)
        if found:
            return Path(found)
    sys.exit("No Chromium binary found — cannot render PDFs.")


def render(chrome: Path, source: Path, target: Path) -> None:
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [
                str(chrome),
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                f"--user-data-dir={profile}",
                "--no-pdf-header-footer",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=20000",
                f"--print-to-pdf={target}",
                source.as_uri(),
            ],
            check=True,
            capture_output=True,
            timeout=240,
        )


def main() -> None:
    chrome = find_chrome()
    sources = sorted(DIST.glob("*.print.html"))
    if not sources:
        sys.exit("No *.print.html in dist/ — run build/bundle.py --mode print first.")

    for source in sources:
        target = DIST / f"{source.name.removesuffix('.print.html')}.pdf"
        render(chrome, source, target)
        print(f"{target.relative_to(ROOT)}  {target.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
