#!/usr/bin/env python3
"""Render the Sultan Hanafi Royal Schools ceremony documents from data.

Two A4 documents come out of one shared design system, so a change to the
palette or the type scale moves both together:

  prospectus/graduation-ceremony-brochure.html   the order of proceedings
  prospectus/graduand-yearbook.html              the class keepsake

Both are self-describing for the Adobe Express importer (hz: metadata, one
.page root per printed page) and both print correctly straight from a browser.

Run: python3 build/build.py
"""

import json
import math
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "prospectus"

# A4 at 96 dpi — the pixel canvas the Express importer resolves mm to.
CANVAS_W, CANVAS_H = 794, 1123

FONT_KIT = '<link rel="stylesheet" href="https://use.typekit.net/ikm7jfn.css">'

PALETTE = {
    "NAVY": "#14305E",
    "NAVY_DEEP": "#0E2246",
    "NAVY_SOFT": "#1D4179",
    "GOLD": "#B98F33",
    "GOLD_LIGHT": "#D9B65F",
    "GOLD_DARK": "#8A6A1F",
    "IVORY": "#FAF6EC",
    "IVORY_DEEP": "#F2EADA",
    "PAPER": "#FFFFFF",
    "INK": "#1F1B14",
    "MUTED": "#5E574A",
    "RULE": "#D8CDB4",
}


# ---------------------------------------------------------------- ornaments


def octagram(size_attr: str = "", fill: str = "currentColor", opacity: str = "1") -> str:
    """An eight-point khātam star — the motif already on the school's own badge.

    Built from two overlapping squares, which is what gives Islamic geometric
    star-and-cross patterning its particular proportion.
    """
    outer, inner = 50.0, 50.0 * 0.76537  # cos(45°)/cos(22.5°)
    points = []
    for k in range(16):
        radius = outer if k % 2 == 0 else inner
        angle = math.radians(k * 22.5 - 90)
        points.append(f"{50 + radius * math.cos(angle):.2f},{50 + radius * math.sin(angle):.2f}")
    return (
        f'<svg class="star" viewBox="0 0 100 100" {size_attr} aria-hidden="true">'
        f'<polygon points="{" ".join(points)}" fill="{fill}" opacity="{opacity}"/></svg>'
    )


def divider(tone: str = "gold") -> str:
    """A centred rule broken by a small star — used between sections."""
    return (
        f'<div class="divider divider--{tone}">'
        f'<span class="divider__line"></span>'
        f'{octagram()}'
        f'<span class="divider__line"></span>'
        f"</div>"
    )


def corner_stars() -> str:
    """A small khātam star set into each corner of the gold frame."""
    return "".join(
        f'<span class="corner-star corner-star--{position}">{octagram()}</span>'
        for position in ("tl", "tr", "bl", "br")
    )


# ---------------------------------------------------------------- helpers


def esc(text) -> str:
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tbc(text) -> str:
    """Wrap placeholder copy so it is visibly unfinished on the printed page."""
    if text is None:
        return ""
    body = esc(text)
    if "⟨" in str(text):
        return f'<span class="tbc">{body}</span>'
    return body


def page(content: str, tone: str = "ivory", extra_class: str = "") -> str:
    classes = f"page page--{tone} {extra_class}".strip()
    return (
        f'<section class="{classes}" data-canvas-width="{CANVAS_W}" '
        f'data-canvas-height="{CANVAS_H}">{content}</section>'
    )


def photo(filename: str, caption: str = "", cls: str = "") -> str:
    cap = f'<figcaption class="caption">{esc(caption)}</figcaption>' if caption else ""
    return (
        f'<figure class="photo {cls}">'
        f'<img src="../assets/web/{filename}" alt="{esc(caption) or "Sultan Hanafi Royal Schools"}">'
        f"{cap}</figure>"
    )


def running_foot(label: str, number: int) -> str:
    return (
        f'<footer class="foot">'
        f'<span class="foot__label">{esc(label)}</span>'
        f'<span class="foot__num">{number}</span>'
        f"</footer>"
    )


def draft_banner(verified: bool) -> str:
    if verified:
        return ""
    return (
        '<div class="draft">Draft — roll pending verification. '
        "Confirm every spelling against the register before printing.</div>"
    )


