# FACTSHEET FS16 · Costs that grow with size

### How much money can these strategies hold before trading costs eat them?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

| Key facts | |
|---|---|
| Rules | `planning/PREREG_FS16.md`, written in the build environment before the run (10:13) and copied to the Factsheets folder right after it (the run finished 10:16); no changes |
| Cost per trade | half-spread 5 bp × (ADV / $50m)^−0.3, 2–50 bp, plus square-root impact 0.7 × daily volatility × √(trade / ADV); sensitivity 1.0 |
| ADV | 63-day average traded value in USD per stock (US: price × volume where the Project1 cache has it; otherwise market cap × the size-quintile median ratio) |
| Sizes | $1m, $10m, $100m, $1bn, $10bn of capital per book |
| Books | the shortlist (low beta + 12-1 momentum, beta-neutral) and four raw long/short books, six markets, 2013–2026; borrow fees and financing as before |
| Replaces | the flat 10 bp per side used in FS01–FS15 |

> **In one paragraph.** Capacity is the binding constraint for these books, far more than the flat-cost results suggested. The shortlist keeps a positive Sharpe ratio up to about **$1.0bn in the US** and **$133m across World**, but only **$29m in the EU, $27m in the UK and $13m in Denmark**, and nothing in Scandinavia. The UK and EU books look best at small size because their low-beta legs sit in thinly traded stocks, which is also why they fill up first. The fast signals are uninvestable: short-term reversal has a Sharpe ratio of -1.76 to -0.32 already at $10m. Two exploratory fixes help: a turnover buffer (hold a stock until it leaves the top 30%) halves turnover and raises the size at which the Sharpe ratio halves 3–7 times with little loss at small size; a liquidity screen raises capacity in the EU and World but removes most of the UK result.

![Capacity](../figures/fs16_capacity.png)

## 1. The shortlist, as pre-registered

| Market | $1m | $10m | $100m | $1bn | $10bn | Sharpe halves at | Net return reaches zero at |
|---|---|---|---|---|---|---|---|
| US | +0.28 | +0.26 | +0.20 | +0.01 | -0.57 | $208m | $1.0bn |
| EU | +0.63 | +0.37 | -0.42 | -1.93 | -2.89 | $12m | $29m |
| UK | +0.88 | +0.48 | -0.64 | -2.05 | -2.55 | $11m | $27m |
| DK | +0.18 | +0.04 | -0.39 | -1.63 | -3.97 | $5m | $13m |
| SCANDI | -0.02 | -0.16 | -0.57 | -1.84 | -4.74 | — | — |
| World | +0.50 | +0.41 | +0.11 | -0.80 | -2.66 | $34m | $133m |


*Sharpe ratio, net of spread, impact (Y = 0.7), borrow fees and financing, 2013–2026. Capital per book; the combined shortlist puts half in each leg.*

## 2. Every book, every market

