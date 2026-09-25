# -*- coding: utf-8 -*-
"""Figures for Case 1 (every bubble rhymes). Reads ../results and ../data."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES, FIG, D = (os.path.join(ROOT, x) for x in ("results", "figures", "data"))
os.makedirs(FIG, exist_ok=True)
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
BLUE, ORANGE, AQUA, VIOLET, GREY, RED = "#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7", "#8a8984", "#e34948"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 1, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.spines.left": False, "axes.axisbelow": True})
S = json.load(open(os.path.join(RES, "summary.json"))); X = json.load(open(os.path.join(RES, "reported_extra.json")))

# ---------- fig1: the rhyme (hero)
P = pd.read_csv(os.path.join(RES, "rhyme_paths.csv"), index_col=0)
cols = {"S&P 500, peak Sep 1929": GREY, "Nikkei 225, peak Dec 1989": ORANGE, "Nasdaq Composite, peak Mar 2000": VIOLET, "AI-leaders basket, today": BLUE}
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
for k, c in cols.items():
    s = P[k].dropna()
    ax.plot(s.index, s.values, color=c, lw=2.6 if "AI" in k else 1.8, label=k, zorder=4 if "AI" in k else 3)
    ax.plot(s.index[-1], s.values[-1], "o", ms=7, color=c, mec=SURF, mew=2, zorder=5)
ax.set_yscale("log"); ax.set_yticks([10, 20, 50, 100, 200]); ax.set_yticklabels(["10", "20", "50", "100", "200"])
ax.axvline(0, color=INK2, lw=1); ax.axhline(100, color=INK2, lw=0.6)
ax.text(1, 175, "peak\n(AI basket: Sep 2026, i.e. today)", fontsize=9.5, color=INK2, va="top")
for k in cols:
    r = X["rhyme"][k]["runup_to_peak"]
    s = P[k].dropna()
    ax.annotate(f"+{r * 100:.0f}%", (s.index[0], s.values[0]), xytext=(-6, 0), textcoords="offset points", ha="right", va="center", fontsize=10, fontweight="bold", color=INK)
ax.set_xlim(-66, 38); ax.set_xlabel("Months from the peak"); ax.set_ylabel("Index, peak = 100 (log scale)")
ax.legend(frameon=False, loc="lower right", fontsize=9.5)
fig.suptitle("Every bubble rhymes. Does this one?", x=0.06, ha="left", fontsize=19, fontweight="bold", color=INK, y=0.975)
c2 = S["trials"]["C1-2"]
ax.set_title(f"The AI leaders' five-year run is Tokyo-sized. The bubble test says it is not explosive now (GSADF p = {c2['gsadf_p']:.2f}).", loc="left", fontsize=10.8, color=INK2, pad=8)
fig.text(0.06, 0.012, "AI-leaders basket: NVDA, AVGO, AMD, MSFT, META, GOOGL, AMZN, ORCL, equal weight. Phillips-Shi-Yu GSADF, monthly. Henrik Gjerning", fontsize=8.3, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.subplots_adjust(top=0.86)
fig.savefig(os.path.join(FIG, "fig1_every_bubble_rhymes.png")); plt.close(fig)

# ---------- fig2: BSADF panels
panels = [("Nasdaq Composite 1985-2002 (legibility)", "bsadf_Nasdaq_Composite_1985_2002.csv"), ("NVIDIA (reported)", "bsadf_NVDA.csv"),
          ("AI-leaders basket (trial C1-2)", "bsadf_AI_leaders_basket.csv"), ("Nasdaq-100 (trial C1-1)", "bsadf_Nasdaq_100__QQQ_.csv")]
fig, axs = plt.subplots(2, 2, figsize=(11, 6.4), dpi=200)
for ax, (t, f) in zip(axs.flat, panels):
    s = pd.read_csv(os.path.join(RES, f), index_col=0, parse_dates=True)
    ax.plot(s.index, s.bsadf, color=BLUE, lw=1.6, label="BSADF statistic")
    ax.plot(s.index, s.cv, color=RED, lw=1.2, label="critical value")
    ax.fill_between(s.index, s.bsadf, s.cv, where=s.bsadf > s.cv, color=RED, alpha=0.2, lw=0)
    ax.set_title(t, loc="left", fontsize=11, fontweight="bold", color=INK)
axs[0, 0].legend(frameon=False, fontsize=9, loc="upper left")
fig.suptitle("Explosive or not? Shaded = price rising faster than a random walk can explain", x=0.02, ha="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_bsadf_panels.png")); plt.close(fig)

# ---------- fig3: GSY crash probability by run-up, with today's AI names
b = pd.read_csv(os.path.join(RES, "gsy_by_runup_bucket.csv"))
lab = ["fell", "0-50%", "50-100%", "100-150%", "150%+"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), dpi=200, gridspec_kw={"width_ratios": [1.25, 1]})
x = np.arange(len(b))
a1.bar(x, b.crash * 100, width=0.56, color=[GREY, GREY, GREY, BLUE, BLUE])
for i, r in enumerate(b.itertuples()):
    a1.text(i, r.crash * 100 + 1, f"{r.crash * 100:.0f}%", ha="center", fontsize=10.5, fontweight="bold", color=INK)
a1.set_xticks(x); a1.set_xticklabels(lab); a1.set_xlabel("Stock's return over the previous 24 months")
a1.set_ylabel("Probability of a 40% crash within 24 months"); a1.set_ylim(0, 75)
a1.set_title("After a doubling, a crash is more likely...", loc="left", fontsize=12, fontweight="bold", color=INK)
a2.bar(x, b.fwd24 * 100, width=0.56, color=[GREY, GREY, GREY, BLUE, BLUE])
for i, r in enumerate(b.itertuples()):
    a2.text(i, r.fwd24 * 100 + 1, f"{r.fwd24 * 100:+.0f}%", ha="center", fontsize=10.5, color=INK)
a2.set_xticks(x); a2.set_xticklabels(lab, fontsize=9.5); a2.set_ylabel("Mean return, next 24 months")
a2.set_title("...but returns stay positive", loc="left", fontsize=12, fontweight="bold", color=INK)
fig.text(0.01, 0.005, "US stocks 2011-2026, non-overlapping windows. Today's listed names only (survivorship lowers crash rates and raises returns).", fontsize=8.3, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(FIG, "fig3_gsy_crash_by_runup.png")); plt.close(fig)

# ---------- fig4: breadth of doublings (relevance)
panel = pd.read_csv(os.path.join(D, "us_monthly_adjclose_panel.csv"), index_col=0, parse_dates=True).loc["2011-06":]
r24 = panel / panel.shift(24) - 1
share = (r24 >= 1).sum(axis=1) / r24.notna().sum(axis=1)
share = share[r24.notna().sum(axis=1) >= 300] * 100
share.to_csv(os.path.join(RES, "share_doubled_24m.csv"), header=["share_pct"])
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
ax.plot(share.index, share, color=BLUE, lw=2)
ax.axhline(share.mean(), color=GREY, lw=1); ax.text(share.index[40], share.mean() - 2.2, f"average {share.mean():.1f}%", fontsize=9.5, color=INK2)
ax.plot(share.index[-1], share.iloc[-1], "o", ms=8, color=BLUE, mec=SURF, mew=2)
ax.annotate(f"today {share.iloc[-1]:.1f}%", (share.index[-1], share.iloc[-1]), xytext=(-8, -18), textcoords="offset points", ha="right", fontsize=10.5, fontweight="bold", color=INK)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.set_title("How broad is the mania? Share of US stocks that doubled over two years", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig4_breadth_of_doublings.png")); plt.close(fig)
json.dump({"share_now": float(share.iloc[-1]), "share_mean": float(share.mean()), "share_max": float(share.max()), "share_max_date": str(share.idxmax().date())[:7]},
          open(os.path.join(RES, "breadth.json"), "w"), indent=2)
print("figures written", float(share.iloc[-1]), float(share.mean()), share.idxmax())