# ---------------------------------------------------------------- stylesheet

CSS = Template(
    """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: #3F4A5A;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10mm;
  padding: 10mm 0;
}

/* ---- print ---- */

@page { size: 210mm 297mm; margin: 0; }

@media print {
  body { display: block; background: $PAPER; gap: 0; padding: 0; }
  .page { break-after: page; page-break-after: always; }
  .page:last-child { break-after: auto; page-break-after: auto; }
}

/* ---- canvas ---- */

.page {
  position: relative;
  width: 210mm;
  height: 297mm;
  overflow: hidden;
  background: $PAPER;
  color: $INK;
}

.page--ivory { background: $IVORY; }
.page--navy  { background: $NAVY; color: $IVORY; }
.page--deep  { background: $NAVY_DEEP; color: $IVORY; }

/* ---- type roles, shared by both documents ---- */

.display {
  font-family: "adobe-caslon-pro", serif;
  font-weight: 600;
  font-size: 34pt;
  line-height: 1.08;
  letter-spacing: 0.01em;
}

.title {
  font-family: "adobe-caslon-pro", serif;
  font-weight: 600;
  font-size: 22pt;
  line-height: 1.15;
}

.heading {
  font-family: "adobe-caslon-pro", serif;
  font-weight: 600;
  font-size: 15pt;
  line-height: 1.2;
  color: $NAVY;
}

.page--navy .heading, .page--deep .heading { color: $GOLD_LIGHT; }

.accent {
  font-family: "adobe-caslon-pro", serif;
  font-weight: 600;
  font-style: italic;
}

.body {
  font-family: "source-serif-4", serif;
  font-weight: 400;
  font-size: 10.5pt;
  line-height: 1.62;
  color: $INK;
}

.page--navy .body, .page--deep .body { color: $IVORY; }

.label {
  font-family: "source-sans-3", sans-serif;
  font-weight: 600;
  font-size: 7.5pt;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: $GOLD_DARK;
}

.page--navy .label, .page--deep .label { color: $GOLD_LIGHT; }

.caption {
  font-family: "source-sans-3", sans-serif;
  font-weight: 400;
  font-size: 7.5pt;
  line-height: 1.4;
  color: $MUTED;
  margin-top: 2mm;
}

.page--navy .caption, .page--deep .caption { color: $IVORY_DEEP; }

.arabic {
  font-family: "adobe-arabic", sans-serif;
  font-weight: 700;
  direction: rtl;
  line-height: 1.7;
}

.tbc {
  color: $GOLD_DARK;
  border-bottom: 0.4mm dotted $GOLD;
  padding-bottom: 0.3mm;
}

.page--navy .tbc, .page--deep .tbc {
  color: $GOLD_LIGHT;
  border-bottom-color: $GOLD_LIGHT;
}

/* ---- ornament ---- */

.star { width: 4mm; height: 4mm; color: $GOLD; flex: none; }

.divider {
  display: flex;
  align-items: center;
  gap: 3mm;
  color: $GOLD;
}

.divider__line {
  flex: 1;
  height: 0.35mm;
  background: $GOLD;
  opacity: 0.55;
}

.divider--light { color: $GOLD_LIGHT; }
.divider--light .divider__line { background: $GOLD_LIGHT; opacity: 0.7; }

.corner-star { position: absolute; display: block; }
.corner-star .star { width: 5.5mm; height: 5.5mm; color: $GOLD; opacity: 0.85; }
.corner-star--tl { left: 8.2mm;  top: 8.2mm; }
.corner-star--tr { right: 8.2mm; top: 8.2mm; }
.corner-star--bl { left: 8.2mm;  bottom: 8.2mm; }
.corner-star--br { right: 8.2mm; bottom: 8.2mm; }

.frame {
  position: absolute;
  inset: 10mm;
  border: 0.5mm solid $GOLD;
  opacity: 0.55;
}

.frame--inner {
  position: absolute;
  inset: 12mm;
  border: 0.2mm solid $GOLD;
  opacity: 0.4;
}

/* ---- page furniture ---- */

.pad { position: absolute; inset: 18mm; }

.foot {
  position: absolute;
  left: 18mm;
  right: 18mm;
  bottom: 10mm;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-family: "source-sans-3", sans-serif;
  font-size: 7pt;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: $MUTED;
  border-top: 0.25mm solid $RULE;
  padding-top: 2mm;
}

.page--navy .foot, .page--deep .foot {
  color: $IVORY_DEEP;
  border-top-color: rgba(217, 182, 95, 0.45);
}

.foot__num { font-weight: 600; color: $GOLD_DARK; }
.page--navy .foot__num, .page--deep .foot__num { color: $GOLD_LIGHT; }

.section-head { margin-bottom: 7mm; }
.section-head .label { display: block; margin-bottom: 2.5mm; }
.section-head .title { color: $NAVY; }
.page--navy .section-head .title, .page--deep .section-head .title { color: $GOLD_LIGHT; }
.section-head .divider { margin-top: 4mm; }

/* ---- cover ---- */

.cover__crest {
  position: absolute;
  left: 50%;
  top: 34mm;
  transform: translateX(-50%);
  width: 62mm;
}

.cover__body { position: absolute; left: 22mm; right: 22mm; top: 108mm; text-align: center; }
.cover__school { font-size: 15pt; letter-spacing: 0.16em; text-transform: uppercase; color: $GOLD_LIGHT;
                 font-family: "source-sans-3", sans-serif; font-weight: 600; }
.cover__arabic { font-size: 17pt; color: $GOLD_LIGHT; margin-top: 3mm; }
.cover__rule { width: 34mm; height: 0.4mm; background: $GOLD; margin: 7mm auto; opacity: 0.8; }
.cover__title { color: $IVORY; margin-bottom: 4mm; }
.cover__arabic-title { font-size: 20pt; color: $IVORY; margin-bottom: 6mm; }
.cover__meta { margin-top: 8mm; }
.cover__meta div { margin-bottom: 2.5mm; }

.cover__foot {
  position: absolute;
  left: 22mm; right: 22mm; bottom: 20mm;
  text-align: center;
}

/* ---- verse panel ---- */

.verse {
  background: $NAVY;
  color: $IVORY;
  padding: 12mm 14mm;
  text-align: center;
}

.verse .arabic { font-size: 19pt; color: $GOLD_LIGHT; margin-bottom: 6mm; }
.verse__translation { font-size: 11pt; line-height: 1.6; font-style: italic;
                      font-family: "adobe-caslon-pro", serif; font-weight: 600; }
.verse__ref { margin-top: 5mm; }

/* ---- identity strip ---- */

.identity { display: flex; gap: 6mm; margin-top: 9mm; }
.identity__col { flex: 1; }
.identity__col .label { display: block; margin-bottom: 2mm; }
.identity ul { list-style: none; }
.identity li {
  font-family: "source-serif-4", serif;
  font-size: 9.5pt;
  line-height: 1.55;
  padding-left: 4mm;
  position: relative;
}
.identity li::before {
  content: "";
  position: absolute;
  left: 0; top: 1.9mm;
  width: 1.6mm; height: 1.6mm;
  background: $GOLD;
  transform: rotate(45deg);
}

/* ---- order of proceedings ---- */

.order { list-style: none; }

.order li {
  display: flex;
  align-items: baseline;
  gap: 4mm;
  padding: 2.15mm 0;
  border-bottom: 0.2mm dotted $RULE;
}

.order__n {
  font-family: "source-sans-3", sans-serif;
  font-weight: 600;
  font-size: 8pt;
  color: $GOLD_DARK;
  width: 7mm;
  flex: none;
}

.order__item {
  font-family: "source-serif-4", serif;
  font-size: 10pt;
  line-height: 1.3;
  flex: 1;
  color: $INK;
}

.order__by {
  font-family: "source-sans-3", sans-serif;
  font-size: 7.5pt;
  color: $MUTED;
  display: block;
  margin-top: 0.6mm;
}

.order__time {
  font-family: "source-sans-3", sans-serif;
  font-size: 7.5pt;
  color: $GOLD_DARK;
  white-space: nowrap;
  flex: none;
}

/* ---- dignitaries ---- */

.dig { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 7mm; margin-top: 6mm; }
.dig__role { font-family: "source-sans-3", sans-serif; font-weight: 600; font-size: 7pt;
             letter-spacing: 0.16em; text-transform: uppercase; color: $GOLD_DARK; }
.dig__name { font-family: "adobe-caslon-pro", serif; font-weight: 600; font-size: 12pt;
             color: $NAVY; margin-top: 1mm; }

/* ---- roll ---- */

.roll {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  column-gap: 7mm;
  margin-top: 5mm;
}

.roll__name {
  font-family: "source-serif-4", serif;
  font-size: 9.5pt;
  line-height: 1.35;
  padding: 1.7mm 0 1.7mm 5mm;
  border-bottom: 0.2mm solid $RULE;
  position: relative;
}

.roll__name::before {
  content: "";
  position: absolute;
  left: 0.5mm; top: 3.3mm;
  width: 1.5mm; height: 1.5mm;
  background: $GOLD;
  transform: rotate(45deg);
}

.roll-section { margin-bottom: 8mm; }
.roll-section__head { display: flex; align-items: baseline; gap: 3mm; margin-bottom: 1mm; }
.roll-section__head .heading { color: $NAVY; }
.roll-section__count { font-family: "source-sans-3", sans-serif; font-size: 7.5pt; color: $MUTED; }

.draft {
  background: $GOLD;
  color: $NAVY_DEEP;
  font-family: "source-sans-3", sans-serif;
  font-weight: 600;
  font-size: 7.5pt;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 2.6mm 4mm;
  margin-bottom: 6mm;
  text-align: center;
}

/* ---- awards ---- */

.awards { list-style: none; margin-top: 4mm; }

.awards li {
  display: flex;
  align-items: baseline;
  gap: 4mm;
  padding: 3.1mm 0;
  border-bottom: 0.2mm dotted $RULE;
}

.awards__body { flex: 1; }
.awards__title { font-family: "adobe-caslon-pro", serif; font-weight: 600; font-size: 11pt; color: $NAVY; }
.awards__sub { font-family: "source-sans-3", sans-serif; font-size: 7.5pt; color: $MUTED; margin-top: 0.7mm; }
.awards__recipient { font-family: "source-serif-4", serif; font-size: 9.5pt; text-align: right;
                     width: 46mm; flex: none; }

.seal { position: absolute; right: 16mm; bottom: 20mm; width: 44mm; opacity: 0.95; }

/* ---- message page ---- */

.message__portrait { width: 100%; margin-bottom: 6mm; }
.message p { margin-bottom: 4mm; }
.message__sign { margin-top: 8mm; padding-top: 4mm; border-top: 0.25mm solid $RULE; }
.message__sign-name { font-family: "adobe-caslon-pro", serif; font-weight: 600; font-size: 13pt; color: $NAVY; }
.message__sign-role { font-family: "source-sans-3", sans-serif; font-size: 7.5pt;
                      letter-spacing: 0.14em; text-transform: uppercase; color: $MUTED; margin-top: 1.2mm; }

/* ---- photography ---- */

.photo { position: relative; }
.photo img { display: block; width: 100%; height: 100%; object-fit: cover; }

.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.grid-2 .photo img { height: 52mm; }

.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }
.grid-3 .photo img { height: 38mm; }

.hero img { height: 82mm; }
.tall img { height: 108mm; }

/* Portrait-format photographs keep their shape instead of being cropped wide. */
.portrait { width: 86mm; margin: 0 auto; }
.portrait img { height: 115mm; }

/* ---- prefects ---- */

.prefects { list-style: none; margin-top: 4mm; }
.prefects li {
  display: flex; align-items: baseline; gap: 4mm;
  padding: 2.9mm 0; border-bottom: 0.2mm dotted $RULE;
}
.prefects__office { font-family: "source-sans-3", sans-serif; font-weight: 600; font-size: 8pt;
                    letter-spacing: 0.1em; text-transform: uppercase; color: $NAVY; flex: 1; }
.prefects__name { font-family: "source-serif-4", serif; font-size: 10pt; width: 62mm; flex: none; }

/* ---- back cover ---- */

.back__crest { position: absolute; left: 50%; top: 46mm; transform: translateX(-50%); width: 52mm; }
.back__body { position: absolute; left: 24mm; right: 24mm; top: 120mm; text-align: center; }
.back__contact { margin-top: 8mm; }
.back__contact div { margin-bottom: 2.4mm; font-family: "source-serif-4", serif; font-size: 10.5pt; color: $IVORY; }
.back__web { font-family: "source-sans-3", sans-serif; font-weight: 600; font-size: 10pt;
             letter-spacing: 0.12em; color: $GOLD_LIGHT; margin-top: 5mm; }

.thanks { list-style: none; margin-top: 5mm; }
.thanks li {
  font-family: "source-serif-4", serif; font-size: 9.5pt; line-height: 1.5;
  padding: 1.6mm 0; border-bottom: 0.2mm dotted rgba(217, 182, 95, 0.4);
}
"""
).substitute(PALETTE)


