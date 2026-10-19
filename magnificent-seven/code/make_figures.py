# -*- coding: utf-8 -*-
"""A03 figures + hero card (film)."""
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
S = json.load(open(os.path.join(RES, "summary.json"))); R = S["reported"]
D = pd.read_csv(os.path.join(RES, "concentration_monthly.csv"), index_col=0, parse_dates=True)
pf = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%")

fig, ax = plt.subplots(figsize=(10, 4.4), dpi=200)
ax.fill_between(D.index, D.C * 100, color=BLUE, alpha=0.15, lw=0); ax.plot(D.index, D.C * 100, color=BLUE, lw=2.4)
ax.annotate(f"{R['C_first']:.0%}\n{R['top10_first'].replace(',', ' ')[:28]}…", (D.index[0], R["C_first"] * 100), xytext=(10, 45), textcoords="offset points", fontsize=9, color=INK2)
ax.annotate(f"{R['C_last']:.0%}", (D.index[-1], R["C_last"] * 100), xytext=(-40, 6), textcoords="offset points", fontsize=12, fontweight="bold", color=INK)
ax.yaxis.set_major_formatter(pf); ax.set_ylim(0, 50); ax.set_ylabel("Top-10 share of the 500 largest, %")
ax.set_title("From a fifth to two-fifths: the top 10 of the 500 largest, 2012-2026", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_concentration.png")); plt.close(fig)

s = D.spread.dropna() * 100
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
ax.bar(s.index, s.values, width=25, color=np.where(s > 0, BLUE, ORANGE))
ax.axhline(0, color=INK2, lw=0.8); ax.yaxis.set_major_formatter(pf)
ax.set_ylabel("Next 12 months: top 10 minus the other 490, % pts")
ax.set_title(f"The giants beat the rest in {S['A03-1']['share_months_top_won']:.0%} of start months (mean {S['A03-1']['mean']:+.1%} a year)", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_top_dog_spread.png")); plt.close(fig)

w = pd.read_csv(os.path.join(RES, "wealth_creation_by_stock.csv"), index_col=0)["usd"]
cum = w.cumsum() / w.sum() * 100
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
ax.plot(np.arange(1, len(cum) + 1), cum.values, color=BLUE, lw=2.4); ax.axhline(100, color=INK2, lw=0.8, ls=":")
ax.set_xscale("log"); ax.yaxis.set_major_formatter(pf); ax.set_xlabel("Number of stocks, best wealth creator first (log scale)")
ax.set_ylabel("Share of net dollar wealth created")
ax.annotate(f"top 10 = {R['wealth_top10_share']:.0%}", (10, cum.iloc[9]), xytext=(20, -25), textcoords="offset points", fontsize=11, fontweight="bold", arrowprops=dict(arrowstyle="-", color=INK2))
ax.set_title(f"${R['wealth_net_usd_tn']:.0f} trillion created 2012-2026; {R['share_negative']:.0%} of stocks destroyed wealth", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_wealth_creation.png")); plt.close(fig)


def draw(ax, acc):
    y = D.C * 100
    ax.fill_between(D.index, y, color=acc, alpha=0.25, lw=0); ax.plot(D.index, y, color=acc, lw=4)
    ax.set_ylim(0, 50); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=15)
    ax.text(D.index[2], R["C_first"] * 100 + 3, f"{R['C_first']:.0%}", color=PINK, fontproperties=BOLD, fontsize=34)
    ax.text(D.index[-40], R["C_last"] * 100 + 3.5, f"{R['C_last']:.0%}", color=PINK, fontproperties=BOLD, fontsize=48)
    ax.text(D.index[2], 45, "the top 10's share of America's 500 largest", color=DIM, fontsize=14)


poster(os.path.join(FIG, "hero_magnificent_seven.png"), 3, "THE\nMAGNIFICENT\nSEVEN", "The giants were supposed to fall. They didn't.", draw,
       "STARRING  NVDA · AAPL · GOOGL · MSFT · AMZN · AVGO · META\nWITH  TESLA, LILLY AND THE OTHER 490 AS THE EXTRAS",
       f"RATED  TOP 10 BEAT THE REST {S['A03-1']['mean']:+.1%} A YEAR  ·  THE LORE FAILED", "IN CINEMAS 20 OCTOBER 2026", accent="#eda100", title_size=66)
