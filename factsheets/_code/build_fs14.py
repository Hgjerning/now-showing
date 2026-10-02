# -*- coding: utf-8 -*-
"""FS14: the multifactor model, step by step, as pre-registered (planning/PREREG_FS14.md)."""
import json
import os

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF
import perf
from battery import DIRECTION
from ledger import dsr
from nbh_figs import DIV

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results"); FIG = os.environ.get("FS_FIGURES") or os.path.join(HERE, "..", "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
SURF, INK, INK2, GRID, BLUE, ORANGE, GREY, GREEN = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0", "#2a78d6", "#eb6834", "#8a8984", "#2c7a4b"
p = lambda x, d=1: f"{x * 100:+.{d}f}%"
FL = {"c_debt_issuance": "Debt issuance (US)", "c_profit_growth": "Profit growth (US)", "c_value": "Value (US)", "c_profitability": "Profitability (US)", "c_investment": "Investment (US)", "c_accruals": "Accruals (US)"}
LAB = lambda s: FL.get(s, DIRECTION[s][2] if s in DIRECTION else s)


def figs(r, D):
    ser, sel = D["ser"], D["sel"]
    # selection frequency heatmap
    sigs = sorted({s for R in U for s in r[R]["_sel"]["kept_freq"]}, key=lambda s: -np.mean([r[R]["_sel"]["kept_freq"].get(s, 0) for R in U]))
    M = np.array([[r[R]["_sel"]["kept_freq"].get(s, 0) * 100 for R in U] for s in sigs])
    fig, ax = plt.subplots(figsize=(8.5, 0.34 * len(sigs) + 1.6)); fig.patch.set_facecolor(SURF)
    ax.imshow(M, cmap="Blues", vmin=0, vmax=60, aspect="auto"); ax.grid(False)
    ax.set_xticks(range(6)); ax.set_xticklabels([UN[R] for R in U]); ax.set_yticks(range(len(sigs))); ax.set_yticklabels([LAB(s) for s in sigs], fontsize=8.5)
    for i in range(M.shape[0]):
        for j in range(6):
            if M[i, j] > 0:
                ax.text(j, i, f"{M[i, j]:.0f}", ha="center", va="center", fontsize=7.5, color=INK if M[i, j] < 40 else "white")
    ax.set_title("Share of months each book was held after filter and pruning, %", loc="left", fontsize=11)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs14_selection.png"), dpi=140, facecolor=SURF); plt.close(fig)
    # cumulative OOS per market
    fig, axs = plt.subplots(2, 3, figsize=(13, 7), sharex=True); fig.patch.set_facecolor(SURF)
    for ax, R in zip(axs.flat, U):
        P = ser[R]
        for c, col, lw in (("RP", BLUE, 2.2), ("W36-L", GREEN, 1.4), ("ALL-EQ", GREY, 1.6), ("SHORT", ORANGE, 1.4)):
            ax.plot((1 + P[c].fillna(0)).cumprod(), color=col, lw=lw, label={"RP": "RP (primary)", "W36-L": "W36-L", "ALL-EQ": "All books, equal", "SHORT": "Fixed shortlist*"}[c])
        ax.axhline(1, color=INK2, lw=0.7); ax.set_title(UN[R], loc="left", fontsize=11); ax.set_facecolor(SURF); ax.grid(color=GRID)
        for sp_ in ax.spines.values(): sp_.set_visible(False)
    axs[0, 0].legend(frameon=False, fontsize=8)
    fig.suptitle("Out of sample, Feb 2016 – Aug 2026: growth of 1, market-neutral books, net (*shortlist chosen with hindsight)", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs14_oos.png"), dpi=140, facecolor=SURF); plt.close(fig)
    # variants grid
    V = r["variants"]; M = np.array([[r[R][v]["sharpe"] for R in U] + [r["pooled"][v]["sharpe"]] for v in V + ["ALL-EQ", "SHORT"]])
    fig, ax = plt.subplots(figsize=(9, 6)); fig.patch.set_facecolor(SURF)
    ax.imshow(M, cmap=DIV, vmin=-0.8, vmax=0.8, aspect="auto"); ax.grid(False)
    ax.set_xticks(range(7)); ax.set_xticklabels([UN[R] for R in U] + ["5-mkt avg"]); ax.set_yticks(range(len(V) + 2)); ax.set_yticklabels(V + ["ALL-EQ", "SHORT*"], fontsize=9)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=8, color=INK)
    ax.set_title("Out-of-sample Sharpe ratio by weighting rule (net)", loc="left", fontsize=11)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs14_variants.png"), dpi=140, facecolor=SURF); plt.close(fig)


