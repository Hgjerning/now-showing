# FACTSHEET FS03 · Momentum

### Buy last year's winners, sell last year's losers

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

<div class="kf" markdown="0">
<div><b>Strategy</b>Cross-sectional momentum (Carhart's UMD, AQR's momentum)</div>
<div><b>Origin</b>Jegadeesh & Titman (1993)</div>
<div><b>Family</b>Momentum & trend</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (winners)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Stocks that did best over the past year keep outperforming the worst over the next months. Jegadeesh & Titman (1993) found about 1% a month for US stocks in 1965–1989; Asness, Moskowitz & Pedersen (2013) found it in every major equity market and asset class. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -2.1% to +9.8% a year and was positive in 5 of the six; no universe passes the 2.87 gate. The long-only book (winners) had a higher Sharpe than the equal-weight universe in 5 of the six (US, EU, UK, DK, World), with alphas of +0.2% to +9.0%, passing the gate in UK, World. **What goes wrong (§10):** the main drags are a market bet (average beta -0.38, worth -4.5% a year in 2013–19), a weaker second half (2020–26). None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Momentum & trend; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours Near 52-week high, Volatility; after its closest neighbours and the market it keeps an alpha of -3.9% to +7.2% (largest |t| 2.2), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 501 / 10 | +1.7% | 0.31 | +9.8% (2.4) | -0.62 | +14.6% | 0.87 | -20% | +12.6% | 0.85 | +14.9% |
| EU | 264 / 10 | +9.8% | 1.93 | +16.7% (3.6) | -0.64 | +14.1% | 0.96 | -33% | +10.1% | 0.75 | +10.2% |
| UK | 324 / 10 | +9.3% | 1.52 | +15.6% (3.0) | -0.66 | +17.2% | 1.13 | -25% | +8.9% | 0.68 | +7.8% |
| DK | 20 / 3 | +5.9% | 1.29 | +9.4% (2.1) | -0.28 | +17.1% | 1.07 | -31% | +12.0% | 0.83 | +10.2% |
| SCANDI | 70 / 5 | -2.1% | -0.54 | +2.1% (0.6) | -0.34 | +10.5% | 0.76 | -34% | +12.2% | 0.89 | +11.0% |
| World | 1086 / 10 | +6.1% | 1.22 | +12.9% (3.5) | -0.60 | +14.6% | 0.94 | -25% | +10.5% | 0.71 | +10.3% |

*Monthly, local currency (World in USD). L/S = equal-weighted winners (highest 12-1 return) minus losers (lowest 12-1 return), net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS03_growth.png)

## 2. Strategy description

Stocks that did best over the past year keep outperforming the worst over the next months. Jegadeesh & Titman (1993) found about 1% a month for US stocks in 1965–1989; Asness, Moskowitz & Pedersen (2013) found it in every major equity market and asset class.

**Why it might work.** Behavioural: investors under-react to news and then herd (Barberis, Shleifer & Vishny 1998; Hong & Stein 1999); the disposition effect slows the price response (Grinblatt & Han 2005). Risk stories exist but explain little.

| Rule | Original (Jegadeesh & Titman (1993)) | This factsheet |
|---|---|---|
| Signal | Past 3–12 month return; the classic 12-1 skips the latest month | Return from month t−11 to t−1 (skip month t) |
| Portfolio | Decile or tercile long/short, 1–12 month holding | Extreme quantile L/S, one-month holding, monthly rebalance |
| Weighting | Equal or value weighted | Equal weighted |

## 3. Data load

| Universe | Prices | Membership | Names eligible (median) | Currency |
|---|---|---|---|---|
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: the S&P 500 members at each month-end (Sharadar add/remove history; corrected 2 Oct 2026) | ~503 | USD |
| EU | Project1 yfinance cache, Adj Close (TR) | **Point-in-time**: union of 11 national blue-chip indices (CAC 40, DAX, AEX, IBEX 35, FTSE MIB, OMXS30, OMXC25, OMXH25, BEL 20, PSI-20, WIG20), quarterly Wikipedia snapshots 2012–2026; 83% of member-quarters priced | ~238 | local (EUR, SEK, DKK, PLN) |
| UK | Project1 cache, Close + pence dividends (Yahoo under-adjusts LSE ~100×) | **Point-in-time**: FTSE 100 + FTSE 250, quarterly snapshots; 75% priced | ~242 | GBP |
| DK | Project1 cache, Adj Close | **Point-in-time**: OMX Copenhagen 25, quarterly snapshots; 91% priced | ~19 | DKK |
| SCANDI | Project1 cache, Adj Close | **Point-in-time**: OMXC25 + OMXS30 + OMXH25 (Oslo has no snapshot history); 88% priced | ~62 | local (DKK, SEK, EUR) |
| World | US Sharadar + UK + EU above | **Point-in-time** union of the three; local-currency returns summed, not converted | ~963 | mixed |

