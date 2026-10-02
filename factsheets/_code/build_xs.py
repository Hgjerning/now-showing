# -*- coding: utf-8 -*-
"""Generic 15-section factsheet builder for the sort strategies FS03-FS12 (FS05 monkey has its own builder).
Every number comes from results/xs_<code>.json, the signal library and the specs; verdict sentences are conditional."""
import json
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF
import library
import specs
from nbh_figs import LABEL as NBL

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); RES = os.path.join(ROOT, "results"); FIG = os.path.join(ROOT, "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = BF.UN; UNL = BF.UNL
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8984"
GATE = 2.87
N_FIX_TRIALS = 25            # 8 sort strategies x 3 steps + BAB 1 step
GATE_P = 0.05 / N_FIX_TRIALS
p = lambda x, d=1: "n/a" if x is None or x != x else f"{x * 100:+.{d}f}%"
pu = lambda x, d=1: "n/a" if x is None or x != x else f"{x * 100:.{d}f}%"
f2 = lambda x: "n/a" if x is None or x != x else f"{x:.2f}"
table = BF.table
LBL = dict(NBL); LBL.update({"vol252": "Volatility (252 days)", "resmom": "Residual momentum", "seas": "Same-month seasonality", "size": "Size"})
CLUSTER = {"mom": "momentum", "resmom": "momentum", "hi52": "momentum", "lo52": "momentum", "brk55": "momentum",
           "vol": "low risk", "vol252": "low risk", "ivol": "low risk", "beta": "low risk", "range": "low risk", "max1": "low risk", "max5": "low risk", "min1": "low risk", "min5": "low risk",
           "r1": "short-term reversal", "seas": "seasonality", "size": "size", "asym": "tail direction", "skew": "tail direction"}


def n6(k):
    return "all six" if k == 6 else ("none of the six" if k == 0 else f"{k} of the six")


def rng(v, fmt=p):
    v = [x for x in v if x == x]
    return f"{fmt(min(v))} to {fmt(max(v))}" if v else "n/a"


# ---------------------------------------------------------------- figures
def figs(code, J, sp):
    ser = pd.read_pickle(os.path.join(RES, f"xs_{code}.pkl"))
    fig, axs = plt.subplots(2, 3, figsize=(12, 6.6), sharex=True)
    for ax, R in zip(axs.flat, U):
        B = ser[R]["books"]
        for c, lab, col in (("L/S (net)", "Long/short", BLUE), ("Long-only (net)", f"Long-only ({sp['good'].split(' (')[0]})", ORANGE), ("EW universe", "Equal-weight universe", GREY)):
            s = B[c].dropna(); w = (1 + s).cumprod()
            ax.plot(w.index, w.values, color=col, lw=2 if col != GREY else 1.6, label=lab)
            ax.annotate(f"{w.iloc[-1]:.1f}x", (w.index[-1], w.iloc[-1]), xytext=(4, 0), textcoords="offset points", fontsize=8, color=INK2, va="center")
        ax.set_yscale("log"); ax.axhline(1, color=INK2, lw=0.8); ax.set_title(UN[R], loc="left", fontsize=11, color=INK, fontweight="bold")
        ax.yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda v, q: f"{v:g}"))
    axs.flat[0].legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle(f"{sp['title']} on six stock universes, 2013–2026", x=0.01, ha="left", fontsize=13, color=INK, fontweight="bold")
    fig.text(0.01, 0.005, "Growth of 1, log scale, local currency, net of costs. Henrik Gjerning · Project 10 factsheets", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 0.96)); fig.savefig(os.path.join(FIG, f"xs_{code}_growth.png"), dpi=150); plt.close(fig)
    # ladder
    steps = J["steps"]; fig, ax = plt.subplots(figsize=(9, 4.2))
    for j, s in enumerate(steps):
        v = [J["per"][R]["ladder"][s]["holdout"]["sharpe"] for R in U]
        ax.scatter([j] * 6, v, color="#b9b8b2", s=30, zorder=2, edgecolor=SURF)
        a = J["avg_holdout"][s]["sharpe"]; ax.scatter([j], [a], color=BLUE, s=90, zorder=3, edgecolor=SURF, linewidth=2)
        ax.annotate(f"{a:.2f}", (j, a), xytext=(10, -3), textcoords="offset points", fontsize=9, color=INK)
    ax.axhline(0, color=INK2, lw=0.8); ax.set_xticks(range(len(steps))); ax.set_xticklabels([s.replace(" + ", "\n+ ", 1) for s in steps], fontsize=8.5)
    ax.scatter([], [], color=BLUE, label="six-universe average book"); ax.scatter([], [], color="#b9b8b2", label="single universe"); ax.legend(frameon=False, fontsize=8.5)
    ax.set_title(f"{sp['title']}: fixes one step at a time, Sharpe of the long/short in the 2020–26 holdout", loc="left", fontsize=10.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, f"xs_{code}_ladder.png"), dpi=150); plt.close(fig)
    # 360 map
    t, m = sp["sig"], sp["mirror"]
    cc = pd.DataFrame({R: J["per"][R]["nbh"]["char_corr"] for R in U}).mean(axis=1); ccm = pd.DataFrame({R: J["per"][R]["nbh"]["char_corr_mirror"] for R in U}).mean(axis=1)
    colors = {"momentum": "#1baf7a", "low risk": "#4a3aa7", "short-term reversal": ORANGE, "seasonality": "#eda100", "size": "#8a5a44", "tail direction": BLUE}
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    for k in library.LIB:
        ax.scatter(cc[k], ccm[k], s=130 if k in (t, m) else 65, color=colors[CLUSTER[k]], edgecolor=SURF, linewidth=1.5, zorder=3)
        ax.annotate(LBL[k].split(" (")[0], (cc[k], ccm[k]), xytext=(5, 4), textcoords="offset points", fontsize=8, color=INK)
    ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
    for lab, col in colors.items():
        ax.scatter([], [], color=col, label=lab)
    ax.legend(frameon=False, fontsize=8, loc="lower left", title="library cluster", title_fontsize=8)
    ax.set_xlabel(f"likeness to {LBL[t].split(' (')[0]} (average rank correlation)"); ax.set_ylabel(f"likeness to {LBL[m].split(' (')[0]}")
    ax.set_title(f"360° map: {sp['title']} among the 19 library signals", loc="left", fontsize=11)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, f"xs_{code}_map.png"), dpi=150); plt.close(fig)
    if J.get("double_sort_avg"):
        D = np.array(J["double_sort_avg"]) * 100
        fig, ax = plt.subplots(figsize=(6.2, 4.4)); ax.imshow(D, cmap="Blues", aspect="auto")
        for i in range(3):
            for j in range(3):
                ax.text(j, i, f"{D[i, j]:.1f}%", ha="center", va="center", fontsize=11, color=INK)
        ax.set_xticks(range(3)); ax.set_xticklabels([f"low {LBL[m].split(' (')[0]}", "middle", f"high {LBL[m].split(' (')[0]}"], fontsize=8.5)
        ax.set_yticks(range(3)); ax.set_yticklabels([f"low {LBL[t].split(' (')[0]}", "middle", f"high {LBL[t].split(' (')[0]}"], fontsize=8.5); ax.grid(False)
        ax.set_title(f"3×3 sort, next-month return a year\n({', '.join(UN[R] for R in J['double_sort_universes'])} averaged)", loc="left", fontsize=10.5)
        fig.tight_layout(); fig.savefig(os.path.join(FIG, f"xs_{code}_dsort.png"), dpi=150); plt.close(fig)


