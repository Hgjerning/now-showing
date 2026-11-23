# -*- coding: utf-8 -*-
"""Minority Report, Part 2: The Slow Print (Now Showing No. 8½, 1 Dec 2026). Written 15 Nov 2026.
Text source: article/minority_report_part2_slow_print_DRAFT_2026-11-08.md  (edit the words THERE).
1) copies the portfolio-level results of the pre-registered run (8 Nov 2026) from Factsheets/_data_private/a31_runs/out_U1_slow
   into results/slow_print/ (summaries and monthly book series only; no per-stock data);
2) rebuilds every number in the text from those files and stops if one differs;
3) draws the figures and the two posters, writes article/minority_report_part2.{md,html}, the one-pager and the PDFs
   (PDFs where Playwright is installed, i.e. on Windows).
Run:  python build_part2.py            (add --check to only check the numbers)
Computes nothing new except straight cost lines (net = gross - 12 x turnover x cost per trade), flat-cost differences
against the fast book (Newey-West, 3 lags) and growth of 1."""
import glob
import json
import os
import shutil
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "_shared", "lib10"))
from common import click_layout, make_pdfs, write_article, write_teaser  # noqa: E402

P10 = os.path.dirname(os.path.dirname(ROOT))
RUN = os.path.join(P10, "Factsheets", "_data_private", "a31_runs", "out_U1_slow")
RES = os.path.join(ROOT, "results", "slow_print"); FIG = os.path.join(ROOT, "figures")
SRC = os.path.join(ROOT, "article", "minority_report_part2_slow_print_DRAFT_2026-11-08.md")
STEM = "minority_report_part2"; REPO = "hgjerning.github.io/now-showing/the-slow-print"

# ---------------------------------------------------------------- 1) results into the article folder
os.makedirs(RES, exist_ok=True)
if os.path.isdir(RUN):
    for f in ["slow_print_results.json"] + [os.path.basename(p) for p in glob.glob(os.path.join(RUN, "monthly_S-*.csv"))]:
        shutil.copy2(os.path.join(RUN, f), os.path.join(RES, f))
D = json.load(open(os.path.join(RES, "slow_print_results.json"), encoding="utf-8"))
M = {k: pd.read_csv(os.path.join(RES, f"monthly_{k}.csv"), index_col=0, parse_dates=True) for k in ("S-1", "S-2", "S-3")}
U1 = os.path.join(ROOT, "results", "U1")
BG = pd.read_csv(os.path.join(U1, "gross_monthly.csv"), index_col=0, parse_dates=True)["Ensemble"]
BT = pd.read_csv(os.path.join(U1, "turnover_monthly.csv"), index_col=0, parse_dates=True)["Ensemble"]
BN = pd.read_csv(os.path.join(U1, "net_monthly.csv"), index_col=0, parse_dates=True)["Ensemble"]   # net at flat 0.50%
SO = pd.read_csv(os.path.join(U1, "simple_sorts.csv"), index_col=0)
text = open(SRC, encoding="utf-8").read()


def nw_t(x, lags=3):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x); e = x - x.mean(); v = e @ e / n
    for k in range(1, lags + 1): v += 2 * (1 - k / (lags + 1)) * (e[k:] @ e[:-k]) / n
    return x.mean() / np.sqrt(v / n)


pc = lambda v: f"{v * 100:+.1f}%"; t2 = lambda v: f"{v:.2f}"; to = lambda v: f"{v * 100:.0f}%"; p0 = lambda v: f"{v * 100:.0f}%"
b, T, CS, GR = D["base_ART"], D["trials"], D["reported"]["cost_sensitivity"], D["reported"]["grids"]
IC, MO = D["reported"]["alpha_decay_ic"], D["reported"]["momentum"]
K = ["S-1", "S-2", "S-3"]
cost_yr = {k: T[k]["gross_ann"] - T[k]["net_ann"] for k in K}; cost_yr["base"] = b["gross_ann"] - b["net_ann"]
per_trade = {k: cost_yr[k] / (12 * T[k]["turnover_m"]) for k in K}; per_trade["base"] = cost_yr["base"] / (12 * b["turnover_m"])
cross = {k: (b["gross_ann"] - T[k]["gross_ann"]) / (12 * (b["turnover_m"] - T[k]["turnover_m"])) for k in K}
# flat 0.50%: slow minus fast, month by month (fast = Part 1's net at 0.50%)
dflat = {}
for k in K:
    s = (M[k]["gross"] - 0.005 * M[k]["turnover"]).reindex(BN.index)
    d = (s - BN).dropna(); dflat[k] = (d.mean() * 12, nw_t(d))