*Membership comes from Project2's cache of dated Wikipedia index pages (the same parsing as `run_wiki_pit.py` / `run_eu_pit.py`), with a short list of verified ticker renames (e.g. NZYM-B → NSIS-B, WDH → DEMANT, DAI → MBG). A name is eligible from the day after the snapshot that lists it, once it has 60 days of prices. Member-quarters without a price are mostly delisted names that Yahoo no longer serves, so some survivorship remains; see §13.*


## 4. Signal creation

MOM<sub>i,t</sub> = P<sub>i,t−1</sub> / P<sub>i,t−12</sub> − 1 on total-return prices; the most recent month is skipped to avoid the one-month reversal. Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = winners (highest 12-1 return) minus losers (lowest 12-1 return); **long-only** = winners (highest 12-1 return); benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (S&P 500 members, point-in-time)**, median 501 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +1.7% | -0.9% | 22.2% | 0.08 [-0.39, 0.53] | -0.05 | -60% | 53% | 0.31 | -0.62 | +9.8% (2.4) | 15.2% |
| Long-only (net) | +15.2% | +14.6% | 17.4% | 0.87 [0.49, 1.31] | 1.46 | -20% | 60% | 4.55 | 0.90 | +3.4% (1.7) | 9.7% |
| Winners (gross) | +15.9% | +15.4% | 17.4% | 0.92 [0.53, 1.36] | 1.56 | -20% | 61% | 4.77 | 0.90 | +4.1% (2.1) | 9.6% |
| Losers (gross) | +11.7% | +8.5% | 26.7% | 0.44 [0.00, 0.93] | 0.51 | -46% | 58% | 1.87 | 1.52 | -8.2% (-2.9) | 15.1% |
| EW universe | +13.1% | +12.6% | 15.5% | 0.85 [0.41, 1.42] | 1.29 | -28% | 67% | 4.20 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.9% | +14.9% | 14.2% | 1.05 [0.60, 1.61] | 1.73 | -24% | 69% | 5.29 | 0.86 | +3.7% (2.4) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 264 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +9.8% | +8.0% | 19.9% | 0.49 [0.01, 1.09] | 0.56 | -41% | 61% | 1.93 | -0.64 | +16.7% (3.6) | 13.0% |
| Long-only (net) | +14.3% | +14.1% | 15.0% | 0.96 [0.37, 1.64] | 1.54 | -33% | 63% | 3.22 | 0.81 | +5.6% (1.9) | 8.3% |
| Winners (gross) | +15.0% | +14.9% | 15.0% | 1.00 [0.42, 1.69] | 1.65 | -32% | 64% | 3.38 | 0.81 | +6.3% (2.1) | 8.3% |
| Losers (gross) | +3.0% | +0.3% | 23.7% | 0.13 [-0.36, 0.58] | 0.02 | -45% | 48% | 0.51 | 1.46 | -12.6% (-4.3) | 12.5% |
| EW universe | +10.7% | +10.1% | 14.3% | 0.75 [0.29, 1.30] | 1.14 | -26% | 61% | 3.18 | 1.00 | – | 8.4% |
| Size-weighted universe | +10.6% | +10.2% | 13.7% | 0.77 [0.32, 1.29] | 1.21 | -25% | 58% | 3.37 | 0.92 | +0.8% (0.6) | 7.9% |

