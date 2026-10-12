# -*- coding: utf-8 -*-
"""Figures for Case 31. Reads ../results, writes ../figures/*.png. No number is typed in."""
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
BLUE, GREY, GREYBAND, RED = "#2a78d6", "#8a8984", "#dcdbd5", "#e34948"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 1, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.spines.left": False, "axes.axisbelow": True})
S = json.load(open(os.path.join(RES, "summary.json")))
RB = json.load(open(os.path.join(RES, "robustness_extra.json")))
tab = pd.read_csv(os.path.join(RES, "windows_by_year.csv"), index_col=0)
pct = lambda v: f"{v * 100:+.1f}%"


def rebase0(p):
    p = p.dropna(); p.columns = p.columns.astype(int)
    return (1 + p).div(1 + p[0], axis=0) - 1


# ---------- Figure 1: the hero (paths rebased at election day)
pm = rebase0(pd.read_csv(os.path.join(RES, "paths_midterm.csv"), index_col=0))
pc = rebase0(pd.read_csv(os.path.join(RES, "paths_control.csv"), index_col=0))
band = pd.read_csv(os.path.join(RES, "band_control_rebased_day0.csv"), index_col=0); band.index = band.index.astype(int)
mm, cm = pm.mean(), pc.mean()
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
bi = band.index >= -40
ax.fill_between(band.index[bi], band.q05[bi] * 100, band.q95[bi] * 100, color=GREYBAND, alpha=0.55, lw=0, label="Range of 24 random non-midterm years (5-95%)")
cm, mm = cm[cm.index >= -40], mm[mm.index >= -40]
ax.plot(cm.index, cm * 100, color=GREY, lw=2, label=f"Same date, the other {len(pc)} years")
ax.plot(mm.index, mm * 100, color=BLUE, lw=2.4, label=f"The {len(pm)} midterms, 1930-2022")
ax.axvline(0, color=INK2, lw=1)
ax.axhline(0, color=INK2, lw=0.8)
for s, c in ((mm, BLUE), (cm, GREY)):
    ax.plot([90], [s[90] * 100], "o", ms=8, color=c, mec=SURF, mew=2, zorder=5)
ax.annotate(pct(mm[90]), (90, mm[90] * 100), xytext=(8, 0), textcoords="offset points", va="center", fontsize=15, fontweight="bold", color=INK)
ax.annotate(pct(cm[90]), (90, cm[90] * 100), xytext=(8, 0), textcoords="offset points", va="center", fontsize=15, fontweight="bold", color=INK2)
ax.text(1.5, ax.get_ylim()[0] + 0.25, "Election day (next: 3 Nov 2026)", fontsize=10, color=INK2, va="bottom")
ax.set_xlim(-40, 104)
ax.set_xlabel("Trading days from US election day (early November)")
ax.set_ylabel("S&P 500, % change from election-day close")
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
fig.suptitle("Is it the midterm, or just November?", x=0.06, ha="left", fontsize=19, fontweight="bold", color=INK, y=0.975)
ax.set_title(f"90 days after a midterm the S&P 500 is up {pct(mm[90])[1:]} on average. After the same date in other years: {pct(cm[90])[1:]}.",
             loc="left", fontsize=11.5, color=INK2, pad=8)
leg = ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.97), frameon=True, facecolor=SURF, edgecolor=SURF, framealpha=1, fontsize=10, labelcolor=INK)
fig.text(0.06, 0.012, f"Permutation test p = {S['C31-1']['p_perm']:.4f} (pre-registered gate 0.025) · S&P 500 price index, Yahoo ^GSPC 1928-2026 · Henrik Gjerning",
         fontsize=8.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1.0))
fig.subplots_adjust(top=0.86)
fig.savefig(os.path.join(FIG, "fig1_midterm_vs_november.png")); plt.close(fig)

