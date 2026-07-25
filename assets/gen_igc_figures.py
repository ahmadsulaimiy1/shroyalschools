#!/usr/bin/env python3
"""Generate branded figures for the AMIU Institutional Governance Compendium.
Reuses the exact brand palette and signature exhibit-plate frame device from
gen_constitution_figures.py so all three flagship publications (Blueprint,
Constitution, Compendium) read as one institutional family."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from igc_data import CATEGORY_TOTALS, PRIORITY_COUNTS, PRIORITY_PERCENTAGES

OUT = "/home/user/shroyalschools/assets/figures"
os.makedirs(OUT, exist_ok=True)

NAVY      = "#122A4E"
NAVY_DK   = "#0A1830"
NAVY_MD   = "#1F3A66"
GOLD      = "#C69A3A"
GOLD_LT   = "#E4C878"
PAPER     = "#FFFFFF"
GREY      = "#6B7280"
TEXT      = "#152238"

plt.rcParams.update({
    "font.family": "Archivo",
    "text.color": TEXT,
    "figure.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "savefig.facecolor": PAPER,
})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=220, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("saved", name)

ROMANG = ["G1", "G2", "G3", "G4", "G5"]
N_EXHIBITS = len(ROMANG)

def _corner(fig, x, y, hsign, vsign, length=0.022, color=GOLD, lw=1.5):
    fig.add_artist(plt.Line2D([x, x + hsign * length], [y, y], transform=fig.transFigure,
                               color=color, linewidth=lw, solid_capstyle="butt", zorder=10))
    fig.add_artist(plt.Line2D([x, x], [y, y + vsign * length], transform=fig.transFigure,
                               color=color, linewidth=lw, solid_capstyle="butt", zorder=10))

def signature_frame(fig, exhibit_no):
    numeral = ROMANG[exhibit_no - 1]
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.975, 0.975], transform=fig.transFigure,
                               color=GOLD, linewidth=1.4, solid_capstyle="butt", zorder=10))
    fig.text(0.04, 0.983, f"AMIU EXHIBIT {numeral}", transform=fig.transFigure,
             fontsize=8.5, color=GOLD, fontweight="bold", ha="left", va="bottom")
    fig.text(0.96, 0.983, "INSTITUTIONAL GOVERNANCE COMPENDIUM", transform=fig.transFigure,
             fontsize=7.5, color=GREY, ha="right", va="bottom")
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.028, 0.028], transform=fig.transFigure,
                               color=NAVY, linewidth=0.8, zorder=10))
    fig.text(0.04, 0.018, "AL-MULK INTERNATIONAL UNIVERSITY", transform=fig.transFigure,
             fontsize=7, color=GREY, ha="left", va="top")
    fig.text(0.96, 0.018, f"EXHIBIT {numeral} OF {N_EXHIBITS}", transform=fig.transFigure,
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
# FIGURE G1 — Governance Hierarchy: Senate and Administration as
# co-equal, parallel bodies under the President, not a strict Level
# 1-4 chain of command — the point the editorial review flagged in
# Section 4.1's numbered table versus Section 4.4's org chart.
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 8.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 90); ax.axis("off")

box(ax, 25, 74, 50, 12, "BOARD OF TRUSTEES\nSupreme Governing Authority · Section 5", fc=NAVY_DK, fs=10.5)
link(ax, 50, 74, 50, 64, color=GOLD, lw=2.2)

box(ax, 25, 52, 50, 12, "PRESIDENT & VICE-CHANCELLOR\nChief Executive Officer · Single Operational Link · Section 6",
    fc=GOLD, tc=NAVY_DK, fs=10)
link(ax, 38, 52, 22, 41); link(ax, 62, 52, 78, 41)

box(ax, 2, 27, 40, 14, "UNIVERSITY SENATE\nSupreme Academic Authority · Section 7", fc=NAVY_DK, fs=10.5)
box(ax, 58, 27, 40, 14, "ADMINISTRATION\nExecutive Management · Section 9", fc="#4C6489", fs=10.5)
link(ax, 22, 27, 22, 18); link(ax, 78, 27, 78, 18)
ax.text(50, 41.5, "PARALLEL, CO-EQUAL BODIES", ha="center", va="center", fontsize=8.5,
        color=GOLD, fontweight="bold")

box(ax, 2, 6, 40, 12, "Academic Affairs · Student Affairs\nCurriculum · Research", fc="#DCE3F0", tc=NAVY_DK, fs=9, bold=False)
box(ax, 58, 6, 40, 12, "Finance & Operations · HR\nInformation Technology · Facilities", fc="#DCE3F0", tc=NAVY_DK, fs=9, bold=False)

ax.text(50, 1.5, "The Senate does not interfere in budget or external strategy; the Administration does not interfere\nin curriculum or grading (Section 4.2). Each body's authority is direct, not delegated through the other.",
        ha="center", va="center", fontsize=8.6, color=GREY, linespacing=1.5)

signature_frame(fig, 1)
save(fig, "igc_fig1_governance.png")

# =====================================================================
# FIGURE G2 — Phased Institutional Growth (Offices & Committees)
# =====================================================================
years = ["Year 1\n(2028)", "Year 3\n(2030)", "Year 5\n(2032)", "Year 10\n(2037)"]
offices = [10, 16, 22, 29]
committees = [5, 9, 14, 19]
enrollment = [347, 1606, 3493, 11021]

fig, ax = plt.subplots(figsize=(11, 7.6))
fig.subplots_adjust(bottom=0.24, top=0.86)
x = range(len(years))
w = 0.32
bars1 = ax.bar([i - w/2 for i in x], offices, width=w, color=NAVY_DK, label="Offices", zorder=3)
bars2 = ax.bar([i + w/2 for i in x], committees, width=w, color=GOLD, label="Committees", zorder=3)
for b in list(bars1) + list(bars2):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5, str(int(b.get_height())),
            ha="center", va="bottom", fontsize=10, fontweight="bold", color=TEXT)
ax.set_xticks(list(x)); ax.set_xticklabels(years, fontsize=10)
for i, e in enumerate(enrollment):
    ax.text(i, -0.16, f"{e:,} students", ha="center", va="top", fontsize=8.8, color=GREY,
             style="italic", transform=ax.get_xaxis_transform())
ax.set_ylim(0, 34)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.yaxis.set_visible(False)
ax.spines["bottom"].set_color("#C9CFDA")
ax.legend(loc="upper left", frameon=False, fontsize=10)
ax.set_title("Institutional Units by Growth Phase (Section 11)", fontsize=12.5, fontweight="bold",
             color=NAVY_DK, pad=14)
signature_frame(fig, 2)
save(fig, "igc_fig2_growth.png")

# =====================================================================
# FIGURE G3 — Document Inventory: Priority Breakdown (corrected)
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 7.6))
labels = ["Critical", "Important", "Complete"]
counts = [PRIORITY_COUNTS[k] for k in labels]
pcts = [PRIORITY_PERCENTAGES[k] for k in labels]
colors = [NAVY_DK, NAVY_MD, GOLD]

wedges, _ = ax.pie(counts, colors=colors, startangle=90, counterclock=False,
                    wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2))
ax.set(aspect="equal")
ax.text(0, 0.06, "107", ha="center", va="center", fontsize=34, fontweight="bold", color=NAVY_DK)
ax.text(0, -0.14, "DOCUMENTS", ha="center", va="center", fontsize=10, color=GREY, fontweight="bold")

legend_y = [0.72, 0.5, 0.28]
for i, (lab, cnt, p, c) in enumerate(zip(labels, counts, pcts, colors)):
    fig.patches.append(plt.Rectangle((0.74, legend_y[i]), 0.025, 0.04, transform=fig.transFigure,
                                      fc=c, ec="none"))
    fig.text(0.775, legend_y[i] + 0.02, f"{lab} — {cnt} documents ({p}%)", transform=fig.transFigure,
             fontsize=11, va="center", color=TEXT)
fig.text(0.5, 0.06, "Category totals: Governance 11 · Academic 19 · Student 23 · Operations 27 ·\n"
                    "Legal & Compliance 11 · Marketing 7 · Waqf & Research 9",
         transform=fig.transFigure, ha="center", fontsize=9, color=GREY, linespacing=1.5)
fig.suptitle("Complete Document Inventory: Priority Breakdown (Sections 17–19)", fontsize=12.5,
             fontweight="bold", color=NAVY_DK, y=0.965)
signature_frame(fig, 3)
save(fig, "igc_fig3_inventory.png")

# =====================================================================
# FIGURE G4 — The Academic Ladder (ascending: foundation at the base).
# Per the Table Design Directive's special requirement, this replaces the
# Section 2.6 plain table with a full exhibit — the same visual device
# already used for the Constitution's Figure C2, redrawn here under the
# Compendium's own exhibit numbering so the in-image label matches its
# caption rather than reading "AMIU EXHIBIT C2" inside this publication.
# =====================================================================
GOLD_LT2 = "#E4C878"
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
colors_t = [NAVY_DK, NAVY, NAVY_MD, "#345385", "#4C6489", GOLD, GOLD_LT2]
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
signature_frame(fig, 4)
save(fig, "igc_fig4_ladder.png")

# =====================================================================
# FIGURE G5 — The ISLAMIC Framework (full-page infographic), replacing
# the Section 3.2 summary table for the same reason as Figure G4.
# =====================================================================
rows = [
    ("I", "Illumination", "The pursuit of knowledge is an act of worship that illuminates the heart."),
    ("S", "Sanad", "Bound to the Prophetic tradition by an unbroken chain of transmission."),
    ("L", "Love", "The University serves the Ummah with love, particularly the marginalized."),
    ("A", "Access", "Financial capacity shall never be a barrier to knowledge."),
    ("M", "Morality", "Honesty, humility, patience, generosity — the Prophetic example."),
    ("I", "Inquiry", "Intellectual rigor and the pursuit of truth through ijtihād and taḥqīq."),
    ("C", "Calling", "Commitment to da'wah — calling to Allah with wisdom, beauty, and mercy."),
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
            fontweight="bold", color=GOLD_LT2, zorder=4)
    ax.text(19, y + h/2 - h*0.28, meaning, ha="left", va="center", fontsize=9.3,
            color="#DCE3F0", zorder=4, linespacing=1.3)
signature_frame(fig, 5)
save(fig, "igc_fig5_islamic.png")
