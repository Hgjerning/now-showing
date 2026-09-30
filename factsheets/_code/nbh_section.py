# -*- coding: utf-8 -*-
"""Section 12 (360° view) for FS02 (lottery vs falling knife) and FS01 (breakout neighbourhood).
All numbers read from results/nbh_<name>.json (neighbourhood.py)."""
import json
import os

import numpy as np
import pandas as pd

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
LABEL = {"max1": "MAX (best day)", "max5": "MAX5 (5 best days)", "min1": "MIN (worst day)", "min5": "MIN5 (5 worst days)", "range": "Range (MAX − MIN)",
         "asym": "Net tail (MAX + MIN)", "skew": "Skewness", "ivol": "Idiosyncratic volatility", "vol": "Volatility (63 days)", "beta": "Beta (252 days)",
         "r1": "Last month's return", "mom": "Momentum 12-1", "hi52": "Price / 52-week high", "lo52": "Price / 52-week low", "brk55": "Price / prior 55-day high"}
p = lambda x, d=1: f"{x * 100:+.{d}f}%"


def table(head, rows):
    s = "| " + " | ".join(str(x).replace("|", "&#124;") for x in head) + " |\n|" + "|".join(["---"] * len(head)) + "|\n"
    for r in rows:
        s += "| " + " | ".join(str(x).replace("|", "&#124;") for x in r) + " |\n"
    return s


def rng(v, f=lambda x: f"{x:.2f}"):
    return f"{f(min(v))} to {f(max(v))}"


def nsig(N, k, sign):
    return sum((N["per"][R]["perf"][k]["t_alpha"] * sign) >= 2 for R in U)


def nb_table(N, roles):
    t = N["target"]; cc = pd.DataFrame(N["char_corr_avg"]); rc = pd.DataFrame(N["ret_corr_avg"]); rows = []
    for k, role in roles:
        pr = [N["per"][R]["perf"][k] for R in U]
        rows.append([LABEL[k], role, f"{cc.loc[k, t]:+.2f}", f"{rc.loc[k, t]:+.2f}", p(np.mean([x['ann'] for x in pr])),
                     rng([x["alpha"] for x in pr], p), f"{nsig(N, k, 1)} / {nsig(N, k, -1)}"])
    return table(["Signal (top minus bottom)", "Role", f"Likeness to {LABEL[t]}: stocks", "Likeness: L/S returns", "Raw L/S, avg of 6", "CAPM alpha range", "Universes with alpha t ≥ +2 / ≤ −2"], rows)


def span_rows(N, key):
    rows = []
    for R in U:
        s = N["per"][R][key]; c, tt = s["coef"], s["t"]
        rows.append([UN[R], p(c["alpha"]), f"{tt['alpha']:.2f}", f"{s['r2']:.2f}", ", ".join(f"{LABEL[k].split(' (')[0]} {c[k]:+.2f} ({tt[k]:+.1f})" for k in c if k not in ("alpha", "mkt") and abs(tt[k]) >= 2)])
    return rows