def library_alpha_fig():
    """Shared figure: CAPM alpha of all 19 library signals in all six universes."""
    A = pd.DataFrame({R: {k: library.build(R)["stats"][k]["alpha"] * 100 for k in library.LIB} for R in U}).loc[library.LIB]
    T = pd.DataFrame({R: {k: library.build(R)["stats"][k]["t_alpha"] for k in library.LIB} for R in U}).loc[library.LIB]
    from nbh_figs import DIV
    fig, ax = plt.subplots(figsize=(7.6, 8.4)); im = ax.imshow(A.values, cmap=DIV, vmin=-15, vmax=15, aspect="auto")
    ax.set_xticks(range(6)); ax.set_xticklabels([UN[R] for R in U]); ax.set_yticks(range(len(library.LIB))); ax.set_yticklabels([LBL[k] for k in library.LIB], fontsize=8.5); ax.grid(False)
    for i in range(len(library.LIB)):
        for j in range(6):
            ax.text(j, i, f"{A.iloc[i, j]:+.0f}\n({T.iloc[i, j]:.1f})" + ("*" if abs(T.iloc[i, j]) >= 2 else ""), ha="center", va="center", fontsize=6.8, color=INK)
    ax.set_title("Signal library: CAPM alpha of each top-minus-bottom sort, % a year (t)", loc="left", fontsize=10.5)
    fig.colorbar(im, ax=ax, fraction=0.04); fig.tight_layout(); fig.savefig(os.path.join(FIG, "lib_alpha.png"), dpi=150); plt.close(fig)


