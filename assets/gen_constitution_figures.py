#!/usr/bin/env python3
"""Generate branded figures for the AMIU Constitution — Flagship Governance Edition.
Reuses the exact brand palette and signature exhibit-plate frame device from
gen_figures.py (the Blueprint's figure generator) so the two flagship
publications read as one institutional family, with a Constitution-specific
exhibit label swapped in."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

OUT = "/home/user/shroyalschools/assets/figures"
os.makedirs(OUT, exist_ok=True)

NAVY      = "#122A4E"
NAVY_DK   = "#0A1830"
NAVY_MD   = "#1F3A66"
GOLD      = "#C69A3A"
GOLD_LT   = "#E4C878"
PAPER     = "#FFFFFF"
BG_TINT   = "#F3F5F9"
GREY      = "#6B7280"
TEXT      = "#152238"

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "text.color": TEXT,
    "figure.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "savefig.facecolor": PAPER,
})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=220, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("saved", name)

ROMANC = ["C1", "C2", "C3", "C4"]

def _corner(fig, x, y, hsign, vsign, length=0.022, color=GOLD, lw=1.5):
    fig.add_artist(plt.Line2D([x, x + hsign * length], [y, y], transform=fig.transFigure,
                               color=color, linewidth=lw, solid_capstyle="butt", zorder=10))
    fig.add_artist(plt.Line2D([x, x], [y, y + vsign * length], transform=fig.transFigure,
                               color=color, linewidth=lw, solid_capstyle="butt", zorder=10))

def signature_frame(fig, exhibit_no):
    numeral = ROMANC[exhibit_no - 1]
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.975, 0.975], transform=fig.transFigure,
                               color=GOLD, linewidth=1.4, solid_capstyle="butt", zorder=10))
    fig.text(0.04, 0.983, f"AMIU EXHIBIT {numeral}", transform=fig.transFigure,
             fontsize=8.5, color=GOLD, fontweight="bold", ha="left", va="bottom")
    fig.text(0.96, 0.983, "CONSTITUTION · FLAGSHIP GOVERNANCE EDITION", transform=fig.transFigure,
             fontsize=7.5, color=GREY, ha="right", va="bottom")
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.028, 0.028], transform=fig.transFigure,
                               color=NAVY, linewidth=0.8, zorder=10))
    fig.text(0.04, 0.018, "AL-MULK INTERNATIONAL UNIVERSITY", transform=fig.transFigure,
             fontsize=7, color=GREY, ha="left", va="top")
    fig.text(0.96, 0.018, f"EXHIBIT {numeral} OF 4", transform=fig.transFigure,
             fontsize=7, color=GREY, ha="right", va="top")
    _corner(fig, 0.025, 0.945, +1, -1)
    _corner(fig, 0.975, 0.058, -1, +1)

def box(ax, x, y, w, h, text, fc=NAVY, tc="white", fs=9.5, bold=True, ec="none", lw=0):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.35,rounding_size=1.6",
                        fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", zorder=4, linespacing=1.35)

def link(ax, x1, y1, x2, y2, color="#9AA5B8", lw=1.4):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=1)

# =====================================================================
# FIGURE C1 — Bicameral Governance Architecture
# Deliberately drawn as two co-equal chambers meeting at a single
# operational link, NOT a top-down chain of command — the point the
# editorial review flagged in Article V's numbered hierarchy table.
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 7.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 78); ax.axis("off")

box(ax, 6, 58, 40, 14, "BOARD OF TRUSTEES\nSupreme Governing Authority\nArticle VI", fc=NAVY_DK, fs=10.5)
box(ax, 54, 58, 40, 14, "UNIVERSITY SENATE\nSupreme Academic Authority\nArticle VIII", fc=NAVY_DK, fs=10.5)
link(ax, 26, 65, 74, 65, color=GOLD, lw=2.2)
ax.text(50, 68.5, "CO-EQUAL CHAMBERS", ha="center", va="center", fontsize=8.5,
        color=GOLD, fontweight="bold")

box(ax, 30, 34, 40, 13, "PRESIDENT & VICE-CHANCELLOR\nSingle Operational Link\nArticle VII", fc=GOLD, tc=NAVY_DK, fs=10)
link(ax, 26, 58, 42, 47); link(ax, 74, 58, 58, 47)

box(ax, 30, 12, 40, 13, "ADMINISTRATION\nExecutive Management\nArticle IX", fc="#4C6489", fs=10)
link(ax, 50, 34, 50, 25)

ax.text(50, 4, "The Board does not interfere in academic matters; the Senate does not interfere in\nfinancial or strategic matters (Section 5.2). Each chamber's authority is direct, not delegated.",
        ha="center", va="center", fontsize=8.8, color=GREY, linespacing=1.5)

signature_frame(fig, 1)
save(fig, "con_fig1_governance.png")

# =====================================================================
# FIGURE C2 — Academic Ladder (ascending: foundation at the base)
# =====================================================================
tiers = [
    ("VII", "Post-Doctoral Fellowship", "Non-credit"),
    ("VI", "Doctor of Philosophy", "60 Credit Hours"),
    ("V", "Master of Arts", "45 Credit Hours"),
    ("IV", "Postgraduate Diploma", "30 Credit Hours"),
    ("III", "Bachelor of Arts", "120 Credit Hours"),
    ("II", "Associate Degree", "60 Credit Hours"),
    ("I", "Undergraduate Diploma", "45 Credit Hours"),
]
fig, ax = plt.subplots(figsize=(11, 8.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 95); ax.axis("off")
n = len(tiers)
top, bottom, gap = 92, 6, 1.6
h = (top - bottom - gap*(n-1)) / n
colors_t = [NAVY_DK, NAVY, NAVY_MD, "#345385", "#4C6489", GOLD, GOLD_LT]
for i, (roman, name, meta) in enumerate(tiers):
    y = top - (i+1)*h - i*gap
    width = 92 - i*8.6
    x0 = 50 - width/2
    box(ax, x0, y, width, h, "", fc=colors_t[i], fs=1)
    ax.text(x0 + 6, y + h/2, roman, ha="center", va="center", fontsize=13, fontweight="bold",
            color=(NAVY_DK if i >= 5 else "white"))
    ax.text(x0 + width/2 + 3, y + h/2 + h*0.16, name, ha="center", va="center", fontsize=10.6,
            fontweight="bold", color=(NAVY_DK if i >= 5 else "white"))
    ax.text(x0 + width/2 + 3, y + h/2 - h*0.32, meta, ha="center", va="center",
            fontsize=8.6, color=(NAVY_DK if i >= 5 else "#DCE3F0"))
signature_frame(fig, 2)
save(fig, "con_fig2_ladder.png")

# =====================================================================
# FIGURE C3 — The ISLAMIC Framework (full-page infographic)
# =====================================================================
rows = [
    ("I", "Illumination", "The pursuit of knowledge is an act of worship that illuminates the heart."),
    ("S", "Sanad", "Bound to the Prophetic tradition by an unbroken chain of transmission."),
    ("L", "Love", "The University serves the Ummah with love, particularly the marginalized."),
    ("A", "Access", "Financial capacity shall never be a barrier to knowledge."),
    ("M", "Morality", "Honesty, humility, patience, generosity — the Prophetic example."),
    ("I", "Inquiry", "Intellectual rigor and the pursuit of truth through ijtihād and taḥqīq."),
    ("C", "Calling", "Commitment to da’wah — calling to Allah with wisdom, beauty, and mercy."),
]
fig, ax = plt.subplots(figsize=(11, 9.2))
ax.set_xlim(0, 100); ax.set_ylim(0, 96); ax.axis("off")
n = len(rows)
top, bottom, gap = 92, 4, 1.4
h = (top - bottom - gap*(n-1)) / n
for i, (letter, word, meaning) in enumerate(rows):
    y = top - (i+1)*h - i*gap
    fc = NAVY_DK if i % 2 == 0 else NAVY
    box(ax, 2, y, 12, h, letter, fc=GOLD, tc=NAVY_DK, fs=22)
    b = FancyBboxPatch((16, y), 82, h, boxstyle="round,pad=0.25,rounding_size=1.2",
                        fc=fc, ec="none", zorder=3)
    ax.add_patch(b)
    ax.text(19, y + h/2 + h*0.20, word, ha="left", va="center", fontsize=13,
            fontweight="bold", color=GOLD_LT, zorder=4)
    ax.text(19, y + h/2 - h*0.28, meaning, ha="left", va="center", fontsize=9.3,
            color="#DCE3F0", zorder=4, linespacing=1.3)
signature_frame(fig, 3)
save(fig, "con_fig3_islamic.png")