def fs02():
    N = json.load(open(os.path.join(RES, "nbh_max.json"))); cc = pd.DataFrame(N["char_corr_avg"]); rc = pd.DataFrame(N["ret_corr_avg"])
    D = np.array(N["double_sort_avg"]) * 100
    per = N["per"]
    ud = lambda k, w: np.mean([per[R]["perf"][k][w] for R in U])
    roles = [("max1", "target: the lottery signal"), ("max5", "lookalike (robust MAX)"), ("skew", "lookalike: up-tail shape"), ("asym", "decomposition: direction of the tails"),
             ("range", "decomposition: size of the tails"), ("ivol", "lookalike: stock-specific risk"), ("vol", "lookalike: total risk"), ("beta", "lookalike: market risk"),
             ("min1", "mirror: the fast falling knife"), ("min5", "mirror (robust MIN)"), ("lo52", "cousin: the slow falling knife"), ("hi52", "cousin: anchoring to the high"),
             ("r1", "cousin: one-month reversal"), ("mom", "cousin: momentum"), ("brk55", "cousin: breakout (FS01)")]
    lo_alpha = [per[R]["perf"]["lo52"]["alpha"] for R in U]; min_alpha = [per[R]["perf"]["min1"]["alpha"] for R in U]
    md = f"""## 12. 360° view: lottery, falling knife and everything in between

A factor is only understood next to its neighbours: the signals that pick the same stocks (lookalikes), the signal that should pick the opposite stocks (the mirror), the same idea at another speed (cousins), and the pieces it is made of (decomposition). MAX is the up-tail of last month's daily returns; its natural mirror is **MIN, the worst day**, which is the fast version of a *falling knife*. The slow version is a stock sitting at its 52-week low. This section tests all of them on the same six point-in-time universes, same months, same construction: equal-weighted top quantile minus bottom quantile, gross, Feb 2013 – Aug 2026 (`code/signals.py`, `code/neighbourhood.py`). Signs are raw: the MAX line is *most lottery-like minus calmest*, the MIN line is *mildest worst day minus deepest crash*, the 52-week-low line is *far above the low minus at the low*.

### 12.1 The neighbourhood in one table

{nb_table(N, roles)}
*Likeness to MAX, stocks = average cross-sectional rank correlation of the signal with MAX; returns = correlation of the monthly long/short returns. CAPM alpha vs the equal-weight universe, Newey-West t.*

![360 map](../figures/nbh_max_map.png)

### 12.2 Are lottery and falling knife mirrors?

**In the stocks they pick: no.** The rank correlation of MAX and MIN is only {cc.loc['max1', 'min1']:+.2f}. A stock with a huge best day usually also has a deep worst day, because both come from volatility: MAX correlates {cc.loc['max1', 'range']:+.2f} with the range and {cc.loc['max1', 'ivol']:+.2f} with idiosyncratic volatility; MIN correlates {cc.loc['min1', 'range']:+.2f} with the range. What separates them is direction: MAX is {cc.loc['max1', 'asym']:+.2f} correlated with the net tail and MIN {cc.loc['min1', 'asym']:+.2f}. So each signal is roughly half "how big are the tails" and half "which tail is bigger".

**In the returns they earn: nearly.** The MAX and MIN long/short returns correlate {rc.loc['max1', 'min1']:+.2f}, because the shared volatility half is also a market bet: MAX's long/short correlates {rc.loc['max1', 'vol']:+.2f} with the volatility sort and {rc.loc['max1', 'beta']:+.2f} with the beta sort. In rising markets the lottery side wins and the crashed side wins; in falling markets both lose:

![Up and down markets](../figures/nbh_max_updown.png)

| Top-minus-bottom sort | Months the market rose, % a year | Months it fell, % a year |
|---|---|---|
| MAX (most lottery-like minus calmest) | {ud('max1', 'up') * 100:+.0f}% | {ud('max1', 'down') * 100:+.0f}% |
| MIN (mildest minus deepest crash) | {ud('min1', 'up') * 100:+.0f}% | {ud('min1', 'down') * 100:+.0f}% |
| Range (biggest minus smallest tails) | {ud('range', 'up') * 100:+.0f}% | {ud('range', 'down') * 100:+.0f}% |
| Net tail (up-tail minus down-tail dominated) | {ud('asym', 'up') * 100:+.0f}% | {ud('asym', 'down') * 100:+.0f}% |

The size of the tails swings with the market; the direction of the tails hardly does.

**The double sort settles it.** Sorting stocks independently into three MAX groups and three MIN groups (universes with at least 60 names, averaged):

![Double sort](../figures/nbh_max_dsort.png)

Holding the worst day fixed (down a column), the best day adds little: the spread from calmest to most lottery-like is {D[2, 0] - D[0, 0]:+.1f}, {D[2, 1] - D[0, 1]:+.1f} and {D[2, 2] - D[0, 2]:+.1f} points a year. Holding the best day fixed (along a row), the worst day matters more: deep crashes out-earned mild worst days by {D[0, 0] - D[0, 2]:+.1f}, {D[1, 0] - D[1, 2]:+.1f} and {D[2, 0] - D[2, 2]:+.1f} points, a beta effect again (§12.3). MAX carries no information that MIN and volatility do not already carry.

### 12.3 What is actually priced

![Alpha grid](../figures/nbh_max_alpha.png)

- **The size of the tails is priced, negatively, once beta is removed.** Range has a negative CAPM alpha in all six universes ({rng([per[R]['perf']['range']['alpha'] for R in U], p)}; t ≤ −2 in {nsig(N, 'range', -1)}). So do idiosyncratic volatility ({nsig(N, 'ivol', -1)} of 6 at t ≤ −2), volatility ({nsig(N, 'vol', -1)}) and beta ({nsig(N, 'beta', -1)}). This is the low-risk anomaly (Frazzini & Pedersen 2014; Ang et al. 2006), and it is where MAX's negative alphas ({nsig(N, 'max1', -1)} of 6 at t ≤ −2) come from.
- **The direction of the tails is not priced.** Net tail and skewness have alphas of {rng([per[R]['perf']['asym']['alpha'] for R in U], p)} and {rng([per[R]['perf']['skew']['alpha'] for R in U], p)} (universes with |t| ≥ 2: net tail {nsig(N, 'asym', 1) + nsig(N, 'asym', -1)}, skewness {nsig(N, 'skew', 1) + nsig(N, 'skew', -1)}). The genuinely "lottery" part of MAX, a big up-day that is *not* matched by a big down-day, earns nothing in these large-cap universes.
- **Spanning.** Regressing the MAX long/short on MIN, idiosyncratic volatility, volatility, beta, skewness, last month's return and the market explains {rng([per[R]['span_target']['r2'] for R in U])} of its variance and leaves an alpha of {rng([per[R]['span_target']['coef']['alpha'] for R in U], p)} (|t| ≤ {max(abs(per[R]['span_target']['t']['alpha']) for R in U):.1f}). **MAX is redundant.** The MIN long/short against MAX and the same neighbours leaves {rng([per[R]['span_mirror']['coef']['alpha'] for R in U], p)} (largest t {max(per[R]['span_mirror']['t']['alpha'] for R in U):.1f}).

{table(["Universe", "MAX alpha after neighbours / yr", "t", "R²", "Neighbours with |t| ≥ 2 (loading, t)"], span_rows(N, "span_target"))}
- **Persistence.** The MAX spread is about as large 2, 3, 4 and 6 months after formation as in the first month (US: {', '.join(f"{k} {v * 100:+.0f}%" for k, v in per['US']['horizon'].items())}). A mispricing that gets corrected would fade; a stable characteristic such as volatility does not. That fits MAX measuring a lasting trait of the stock rather than a passing overreaction.

### 12.4 The falling knife at two speeds

| | Fast knife: MIN, a big one-day crash | Slow knife: sitting at the 52-week low |
|---|---|---|
| Stocks it picks | Volatile stocks (rank corr with volatility {cc.loc['min1', 'vol']:+.2f}) | Losers (rank corr with momentum {cc.loc['lo52', 'mom']:+.2f}) |
| Raw return of *avoiding* the knife, avg of 6 | {p(np.mean([per[R]['perf']['min1']['ann'] for R in U]))} a year{' (knives won, via beta)' if np.mean([per[R]['perf']['min1']['ann'] for R in U]) < 0 else ''} | {p(np.mean([per[R]['perf']['lo52']['ann'] for R in U]))} a year |
| CAPM alpha of avoiding it | {rng(min_alpha, p)}, t ≥ 2 in {nsig(N, 'min1', 1)} of 6 | {rng(lo_alpha, p)}, t ≥ 2 in {nsig(N, 'lo52', 1)} of 6 |
| What explains it | Low risk: crashed stocks are high-beta, high-vol | Momentum: losers keep losing (correlation of returns with momentum {rc.loc['lo52', 'mom']:+.2f}) |

Both speeds say the same thing once beta is removed: **the knife keeps falling relative to the market.** Only its beta makes a fast knife look like a bargain in a bull market. This matches A10 *Free Fallin'*, where knives rebounded only in market-wide crashes (0 of 3 tests passed), and it is the reverse of the "blood in the streets" folklore.

### 12.5 Verdict of the 360° view, and what is still missing

**Lottery and falling knife are the two tails of the same volatility.** They are mirrors in their returns ({rc.loc['max1', 'min1']:+.2f}) but not in the stocks they pick ({cc.loc['max1', 'min1']:+.2f}). Neither tail carries a premium of its own once volatility and beta are in the model (largest exception: MIN in {UN[max(U, key=lambda R: per[R]['span_mirror']['t']['alpha'])]}, t {max(per[R]['span_mirror']['t']['alpha'] for R in U):.1f} after its neighbours); what remains priced is the low-risk anomaly (avoid large tails of either sign) and, for the slow knife, momentum. For the multifactor battery this means: keep the root signals (volatility or beta, momentum), not MAX or MIN.

Not covered, and why:

| Missing angle | Why it matters | Why it is not here |
|---|---|---|
| Size and liquidity | The lottery effect lives in small, illiquid stocks | No market caps outside the US; the universes are blue chips by design |
| News versus non-news jumps | An earnings jump is information, a no-news jump is closer to gambling | No announcement dates outside the US in the data set |
| Retail attention and flows (search volume, broker app data) | The behavioural story is about retail demand | No attention data |
| Option-implied skewness | Forward-looking lottery-ness (Conrad, Dittmar & Ghysels 2013) | No option data |
| Nominal share price | Kumar (2009): lottery stocks are cheap per share | Only adjusted prices for most markets |
| Short interest and borrow fees | Limits to arbitrage on the short leg | Not in the data set |

"""
    return md


