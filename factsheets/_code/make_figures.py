# -*- coding: utf-8 -*-
import json, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import data, perf
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results"); FIG = os.environ.get("FS_FIGURES") or os.path.join(HERE, "..", "figures")
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8984"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF, "axes.grid": True, "grid.color": GRID,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False, "axes.axisbelow": True, "lines.linewidth": 2})
ORDER = data.REGIONS
LAB = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}


def growth_grid(series, cols, labels, colors, fname, title, freq="D"):
    fig, axs = plt.subplots(2, 3, figsize=(12, 6.6), sharex=True)
    for ax, R in zip(axs.flat, ORDER):
        S = series[R]
        for c, l, col in zip(cols, labels, colors):
            s = S[c].dropna()
            w = (1 + s).cumprod()
            ax.plot(w.index, w.values, color=col, lw=2 if col != GREY else 1.6, label=l)
            ax.annotate(f"{w.iloc[-1]:.1f}x", (w.index[-1], w.iloc[-1]), xytext=(4, 0), textcoords="offset points", fontsize=8, color=INK2, va="center")
        ax.set_yscale("log"); ax.set_title(LAB[R], loc="left", fontsize=11, color=INK, fontweight="bold")
        ax.axhline(1, color=INK2, lw=0.8)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}"))
    axs.flat[0].legend(frameon=False, fontsize=8.5, loc="upper left")
    fig.suptitle(title, x=0.01, ha="left", fontsize=13, color=INK, fontweight="bold")
    fig.text(0.01, 0.005, "Growth of 1, log scale, local currency, net of costs. Henrik Gjerning · Project 10 factsheets", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 0.96)); fig.savefig(os.path.join(FIG, fname), dpi=150); plt.close(fig)