| Book | Market | Flat 10 bp | $1m | $100m | $1bn | $100m, Y = 1.0 | Spread cost / yr | All-in cost / yr at $100m | Monthly turnover | Net return reaches zero at |
|---|---|---|---|---|---|---|---|---|---|---|
| low beta (beta-neutral) | US | +0.13 | +0.15 | +0.11 | +0.01 | +0.09 | 0.3% | 1.9% | 0.42 | $1.1bn |
|  | EU | +0.56 | +0.47 | -0.30 | -1.36 | -0.60 | 0.9% | 27.5% | 0.45 | $30m |
|  | UK | +0.98 | +0.84 | -0.39 | -1.49 | -0.79 | 1.4% | 40.1% | 0.50 | $38m |
|  | DK | +0.08 | +0.06 | -0.22 | -0.85 | -0.35 | 0.3% | 5.7% | 0.20 | $7m |
|  | SCANDI | +0.09 | +0.08 | -0.18 | -0.77 | -0.30 | 0.4% | 5.2% | 0.27 | $12m |
|  | World | +0.31 | +0.30 | +0.02 | -0.62 | -0.11 | 0.7% | 9.9% | 0.48 | $107m |
| 12-1 momentum (beta-neutral) | US | +0.29 | +0.33 | +0.23 | -0.00 | +0.19 | 0.5% | 2.3% | 0.57 | $975m |
|  | EU | +0.55 | +0.48 | -0.36 | -1.90 | -0.73 | 1.0% | 16.3% | 0.57 | $27m |
|  | UK | +0.70 | +0.54 | -0.74 | -2.23 | -1.20 | 1.3% | 28.8% | 0.55 | $16m |
|  | DK | +0.26 | +0.22 | -0.37 | -1.68 | -0.64 | 0.7% | 11.7% | 0.43 | $15m |
|  | SCANDI | -0.10 | -0.14 | -0.75 | -2.14 | -1.04 | 0.8% | 10.2% | 0.54 | — |
|  | World | +0.55 | +0.55 | +0.22 | -0.56 | +0.06 | 0.8% | 6.3% | 0.56 | $189m |
| 12-1 momentum (L/S) | US | +0.32 | +0.36 | +0.27 | +0.05 | +0.22 | 0.5% | 2.5% | 0.58 | $1.2bn |
|  | EU | +0.34 | +0.28 | -0.42 | -1.72 | -0.73 | 0.9% | 17.0% | 0.53 | $16m |
|  | UK | +0.43 | +0.30 | -0.74 | -2.17 | -1.14 | 1.3% | 29.1% | 0.53 | $11m |
|  | DK | +0.31 | +0.27 | -0.26 | -1.43 | -0.50 | 0.6% | 11.3% | 0.38 | $22m |
|  | SCANDI | -0.19 | -0.22 | -0.75 | -1.98 | -1.00 | 0.7% | 9.8% | 0.48 | — |
|  | World | +0.41 | +0.41 | +0.11 | -0.58 | -0.03 | 0.8% | 6.9% | 0.56 | $145m |
| low volatility (L/S) | US | -0.60 | -0.59 | -0.61 | -0.67 | -0.63 | 0.2% | 0.9% | 0.22 | — |
|  | EU | -0.08 | -0.09 | -0.28 | -0.71 | -0.37 | 0.3% | 4.6% | 0.20 | — |
|  | UK | -0.30 | -0.35 | -0.74 | -1.26 | -0.89 | 0.5% | 10.9% | 0.18 | — |
|  | DK | -0.08 | -0.10 | -0.32 | -0.82 | -0.42 | 0.3% | 5.0% | 0.16 | — |
|  | SCANDI | -0.26 | -0.27 | -0.45 | -0.86 | -0.53 | 0.3% | 3.5% | 0.18 | — |
|  | World | -0.48 | -0.48 | -0.58 | -0.81 | -0.63 | 0.3% | 2.5% | 0.20 | — |
| short-term reversal (L/S) | US | -0.36 | -0.24 | -0.57 | -1.35 | -0.72 | 1.4% | 7.9% | 1.74 | — |
|  | EU | -0.61 | -0.83 | -3.18 | -5.74 | -3.98 | 2.8% | 53.0% | 1.72 | — |
|  | UK | -0.17 | -0.67 | -4.46 | -6.51 | -5.39 | 4.1% | 91.4% | 1.71 | — |
|  | DK | -0.38 | -0.58 | -2.98 | -6.98 | -4.00 | 2.1% | 46.0% | 1.34 | — |
|  | SCANDI | +0.01 | -0.14 | -2.38 | -6.72 | -3.37 | 2.4% | 36.6% | 1.58 | — |
|  | World | -0.49 | -0.51 | -1.64 | -4.20 | -2.18 | 2.4% | 21.9% | 1.73 | — |
| low MAX (L/S) | US | -0.81 | -0.71 | -0.95 | -1.52 | -1.06 | 1.2% | 6.1% | 1.51 | — |
|  | EU | -0.09 | -0.27 | -2.42 | -5.47 | -3.28 | 2.5% | 40.1% | 1.51 | — |
|  | UK | -0.20 | -0.70 | -3.12 | -3.96 | -3.50 | 3.7% | 81.2% | 1.40 | — |
|  | DK | -0.26 | -0.41 | -2.12 | -5.41 | -2.87 | 1.7% | 35.0% | 1.09 | — |
|  | SCANDI | -0.17 | -0.28 | -2.04 | -5.76 | -2.84 | 2.1% | 28.8% | 1.38 | — |
|  | World | -0.69 | -0.70 | -1.66 | -3.68 | -2.10 | 2.2% | 18.1% | 1.50 | — |


**Reading it.**

