# -*- coding: utf-8 -*-
"""A01 hero card (revised 9 Oct 2026 after the stress test: poster No. 2, question tagline). No number typed in."""
import json, os, sys
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.environ.get("P10_LIB", os.path.join(ROOT, "..", "_shared", "lib10")))
from poster import poster, DIM, BOLD  # noqa: E402
R = os.path.join(ROOT, "results")
S = json.load(open(os.path.join(R, "summary.json")))
def reb(f):
    p = pd.read_csv(os.path.join(R, f), index_col=0).dropna(); p.columns = p.columns.astype(int)
    return ((1 + p).div(1 + p[0], axis=0) - 1).mean()
mm, cm = reb("paths_midterm.csv"), reb("paths_control.csv")
def draw(ax, acc):
    x = np.arange(0, 91)
    ax.plot(x, cm.loc[0:90] * 100, color=DIM, lw=4); ax.plot(x, mm.loc[0:90] * 100, color=acc, lw=6)
    ax.text(92, mm[90] * 100, f"{mm[90] * 100:+.1f}%", color=acc, fontproperties=BOLD, fontsize=34, va="center")
    ax.text(92, cm[90] * 100, f"{cm[90] * 100:+.1f}%", color=DIM, fontproperties=BOLD, fontsize=26, va="center")
    ax.text(3, mm[90] * 100 * 0.93, "after a midterm, 1930-2022", color=acc, fontsize=17, fontproperties=BOLD)
    ax.text(3, mm[90] * 100 * 0.80, "same days, every other year", color=DIM, fontsize=15)
    ax.set_xlim(0, 112); ax.set_xticks([0, 30, 60, 90]); ax.set_xticklabels(["election\nday", "+30", "+60", "+90 days"])
    ax.yaxis.set_major_formatter(__import__("matplotlib").ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
p = S["C31-1"]["p_perm"]
poster(os.path.join(ROOT, "figures", "hero_groundhog_day.png"), 2, "GROUNDHOG\nDAY",
       "Does the market rally every four years?", draw,
       f"STARRING  {S['n_midterm']} MIDTERMS  ·  {S['n_control']} ORDINARY NOVEMBERS\n10,000 SHUFFLED LABELS  ·  AND 14 OLDER MIDTERMS",
       f"RATED  p = {p:.3f}  ·  GATE 0.025", "SEQUEL OPENS 3 NOVEMBER 2026", accent="#f5b301")
print("hero written")
