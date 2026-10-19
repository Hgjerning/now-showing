# -*- coding: utf-8 -*-
"""A03 v3 Figure 4: the monthly top-10 minus rest spread (growth of $1 and drawdown) and its factor loadings."""
import json, os, sys
import pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "lib10"))
from common import mpl_style, BLUE, ORANGE, GREY, INK2  # noqa: E402
mpl_style(plt)
S = pd.read_csv(os.path.join(ROOT, "results", "v3_monthly_spread.csv"), index_col=0, parse_dates=True)
X = json.load(open(os.path.join(ROOT, "results", "v3_extras.json")))
cum = (1 + S.spread).cumprod(); dd = cum / cum.cummax() - 1
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.5, 1]})
a = ax[0]; a.plot(cum.index, cum, color=BLUE, lw=2); a.axhline(1, color=GREY, lw=1)
a2 = a.twinx(); a2.fill_between(dd.index, dd, 0, color=ORANGE, alpha=0.25, lw=0); a2.set_ylim(-1.2, 0); a2.set_yticks([-0.3, -0.2, -0.1, 0]); a2.set_yticklabels(["-30%", "-20%", "-10%", "0"]); a2.grid(False)
for s in a2.spines.values(): s.set_visible(False)
r = X["risk"]
a.set_title(f"Top 10 minus the rest, rebalanced monthly: growth of $1\n{r['ann_mean']:+.1%}/yr, volatility {r['ann_vol']:.0%}, IR {r['info_ratio']:.2f}, worst drawdown {r['max_drawdown']:.0%} (orange)", fontsize=11, color=INK2, loc="left")
L = X["attribution"]["loadings"]; names = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "MOM"]
lab = ["Market", "Small minus big", "Value", "Profitability", "Conservative inv.", "Momentum"]
b = [L[n]["beta"] for n in names]; t = [L[n]["t"] for n in names]
cols = [BLUE if abs(x) >= 1.96 else GREY for x in t]
ax[1].barh(lab[::-1], b[::-1], color=cols[::-1]); ax[1].axvline(0, color=INK2, lw=1)
for i, (bb, tt) in enumerate(zip(b[::-1], t[::-1])):
    ax[1].text(bb + (0.02 if bb >= 0 else -0.02), i, f"t {tt:+.1f}", va="center", ha="left" if bb >= 0 else "right", fontsize=9, color=INK2)
A = X["attribution"]
ax[1].set_xlim(-0.65, 0.4)
ax[1].set_title(f"Factor loadings (FF5 + momentum)\nalpha {A['alpha_ann']:+.1%}/yr (t {A['alpha_t']:.1f}), R² {A['r2']:.2f}; blue = |t| ≥ 1.96", fontsize=11, color=INK2, loc="left")
fig.tight_layout(); fig.savefig(os.path.join(ROOT, "figures", "fig4_spread_risk_factors.png"), dpi=150)
print("ok")