1. **At $1m the model is close to the flat 10 bp in large-cap markets and harsher in small ones**: the spread alone costs more than 10 bp per side in the UK, EU and Scandinavian small caps.
2. **Impact grows with the square root of size**, so costs rise about three times for every tenfold increase in capital, and far faster in markets where the traded stocks are thin.
3. **Slow signals scale; fast ones do not.** Low volatility and low beta change little from month to month; reversal and low MAX replace most of the book every month and collapse even at $10m.
4. **Beta-neutral books pay twice**: their low-beta leg is levered up (about 2× in most markets), so its trades are twice as large as the capital suggests.

## 3. Exploratory fix 1 · A turnover buffer (not pre-registered)

| Market | Monthly turnover (was about 0.5) | $1m | $10m | $100m | $1bn | Sharpe halves at | Net return reaches zero at |
|---|---|---|---|---|---|---|---|
| US | 0.22 | +0.23 | +0.22 | +0.20 | +0.12 | $1.0bn | $3.0bn |
| EU | 0.23 | +0.62 | +0.54 | +0.28 | -0.49 | $79m | $233m |
| UK | 0.24 | +0.91 | +0.73 | +0.14 | -0.86 | $29m | $138m |
| DK | 0.20 | +0.27 | +0.19 | -0.05 | -0.77 | $17m | $62m |
| SCANDI | 0.18 | +0.07 | +0.01 | -0.16 | -0.68 | $4m | $12m |
| World | 0.23 | +0.49 | +0.45 | +0.34 | -0.00 | $193m | $978m |


*The FS03–FS12 fix ladder's buffer: a stock enters in the top decile (quintile, tercile) and is sold only when it leaves the top 30%.*

## 4. Exploratory fix 2 · A liquidity screen (not pre-registered)

| Market | Stocks left (median) | $1m | $10m | $100m | $1bn | Sharpe halves at | Net return reaches zero at |
|---|---|---|---|---|---|---|---|
| US | 652 | +0.27 | +0.26 | +0.20 | +0.01 | $208m | $1.0bn |
| EU | 298 | +0.45 | +0.37 | +0.12 | -0.67 | $38m | $141m |
| UK | 149 | +0.24 | +0.10 | -0.37 | -1.83 | $7m | $16m |
| DK | 24 | +0.25 | +0.11 | -0.33 | -1.60 | $8m | $18m |
| SCANDI | 79 | +0.00 | -0.12 | -0.52 | -1.75 | $1m | $1m |
| World | 1095 | +0.36 | +0.33 | +0.24 | -0.06 | $155m | $627m |


*Stocks with less than $5m average daily traded value removed before sorting.*

## 5. What it means

1. **The factsheet results are small-fund results.** Outside the US and World, the shortlist's edge disappears somewhere between $10m and $100m per book with monthly rebalancing.
2. **A buffer is the cheapest capacity there is**: it keeps most of the small-size Sharpe ratio and multiplies capacity.
3. **The UK low-beta premium lives in thin stocks.** Screened for liquidity, it largely goes away: a warning for anyone reading FS10's UK result as investable at scale.
4. **For the multifactor model**, cost-aware construction (buffers, trading towards targets over several days, liquidity-weighted positions) matters more than the choice of signals.

## 6. Caveats

- One cost model with textbook parameters; real costs depend on execution skill, venue and timing. Y = 1.0 is shown as the harsher case.
- US volume data are missing for about a third of the stocks ever in the top 500 (mostly delisted names); their ADV comes from market cap, a proxy.
- Trades are costed as if done in one day; spreading large trades over several days lowers impact but adds tracking error.
- The exploratory sections were decided after seeing the pre-registered results and are not tests.

## 7. References

- Almgren, R., Thum, C., Hauptmann, E. & Li, H. (2005). Direct estimation of equity market impact. *Risk* 18(7), 58–62.
- Frazzini, A., Israel, R. & Moskowitz, T. J. (2018). Trading costs. Working paper, AQR Capital Management.
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies* 29(1), 104–147.
- Korajczyk, R. A. & Sadka, R. (2004). Are momentum profits robust to trading costs? *Journal of Finance* 59(3), 1039–1082.
- Bouchaud, J.-P., Bonart, J., Donier, J. & Gould, M. (2018). *Trades, Quotes and Prices*. Cambridge University Press.

## 8. Reproduce

`planning/PREREG_FS16.md` → `code/impact.py` (`run`, and the exploratory `run_buffer`, `run_liquid`) → `code/build_fs16.py`. US volume from the Project1 price cache (`_data_private/pit/US_tradedvalue.parquet`, private).
