# -*- coding: utf-8 -*-
"""A02 hero card (revised 9 Oct 2026 after the stress test): the path to the number of record only; currency is not
drawn on the path, and the out-of-sample bar is labelled as the locked version. No number typed in."""
import json, os, sys
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.environ.get("P10_LIB", os.path.join(ROOT, "..", "_shared", "lib10")))
from poster import poster, DIM, INK, BOLD  # noqa: E402
S = json.load(open(os.path.join(ROOT, "results", "summary.json"))); wf = pd.DataFrame(S["waterfall"])
vals = [wf.alpha_ann.iloc[i] * 100 for i in (0, 1, 3, 4)] + [S["oos"]["record_alpha"] * 100]
labs = ["first\nresult", "total return,\nnew setup", "lock\nfixed", "factors", "out of sample\n(locked)"]
def draw(ax, acc):
    x = np.arange(len(vals)); cols = [acc] + ["#6f8fb8"] * 3 + [DIM]
    ax.bar(x, vals, width=0.62, color=cols); ax.axhline(0, color=DIM, lw=1.5)
    for i, v in enumerate(vals):
        ax.text(i, v + (0.3 if v >= 0 else -0.3), f"{v:+.1f}%", ha="center", va="bottom" if v >= 0 else "top", color=INK, fontproperties=BOLD, fontsize=24 if i == 0 else 20)
    ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=14); ax.set_ylim(-3, 6.8); ax.set_yticks([])
    ax.text(4.4, 6.2, "alpha a year", color=DIM, fontsize=14, ha="right")
poster(os.path.join(ROOT, "figures", "hero_back_to_the_future.png"), 2, "BACK TO\nTHE FUTURE",
       "My strategy beat the market by 5% a year. In the past.", draw,
       "STARRING  ONE MOMENTUM STRATEGY  ·  33 TRIALS\nSURVIVORSHIP BIAS  ·  AND 17 YEARS IT HAD NEVER SEEN",
       f"RATED  t = {S['record']['t_block']:.2f}  ·  BAR {S['record']['bonferroni_t']:.2f}", "IN CINEMAS 13 OCTOBER 2026", accent="#f5b301")
print("hero written")
