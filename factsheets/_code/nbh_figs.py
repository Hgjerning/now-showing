# -*- coding: utf-8 -*-
"""Figures for the 360° neighbourhood section (generic: target + mirror)."""
import json
import os

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); FIG = os.path.join(HERE, "..", "figures")
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
BLUE, ORANGE, AQUA, VIOLET, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7", "#8a8984"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.facecolor": SURF, "figure.facecolor": SURF, "axes.grid": True, "grid.color": GRID, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "axes.axisbelow": True})
DIV = LinearSegmentedColormap.from_list("div", ["#c0392b", "#f4f3ef", "#2a78d6"])
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UL = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
LABEL = {"max1": "MAX (best day)", "max5": "MAX5", "min1": "MIN (worst day)", "min5": "MIN5", "range": "Range (MAX−MIN)", "asym": "Net tail (MAX+MIN)",
         "skew": "Skewness", "ivol": "Idiosyncratic vol", "vol": "Volatility", "beta": "Beta", "r1": "Last month return", "mom": "Momentum 12-1",
         "hi52": "Near 52-week high", "lo52": "Above 52-week low", "brk55": "55-day breakout"}
FAM = {"max1": BLUE, "max5": BLUE, "skew": BLUE, "asym": BLUE, "min1": ORANGE, "min5": ORANGE, "lo52": ORANGE, "range": VIOLET, "ivol": VIOLET, "vol": VIOLET, "beta": VIOLET,
       "r1": AQUA, "mom": AQUA, "hi52": AQUA, "brk55": AQUA}
FAMNAME = [(BLUE, "up-tail / lottery"), (ORANGE, "down-tail / falling knife"), (VIOLET, "volatility and beta"), (AQUA, "price path (reversal, momentum, highs)")]


