# -*- coding: utf-8 -*-
"""A05 figures added 7 Oct 2026 after external review: fig4 fake gurus, fig5 where the legends died. Reads ../results."""
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


# ---------- added 7 Oct 2026 after external review (reported, not gated)
_fg = os.path.join(RES, "fake_gurus.json")
if os.path.exists(_fg):
    FG = json.load(open(_fg)); R = pd.read_csv(os.path.join(RES, "fake_gurus_draws.csv"))
    usr = pd.read_csv(os.path.join(RES, "suspects_us.csv"), index_col=0)
    # fig4: fake gurus
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4), dpi=200, gridspec_kw={"width_ratios": [1, 1.15]})
    panels = R.passed.values[: len(R) // 16 * 16].reshape(-1, 16).sum(axis=1)
    cnt = pd.Series(panels).value_counts().reindex(range(17), fill_value=0)
    a1.bar(cnt.index, cnt.values / cnt.sum() * 100, color=GREY, width=0.8, zorder=3)
    a1.bar([FG["real_n_pass"]], [cnt[FG["real_n_pass"]] / cnt.sum() * 100], color=BLUE, width=0.8, zorder=4)
    a1.annotate(f"The 16 recipes:\n{FG['real_n_pass']} pass", (FG["real_n_pass"], cnt[FG["real_n_pass"]] / cnt.sum() * 100),
                xytext=(-10, 40), textcoords="offset points", ha="right", fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    a1.set_xticks(range(0, 17, 2)); a1.set_xlabel("Recipes out of 16 that pass the A05-1 gate"); a1.set_ylabel("% of 625 panels of 16 fake gurus")
    a1.set_title(f"Independent fake gurus: {FG['expected_of_16']:.1f} of 16 pass on average", loc="left", fontsize=11.5, color=INK)
    a2.scatter(R.raw * 100, R.alpha * 100, s=4, color=GREY, alpha=0.25, lw=0, label="10,000 fake gurus")
    a2.scatter(usr.raw_ann * 100, usr.alpha_ann * 100, s=38, color=BLUE, zorder=5, label="The 16 recipes", edgecolor=SURF, lw=0.8)
    off = {"O'Neil CAN SLIM": (6, -12)}
    for n in ["Buffett (quality)", "Graham", "Lynch", "Greenblatt", "O'Neil CAN SLIM"]:
        a2.annotate(n.split(" (")[0].replace(" CAN SLIM", ""), (usr.loc[n, "raw_ann"] * 100, usr.loc[n, "alpha_ann"] * 100), xytext=off.get(n, (5, 3)),
                    textcoords="offset points", fontsize=9, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6) if n in off else None)
    a2.axhline(0, color=INK2, lw=0.8); a2.set_xlim(-1, 9); a2.set_ylim(-3, 6)
    a2.set_xlabel("Raw premium, % a year"); a2.set_ylabel("Six-factor alpha, % a year")
    a2.set_title("Same raw premium, less alpha left: the legends are more 'usual'", loc="left", fontsize=11.5, color=INK)
    a2.legend(frameon=False, fontsize=9.5, loc="upper left", markerscale=2)
    fig.suptitle("Is five survivors a lot? Not against random recipes", x=0.03, ha="left", fontsize=16, fontweight="bold", color=INK)
    fig.text(0.03, 0.01, "Fake guru: 1-5 legs drawn at random from 153 JKP US factors in JKP's published direction, equal weight; same regression and gate. Seed 42. Reported, not gated. Henrik Gjerning",
             fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94)); fig.savefig(os.path.join(FIG, "fig4_fake_gurus.png")); plt.close(fig)
    # fig5: where the legends died
    W = pd.read_csv(os.path.join(RES, "where_legends_died.csv"))
    steps = ["Raw premium", "+ Market", "+ Size", "+ Value", "+ Profitability", "+ Investment", "+ Momentum", "+ Quality (QMJ)"]
    short = ["Raw", "Mkt", "Size", "Value", "Prof", "Inv", "Mom", "Quality"]
    # 23 Oct 2026 (Henrik: "5 gurus but only 4 graphs"): all five survivors, plus Lynch as the non-survivor for contrast
    PANELS = ["Buffett (quality)", "Graham", "Greenblatt", "Mohanram P/B growth", "P. O'Shaughnessy millennial", "Lynch"]
    fig, axs = plt.subplots(3, 2, figsize=(12, 10.8), dpi=200, sharey=True)
    for ax, n in zip(axs.flat, PANELS):
        w = W[W.recipe == n].set_index("step").alpha.reindex(steps) * 100
        prev = 0.0
        for i, s_ in enumerate(steps):
            v = w[s_]
            if i == 0:
                ax.bar(i, v, color=BLUE, width=0.62, zorder=3)
            else:
                lo, hi = sorted([prev, v]); ax.bar(i, max(hi - lo, 0.04), bottom=lo, width=0.62, zorder=3,
                                                    color=(RED if v < prev else GOLD) if i < 7 else (RED if v < prev else GOLD))
                ax.plot([i - 1 + 0.31, i - 0.31], [prev, prev], color=INK2, lw=0.8)
            prev = v
        ax.bar(8, w.iloc[-1], color=INK2, width=0.62, zorder=3)
        ax.text(0, w.iloc[0] + 0.15, f"{w.iloc[0]:+.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
        ax.text(6, max(w.iloc[5], w.iloc[6], 0) + 0.15, f"{w.iloc[6]:+.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
        ax.text(8, w.iloc[-1] + (0.15 if w.iloc[-1] >= 0 else -0.15), f"{w.iloc[-1]:+.1f}", ha="center", va="bottom" if w.iloc[-1] >= 0 else "top", fontsize=10, fontweight="bold")
        ax.set_ylim(-1.0, 6.9); ax.axhline(0, color=INK2, lw=0.8); ax.set_xticks(range(9)); ax.set_xticklabels(short + ["Left"], fontsize=8.8)
        ax.set_title(f"{n} recipe" + ("  (did not survive)" if n == "Lynch" else "  (survived)"), loc="left", fontsize=12, color=INK, fontweight="bold")
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    for r_ in range(3): axs[r_, 0].set_ylabel("Alpha, % a year")
    fig.suptitle("Where the legends died: the five survivors, and one that did not", x=0.03, ha="left", fontsize=16, fontweight="bold", color=INK)
    fig.text(0.03, 0.01, "US 1963-2025. Red: the step removed alpha; gold: it added alpha (typically a negative loading on that factor). Order of entry is a choice. Quality = AQR QMJ, reported, not gated. Henrik Gjerning",
             fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.025, 1, 0.955)); fig.savefig(os.path.join(FIG, "fig5_where_legends_died.png")); plt.close(fig)
