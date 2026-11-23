# -*- coding: utf-8 -*-
"""A06 figures + hero card (film)."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from common import BLUE, GREY, INK, INK2, ORANGE, mpl_style  # noqa: E402
from poster import BOLD, DIM, poster  # noqa: E402
from poster import INK as PINK  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES, FIG = os.path.join(ROOT, "results"), os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True); mpl_style(plt)
# 23 Oct 2026 (stress test): figures and posters read the numbers of record, the corrected universe (results_pit/:
# actual S&P 500 members at each date). The registered-universe numbers stay in the article's tables.
PIT = os.path.join(ROOT, "results_pit")
S = json.load(open(os.path.join(PIT, "summary.json")))
B = pd.read_csv(os.path.join(PIT, "scoreboard.csv"), index_col=0)
LS = pd.read_csv(os.path.join(PIT, "longshort_monthly.csv"), index_col=0, parse_dates=True)
H = 57   # halves: formation months Jan 2017-Sep 2021 (57) and Oct 2021-Jul 2026 (58), as in run_ml.py
order = B.sharpe.sort_values().index
col = lambda n: ORANGE if n == "Momentum" else (BLUE if n == "Ensemble" else GREY)

fig, ax = plt.subplots(figsize=(10, 4.8), dpi=200)
ax.barh(range(len(order)), B.loc[order, "sharpe"], color=[col(n) for n in order], height=0.62)
for i, n in enumerate(order):
    v = B.loc[n, "sharpe"]; ax.text(max(v, 0) + 0.01, i, f"{v:.2f}  (t {B.loc[n, 'nw_t']:.1f})", va="center", fontsize=9.5)
ax.set_yticks(range(len(order))); ax.set_yticklabels(order); ax.set_xlim(-0.32, 0.45); ax.axvline(0, color=INK2, lw=0.8)
ax.set_xlabel("Annualised Sharpe of the top-minus-bottom decile, out of sample 2017-2026")
ax.set_title("Actual index members: eight machines and a 1993 rule, nobody clears the bar", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_scoreboard.png")); plt.close(fig)

cum = (1 + LS[["Ensemble", "MLP", "Momentum"]].fillna(0)).cumprod()
cum.index = cum.index + pd.offsets.MonthEnd(1)
fig, ax = plt.subplots(figsize=(10, 4.4), dpi=200)
for n, c, lw in (("Ensemble", BLUE, 2.4), ("MLP", GREY, 1.6), ("Momentum", ORANGE, 2.0)):
    ax.plot(cum.index, cum[n], color=c, lw=lw, label=n)
ax.axhline(1, color=INK2, lw=0.8); ax.legend(frameon=False, loc="upper left")
ax.axvline(LS.index[H - 1] + pd.offsets.MonthEnd(1), color=INK2, lw=0.8, ls=":")   # end of the return month of the last first-half portfolio
ax.set_ylabel("Growth of $1, long-short (return month)")
ax.set_title("Brilliant until 2021, then not (actual index members)", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_cumulative.png")); plt.close(fig)

nm = [n for n in B.index]
fig, ax = plt.subplots(figsize=(10, 4.4), dpi=200)
x = np.arange(len(nm)); w = 0.38
ax.bar(x - w / 2, B.loc[nm, "sharpe_h1"], w, color=GREY, label="portfolios formed Jan 2017 to Sep 2021")
ax.bar(x + w / 2, B.loc[nm, "sharpe_h2"], w, color=BLUE, label="formed Oct 2021 to Jul 2026")
ax.axhline(0, color=INK2, lw=0.8); ax.set_xticks(x); ax.set_xticklabels(nm, rotation=30, ha="right", fontsize=9.5)
ax.set_ylabel("Sharpe ratio"); ax.legend(frameon=False)
ax.set_title("On the actual index members all 8 ML models flipped sign; momentum did the opposite", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_halves.png")); plt.close(fig)


def draw(ax, acc):
    ks = [n for n in B.index if n != "Ensemble"]
    h1, h2 = B.loc[ks, "sharpe_h1"], B.loc[ks, "sharpe_h2"]
    for i, n in enumerate(ks):
        c = GOLDC if n == "Momentum" else acc
        ax.annotate("", xy=(1, h2[n]), xytext=(0, h1[n]), arrowprops=dict(arrowstyle="-|>", color=c, lw=3 if n == "Momentum" else 2, mutation_scale=22))
    ax.text(0.0, 1.12, "2017 → Sep 2021", color=DIM, fontsize=17, ha="center"); ax.text(1.0, 1.12, "Oct 2021 → 2026", color=DIM, fontsize=17, ha="center")
    ax.text(0.5, 0.78, "8 ML MODELS", color=acc, fontproperties=BOLD, fontsize=26, ha="center")
    ax.text(0.83, 0.5, "MOMENTUM", color=GOLDC, fontproperties=BOLD, fontsize=22, ha="center")
    ax.axhline(0, color=DIM, lw=1.2); ax.set_xlim(-0.25, 1.25); ax.set_ylim(-0.85, 1.25); ax.set_xticks([]); ax.set_yticks([-0.5, 0, 0.5]); ax.grid(False)
    ax.set_yticklabels(["-0.5", "0", "0.5"], fontsize=14); ax.text(-0.22, 0.95, "Sharpe", color=DIM, fontsize=14)


GOLDC = "#f5b301"
poster(os.path.join(FIG, "hero_minority_report.png"), 6, "MINORITY\nREPORT", "The machines saw the past. Then the list changed.", draw,
       "STARRING  A RANDOM FOREST · BOOSTING · A NEURAL NET · k-NN · FOUR REGRESSIONS\nAND 12-1 MOMENTUM (1993) AS THE OLD DETECTIVE",
       f"RATED  0 OF 3  ·  ENSEMBLE t = {S['A06-1']['t']:.2f}  ·  DEFLATED SHARPE {S['A06-3']['dsr']:.2f}", "IN CINEMAS 10 NOVEMBER 2026", accent="#3987e5")


# 23 Oct 2026 (click teaser, as A04/A05): a teaser version of the poster that asks instead of answering.
# First-list Sharpe ratios only, "at first sight": no t, no deflated Sharpe, no verdict.
R0 = pd.read_csv(os.path.join(RES, "scoreboard.csv"), index_col=0)


def draw_teaser(ax, acc):
    o = R0.sharpe.sort_values().index
    ax.barh(range(len(o)), R0.loc[o, "sharpe"], color=[GOLDC if n == "Momentum" else acc for n in o], height=0.6)
    ax.set_yticks(range(len(o))); ax.set_yticklabels(o, fontsize=13.5); ax.set_xlim(0, 0.75); ax.set_xticks([]); ax.grid(False)
    ax.text(0.74, len(o) - 0.4, "Sharpe, first stock list (at first sight)", color=DIM, fontsize=12, ha="right")
    ax.text(0.56, 2.0, "SEEING THE\nFUTURE?", ha="center", va="center", color=PINK, fontproperties=BOLD, fontsize=24)


poster(os.path.join(FIG, "hero_minority_report_teaser.png"), 6, "MINORITY\nREPORT", "Eight machines. One rule from 1993.", draw_teaser,
       "STARRING  A RANDOM FOREST · BOOSTING · A NEURAL NET · k-NN · FOUR REGRESSIONS\nAND 12-1 MOMENTUM (1993) AS THE OLD DETECTIVE",
       "RATED  THREE PRE-REGISTERED TESTS  ·  THE VERDICT IS IN THE ARTICLE", "IN CINEMAS 10 NOVEMBER 2026", accent="#3987e5", ax_left=0.24)
print("figures and posters written")