# ---------------------------------------------------------------- text
def build(code):
    sp = specs.S[code]; J = json.load(open(os.path.join(RES, f"xs_{code}.json"))); per = J["per"]
    figs(code, J, sp)
    LS, LO, EW, SW = "L/S (net)", "Long-only (net)", "EW universe", "Size-weighted universe"
    st = lambda R, b: per[R]["stats"][b]
    ls_pos = sum(st(R, LS)["ann_mean"] > 0 for R in U); ls_pass = [UN[R] for R in U if st(R, LS)["t_mean"] > GATE]
    ls_neg_pass = [UN[R] for R in U if st(R, LS)["t_mean"] < -GATE]
    capm_pass = [UN[R] for R in U if abs(st(R, LS)["t_alpha"]) > GATE]
    lo_beats = [UN[R] for R in U if st(R, LO)["sharpe"] > st(R, EW)["sharpe"]]
    lo_alpha_pass = [UN[R] for R in U if st(R, LO)["t_alpha"] > GATE]
    steps = J["steps"]; last = steps[-1]
    passed = [s for s in steps[1:] if J["pooled"][s]["holdout"]["p"] < GATE_P and J["pooled"][s]["design"]["p"] < GATE_P]
    near_all = Counter(k for R in U for k in per[R]["nbh"]["near"][:2])
    near2 = [k for k, _ in near_all.most_common(2)]
    span_t = [per[R]["nbh"]["span"]["t"]["alpha"] for R in U]; span_a = [per[R]["nbh"]["span"]["coef"]["alpha"] for R in U]
    redundant = max(abs(x) for x in span_t) < 2
    clus = Counter(CLUSTER[k] for R in U for k in per[R]["nbh"]["near"][:3]).most_common(1)[0][0]
    jkp_top = Counter(per[R]["cls"]["top"][0][0] for R in U).most_common(1)[0][0]
    verdict = (f"**The claim.** {sp['claim']} **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned "
               f"{rng([st(R, LS)['ann_mean'] for R in U])} a year and was positive in {n6(ls_pos)}"
               + (f"; it passes the {GATE} gate in {', '.join(ls_pass)}" if ls_pass else f"; no universe passes the {GATE} gate")
               + (f" (significantly negative in {', '.join(ls_neg_pass)})" if ls_neg_pass else "") + ". "
               f"The long-only book ({sp['good'].split(' (')[0]}) had a higher Sharpe than the equal-weight universe in {n6(len(lo_beats))}"
               + (f" ({', '.join(lo_beats)})" if 0 < len(lo_beats) < 6 else "") + f", with alphas of {rng([st(R, LO)['alpha'] for R in U])}"
               + (f", passing the gate in {', '.join(lo_alpha_pass)}." if lo_alpha_pass else ", none past the gate.")
               + f" **What goes wrong (§10):** " + diag_sentence(J, sp) + " "
               + (f"Of the pre-declared fixes, {', '.join(passed)} passed in both windows." if passed else "None of the pre-declared fixes passes the gate in both windows.")
               + f" **Classification (§11):** {sp['family']}; its returns sit closest to the {clus} cluster of the signal library. "
               f"**360° view (§12):** nearest neighbours {', '.join(LBL[k] for k in near2)}; "
               + ("after those neighbours and the market, nothing is left (alpha |t| < 2 everywhere): the signal is redundant." if redundant else
                  f"after its closest neighbours and the market it keeps an alpha of {rng(span_a)} (largest |t| {max(abs(x) for x in span_t):.1f}), so it carries some information of its own."))
    head = []
    for R in U:
        head.append([UN[R], f"{per[R]['n']} / {per[R]['q']}", p(st(R, LS)["ann_mean"]), f2(st(R, LS)["t_mean"]), f"{p(st(R, LS)['alpha'])} ({st(R, LS)['t_alpha']:.1f})", f2(st(R, LS)["beta"]),
                     p(st(R, LO)["cagr"]), f2(st(R, LO)["sharpe"]), pu(st(R, LO)["maxdd"], 0), p(st(R, EW)["cagr"]), f2(st(R, EW)["sharpe"]), p(st(R, SW)["cagr"])])
    rules = table(["Rule", f"Original ({sp['origin']})", "This factsheet"], sp["rule_rows"])
    md = f"""# FACTSHEET {code} · {sp['title']}

### {sp['sub']}

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>{sp['style']}</div>
<div><b>Origin</b>{sp['origin']}</div>
<div><b>Family</b>{sp['family']}</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only ({sp['good'].split(' (')[0]})</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> {verdict}

## 1. Headline performance

{table(["Universe", "Names / groups", "L/S return / yr", "L/S t", "L/S CAPM alpha (t)", "L/S beta", "Long-only CAGR", "Long-only Sharpe", "Long-only max DD", "EW CAGR", "EW Sharpe", "Size-weighted CAGR"], head)}
*Monthly, local currency (World in USD). L/S = equal-weighted {sp['good']} minus {sp['bad']}{' (rank-weighted, each leg scaled to beta 1)' if sp['construction'] == 'bab' else ''}, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_{code}_growth.png)

## 2. Strategy description

{sp['claim']}

**Why it might work.** {sp['rationale']}

{rules}
## 3. Data load

{BF.universe_table()}
""" + "".join(f"- **Data gap:** {g}\n" for g in sp["gaps"]) + f"""
## 4. Signal creation

{sp['signal_text']} Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = {sp['good']} minus {sp['bad']}; **long-only** = {sp['good']}; benchmarks: equal-weight universe and size-weighted universe.
- {'Frazzini & Pedersen construction: betas ranked, each leg weighted by rank distance from the median and scaled to an ex-ante beta of 1; no risk-free rate is subtracted.' if sp['construction'] == 'bab' else 'Equal weights within each leg, rebalanced monthly.'}
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

"""
    for R in U:
        rows = []
        for k, lab in ((LS, "L/S (net)"), (LO, "Long-only (net)"), ("Good leg (gross)", f"{sp['good'].split(' (')[0].capitalize()} (gross)"), ("Bad leg (gross)", f"{sp['bad'].split(' (')[0].capitalize()} (gross)"), (EW, "EW universe"), (SW, "Size-weighted universe")):
            s = st(R, k)
            rows.append([lab, p(s["ann_mean"]), p(s["cagr"]), pu(s["vol"]), f"{s['sharpe']:.2f} {BF.ci(s['sharpe_ci'])}", f2(s["il_sortino"]), pu(s["maxdd"], 0), pu(s["hit"], 0), f"{s['t_mean']:.2f}",
                         f2(s["beta"]) if k != EW else "1.00", f"{p(s['alpha'])} ({s['t_alpha']:.1f})" if k != EW else "–", pu(s["cvar95"], 1)])
        md += f"**{UNL[R]}**, median {per[R]['n']} names, {per[R]['q']} groups\n\n" + table(["Book", "Mean / yr", "CAGR", "Vol", "Sharpe [95% CI]", "Sortino", "Max DD", "Hit", "t(mean)", "Beta", "Alpha/yr (t)", "CVaR 95% (month)"], rows) + "\n"
    cal = lambda b: table(["Year"] + [UN[R] for R in U], [[str(y)] + [p(per[R]["stats"][b]["calendar"].get(str(y))) for R in U] for y in sorted({int(y) for R in U for y in per[R]["stats"][b]["calendar"]})])
    md += "*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*\n\n**Calendar-year returns, L/S (net)**\n\n" + cal(LS) + "\n**Calendar-year returns, long-only (net)**\n\n" + cal(LO)
    rec_rows = []
    for R in U:
        rec = pd.read_csv(os.path.join(RES, f"xs_{code}_record_{R}.csv"), index_col=0)
        rec_rows.append([UN[R], f"{len(rec)}", f"{rec.n_good.median():.0f} / {rec.n_bad.median():.0f}", pu(rec.to_good.mean(), 0), pu(rec.to_bad.mean(), 0), pu((rec.ls_net > 0).mean(), 0), p(rec.ls_net.min()), rec.ls_net.idxmin()[:7]])
    cur = [[UN[R], ", ".join(per[R]["current_good"][:8]), ", ".join(per[R]["current_bad"][:8])] for R in ["US", "EU", "UK", "DK", "SC"]]
    md += f"""
## 7. Trading record

The rebalance log per universe is in `results/xs_{code}_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

{table(["Universe", "Rebalances", "Names long / short", "Turnover long leg / month", "Turnover short leg / month", "L/S months positive", "Worst L/S month", "When"], rec_rows)}
**Current book** (signal at 31 August 2026; first 8 names per leg)

{table(["Universe", f"Long: {sp['good'].split(' (')[0]}", f"Short: {sp['bad'].split(' (')[0]}"], cur)}
## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

{attr(per, LS)}
**Long-only**

{attr(per, LO)}
## 9. Statistical verdict

- **Gate:** |t| > {GATE} (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in {n6(ls_pos)}; passes in {len(ls_pass)} of 6{(' (' + ', '.join(ls_pass) + ')') if ls_pass else ''}.
- **L/S CAPM alpha:** {rng([st(R, LS)['alpha'] for R in U])}, |t| past the gate in {len(capm_pass)} of 6.
- **Long-only:** Sharpe above the equal-weight universe in {n6(len(lo_beats))}; alpha {rng([st(R, LO)['alpha'] for R in U])}, passing in {len(lo_alpha_pass)} of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): {', '.join(f"{UN[R]} {st(R, LS)['psr0']:.2f}" for R in U)}.
- **Publication decay:** gross L/S {rng([per[R]['diag']['first_half'] for R in U])} a year in 2013–19 against {rng([per[R]['diag']['second_half'] for R in U])} in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. {N_FIX_TRIALS} fix trials across FS03–FS12, gate p < {GATE_P:.4f}.

### 10.1 Diagnosis (design window 2013–2019)

{table(["Universe", "L/S gross / yr", "Beta", "Beta drag / yr", "CAPM alpha (gross)", "Costs / yr", "Long leg vs EW / yr", "EW vs short leg / yr", "Turnover / month", "Worst months"],
       [[UN[R], p(per[R]['diag']['gross']), f2(per[R]['diag']['beta']), p(per[R]['diag']['beta_drag']), p(per[R]['diag']['alpha_gross']), p(-per[R]['diag']['cost']), p(per[R]['diag']['good_vs_ew']), p(per[R]['diag']['ew_vs_bad']), pu(per[R]['diag']['to'], 0), ", ".join(f"{m} {p(v, 0)}" for m, v in per[R]['diag']['worst'])] for R in U])}
{diag_text(J, sp)}

### 10.2 The fix ladder

{'X0 baseline → X3 volatility targeting (BAB is beta-neutral and rank-weighted by construction, so the beta-neutral and buffer steps do not apply).' if sp['construction'] == 'bab' else 'X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).'}

{ladder_table(J)}
*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_{code}_ladder.png)

{ladder_text(J)}

## 11. Classification: where does it fit?

{table(["Dimension", sp['title']], class_rows(J, sp))}
![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **{LBL[sp['mirror']].split(' (')[0]}**.

{nb_table(J, sp)}
![360 map](../figures/xs_{code}_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

{span_table(J)}
{('![Double sort](../figures/xs_' + code + '_dsort.png)' + chr(10) + chr(10) + dsort_text(J, sp)) if J.get('double_sort_avg') else ''}
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): {p(np.mean([per[R]['nbh']['up'] for R in U]), 0)} vs {p(np.mean([per[R]['nbh']['down'] for R in U]), 0)} a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages {', '.join(p(np.mean([per[R]['nbh']['horizon'][h] for R in U]), 1) for h in ['t+1', 't+2', 't+3', 't+6'])} a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
""" + "".join(f"{i + 4}. **Data gap.** {g}\n" for i, g in enumerate(sp["gaps"])) + f"""{len(sp['gaps']) + 4}. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 ({N_FIX_TRIALS} trials).

## 14. Academic references

""" + "".join(f"- {r}\n" for r in sp["refs"] + specs.COMMON_REFS) + f"""
## 15. Reproduce

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py {code}` → `build_xs.py {code}`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
"""
    # 2026-10-02 layout v2 (Factsheet Content Review): verdict/scorecard, Sharpe anatomy, fit, appendix. Same numbers.
    import factsheet_v2 as V2
    V2.panel(code)
    md = V2.reorganise(md, code, per, rng([per[R]["attribution"][LS]["coef"]["alpha"] for R in U]), rng([st(R, LS)["alpha"] for R in U]))
    BF.write(sp["stem"], md, f"{code} {sp['title']}: factsheet")
    return md