**UK (FTSE 350, point-in-time)**, median 324 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +9.3% | +6.6% | 22.9% | 0.41 [-0.07, 0.98] | 0.39 | -52% | 61% | 1.52 | -0.66 | +15.6% (3.0) | 16.4% |
| Long-only (net) | +17.2% | +17.2% | 15.2% | 1.13 [0.58, 1.80] | 1.90 | -25% | 66% | 4.46 | 0.86 | +9.0% (3.7) | 9.1% |
| Winners (gross) | +17.8% | +18.0% | 15.2% | 1.17 [0.62, 1.85] | 2.00 | -25% | 66% | 4.63 | 0.86 | +9.6% (4.0) | 9.0% |
| Losers (gross) | +6.6% | +3.4% | 25.7% | 0.26 [-0.21, 0.73] | 0.21 | -49% | 52% | 0.97 | 1.51 | -7.9% (-2.4) | 14.6% |
| EW universe | +9.6% | +8.9% | 14.1% | 0.68 [0.19, 1.28] | 0.96 | -30% | 58% | 2.87 | 1.00 | – | 8.8% |
| Size-weighted universe | +8.4% | +7.8% | 12.9% | 0.65 [0.16, 1.25] | 0.90 | -28% | 62% | 2.68 | 0.84 | +0.3% (0.2) | 7.8% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +5.9% | +4.5% | 17.3% | 0.34 [-0.18, 0.85] | 0.39 | -47% | 55% | 1.29 | -0.28 | +9.4% (2.1) | 10.6% |
| Long-only (net) | +17.1% | +17.1% | 16.0% | 1.07 [0.49, 1.68] | 1.95 | -31% | 63% | 3.98 | 0.90 | +5.9% (2.6) | 7.7% |
| Winners (gross) | +17.5% | +17.6% | 16.0% | 1.10 [0.52, 1.71] | 2.01 | -31% | 64% | 4.08 | 0.90 | +6.3% (2.8) | 7.7% |
| Losers (gross) | +9.9% | +8.1% | 20.6% | 0.48 [0.00, 1.03] | 0.60 | -45% | 62% | 1.96 | 1.17 | -4.8% (-1.8) | 12.2% |
| EW universe | +12.6% | +12.0% | 15.2% | 0.83 [0.31, 1.44] | 1.27 | -33% | 66% | 3.31 | 1.00 | – | 8.8% |
| Size-weighted universe | +11.1% | +10.2% | 16.4% | 0.68 [0.11, 1.33] | 0.94 | -40% | 62% | 2.55 | 0.93 | -0.6% (-0.2) | 10.7% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -2.1% | -3.2% | 15.0% | -0.14 [-0.62, 0.35] | -0.28 | -56% | 50% | -0.54 | -0.34 | +2.1% (0.6) | 9.9% |
| Long-only (net) | +11.1% | +10.5% | 14.7% | 0.76 [0.21, 1.36] | 1.15 | -34% | 63% | 2.83 | 0.87 | +0.2% (0.1) | 8.4% |
| Winners (gross) | +11.7% | +11.2% | 14.7% | 0.80 [0.25, 1.40] | 1.24 | -33% | 63% | 2.98 | 0.87 | +0.8% (0.4) | 8.3% |
| Losers (gross) | +11.9% | +10.6% | 19.2% | 0.62 [0.12, 1.18] | 0.88 | -43% | 58% | 2.45 | 1.21 | -3.3% (-1.4) | 11.5% |
| EW universe | +12.6% | +12.2% | 14.2% | 0.89 [0.37, 1.51] | 1.38 | -29% | 66% | 3.63 | 1.00 | – | 8.4% |
| Size-weighted universe | +11.4% | +11.0% | 13.5% | 0.84 [0.37, 1.41] | 1.32 | -26% | 63% | 3.59 | 0.90 | +0.0% (0.0) | 8.1% |

