# FACTSHEET FS16 · Costs that grow with size

### How much money can these strategies hold before trading costs eat them?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

| Key facts | |
|---|---|
| Rules | `planning/PREREG_FS16.md`, written in the build environment before the run (10:13) and copied to the Factsheets folder right after it (the run finished 10:16); no changes |
| Cost per trade | half-spread 5 bp × (ADV / $50m)^−0.3, 2–50 bp, plus square-root impact 0.7 × daily volatility × √(trade / ADV); sensitivity 1.0 |
| ADV | 63-day average traded value in USD per stock (US: price × volume where the Project1 cache has it; otherwise market cap × the size-quintile median ratio) |
| Sizes | $1m, $10m, $100m, $1bn, $10bn of capital per book |
| Books | the shortlist (low beta + 12-1 momentum, beta-neutral) and four raw long/short books, six markets, 2013–2026; borrow fees and financing as before |
| Replaces | the flat 10 bp per side used in FS01–FS15 |

> **In one paragraph.** Capacity is the binding constraint for these books, far more than the flat-cost results suggested. The shortlist keeps a positive Sharpe ratio up to about **$1.0bn in the US** and **$33m across World**, but only **$26m in the EU, $3m in the UK and $16m in Denmark**, and nothing in Scandinavia. The UK and EU books look best at small size because their low-beta legs sit in thinly traded stocks, which is also why they fill up first. The fast signals are uninvestable: short-term reversal has a Sharpe ratio of -2.27 to -0.29 already at $10m. Two exploratory fixes help: a turnover buffer (hold a stock until it leaves the top 30%) halves turnover and raises the size at which the Sharpe ratio halves 1–16 times with little loss at small size; a liquidity screen raises capacity in the EU and World but removes most of the UK result.

![Capacity](../figures/fs16_capacity.png)

## 1. The shortlist, as pre-registered

| Market | $1m | $10m | $100m | $1bn | $10bn | Sharpe halves at | Net return reaches zero at |
|---|---|---|---|---|---|---|---|
| US | +0.26 | +0.24 | +0.18 | +0.01 | -0.53 | $207m | $1.0bn |
| EU | +0.69 | +0.38 | -0.54 | -2.03 | -2.72 | $11m | $26m |
| UK | +0.45 | -0.44 | -1.23 | -1.46 | -1.51 | $2m | $3m |
| DK | +0.23 | +0.09 | -0.35 | -1.66 | -4.13 | $7m | $16m |
| SCANDI | +0.17 | +0.03 | -0.40 | -1.74 | -4.68 | $4m | $12m |
| World | +0.43 | +0.27 | -0.25 | -1.54 | -2.56 | $13m | $33m |


*Sharpe ratio, net of spread, impact (Y = 0.7), borrow fees and financing, 2013–2026. Capital per book; the combined shortlist puts half in each leg.*

## 2. Every book, every market

