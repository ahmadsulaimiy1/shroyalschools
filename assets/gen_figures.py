#!/usr/bin/env python3
"""Generate branded figures for the AMIU Strategic Implementation Blueprint 2028-2050."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
import matplotlib.font_manager as fm
import numpy as np
import os

OUT = "/home/user/shroyalschools/assets/figures"
os.makedirs(OUT, exist_ok=True)

# ---- Brand palette ----
NAVY      = "#122A4E"
NAVY_DK   = "#0A1830"
NAVY_MD   = "#1F3A66"
GOLD      = "#C69A3A"
GOLD_LT   = "#E4C878"
PAPER     = "#FFFFFF"
BG_TINT   = "#F3F5F9"
GREY      = "#6B7280"
TEXT      = "#152238"
PALETTE7  = ["#122A4E", "#1F3A66", "#345385", "#C69A3A", "#8C97AB", "#4C6489", "#D9B36A"]

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "text.color": TEXT,
    "axes.edgecolor": "#D8DCE5",
    "axes.labelcolor": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "figure.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "savefig.facecolor": PAPER,
})

def save(fig, name, w=None, h=None):
    fig.savefig(os.path.join(OUT, name), dpi=220, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("saved", name)

# ---------------------------------------------------------------------------
# Signature exhibit-plate frame — the one recurring device applied to every
# figure so an AMIU exhibit is recognisable independent of chart type.
# Titles live in the document's own caption typography, not inside the image;
# the frame carries only a small brand kicker, corner marks and a micro-footer.
# ---------------------------------------------------------------------------
ROMAN10 = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

def _corner(fig, x, y, hsign, vsign, length=0.022, color=GOLD, lw=1.5):
    fig.add_artist(plt.Line2D([x, x + hsign * length], [y, y], transform=fig.transFigure,
                               color=color, linewidth=lw, solid_capstyle="butt", zorder=10))
    fig.add_artist(plt.Line2D([x, x], [y, y + vsign * length], transform=fig.transFigure,
                               color=color, linewidth=lw, solid_capstyle="butt", zorder=10))

def signature_frame(fig, exhibit_no):
    numeral = ROMAN10[exhibit_no - 1]
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.975, 0.975], transform=fig.transFigure,
                               color=GOLD, linewidth=1.4, solid_capstyle="butt", zorder=10))
    fig.text(0.04, 0.983, f"AMIU EXHIBIT {numeral}", transform=fig.transFigure,
             fontsize=8.5, color=GOLD, fontweight="bold", ha="left", va="bottom")
    fig.text(0.96, 0.983, "STRATEGIC IMPLEMENTATION BLUEPRINT", transform=fig.transFigure,
             fontsize=7.5, color=GREY, ha="right", va="bottom")
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.028, 0.028], transform=fig.transFigure,
                               color=NAVY, linewidth=0.8, zorder=10))
    fig.text(0.04, 0.018, "AL-MULK INTERNATIONAL UNIVERSITY", transform=fig.transFigure,
             fontsize=7, color=GREY, ha="left", va="top")
    fig.text(0.96, 0.018, f"EXHIBIT {numeral} OF 10", transform=fig.transFigure,
             fontsize=7, color=GREY, ha="right", va="top")
    _corner(fig, 0.025, 0.945, +1, -1)
    _corner(fig, 0.975, 0.058, -1, +1)

# =====================================================================
# FIGURE 1 — Revenue Allocation Framework (donut)
# =====================================================================
labels = ["Liquidity Reserve\n35%", "Payroll\n20%", "Waqf & Stakeholder\nReserve 20%",
          "Marketing &\nAcquisition 10%", "Operating\nExpenses 5%",
          "LMS & Technology\nInfrastructure 5%", "Da'wah & Community\nOutreach 5%"]
sizes = [35, 20, 20, 10, 5, 5, 5]
colors = [NAVY, NAVY_MD, GOLD, "#345385", "#8C97AB", "#4C6489", "#D9B36A"]

fig, ax = plt.subplots(figsize=(9, 7.2))
wedges, _ = ax.pie(sizes, colors=colors, startangle=90, counterclock=False,
                    wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2.5))
ax.text(0, 0.06, "100%", ha="center", va="center", fontsize=22, fontweight="bold", color=NAVY)
ax.text(0, -0.14, "Zero Unallocated\nResidual", ha="center", va="center", fontsize=10, color=GREY)

# legend with values, executive style
legend_names = ["Liquidity Reserve", "Payroll", "Waqf & Stakeholder Reserve",
                 "Marketing & Student Acquisition", "Operating Expenses",
                 "LMS & Technology Infrastructure", "Da'wah & Community Outreach"]
legend_labels = [f"{n} — {s}%" for n, s in zip(legend_names, sizes)]
ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1.02, 0.5),
          frameon=False, fontsize=11, labelspacing=1.3, handlelength=1.4, handleheight=1.4)
ax.set(aspect="equal")
signature_frame(fig, 8)
save(fig, "fig01_revenue_allocation.png")

# =====================================================================
# FIGURE 2 — Ten-Year Enrollment Growth (bar)
# =====================================================================
years = list(range(1, 11))
enrol = [347, 896, 1606, 2468, 3493, 4691, 6051, 7559, 9216, 11021]
cal_years = [2028+i for i in range(10)]

fig, ax = plt.subplots(figsize=(10.5, 5.6))
bars = ax.bar(years, enrol, color=NAVY, width=0.62, zorder=3)
for i in [0, 4, 9]:
    bars[i].set_color(GOLD)
for x, y in zip(years, enrol):
    ax.text(x, y + 220, f"{y:,}", ha="center", fontsize=9.5, color=NAVY, fontweight="bold")
ax.set_xticks(years)
ax.set_xticklabels([f"Yr {y}\n{c}" for y, c in zip(years, cal_years)], fontsize=9)
ax.set_ylabel("Total Active Students", fontsize=11)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.yaxis.grid(True, color="#E5E8EF", zorder=0)
ax.set_ylim(0, 12500)
ax.tick_params(left=False)
signature_frame(fig, 1)
save(fig, "fig02_enrollment_growth.png")

# =====================================================================
# FIGURE 3 — Ten-Year Gross Revenue Growth (bar + cumulative line)
# =====================================================================
revenue = [224747, 451397, 672153, 1034978, 1290784, 1567214, 2191110, 2530061, 2876197, 3830549]
cumulative = np.cumsum(revenue)

fig, ax1 = plt.subplots(figsize=(10.5, 5.8))
bars = ax1.bar(years, [r/1e6 for r in revenue], color=NAVY_MD, width=0.55, zorder=3, label="Annual Gross Revenue")
ax1.set_ylabel("Annual Gross Revenue (US$ millions)", fontsize=10.5, color=NAVY)
ax1.set_xticks(years)
ax1.set_xticklabels([f"Yr {y}\n{c}" for y, c in zip(years, cal_years)], fontsize=9)
ax1.spines[["top", "left"]].set_visible(False)
ax1.tick_params(left=False)

ax1.set_ylim(0, 5.2)

ax2 = ax1.twinx()
ax2.plot(years, [c/1e6 for c in cumulative], color=GOLD, marker="o", markersize=5,
         linewidth=2.6, zorder=4, label="Cumulative Gross Revenue")
ax2.set_ylabel("Cumulative Gross Revenue (US$ millions)", fontsize=10.5, color="#8A6A1E")
ax2.spines[["top"]].set_visible(False)
ax2.set_ylim(0, 18.5)
ax2.text(9.55, cumulative[-1]/1e6 + 0.9, f"${cumulative[-1]/1e6:.1f}M cumulative",
          ha="right", fontsize=9.5, color="#8A6A1E", fontweight="bold")
ax1.text(9.55, revenue[-1]/1e6 + 0.28, f"${revenue[-1]/1e6:.2f}M annual",
          ha="right", fontsize=9.5, color=NAVY, fontweight="bold")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=False, fontsize=10)
signature_frame(fig, 2)
save(fig, "fig03_revenue_growth.png")

# =====================================================================
# FIGURE 4 — Twenty-Year Revenue Trajectory with era shading
# =====================================================================
yrs20 = list(range(1, 21))
cal20 = [2028+i for i in range(20)]
rev20 = revenue + [8357562/1e6*1e6, 14625734, 22669888, 32191241, 43136263,
                    54800000, 63000000, 74000000, 86100000, 93871577]
rev20_m = [r/1e6 for r in rev20]

fig, ax = plt.subplots(figsize=(11, 5.8))
ax.axvspan(0.4, 10.5, color=BG_TINT, zorder=0)
ax.axvspan(10.5, 20.6, color="#FBF3E1", zorder=0)
ax.plot(yrs20, rev20_m, color=NAVY, linewidth=2.6, marker="o", markersize=4, zorder=3)
ax.axvline(10.5, color=GREY, linestyle="--", linewidth=1)
ax.text(5.4, max(rev20_m)*0.94, "ERA I\nFounding Decade\n2028–2037", ha="center", fontsize=10,
        color=NAVY, fontweight="bold")
ax.text(15.5, max(rev20_m)*0.94, "ERA II\nSecular Expansion\n2038–2047", ha="center", fontsize=10,
        color="#8A6A1E", fontweight="bold")
ax.set_xticks(yrs20[::2])
ax.set_xticklabels([f"{c}" for c in cal20[::2]], fontsize=9, rotation=0)
ax.set_ylabel("Illustrative Gross Revenue (US$ millions)", fontsize=10.5)
ax.spines[["top", "right"]].set_visible(False)
ax.annotate(f"${rev20_m[-1]:.1f}M", xy=(20, rev20_m[-1]), xytext=(18.3, rev20_m[-1]-6),
            fontsize=10, color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
ax.set_xlim(0.4, 20.6)
signature_frame(fig, 10)
save(fig, "fig04_twenty_year_trajectory.png")

# =====================================================================
# FIGURE 5 — Waqf & Stakeholder Reserve Distribution
# =====================================================================
fig, ax = plt.subplots(figsize=(9.5, 5.8))
cats = ["Islamic Schools &\nMosque Support", "Widows & Orphans\nSponsorship",
        "Waqf Scholarship\nBlock", "Nigeria Mega-University\nReserve", "Emergency Relief\n& Contingency"]
vals = [25, 25, 20, 20, 10]
tenyr = [416729, 416729, 333383, 333383, 166692]
colors5 = [NAVY, NAVY_MD, GOLD, "#4C6489", "#8C97AB"]
y = np.arange(len(cats))
bars = ax.barh(y, vals, color=colors5, height=0.58, zorder=3)
for i, (v, d) in enumerate(zip(vals, tenyr)):
    ax.text(v + 0.8, i, f"{v}%   ·   ${d:,} (10-yr)", va="center", fontsize=10, color=NAVY, fontweight="bold")
ax.set_yticks(y)
ax.set_yticklabels(cats, fontsize=10.5)
ax.invert_yaxis()
ax.set_xlim(0, 42)
ax.set_xlabel("Share of the Distributed Half of the Waqf & Stakeholder Reserve (20% of Gross Revenue)", fontsize=9.5)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.xaxis.grid(True, color="#E5E8EF", zorder=0)
ax.tick_params(left=False)
signature_frame(fig, 7)
save(fig, "fig05_waqf_distribution.png")

# =====================================================================
# FIGURE 6 — Governance Organisational Chart (diagram)
# =====================================================================
fig, ax = plt.subplots(figsize=(11.5, 9.0))
ax.set_xlim(0, 100); ax.set_ylim(0, 99); ax.axis("off")

def box(x, y, w, h, text, fc=NAVY, tc="white", fs=9.5, bold=True, ec="none", lw=0):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.35,rounding_size=1.6",
                        fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", zorder=4, linespacing=1.35)

def link(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color="#9AA5B8", lw=1.4, zorder=1)

# Top: Board & Senate
box(6, 84, 40, 11, "BOARD OF TRUSTEES\nStrategy · Finance · Legal · Tuition ·\nCommercial Engine Oversight", fc=NAVY_DK, fs=9.5)
box(54, 84, 40, 11, "UNIVERSITY SENATE — 18 SEATS\nSupreme Academic Authority", fc=NAVY_DK, fs=9.5)
link(26, 84, 74, 84)  # bicameral link

# Board committees
box(2, 66, 22, 11, "Audit & Risk\nCommittee", fc=NAVY_MD, fs=8.7)
box(26, 66, 22, 11, "Waqf & Endowment\nBoard (fiduciary)", fc=NAVY_MD, fs=8.7)
link(13, 84, 13, 77); link(37, 84, 37, 77)

# Senate groups
box(52, 66, 21, 11, "Group I\nExecutive Leadership\n(3 seats)", fc=GOLD, tc=NAVY_DK, fs=8.4)
box(75, 66, 21, 11, "Group II\nAcademic Operations\n(5 seats)", fc=GOLD, tc=NAVY_DK, fs=8.4)
link(60, 84, 62, 77); link(70, 84, 85, 77)

box(52, 50, 21, 11, "Group III\nFrontline Instructional\nMgmt (6 seats)", fc=GOLD, tc=NAVY_DK, fs=8.4)
box(75, 50, 21, 11, "Group IV\nInstitutional & Digital\nStrategy (4 seats,\nincl. 3 independent)", fc=GOLD_LT, tc=NAVY_DK, fs=8.2)
link(62, 66, 62, 61); link(85, 66, 85, 61)

# Independent safeguard box
box(2, 50, 22, 11, "Independent\nSharī'ah Advisory\nBoard", fc=NAVY_MD, fs=8.7)
link(37, 66, 13, 55.5)

# Bottom operational layer
box(20, 30, 26, 11, "College Deans (6)\nDepartment Heads (6)", fc="#4C6489", fs=8.7)
box(50, 30, 26, 11, "DVC Academic Affairs /\nDVC Admin & Finance", fc="#4C6489", fs=8.7)
box(80, 30, 18, 11, "University\nRegistrar &\nLibrarian", fc="#4C6489", fs=8.4)
link(62, 50, 62, 41); link(85, 50, 89, 41); link(85, 61, 33, 41)

# Faculty
box(35, 12, 42, 11, "Faculty — Adjunct → Assistant → Associate → Full Professor\n(Honoraria-Based, 40% of Payroll)", fc=BG_TINT, tc=NAVY, fs=8.6, ec=NAVY, lw=1.1)
link(33, 30, 56, 23); link(62, 30, 56, 23)

signature_frame(fig, 3)
save(fig, "fig06_governance_orgchart.png")

# =====================================================================
# FIGURE 7 — Seven-Tier Academic Ladder (stacked pyramid)
# =====================================================================
tiers = [
    ("VII", "Post-Doctoral Research Fellowship", "Non-credit · Launch Yr 6 (2033)", 4),
    ("VI", "Doctor of Philosophy", "60 CH · Launch Yr 3 (2030)", 6),
    ("V", "Master of Arts", "45 CH · Launch Yr 2 (2029)", 8),
    ("IV", "Higher Postgraduate Diploma", "30 CH · Launch Yr 2 (2029)", 6),
    ("III", "Bachelor of Arts", "120 CH · Launch Yr 1 (2028)", 14),
    ("II", "Associate Degree", "60 CH · Launch Yr 1 (2028)", 15),
    ("I", "Undergraduate Diploma", "45 CH · Launch Yr 1 (2028)", 18),
]
fig, ax = plt.subplots(figsize=(11, 8.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 95); ax.axis("off")
n = len(tiers)
top, bottom, gap = 92, 6, 1.6
h = (top - bottom - gap*(n-1)) / n
colors_t = [NAVY_DK, NAVY, NAVY_MD, "#345385", "#4C6489", GOLD, GOLD_LT]
for i, (roman, name, meta, progs) in enumerate(tiers):
    y = top - (i+1)*h - i*gap
    width = 92 - i*8.6   # widening toward the base
    x0 = 50 - width/2
    box(x0, y, width, h, "", fc=colors_t[i], fs=1)
    ax.text(x0 + 6, y + h/2, roman, ha="center", va="center", fontsize=13, fontweight="bold",
            color=(NAVY_DK if i >= 5 else "white"))
    ax.text(x0 + width/2 + 3, y + h/2 + h*0.16, name, ha="center", va="center", fontsize=10.6,
            fontweight="bold", color=(NAVY_DK if i >= 5 else "white"))
    ax.text(x0 + width/2 + 3, y + h/2 - h*0.32, f"{meta} · {progs} named programs", ha="center", va="center",
            fontsize=8.6, color=(NAVY_DK if i >= 5 else "#DCE3F0"))
signature_frame(fig, 4)
save(fig, "fig07_seven_tier_ladder.png")

# =====================================================================
# FIGURE 8 — Capital Firewall Structure
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 7.2))
ax.set_xlim(0, 100); ax.set_ylim(0, 80); ax.axis("off")
box(4, 24, 42, 50, "", fc=BG_TINT, ec=NAVY, lw=1.6, fs=1)
box(54, 24, 42, 50, "", fc="#FBF3E1", ec=GOLD, lw=1.6, fs=1)
ax.text(25, 68, "AL-MULK INTERNATIONAL\nUNIVERSITY", ha="center", va="center", fontsize=12, fontweight="bold", color=NAVY)
ax.text(25, 60.5, "(Academic — 501(c)(3) Nonprofit)", ha="center", fontsize=9.2, color=NAVY, style="italic")
for i, t in enumerate(["100% tuition & ancillary revenue", "Separate audited accounts",
                        "Entirely separate bank accounts", "Operates per fixed allocation\nframework only",
                        "No investor obligations"]):
    ax.text(25, 53.5 - i*6.6, "• " + t, ha="center", fontsize=8.8, color=NAVY)

ax.text(75, 68, "AMIU GLOBAL SERVICES LLC", ha="center", va="center", fontsize=12, fontweight="bold", color="#8A6A1E")
ax.text(75, 60.5, "(Commercial Engine — Texas LLC)", ha="center", fontsize=9.2, color="#8A6A1E", style="italic")
for i, t in enumerate(["Independently raised investor\nsubscriptions", "Separate audited accounts",
                        "Entirely separate bank accounts", "Gate A / B / C due-diligence\nclearance required",
                        "No claim on University tuition"]):
    ax.text(75, 53.5 - i*6.6, "• " + t, ha="center", fontsize=8.8, color="#5C4A17")

# Firewall bar (two lines, distinct sizes, generous width margin)
box(2, 6, 96, 13, "", fc=NAVY_DK, fs=1)
ax.text(50, 14.4, "PERMANENT FIREWALL", ha="center", va="center", fontsize=11,
        fontweight="bold", color="white")
ax.text(50, 9.6, "No tuition revenue may ever fund an investor return, dividend, buyback, or redemption",
        ha="center", va="center", fontsize=8.8, color="#DCE3F0")
ax.annotate("", xy=(52, 48), xytext=(48, 48),
            arrowprops=dict(arrowstyle="-|>", color="#B23B3B", lw=2.4, mutation_scale=18))
ax.annotate("", xy=(48, 40), xytext=(52, 40),
            arrowprops=dict(arrowstyle="-|>", color="#B23B3B", lw=2.4, mutation_scale=18))
ax.text(50, 44, "NO\nFLOW", ha="center", va="center", fontsize=9, fontweight="bold", color="#B23B3B")

signature_frame(fig, 9)
save(fig, "fig08_capital_firewall.png")

# =====================================================================
# FIGURE 9 — Student Journey Map (flowchart)
# =====================================================================
stages = ["Inquiry", "Application", "Tier\nPlacement", "Admission\nDecision",
          "Enrollment &\nOrientation", "Ladder\nProgression", "Graduation", "Alumni /\nRe-Stacking"]
fig, ax = plt.subplots(figsize=(12.5, 4.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 27); ax.axis("off")
n = len(stages)
w = 10.6; gap = (100 - n*w) / (n+1)
xs = [gap + i*(w+gap) for i in range(n)]
for i, (x, s) in enumerate(zip(xs, stages)):
    fc = GOLD if i in (5,) else (NAVY if i % 2 == 0 else NAVY_MD)
    box(x, 12, w, 12, s, fc=fc, tc=(NAVY_DK if i == 5 else "white"), fs=8.8)
    if i < n - 1:
        ax.annotate("", xy=(x + w + gap - 0.6, 18), xytext=(x + w + 0.6, 18),
                    arrowprops=dict(arrowstyle="-|>", color="#9AA5B8", lw=1.6, mutation_scale=14))
ax.text(50, 3, "Digital self-service by design — human touch reserved for tier disputes, Fast-Track review, and Waqf adjudication",
        ha="center", fontsize=9, color=GREY)
signature_frame(fig, 5)
save(fig, "fig09_student_journey.png")

# =====================================================================
# FIGURE 10 — Accreditation & Expansion Roadmap Timeline
# =====================================================================
events = [
    (2028, "Academic Launch\n& Formation", 1),
    (2029, "CPD Accreditation ·\nGambia Stage 3 Begins", -1),
    (2030, "ISO 21001 ·\nPhD Tier Launch", 1),
    (2031, "Gambia NAQAA\nAccredited", -1),
    (2033, "Post-Doctoral\nFellowship Launch", 1),
    (2037, "Founding Decade Closes ·\nNigeria Charter Filed", -1),
    (2038, "Secular Schools Launch\n(28 Programs)", 1),
    (2039, "Texas Secular\nAccreditation Targeted", -1),
    (2040, "First Gulf Ministry\nRecognition Targeted", 1),
    (2047, "Twenty-Year Horizon\n$90M–$150M Target", -1),
]
# Use evenly-spaced categorical x-positions (not true calendar scale) so close
# milestones never collide; the true year is printed with each label instead.
n_ev = len(events)
xpos = list(range(n_ev))
fig, ax = plt.subplots(figsize=(15, 6.6))
ax.set_xlim(-0.6, n_ev - 0.4); ax.set_ylim(-3.0, 3.0); ax.axis("off")
ax.plot([xpos[0] - 0.35, xpos[-1] + 0.35], [0, 0], color=NAVY, lw=2.6, zorder=2, solid_capstyle="round")
for x, (yr, label, side) in zip(xpos, events):
    ax.plot([x], [0], marker="o", markersize=11, color=GOLD, zorder=4,
            markeredgecolor=NAVY_DK, markeredgewidth=1.3)
    ytxt = 1.3 if side == 1 else -1.3
    va = "bottom" if side == 1 else "top"
    ax.plot([x, x], [0, ytxt * 0.5], color="#9AA5B8", lw=1, zorder=1)
    ax.text(x, ytxt, f"{yr}", ha="center", va=va, fontsize=11.5, color=GOLD if False else "#8A6A1E",
            fontweight="bold")
    ax.text(x, ytxt + (0.75 if side == 1 else -0.75), label, ha="center", va=va, fontsize=9,
            color=NAVY, fontweight="bold", linespacing=1.35)
signature_frame(fig, 6)
save(fig, "fig10_accreditation_roadmap.png")

print("ALL FIGURES GENERATED")
