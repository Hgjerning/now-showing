# -*- coding: utf-8 -*-
"""Figures for Case 33 from ../results. No number typed in."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES, FIG = os.path.join(ROOT, "results"), os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
BLUE, GREY, RED, AQUA = "#2a78d6", "#8a8984", "#e34948", "#1baf7a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 1, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.spines.left": False, "axes.axisbelow": True})
S = json.load(open(os.path.join(RES, "summary.json")))
pctf = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%")

# ---------- fig1: the waterfall (hero)
wf = pd.DataFrame(S["waterfall"])
labels = ["In-sample\n(first result)", "Dividends\nincluded", "Measured in\none currency", "Holding bug\nfixed", "Adjusted for\nknown factors", "Out of sample\n1995-2011"]
vals = list(wf.alpha_ann * 100) + [S["oos"]["record_alpha"] * 100]
ts = list(wf.t_stat) + [S["oos"]["record_t"]]
cols = [BLUE] * 5 + [GREY]
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
x = np.arange(len(vals))
ax.bar(x, vals, width=0.56, color=cols, zorder=3)
ax.axhline(0, color=INK2, lw=1)
for i, (v, t) in enumerate(zip(vals, ts)):
    y = v + 0.25 if v >= 0 else v - 0.25
    ax.text(i, y, f"{v:+.1f}%", ha="center", va="bottom" if v >= 0 else "top", fontsize=15, fontweight="bold", color=INK)
    ax.text(i, (v + 0.9) if v >= 0 else (v - 1.05), f"t = {t:.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=10, color=INK2)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10.5)
ax.yaxis.set_major_formatter(pctf); ax.set_ylim(-3.2, 7.2)
ax.set_ylabel("Alpha against the MSCI World ETF, % a year")
ax.axvline(4.5, color=GRID, lw=1.5)
fig.suptitle("My strategy beat the market by 5% a year.\nThen I tested it properly.", x=0.06, ha="left", fontsize=19, fontweight="bold", color=INK, y=0.975)
ax.set_title(f"The same strategy, restated after each correction. A t-stat of {S['record']['bonferroni_t']:.2f} was needed after {S['record']['trials']} trials. None got there.",
             loc="left", fontsize=11, color=INK2, pad=10)
fig.text(0.06, 0.012, "Weekly returns 2012-2026 (in-sample) and 1995-2011 (out of sample, point-in-time universe). Henrik Gjerning", fontsize=8.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.subplots_adjust(top=0.80)
fig.savefig(os.path.join(FIG, "fig1_alpha_waterfall.png")); plt.close(fig)

# ---------- fig2: out-of-sample drawdowns
dd = pd.read_csv(os.path.join(RES, "oos_drawdown.csv"), index_col=0, parse_dates=True) * 100
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.fill_between(dd.index, dd.benchmark, 0, color=GREY, alpha=0.25, lw=0)
ax.plot(dd.index, dd.benchmark, color=GREY, lw=1.6, label="Benchmark (same universe, cap-weighted)")
ax.plot(dd.index, dd.strategy, color=BLUE, lw=2, label="Strategy")
i1, i2 = dd.strategy.idxmin(), dd.benchmark.idxmin()
ax.annotate(f"{dd.strategy.min():.0f}%", (i1, dd.strategy.min()), xytext=(8, 0), textcoords="offset points", fontsize=12, fontweight="bold", color=INK, va="center")
ax.annotate(f"{dd.benchmark.min():.0f}%", (i2, dd.benchmark.min()), xytext=(8, 6), textcoords="offset points", fontsize=12, fontweight="bold", color=INK2)
ax.yaxis.set_major_formatter(pctf); ax.set_ylabel("Below previous peak")
ax.legend(frameon=False, loc="lower left", fontsize=10)
ax.set_title("Out of sample, the 'defensive' strategy fell further than the market", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_oos_drawdown.png")); plt.close(fig)

# ---------- fig3: survivorship
sv = pd.DataFrame(S["survivorship"])
fig, ax = plt.subplots(figsize=(10, 4.4), dpi=200)
y = np.arange(len(sv))[::-1]
for yi, r in zip(y, sv.itertuples()):
    ax.plot([r.pit, r.biased], [yi, yi], color=GRID, lw=6, solid_capstyle="round", zorder=1)
    ax.plot(r.biased, yi, "o", ms=11, color=GREY, mec=SURF, mew=2, zorder=3)
    ax.plot(r.pit, yi, "o", ms=11, color=BLUE, mec=SURF, mew=2, zorder=3)
    ax.text(r.biased + 0.03, yi, f"{r.biased:.2f}", va="center", fontsize=10, color=INK2)
    ax.text(r.pit - 0.03, yi, f"{r.pit:.2f}", va="center", ha="right", fontsize=10, color=INK)
    ax.text(1.42, yi, f"-{r.haircut * 100:.0f}%", va="center", fontsize=11, fontweight="bold", color=INK)
ax.set_yticks(y); ax.set_yticklabels(sv.region); ax.set_xlim(0.3, 1.52); ax.set_xlabel("Strategy Sharpe ratio")
ax.plot([], [], "o", color=GREY, label="Today's index members (survivors)"); ax.plot([], [], "o", color=BLUE, label="Members at the time (point-in-time)")
ax.legend(frameon=False, loc="lower left", fontsize=9.5, ncol=2, bbox_to_anchor=(0, -0.32))
ax.set_title("Survivorship: backtesting on today's winners flatters the result", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_survivorship.png")); plt.close(fig)

# ---------- fig4: random books
nb = pd.read_csv(os.path.join(ROOT, "data", "dd_selection_alpha_null.csv"))
rb = S["random_books"]
fig, ax = plt.subplots(figsize=(10, 4.4), dpi=200)
ax.hist(nb.t, bins=40, color=GREY, edgecolor=SURF, linewidth=1)
ax.axvline(2, color=RED, lw=1.4); ax.text(2.04, ax.get_ylim()[1] * 0.92, f"t = 2: {rb['share_t_gt_2'] * 100:.1f}% of random books 'pass'", fontsize=10, color=INK)
ax.axvline(rb["frozen_t"], color=BLUE, lw=2); ax.text(rb["frozen_t"] - 0.05, ax.get_ylim()[1] * 0.72, f"the strategy\nt = {rb['frozen_t']:.2f}", ha="right", fontsize=10, color=INK)
ax.set_xlabel("t-statistic of alpha, 2,000 random 10-stock books from the same survivor universe")
ax.set_title("The wrong null: a monkey with a dartboard 'beats' the market a third of the time", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig4_random_books.png")); plt.close(fig)

# ---------- fig5: what survived (band) + rolling alpha
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.4), dpi=200, gridspec_kw={"width_ratios": [1, 1.4]})
br = pd.DataFrame(S["band"]["regions"])
yy = np.arange(len(br))[::-1]
a1.errorbar(br["diff"], yy, xerr=[br["diff"] - br.ci_lo, br.ci_hi - br["diff"]], fmt="o", color=AQUA, ms=8, mec=SURF, mew=2, ecolor=INK, elinewidth=1.2, capsize=3)
a1.axvline(0, color=INK2, lw=1); a1.set_yticks(yy); a1.set_yticklabels(br.region.map({"EU": "Europe", "UK": "UK", "WD": "World", "DK": "Denmark", "US": "US"}))
a1.set_xlabel("Sharpe gain from skipping small trades, 95% CI")
a1.set_title("What survived: trading less", loc="left", fontsize=12, fontweight="bold", color=INK)
ra = pd.read_csv(os.path.join(ROOT, "data", "alpha_rolling_book_urth.csv"), index_col=0, parse_dates=True).iloc[:, 0] * 100
a2.fill_between(ra.index, ra, 0, where=ra < 0, color=RED, alpha=0.18, lw=0)
a2.plot(ra.index, ra, color=BLUE, lw=2); a2.axhline(0, color=INK2, lw=1); a2.yaxis.set_major_formatter(pctf)
a2.set_title("Rolling 3-year alpha vs the market", loc="left", fontsize=12, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig5_band_and_rolling_alpha.png")); plt.close(fig)
print("figures written")


# ---------- fig6 (added 7 Oct 2026 after external review): where the alpha died -- a bridge of the restatements
wf6 = pd.DataFrame(S["waterfall"]); v6 = list(wf6.alpha_ann * 100)
steps = [("First result", v6[0], None), ("Dividends", v6[1] - v6[0], "the benchmark on total return too"),
         ("Currency", v6[2] - v6[1], "European legs in USD"), ("Holding bug", v6[3] - v6[2], "the book had stopped trading"),
         ("Known factors", v6[4] - v6[3], "momentum loading +0.51")]
fig, ax = plt.subplots(figsize=(10, 6.0), dpi=200)
level = 0.0
for i, (lab, d, why) in enumerate(steps):
    if i == 0:
        ax.bar(i, d, width=0.56, color=BLUE, zorder=3); level = d
        ax.text(i, d + 0.15, f"{d:+.2f}%", ha="center", va="bottom", fontsize=14, fontweight="bold", color=INK)
    else:
        lo, hi = sorted([level, level + d])
        ax.bar(i, hi - lo, bottom=lo, width=0.56, color=RED if d < 0 else BLUE, zorder=3)
        ax.plot([i - 1 + 0.28, i - 0.28], [level, level], color=INK2, lw=1, zorder=4)
        ax.text(i, lo - 0.15, f"{d:+.2f}", ha="center", va="top", fontsize=13, fontweight="bold", color=INK)
        level += d
ax.bar(5, level, width=0.56, color=INK2, zorder=3)
ax.plot([4 + 0.28, 5 - 0.28], [level, level], color=INK2, lw=1, zorder=4)
ax.text(5, level - 0.15, f"{level:+.2f}%", ha="center", va="top", fontsize=14, fontweight="bold", color=INK)
oos6 = S["oos"]["record_alpha"] * 100
ax.bar(6.3, oos6, width=0.56, color=GREY, zorder=3)
ax.text(6.3, oos6 + 0.15, f"{oos6:+.2f}%", ha="center", va="bottom", fontsize=14, fontweight="bold", color=INK)
ax.axvline(5.65, color=GRID, lw=1.5)
ax.axhline(0, color=INK2, lw=1)
ax.set_xticks([0, 1, 2, 3, 4, 5, 6.3])
ax.set_xticklabels(["First result\n(1 Sep)", "Dividends\n(benchmark on\ntotal return)", "Currency\n(European legs\nin USD)", "Holding bug\n(the book had\nstopped trading)", "Known factors\n(momentum\nloading +0.51)", "Left after\nfactors", "Out of sample\n1995-2011\n(separate test)"], fontsize=9.5)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%")); ax.set_ylim(-3.0, 6.6)
ax.set_ylabel("Alpha against the MSCI World ETF, % a year")
fig.suptitle("Where the alpha died", x=0.06, ha="left", fontsize=19, fontweight="bold", color=INK, y=0.975)
ax.set_title("Each bar is the change at one restatement, in percentage points a year. The bug and the factors took the most.",
             loc="left", fontsize=11, color=INK2, pad=10)
fig.text(0.06, 0.012, "Restatements in the order they happened (Table 1); they are sequential, not independent effects. Henrik Gjerning",
         fontsize=8.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.subplots_adjust(top=0.85, bottom=0.2)
fig.savefig(os.path.join(FIG, "fig6_where_the_alpha_died.png")); plt.close(fig)