# ---------- Figure 2: every observation (strip)
M = tab[tab.kind == "midterm"]["ret[1,90]"].dropna(); C = tab[tab.kind != "midterm"]["ret[1,90]"].dropna()
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
rng = np.random.default_rng(1)
for i, (vals, c, lab) in enumerate(((C, GREY, f"Other years (n={len(C)})"), (M, BLUE, f"Midterm years (n={len(M)})"))):
    y = i + rng.uniform(-0.15, 0.15, len(vals))
    ax.scatter(vals * 100, y, s=46, color=c, edgecolor=SURF, linewidth=1.5, zorder=3)
    ax.plot([vals.mean() * 100] * 2, [i - 0.32, i + 0.32], color=INK, lw=2.4, zorder=4)
    ax.text(vals.mean() * 100, i + 0.38, f"mean {pct(vals.mean())}", ha="center", fontsize=10, color=INK)
for yr in (1934, 1938, 2002):
    ax.annotate(str(yr), (M[yr] * 100, 1), xytext=(0, -16), textcoords="offset points", ha="center", fontsize=8, color=INK2)
for yr in C.nsmallest(3).index:
    ax.annotate(str(yr), (C[yr] * 100, 0), xytext=(0, -16), textcoords="offset points", ha="center", fontsize=8, color=INK2)
ax.set_yticks([0, 1]); ax.set_yticklabels([f"Other years (n={len(C)})", f"Midterm years (n={len(M)})"])
ax.set_ylim(-0.6, 1.7); ax.axvline(0, color=INK2, lw=0.8)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.set_xlabel("S&P 500 return, election-day close to day +90")
ax.set_title(f"Each dot is one year: 21 of 24 midterm windows rose, against {S['hit_rate']['ctrl_hit'] * 100:.0f}% of other years", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_every_year.png")); plt.close(fig)

# ---------- Figure 3: horizons
hz = pd.read_csv(os.path.join(RES, "horizons.csv"))
hz = hz[hz.window != "ret[-119,0]"]
lab = {"ret[1,20]": "+20", "ret[1,60]": "+60", "ret[1,90]": "+90", "ret[1,125]": "+125", "ret[1,250]": "+250"}
x = np.arange(len(hz)); w = 0.34
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.bar(x - w / 2 - 0.01, hz.mid_mean * 100, w, color=BLUE, label="Midterm years")
ax.bar(x + w / 2 + 0.01, hz.ctrl_mean * 100, w, color=GREY, label="Same date, other years")
ax.errorbar(x - w / 2 - 0.01, hz.mid_mean * 100, yerr=[(hz.mid_mean - hz.mid_ci_lo) * 100, (hz.mid_ci_hi - hz.mid_mean) * 100],
            fmt="none", ecolor=INK, elinewidth=1.2, capsize=3)
for i, r in enumerate(hz.itertuples()):
    ax.text(i - w / 2, r.mid_ci_hi * 100 + 0.5, pct(r.mid_mean), ha="center", fontsize=9, color=INK)
    ax.text(i + w / 2, max(r.ctrl_mean, 0) * 100 + 0.5, pct(r.ctrl_mean), ha="center", fontsize=9, color=INK2)
ax.set_xticks(x); ax.set_xticklabels([f"{lab[k]} days" for k in hz.window]); ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.set_title("The gap is not an election-night pop: it builds from December to spring", loc="left", fontsize=13, fontweight="bold", color=INK)
ax.legend(frameon=False, loc="upper left", fontsize=10)
ax.text(0, -0.2, "Bars: mean S&P 500 return from election-day close. Whiskers: bootstrap 95% CI of the midterm mean.", transform=ax.transAxes, fontsize=8.5, color=MUTED)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_horizons.png")); plt.close(fig)

# ---------- Figure 4: what 2026 needs
g = S["forward_2026"]["grid"]; r26 = np.array(g["r26"]) * 100; pw = np.array(g["p_welch"])
be = RB["r26_welch_breakeven"] * 100; st = RB["r26_range_that_strengthens"][0] * 100
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.plot(r26, pw, color=BLUE, lw=2.2)
ax.axhline(0.025, color=RED, lw=1.2); ax.text(39, 0.0262, "pre-registered gate p = 0.025", ha="right", fontsize=9, color=INK2)
ax.axhline(RB["welch_p_now"], color=GREY, lw=1); ax.text(39, RB["welch_p_now"] + 0.0012, f"today, 24 midterms: p = {RB['welch_p_now']:.4f}", ha="right", fontsize=9, color=INK2)
ax.axvspan(r26.min(), be, color="#f6d7d6", alpha=0.6, lw=0); ax.text(be + 1, 0.034, f"← 2026 below {be:.0f}%:\n    the pass is lost", ha="left", fontsize=10, color=INK)
ax.axvline(st, color=INK2, lw=0.8, ls=(0, (2, 2))); ax.text(st + 1, 0.034, f"above {st:+.1f}%:\nthe evidence gets stronger", fontsize=10, color=INK)
ax.set_xlim(r26.min(), 40); ax.set_ylim(0, 0.04)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.set_xlabel("S&P 500 return, 3 Nov 2026 close to day +90 (mid-March 2027)")
ax.set_ylabel("One-sided p, 25 midterms (Welch approximation)")
ax.set_title("What the 2026 midterm has to do", loc="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig4_what_2026_needs.png")); plt.close(fig)
print("figures written")