# ---------------------------------------------------------------- document shell


def document(title: str, pages: list) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{esc(title)}</title>
<meta name="hz:slide-selector" content=".page">
<meta name="hz:canvas-width" content="{CANVAS_W}">
<meta name="hz:canvas-height" content="{CANVAS_H}">
{FONT_KIT}
<style>{CSS}</style>
</head>
<body>
{chr(10).join(pages)}
</body>
</html>
"""


# ---------------------------------------------------------------- shared pages


def cover_page(school, ceremony, kicker, title_en, title_ar):
    return page(
        f"""
<div class="frame"></div><div class="frame--inner"></div>
<img class="cover__crest" src="../assets/web/crest-mark.png" alt="Crest of Sultan Hanafi Royal Schools">
<div class="cover__body">
  <div class="cover__school">{esc(school["name"])}</div>
  <div class="cover__arabic arabic">{esc(school["name_arabic"])}</div>
  <div class="cover__rule"></div>
  <div class="label">{esc(kicker)}</div>
  <h1 class="display cover__title" style="margin-top:5mm">{esc(title_en)}</h1>
  <div class="cover__arabic-title arabic">{esc(title_ar)}</div>
  {divider("light")}
  <div class="cover__meta body">
    <div>{tbc(ceremony["session"])}</div>
    <div>{tbc(ceremony["date"])}</div>
    <div>{tbc(ceremony["venue"])}</div>
  </div>
