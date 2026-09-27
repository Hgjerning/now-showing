# -*- coding: utf-8 -*-
"""FS00: overview of all twelve factsheets and the gap analysis (data, models, implementation, coverage, process)."""
import json
import os
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF
import specs
from build_xs import LBL, CLUSTER, GATE, GATE_P, n6

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); FIG = os.path.join(HERE, "..", "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = BF.UN; table = BF.table
p = lambda x, d=1: f"{x * 100:+.{d}f}%"; f2 = lambda x: f"{x:.2f}"
SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"


def rows_all():
    """One row per strategy with L/S and long-only Sharpe per universe (for the heatmaps) and summary fields."""
    R = []
    T = json.load(open(os.path.join(RES, "turtle_summary.json"))); L = json.load(open(os.path.join(RES, "lottery_summary.json"))); F = json.load(open(os.path.join(RES, "fix_summary.json")))
    N1 = json.load(open(os.path.join(RES, "nbh_brk.json"))); N2 = json.load(open(os.path.join(RES, "nbh_max.json")))
    t = {u: T[u]["stats"] for u in U}
    R.append(dict(code="FS01", title="Turtle Traders", family="Breakout & trend", ls={u: t[u]["Turtle L/S (S1+S2)"]["sharpe"] for u in U}, ls_ann={u: t[u]["Turtle L/S (S1+S2)"]["ann_mean"] for u in U},
                  ls_t={u: t[u]["Turtle L/S (S1+S2)"]["t_mean"] for u in U}, alpha={u: t[u]["Turtle L/S (S1+S2)"]["alpha"] for u in U},
                  lo={u: t[u]["Turtle long-only (S1+S2)"]["sharpe"] for u in U}, ew={u: t[u]["EW universe (benchmark)"]["sharpe"] for u in U},
                  lo_alpha_t={u: t[u]["Turtle long-only (S1+S2)"]["t_alpha"] for u in U},
                  fix=f"T0 {F['turtle']['avg_holdout']['T0 baseline L/S']['sharpe']:.2f} → T3 {F['turtle']['avg_holdout']['T3 + 4N stop']['sharpe']:.2f} (drop shorts, 4N stop)",
                  redundant=max(abs(N1['per'][u]['span_target']['t']['alpha']) for u in U) < 2, cluster="momentum (time series)"))
    l = {u: L[u]["stats"] for u in U}
    R.append(dict(code="FS02", title="Lottery (MAX)", family="Lottery & attention", ls={u: l[u]["L/S low minus high MAX (net)"]["sharpe"] for u in U}, ls_ann={u: l[u]["L/S low minus high MAX (net)"]["ann_mean"] for u in U},
                  ls_t={u: l[u]["L/S low minus high MAX (net)"]["t_mean"] for u in U}, alpha={u: l[u]["L/S low minus high MAX (net)"]["alpha"] for u in U},
                  lo={u: l[u]["Low-MAX long-only (net)"]["sharpe"] for u in U}, ew={u: l[u]["EW universe (benchmark)"]["sharpe"] for u in U},
                  lo_alpha_t={u: l[u]["Low-MAX long-only (net)"]["t_alpha"] for u in U},
                  fix=f"L0 {F['lottery']['avg_holdout']['L0 baseline']['sharpe']:.2f} → L1 {F['lottery']['avg_holdout']['L1 beta-neutral']['sharpe']:.2f} (beta-neutral legs)",
                  redundant=max(abs(N2['per'][u]['span_target']['t']['alpha']) for u in U) < 2, cluster="low risk"))
    for code in specs.ORDER:
        sp = specs.S[code]; J = json.load(open(os.path.join(RES, f"xs_{code}.json"))); per = J["per"]; st = lambda u, b: per[u]["stats"][b]
        s0, s1 = J["steps"][0], J["steps"][-1]
        clus = Counter(CLUSTER[k] for u in U for k in per[u]["nbh"]["near"][:3]).most_common(1)[0][0]
        R.append(dict(code=code, title=sp["title"], family=sp["family"], ls={u: st(u, "L/S (net)")["sharpe"] for u in U}, ls_ann={u: st(u, "L/S (net)")["ann_mean"] for u in U},
                      ls_t={u: st(u, "L/S (net)")["t_mean"] for u in U}, alpha={u: st(u, "L/S (net)")["alpha"] for u in U},
                      beta={u: st(u, "L/S (net)")["beta"] for u in U}, ew_ann={u: st(u, "EW universe")["ann_mean"] for u in U},
                      lo={u: st(u, "Long-only (net)")["sharpe"] for u in U}, ew={u: st(u, "EW universe")["sharpe"] for u in U}, lo_alpha_t={u: st(u, "Long-only (net)")["t_alpha"] for u in U},
                      fix=f"{J['avg_holdout'][s0]['sharpe']:.2f} → {J['avg_holdout'][s1]['sharpe']:.2f} (full ladder)",
                      redundant=max(abs(per[u]['nbh']['span']['t']['alpha']) for u in U) < 2, cluster=clus))
    return R


def heatmaps(R):
    from nbh_figs import DIV
    codes = [r["code"] + " " + r["title"] for r in R]
    A = np.array([[r["ls"][u] for u in U] for r in R]); B = np.array([[r["lo"][u] - r["ew"][u] for u in U] for r in R])
    fig, axs = plt.subplots(1, 2, figsize=(13, 6.6))
    for ax, M, title in ((axs[0], A, "Long/short Sharpe ratio (net)"), (axs[1], B, "Long-only Sharpe minus equal-weight universe Sharpe")):
        im = ax.imshow(M, cmap=DIV, vmin=-1.2, vmax=1.2, aspect="auto")
        ax.set_xticks(range(6)); ax.set_xticklabels([UN[u] for u in U]); ax.set_yticks(range(len(codes))); ax.set_yticklabels(codes, fontsize=8.5); ax.grid(False)
        for i in range(M.shape[0]):
            for j in range(6):
                ax.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=7.5, color=INK)
        ax.set_title(title, loc="left", fontsize=11)
    fig.suptitle("Eleven strategies, six markets, 2013–2026 (FS05 monkeys are shown separately)", x=0.01, ha="left", fontsize=12.5, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(os.path.join(FIG, "fs00_heatmap.png"), dpi=150); plt.close(fig)


def coverage_fig():
    fam = ["Momentum & trend", "Short-term reversal", "Low risk (vol, beta, MAX)", "Seasonality", "Size", "Value", "Quality / profitability", "Investment / asset growth",
           "Earnings momentum / PEAD", "Analyst revisions", "Dividend / payout", "Liquidity", "Short interest", "News / sentiment", "Option-implied risk"]
    # 2 = stock level in all six, 1 = stock level US only or factor level elsewhere, 0 = not covered
    cov = {"Momentum & trend": [2] * 6, "Short-term reversal": [2] * 6, "Low risk (vol, beta, MAX)": [2] * 6, "Seasonality": [2] * 6, "Size": [2, 1, 1, 1, 1, 1],
           "Value": [1, 0, 1, 1, 0, 1], "Quality / profitability": [1, 0, 1, 1, 0, 1], "Investment / asset growth": [1, 0, 1, 1, 0, 1], "Earnings momentum / PEAD": [1, 0, 1, 1, 0, 1],
           "Analyst revisions": [0] * 6, "Dividend / payout": [1, 0, 1, 1, 0, 1], "Liquidity": [1, 1, 1, 1, 1, 1], "Short interest": [0] * 6, "News / sentiment": [0] * 6, "Option-implied risk": [0] * 6}
    M = np.array([cov[f] for f in fam])
    from matplotlib.colors import ListedColormap
    fig, ax = plt.subplots(figsize=(8.4, 7)); ax.imshow(M, cmap=ListedColormap(["#f1d3cf", "#f6e7b9", "#cfe3f7"]), vmin=0, vmax=2, aspect="auto")
    lab = {0: "not covered", 1: "partial", 2: "covered"}
    for i in range(M.shape[0]):
        for j in range(6):
            ax.text(j, i, lab[M[i, j]], ha="center", va="center", fontsize=7.5, color=INK)
    ax.set_xticks(range(6)); ax.set_xticklabels([UN[u] for u in U]); ax.set_yticks(range(len(fam))); ax.set_yticklabels(fam, fontsize=8.5); ax.grid(False)
    ax.set_title("Factor coverage today: stock-level in the six universes", loc="left", fontsize=11)
    fig.text(0.01, 0.01, "partial = stock level in the US only (Sharadar fundamentals, not yet built) or factor-level returns elsewhere (JKP: UK, DK, World; none for EU, SCANDI);\nliquidity = traded-value proxy only", fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(FIG, "fs00_coverage.png"), dpi=150); plt.close(fig)


GAPS = [
 # (category, gap, where it bites, impact, effort, remedy, source we already have)
 ("Data", "Residual survivorship outside the US: 9–25% of index member-quarters have no price (mostly delisted names)", "all non-US results; short legs penalised, long legs flattered", "High", "Medium", "Buy delisted-inclusive history for Europe, or lengthen with the ART archive (1996–2013)", "ART PIT database (Project1, to 2013); none for 2013–26"),
 ("Data", "No company fundamentals outside the US", "value, quality, investment, payout and earnings families missing in 5 of 6 universes", "High", "High", "JKP factor-level returns for UK, DK, World now; a licensed global fundamentals feed later", "JKP 153 factors per country (Project2 cache); Sharadar US fundamentals (staged, unused)"),
 ("Data", "No shares outstanding outside the US", "FS07 size and the FS05 index benchmark use traded value as a proxy", "Medium", "Medium", "Shares-outstanding history or free-float index weights", "none"),
 ("Data", "Short history (from 2012)", "FS06 seasonality averages 1–13 years (paper: 20); FS11 starts 2014; holdout only 6.7 years", "Medium", "Medium", "Extend back with ART (1996–2013) for EU, UK, DK, US", "ART PIT database"),
 ("Data", "Oslo missing from SCANDI; DK has ~19 names", "SCANDI and DK sorts use 3–5 groups of 6–12 stocks; noisy", "Medium", "Low", "Add OBX history; report DK only as a robustness market", "none"),
 ("Data", "US prices without high/low or volume in our Sharadar extract", "FS01 true-range N; US size-independent liquidity signals", "Low", "Low", "Re-pull Sharadar SEP with OHLCV", "Sharadar subscription"),
 ("Data", "No FX conversion; World sums local-currency returns", "World universe; factor attribution (JKP in USD vs local books)", "Medium", "Low", "Convert with daily FX; run hedged and unhedged", "Project2 pit_currency cache"),
 ("Data", "Event and positioning data not used: earnings dates, analyst revisions, short interest, options, news", "360° gaps in FS02 (news vs no-news jumps, implied skew, borrow)", "Medium", "Medium–High", "Check coverage of the Project2 caches, start with the US", "Project2 pit_short_positions, pit_options, pit_headlines, pit_13f; ART IBES (to 2013)"),
 ("Model", "Sort-based tests only; no multivariate (Fama-MacBeth) regressions", "overlapping signals (momentum family, low-risk family) are judged one at a time", "High", "Medium", "Monthly cross-sectional regressions on all library signals, per universe", "code/signals*.py library"),
 ("Model", "Raw 252-day betas, no shrinkage", "FS10 BAB, beta-neutral fixes, attribution", "Medium", "Low", "Vasicek or Frazzini-Pedersen shrinkage", "—"),
 ("Model", "Residual momentum on a market-only model, 24 months", "FS11", "Low", "Low", "Fama-French 3-factor residuals (US), 36 months when history allows", "French factors (Project2 cache)"),
 ("Model", "No factor model for Europe or SCANDI inside JKP; French Europe used, in USD", "attribution alphas for EU and SCANDI", "Medium", "Low", "Build local-currency factor returns from the library itself", "library L/S returns"),
 ("Model", "Equal weighting and one-month holding everywhere", "turnover-heavy strategies (FS08, FS06); comparability with papers that value-weight or hold 6–12 months", "Medium", "Low", "Add value-weighted (US) and overlapping 3/6/12-month holdings", "—"),
 ("Model", "Programme-level multiple testing not yet consolidated", "12 factsheets × 6 universes × books × fix steps", "High", "Low", "One trial ledger for the factsheets; deflated Sharpe on the final battery selection", "Project3 trial ledger format"),
 ("Implementation", "Flat 10 bp per side; no size- or liquidity-dependent costs, no market impact", "all net numbers; small names in DK/SCANDI understated", "High", "Medium", "Spread and impact model by traded value (e.g. square-root impact)", "Project1 art_cost_model, Saxo measured fees (Project2)"),
 ("Implementation", "Short side: no borrow fees or availability in the sorts (50 bp flat in FS01 only)", "every long/short book", "High", "Medium", "Borrow-fee proxy by size and short interest; report long-only as the primary book", "Project2 pit_short_positions"),
 ("Implementation", "Leverage without financing: BAB (rf = 0, no spread), vol targeting up to 3×", "FS10 passes the gate in UK and World partly for this reason", "High", "Low", "Subtract rf and a financing spread; cap leverage", "French RF (Project2 cache)"),
 ("Implementation", "No taxes, dividend withholding or currency hedging costs", "Danish and cross-border investors", "Medium", "Medium", "Investor-specific net-of-tax layer", "Project1 art_measured_taxes"),
 ("Implementation", "Close-to-close execution, monthly rebalance at month-end", "all strategies; month-end crowding", "Low", "Low", "Next-day VWAP proxy; staggered rebalance days", "—"),
 ("Coverage", "Missing factor families: value, quality, investment, earnings momentum, analyst revisions, payout, liquidity", "the multifactor battery would be price-only", "High", "Medium (US) / High (non-US)", "US stock-level from Sharadar now; JKP factor-level for UK, DK, World", "Sharadar US fundamentals; JKP"),
("Validation", "The six universes overlap and co-move: World contains US, UK and EU; EU contains the Danish, Swedish and Finnish blue chips", "every 'positive in k of six' count; six markets are worth fewer than two independent tests", "High", "Low", "Report the effective number of markets; judge on pooled evidence; treat World as a summary, not a seventh market; run EU ex-Nordics", "the L/S series already on disk"),
 ("Validation", "No replication check against published factor returns", "credibility of the engine; a coding error would pass unnoticed", "High", "Low", "Correlate our US momentum, size, low-vol and BAB books with French UMD/SMB and AQR BAB/JKP series; expect > 0.7", "French and JKP factors (Project2 cache)"),
 ("Validation", "No sector or industry neutrality", "low volatility and BAB may be utilities/staples bets; momentum partly industry momentum", "Medium", "Medium", "Sector-neutral sorts (US from Sharadar sectors; elsewhere ICB/GICS from index files)", "Sharadar TICKERS sector field (US)"),
 ("Validation", "No stress tests of named episodes (2015–16, COVID crash and rebound, 2022 rate shock) and no crash-risk analysis for momentum", "FS03, FS09, FS11 (momentum crashes); FS04, FS10 (rate sensitivity)", "Medium", "Low", "Episode table and Daniel–Moskowitz bear-market/rebound regression", "—"),
 ("Validation", "No capacity estimate", "which books survive at realistic AUM, above all DK and SCANDI", "Medium", "Medium", "Capacity at a participation cap (e.g. 5% of daily traded value) per book", "traded-value panels (PIT)"),
 ("Validation", "No unit tests of the engine (look-ahead, signal lags, cost accounting)", "all factsheets", "Medium", "Low", "Synthetic-data tests: random signals must give ~0 before costs; a shifted signal must not change results", "—"),
 ("Process", "Factsheet trials outside the programme ledger", "credibility of the later battery selection", "Medium", "Low", "Register the battery filter and weighting rules before running them", "PREREGISTRATION template (Articles)"),
 ("Process", "Repo assembly script does not know the factsheets", "publishing", "Low", "Low", "Add factsheets to assemble_repo.py", "—"),
]


CLOSED = {
    "No FX conversion": "World converted to USD, unhedged, with Fed H.10 daily rates (EUR, GBP, DKK, SEK) and Yahoo PLN from 2015; the 21 Polish names stay in PLN before 2015 (`data.to_usd`).",
    "Programme-level multiple testing": "One ledger of every gated test in FS01–FS13 with programme-wide Bonferroni, Benjamini–Hochberg and deflated Sharpe (`code/ledger.py`, `planning/FACTSHEET_TRIAL_LEDGER.md`).",
    "Short side: no borrow fees": "Every short leg pays a size-tiered borrow fee: 0.25% a year for the largest half of the universe, 0.75% for the next 30%, 2% for the smallest 20% (`code/borrow.py`); FS01 keeps its flat 0.5%.",
    "Leverage without financing": "Net long cash in beta-neutral and BAB books is charged at the USD risk-free rate + 0.5% (`borrow.financing`). Volatility targeting scales a dollar-neutral book and is not charged for cash; its margin cost is still missing.",
    "No replication check": "FS13: our US signals correlate 0.8 or more with the matching JKP factor for 8 of 12.",
    "Factsheet trials outside the programme ledger": "All factsheet trials are now in the factsheet trial ledger; FS14 will be pre-registered there.",
}


def is_closed(g):
    return next((v for k, v in CLOSED.items() if g[1].startswith(k)), None)


def build():
    R = rows_all(); heatmaps(R); coverage_fig()
    closed = [(g, is_closed(g)) for g in GAPS if is_closed(g)]
    GAPS_OPEN = [g for g in GAPS if not is_closed(g)]
    M = json.load(open(os.path.join(RES, "monkey_summary.json")))
    summ = []
    for r in R:
        ls = r["ls_ann"]; pos = sum(v > 0 for v in ls.values()); gate = [UN[u] + ("+" if r["ls_t"][u] > 0 else "−") for u in U if abs(r["ls_t"][u]) > GATE]
        lob = sum(r["lo"][u] > r["ew"][u] for u in U); lop = [UN[u] for u in U if r["lo_alpha_t"][u] > GATE]
        summ.append([f"{r['code']} {r['title']}", r["family"], f"{p(min(ls.values()))} to {p(max(ls.values()))}", f"{pos} / 6", ", ".join(gate) or "—",
                     f"{p(min(r['alpha'].values()))} to {p(max(r['alpha'].values()))}", f"{lob} / 6", ", ".join(lop) or "—", r["fix"], "yes" if r["redundant"] else "no", r["cluster"]])
    monkey_row = ["FS05 Monkey portfolios", "Portfolio folklore", f"beat the index: {min(M[u]['share_beat_cagr'] for u in U) * 100:.0f}–{max(M[u]['share_beat_cagr'] for u in U) * 100:.0f}% of monkeys", "—", "—", "—", "—", "—", "no fix: a benchmark", "—", "size (equal weight)"]
    summ.insert(4, monkey_row)
    gaps_by = {c: [g for g in GAPS_OPEN if g[0] == c] for c in ["Data", "Model", "Implementation", "Coverage", "Validation", "Process"]}
    prio = sorted(GAPS_OPEN, key=lambda g: ({"High": 0, "Medium": 1, "Low": 2}[g[3]], {"Low": 0, "Medium": 1, "Medium–High": 2, "Medium (US) / High (non-US)": 2, "High": 3}[g[4]]))[:8]
    npos = sum(1 for r in R if any(r['ls_t'][u] > GATE for u in U)); nneg = sum(1 for r in R if any(r['ls_t'][u] < -GATE for u in U))
    posnames = ", ".join(r['code'] for r in R if any(r['ls_t'][u] > GATE for u in U)); negnames = ", ".join(r['code'] for r in R if any(r['ls_t'][u] < -GATE for u in U))
    BR = [r for r in R if "beta" in r and np.median(list(r["beta"].values())) < -0.4]
    bmin = min(min(r["beta"].values()) for r in BR); bmax = max(max(r["beta"].values()) for r in BR)
    drag = [-(r["beta"][u] * r["ew_ann"][u]) for r in BR for u in U]
    brnames = ", ".join(r['code'] for r in BR)
    import pickle
    NE = []
    for c in ["FS03", "FS04", "FS09", "FS10", "FS11", "FS12"]:
        d = pickle.load(open(os.path.join(RES, f"xs_{c}.pkl"), "rb")); df = pd.DataFrame({u: d[u]["books"]["L/S (net)"] for u in U}).dropna(); C = df.corr().values
        NE.append([f"{c} {specs.S[c]['title']}", f2(C[np.triu_indices(6, 1)].mean()), f2(df.corr().loc["US", "WD"]), f2(df.corr().loc["EU", "SC"]), f"{36 / C.sum():.1f}"])
    ne_lo, ne_hi = min(float(r[-1]) for r in NE), max(float(r[-1]) for r in NE)
    LG = json.load(open(os.path.join(RES, "trial_ledger.json")))
    def cost_rng(c):
        P = json.load(open(os.path.join(RES, f"xs_{c}.json")))["per"]
        d = [P[u]["stats"]["Good leg (gross)"]["ann_mean"] - P[u]["stats"]["Bad leg (gross)"]["ann_mean"] - P[u]["stats"]["L/S (net)"]["ann_mean"] for u in U]
        return f"{min(d) * 100:.1f}–{max(d) * 100:.1f}%"
    md = f"""# FACTSHEET FS00 · Overview and gap analysis

### Twelve famous strategies, six markets, one set of rules: what we know, and what is missing

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **In one paragraph.** Twelve strategies were run with the same code on six point-in-time universes (US, EU, UK, Denmark, Scandinavia, World), 2013–2026, after costs, each with a full factsheet: P&L, trade records, drawdowns, attribution, a pre-declared fix ladder, a classification and a 360° view. Only {npos} of eleven long/short books ({posnames or "none"}) {"earns" if npos == 1 else "earn"} a **positive** return that passes the {GATE} gate in at least one market; {nneg} ({negnames or 'none'}) pass it with a significantly **negative** return; long-only books beat the equal-weight universe's Sharpe most often in the momentum and low-risk families. Many signals are **redundant**: once their nearest library neighbours are in the model, {sum(r['redundant'] for r in R)} of eleven have no alpha left. The price-only battery collapses into a few roots: **momentum** (12-1, 52-week high, residual momentum), **low risk** (volatility, beta, MAX) and, weakly, **reversal** and **size**. The biggest gaps are data (fundamentals and delisted prices outside the US), models (no multivariate test yet) and implementation (flat trading costs and no market impact). Borrow fees, financing of leverage, World in one currency, a replication check and a programme-wide trial ledger were added on 27 September 2026 (§3.0).

## 1. All strategies in one table

{table(["Strategy", "Family", "L/S net return / yr (range over 6)", "L/S positive", f"L/S passes |t| > {GATE}", "L/S CAPM alpha range", "Long-only beats EW Sharpe", "Long-only alpha passes", "Fixes: holdout Sharpe", "Redundant in 360° view", "Library cluster"], summ)}
*Net of costs, local currency, Feb 2013 – Aug 2026 (FS01 daily from Jan 2013). In the gate column + marks a significantly positive return, − a significantly negative one. The gate is Bonferroni over 12 cells per factsheet; fix ladders are judged on the 2020–26 holdout. Redundant = alpha |t| < 2 in every universe after the signal's closest library neighbours and the market.*

![Heatmap](../figures/fs00_heatmap.png)

![Battery map](../figures/battery_map.png)

## 2. What the twelve factsheets say together

1. **Two roots carry almost everything.** The momentum family (FS03, FS09, FS11, and the breakout inside FS01) and the low-risk family (FS02, FS04, FS10) are where the beta-adjusted alphas are. Within each family the signals are close substitutes.
2. **Raw long/short numbers mislead in a bull market.** The long/short books of {brnames} carry market betas of {bmin:.2f} to {bmax:.2f} against the equal-weight universe; in a rising market that short beta alone cost {min(drag) * 100:.0f}–{max(drag) * 100:.0f}% a year (beta × universe return). Beta-neutral legs remove most of this drag, but the neutralised books rarely pass the gate.
3. **Costs matter most for the fast signals.** Trading costs take {cost_rng('FS08')} a year from short-term reversal (FS08) and {cost_rng('FS06')} from seasonality (FS06), against {cost_rng('FS03')} for 12-1 momentum and {cost_rng('FS04')} for low volatility; both fast signals are negative after costs in most markets.
4. **Folklore fails where it contradicts momentum.** Buying at the 52-week low (FS12) and buying breakouts with tight stops on single stocks (FS01) both lose; the monkeys (FS05) only reflect whether small beat big.
5. **Survivorship was worth 2–5 percentage points a year** on the equal-weight universes outside the US; moving to point-in-time membership changed several conclusions (FS02).
6. **Six markets are not six tests.** The long/short books co-move strongly across universes (World contains the US; EU contains the Nordic blue chips), so the six markets are worth only {ne_lo:.1f}–{ne_hi:.1f} independent tests (effective number = 36 / sum of the 6×6 correlation matrix). "Positive in all six" is weaker evidence than it sounds.

{table(["Strategy (L/S net)", "Mean pairwise correlation", "US–World", "EU–SCANDI", "Effective number of markets"], NE)}

7. **Across the whole programme, few winners survive.** The factsheet trial ledger holds {LG['n']} gated tests. Under a programme-wide Benjamini–Hochberg correction {LG['n_pos']} positive results survive ({LG['n_pos_bonf']} also Bonferroni, |t| > {LG['z_bonf']:.2f}) against {LG['n_neg']} reliable losers; the best positive candidates have a deflated Sharpe ratio of {max(d['dsr_null'] for d in LG['dsr']):.2f} at most even on the lenient bound, below the usual 0.95 (`planning/FACTSHEET_TRIAL_LEDGER.md`).

## 3. Gap analysis

![Coverage](../figures/fs00_coverage.png)

### 3.0 Closed since the first edition (27 Sep 2026)

{table(["Category", "Gap", "What was done"], [[g[0], g[1], note] for g, note in closed])}

### 3.1 Priority gaps still open (impact high, effort lowest first)

{table(["Category", "Gap", "Impact", "Effort", "Remedy"], [[g[0], g[1], g[3], g[4], g[5]] for g in prio])}
"""
    for c, gs in gaps_by.items():
        md += f"\n### 3.{list(gaps_by).index(c) + 2} {c}\n\n" + table(["Gap", "Where it bites", "Impact", "Effort", "Remedy", "Source we already have"], [[g[1], g[2], g[3], g[4], g[5], g[6]] for g in gs])
    md += f"""
## 4. Recommended next steps

1. **Close the remaining cheap gaps:** a size- and liquidity-dependent cost and impact model, engine unit tests on synthetic data, named-episode stress tests and sector-neutral variants of the low-risk and momentum books.
2. **Add the missing families in the US at stock level** from the Sharadar fundamentals already on disk (value, quality/profitability, investment, payout, earnings momentum), and at factor level for UK, Denmark and World from JKP.
3. **Run a multivariate test** (monthly Fama-MacBeth regressions of returns on all library signals, per universe) before the battery filter, so substitutes are recognised as such.
4. **Then the multifactor battery** as planned: pre-registered filters on net return, Sharpe and turnover per segment; rolling 3-year correlations; dynamic weights over 12/36/60-month windows with equal, linear and exponential decay and volatility scaling; strict walk-forward; deflated Sharpe on the final pick.
5. **Longer history** from the ART archive (1996–2013) for EU, UK, DK and US, to give every conclusion a genuine pre-2013 out-of-sample check.

## 5. Reproduce

`code/build_overview.py` reads `results/xs_*.json`, `turtle_summary.json`, `lottery_summary.json`, `fix_summary.json`, `monkey_summary.json` and the neighbourhood files.
"""
    BF.write("FS00_Overview_and_Gap_Analysis", md, "FS00 Overview and gap analysis")
    BF.pdf("FS00_Overview_and_Gap_Analysis")
    json.dump(dict(summary=summ, gaps=GAPS), open(os.path.join(RES, "fs00_summary.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    build(); print("built FS00")
