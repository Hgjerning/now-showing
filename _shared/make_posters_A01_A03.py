import os
# -*- coding: utf-8 -*-
"""Hero cards for A01-A03 from each article's results. No number typed in."""
import json
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib10"))
from poster import poster, DIM, INK, BOLD  # noqa: E402

# ---------------- A01 Groundhog Day
R = ROOT + "/groundhog-day/results/"
S = json.load(open(R + "summary.json")); RB = json.load(open(R + "robustness_extra.json"))
def reb(f):
    p = pd.read_csv(R + f, index_col=0).dropna(); p.columns = p.columns.astype(int)
    return ((1 + p).div(1 + p[0], axis=0) - 1).mean()
mm, cm = reb("paths_midterm.csv"), reb("paths_control.csv")
def d1(ax, acc):
    x = np.arange(0, 91)
    ax.plot(x, cm.loc[0:90] * 100, color=DIM, lw=4)
    ax.plot(x, mm.loc[0:90] * 100, color=acc, lw=6)
    ax.text(92, mm[90] * 100, f"{mm[90] * 100:+.1f}%", color=acc, fontproperties=BOLD, fontsize=34, va="center")
    ax.text(92, cm[90] * 100, f"{cm[90] * 100:+.1f}%", color=DIM, fontproperties=BOLD, fontsize=26, va="center")
    ax.text(3, mm[90] * 100 * 0.93, "after a midterm", color=acc, fontsize=17, fontproperties=BOLD)
    ax.text(3, mm[90] * 100 * 0.80, "same days, every other year", color=DIM, fontsize=15)
    ax.set_xlim(0, 112); ax.set_xticks([0, 30, 60, 90]); ax.set_xticklabels(["election\nday", "+30", "+60", "+90 days"])
    ax.yaxis.set_major_formatter(__import__("matplotlib").ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
poster(ROOT + "/groundhog-day/figures/hero_groundhog_day.png", 3, "GROUNDHOG\nDAY",
       "The rally that comes back every four years", d1,
       f"STARRING  {S['n_midterm']} MIDTERMS  ·  {S['n_control']} ORDINARY NOVEMBERS\n10,000 SHUFFLED LABELS  ·  ONE PRE-REGISTRATION",
       f"RATED  p = {S['C31-1']['p_perm']:.3f}  ·  GATE 0.025", "SEQUEL OPENS 3 NOVEMBER 2026", accent="#f5b301")

# ---------------- A02 Back to the Future
R2 = ROOT + "/back-to-the-future/results/"
S2 = json.load(open(R2 + "summary.json")); wf = pd.DataFrame(S2["waterfall"])
vals = list(wf.alpha_ann * 100) + [S2["oos"]["record_alpha"] * 100]
labs = ["first\nresult", "dividends", "one\ncurrency", "bug\nfixed", "factors", "out of\nsample"]
def d2(ax, acc):
    x = np.arange(len(vals))
    cols = [acc] + ["#6f8fb8"] * 4 + [DIM]
    ax.bar(x, vals, width=0.62, color=cols)
    ax.axhline(0, color=DIM, lw=1.5)
    for i, v in enumerate(vals):
        ax.text(i, v + (0.3 if v >= 0 else -0.3), f"{v:+.1f}%", ha="center", va="bottom" if v >= 0 else "top", color=INK, fontproperties=BOLD, fontsize=24 if i == 0 else 20)
    ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=14)
    ax.set_ylim(-3, 6.8); ax.set_yticks([])
    ax.text(5.4, 6.2, "alpha a year", color=DIM, fontsize=14, ha="right")
poster(ROOT + "/back-to-the-future/figures/hero_back_to_the_future.png", 2, "BACK TO\nTHE FUTURE",
       "My strategy beat the market by 5% a year. In the past.", d2,
       "STARRING  ONE MOMENTUM STRATEGY  ·  33 TRIALS\nSURVIVORSHIP BIAS  ·  AND 16 YEARS IT HAD NEVER SEEN",
       f"RATED  t = {S2['record']['t_block']:.2f}  ·  BAR {S2['record']['bonferroni_t']:.2f}", "IN CINEMAS 13 OCTOBER 2026", accent="#f5b301")

# ---------------- A03 Titanic
R3 = ROOT + "/titanic/results/"
X3 = json.load(open(R3 + "reported_extra.json")); S3 = json.load(open(R3 + "summary.json"))
P = pd.read_csv(R3 + "rhyme_paths.csv", index_col=0)
def d3(ax, acc):
    cols = {"S&P 500, peak Sep 1929": ("#6b6962", "1929"), "Nikkei 225, peak Dec 1989": ("#c96a3d", "Tokyo 1989"),
            "Nasdaq Composite, peak Mar 2000": ("#8a7fd1", "Nasdaq 2000"), "AI-leaders basket, today": (acc, "AI, 2026")}
    for k, (c, lab) in cols.items():
        s = P[k].dropna()
        ax.plot(s.index, s.values, color=c, lw=6 if "AI" in k else 3.2)
        if "AI" in k:
            ax.text(-22, 140, lab + "  \u2192", color=c, fontproperties=BOLD, fontsize=18, va="center")
        else:
            ax.text(s.index[-1] + 1.5, s.values[-1], lab, color=c, fontproperties=BOLD, fontsize=14, va="center")
    ax.set_yscale("log"); ax.set_yticks([]); ax.minorticks_off()
    ax.axvline(0, color=DIM, lw=1.2, ls=(0, (3, 3)))
    ax.text(-1, 330, "the peak", color=DIM, fontsize=14, ha="right", va="center")
    ax.text(4, 190, "?", color=acc, fontproperties=BOLD, fontsize=70, va="center")
    ax.set_ylim(P.min().min() * 0.85, 420)
    ax.set_xlim(-62, 55); ax.set_xticks([-60, -30, 0, 30]); ax.set_xticklabels(["-5 yrs", "-2.5", "peak", "+2.5 yrs"])
poster(ROOT + "/titanic/figures/hero_titanic.png", 1, "TITANIC",
       "Every bubble was unsinkable. Is this one?", d3,
       "STARRING  TOKYO 1989  ·  NASDAQ 2000  ·  AND 8 AI LEADERS\nA PHILLIPS-SHI-YU BUBBLE TEST  ·  3,053 DOUBLED STOCKS",
       f"RATED  NOT EXPLOSIVE  ·  p = {S3['trials']['C1-2']['gsadf_p']:.2f}", "IN CINEMAS 6 OCTOBER 2026", accent="#3987e5", title_size=92)
print("done")