def dd_grid(series, cols, labels, colors, fname, title):
    fig, axs = plt.subplots(2, 3, figsize=(12, 6), sharex=True, sharey=True)
    for ax, R in zip(axs.flat, ORDER):
        for c, l, col in zip(cols, labels, colors):
            s = series[R][c].dropna(); d = perf.drawdown(s) * 100
            ax.plot(d.index, d.values, color=col, lw=1.6, label=l)
        ax.set_title(LAB[R], loc="left", fontsize=11, color=INK, fontweight="bold")
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:.0f}%"))
    axs.flat[0].legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.suptitle(title, x=0.01, ha="left", fontsize=13, color=INK, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(os.path.join(FIG, fname), dpi=150); plt.close(fig)


def turtle_figs():
    S = pd.read_pickle(os.path.join(RES, "turtle_series.pkl"))
    cols = ["Turtle L/S (S1+S2)", "Turtle long-only (S1+S2)", "EW universe (benchmark)"]
    labs = ["Turtle long/short", "Turtle long-only", "Equal-weight universe"]
    growth_grid(S, cols, labs, [BLUE, ORANGE, GREY], "fs01_fig1_growth.png", "Turtle rules on six stock universes, 2013–2026")
    dd_grid(S, cols, labs, [BLUE, ORANGE, GREY], "fs01_fig2_drawdown.png", "Drawdown from the previous peak")
    # trade distribution pooled
    tl = pd.concat([pd.read_csv(os.path.join(RES, f"turtle_trades_{R}.csv")).assign(u=R) for R in ORDER])
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
    x = tl.R.clip(-6, 40)
    axs[0].hist(x, bins=np.arange(-6, 41, 1), color=BLUE, edgecolor=SURF, linewidth=1)
    axs[0].axvline(0, color=INK2, lw=1)
    axs[0].set_title("Trade outcome in R (1R = risk of the first unit, 2N)", loc="left", fontsize=11)
    axs[0].set_ylabel("trades"); axs[0].set_xlabel("R multiple (clipped at -6 and +40)")
    s = tl.sort_values("pnl_pct", ascending=False).pnl_pct.values; cum = np.cumsum(s)
    share = np.arange(1, len(s) + 1) / len(s) * 100
    axs[1].plot(share, cum * 100 / len(ORDER), color=BLUE)
    axs[1].axhline(0, color=INK2, lw=1)
    k = np.argmax(cum); axs[1].annotate(f"best {share[k]:.0f}% of trades\n= peak cumulative P&L", (share[k], cum[k] * 100 / len(ORDER)), xytext=(20, -30), textcoords="offset points", fontsize=8.5, color=INK2, arrowprops=dict(arrowstyle="-", color=INK2))
    axs[1].set_title("Cumulative P&L, trades sorted best to worst (avg per universe)", loc="left", fontsize=11)
    axs[1].set_xlabel("% of trades"); axs[1].set_ylabel("% of equity")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs01_fig3_trades.png"), dpi=150); plt.close(fig)


def lottery_figs():
    S = pd.read_pickle(os.path.join(RES, "lottery_series.pkl")); J = json.load(open(os.path.join(RES, "lottery_summary.json")))
    cols = ["L/S low minus high MAX (net)", "Low-MAX long-only (net)", "EW universe (benchmark)"]
    labs = ["Low-minus-high MAX (L/S)", "Low-MAX long-only", "Equal-weight universe"]
    growth_grid(S, cols, labs, [BLUE, ORANGE, GREY], "fs02_fig1_growth.png", "The lottery factor on six stock universes, 2013–2026")
    dd_grid(S, cols, labs, [BLUE, ORANGE, GREY], "fs02_fig2_drawdown.png", "Drawdown from the previous peak")
    fig, axs = plt.subplots(2, 3, figsize=(12, 6.2))
    for ax, R in zip(axs.flat, ORDER):
        q = J[R]["quantile_ann"]; k = list(q); v = [q[i] * 100 for i in k]
        c = [BLUE if i == k[0] else ORANGE if i == k[-1] else "#b9b8b2" for i in k]
        ax.bar(range(len(k)), v, color=c, width=0.8, edgecolor=SURF, linewidth=2)
        ax.axhline(J[R]["stats"]["EW universe (benchmark)"]["ann_mean"] * 100, color=INK2, lw=1, ls="--")
        ax.set_xticks(range(len(k))); ax.set_xticklabels([i.replace("Q", "") for i in k], fontsize=8)
        ax.set_title(f"{LAB[R]}  ({len(k)} groups)", loc="left", fontsize=11, color=INK, fontweight="bold")
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:.0f}%"))
        b = J[R]["quantile_beta"]; ax.text(0.02, 0.96, f"beta {b[k[0]]:.2f} → {b[k[-1]]:.2f}", transform=ax.transAxes, fontsize=8.5, color=INK2, va="top")
    fig.suptitle("Average annual return by MAX group (1 = calmest, last = most lottery-like); dashed = universe", x=0.01, ha="left", fontsize=12, color=INK, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(os.path.join(FIG, "fs02_fig3_quantiles.png"), dpi=150); plt.close(fig)
    # beta vs return scatter
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    xs, ys = [], []
    for R in ORDER:
        b, q = J[R]["quantile_beta"], J[R]["quantile_ann"]; k = list(q)
        for i in k:
            col = BLUE if i == k[0] else ORANGE if i == k[-1] else "#b9b8b2"
            ax.scatter(b[i], q[i] * 100, s=46, color=col, edgecolor=SURF, linewidth=1.5, zorder=3)
            xs.append(b[i]); ys.append(q[i] * 100)
    p = np.polyfit(xs, ys, 1); xx = np.linspace(min(xs), max(xs), 10); ax.plot(xx, np.polyval(p, xx), color=INK2, lw=1)
    ax.set_xlabel("beta to the equal-weight universe"); ax.set_ylabel("average annual return")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:.0f}%"))
    ax.scatter([], [], color=BLUE, label="calmest group (low MAX)"); ax.scatter([], [], color=ORANGE, label="most lottery-like (high MAX)"); ax.scatter([], [], color="#b9b8b2", label="middle groups")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title(f"All MAX groups in all six universes: return lines up with beta (slope {p[0]:.1f}% per unit)", loc="left", fontsize=10.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs02_fig4_beta.png"), dpi=150); plt.close(fig)




def fix_figs():
    F = json.load(open(os.path.join(RES, "fix_summary.json"))); D = json.load(open(os.path.join(RES, "turtle_diagnostics.json")))
    T, L, C = F["turtle"], F["lottery"], F["classification"]
    # ---- FS01 diagnosis
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.2))
    cc = T["cost_check"]; ks = [k for k in ORDER if k in cc]; x = np.arange(len(ks))
    axs[0].bar(x - 0.2, [cc[k]["gross"] * 100 for k in ks], 0.38, color="#b9b8b2", label="before costs", edgecolor=SURF, linewidth=1.5)
    axs[0].bar(x + 0.2, [cc[k]["net"] * 100 for k in ks], 0.38, color=BLUE, label="after costs", edgecolor=SURF, linewidth=1.5)
    axs[0].axhline(0, color=INK2, lw=1); axs[0].set_xticks(x); axs[0].set_xticklabels([LAB[k] for k in ks])
    axs[0].set_title("A. Costs: L/S return a year, 2013–19", loc="left", fontsize=10.5); axs[0].legend(frameon=False, fontsize=8.5)
    axs[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:.0f}%"))
    x = np.arange(len(ORDER))
    st = [D[R]["pnl"]["by_reason"]["2N stop"]["pnl"] * 100 / 7 for R in ORDER]; ch = [D[R]["pnl"]["by_reason"]["channel exit"]["pnl"] * 100 / 7 for R in ORDER]
    axs[1].bar(x - 0.2, st, 0.38, color=ORANGE, label="trades closed by the 2N stop", edgecolor=SURF, linewidth=1.5)
    axs[1].bar(x + 0.2, ch, 0.38, color=BLUE, label="trades closed by the channel exit", edgecolor=SURF, linewidth=1.5)
    axs[1].axhline(0, color=INK2, lw=1); axs[1].set_xticks(x); axs[1].set_xticklabels([LAB[R] for R in ORDER], fontsize=8.5)
    axs[1].set_title("B. Stops: summed trade P&L a year, 2013–19", loc="left", fontsize=10.5); axs[1].legend(frameon=False, fontsize=8)
    axs[1].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:.0f}%"))
    qs = [5, 20, 60]
    for key, col, lab in (("idio", BLUE, "single stock, net of market"), ("stock", ORANGE, "single stock"), ("index", GREY, "equal-weight index")):
        v = [np.median([D[R]["vr"][str(q)][key] for R in ORDER]) for q in qs]
        axs[2].plot(qs, v, marker="o", ms=7, color=col, label=lab)
    axs[2].axhline(1, color=INK2, lw=1, ls="--"); axs[2].text(62, 1.005, "random walk", fontsize=8, color=INK2)
    axs[2].set_xticks(qs); axs[2].set_xlabel("horizon q (days)"); axs[2].set_ylim(0.55, 1.1)
    axs[2].set_title("C. No trend to follow: variance ratio VR(q)", loc="left", fontsize=10.5); axs[2].legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs01_fig4_diagnosis.png"), dpi=150); plt.close(fig)
    # ---- ladders
    for key, fname, title, bench in ((T, "fs01_fig5_fixes.png", "Turtle fixes, one step at a time: Sharpe ratio in the 2020–26 holdout", "EW universe"),
                                     (L, "fs02_fig5_fixes.png", "MAX fixes, one step at a time: Sharpe ratio of the long/short in the 2020–26 holdout", None)):
        steps = key["steps"]; fig, ax = plt.subplots(figsize=(10, 4.4))
        for j, s in enumerate(steps):
            v = [key["per"][R][s]["holdout"]["sharpe"] for R in ORDER]
            ax.scatter([j] * len(v), v, color="#b9b8b2", s=30, zorder=2, edgecolor=SURF)
            ax.scatter([j], [key["avg_holdout"][s]["sharpe"]], color=BLUE, s=90, zorder=3, edgecolor=SURF, linewidth=2)
            ax.annotate(f"{key['avg_holdout'][s]['sharpe']:.2f}", (j, key["avg_holdout"][s]["sharpe"]), xytext=(10, -3), textcoords="offset points", fontsize=9, color=INK)
        if bench:
            b = key["avg_holdout"][bench]["sharpe"]; ax.axhline(b, color=INK2, ls="--", lw=1); ax.text(0.35, b + 0.04, f"equal-weight universe {b:.2f}", fontsize=8.5, color=INK2, ha="left")
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_xticks(range(len(steps))); ax.set_xticklabels([s.replace(" + ", "\n+ ", 1) for s in steps], fontsize=8.5)
        ax.scatter([], [], color=BLUE, label="six-universe average book"); ax.scatter([], [], color="#b9b8b2", label="single universe"); ax.legend(frameon=False, fontsize=8.5, loc="upper left")
        ax.set_title(title, loc="left", fontsize=11); fig.tight_layout(); fig.savefig(os.path.join(FIG, fname), dpi=150); plt.close(fig)
    # ---- classification map (JKP universes only: US, UK, DK, World)
    fig, ax = plt.subplots(figsize=(8, 5.6))
    style = {"Turtle L/S": (BLUE, "o"), "Turtle long-only": (BLUE, "s"), "Turtle fixed (T3)": (BLUE, "^"), "MAX L/S": (ORANGE, "o"), "MAX beta-neutral (L1)": (ORANGE, "^")}
    for n, (col, mk) in style.items():
        pts = [(C[n][R]["corr"]["momentum"], C[n][R]["corr"]["low_risk"]) for R in ["US", "UK", "DK", "WD"]]
        ax.scatter(*zip(*pts), color=col, marker=mk, s=70, edgecolor=SURF, linewidth=1.5, label=n, zorder=3)
    ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
    ax.set_xlabel("correlation with JKP momentum theme"); ax.set_ylabel("correlation with JKP low-risk theme")
    ax.text(0.98, 0.02, "trend / momentum", transform=ax.transAxes, ha="right", fontsize=9, color=INK2)
    ax.text(0.02, 0.97, "defensive / low risk", transform=ax.transAxes, va="top", fontsize=9, color=INK2)
    ax.text(0.02, 0.02, "high beta, high volatility", transform=ax.transAxes, fontsize=9, color=INK2)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right"); ax.set_xlim(-0.35, 0.75); ax.set_ylim(-0.7, 1.0)
    ax.set_title("Where the books sit in factor space (US, UK, DK, World; monthly 2013–2025)", loc="left", fontsize=10.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs_class_map.png"), dpi=150); plt.close(fig)


if __name__ == "__main__":
    import sys
    if "fix" in sys.argv: fix_figs()
    else: turtle_figs(); lottery_figs(); fix_figs()
    print(sorted(os.listdir(FIG)))
