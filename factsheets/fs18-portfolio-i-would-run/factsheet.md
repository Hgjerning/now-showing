# FACTSHEET FS18 · The portfolio I would actually run

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

> **In one paragraph.** **Not passed, narrowly.** Pooled over the five markets the overlay adds **+1.9% a year (t 1.85)**, positive in both halves (+3.0% in 2014–19, +0.9% in 2020–26) but short of the pre-registered t > 2. Market by market the picture splits cleanly. In the **US, EU, UK and World** the overlay has a Sharpe ratio near 0.5–0.6, is uncorrelated with the market and lifts the portfolio's Sharpe ratio by 0.15–0.21 at $50m per book. In **Denmark and SCANDI** it adds nothing, as FS13 and FS16 predicted. At **$250m per book** the gain shrinks sharply outside the US and turns negative in the UK, Denmark and SCANDI (pooled +0.2%, t 0.2). The honest verdict: a small, cheap-to-run overlay in large, liquid markets is worth having; it is not a strategy that scales, and it is not a reason to trade the Nordics.

![Market vs market + overlay](../figures/fs18_portfolio.png)

## 1. Market by market

| Market | Books | Overlay return (t) | Overlay Sharpe | Correlation with market | Market Sharpe | Market + overlay Sharpe | Gain at $50m | Gain at $250m |
|---|---|---|---|---|---|---|---|---|
| US | low beta, 12-1 momentum, profit growth, debt issuance | +3.1% (t +2.6) | 0.55 | -0.15 | 0.89 | 1.08 | +0.19 | +0.17 |
| EU | low beta, 12-1 momentum | +3.7% (t +2.5) | 0.60 | -0.11 | 0.58 | 0.79 | +0.22 | +0.09 |
| UK | low beta, 12-1 momentum | +2.8% (t +1.8) | 0.46 | -0.04 | 0.54 | 0.69 | +0.15 | -0.09 |
| Denmark | low beta, 12-1 momentum | +0.5% (t +0.3) | 0.08 | +0.01 | 0.47 | 0.47 | +0.00 | -0.09 |
| SCANDI | low beta, 12-1 momentum | -0.4% (t -0.3) | -0.08 | -0.09 | 0.62 | 0.57 | -0.05 | -0.13 |
| World | low beta, 12-1 momentum | +3.3% (t +2.4) | 0.57 | +0.03 | 0.59 | 0.75 | +0.16 | +0.11 |


*Sharpe ratios of excess returns over the US T-bill rate (French data); market in USD for World, local currency elsewhere; overlay returns are self-financing and net of every cost in the model. Gain = Sharpe of market + overlay minus Sharpe of the market alone.*

## 2. Drawdowns and sizing

| Market | Market max drawdown | Market + overlay max drawdown | Overlay max drawdown | Average overlay scale |
|---|---|---|---|---|
| US | -24% | -21% | -7% | 0.75 |
| EU | -26% | -30% | -13% | 0.48 |
| UK | -27% | -27% | -13% | 0.48 |
| Denmark | -40% | -40% | -19% | 0.49 |
| SCANDI | -27% | -29% | -22% | 0.64 |
| World | -28% | -30% | -7% | 0.50 |


The overlay reduces the worst drawdown only in the US (by about 3 points); elsewhere it leaves it unchanged or slightly deeper. Its value is return per unit of risk, not protection. The average scale well below 1 means the raw book mix ran above 5% volatility; at 5% target volatility the overlay is small next to a market leg with 15–20% volatility.

## 3. The books inside the overlay ($50m per book)

| Market | Book | Net return a year | Sharpe | Monthly turnover | Weight, last month |
|---|---|---|---|---|---|
| US | low beta | +2.8% | 0.11 | 15% | 0.11 |
| US | 12-1 momentum | +3.4% | 0.24 | 29% | 0.22 |
| US | profit growth | +4.9% | 0.44 | 28% | 0.31 |
| US | debt issuance | +1.0% | 0.12 | 14% | 0.36 |
| EU | low beta | +5.8% | 0.30 | 18% | 0.38 |
| EU | 12-1 momentum | +4.3% | 0.30 | 28% | 0.62 |
| UK | low beta | +8.9% | 0.45 | 20% | 0.40 |
| UK | 12-1 momentum | +2.4% | 0.16 | 28% | 0.60 |
| Denmark | low beta | +1.7% | 0.11 | 11% | 0.47 |
| Denmark | 12-1 momentum | -0.4% | -0.03 | 28% | 0.53 |
| SCANDI | low beta | -0.4% | -0.03 | 11% | 0.52 |
| SCANDI | 12-1 momentum | -1.1% | -0.10 | 25% | 0.48 |
| World | low beta | +4.8% | 0.23 | 18% | 0.33 |
| World | 12-1 momentum | +5.2% | 0.41 | 27% | 0.67 |


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
- FS18 adds 14 trials to the ledger (now 638).

## 6. References

- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics* 111(1), 1–25.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance* 48(1), 65–91.
- Moreira, A. & Muir, T. (2017). Volatility-managed portfolios. *Journal of Finance* 72(4), 1611–1644.
- Frazzini, A., Israel, R. & Moskowitz, T. J. (2018). Trading costs. SSRN working paper 3229719.
- DeMiguel, V., Garlappi, L. & Uppal, R. (2009). Optimal versus naive diversification. *Review of Financial Studies* 22(5), 1915–1953.

## 7. Reproduce

`planning/PREREG_FS18.md` → `code/fs18.py` (→ `results/fs18.json`) → `code/build_fs18.py`. Reuses `impact.py` (FS16) and `fundamentals.py` (FS13b).