def attr(per, key):
    rows = []
    for R in U:
        a = per[R]["attribution"][key]; c, t = a["coef"], a["t"]
        loads = ", ".join(f"{k} {c[k]:+.2f} ({t[k]:+.1f})" for k in c if k != "alpha" and abs(t[k]) >= 2)
        rows.append([UN[R], a["model"], p(c["alpha"]), f2(t["alpha"]), f2(a["r2"]), loads or "none |t| ≥ 2"])
    return table(["Universe", "Factor model", "Alpha / yr", "t(alpha)", "R²", "Loadings with |t| ≥ 2 (t)"], rows)


def diag_sentence(J, sp):
    per = J["per"]; d = lambda k: [per[R]["diag"][k] for R in U]
    parts = []
    bd = np.mean(d("beta_drag")); cost = np.mean(d("cost")); gross = np.mean(d("gross"))
    if abs(bd) > 0.02:
        parts.append(f"a market bet (average beta {np.mean(d('beta')):+.2f}, worth {p(bd)} a year in 2013–19)")
    if cost > 0.02:
        parts.append(f"costs of about {pu(cost)} a year")
    if np.mean(d("first_half")) - np.mean(d("second_half")) > 0.03:
        parts.append("a weaker second half (2020–26)")
    if abs(gross) < 0.02 and not parts:
        parts.append("a spread close to zero before costs")
    return ("the main drags are " + ", ".join(parts) + ".") if parts else "no single dominant drag."