</div>
<div class="cover__foot">
  <div class="label">{esc(school["modes"])} &nbsp;·&nbsp; {esc(school["website"])}</div>
</div>
""",
        tone="navy",
    )


def verse_page(school, verse_ar, verse_en, verse_ref, page_no, foot):
    provisions = "".join(f"<li>{esc(p)}</li>" for p in school["provisions"])
    phones = "".join(f"<li>{esc(p)}</li>" for p in school["phones"])
    return page(
        f"""
<div class="pad">
  <div class="verse">
    <div class="arabic">{esc(verse_ar)}</div>
    <div class="verse__translation">{esc(verse_en)}</div>
    <div class="verse__ref label">{esc(verse_ref)}</div>
  </div>

  <div style="margin-top:10mm">
    <div class="section-head">
      <span class="label">The School</span>
      <h2 class="title">{esc(school["name"])}</h2>
      {divider()}
    </div>
    <p class="body">Sultan Hanafi Royal Schools educates on three tracks at once — the
    national secular curriculum, Islamic and Arabic education, and complete
    memorization of the Qur'an — as day and boarding provision on one campus.</p>

    <div class="identity">
      <div class="identity__col">
        <span class="label">What we provide</span>
        <ul>{provisions}</ul>
      </div>
      <div class="identity__col">
        <span class="label">Contact</span>
        <ul>{phones}</ul>
      </div>
    </div>
  </div>

  <div style="margin-top:9mm">{photo("campus-front-elevation.jpg", "The school campus", "hero")}</div>
