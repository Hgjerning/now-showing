# -*- coding: utf-8 -*-
"""FS13c: all signals together (Fama-MacBeth)."""
import json
import os

import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF
from nbh_figs import DIV

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); FIG = os.path.join(HERE, "..", "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
SURF, INK = "#fcfcfb", "#0b0b0b"
p = lambda x, d=1: f"{x * 100:+.{d}f}%"


def fig(r):
    P = r["price"]; L = r["labels"]
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 6)); fig.patch.set_facecolor(SURF)
    for ax, key, title in ((axs[0], "uni", "Each signal alone (univariate slope t)"), (axs[1], "multi", "All together (multivariate slope t)")):
        M = np.array([[(r[u][key][s]["t"] if r[u][key] else np.nan) for u in U] for s in P])
        ax.imshow(np.nan_to_num(M), cmap=DIV, vmin=-4, vmax=4, aspect="auto"); ax.grid(False); ax.set_title(title, loc="left", fontsize=11.5)
        ax.set_xticks(range(6)); ax.set_xticklabels([UN[u] for u in U]); ax.set_yticks(range(len(P))); ax.set_yticklabels([L[s] for s in P], fontsize=9)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                ax.text(j, i, "–" if np.isnan(M[i, j]) else f"{M[i, j]:+.1f}", ha="center", va="center", fontsize=8, color=INK)
    fig.suptitle("Fama-MacBeth slopes, next-month returns, 2013–2026 (Denmark: too few stocks for the joint regression)", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs13c_fmb.png"), dpi=140, facecolor=SURF); plt.close(fig)


def build():
    r = json.load(open(os.path.join(RES, "fmb.json"))); fig(r)
    P, F, L = r["price"], r["fund"], r["labels"]; po = r["pooled"]
    LG = json.load(open(os.path.join(RES, "trial_ledger.json"))); fsp = [x for x in LG["passes"] if x["fs"] == "FS13c"]
    mu = [u for u in U if r[u]["multi"]]
    absorbed = [s for s in ["resmom", "hi52"] if np.mean([r[u]["uni"][s]["t"] for u in mu]) > 0 and np.mean([r[u]["multi"][s]["t"] for u in mu]) < 0.5]
    keep = [s for s in P if po[s]["t"] > 2]
    rows = []
    for s in sorted(P, key=lambda s: -po[s]["t"]):
        rows.append([L[s], f"{np.mean([r[u]['uni'][s]['t'] for u in mu]):+.1f}", f"{np.mean([r[u]['multi'][s]['t'] for u in mu]):+.1f}", f"{p(po[s]['ann'])} (t {po[s]['t']:+.1f})", f"{po[s]['pos']} / {po[s]['n']}", f"{po[s]['neff']:.1f}"])
    us = r["US"]; one = r["us_one_at_a_time"]
    frows = [[L[f], f"{us['uni'][f]['t']:+.1f}", f"{one[f]['fund']['t']:+.1f}", f"{us['multi'][f]['t']:+.1f}", f"{p(us['multi'][f]['ann'])}", f"{one[f]['mom']['t']:+.1f}"] for f in F]
    di, pg = "c_debt_issuance", "c_profit_growth"
    md = f"""# FACTSHEET FS13c · All signals together

### Which signals still matter once the others are in the model?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

| Key facts | |
|---|---|
| Method | Fama-MacBeth: every month, next-month stock returns regressed on all signals at once; slopes averaged over time, Newey–West t (6 lags) |
| Signals | one representative per FS13 cluster (10 price signals) in all markets; plus the six US fundamental composites from FS13b in the US |
| Scaling | each signal is a signed percentile rank from −0.5 to +0.5 (high = the literature's good end), so a slope reads as the top-minus-bottom return the signal adds with the others held fixed |
| Universe | the point-in-time universes of FS01–FS13, eligible stocks only, Feb 2013 – Aug 2026; Denmark (about 19 stocks) is too small for a joint regression and gets univariate slopes only |
| Returns | raw next-month returns in local currency (World in USD), no costs; this measures information, not an implementable book |

> **In one paragraph.** Put all signals into one regression and **12-1 momentum is the only price signal that keeps a clear marginal return**: {p(po['mom']['ann'])} a year top-minus-bottom on average across the five markets with a joint regression (t {po['mom']['t']:.1f}), positive in {po['mom']['pos']} of {po['mom']['n']}. Its close cousins, {' and '.join(L[s].lower() for s in absorbed) or 'none'}, look useful alone but add nothing once momentum is in: they are the same bet. Low beta and low volatility have negative raw slopes: they lower risk but do not raise the return, which is why FS13 needed beta-neutral, leveraged books to make them pay. In the US, **debt issuance** keeps its return next to all price signals and the other fundamentals (t {us['multi'][di]['t']:.1f}); **profit growth** does not (t {us['multi'][pg]['t']:.1f} jointly, {one[pg]['fund']['t']:+.1f} with the price signals only), although it survived the price signals in FS13b's beta-neutral decile books. Programme-wide, {len(fsp)} of the FS13c slopes survive the Benjamini–Hochberg correction: {'; '.join(x['strategy'] + ' (' + x['test'].replace('multivariate slope, ', '') + ', t ' + format(x['t'], '+.1f') + ')' for x in fsp)}.

![Fama-MacBeth](../figures/fs13c_fmb.png)

## 1. Price signals, all markets

{BF.table(["Signal", "Alone: average t", "Together: average t", "Together: marginal return / yr, market average (t)", "Markets positive", "Effective markets"], rows)}

*Averages over the markets with a joint regression ({', '.join(UN[u] for u in mu)}). Market average = the mean of the monthly slopes across those markets. Effective markets = n² / sum of the correlation matrix of the slope series.*

**Reading it.**

1. **Momentum is the price signal to keep.** Its average t rises from {np.mean([r[u]['uni']['mom']['t'] for u in mu]):.1f} alone to {np.mean([r[u]['multi']['mom']['t'] for u in mu]):.1f} together: once the other signals soak up the parts of past returns that do not pay (short-term reversal, the low-risk tilt), what remains of momentum pays more clearly.
2. **Momentum's cousins are redundant.** Residual momentum and the 52-week high each earn a positive slope alone and about zero together. In FS14 the momentum block needs one representative, not three.
3. **Low risk does not raise returns.** Beta and volatility have negative raw slopes in most markets. Their value is lower risk at similar return, which a beta-neutral or leveraged construction turns into return (FS10, FS13); a raw-return regression cannot see that.
4. **Seasonality, reversal, tail direction and size** are unreliable: signs flip between markets.

## 2. US fundamentals

{BF.table(["Composite", "Alone: t", "With the 10 price signals: t", "With price signals and the other fundamentals: t", "Marginal return / yr (joint)", "Momentum t in the same regression"], frows)}

**Debt issuance is the fundamental that adds most**: its slope stays at t {us['multi'][di]['t']:.1f} next to every other signal, stronger than its decile long/short in FS13b (t 1.9), because the regression uses the whole cross-section rather than the two extreme deciles. **Profit growth** is weaker here than in FS13b: most of its linear information overlaps with momentum (firms whose earnings rise also see their prices rise), while its extremes (the top and bottom deciles FS13b trades) keep an edge. The two tests measure different things; FS14 will test profit growth as a decile book, where it worked. Value and investment stay negative; accruals and profitability are positive but weak.

## 3. What goes into the multifactor model (FS14)

- **Momentum block:** 12-1 momentum as the representative (residual momentum and the 52-week high as alternatives, never all three).
- **Low-risk block:** low beta, but only as a beta-neutral, financed book; it is a risk reducer, not a return source in raw terms.
- **US fundamentals:** debt issuance (strongest marginal contribution) and profit growth (decile book).
- **Out:** seasonality, reversal, tail direction, size, and the redundant momentum cousins.

## 4. Caveats

- Raw returns, no costs, no borrow or financing: slopes show information, not what a book would earn (the factsheets' books do that).
- Linear in ranks: a signal that works only in the extremes (profit growth) is understated.
- Collinearity: value, investment and profit growth are strongly correlated in the US (FS13b), so their joint slopes are imprecise.
- Denmark is too small for a joint regression; its univariate slopes are in `results/fmb.json`.
- Multiple testing: the multivariate slopes add {sum(1 for u in mu for _ in r[u]['multi']) + len(po)} trials to the factsheet ledger (`planning/FACTSHEET_TRIAL_LEDGER.md`), now {LG['n']} in all.

## 5. References

- Fama, E. F. & MacBeth, J. D. (1973). Risk, return, and equilibrium: empirical tests. *Journal of Political Economy* 81(3), 607–636.
- Newey, W. K. & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica* 55(3), 703–708.
- Green, J., Hand, J. R. M. & Zhang, X. F. (2017). The characteristics that provide independent information about average U.S. monthly stock returns. *Review of Financial Studies* 30(12), 4389–4436.
- Lewellen, J. (2015). The cross-section of expected stock returns. *Critical Finance Review* 4(1), 1–44.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.

## 6. Reproduce

`code/fmb.py` (regressions → `results/fmb.json`, slope series in `results/fmb.pkl`) → `code/build_fs13c.py`.
"""
    BF.write("FS13c_All_Signals_Together", md, "FS13c All signals together")
    BF.pdf("FS13c_All_Signals_Together")


if __name__ == "__main__":
    build(); print("built FS13c")
