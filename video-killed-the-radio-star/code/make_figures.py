# -*- coding: utf-8 -*-
"""A08 figures + hero card (song)."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from common import BLUE, GREY, INK, INK2, RED, mpl_style  # noqa: E402
from poster import BOLD, DIM, poster  # noqa: E402
from poster import INK as PINK  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES, FIG = os.path.join(ROOT, "results"), os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True); mpl_style(plt)
S = json.load(open(os.path.join(RES, "summary.json"))); R = S["reported"]
T = pd.read_csv(os.path.join(RES, "decay_by_factor.csv"), index_col=0).sort_values("year")
pb = np.load(os.path.join(RES, "placebo_coef.npy")) * 1200
RB = json.load(open(os.path.join(RES, "robustness_2026-10-23.json")))   # 23 Oct 2026 stress test (reported, not tested)

fig, ax = plt.subplots(figsize=(10, 8.2), dpi=200)
y = np.arange(len(T))[::-1]
for yi, (_, r) in zip(y, T.iterrows()):
    ax.plot([r.pre_ann * 100, r.post_ann * 100], [yi, yi], color=GREY, lw=1.4, zorder=1)
ax.scatter(T.pre_ann * 100, y, color=GREY, s=36, label="before publication", zorder=2)
ax.scatter(T.post_ann * 100, y, color=BLUE, s=36, label="after publication", zorder=3)
ax.set_yticks(y); ax.set_yticklabels([f"{r.label} ({r.year})" for _, r in T.iterrows()], fontsize=8.5)
ax.axvline(0, color=INK2, lw=0.8); ax.set_xlabel("Average return, % a year (JKP US factor, long-short)"); ax.legend(frameon=False, loc="lower right")
ax.set_title(f"29 famous factors, before and after the paper: {R['share_decayed']:.0%} shrank", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_before_after.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
ax.hist(pb, bins=50, color=GREY, edgecolor="#fcfcfb"); ax.axvline(S["A08-1"]["coef_ann"] * 100, color=RED, lw=2.5)
ax.text(S["A08-1"]["coef_ann"] * 100 + 0.04, ax.get_ylim()[1] * 0.88, f"real dates\n{S['A08-1']['coef_ann']:+.1%} a year", fontsize=10.5)
sm = RB["shuffle_placebo"]["mean_ann"] * 100; fe = RB["month_fixed_effects"]["coef_ann"] * 100
ax.axvline(sm, color=INK2, lw=1.6, ls="--"); ax.axvline(fe, color=BLUE, lw=1.6, ls=":")
ax.text(sm - 0.04, ax.get_ylim()[1] * 0.55, f"shuffled real years\n(mean {sm:+.1f}%)", fontsize=9, color=INK2, ha="right")
ax.text(fe + 0.05, ax.get_ylim()[1] * 0.2, f"month effects\n{fe:+.1f}%", fontsize=9, color=BLUE)
ax.set_xlabel("Post-'publication' change in factor return, % a year (grey: 1,000 random publication years, registered placebo)")
ax.set_title("Bigger than random dates, but part of the fall is a slump that hit every factor", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.text(0.01, 0.005, "Dashed and dotted lines: robustness checks from the 23 Oct 2026 stress test, reported, not tested.", fontsize=8, color=INK2)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_placebo.png")); plt.close(fig)


def draw(ax, acc):
    for _, r in T.iterrows():
        ax.plot([0, 1], [r.pre_ann * 100, r.post_ann * 100], color=DIM, lw=1.2, alpha=0.55)
    a, b = T.pre_ann.mean() * 100, T.post_ann.mean() * 100
    ax.plot([0, 1], [a, b], color=acc, lw=7, solid_capstyle="round")
    ax.text(-0.04, a, f"{a:.1f}%", ha="right", va="center", color=PINK, fontproperties=BOLD, fontsize=36)
    ax.text(1.04, b, f"{b:.1f}%", ha="left", va="center", color=PINK, fontproperties=BOLD, fontsize=36)
    ax.set_xlim(-0.45, 1.45); ax.set_xticks([0, 1]); ax.set_xticklabels(["BEFORE THE PAPER", "AFTER THE PAPER"], fontsize=16); ax.set_yticks([]); ax.grid(False)
    ax.axhline(0, color=DIM, lw=1, ls=":")
    ax.text(0.5, T.pre_ann.max() * 100 + 0.4, "29 famous factors: average of each factor's own return a year", ha="center", color=DIM, fontsize=13)


poster(os.path.join(FIG, "hero_video_killed.png"), 7, "VIDEO KILLED\nTHE RADIO STAR", "After the paper, the factors faded. Not all of it was the paper.", draw,
       "FEATURING  VALUE · MOMENTUM · QUALITY · ACCRUALS · MAX AND 24 MORE\nJENSEN-KELLY-PEDERSEN DATA  ·  US 1926-2025",
       f"RATED  2 OF 2 PASSED  ·  {S['A08-1']['coef_ann']:+.1%} A YEAR AFTER  ·  PART IS A SLUMP", "ON REPEAT FROM 17 NOVEMBER 2026", accent="#eb6834", kind="song", title_size=62)


# 23 Oct 2026 (click teaser, as A04-A07): a teaser poster that asks. Before-publication returns only; no after, no verdict.
def draw_teaser(ax, acc):
    for _, r in T.iterrows():
        ax.plot([0, 0.55], [r.pre_ann * 100, r.pre_ann * 100], color=DIM, lw=1.0, alpha=0.5)
    a = T.pre_ann.mean() * 100
    ax.plot([0, 0.55], [a, a], color=acc, lw=7, solid_capstyle="round")
    ax.text(-0.04, a, f"{a:.1f}%", ha="right", va="center", color=PINK, fontproperties=BOLD, fontsize=36)
    ax.text(1.0, a, "?", ha="center", va="center", color=PINK, fontproperties=BOLD, fontsize=60)
    ax.set_xlim(-0.45, 1.45); ax.set_xticks([0, 1]); ax.set_xticklabels(["BEFORE THE PAPER", "AFTER THE PAPER?"], fontsize=16); ax.set_yticks([]); ax.grid(False)
    ax.axhline(0, color=DIM, lw=1, ls=":")
    ax.text(0.5, T.pre_ann.max() * 100 + 0.4, "29 famous factors, return a year before their paper (at first sight)", ha="center", color=DIM, fontsize=13)


poster(os.path.join(FIG, "hero_video_killed_teaser.png"), 7, "VIDEO KILLED\nTHE RADIO STAR", "29 famous factors. What happened after the paper?", draw_teaser,
       "FEATURING  VALUE · MOMENTUM · PROFITABILITY · ACCRUALS · MAX AND 24 MORE\nJENSEN-KELLY-PEDERSEN DATA  ·  US 1926-2025",
       "RATED  TWO PRE-REGISTERED TESTS  ·  THE VERDICT IS IN THE ARTICLE", "ON REPEAT FROM 17 NOVEMBER 2026", accent="#eb6834", kind="song", title_size=62)
print("teaser poster written")