def diag_text(J, sp):
    per = J["per"]; d = lambda k: np.mean([per[R]["diag"][k] for R in U])
    return (f"On average across the six universes the gross spread was {p(d('gross'))} a year, of which the market exposure (beta {d('beta'):+.2f}) contributed {p(d('beta_drag'))}; "
            f"the beta-adjusted spread (CAPM alpha) was {p(d('alpha_gross'))}. Costs took {pu(d('cost'))} a year at {pu(d('to'), 0)} monthly turnover across both legs. "
            f"The long leg beat the universe by {p(d('good_vs_ew'))} and the short leg lagged it by {p(d('ew_vs_bad'))} a year, so "
            + ("most of the spread comes from the short side." if d('ew_vs_bad') > d('good_vs_ew') else "most of the spread comes from the long side.")
            + f" Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages "
            + ", ".join(p(np.mean([per[R]['nbh']['horizon'][h] for R in U])) for h in ['t+2', 't+3', 't+6']) + " a year.")


def ladder_table(J):
    per = J["per"]; steps = J["steps"]; rows = []
    for j, s in enumerate(steps):
        dsg = np.mean([per[R]["ladder"][s]["design"]["sharpe"] for R in U])
        if j == 0:
            a, b, c = "–", "–", "–"
        else:
            pp = J["pooled"][s]; prev = steps[j - 1]
            a = f"{pp['design']['diff']:+.2f} (p {pp['design']['p']:.3f})"
            b = f"{pp['holdout']['diff']:+.2f} (p {pp['holdout']['p']:.3f})" + (" ✔" if pp["holdout"]["p"] < GATE_P else "")
            c = f"{sum(per[R]['ladder'][s]['holdout']['sharpe'] > per[R]['ladder'][prev]['holdout']['sharpe'] for R in U)} of 6"
        h = J["avg_holdout"][s]
        rows.append([s, f"{dsg:.2f}", a, f"{h['sharpe']:.2f}", b, c, p(h["ann"]), p(h["maxdd"], 0), f"{p(h['alpha'])} ({h['t_alpha']:.1f})", pu(np.mean([per[R]['ladder'][s]['cost'] for R in U]))])
    return table(["Step", "Design Sharpe (avg)", "Δ design (p)", "Holdout Sharpe (book)", "Δ holdout (p)", "Universes improved", "Holdout return / yr", "Holdout max DD", "Holdout alpha vs EW (t)", "Costs / yr"], rows)


