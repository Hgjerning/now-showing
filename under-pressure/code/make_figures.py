# -*- coding: utf-8 -*-
"""A07 figures + hero card (song)."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from common import AQUA, BLUE, GREY, INK, INK2, RED, mpl_style  # noqa: E402
from poster import BOLD, DIM, poster  # noqa: E402
from poster import INK as PINK  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES, FIG = os.path.join(ROOT, "results_pit"), os.path.join(ROOT, "figures")   # 23 Oct 2026: the corrected list is the record (Henrik)
os.makedirs(FIG, exist_ok=True); mpl_style(plt)
S = json.load(open(os.path.join(RES, "summary.json"))); R = S["reported"]
D = pd.read_csv(os.path.join(RES, "scores_panel.csv"), parse_dates=["date"]); D = D[D.date <= "2025-06-30"].dropna(subset=["crash"])
D["crash"] = D.crash.astype(bool)
aucs = [("Trailing volatility\n(market)", R["auc_vol_all"], BLUE), ("Piotroski F\n(2000)", R["auc_F"], GREY), ("Altman Z\n(1968)", R["auc_Z"], GREY), ("Ohlson O\n(1980)", R["auc_O_all"], GREY)]

# fig1 AUC bars
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.bar(range(4), [a[1] for a in aucs], color=[a[2] for a in aucs], width=0.6)
for i, a in enumerate(aucs):
    ax.text(i, a[1] + 0.01, f"{a[1]:.2f}", ha="center", fontsize=12, fontweight="bold", color=INK)
ax.axhline(0.5, color=RED, lw=1.5, ls="--"); ax.text(3.45, 0.505, "coin flip", color=RED, ha="right", fontsize=10)
ax.set_xticks(range(4)); ax.set_xticklabels([a[0] for a in aucs]); ax.set_ylim(0.3, 0.85)
ax.set_ylabel("AUC: ranks next-year crashes (≥40% drawdown)")
ax.set_title(f"Volatility ranks next-year crashes best ({R['n_dates']} quarter-ends, {R['n_obs']:,} firm-quarters, actual index members)", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_auc.png")); plt.close(fig)

# fig2 crash rate by decile of volatility vs O-score
def dec_rate(col):
    g = D.dropna(subset=[col]).copy(); g["d"] = g.groupby("date")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False) + 1)
    return g.groupby("d").crash.mean()
v, o = dec_rate("vol"), dec_rate("O")
pd.DataFrame({"vol_decile": v, "O_decile": o}).to_csv(os.path.join(RES, "crash_rate_by_decile.csv"))
fig, ax = plt.subplots(figsize=(10, 4.4), dpi=200)
x = np.arange(1, 11); w = 0.38
ax.bar(x - w / 2, v * 100, w, color=BLUE, label="sorted on trailing volatility")
ax.bar(x + w / 2, o * 100, w, color=GREY, label="sorted on Ohlson O-score")
ax.axhline(R["base_rate"] * 100, color=INK2, lw=1, ls=":"); ax.text(10.6, R["base_rate"] * 100 + 0.6, f"base rate {R['base_rate']:.1%}", ha="right", fontsize=9.5, color=INK2)
ax.set_xticks(x); ax.set_xticklabels(["1\nsafest"] + [str(i) for i in range(2, 10)] + ["10\nriskiest"])
ax.set_ylabel("Share that crashed within 12 months, %"); ax.legend(frameon=False, loc="upper left")
ax.set_title("Crash rate by decile (actual index members): the volatility staircase vs a flat accounting line", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_crash_by_decile.png")); plt.close(fig)

# fig3 AUC by year
Y = pd.read_csv(os.path.join(RES, "auc_by_year.csv"), index_col=0)
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
for c, col, lab in (("auc_vol", BLUE, "volatility"), ("auc_F", AQUA, "Piotroski F"), ("auc_Z", GREY, "Altman Z"), ("auc_O", RED, "Ohlson O")):
    ax.plot(Y.index, Y[c], color=col, lw=2.2 if c == "auc_vol" else 1.6, marker="o", ms=4, label=lab)
ax.axhline(0.5, color=INK2, lw=0.8, ls="--"); ax.legend(frameon=False, ncol=4, loc="lower center"); ax.set_ylim(0.3, 0.95)
ax.set_title("Volatility leads in all 14 years (actual index members; Altman ahead on 2 of 50 dates)", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_auc_by_year.png")); plt.close(fig)


def draw(ax, acc):
    labs = ["VOLATILITY", "PIOTROSKI", "ALTMAN", "OHLSON"]; vals = [a[1] for a in aucs]
    ys = np.arange(4)[::-1]
    ax.barh(ys, [v - 0.5 for v in vals], left=0.5, color=[acc, DIM, DIM, DIM], height=0.6)
    for y, l, v in zip(ys, labs, vals):
        ax.text(0.33, y, l, va="center", ha="left", color=PINK, fontproperties=BOLD, fontsize=22)
        ax.text(max(v, 0.5) + 0.012, y, f"{v:.2f}", va="center", color=PINK, fontproperties=BOLD, fontsize=26)
    ax.axvline(0.5, color=DIM, lw=1.5); ax.set_xlim(0.32, 0.88); ax.set_yticks([]); ax.set_xticks([0.5, 0.6, 0.7, 0.8])
    ax.text(0.5, -0.85, "0.50 = a coin flip", color=DIM, fontsize=13, ha="center")
    ax.text(0.87, 3.55, "who saw the crash coming? (AUC)", color=DIM, fontsize=13, ha="right")


poster(os.path.join(FIG, "hero_under_pressure.png"), 6, "UNDER\nPRESSURE", "The price chart ranks the crashes better", draw,
       f"FEATURING  ALTMAN · OHLSON · PIOTROSKI  vs  ONE VOLATILITY NUMBER\n{R['n_obs']:,} FIRM-QUARTERS  ·  ACTUAL S&P 500 MEMBERS  ·  2012-2025 FORMATIONS",
       f"RATED  1 OF 3  ·  VOLATILITY AUC {R['auc_vol_all']:.2f}  ·  ALTMAN {R['auc_Z']:.2f}", "ON REPEAT FROM 10 NOVEMBER 2026", accent="#c23b8e", kind="song")
print(v.round(3).to_dict(), o.round(3).to_dict())

# 23 Oct 2026 (click teaser, as A04-A06): a teaser poster that asks. Altman and Ohlson only, on the FIRST (registered) list,
# "at first sight": the post's one number. No volatility bar, no verdict.
R0 = json.load(open(os.path.join(ROOT, "results", "summary.json")))["reported"]
def draw_teaser(ax, acc):
    labs, vals = ["ALTMAN Z", "OHLSON O"], [R0["auc_Z"], R0["auc_O_all"]]
    ys = np.array([2.2, 1.2])
    ax.barh(ys, [v - 0.5 for v in vals], left=0.5, color=[DIM, DIM], height=0.6)
    for y, l, v in zip(ys, labs, vals):
        ax.text(0.33, y, l, va="center", ha="left", color=PINK, fontproperties=BOLD, fontsize=22)
        ax.text(max(v, 0.5) + 0.012, y, f"{v:.2f}", va="center", color=PINK, fontproperties=BOLD, fontsize=26)
    ax.text(0.70, 0.15, "AND THE\nCHALLENGER?", ha="center", va="center", color=PINK, fontproperties=BOLD, fontsize=26)
    ax.axvline(0.5, color=DIM, lw=1.5); ax.set_xlim(0.32, 0.88); ax.set_ylim(-0.6, 3.2); ax.set_yticks([]); ax.set_xticks([0.5, 0.6, 0.7, 0.8])
    ax.text(0.5, -0.45, "0.50 = a coin flip", color=DIM, fontsize=13, ha="center")
    ax.text(0.87, 3.0, "who saw the crash coming? (AUC, first list, at first sight)", color=DIM, fontsize=13, ha="right")


poster(os.path.join(FIG, "hero_under_pressure_teaser.png"), 6, "UNDER\nPRESSURE", "Two textbook scores. One number from the chart.", draw_teaser,
       "FEATURING  ALTMAN · OHLSON · PIOTROSKI  vs  ONE NUMBER FROM THE PRICE CHART\nS&P 500 NAMES  ·  2012-2025 FORMATIONS",
       "RATED  THREE PRE-REGISTERED TESTS  ·  THE VERDICT IS IN THE ARTICLE", "ON REPEAT FROM 10 NOVEMBER 2026", accent="#c23b8e", kind="song")
print("teaser poster written")