def make(name):
    N = json.load(open(os.path.join(RES, f"nbh_{name}.json"))); t, m = N["target"], N["mirror"]; sig = N["signals"]
    cc = pd.DataFrame(N["char_corr_avg"]).loc[sig, sig]; rc = pd.DataFrame(N["ret_corr_avg"]).loc[sig, sig]
    # 1. 360 map
    fig, ax = plt.subplots(figsize=(8.6, 6.6))
    for k in sig:
        x, y = cc.loc[k, t], cc.loc[k, m]
        ax.scatter(x, y, s=120 if k in (t, m) else 70, color=FAM[k], edgecolor=SURF, linewidth=1.5, zorder=3)
        ax.annotate(LABEL[k], (x, y), xytext=(6, 4), textcoords="offset points", fontsize=8.5, color=INK)
    ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
    ax.plot([-1, 1], [1, -1], ls=":", color=GREY, lw=1); ax.text(-0.72, 0.58, f"if {LABEL[t].split(' (')[0]} and {LABEL[m].split(' (')[0]} were exact\nmirrors, every signal would\nsit on the dotted line", fontsize=8, color=GREY)
    ax.set_xlim(-0.75, 1.15); ax.set_ylim(-0.95, 1.15)
    ax.set_xlabel(f"likeness to {LABEL[t]}: average cross-sectional rank correlation"); ax.set_ylabel(f"likeness to {LABEL[m]}")
    for col, lab in FAMNAME:
        ax.scatter([], [], color=col, label=lab)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    ax.set_title(f"360° map: which stocks does each signal pick? (six universes, 2013–2026)", loc="left", fontsize=11)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, f"nbh_{name}_map.png"), dpi=150); plt.close(fig)
    # 2. return correlation heatmap
    order = [k for k in sig]
    fig, ax = plt.subplots(figsize=(8.4, 7))
    im = ax.imshow(rc.loc[order, order].values, cmap=DIV, vmin=-1, vmax=1)
    ax.set_xticks(range(len(order))); ax.set_xticklabels([LABEL[k] for k in order], rotation=60, ha="right", fontsize=8)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([LABEL[k] for k in order], fontsize=8); ax.grid(False)
    for i in range(len(order)):
        for j in range(len(order)):
            v = rc.loc[order[i], order[j]]; ax.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=6.5, color=INK if abs(v) < 0.6 else "white")
    ax.set_title("Correlation of the long/short returns (average over six universes)", loc="left", fontsize=11)
    fig.colorbar(im, ax=ax, fraction=0.035); fig.tight_layout(); fig.savefig(os.path.join(FIG, f"nbh_{name}_retcorr.png"), dpi=150); plt.close(fig)
    # 3. CAPM alpha heatmap (signal x universe) with t in cells
    A = pd.DataFrame({R: {k: N["per"][R]["perf"][k]["alpha"] * 100 for k in sig} for R in U}).loc[sig]
    Tt = pd.DataFrame({R: {k: N["per"][R]["perf"][k]["t_alpha"] for k in sig} for R in U}).loc[sig]
    fig, ax = plt.subplots(figsize=(7.6, 7))
    im = ax.imshow(A.values, cmap=DIV, vmin=-15, vmax=15, aspect="auto")
    ax.set_xticks(range(len(U))); ax.set_xticklabels([UL[R] for R in U]); ax.set_yticks(range(len(sig))); ax.set_yticklabels([LABEL[k] for k in sig], fontsize=8.5); ax.grid(False)
    for i in range(len(sig)):
        for j in range(len(U)):
            a, tt = A.iloc[i, j], Tt.iloc[i, j]
            ax.text(j, i, f"{a:+.0f}\n({tt:.1f})" + ("*" if abs(tt) >= 2 else ""), ha="center", va="center", fontsize=7, color=INK)
    ax.set_title("CAPM alpha of each top-minus-bottom sort, % a year (t); * = |t| ≥ 2", loc="left", fontsize=10.5)
    fig.colorbar(im, ax=ax, fraction=0.04); fig.tight_layout(); fig.savefig(os.path.join(FIG, f"nbh_{name}_alpha.png"), dpi=150); plt.close(fig)
    # 4. double sort heatmap (pooled)
    D = np.array(N["double_sort_avg"]) * 100
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    im = ax.imshow(D, cmap="Blues", aspect="auto")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{D[i, j]:.1f}%", ha="center", va="center", fontsize=11, color=INK)
    XL = {"min1": ["deepest worst day\n(fast falling knife)", "middle", "mildest worst day"], "lo52": ["at the 52-week low\n(slow falling knife)", "middle", "far above the low"]}[m]
    YL = {"max1": ["calmest best day", "middle", "biggest best day\n(lottery)"], "brk55": ["far below the\n55-day high", "middle", "at a 55-day\nbreakout"]}[t]
    ax.set_xticks(range(3)); ax.set_xticklabels(XL, fontsize=8.5)
    ax.set_yticks(range(3)); ax.set_yticklabels(YL, fontsize=8.5); ax.grid(False)
    ax.set_title(f"Mirror test: next-month return a year, 3×3 sort\n({', '.join(UL[R] for R in N['double_sort_universes'])} averaged)", loc="left", fontsize=10.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, f"nbh_{name}_dsort.png"), dpi=150); plt.close(fig)
    # 5. up / down markets
    keys = [t, m, "range", "asym"] if name == "max" else [t, m, "hi52", "mom"]
    fig, ax = plt.subplots(figsize=(8.4, 4.2)); x = np.arange(len(keys))
    up = [np.mean([N["per"][R]["perf"][k]["up"] for R in U]) * 100 for k in keys]; dn = [np.mean([N["per"][R]["perf"][k]["down"] for R in U]) * 100 for k in keys]
    ax.bar(x - 0.2, up, 0.38, color=BLUE, label="months the market rose", edgecolor=SURF, linewidth=2)
    ax.bar(x + 0.2, dn, 0.38, color=ORANGE, label="months the market fell", edgecolor=SURF, linewidth=2)
    for i in range(len(keys)):
        ax.text(x[i] - 0.2, up[i] + (1 if up[i] >= 0 else -3), f"{up[i]:+.0f}", ha="center", fontsize=8.5, color=INK)
        ax.text(x[i] + 0.2, dn[i] + (1 if dn[i] >= 0 else -3), f"{dn[i]:+.0f}", ha="center", fontsize=8.5, color=INK)
    ax.axhline(0, color=INK2, lw=1); ax.set_xticks(x); ax.set_xticklabels([LABEL[k] for k in keys])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:.0f}%"))
    ax.legend(frameon=False, fontsize=8.5); ax.set_title("Top-minus-bottom return, annualised, by market direction (average of six universes)", loc="left", fontsize=10.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, f"nbh_{name}_updown.png"), dpi=150); plt.close(fig)


if __name__ == "__main__":
    make("max"); make("brk"); print("ok")
