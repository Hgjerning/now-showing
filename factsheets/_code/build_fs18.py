# -*- coding: utf-8 -*-
"""FS18: the portfolio I would actually run (planning/PREREG_FS18.md)."""
import json
import os

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results"); FIG = os.environ.get("FS_FIGURES") or os.path.join(HERE, "..", "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "Denmark", "SC": "SCANDI", "WD": "World"}
SURF, INK2, GRID, BLUE, GREY = "#fcfcfb", "#52514e", "#e6e5e0", "#2a78d6", "#9a9892"
p = lambda x, d=1: f"{x * 100:+.{d}f}%"
K1, K2 = "5e+07", "2e+08"   # $50m and $250m per book (key rounding of 2.5e8)


def fig(ser):
    fg, axs = plt.subplots(2, 3, figsize=(11, 6.2), sharex=True); fg.patch.set_facecolor(SURF)
    for ax, R in zip(axs.ravel(), U):
        d = ser[(R, 5e7)]; ax.set_facecolor(SURF)
        ax.plot((1 + d.market_ex + d.rf).cumprod(), color=GREY, lw=1.6, label="market")
        ax.plot((1 + d.portfolio_ex + d.rf).cumprod(), color=BLUE, lw=1.8, label="market + overlay")
        ax.set_title(UN[R], loc="left", fontsize=10.5); ax.grid(color=GRID)
        for s in ax.spines.values(): s.set_visible(False)
    axs[0, 0].legend(frameon=False, fontsize=9)
    fg.suptitle("Growth of \\$1, 2014–2026: market alone vs market + 5%-volatility overlay, net of costs at \\$50m per book", x=0.01, ha="left", fontsize=11.5)
    fg.tight_layout(); fg.savefig(os.path.join(FIG, "fs18_portfolio.png"), dpi=140, facecolor=SURF); plt.close(fg)