</div>
{running_foot(foot, page_no)}
""",
    )


def message_page(message, page_no, foot, portrait=None):
    paragraphs = "".join(f"<p>{tbc(p)}</p>" for p in message["paragraphs"])
    portrait_html = photo(portrait, "", "message__portrait hero") if portrait else ""
    return page(
        f"""
<div class="pad">
  <div class="section-head">
    <span class="label">Address</span>
    <h2 class="title">{esc(message["heading"])}</h2>
    {divider()}
  </div>
  {portrait_html}
  <div class="message body">
    {paragraphs}
    <div class="message__sign">
      <div class="message__sign-name">{tbc(message["signature"])}</div>
      <div class="message__sign-role">{esc(message["signature_role"])}</div>
    </div>
  </div>
</div>
{running_foot(foot, page_no)}
""",
    )


def roll_pages(graduands, page_no, foot, intro):
    """The class roll — one page, with the draft banner while unverified."""
    blocks = []
    for section in graduands["sections"]:
        names = "".join(f'<div class="roll__name">{tbc(n)}</div>' for n in section["names"])
        blocks.append(
            f"""
<div class="roll-section">
  <div class="roll-section__head">
    <h3 class="heading">{esc(section["title"])}</h3>
    <span class="roll-section__count">{len(section["names"])} names</span>
  </div>
  <div class="caption" style="margin-top:0">{tbc(section["subtitle"])}</div>
  <div class="roll">{names}</div>