gp = SO.loc["Profitability (GP/A)"]
fell_gross = [1 - T[k]["alpha_kept"] for k in K]; fell_to = [1 - T[k]["turnover_kept"] for k in K]
cs = lambda k, key: f"{pc(CS[k][key]['net_ann'])} ({t2(CS[k][key]['net_t'])})"

# ---------------------------------------------------------------- 2) every number in the text
C = []
for k, lab in zip(K, ["| A31-S-1 | S1 partial trading, 50% |", "| A31-S-2 | S2 buffer, 10% in / 30% out |", "| A31-S-3 | S3 three-month smoothed signal |"]):
    h = T[k]["holm"]
    C.append((f"T1 {k}", f"{lab} {pc(T[k]['net_ann'])} | {t2(T[k]['net_t'])} | {T[k]['p_one_sided']:.3f} | {h['bar']:.3f} | fail |"))
C.append(("T2 base", f"| Fast book (Part 1) | {pc(b['gross_ann'])} | {to(b['turnover_m'])} | {cost_yr['base'] * 100:.1f}% | **{pc(b['net_ann'])}** | {t2(b['net_t'])} | {t2(b['net_sharpe'])} | 100% | 100% | {b['breakeven_cost'] * 100:.2f}% |"))
for k, lab in zip(K, ["S1 partial 50%", "S2 buffer 10/30", "S3 smoothed, 3 months"]):
    r = T[k]
    C.append((f"T2 {k}", f"| {lab} | {pc(r['gross_ann'])} | {to(r['turnover_m'])} | {cost_yr[k] * 100:.1f}% | {pc(r['net_ann'])} | {t2(r['net_t'])} | {t2(r['net_sharpe'])} | {p0(r['alpha_kept'])} | {p0(r['turnover_kept'])} | {r['breakeven_cost'] * 100:.2f}% |"))
rows3 = [("ART_x0.5", "| Live-fill ×0.5 (about 0.17% per trade) |"), ("ART_DKK1m", "| Live-fill, book DKK 1m |"),
         ("ART_DKK100m", "| Live-fill, book DKK 100m |"), ("flat0.40", "| Flat 0.40% |"), ("flat0.50", "| Flat 0.50% (Part 1) |"),
         ("ART_x2", "| Live-fill ×2 (about 0.67% per trade) |")]
for key, lab in rows3:
    vals = [cs(k, key) for k in ["base"] + K]
    C.append((f"T3 {key}", lab + " " + " | ".join(vals)))       # bold marks are checked by value below