# ---------- Figure 5 (version 2, after external review): decay and recessions. Reported, not gated.
_v2p = os.path.join(RES, "v2_checks.json")
if os.path.exists(_v2p):
    V2 = json.load(open(_v2p)); rr = pd.read_csv(os.path.join(RES, "v2_rolling26.csv"))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4), dpi=200, gridspec_kw={"width_ratios": [1.5, 1]})
    a1.plot(rr.end, rr["diff"] * 100, color=BLUE, lw=2.2)
    a1.axhline(S["C31-1"]["diff"] * 100, color=GREY, lw=1, ls="--")
    a1.text(1972, S["C31-1"]["diff"] * 100 - 0.35, f"Whole sample {pct(S['C31-1']['diff'])[:-1]} pts", color=INK2, fontsize=9.5, va="top")
    a1.axhline(0, color=INK2, lw=0.8)
    a1.set_xlabel("Last year of the 26-year window (about six midterms each)")
    a1.set_ylabel("Midterm minus control, +90 days (pts)")
    a1.set_title("Rolling 26-year gap: positive in every window, smaller lately", loc="left", fontsize=11.5, color=INK)
    R = V2["recessions"]["recession_at_election"]
    lab2 = ["Recession at the vote", "No recession"]
    xm = np.arange(2)
    a2.bar(xm - 0.18, [R["mid_rec"] * 100, R["mid_norec"] * 100], 0.36, color=BLUE, label="Midterm years")
    a2.bar(xm + 0.18, [R["ctrl_rec"] * 100, R["ctrl_norec"] * 100], 0.36, color=GREY, label="Control years")
    for x, vv in zip(list(xm - 0.18) + list(xm + 0.18), [R["mid_rec"], R["mid_norec"], R["ctrl_rec"], R["ctrl_norec"]]):
        a2.text(x, vv * 100 + (0.4 if vv >= 0 else -0.4), pct(vv), ha="center", va="bottom" if vv >= 0 else "top", fontsize=10, color=INK)
    a2.set_xticks(xm, [f"{lab2[0]}\n({len(R['mid_years_with'])} vs {R['n_ctrl_rec']} years)", f"{lab2[1]}\n({R['excl_n_mid']} vs {R['excl_n_ctrl']} years)"])
    a2.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(4)); a2.set_ylim(-6, 18)
    a2.axhline(0, color=INK2, lw=0.8); a2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    a2.set_title("Recession years carry much of the gap", loc="left", fontsize=11.5, color=INK)
    a2.legend(frameon=False, fontsize=9.5, loc="upper right", bbox_to_anchor=(1, 0.93))
    fig.suptitle("When the midterm gap was earned", x=0.03, ha="left", fontsize=16, fontweight="bold", color=INK)
    fig.text(0.03, 0.01, "NBER recession dates · S&P 500 price index, +1 to +90 trading days after election day · reported, not gated · Henrik Gjerning",
             fontsize=8.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94)); fig.savefig(os.path.join(FIG, "fig5_v2_decay_recessions.png")); plt.close(fig)