</div>"""
        )

    return page(
        f"""
<div class="pad">
  <div class="section-head">
    <span class="label">The Class</span>
    <h2 class="title">{esc(intro)}</h2>
    {divider()}
  </div>
  {draft_banner(graduands["verified"])}
  {"".join(blocks)}
  <div style="margin-top:4mm">{divider()}</div>
</div>
{running_foot(foot, page_no)}
""",
    )


def back_page(school, closing_ar, closing_en):
    phones = "".join(f"<div>{esc(p)}</div>" for p in school["phones"])
    return page(
        f"""
<div class="frame"></div><div class="frame--inner"></div>
<img class="back__crest" src="../assets/web/crest-mark.png" alt="Crest of Sultan Hanafi Royal Schools">
<div class="back__body">
  <div class="arabic" style="font-size:17pt;color:#D9B65F">{esc(closing_ar)}</div>
  <div class="body" style="font-style:italic;margin-top:4mm">{esc(closing_en)}</div>
  {divider("light")}
  <div class="back__contact">
    <div class="label" style="margin-bottom:3mm">{esc(school["name"])}</div>
    {phones}
    <div class="back__web">{esc(school["website"])}</div>
  </div>
</div>
{corner_stars()}
""",
        tone="deep",
    )


# ---------------------------------------------------------------- brochure


def build_brochure(school, ceremony, graduands) -> str:
    foot = f'{school["name"]} · Graduation Ceremony'

    order_items = []
    for i, entry in enumerate(ceremony["order"], start=1):
        by = f'<span class="order__by">{tbc(entry["by"])}</span>' if entry.get("by") else ""
        time = f'<span class="order__time">{tbc(entry["time"])}</span>' if entry.get("time") else ""
        order_items.append(
            f'<li><span class="order__n">{i:02d}</span>'
            f'<span class="order__item">{esc(entry["item"])}{by}</span>{time}</li>'
        )

    dignitaries = "".join(
        f'<div><div class="dig__role">{esc(d["role"])}</div>'
        f'<div class="dig__name">{tbc(d["name"])}</div></div>'
        for d in ceremony["dignitaries"]
    )

    awards = "".join(
        f'<li><div class="awards__body">'
        f'<div class="awards__title">{esc(a["title"])}</div>'
        f'<div class="awards__sub">{esc(a["subtitle"])}</div></div>'
        f'<div class="awards__recipient">{tbc(a["recipient"])}</div></li>'
        for a in ceremony["awards"]
    )

    thanks = "".join(f"<li>{tbc(t)}</li>" for t in ceremony["acknowledgements"])

    pages = [
        cover_page(
            school,
            ceremony,
            ceremony["edition"],
            "Graduation Ceremony",
            "حفلة تخرج",
        ),
        verse_page(
            school,
            "يَرْفَعِ اللَّهُ الَّذِينَ آمَنُوا مِنكُمْ وَالَّذِينَ أُوتُوا الْعِلْمَ دَرَجَاتٍ",
            "Allah will raise, by degrees, those of you who believe and those who are given knowledge.",
            "Sūrah al-Mujādilah 58 : 11",
            2,
            foot,
        ),
        message_page(ceremony["proprietor_message"], 3, foot),
        # Dignitaries
        page(
            f"""