def build():
    r = json.load(open(os.path.join(RES, "fs18.json"))); ser = pd.read_pickle(os.path.join(RES, "fs18.pkl")); fig(ser)
    LG = json.load(open(os.path.join(RES, "trial_ledger.json")))
    M = r["markets"]; P1, P2 = r[f"pooled_{K1}"], r[f"pooled_{K2}"]
    rows = []
    for R in U:
        a, b = M[R][K1], M[R][K2]
        rows.append([UN[R], ", ".join(M[R]["books"]), f"{p(a['overlay']['ann'])} (t {a['overlay']['t']:+.1f})", f"{a['overlay']['sharpe']:.2f}", f"{a['overlay']['corr_market']:+.2f}",
                     f"{a['market']['sharpe']:.2f}", f"{a['portfolio']['sharpe']:.2f}", f"{a['sharpe_diff']:+.2f}", f"{b['sharpe_diff']:+.2f}"])
    dd = [[UN[R], f"{M[R][K1]['market']['mdd'] * 100:.0f}%", f"{M[R][K1]['portfolio']['mdd'] * 100:.0f}%", f"{M[R][K1]['overlay']['mdd'] * 100:.0f}%", f"{M[R][K1]['overlay']['scale_mean']:.2f}"] for R in U]
    bk = []
    for R in U:
        for n, v in M[R][K1]["books"].items():
            bk.append([UN[R], n, p(v["ann"]), f"{v['sharpe']:.2f}", f"{M[R]['turnover'][n] * 100:.0f}%", f"{M[R][K1]['weights_last'][n]:.2f}"])
    s1, s2 = P1["sub"]["2013-19"], P1["sub"]["2020-26"]
    nfs = next(x['trials'] for x in LG['by'] if x['fs'] == 'FS18')
    md = f"""# FACTSHEET FS18 · The portfolio I would actually run

### Everything that survived the series, net of realistic costs, next to a plain market portfolio

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · February 2014 – 2026*

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS18.md`, saved to the Factsheets folder before any FS18 number was computed; no deviations |
| Portfolio | 100% size-weighted market (long-only) + an overlay scaled to 5% annual volatility |
| Overlay books | low beta and 12-1 momentum (all markets); plus profit growth and debt issuance composites (US only, FS13b); all beta-neutral with the turnover buffer |
| Costs | FS16 model: liquidity-dependent spread + square-root impact (Y = 0.7) at **$50m per book**, plus size-tiered borrow and financing; sensitivity at $250m |
| Weights | inverse 36-month volatility per book (equal weights before 36 months); overlay scaled by its trailing 12-month volatility, cap 3× |
| First month | February 2014: the 12-month volatility estimate needs a year of overlay history |
| Primary test | mean monthly overlay return pooled over US, EU, UK, Denmark and SCANDI: Newey–West t > 2 and positive in 2013–19 and 2020–26 |

> **In one paragraph.** **Not passed, narrowly.** Pooled over the five markets the overlay adds **{p(P1['ann'])} a year (t {P1['t']:.2f})**, positive in both halves ({p(s1['ann'])} in 2014–19, {p(s2['ann'])} in 2020–26) but short of the pre-registered t > 2. Market by market the picture splits cleanly. In the **US, EU, UK and World** the overlay has a Sharpe ratio near 0.5–0.6, is uncorrelated with the market and lifts the portfolio's Sharpe ratio by 0.15–0.21 at $50m per book. In **Denmark and SCANDI** it adds nothing, as FS13 and FS16 predicted. At **$250m per book** the gain shrinks sharply outside the US and turns negative in the UK, Denmark and SCANDI (pooled {p(P2['ann'])}, t {P2['t']:.1f}). The honest verdict: a small, cheap-to-run overlay in large, liquid markets is worth having; it is not a strategy that scales, and it is not a reason to trade the Nordics.

![Market vs market + overlay](../figures/fs18_portfolio.png)

## 1. Market by market

{BF.table(["Market", "Books", "Overlay return (t)", "Overlay Sharpe", "Correlation with market", "Market Sharpe", "Market + overlay Sharpe", "Gain at $50m", "Gain at $250m"], rows)}

*Sharpe ratios of excess returns over the US T-bill rate (French data); market in USD for World, local currency elsewhere; overlay returns are self-financing and net of every cost in the model. Gain = Sharpe of market + overlay minus Sharpe of the market alone.*

## 2. Drawdowns and sizing

{BF.table(["Market", "Market max drawdown", "Market + overlay max drawdown", "Overlay max drawdown", "Average overlay scale"], dd)}

The overlay reduces the worst drawdown only in the US (by about 3 points); elsewhere it leaves it unchanged or slightly deeper. Its value is return per unit of risk, not protection. The average scale well below 1 means the raw book mix ran above 5% volatility; at 5% target volatility the overlay is small next to a market leg with 15–20% volatility.

## 3. The books inside the overlay ($50m per book)

{BF.table(["Market", "Book", "Net return a year", "Sharpe", "Monthly turnover", "Weight, last month"], bk)}

## 4. What the whole series leaves standing

| Question | Answer | Where |
|---|---|---|
| Do the famous trading rules work as sold? | Mostly not after costs, borrow and multiple testing | FS01–FS12, FS00 |
| Which price signals survive across markets? | Low beta (beta-neutral) and 12-1 momentum are the most consistent; none survives the correction on its own | FS13, FS13c |
| Do fundamentals add anything? | Yes: profit growth and issuance, in the US stock by stock and outside the US at factor level | FS13b, FS17 |
| Does a clever multifactor selection rule beat equal weights? | No, in 2013–26 or in 1999–2013 | FS14, FS15 |
| Does the shortlist hold up before 2013? | Yes, out of sample (Sharpe 0.8, 1999–2013) | FS15 |
| How big can it get? | US about $1bn; Europe and the UK tens of millions; the Nordics never | FS16 |
| Does it improve a market portfolio? | A little, in large markets, at small size; not significantly when pooled | FS18 |

## 5. Caveats

- Not out of sample for the US fundamental legs, which were chosen from 2013–26 results (FS13b). FS15 is the out-of-sample evidence for the price legs.
- Cost model parameters (spread law, Y = 0.7) are literature values, not calibrated to our own fills.
- The overlay is scaled on its own trailing volatility; a sharp volatility regime change can leave it over- or under-sized for months.
- Market portfolios are our point-in-time universes, not investable indices; no fees are charged on the market leg.
- FS18 adds {nfs} trials to the ledger (now {LG['n']}).

## 6. References

- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics* 111(1), 1–25.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance* 48(1), 65–91.
- Moreira, A. & Muir, T. (2017). Volatility-managed portfolios. *Journal of Finance* 72(4), 1611–1644.
- Frazzini, A., Israel, R. & Moskowitz, T. J. (2018). Trading costs. SSRN working paper 3229719.
- DeMiguel, V., Garlappi, L. & Uppal, R. (2009). Optimal versus naive diversification. *Review of Financial Studies* 22(5), 1915–1953.

## 7. Reproduce

`planning/PREREG_FS18.md` → `code/fs18.py` (→ `results/fs18.json`) → `code/build_fs18.py`. Reuses `impact.py` (FS16) and `fundamentals.py` (FS13b).
"""
    BF.write("FS18_Portfolio_I_Would_Run", md, "FS18 The portfolio I would actually run")
    BF.pdf("FS18_Portfolio_I_Would_Run")


if __name__ == "__main__":
    build(); print("built FS18")
