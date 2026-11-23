# -*- coding: utf-8 -*-
"""Minority Report, Part 1 (Now Showing No. 8): figures, the two posters and the teaser drawing. Written 13 Nov 2026.
Reads only result files (this folder's results_pit/ and ../A09_Minority_Report_2_Small_Print/results/); computes nothing new
except cumulative growth and the straight cost lines (net = gross - 12 x turnover x cost per trade).
Writes figures/p1_*.png, hero_minority_report_part1*.png and teaser_precogs_part1.png. The old article's figures are untouched."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, Ellipse, Polygon

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10"))
from common import BLUE, GREY, INK, INK2, ORANGE, AQUA, mpl_style  # noqa: E402
from poster import BOLD, DIM, poster  # noqa: E402
from poster import INK as PINK  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FIG = os.path.join(ROOT, "figures")
A31 = os.path.join(ROOT, "..", "A09_Minority_Report_2_Small_Print", "results")
mpl_style(plt)
L4L = json.load(open(os.path.join(ROOT, "results_pit", "costs_like_for_like.json")))
U1 = pd.read_csv(os.path.join(A31, "U1", "scoreboard.csv"), index_col=0)
U2 = pd.read_csv(os.path.join(A31, "U2", "scoreboard.csv"), index_col=0)
SORTS = pd.read_csv(os.path.join(A31, "U1", "simple_sorts.csv"), index_col=0)
G = pd.read_csv(os.path.join(A31, "U1", "gross_monthly.csv"), index_col=0, parse_dates=True)
N = pd.read_csv(os.path.join(A31, "U1", "net_monthly.csv"), index_col=0, parse_dates=True)
sp, sc = L4L["sp500_Ensemble_cost0.10pct"], L4L["smallcap_Ensemble_cost0.50pct"]
NAMES = {"OLS": "OLS", "Ridge": "Ridge", "Lasso": "Lasso", "ElasticNet": "Elastic Net", "RandomForest": "Random forest",
         "GradBoost": "Gradient boosting", "MLP": "Neural net", "kNN": "k-nearest neighbours", "Ensemble": "Ensemble", "Momentum": "12-1 momentum"}
pct = lambda v: f"{v * 100:+.1f}%"

# ---- Figure 1: where to look (same window, each universe at its own cost)
uni = [("S&P 500\n(0.10% per trade)", sp["gross_ann"], sp["net_ann"]),
       ("European blue chips\n(0.15% per trade)", U2.loc["Ensemble", "gross_ann"], U2.loc["Ensemble", "net_ann"]),
       ("US small caps\n(0.50% per trade)", sc["gross_ann"], sc["net_ann"])]
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200); x = np.arange(3); w = 0.36
b1 = ax.bar(x - w / 2, [u[1] * 100 for u in uni], w, color=BLUE, label="before trading costs")
b2 = ax.bar(x + w / 2, [u[2] * 100 for u in uni], w, color=ORANGE, label="after trading costs")
for bars, k in ((b1, 1), (b2, 2)):
    for r, u in zip(bars, uni):
        v = u[k] * 100; ax.text(r.get_x() + r.get_width() / 2, v + (0.5 if v >= 0 else -0.5), pct(u[k]), ha="center", va="bottom" if v >= 0 else "top", fontsize=10.5, color=INK)
ax.axhline(0, color=INK2, lw=0.8); ax.set_xticks(x); ax.set_xticklabels([u[0] for u in uni]); ax.set_ylim(-8, 17.5)
ax.set_ylabel("Return a year, top minus bottom 10%, %"); ax.legend(frameon=False, loc="upper left")
ax.set_title("Where you look: the same eight models, three markets (2017-2026)", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "p1_fig1_where_to_look.png")); plt.close(fig)

# ---- Figure 2: US small caps, every model before and after costs (2004-2026)
order = ["OLS", "Ridge", "Lasso", "ElasticNet", "RandomForest", "GradBoost", "MLP", "kNN", "Ensemble", "Momentum"]
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=200); x = np.arange(len(order)); w = 0.38
ax.bar(x - w / 2, U1.loc[order, "gross_ann"] * 100, w, color=BLUE, label="before costs")
ax.bar(x + w / 2, U1.loc[order, "net_ann"] * 100, w, color=ORANGE, label="after 0.50% per trade")
for i, n in enumerate(order):
    v = U1.loc[n, "net_ann"] * 100; ax.text(i + w / 2, v + (0.4 if v >= 0 else -0.4), f"{v:+.1f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=9, color=INK)
ax.axhline(0, color=INK2, lw=0.8); ax.set_xticks(x); ax.set_xticklabels([NAMES[n] for n in order], rotation=30, ha="right", fontsize=9.5)
ax.set_ylabel("Return a year, %"); ax.set_ylim(-6.5, 20); ax.legend(frameon=False, loc="upper left", ncol=2)
ax.set_title("US small caps 2004-2026: every model earns 12-16% a year, until it has to trade", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "p1_fig2_small_caps_models.png")); plt.close(fig)

# ---- Figure 3: the bill (growth of 1, small-cap ensemble before and after costs)
cg = (1 + G["Ensemble"].fillna(0)).cumprod(); cn = (1 + N["Ensemble"].fillna(0)).cumprod()
for c in (cg, cn): c.index = c.index + pd.offsets.MonthEnd(1)       # shown at the end of the return month
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.plot(cg.index, cg, color=BLUE, lw=2.2, label=f"before costs (ends at {cg.iloc[-1]:.1f})")
ax.plot(cn.index, cn, color=ORANGE, lw=2.2, label=f"after 0.50% per trade (ends at {cn.iloc[-1]:.1f})")
ax.set_yscale("log"); ax.set_yticks([1, 2, 5, 10, 20]); ax.set_yticklabels(["1", "2", "5", "10", "20"]); ax.axhline(1, color=INK2, lw=0.8)
ax.set_ylabel("Growth of 1, long-short, log scale"); ax.legend(frameon=False, loc="upper left")
ax.set_title(f"The bill: {U1.loc['Ensemble', 'turnover_m']:.0%} turnover a month takes {12 * U1.loc['Ensemble', 'turnover_m'] * 0.005:.1%} a year", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "p1_fig3_the_bill.png")); plt.close(fig)

# ---- Figure 4: what is left at each cost per trade (straight lines: gross - 12 x turnover x cost)
gp = SORTS.loc["Profitability (GP/A)"]; en = U1.loc["Ensemble"]; c = np.linspace(0, 0.01, 101)
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
for r, col, lab in ((en, BLUE, f"Machine-learning ensemble ({en.turnover_m:.0%} turnover a month)"), (gp, AQUA, f"Gross profitability sort ({gp.turnover_m:.0%} turnover a month)")):
    ax.plot(c * 100, (r.gross_ann - 12 * r.turnover_m * c) * 100, color=col, lw=2.4, label=lab)
ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0.5, color=INK2, lw=0.8, ls=":")
ax.text(0.505, -5.2, "0.50%: the registered cost", fontsize=9.5, color=INK2)
ax.plot([en.breakeven_cost * 100], [0], "o", color=BLUE); ax.text(en.breakeven_cost * 100 + 0.01, 0.7, f"break-even {en.breakeven_cost:.2%}", fontsize=9.5, color=BLUE)
ax.plot([0.5, 0.5], [en.net_ann * 100, gp.net_ann * 100], "o", color=INK, ms=4)
ax.text(0.49, en.net_ann * 100 - 0.2, pct(en.net_ann), ha="right", va="top", fontsize=10, color=BLUE); ax.text(0.49, gp.net_ann * 100 + 0.3, pct(gp.net_ann), ha="right", va="bottom", fontsize=10, color=AQUA)
ax.set_xlim(0, 1.0); ax.set_ylim(-6, 16.5); ax.set_xlabel("Cost per trade (one way), %"); ax.set_ylabel("Return a year after costs, %"); ax.legend(frameon=False, loc="upper right")
ax.set_title("US small caps 2004-2026: the slow signal keeps more of less", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "p1_fig4_cost_per_trade.png")); plt.close(fig)

# ---- Posters (No. 8). The article poster answers; the teaser poster asks.
GOLDC = "#f5b301"
STARS = "STARRING  A RANDOM FOREST · BOOSTING · A NEURAL NET · k-NN · FOUR REGRESSIONS\nAND THE TRADING BILL AS THE VILLAIN"


def draw(ax, acc):
    lab = ["S&P 500", "EUROPE", "US SMALL CAPS"]; x = np.arange(3); w = 0.36
    ax.bar(x - w / 2, [u[1] * 100 for u in uni], w, color=acc); ax.bar(x + w / 2, [u[2] * 100 for u in uni], w, color=GOLDC)
    for i, u in enumerate(uni):
        for k, dx, col in ((1, -w / 2, acc), (2, w / 2, GOLDC)):
            v = u[k] * 100; ax.text(i + dx, v + (0.5 if v >= 0 else -0.5), f"{v:+.1f}%", ha="center", va="bottom" if v >= 0 else "top", color=col, fontproperties=BOLD, fontsize=17)
    ax.axhline(0, color=DIM, lw=1.2); ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=16); ax.set_yticks([]); ax.grid(False); ax.set_ylim(-9, 19)
    ax.text(-0.45, 17.6, "BEFORE COSTS", color=acc, fontproperties=BOLD, fontsize=17); ax.text(-0.45, 15.4, "AFTER COSTS", color=GOLDC, fontproperties=BOLD, fontsize=17)
    ax.text(-0.45, 13.4, "a year, 2017-2026", color=DIM, fontsize=13)


poster(os.path.join(FIG, "hero_minority_report_part1.png"), 8, "MINORITY\nREPORT", "Part 1: Where to look, and what it costs", draw, STARS,
       f"RATED  0 OF 9  ·  SMALL CAPS TRADE {en.turnover_m:.0%} OF CAPITAL A MONTH", "IN CINEMAS 24 NOVEMBER 2026", accent="#3987e5")


def draw_teaser(ax, acc):
    o = [n for n in order if n not in ("Ensemble", "Momentum")]
    ax.barh(range(len(o)), U1.loc[o, "gross_ann"] * 100, color=acc, height=0.6)
    ax.set_yticks(range(len(o))); ax.set_yticklabels([NAMES[n] for n in o], fontsize=13.5); ax.set_xlim(0, 27); ax.set_xticks([]); ax.grid(False); ax.invert_yaxis()
    ax.text(26.8, -0.75, "US small caps, a year, before costs", color=DIM, fontsize=12, ha="right")
    ax.text(22, 3.5, "WHAT IS LEFT\nAFTER THE\nTRADING BILL?", ha="center", va="center", color=PINK, fontproperties=BOLD, fontsize=21)


poster(os.path.join(FIG, "hero_minority_report_part1_teaser.png"), 8, "MINORITY\nREPORT", "Part 1: Eight machines. Three markets. One bill.", draw_teaser, STARS,
       "RATED  NINE PRE-REGISTERED TESTS  ·  THE VERDICT IS IN THE ARTICLE", "IN CINEMAS 24 NOVEMBER 2026", accent="#3987e5", ax_left=0.30)

# ---- Teaser drawing: the three precogs' crystal balls with Part 1's questions (original drawing)
INKD, INK2D, ACC, GOLD, BG, POOL = "#0b0b0b", "#52514e", "#2a78d6", "#c9a227", "#fcfcfb", "#dfeaf6"
fig, ax = plt.subplots(figsize=(4.2, 5.0), dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
ax.text(5.0, 11.2, "THE PRECOGS", ha="center", va="center", fontsize=15, fontweight="bold", color=INKD, family="DejaVu Sans")
ax.add_patch(Ellipse((5.0, 2.2), 9.2, 1.6, fc=POOL, ec=INKD, lw=1.4))
for i, (n, lab) in enumerate([("1", "large or\nsmall?"), ("2", "what is\nleft?"), ("3", "which\none rule?")]):
    cx, cy = 1.9 + i * 3.1, 6.6 + (0.5 if i == 1 else 0)
    ax.add_patch(Polygon([[cx - 0.9, cy - 2.6], [cx + 0.9, cy - 2.6], [cx + 0.5, cy - 1.45], [cx - 0.5, cy - 1.45]], closed=True, fc="#3b3a38", ec=INKD, lw=1.3))
    ax.add_patch(Circle((cx, cy), 1.35, fc="white", ec=INKD, lw=1.6))
    ax.add_patch(Ellipse((cx - 0.45, cy + 0.6), 0.55, 0.3, angle=30, fc="#eef3fa", ec="none"))
    ax.add_patch(Circle((cx, cy + 0.8), 0.26, fc=GOLD, ec=INKD, lw=1.0)); ax.text(cx, cy + 0.8, n, ha="center", va="center", fontsize=8.5, fontweight="bold", color=INKD)
    ax.text(cx, cy - 0.2, lab, ha="center", va="center", fontsize=8.2, fontweight="bold", color=ACC, linespacing=1.05)
    ax.plot([cx, cx], [cy - 2.6, 2.9], color=INK2D, lw=0.8, ls=(0, (2, 2)))
ax.text(5.0, 0.55, "Three questions. The answers are in the article", ha="center", va="center", fontsize=8, color=INK2D)
fig.savefig(os.path.join(FIG, "teaser_precogs_part1.png"), facecolor=BG, bbox_inches="tight", pad_inches=0.05); plt.close(fig)
print("Part 1 figures, posters and teaser drawing written")