C += [
    ("summary range", f"**{pc(min(T[k]['net_ann'] for k in K))} to {pc(max(T[k]['net_ann'] for k in K))} a year after costs estimated from live fills (t {t2(min(T[k]['net_t'] for k in K))} to {t2(max(T[k]['net_t'] for k in K))})**"),
    ("summary fast", f"({pc(b['net_ann'])} a year, t {t2(b['net_t'])}; reported, not a trial"),
    ("summary crossover", f"Above about {min(cross.values()) * 100:.2f}-{max(cross.values()) * 100:.2f}% per trade"),
    ("summary double", f"the fast book is left with {pc(CS['base']['ART_x2']['net_ann'])} a year, partial trading with {pc(CS['S-1']['ART_x2']['net_ann'])} and the buffer, which trades least, with {pc(CS['S-2']['ART_x2']['net_ann'])}"),
    ("recap", f"**{pc(b['gross_ann'])} a year before costs (t {t2(b['gross_t'])})**"),
    ("recap turnover", f"**{to(b['turnover_m'])} of its capital a month**"),
    ("recap net", f"left {pc(CS['base']['flat0.50']['net_ann'])} a year (t {t2(CS['base']['flat0.50']['net_t'])})"),
    ("per trade", f"averages **{min(per_trade[k] for k in K + ['base']) * 100:.2f}-{max(per_trade[k] for k in K + ['base']) * 100:.2f}% per trade**"),
    ("fell", f"turnover fell by {min(fell_to) * 100:.0f}-{max(fell_to) * 100:.0f}%, gross by {min(fell_gross) * 100:.0f}-{max(fell_gross) * 100:.0f}%"),
    ("S1 trade-off", f"S1 saves {(cost_yr['base'] - cost_yr['S-1']) * 100:.1f} points a year in costs and gives up {(b['gross_ann'] - T['S-1']['gross_ann']) * 100:.1f} points of signal"),
    ("minus base", f"S1 is {abs(T['S-1']['minus_base_net_ann']) * 100:.1f} points a year behind (t {t2(T['S-1']['minus_base_t'])}), S2 {abs(T['S-2']['minus_base_net_ann']) * 100:.1f} behind (t {t2(T['S-2']['minus_base_t'])}), S3 {abs(T['S-3']['minus_base_net_ann']) * 100:.1f} behind (t {t2(T['S-3']['minus_base_t'])})"),
    ("crossovers", f"S1 overtakes the fast book at about **{cross['S-1'] * 100:.2f}% per trade**, S3 at about {cross['S-3'] * 100:.2f}% and S2 at about {cross['S-2'] * 100:.2f}%"),
    ("flat diffs", f"at a flat 0.50% they are {pc(dflat['S-1'][0])[:-1]} (t {t2(dflat['S-1'][1])}), {pc(dflat['S-2'][0])[:-1]} (t {t2(dflat['S-2'][1])}) and {pc(dflat['S-3'][0])[:-1]} points (t {t2(dflat['S-3'][1])})"),
    ("IC", "| Mean rank IC | " + " | ".join(f"{IC[str(h)]:.3f}" for h in range(1, 7)) + " |"),
    ("IC share", "| Share of month 1 | " + " | ".join(f"{IC[str(h)] / IC['1'] * 100:.0f}%" for h in range(1, 7)) + " |"),
    ("grid S1", f"| Net a year (live-fill) | {pc(GR['S1_a0.25']['net_ann'])} | {pc(T['S-1']['net_ann'])} | {pc(GR['S1_a0.75']['net_ann'])} | {pc(b['net_ann'])} |"),
    ("grid S2", f"| Net a year (live-fill) | {pc(GR['S2_exit0.20']['net_ann'])} | {pc(T['S-2']['net_ann'])} | {pc(GR['S2_exit0.40']['net_ann'])} |"),
    ("grid S3", f"| Net a year (live-fill) | {pc(b['net_ann'])} | {pc(GR['S3_n2']['net_ann'])} | {pc(T['S-3']['net_ann'])} | {pc(GR['S3_n6']['net_ann'])} |"),
    ("2017", f"the fast book earned {pc(b['net_ann_2017'])} a year after live-fill costs (t {t2(b['net_t_2017'])}) and the slow variants {pc(min(T[k]['net_ann_2017'] for k in K))} to {pc(max(T[k]['net_ann_2017'] for k in K))}"),
    ("halves", f"fast book {pc(b['net_ann_h1'])} / {pc(b['net_ann_h2'])}; S1 {pc(T['S-1']['net_ann_h1'])} / {pc(T['S-1']['net_ann_h2'])}; S2 {pc(T['S-2']['net_ann_h1'])} / {pc(T['S-2']['net_ann_h2'])}; S3 {pc(T['S-3']['net_ann_h1'])} / {pc(T['S-3']['net_ann_h2'])}"),
    ("momentum", f"earns {pc(MO['base']['gross_ann'])} a year gross and {pc(MO['base']['net_ann'])} a year after live-fill costs (t {t2(MO['base']['net_t'])}); slowing it leaves it between {pc(max(MO[k]['net_ann'] for k in K))} and {pc(min(MO[k]['net_ann'] for k in K))}"),
    ("profitability", f"(+{gp.net_ann * 100:.1f}% a year, t {gp.net_t:.2f}; reported"),
    ("answer 1", f"Partial trading: {pc(T['S-1']['net_ann'])} a year after live-fill costs (t {t2(T['S-1']['net_t'])}), against {pc(T['S-3']['net_ann'])} for the smoothed signal and {pc(T['S-2']['net_ann'])} for the buffer"),
    ("answer 2", f"the fast book earned {pc(b['net_ann'])} a year (t {t2(b['net_t'])}; reported, not a trial)"),
    ("answer 3", f"Above about {cross['S-1'] * 100:.2f}% per trade for partial trading, {cross['S-3'] * 100:.2f}% for smoothing and {cross['S-2'] * 100:.2f}% for the buffer"),
    ("verdict", f"0 of 3 passed (S-1 t {t2(T['S-1']['net_t'])}, S-2 t {t2(T['S-2']['net_t'])}, S-3 t {t2(T['S-3']['net_t'])}; Holm bars not reached)"),
    ("verdict IC", f"IC still {IC['6'] / IC['1'] * 100:.0f}% of its first-month level after six months"),
    ("months", f"({b['months']} months)"),
]
TX = text.replace("**", "")
bad = [(w, s) for w, s in C if s not in text and s not in TX]
flags = {"no trial passed": not any(T[k]["holm"]["passes"] for k in K),
         "S-2 trades least": T["S-2"]["turnover_m"] == min(T[k]["turnover_m"] for k in K),
         "every slow book trails profitability at 0.50%": all(CS[k]["flat0.50"]["net_ann"] < gp.net_ann for k in K),
         "no slow-minus-fast difference significant at 0.50%": all(abs(v[1]) < 1.96 for v in dflat.values()),
         "no former-employer names or trade count in the text": not any(w in text for w in ("ATP", " ART ", "ART live", "65,920", "2009 to 2013")),
         "fast-book rows of Table 3 match Part 1's flat 0.50% series": abs(BN.mean() * 12 - CS["base"]["flat0.50"]["net_ann"]) < 5e-4}