def ladder_text(J):
    steps = J["steps"]; out = []
    for s in steps[1:]:
        pp = J["pooled"][s]; d, h = pp["design"], pp["holdout"]
        if d["p"] < GATE_P and h["p"] < GATE_P:
            verdict = "passes in both windows"
        elif d["diff"] > 0 and h["diff"] > 0:
            verdict = "helps in both windows but does not pass the gate"
        elif d["diff"] * h["diff"] < 0:
            verdict = "helps in one window and hurts in the other: not reliable"
        else:
            verdict = "hurts in both windows"
        out.append(f"- **{s}:** {d['diff']:+.2f} design, {h['diff']:+.2f} holdout; {verdict}.")
    a0, a1 = J["avg_holdout"][steps[0]], J["avg_holdout"][steps[-1]]
    out.append(f"\n**Where it ends:** holdout Sharpe {a0['sharpe']:.2f} → {a1['sharpe']:.2f}, return {p(a0['ann'])} → {p(a1['ann'])} a year (six-universe book).")
    return "\n".join(out)


def class_rows(J, sp):
    per = J["per"]; ls = lambda R: per[R]["stats"]["L/S (net)"]
    tg = [per[R]["cls"]["tm_gamma"] for R in U]; tt = [per[R]["cls"]["tm_t"] for R in U]
    jt = Counter(per[R]["cls"]["top"][0][0] for R in U).most_common(2)
    near = Counter(k for R in U for k in per[R]["nbh"]["near"][:3]).most_common(3)
    clus = Counter(CLUSTER[k] for R in U for k in per[R]["nbh"]["near"][:3]).most_common(1)[0][0]
    to = np.mean([per[R]["diag"]["to"] for R in U])
    return [["Series family", f"**{sp['family']}**"], ["Academic style", sp["style"]], ["Signal", "Price only (daily total returns)"],
            ["Cross-section vs time series", "**Cross-sectional**: stocks ranked against each other each month"],
            ["Horizon and turnover", f"One month; {pu(to, 0)} of the two legs replaced monthly"],
            ["Market exposure", f"L/S beta {rng([ls(R)['beta'] for R in U], f2)}"],
            ["Payoff shape", f"Treynor–Mazuy γ {rng(tg, f2)} (t {rng(tt, lambda x: f'{x:.1f}')}); worst 10% of market months {rng([per[R]['cls']['worst_mkt'] for R in U])} a month, best 10% {rng([per[R]['cls']['best_mkt'] for R in U])}"],
            ["Nearest factor theme", ", ".join(f"{k} ({v} of 6 universes)" for k, v in jt)],
            ["Nearest library signals (returns)", ", ".join(f"{LBL[k]} ({v} universes)" for k, v in near)],
            ["Economic rationale", sp["rationale"]], ["Publication", sp["publication"]],
            ["Where it fits", f"In the **{clus}** cluster of the library; " + ("fully explained by its neighbours." if max(abs(per[R]['nbh']['span']['t']['alpha']) for R in U) < 2 else "with some information beyond its neighbours.")]]