**World (US + UK + EU, point-in-time)**, median 1086 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +6.1% | +4.1% | 19.4% | 0.31 [-0.16, 0.87] | 0.28 | -45% | 58% | 1.22 | -0.60 | +12.9% (3.5) | 14.0% |
| Long-only (net) | +15.0% | +14.6% | 15.9% | 0.94 [0.46, 1.51] | 1.55 | -25% | 63% | 4.04 | 0.86 | +5.3% (3.0) | 9.2% |
| Winners (gross) | +15.7% | +15.4% | 15.9% | 0.99 [0.51, 1.55] | 1.65 | -25% | 63% | 4.23 | 0.86 | +6.0% (3.4) | 9.1% |
| Losers (gross) | +7.4% | +4.2% | 25.8% | 0.29 [-0.18, 0.77] | 0.26 | -45% | 53% | 1.13 | 1.46 | -9.1% (-3.7) | 14.0% |
| EW universe | +11.3% | +10.5% | 16.0% | 0.71 [0.25, 1.28] | 1.02 | -30% | 63% | 3.07 | 1.00 | – | 9.7% |
| Size-weighted universe | +11.0% | +10.3% | 14.8% | 0.74 [0.28, 1.31] | 1.10 | -28% | 61% | 3.19 | 0.91 | +0.7% (0.8) | 8.9% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +12.1% | +7.6% | +60.8% | -7.0% | -0.2% | +22.4% |
| 2014 | +1.7% | +13.9% | +10.2% | +8.6% | +6.5% | +9.5% |
| 2015 | +41.4% | +36.5% | +39.1% | +24.6% | +12.0% | +38.6% |
| 2016 | -31.2% | -8.2% | -23.8% | -16.8% | -5.7% | -22.2% |
| 2017 | +6.0% | +4.4% | +21.3% | -3.7% | -3.6% | +7.6% |
| 2018 | +5.7% | -4.2% | -7.0% | +7.7% | -0.0% | -0.8% |
| 2019 | -12.3% | +1.4% | +19.8% | +42.6% | -13.4% | +1.4% |
| 2020 | -19.2% | -4.1% | -0.9% | +15.5% | -20.7% | -10.9% |
| 2021 | -21.1% | +0.6% | -14.9% | +9.0% | -0.5% | -11.8% |
| 2022 | +19.3% | -5.9% | +18.9% | -6.0% | -7.1% | +12.4% |
| 2023 | -18.0% | -8.2% | -13.5% | -16.8% | -18.8% | -11.1% |
| 2024 | +27.4% | +24.6% | +1.5% | -19.9% | +12.7% | +17.7% |
| 2025 | -3.6% | +72.6% | +16.4% | +22.3% | +6.6% | +17.1% |
| 2026 | +6.6% | +1.5% | -8.0% | +22.3% | -4.1% | +2.3% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +35.9% | +29.4% | +50.6% | +40.4% | +24.3% | +39.7% |
| 2014 | +13.0% | -4.7% | +11.1% | +13.7% | +6.3% | +1.8% |
| 2015 | +6.5% | +14.4% | +30.1% | +47.9% | +20.0% | +10.4% |
| 2016 | +2.2% | +28.4% | +23.5% | +2.0% | +30.7% | +6.5% |
| 2017 | +19.8% | +16.6% | +44.7% | +18.7% | +16.2% | +31.4% |
| 2018 | -6.4% | -10.5% | -12.7% | -1.6% | -4.2% | -11.7% |
| 2019 | +22.9% | +30.0% | +30.2% | +45.6% | +25.0% | +26.9% |
| 2020 | +16.6% | +7.1% | +13.0% | +42.3% | +8.5% | +15.5% |
| 2021 | +17.5% | +7.1% | +12.9% | +27.0% | +18.6% | +11.1% |
| 2022 | -3.0% | -20.5% | -10.5% | -20.2% | -22.8% | -12.3% |
| 2023 | +8.9% | +16.3% | +3.1% | +6.7% | -4.4% | +14.9% |
| 2024 | +31.0% | +17.5% | +10.8% | -8.2% | +7.0% | +20.2% |
| 2025 | +12.9% | +74.6% | +31.0% | +15.5% | +18.8% | +38.0% |
| 2026 | +29.2% | +11.8% | +14.6% | +27.4% | +12.1% | +21.2% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS03_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 30% | 26% | 53% | -27.6% | 2020-11 |
| EU | 163 | 27 / 26 | 29% | 24% | 61% | -33.1% | 2020-11 |
| UK | 163 | 33 / 32 | 28% | 26% | 61% | -40.1% | 2020-11 |
| DK | 163 | 7 / 6 | 17% | 19% | 55% | -14.1% | 2022-05 |
| SCANDI | 163 | 14 / 14 | 25% | 24% | 50% | -14.8% | 2018-11 |
| World | 163 | 109 / 108 | 29% | 25% | 58% | -34.0% | 2020-11 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: winners | Short: losers |
|---|---|---|
| US | SNDK, MU, WDC, LITE, STX, CIEN, INTC, DELL | CSGP, TTD, FISV, BSX, BLDR, INTU, COIN, PODD |
| EU | KGH.WA, ASML.AS, MT.AS, MTS.MC, REP.MC, ASM.AS, TYRES.HE, NOKIA.HE | ONTEX.BR, AGFB.BR, QTCOM.HE, UMG.AS, GTC.WA, BAR.BR, ADYEN.AS, STLAM.MI |
| UK | SAGA.L, CMCX.L, CWR.L, KLR.L, WOSG.L, SSIT.L, CCC.L, APN.L | VTY.L, AML.L, TEP.L, MEGP.L, BCG.L, DATA.L, ONT.L, ENT.L |
| DK | DANSKE.CO, ISS.CO, JYSK.CO, NKT.CO, VWS.CO, MAERSK-B.CO, NDA-DK.CO, MAERSK-A.CO | ZEAL.CO, COLO-B.CO, ORSTED.CO, BAVA.CO, AMBU-B.CO, GN.CO, ROCK-B.CO, NOVO-B.CO |
| SCANDI | NOKIA.HE, TYRES.HE, NESTE.HE, DANSKE.CO, JYSK.CO, SWED-A.ST, SAND.ST, ISS.CO | QTCOM.HE, ORSTED.CO, COLO-B.CO, BAVA.CO, PNDORA.CO, AMBU-B.CO, GN.CO, ELISA.HE |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -4.6% | -1.80 | 0.81 | value -0.62 (-5.4), momentum +1.51 (+11.3) |
| EU | French Europe 5F + WML | -4.1% | -1.42 | 0.66 | WML +1.50 (+13.8) |
| UK | JKP GBR 7 themes | +2.4% | 0.61 | 0.68 | momentum +1.22 (+7.0), low_risk +0.94 (+3.1), quality +0.94 (+2.3) |
| DK | JKP DNK 7 themes | -3.5% | -1.14 | 0.55 | size -0.29 (-2.7), momentum +1.14 (+11.9), quality +0.28 (+2.5), short_term_reversal +0.27 (+2.5) |
| SCANDI | French Europe 5F + WML | -10.4% | -2.88 | 0.35 | WML +0.85 (+7.6) |
| World | JKP World 7 themes | +2.8% | 0.64 | 0.63 | value -0.53 (-3.3), momentum +1.26 (+9.2) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +0.9% | 0.64 | 0.90 | mkt +0.96 (+23.5), size -0.41 (-3.8), momentum +0.79 (+9.8), low_risk -0.31 (-4.3) |
| EU | French Europe 5F + WML | +3.1% | 1.00 | 0.56 | Mkt-RF +0.75 (+13.3), WML +0.53 (+6.2) |
| UK | JKP GBR 7 themes | +8.1% | 3.78 | 0.70 | mkt +0.57 (+11.6), momentum +0.65 (+6.8), low_risk -0.59 (-4.6), quality +0.69 (+4.3) |
| DK | JKP DNK 7 themes | +5.8% | 2.23 | 0.68 | mkt +0.68 (+15.9), size -0.18 (-2.4), momentum +0.36 (+4.0), low_risk -0.46 (-5.3), quality +0.31 (+3.2) |
| SCANDI | French Europe 5F + WML | +2.5% | 0.72 | 0.48 | Mkt-RF +0.65 (+9.2), WML +0.28 (+3.5) |
| World | JKP World 7 themes | +6.5% | 2.76 | 0.77 | mkt +0.69 (+11.6), momentum +0.61 (+6.9) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 5 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** +2.1% to +16.7%, |t| past the gate in 3 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 5 of the six; alpha +0.2% to +9.0%, passing in 2 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.61, EU 0.95, UK 0.91, DK 0.89, SCANDI 0.30, World 0.86.
- **Publication decay:** gross L/S +2.0% to +17.5% a year in 2013–19 against -2.5% to +13.8% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +5.5% | -0.57 | -7.5% | +13.0% | -1.3% | +0.6% | +4.9% | 56% | 2015-04 -13%, 2016-04 -12%, 2016-03 -10% |
| EU | +10.3% | -0.58 | -6.2% | +16.5% | -1.3% | +4.1% | +6.3% | 55% | 2016-12 -11%, 2015-02 -10%, 2016-03 -10% |
| UK | +17.5% | -0.43 | -5.0% | +22.4% | -1.3% | +11.5% | +6.0% | 52% | 2016-02 -17%, 2016-04 -14%, 2013-08 -13% |
| DK | +9.1% | 0.01 | +0.2% | +9.0% | -0.9% | +6.7% | +2.5% | 36% | 2018-11 -13%, 2013-08 -10%, 2013-02 -8% |
| SCANDI | +2.0% | -0.18 | -2.7% | +4.8% | -1.2% | +1.8% | +0.2% | 50% | 2018-11 -15%, 2015-04 -9%, 2017-05 -8% |
| World | +10.0% | -0.54 | -5.8% | +15.8% | -1.3% | +3.6% | +6.4% | 54% | 2016-04 -12%, 2015-04 -11%, 2016-03 -8% |