print(f"number check: {len(C) - len(bad)} of {len(C)} strings match the result files; {sum(flags.values())} of {len(flags)} facts hold")
for w, s in bad: print("  NOT IN TEXT:", w, "->", s)
for k, v in flags.items():
    if not v: print("  FALSE:", k)
if bad or not all(flags.values()):
    sys.exit("build stopped: fix the text or the check first")
if "--check" in sys.argv: sys.exit(0)

# ---------------------------------------------------------------- 3) figures and posters
from common import BLUE, GREY, INK, INK2, ORANGE, AQUA, mpl_style  # noqa: E402
from poster import BOLD, DIM, poster  # noqa: E402
from poster import INK as PINK  # noqa: E402
mpl_style(plt); os.makedirs(FIG, exist_ok=True)
NAMES = {"base": "Fast book (Part 1)", "S-1": "S1 partial trading", "S-2": "S2 buffer", "S-3": "S3 smoothed signal"}
COL = {"base": INK, "S-1": BLUE, "S-2": ORANGE, "S-3": AQUA}
gross = {"base": b["gross_ann"], **{k: T[k]["gross_ann"] for k in K}}; turn = {"base": b["turnover_m"], **{k: T[k]["turnover_m"] for k in K}}

# Figure 1: net return against a flat cost per trade (straight lines), live-fill average and Part 1's 0.50% marked
c = np.linspace(0, 0.008, 81)
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=200)
for k in ["base"] + K:
    ax.plot(c * 100, (gross[k] - 12 * turn[k] * c) * 100, color=COL[k], lw=2.4 if k == "base" else 1.8, label=NAMES[k])
lo, hi = min(per_trade.values()), max(per_trade.values())
ax.axvspan(lo * 100, hi * 100, color=GREY, alpha=0.18, lw=0); ax.text((lo + hi) / 2 * 100, 15.6, "live-fill\naverage", ha="center", va="top", fontsize=9.5, color=INK2)
ax.axvline(0.5, color=INK2, lw=0.9, ls="--"); ax.text(0.51, 15.6, "Part 1's\n0.50%", va="top", fontsize=9.5, color=INK2)
ax.axhline(0, color=INK2, lw=0.8)
ax.set_xlabel("Cost per trade, % (one-way, flat)"); ax.set_ylabel("Net return a year, %"); ax.set_xlim(0, 0.8); ax.set_ylim(-6, 16.5)
ax.legend(frameon=False, loc="lower left", fontsize=10)
ax.set_title("Fast wins while trading is cheap; slower books lose less as costs rise", loc="left", fontsize=12.5, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "p2_fig1_cost_lines.png")); plt.close(fig)

# Figure 2: growth of 1 after live-fill costs, the three slow books (the fast book's live-fill series was not saved)
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
for k in K:
    g = (1 + M[k]["net_art"]).cumprod(); ax.plot(g.index, g.values, color=COL[k], lw=1.8, label=f"{NAMES[k]} ({g.iloc[-1]:.1f})")
ax.set_yscale("log"); ax.set_yticks([1, 1.5, 2, 3, 4, 6]); ax.set_yticklabels(["1", "1.5", "2", "3", "4", "6"]); ax.yaxis.set_minor_formatter(plt.NullFormatter()); ax.set_ylabel("Growth of 1 after live-fill costs (log scale)"); ax.legend(frameon=False, loc="upper left", fontsize=10)
ax.set_title("Slow books after live-fill costs: a long climb to 2025, then a sharp fall", loc="left", fontsize=12.5, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "p2_fig2_growth.png")); plt.close(fig)