def build():
    r = json.load(open(os.path.join(RES, "fs14.json"))); D = pd.read_pickle(os.path.join(RES, "fs14.pkl")); figs(r, D)
    V = r["variants"]; M5 = [R for R in U if R != "WD"]; pr = r["primary"]; po = r["pooled"]
    LG = json.load(open(os.path.join(RES, "trial_ledger.json")))
    passed = pr["t"] > 2 and pr["s1"] > 0 and pr["s2"] > 0
    best = max(V, key=lambda v: po[v]["sharpe"])
    x_best = pd.DataFrame({R: D["ser"][R][best] for R in M5}).dropna().mean(axis=1)
    sr_m = pd.Series([r[R][v]["t"] for R in U for v in V]) / np.sqrt(127)
    d_in = dsr(x_best, 78, float(sr_m.var())); d_null = dsr(x_best, 78, 1 / len(x_best))
    # exploratory (not pre-registered): market plus the RP overlay at 10% volatility
    ex = []
    for R in U:
        P = D["ser"][R]; m = P["MARKET"]; o = P["RP (10% vol)"]
        c = float(pd.concat([m, o], axis=1).dropna().corr().iloc[0, 1]); both = (m + o).dropna()
        ex.append([UN[R], f"{perf.sharpe(m.dropna()):.2f}", f"{perf.sharpe(o.dropna()):.2f}", f"{c:+.2f}", f"{perf.sharpe(both):.2f}"])
    steps = [[UN[R], r[R]["_sel"]["n_cand"], f"{r[R]['_sel']['pass_med']:.0f}", f"{r[R]['_sel']['kept_med']:.0f}", r[R]["_sel"]["cash_months"], ", ".join(LAB(s) for s in r[R]["_sel"]["last_kept"]) or "cash"] for R in U]
    res_rows = []
    for R in U:
        q = r[R]
        res_rows.append([UN[R], f"{q['RP']['sharpe']:+.2f}", f"{q[best]['sharpe']:+.2f}", f"{q['ALL-EQ']['sharpe']:+.2f}", f"{q['SHORT']['sharpe']:+.2f}", f"{q['MARKET']['sharpe']:+.2f}", f"{p(q['RP (10% vol)']['ann'])}", f"{q['RP (10% vol)']['maxdd'] * 100:.0f}%"])
    res_rows.append(["**5-market average**", f"{po['RP']['sharpe']:+.2f}", f"{po[best]['sharpe']:+.2f}", f"{po['ALL-EQ']['sharpe']:+.2f}", f"{po['SHORT']['sharpe']:+.2f}", "—", "—", "—"])
    var_rows = [[v, f"{po[v]['sharpe']:+.2f}", f"{po[v]['s1']:+.2f} / {po[v]['s2']:+.2f}", f"{p(r['vs_alleq'][v]['ann'])} (t {r['vs_alleq'][v]['t']:+.1f})", f"{p(r['vs_short'][v]['ann'])} (t {r['vs_short'][v]['t']:+.1f})"] for v in V]
    freq_all = pd.Series({s: np.mean([r[R]["_sel"]["kept_freq"].get(s, 0) for R in U]) for s in {s for R in U for s in r[R]["_sel"]["kept_freq"]}}).sort_values(ascending=False)
    top_sel = ", ".join(f"{LAB(s).lower()} ({v * 100:.0f}%)" for s, v in freq_all.head(5).items())
    everything = [
        ["FS01–FS12", "12 famous strategies × 6 markets, full factsheets", "Only betting against beta has a long/short book that passes positively (UK) after borrow and financing; buying 52-week lows, the Turtle rules and seasonality reliably lose", "Momentum and low-risk families"],
        ["FS05", "10,000 random portfolios", "Monkeys beat the index where small beat big: a size bet, not skill", "Equal-weight universe as the honest benchmark"],
        ["FS00", "All strategies in one table + gap analysis", "Six markets count as fewer than two independent tests; gaps in data, costs and validation", "Borrow, financing, USD World, ledger (closed)"],
        ["FS13", "19 price signals × 6 markets + 153 JKP factors", "No positive price signal survives the correction; momentum positive almost everywhere; debt issuance and profit growth are the published common ground", "Low beta, momentum, debt issuance, profit growth"],
        ["FS13b", "14 US fundamentals, stock level", "Profit growth works on every test; debt issuance on the long side; value and investment lost since 2013", "Profit growth, debt issuance (US)"],
        ["FS13c", "All signals together (Fama-MacBeth)", "12-1 momentum is the only price signal with a marginal return; its cousins are redundant; low risk lowers risk, not return", "One momentum signal"],
        ["FS14", "Pre-registered dynamic selection and weighting", f"Selection beats owning all books ({p(pr['ann'])} a year, t {pr['t']:.1f}) but {'passes' if passed else 'fails'} the pre-registered bar; it trails the hindsight shortlist", "See §8"],
        ["Ledger", f"{LG['n']} gated tests across FS01–FS14", f"{LG['n_pos']} positive and {LG['n_neg']} negative survive Benjamini–Hochberg; no candidate reaches a deflated Sharpe of 0.95", "Honest headline claims"],
    ]
    md = f"""# FACTSHEET FS14 · The multifactor model

### From a battery of 25 books to one portfolio, step by step, as pre-registered

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS14.md`, written and saved before the first run (27 Sep 2026); no deviations |
| Building blocks | 19 beta-neutral price books per market (FS13), plus 6 US fundamental composites (FS13b); all net of trading costs, borrow fees and financing |
| Walk-forward | every month-end: filter → prune → weight, using only past data; out of sample Feb 2016 – Aug 2026 (127 months) |
| Filter | trailing 36 months: positive mean, probabilistic Sharpe ≥ 0.80, costs < 50% of the gross spread |
| Pruning | rank by trailing Sharpe, drop any book correlated above 0.70 with one already kept |
| Weighting | 11 rules: equal (EQ), risk parity (RP, primary), and mean/variance weights over 12/36/60 months with equal, linear or exponential decay |
| Benchmarks | all books equally weighted (ALL-EQ); the fixed FS13 shortlist (SHORT, chosen with hindsight); the equal-weight market |
| Primary test | RP minus ALL-EQ, 5-market average (World excluded as overlapping), Newey–West t > 2 and positive in both halves |

> **In one paragraph.** The selection process works in the direction it should but not strongly enough to pass its own bar. The pre-registered primary portfolio (risk parity over the books that survive the filter and the pruning) beats owning every book equally by **{p(pr['ann'])} a year** on the five-market average (t {pr['t']:.1f}; {pr['s1'] * 100:+.1f}% in 2016–19 and {pr['s2'] * 100:+.1f}% in 2020–26; better in {pr['pos']} of 5 markets). The bar was t > 2, so **the claim that the selection adds value is not established**. The mean/variance weighting rules do somewhat better than risk parity (best: {best}, Sharpe {po[best]['sharpe']:.2f} against {po['RP']['sharpe']:.2f}), but none beats the fixed shortlist of low beta, momentum and the two US fundamentals (Sharpe {po['SHORT']['sharpe']:.2f}), and that shortlist was picked with hindsight from the same data. The filter is strict: in a typical month {min(r[R]['_sel']['kept_med'] for R in U):.0f}–{max(r[R]['_sel']['kept_med'] for R in U):.0f} books are held and the portfolio sits in cash for {min(r[R]['_sel']['cash_months'] for R in U)}–{max(r[R]['_sel']['cash_months'] for R in U)} of 127 months, depending on the market. None of these market-neutral books comes close to the Sharpe ratio of simply owning the market ({min(r[R]['MARKET']['sharpe'] for R in U):.2f}–{max(r[R]['MARKET']['sharpe'] for R in U):.2f}) over the same years.

## Step 1 · The battery

Nineteen beta-neutral long/short price books in every market (FS13): each leg scaled to beta one, net of 10 bp per side, a size-tiered borrow fee on the short leg and financing of the net long cash. In the US the six fundamental composites of FS13b are added, for 25 candidates. Beta-neutral books are used so that the combination is a market-neutral overlay rather than a disguised market bet.

## Step 2 · Filter and Step 3 · Pruning

{BF.table(["Market", "Candidates", "Pass the filter (median per month)", "Kept after pruning (median)", "Months in cash (of 127)", "Held in the last month"], steps)}

![Selection](../figures/fs14_selection.png)

The books selected most often across markets: {top_sel}. The selection moves: momentum and residual momentum dominate some years, low-risk books others, and in the US the fundamental composites (profit growth above all) are held most. The filter's probabilistic-Sharpe bar of 0.80 over 36 months is demanding for books with Sharpe ratios of 0.3–0.6, which is why the portfolio is often small or in cash, especially in World.

## Step 4 · Weighting

{BF.table(["Rule", "Sharpe, 5-market average", "2016–19 / 2020–26", "Minus ALL-EQ / yr (t)", "Minus SHORT / yr (t)"], var_rows)}

![Variants](../figures/fs14_variants.png)

Weighting by recent mean over variance helps a little over equal or risk-parity weights, and the result hardly depends on the window (12, 36 or 60 months) or on the decay (equal, linear, exponential). That insensitivity is reassuring: no single tuning choice drives the result.

## Step 5 · Out of sample, market by market

{BF.table(["Market", "RP (primary) Sharpe", f"{best} Sharpe", "ALL-EQ Sharpe", "SHORT* Sharpe", "Market Sharpe", "RP at 10% vol: return / yr", "RP at 10% vol: max drawdown"], res_rows)}

*Net, monthly, Feb 2016 – Aug 2026. SHORT* = low beta and 12-1 momentum (plus debt issuance and profit growth in the US), fixed in advance but chosen from FS13 results that cover the whole period, so it has hindsight. 10% vol = scaled with its own trailing 12-month volatility, capped at 3×.*

![OOS](../figures/fs14_oos.png)

## Step 6 · Is it real?

- **Primary test:** RP − ALL-EQ = {p(pr['ann'])} a year, t {pr['t']:.2f}, positive in both halves. **{'Passed' if passed else 'Not passed'}** (bar: t > 2 and both halves positive).
- **Deflated Sharpe ratio** of the best rule ({best}, five-market average): {d_in['dsr']:.2f} using the observed spread of the 78 FS14 trials (they are highly correlated variations of one idea) and {d_null['dsr']:.2f} if the 78 trials were independent noise. Both are below the usual bar of 0.95.
- **Programme ledger:** FS14 adds 78 trials (now {LG['n']}); none of them survives the programme-wide correction.

## Step 7 · Exploratory: the overlay next to the market (not pre-registered)

{BF.table(["Market", "Market Sharpe", "RP overlay (10% vol) Sharpe", "Correlation", "Market + overlay Sharpe"], ex)}

*Not part of the pre-registration; shown because a market-neutral overlay is meant to be held next to a market portfolio, not instead of it.* Added to the market, the overlay raises the Sharpe ratio in {', '.join(e[0] for e in ex if float(e[4]) > float(e[1]))} and lowers it in {', '.join(e[0] for e in ex if float(e[4]) <= float(e[1])) or 'none'}.

## Step 8 · What this means

1. **A disciplined process did not beat a simple one here.** Filtering, pruning and weighting beat owning everything, by a margin that the data cannot yet separate from luck; they did not beat a fixed shortlist of two to four well-understood books.
2. **The shortlist's edge is partly hindsight.** It was chosen after looking at 2013–2026 results; the dynamic process had to learn as it went.
3. **Fewer, better-understood books.** For an implementation: low beta (beta-neutral) and one momentum signal in every market, profit growth and debt issuance in the US, sized as an overlay next to the market.
4. **What would change the verdict:** longer history (ART 1996–2013) to double the out-of-sample period, the fundamental themes outside the US, and a cost model with market impact.

## 9. Everything in one table

{BF.table(["Stage", "What was tested", "What we found", "Carried forward"], everything)}

## 10. Caveats

- Out of sample only since 2016 because the filter needs 36 months; 127 months is short for books with Sharpe ratios below 0.6.
- The candidate books themselves were designed before FS14 but on data that overlap the out-of-sample period; the walk-forward protects the selection, not the design of the signals.
- Weight changes between books cost 10 bp per unit of turnover; the books' own trading costs are inside their returns. Market impact is not modelled.
- EU and SCANDI overlap (Nordic blue chips), and World overlaps the US, UK and EU.

## 11. References

- Bailey, D. H. & López de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk* 15(2), 3–44.
- Bailey, D. H. & López de Prado, M. (2014). The deflated Sharpe ratio. *Journal of Portfolio Management* 40(5), 94–107.
- DeMiguel, V., Garlappi, L. & Uppal, R. (2009). Optimal versus naive diversification: how inefficient is the 1/N portfolio strategy? *Review of Financial Studies* 22(5), 1915–1953.
- Asness, C. S., Moskowitz, T. J. & Pedersen, L. H. (2013). Value and momentum everywhere. *Journal of Finance* 68(3), 929–985.
- Harvey, C. R., Liu, Y. & Zhu, H. (2016). … and the cross-section of expected returns. *Review of Financial Studies* 29(1), 5–68.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Moreira, A. & Muir, T. (2017). Volatility-managed portfolios. *Journal of Finance* 72(4), 1611–1644.

## 12. Reproduce

`planning/PREREG_FS14.md` (rules) → `code/fs14.py` (walk-forward → `results/fs14.json`, series in `results/fs14.pkl`) → `code/build_fs14.py`. The candidate books come from `code/battery.py` and `code/fund_battery.py`.
"""
    BF.write("FS14_Multifactor_Model", md, "FS14 The multifactor model")
    BF.pdf("FS14_Multifactor_Model")


if __name__ == "__main__":
    build(); print("built FS14")