| Book | Market | Flat 10 bp | $1m | $100m | $1bn | $100m, Y = 1.0 | Spread cost / yr | All-in cost / yr at $100m | Monthly turnover | Net return reaches zero at |
|---|---|---|---|---|---|---|---|---|---|---|
| low beta (beta-neutral) | US | +0.19 | +0.21 | +0.17 | +0.08 | +0.15 | 0.3% | 1.8% | 0.41 | $1.8bn |
|  | EU | +0.56 | +0.47 | -0.35 | -1.40 | -0.66 | 0.9% | 29.2% | 0.45 | $27m |
|  | UK | +0.80 | +0.34 | -0.94 | -1.09 | -1.01 | 1.5% | 119.1% | 0.51 | $3m |
|  | DK | +0.08 | +0.06 | -0.22 | -0.87 | -0.36 | 0.3% | 5.6% | 0.20 | $7m |
|  | SCANDI | +0.29 | +0.28 | +0.01 | -0.64 | -0.12 | 0.4% | 5.7% | 0.28 | $103m |
|  | World | +0.30 | +0.26 | -0.22 | -1.13 | -0.44 | 0.8% | 16.7% | 0.48 | $25m |
| 12-1 momentum (beta-neutral) | US | +0.15 | +0.19 | +0.10 | -0.14 | +0.05 | 0.5% | 2.3% | 0.57 | $262m |
|  | EU | +0.72 | +0.61 | -0.48 | -1.46 | -0.83 | 1.0% | 21.5% | 0.56 | $26m |
|  | UK | +0.73 | +0.41 | -1.43 | -2.16 | -1.75 | 1.3% | 53.6% | 0.55 | $4m |
|  | DK | +0.33 | +0.28 | -0.30 | -1.63 | -0.58 | 0.7% | 11.1% | 0.41 | $21m |
|  | SCANDI | -0.03 | -0.07 | -0.70 | -2.15 | -1.00 | 0.8% | 10.5% | 0.54 | — |
|  | World | +0.53 | +0.50 | -0.14 | -1.35 | -0.43 | 0.8% | 11.2% | 0.55 | $51m |
| 12-1 momentum (L/S) | US | +0.08 | +0.11 | +0.02 | -0.17 | -0.02 | 0.5% | 2.5% | 0.55 | $132m |
|  | EU | +0.49 | +0.40 | -0.54 | -1.48 | -0.86 | 0.9% | 23.0% | 0.53 | $17m |
|  | UK | +0.41 | +0.16 | -1.32 | -1.98 | -1.60 | 1.3% | 56.4% | 0.53 | $2m |
|  | DK | +0.34 | +0.30 | -0.23 | -1.41 | -0.47 | 0.6% | 10.8% | 0.36 | $27m |
|  | SCANDI | -0.14 | -0.18 | -0.73 | -2.01 | -0.99 | 0.8% | 10.1% | 0.49 | — |
|  | World | +0.31 | +0.28 | -0.24 | -1.27 | -0.48 | 0.8% | 12.2% | 0.54 | $24m |
| low volatility (L/S) | US | -0.34 | -0.33 | -0.35 | -0.41 | -0.36 | 0.2% | 0.9% | 0.19 | — |
|  | EU | +0.08 | +0.06 | -0.17 | -0.69 | -0.28 | 0.3% | 5.6% | 0.20 | $11m |
|  | UK | -0.28 | -0.34 | -0.76 | -1.18 | -0.90 | 0.5% | 13.3% | 0.17 | — |
|  | DK | -0.06 | -0.08 | -0.31 | -0.85 | -0.42 | 0.3% | 5.0% | 0.17 | — |
|  | SCANDI | -0.19 | -0.20 | -0.37 | -0.79 | -0.46 | 0.3% | 3.7% | 0.18 | — |
|  | World | -0.27 | -0.28 | -0.40 | -0.68 | -0.46 | 0.3% | 3.2% | 0.19 | — |
| short-term reversal (L/S) | US | -0.31 | -0.21 | -0.56 | -1.42 | -0.73 | 1.4% | 8.8% | 1.74 | — |
|  | EU | -0.79 | -1.12 | -3.64 | -4.81 | -4.16 | 3.0% | 67.3% | 1.72 | — |
|  | UK | -0.32 | -1.32 | -2.58 | -2.59 | -2.59 | 4.1% | 209.3% | 1.70 | — |
|  | DK | -0.42 | -0.63 | -3.09 | -7.37 | -4.15 | 2.1% | 44.7% | 1.34 | — |
|  | SCANDI | +0.05 | -0.11 | -2.44 | -6.92 | -3.49 | 2.5% | 37.8% | 1.60 | — |
|  | World | -0.50 | -0.66 | -2.56 | -3.85 | -3.08 | 2.6% | 43.8% | 1.72 | — |
| low MAX (L/S) | US | -0.58 | -0.47 | -0.73 | -1.36 | -0.86 | 1.2% | 6.4% | 1.50 | — |
|  | EU | +0.13 | -0.12 | -2.26 | -3.63 | -2.80 | 2.6% | 50.0% | 1.48 | — |
|  | UK | -0.29 | -1.27 | -2.65 | -2.68 | -2.67 | 3.7% | 166.5% | 1.38 | — |
|  | DK | -0.23 | -0.38 | -2.16 | -5.51 | -2.93 | 1.7% | 34.9% | 1.11 | — |
|  | SCANDI | -0.16 | -0.28 | -2.09 | -5.98 | -2.93 | 2.1% | 29.1% | 1.39 | — |
|  | World | -0.44 | -0.58 | -2.21 | -3.59 | -2.70 | 2.3% | 35.1% | 1.48 | — |


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
- US volume data are missing for about a third of the stocks ever in the US universe (mostly delisted names); their ADV comes from market cap, a proxy.
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