On average across the six universes the gross spread was +9.1% a year, of which the market exposure (beta -0.38) contributed -4.5%; the beta-adjusted spread (CAPM alpha) was +13.6%. Costs took 1.2% a year at 51% monthly turnover across both legs. The long leg beat the universe by +4.7% and the short leg lagged it by +4.4% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +6.4%, +6.6%, +5.9% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.39 | – | 0.18 | – | – | +3.2% | -37% | +9.7% (2.0) | 1.2% |
| X1 beta-neutral legs | 0.55 | +0.23 (p 0.022) | 0.37 | +0.19 (p 0.080) | 6 of 6 | +4.8% | -25% | +7.6% (1.7) | 1.3% |
| X2 + turnover buffer | 0.54 | -0.02 (p 0.559) | 0.36 | -0.00 (p 0.493) | 4 of 6 | +4.3% | -26% | +6.8% (1.6) | 0.6% |
| X3 + volatility targeting | 0.43 | -0.16 (p 0.648) | 0.56 | +0.20 (p 0.009) | 4 of 6 | +5.8% | -17% | +7.9% (2.1) | 0.6% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS03_ladder.png)

- **X1 beta-neutral legs:** +0.23 design, +0.19 holdout; helps in both windows but does not pass the gate.
- **X2 + turnover buffer:** -0.02 design, -0.00 holdout; hurts in both windows.
- **X3 + volatility targeting:** -0.16 design, +0.20 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe 0.18 → 0.56, return +3.2% → +5.8% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Momentum |
|---|---|
| Series family | **Momentum & trend** |
| Academic style | Cross-sectional momentum (Carhart's UMD, AQR's momentum) |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 51% of the two legs replaced monthly |
| Market exposure | L/S beta -0.66 to -0.28 |
| Payoff shape | Treynor–Mazuy γ -3.73 to 0.43 (t -2.2 to 0.5); worst 10% of market months +2.5% to +4.5% a month, best 10% -6.1% to -2.2% |
| Nearest factor theme | momentum (4 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | Near 52-week high (6 universes), Residual momentum (4 universes), 55-day breakout (2 universes) |
| Economic rationale | Behavioural: investors under-react to news and then herd (Barberis, Shleifer & Vishny 1998; Hong & Stein 1999); the disposition effect slows the price response (Grinblatt & Han 2005). Risk stories exist but explain little. |
| Publication | Jegadeesh & Titman 1993 (data to 1989); Carhart 1997 factor; known crash risk after market rebounds (Daniel & Moskowitz 2016) |
| Where it fits | In the **momentum** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Last month return**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Momentum 12-1 **(this strategy)** | momentum | +1.00 | +1.00 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| Near 52-week high | momentum | +0.59 | +0.80 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| Residual momentum | momentum | +0.66 | +0.64 | +6.4% | +8.0% to +12.2% | 6 / 0 |
| Above 52-week low | momentum | +0.63 | +0.60 | +7.5% | +5.2% to +13.6% | 4 / 0 |
| 55-day breakout | momentum | +0.21 | +0.58 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| Volatility | low risk | -0.18 | -0.54 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| MIN5 | low risk | +0.13 | +0.52 | -0.9% | +2.3% to +13.7% | 4 / 0 |
| Volatility (252 days) | low risk | -0.15 | -0.50 | +2.4% | -12.9% to -4.8% | 0 / 3 |
| Range (MAX−MIN) | low risk | -0.14 | -0.50 | -0.7% | -15.4% to -4.8% | 0 / 4 |
| Beta | low risk | -0.11 | -0.47 | +4.4% | -12.6% to -4.2% | 0 / 4 |
| MIN (worst day) | low risk | +0.10 | +0.47 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| MAX (best day) | low risk | -0.14 | -0.42 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| Idiosyncratic vol | low risk | -0.13 | -0.42 | -3.6% | -15.5% to -4.8% | 0 / 4 |
| MAX5 | low risk | -0.15 | -0.41 | +0.6% | -11.3% to -3.5% | 0 / 2 |
| Size | size | +0.12 | +0.33 | +0.1% | -3.8% to +9.9% | 1 / 0 |
| Last month return (mirror) | short-term reversal | -0.01 | +0.33 | +1.8% | -3.2% to +11.0% | 2 / 0 |
| Same-month seasonality | seasonality | +0.12 | +0.14 | -1.9% | -9.4% to +6.6% | 0 / 1 |
| Skewness | tail direction | -0.05 | -0.10 | -0.4% | -6.7% to +3.9% | 0 / 2 |
| Net tail (MAX+MIN) | tail direction | -0.04 | +0.06 | -0.9% | -5.2% to +5.2% | 0 / 0 |

![360 map](../figures/xs_FS03_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | -2.7% | -1.48 | 0.89 | Near 52-week high +0.71 (+7.5), Size +0.41 (+5.4), 55-day breakout -0.35 (-4.0), Above 52-week low +0.35 (+5.5), Residual momentum +0.26 (+3.3) |
| EU | -1.6% | -0.53 | 0.80 | Near 52-week high +1.07 (+9.9), Residual momentum +0.33 (+3.7), MIN5 -0.31 (-2.6) |
| UK | +7.2% | 2.19 | 0.76 | Near 52-week high +1.25 (+9.9), MIN5 -0.38 (-2.2), 55-day breakout -0.28 (-2.3) |
| DK | -0.2% | -0.07 | 0.74 | Near 52-week high +0.31 (+5.8), Above 52-week low +0.41 (+6.9), Residual momentum +0.41 (+8.8), Size +0.19 (+3.4) |
| SCANDI | -3.9% | -1.51 | 0.69 | Near 52-week high +0.67 (+9.3), Residual momentum +0.32 (+5.3), Above 52-week low +0.22 (+2.3) |
| World | +2.4% | 1.26 | 0.90 | Near 52-week high +1.17 (+15.4), 55-day breakout -0.26 (-3.0), Residual momentum +0.40 (+5.5), MIN5 -0.25 (-2.9) |

![Double sort](../figures/xs_FS03_dsort.png)

Holding Last month return fixed (down a column), moving from low to high Momentum 12-1 changes the return by +2.2, +4.7 and +4.9 points a year; holding Momentum 12-1 fixed (along a row), moving from low to high Last month return changes it by -2.8, +0.9 and +0.0.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -4% vs +27% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +7.2%, +6.4%, +6.6%, +5.9% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1), 65–91.
- Carhart, M. (1997). On persistence in mutual fund performance. *Journal of Finance*, 52(1), 57–82.
- Asness, C., Moskowitz, T. & Pedersen, L. H. (2013). Value and momentum everywhere. *Journal of Finance*, 68(3), 929–985.
- Daniel, K. & Moskowitz, T. (2016). Momentum crashes. *Journal of Financial Economics*, 122(2), 221–247.
- Barberis, N., Shleifer, A. & Vishny, R. (1998). A model of investor sentiment. *Journal of Financial Economics*, 49(3), 307–343.
- Hong, H. & Stein, J. (1999). A unified theory of underreaction, momentum trading, and overreaction in asset markets. *Journal of Finance*, 54(6), 2143–2184.
- Grinblatt, M. & Han, B. (2005). Prospect theory, mental accounting, and momentum. *Journal of Financial Economics*, 78(2), 311–339.
- Newey, W. & West, K. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.
- Politis, D. & Romano, J. (1994). The stationary bootstrap. *Journal of the American Statistical Association*, 89(428), 1303–1313.
- Bailey, D. & López de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk*, 15(2), 3–44.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5), 2465–2518.
- Fama, E. & French, K. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1–22.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance*, 71(1), 5–32.
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies*, 29(1), 104–147.
- Barroso, P. & Santa-Clara, P. (2015). Momentum has its moments. *Journal of Financial Economics*, 116(1), 111–120.
- Moreira, A. & Muir, T. (2017). Volatility-managed portfolios. *Journal of Finance*, 72(4), 1611–1644.
- Treynor, J. & Mazuy, K. (1966). Can mutual funds outguess the market? *Harvard Business Review*, 44(4), 131–136.

## 15. Reproduce

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS03` → `build_xs.py FS03`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