def fs01():
    N = json.load(open(os.path.join(RES, "nbh_brk.json"))); cc = pd.DataFrame(N["char_corr_avg"]); rc = pd.DataFrame(N["ret_corr_avg"]); per = N["per"]
    D = np.array(N["double_sort_avg"]) * 100
    roles = [("brk55", "target: the cross-sectional breakout"), ("hi52", "lookalike: near the 52-week high"), ("r1", "lookalike: last month's winner"), ("mom", "cousin: slow momentum"),
             ("lo52", "mirror: at the 52-week low (short breakout)"), ("min1", "cousin: no crash lately"), ("max1", "cousin: lottery"), ("vol", "lookalike (inverse): calm stocks"),
             ("beta", "lookalike (inverse): low beta")]
    md = f"""## 12. 360° view: the breakout neighbourhood

The Turtle book trades each stock's own channel over time. Its cross-sectional twin ranks stocks by how close they are to their prior 55-day high (**price / 55-day high**, top = at a breakout). Placing that signal among its neighbours shows what a breakout really selects, and whether the information survives outside the Turtle's execution. Same six point-in-time universes, equal-weighted top minus bottom quantile, gross, Feb 2013 – Aug 2026.

{nb_table(N, roles)}
![360 map](../figures/nbh_brk_map.png)

**What a breakout selects.** Stocks at a 55-day high are last month's winners (rank corr with last month's return {cc.loc['brk55', 'r1']:+.2f}), close to their 52-week high ({cc.loc['brk55', 'hi52']:+.2f}), calm rather than volatile ({cc.loc['brk55', 'vol']:+.2f} with volatility) and without recent crashes ({cc.loc['brk55', 'min1']:+.2f} with MIN). It is *not* the lottery signal ({cc.loc['brk55', 'max1']:+.2f} with MAX).

**Is there information?** Yes, once beta is removed: the breakout sort has a CAPM alpha of {rng([per[R]['perf']['brk55']['alpha'] for R in U], p)} (t ≥ 2 in {nsig(N, 'brk55', 1)} of 6), because breakout stocks are low-beta and the raw spread is dragged down in a bull market. But it is a weaker copy of its neighbours: nearness to the 52-week high earns {rng([per[R]['perf']['hi52']['alpha'] for R in U], p)} (t ≥ 2 in {nsig(N, 'hi52', 1)}) and 12-1 momentum {rng([per[R]['perf']['mom']['alpha'] for R in U], p)} (t ≥ 2 in {nsig(N, 'mom', 1)}).

**Spanning.** Against momentum, the 52-week high, last month's return, volatility, MAX and the market, the breakout sort keeps an alpha of {rng([per[R]['span_target']['coef']['alpha'] for R in U], p)} (|t| ≤ {max(abs(per[R]['span_target']['t']['alpha']) for R in U):.1f}), with R² {rng([per[R]['span_target']['r2'] for R in U])}. **The breakout is redundant given the 52-week high and one-month return.**

{table(["Universe", "Breakout alpha after neighbours / yr", "t", "R²", "Neighbours with |t| ≥ 2 (loading, t)"], span_rows(N, "span_target"))}
![Double sort](../figures/nbh_brk_dsort.png)

**Mirror.** The short-side mirror, a stock at its 52-week low, is the stronger signal: holding the breakout fixed, stocks far above their 52-week low out-earn stocks at the low by {D[0, 2] - D[0, 0]:+.1f}, {D[1, 2] - D[1, 0]:+.1f} and {D[2, 2] - D[2, 0]:+.1f} points a year, while the breakout adds little within each column. That is consistent with §10: the Turtle's short breakouts lost because the stock was high-beta in a rising market, not because the cross-sectional information pointed the wrong way.

**Verdict of the 360° view.** The breakout carries real, beta-adjusted information, but it is a noisy subset of the 52-week-high and momentum effects (George & Hwang 2004; Jegadeesh & Titman 1993). The Turtle rules waste it through time-series execution, stops and shorts (§10). For the factor battery, FS09 (52-week high) and FS03 (momentum) are the signals to carry forward, not the breakout itself.

"""
    return md