# Figure 3: how long the prediction lasts (rank IC by horizon)
fig, ax = plt.subplots(figsize=(10, 4.0), dpi=200)
hs = list(range(1, 7)); v = [IC[str(h)] for h in hs]
ax.bar(hs, v, color=BLUE, width=0.6)
for h, x in zip(hs, v): ax.text(h, x + 0.0015, f"{x / v[0] * 100:.0f}%", ha="center", fontsize=10, color=INK)
ax.set_xticks(hs); ax.set_xlabel("Months ahead"); ax.set_ylabel("Mean rank IC"); ax.set_ylim(0, 0.075)
ax.set_title("The ranking fades slowly: 71% of its month-1 strength is left at month 3", loc="left", fontsize=12.5, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "p2_fig3_ic_decay.png")); plt.close(fig)

GOLDC = "#f5b301"
STARS = "STARRING  PARTIAL TRADING · A BUFFER · A SMOOTHED SIGNAL\nAND THE COST PER TRADE AS THE JUDGE"


def draw(ax, acc):
    lab = ["FAST", "S1", "S2", "S3"]; ks = ["base"] + K; x = np.arange(4); w = 0.36
    a = [(CS[k]["ART_x0.5"] if False else None) for k in ks]  # noqa: F841
    live = [b["net_ann"]] + [T[k]["net_ann"] for k in K]; dbl = [CS[k]["ART_x2"]["net_ann"] for k in ks]
    ax.bar(x - w / 2, [v * 100 for v in live], w, color=acc); ax.bar(x + w / 2, [v * 100 for v in dbl], w, color=GOLDC)
    for i in range(4):
        for vv, dx, col in ((live[i], -w / 2, acc), (dbl[i], w / 2, GOLDC)):
            ax.text(i + dx, vv * 100 + 0.3, f"{vv * 100:+.1f}%", ha="center", va="bottom", color=col, fontproperties=BOLD, fontsize=15)
    ax.axhline(0, color=DIM, lw=1.2); ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=16); ax.set_yticks([]); ax.grid(False); ax.set_ylim(-1, 12)
    ax.text(-0.45, 11.3, "LIVE-FILL COSTS", color=acc, fontproperties=BOLD, fontsize=16); ax.text(-0.45, 10.1, "COSTS × 2", color=GOLDC, fontproperties=BOLD, fontsize=16)
    ax.text(-0.45, 9.1, "net a year, 2004-2026", color=DIM, fontsize=12.5)


poster(os.path.join(FIG, "hero_minority_report_part2.png"), "8½", "MINORITY\nREPORT", "Part 2: The Slow Print", draw, STARS,
       "RATED  0 OF 3  ·  SLOWING IS INSURANCE, NOT ALPHA", "IN CINEMAS 1 DECEMBER 2026", accent="#3987e5")


def draw_teaser(ax, acc):
    ks = ["base"] + K; lab = ["Fast book", "S1 partial", "S2 buffer", "S3 smoothed"]
    ax.barh(range(4), [turn[k] * 100 for k in ks], color=acc, height=0.6)
    ax.set_yticks(range(4)); ax.set_yticklabels(lab, fontsize=14); ax.set_xlim(0, 260); ax.set_xticks([]); ax.grid(False); ax.invert_yaxis()
    for i, k in enumerate(ks): ax.text(turn[k] * 100 + 4, i, f"{turn[k] * 100:.0f}%", va="center", color=acc, fontproperties=BOLD, fontsize=14)
    ax.text(258, -0.75, "share of the book traded a month", color=DIM, fontsize=12, ha="right")
    ax.text(205, 2.6, "DOES SLOWER\nKEEP MORE?", ha="center", va="center", color=PINK, fontproperties=BOLD, fontsize=20)


poster(os.path.join(FIG, "hero_minority_report_part2_teaser.png"), "8½", "MINORITY\nREPORT", "Part 2: Three ways to trade slower. One bill.", draw_teaser, STARS,
       "RATED  THREE PRE-REGISTERED TESTS  ·  THE VERDICT IS IN THE ARTICLE", "IN CINEMAS 1 DECEMBER 2026", accent="#3987e5", ax_left=0.30)