def nb_table(J, sp):
    per = J["per"]; rows = []
    cc = pd.DataFrame({R: per[R]["nbh"]["char_corr"] for R in U}).mean(axis=1); rc = pd.DataFrame({R: per[R]["nbh"]["ret_corr"] for R in U}).mean(axis=1)
    order = rc.drop(sp["sig"]).abs().sort_values(ascending=False).index.tolist()
    for k in [sp["sig"]] + order:
        stt = [library.build(R)["stats"][k] for R in U]
        rows.append([LBL[k] + (" **(this strategy)**" if k == sp["sig"] else " (mirror)" if k == sp["mirror"] else ""), CLUSTER[k], f"{cc[k]:+.2f}", f"{rc[k]:+.2f}",
                     p(np.mean([x["ann"] for x in stt])), rng([x["alpha"] for x in stt]), f"{sum(x['t_alpha'] >= 2 for x in stt)} / {sum(x['t_alpha'] <= -2 for x in stt)}"])
    return table(["Signal (top minus bottom, raw sign)", "Cluster", "Likeness: stocks", "Likeness: returns", "Raw L/S, avg of 6", "CAPM alpha range", "Universes alpha t ≥ +2 / ≤ −2"], rows)


def span_table(J):
    rows = []
    for R in U:
        s = J["per"][R]["nbh"]["span"]; c, t = s["coef"], s["t"]
        rows.append([UN[R], p(c["alpha"]), f"{t['alpha']:.2f}", f"{s['r2']:.2f}", ", ".join(f"{LBL[k].split(' (')[0]} {c[k]:+.2f} ({t[k]:+.1f})" for k in c if k not in ("alpha", "mkt") and abs(t[k]) >= 2)])
    return table(["Universe", "Alpha after neighbours / yr", "t", "R²", "Neighbours with |t| ≥ 2"], rows)


