# -*- coding: utf-8 -*-
"""A05 figures + hero card. Reads ../results."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES, FIG = os.path.join(ROOT, "results"), os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
BLUE, GOLD, GREY, RED = "#2a78d6", "#eda100", "#8a8984", "#e34948"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 1, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.spines.left": False, "axes.axisbelow": True})
us = pd.read_csv(os.path.join(RES, "suspects_us.csv"), index_col=0)
q7 = pd.read_csv(os.path.join(RES, "suspects_us_with_qmj.csv"), index_col=0)
S = json.load(open(os.path.join(RES, "summary.json")))
us = us.sort_values("raw_ann")
FAC = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "Mom"]
LBL = {"Mkt-RF": "Market", "SMB": "Size", "HML": "Value", "RMW": "Profitability", "CMA": "Investment", "Mom": "Momentum"}


def dumbbell(ax, df, acc, gold, grey, ink, dark=False):
    y = np.arange(len(df))
    for yi, (_, r) in zip(y, df.iterrows()):
        c = gold if bool(r["pass"]) else acc
        ax.plot([r.raw_ann * 100, r.alpha_ann * 100], [yi, yi], color=grey, lw=2.5, alpha=0.6, solid_capstyle="round")
        ax.plot(r.raw_ann * 100, yi, "o", ms=9, color=grey, mec="none")
        ax.plot(r.alpha_ann * 100, yi, "o", ms=11, color=c, mec="none")
    ax.axvline(0, color=grey, lw=1)
    ax.set_yticks(y); ax.set_yticklabels([{"Fisher (price/sales)": "Ken Fisher (price/sales)"}.get(n, n) for n in df.index], color=ink)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))


# ---------- fig1 dumbbell
fig, ax = plt.subplots(figsize=(10, 7.2), dpi=200)
dumbbell(ax, us, BLUE, GOLD, GREY, INK)
ax.set_xlabel("% a year: grey = raw premium, colour = alpha after six factors")
ax.plot([], [], "o", color=GREY, label="raw premium"); ax.plot([], [], "o", color=BLUE, label="alpha after 6 factors")
ax.plot([], [], "o", color=GOLD, label=f"alpha survives (|t| > {S['gate_t']:.2f}, both halves)")
ax.legend(frameon=True, facecolor=SURF, edgecolor=SURF, loc="center right", fontsize=9.5)
ax.set_title(f"{S['n_recipes'] - S['n_pass']} of {S['n_recipes']} guru recipes leave no robust alpha after six factors", loc="left", fontsize=14, fontweight="bold", color=INK)
fig.text(0.01, 0.005, "US, JKP factor legs, monthly 1963-2025. Six factors: Fama-French 5 + momentum (French data). Newey-West t.", fontsize=8.3, color=MUTED)
fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(os.path.join(FIG, "fig1_suspects_dumbbell.png")); plt.close(fig)

# ---------- fig2 loadings heatmap
B = us[[f"b_{f}" for f in FAC]].astype(float); B.columns = [LBL[f] for f in FAC]
fig, ax = plt.subplots(figsize=(10, 7.2), dpi=200)
v = np.nanmax(np.abs(B.values))
im = ax.imshow(B.values, cmap="RdBu_r", vmin=-v, vmax=v, aspect="auto")
ax.set_xticks(range(len(B.columns))); ax.set_xticklabels(B.columns); ax.set_yticks(range(len(B))); ax.set_yticklabels([{"Fisher (price/sales)": "Ken Fisher (price/sales)"}.get(n, n) for n in B.index])
ax.grid(False)
for i in range(B.shape[0]):
    for j in range(B.shape[1]):
        val = B.values[i, j]
        ax.text(j, i, f"{val:+.2f}", ha="center", va="center", fontsize=8.5, color="#ffffff" if abs(val) > v * 0.55 else INK)
ax2 = ax.twinx(); ax2.set_ylim(ax.get_ylim()); ax2.set_yticks(range(len(B))); ax2.set_yticklabels([f"R² {r:.2f}" for r in us.r2.astype(float)], fontsize=8.5); ax2.grid(False)
for s in ax2.spines.values(): s.set_visible(False)
ax.set_title("Who did it: each recipe's factor fingerprint", loc="left", fontsize=14, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_fingerprints.png")); plt.close(fig)

# ---------- fig3 the seventh suspect
ps = us[us["pass"].astype(bool)].index
fig, ax = plt.subplots(figsize=(10, 4.4), dpi=200)
x = np.arange(len(ps)); w = 0.36
ax.bar(x - w / 2, us.loc[ps, "alpha_ann"] * 100, w, color=GOLD, label="alpha after 6 factors")
ax.bar(x + w / 2, q7.loc[ps, "alpha_ann"] * 100, w, color=BLUE, label="... after adding quality (QMJ)")
for i, p in enumerate(ps):
    ax.text(i - w / 2, us.loc[p, "alpha_ann"] * 100 + 0.08, f"{us.loc[p, 'alpha_ann'] * 100:.1f}%", ha="center", fontsize=9.5)
    ax.text(i + w / 2, q7.loc[p, "alpha_ann"] * 100 + 0.08, f"{q7.loc[p, 'alpha_ann'] * 100:.1f}%\nt {q7.loc[p, 'alpha_t']:.1f}", ha="center", fontsize=8.5)
ax.set_xticks(x); ax.set_xticklabels(ps, fontsize=9.5); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.legend(frameon=False, fontsize=9.5); ax.set_ylim(0, 4.6)
ax.set_title("The seventh suspect: quality takes most of Greenblatt's alpha and a quarter to a half of the rest", loc="left", fontsize=12, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_seventh_suspect.png")); plt.close(fig)

# ---------- hero card
sys.path.insert(0, os.path.join(ROOT, "..", "_shared", "lib10"))
from poster import poster, DIM, INK as PINK, BOLD, GOLD as PGOLD  # noqa: E402
top = us.sort_values("raw_ann")
def draw(ax, acc):
    dumbbell(ax, top, acc, PGOLD, DIM, PINK, dark=True)
    short = {"P. O'Shaughnessy millennial": "P. O'Shaughnessy", "O'Shaughnessy growth": "O'Shaughnessy growth", "O'Shaughnessy value": "O'Shaughnessy value",
             "Buffett (quality)": "Buffett", "O'Neil CAN SLIM": "O'Neil", "Fisher (price/sales)": "Ken Fisher", "Piotroski-type small growth": "Piotroski-type",
             "Motley Fool small-cap growth": "the Motley Fool", "Mohanram P/B growth": "Mohanram"}
    ax.set_yticklabels([short.get(n, n) for n in top.index], fontsize=13.5)
    ax.set_xlim(-1, 7)
    ax.text(6.9, len(top) - 0.2, "grey: raw premium   blue: after 6 factors   gold: survives", color=DIM, fontsize=11.5, ha="right")
poster(os.path.join(FIG, "hero_usual_suspects.png"), 5, "THE USUAL\nSUSPECTS", "Fifteen legends, one Fool, one regression", draw,
       f"STARRING  GRAHAM · BUFFETT · LYNCH · GREENBLATT · O'NEIL AND 11 MORE\nFACTOR RECIPES OF PUBLISHED RULES, NOT THE INVESTORS' PORTFOLIOS",
       f"RATED  TRIAL PASSED, {S['n_pass']} OF {S['n_recipes']}  ·  NO BETTER THAN RANDOM RECIPES", "IN CINEMAS 3 NOVEMBER 2026", accent="#3987e5", ax_left=0.27)
print("figures written")

# 23 Oct 2026 (click teaser, as A04): a teaser version of the poster that asks instead of answering.
# Raw premiums only: no alphas, no pass count, no verdict -- those are the answers to the teaser's questions.
def draw_teaser(ax, acc):
    y = np.arange(len(top))
    ax.barh(y, top.raw_ann * 100, color=DIM, height=0.55)
    ax.set_yticks(y)
    short = {"P. O'Shaughnessy millennial": "P. O'Shaughnessy", "Buffett (quality)": "Buffett", "O'Neil CAN SLIM": "O'Neil",
             "Fisher (price/sales)": "Ken Fisher", "Piotroski-type small growth": "Piotroski-type",
             "Motley Fool small-cap growth": "the Motley Fool", "Mohanram P/B growth": "Mohanram"}
    ax.set_yticklabels([short.get(n, n) for n in top.index], fontsize=13.5)
    ax.set_xlim(0, 7); ax.grid(False)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.text(6.9, len(top) - 0.2, "raw premium, % a year (at first sight)", color=DIM, fontsize=11.5, ha="right")
    ax.text(4.2, 3.0, "HOW MUCH\nSURVIVES?", ha="center", va="center", color=PINK, fontproperties=BOLD, fontsize=26)


poster(os.path.join(FIG, "hero_usual_suspects_teaser.png"), 5, "THE USUAL\nSUSPECTS", "Sixteen legends' rules. Six textbook factors.", draw_teaser,
       f"STARRING  GRAHAM · BUFFETT · LYNCH · GREENBLATT · O'NEIL AND 11 MORE\nFACTOR RECIPES OF PUBLISHED RULES, NOT THE INVESTORS' PORTFOLIOS",
       "RATED  ONE PRE-REGISTERED TRIAL  ·  THE VERDICT IS IN THE ARTICLE", "IN CINEMAS 3 NOVEMBER 2026", accent="#3987e5", ax_left=0.27)
print("teaser poster written")