# Teaser drawing: three hourglasses with the three questions (original drawing)
INKD, INK2D, ACC, GOLD, BGC = "#0b0b0b", "#52514e", "#2a78d6", "#c9a227", "#fcfcfb"
fig, ax = plt.subplots(figsize=(4.2, 5.0), dpi=200); fig.patch.set_facecolor(BGC); ax.set_facecolor(BGC)
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
ax.text(5.0, 11.2, "THE SLOW PRINT", ha="center", va="center", fontsize=15, fontweight="bold", color=INKD, family="DejaVu Sans")
for i, (n, lab) in enumerate([("1", "which\nkept most?"), ("2", "beat the\nfast book?"), ("3", "at what\ncost?")]):
    cx, cy = 1.9 + i * 3.1, 6.2
    ax.add_patch(Rectangle((cx - 1.15, cy + 2.55), 2.3, 0.3, fc="#3b3a38", ec=INKD, lw=1.2))
    ax.add_patch(Rectangle((cx - 1.15, cy - 2.85), 2.3, 0.3, fc="#3b3a38", ec=INKD, lw=1.2))
    ax.add_patch(Polygon([[cx - 1.0, cy + 2.55], [cx + 1.0, cy + 2.55], [cx + 0.12, cy], [cx + 1.0, cy - 2.55], [cx - 1.0, cy - 2.55], [cx - 0.12, cy]],
                         closed=True, fc="white", ec=INKD, lw=1.5))
    ax.add_patch(Polygon([[cx - 0.75, cy - 2.55], [cx + 0.75, cy - 2.55], [cx, cy - 1.3]], closed=True, fc=GOLD, ec="none", alpha=0.85))
    ax.text(cx, cy + 1.35, n, ha="center", va="center", fontsize=11, fontweight="bold", color=INKD)
    ax.text(cx, cy + 0.65, lab, ha="center", va="center", fontsize=7.6, fontweight="bold", color=ACC, linespacing=1.05)
ax.text(5.0, 1.6, "Three questions. The answers are in the article", ha="center", va="center", fontsize=8, color=INK2D)
fig.savefig(os.path.join(FIG, "teaser_hourglasses_part2.png"), facecolor=BGC, bbox_inches="tight", pad_inches=0.05); plt.close(fig)

# ---------------------------------------------------------------- 4) article, one-pager, PDFs
md = text
if "![Figure 1]" not in md:   # figures go in after the tables they illustrate
    md = md.replace("## 6. Why didn't slowing do more?", "![Figure 1](../figures/p2_fig1_cost_lines.png)\n\n## 6. Why didn't slowing do more?", 1)
    md = md.replace("Before the run I wrote that a pass would need", "![Figure 3](../figures/p2_fig3_ic_decay.png)\n\nBefore the run I wrote that a pass would need", 1)
    md = md.replace("**Momentum, the benchmark, still loses after costs.**", "![Figure 2](../figures/p2_fig2_growth.png)\n\n**Momentum, the benchmark, still loses after costs.**", 1)
md = md.replace("<!-- HENRIK: hero/poster card here, as in Part 1. Suggested rating line: 0 OF 3 PASSED · SLOWING IS INSURANCE, NOT ALPHA -->",
                "![Now Showing](../figures/hero_minority_report_part2.png)")
write_article(ROOT, STEM, md, "Minority Report, Part 2: The Slow Print")

post = f"""MINORITY REPORT, PART 2: can a machine's signal be traded slowly enough to keep it?

Last week the machines found a strong signal in US small caps before costs ({pc(b['gross_ann'])} a year), and trading at {to(b['turnover_m'])} of capital a month ate most of it.

The textbook answer is "trade slower" (Garleanu & Pedersen, 2013). I signed three ways to do it before computing any of them, and priced every trade with a cost model fitted on real institutional fills.

Three questions:
1. Trade halfway, wait for a clear exit, or smooth the signal: which kept the most after costs?
2. Does slowing down beat the plain fast book?
3. At what cost per trade does slowing start to pay?

Your answer to question 2 in the comments, then check it here, with tables, code and the pre-registration: {REPO} · Not investment advice.

#machinelearning #AI #investing #quant
"""
os.makedirs(os.path.join(ROOT, "linkedin"), exist_ok=True)
write_teaser(ROOT, post, "hero_minority_report_part2_teaser.png", "Minority Report, Part 2", "1 December 2026")
click_layout(ROOT, "teaser_hourglasses_part2.png", alt="Drawing: the three questions inside three hourglasses")
try:
    make_pdfs(ROOT, STEM)
except Exception as e:  # no browser here: print the PDFs on Windows
    print("PDFs not built here:", type(e).__name__)
print("words in post:", len(post.split()))