def dsort_text(J, sp):
    D = np.array(J["double_sort_avg"]) * 100
    t, m = LBL[sp["sig"]].split(" (")[0], LBL[sp["mirror"]].split(" (")[0]
    return (f"Holding {m} fixed (down a column), moving from low to high {t} changes the return by {D[2, 0] - D[0, 0]:+.1f}, {D[2, 1] - D[0, 1]:+.1f} and {D[2, 2] - D[0, 2]:+.1f} points a year; "
            f"holding {t} fixed (along a row), moving from low to high {m} changes it by {D[0, 2] - D[0, 0]:+.1f}, {D[1, 2] - D[1, 0]:+.1f} and {D[2, 2] - D[2, 0]:+.1f}.")


def battery_map():
    """Every strategy's L/S (FS01-FS12, where available) in factor space: correlation with JKP momentum vs low risk."""
    fig, ax = plt.subplots(figsize=(8.4, 6.2))
    pts = {}
    for code in specs.ORDER:
        f = os.path.join(RES, f"xs_{code}.json")
        if not os.path.exists(f):
            continue
        J = json.load(open(f)); c = [J["per"][R]["cls"]["corr"] for R in ["US", "UK", "DK", "WD"]]
        pts[code] = (np.mean([x.get("momentum", np.nan) for x in c]), np.mean([x.get("low_risk", np.nan) for x in c]))
    F = json.load(open(os.path.join(RES, "fix_summary.json")))["classification"]
    pts["FS01"] = (np.mean([F["Turtle L/S"][R]["corr"]["momentum"] for R in ["US", "UK", "DK", "WD"]]), np.mean([F["Turtle L/S"][R]["corr"]["low_risk"] for R in ["US", "UK", "DK", "WD"]]))
    pts["FS02"] = (np.mean([F["MAX L/S"][R]["corr"]["momentum"] for R in ["US", "UK", "DK", "WD"]]), np.mean([F["MAX L/S"][R]["corr"]["low_risk"] for R in ["US", "UK", "DK", "WD"]]))
    names = {c: specs.S[c]["title"] for c in specs.ORDER}; names.update({"FS01": "Turtle L/S", "FS02": "Lottery (low − high MAX)"})
    for c, (x, y) in pts.items():
        ax.scatter(x, y, s=80, color=BLUE if c not in ("FS01", "FS02") else ORANGE, edgecolor=SURF, linewidth=1.5, zorder=3)
        ax.annotate(f"{c} {names[c]}", (x, y), xytext=(5, 4), textcoords="offset points", fontsize=8, color=INK)
    ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
    ax.set_xlabel("correlation with JKP momentum theme"); ax.set_ylabel("correlation with JKP low-risk theme")
    ax.set_title("All factsheets in factor space (long/short books; US, UK, DK, World average)", loc="left", fontsize=10.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "battery_map.png"), dpi=150); plt.close(fig)


if __name__ == "__main__":
    library_alpha_fig(); battery_map()
    for c in (sys.argv[1:] or specs.ORDER):
        build(c); BF.pdf(specs.S[c]["stem"]); print("built", c)