<div class="pad">
  <div class="section-head">
    <span class="label">In Attendance</span>
    <h2 class="title">Guests and Dignitaries</h2>
    {divider()}
  </div>
  <div class="dig">{dignitaries}</div>
  <div style="margin-top:10mm">
    <span class="label" style="display:block;margin-bottom:3mm">The Occasion</span>
    <p class="body">{tbc(ceremony["session"])} &nbsp;·&nbsp; {tbc(ceremony["date"])}
    &nbsp;·&nbsp; {tbc(ceremony["time"])}</p>
    <p class="body" style="margin-top:2mm">{tbc(ceremony["venue"])}</p>
  </div>
  <div style="margin-top:9mm">{photo("campus-main-gate.jpg", "The main gate", "hero")}</div>
</div>
{running_foot(foot, 4)}
""",
        ),
        # Order of proceedings
        page(
            f"""
<div class="pad">
  <div class="section-head">
    <span class="label">Programme</span>
    <h2 class="title">Order of Proceedings</h2>
    {divider()}
  </div>
  <ul class="order">{"".join(order_items)}</ul>
</div>
{running_foot(foot, 5)}
""",
        ),
        roll_pages(graduands, 6, foot, "The Graduands"),
        # Awards
        page(
            f"""
<div class="pad">
  <div class="section-head">
    <span class="label">Honours</span>
    <h2 class="title">Awards and Prizes</h2>
    {divider()}
  </div>
  <ul class="awards">{awards}</ul>
</div>
<img class="seal" src="../assets/web/award-seal.png" alt="The Sultan Royal Annual Competition Awards seal">
{running_foot(foot, 7)}
""",
        ),
        # Acknowledgements
        page(
            f"""
<div class="pad">
  <div class="section-head">
    <span class="label">With Gratitude</span>
    <h2 class="title">Acknowledgements</h2>
    {divider()}
  </div>
  <p class="body">The Management of {esc(school["name"])} records its thanks to all
  who made this ceremony possible.</p>
  <ul class="thanks" style="border-top:0.2mm dotted #D8CDB4">{thanks}</ul>
  <div class="grid-2" style="margin-top:9mm">
    {photo("classroom-session.jpg", "A class in session")}
    {photo("spelling-medalists-a.jpg", "SPELL Africa Spelling Leaders Competition")}
  </div>
</div>
{running_foot(foot, 8)}
""",
        ),
        back_page(
            school,
            "رَبِّ زِدْنِي عِلْمًا",
            "My Lord, increase me in knowledge.  ·  Sūrah Ṭā Hā 20 : 114",
        ),
    ]
    return document("Graduation Ceremony Brochure — Sultan Hanafi Royal Schools", pages)


# ---------------------------------------------------------------- yearbook


def build_yearbook(school, ceremony, graduands) -> str:
    foot = f'{school["name"]} · Graduand Yearbook'

    prefects = "".join(
        f'<li><span class="prefects__office">{esc(p["office"])}</span>'
        f'<span class="prefects__name">{tbc(p["name"])}</span></li>'
        for p in graduands["prefects"]
    )

    pages = [
        cover_page(
            school,
            ceremony,
            f'Graduand Yearbook · Class of {ceremony["class_year"]}',
            "The Graduating Set",
            "الدفعة المتخرجة",
        ),
        verse_page(
            school,
            "وَقُل رَّبِّ زِدْنِي عِلْمًا",
            "And say: My Lord, increase me in knowledge.",
            "Sūrah Ṭā Hā 20 : 114",
            2,
            foot,
        ),
        message_page(ceremony["head_teacher_message"], 3, foot),
        roll_pages(graduands, 4, foot, f'The Class of {ceremony["class_year"]}'),
        # Academics
        page(
            f"""
<div class="pad">
  <div class="section-head">
    <span class="label">Life at Sultan Hanafi</span>
    <h2 class="title">In the Laboratories</h2>
    {divider()}
  </div>
  <p class="body">Three equipped laboratories carried this set through the sciences —
  chemistry, biology and physics — alongside the Islamic and Arabic syllabus.</p>
  <div style="margin-top:6mm">{photo("lab-chemistry.jpg", "The chemistry laboratory", "hero")}</div>
  <div class="grid-2" style="margin-top:5mm">
    {photo("lab-biology.jpg", "The biology laboratory")}
    {photo("lab-physics.jpg", "The physics laboratory")}
  </div>
</div>
{running_foot(foot, 5)}
""",
        ),
        # Skills and boarding
        page(
            f"""
<div class="pad">
  <div class="section-head">
    <span class="label">Life at Sultan Hanafi</span>
    <h2 class="title">Skills, Board and Games</h2>
    {divider()}
  </div>
  <p class="body">Beyond the classroom: the vocational and technical workshop, the
  boarding house, and the games that filled the evenings.</p>
  <div style="margin-top:6mm">{photo("vocational-workshop.jpg", "The vocational and technical workshop", "hero")}</div>
  <div class="grid-2" style="margin-top:5mm">
    {photo("boarding-dining.jpg", "The boarding house dining room")}
    {photo("sports-and-games.jpg", "Games and sports equipment")}
  </div>
</div>
{running_foot(foot, 6)}
""",
        ),
        # Achievements
        page(
            f"""
<div class="pad">
  <div class="section-head">
    <span class="label">Achievement</span>
    <h2 class="title">Competitions and Honours</h2>
    {divider()}
  </div>
  <p class="body">Pupils of Sultan Hanafi Royal Schools carried medals home from the
  SPELL Africa International Spelling Leaders Competition, and the school's own annual
  awards recognise excellence in Qur'an, Arabic language and adhān.</p>
  <div class="grid-2" style="margin-top:6mm">
    {photo("spelling-medalists-a.jpg", "Medalists at the Spelling Leaders Competition")}
    {photo("spelling-medalists-b.jpg", "Medalists at the Spelling Leaders Competition")}
  </div>
  <div style="margin-top:6mm">
    {photo("graduands-name-cards.jpg", "Students with name cards — confirm the occasion before captioning", "portrait")}
  </div>
</div>
{running_foot(foot, 7)}
""",
        ),
        # Prefects
        page(
            f"""
<div class="pad">
  <div class="section-head">
    <span class="label">Office</span>
    <h2 class="title">Prefects of the Set</h2>
    {divider()}
  </div>
  <ul class="prefects">{prefects}</ul>
  <div style="margin-top:9mm">
    <span class="label" style="display:block;margin-bottom:3mm">The Stole</span>
    <p class="body">Each graduand is invested with the school stole in royal blue and gold,
    bearing the crest and the words <span class="accent">Graduation Ceremony · حفلة تخرج</span>.</p>
  </div>
  <img src="../assets/web/graduation-stole.png" alt="The graduation stole"
       style="display:block;width:64mm;margin:5mm auto 0">
</div>
{running_foot(foot, 8)}
""",
        ),
        back_page(
            school,
            "وَفَوْقَ كُلِّ ذِي عِلْمٍ عَلِيمٌ",
            "And above every possessor of knowledge is one more knowing.  ·  Sūrah Yūsuf 12 : 76",
        ),
    ]
    return document("Graduand Yearbook — Sultan Hanafi Royal Schools", pages)


# ---------------------------------------------------------------- main


def main() -> None:
    school = json.loads((DATA / "school.json").read_text(encoding="utf-8"))
    ceremony = json.loads((DATA / "ceremony.json").read_text(encoding="utf-8"))
    graduands = json.loads((DATA / "graduands.json").read_text(encoding="utf-8"))

    OUT.mkdir(parents=True, exist_ok=True)

    targets = {
        "graduation-ceremony-brochure.html": build_brochure(school, ceremony, graduands),
        "graduand-yearbook.html": build_yearbook(school, ceremony, graduands),
    }

    for name, html in targets.items():
        path = OUT / name
        path.write_text(html, encoding="utf-8")
        pages = html.count('class="page ')
        print(f"{name:<42} {pages} pages   {len(html) // 1024} KB")

    if not graduands["verified"]:
        print('\nNote: data/graduands.json has "verified": false — the roll pages carry a DRAFT banner.')


if __name__ == "__main__":
    main()
