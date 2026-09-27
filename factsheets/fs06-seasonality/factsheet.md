# FACTSHEET FS06 · Same-month seasonality

### Do stocks repeat their best calendar month?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Return seasonality (cross-sectional)</div>
<div><b>Origin</b>Heston & Sadka (2008)</div>
<div><b>Family</b>Calendar & seasonality</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (stocks with the highest past returns in the coming calendar month)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** A stock that did well relative to others in, say, March tends to do well again in March in later years, at annual lags up to 20 years. Heston & Sadka (2008) found it in US stocks 1965–2002; Keloharju, Linnainmaa & Nyberg (2016) found the same across markets and asset classes. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -12.7% to +3.1% a year and was positive in 1 of the six; no universe passes the 2.87 gate (significantly negative in EU). The long-only book (stocks with the highest past returns in the coming calendar month) had a higher Sharpe than the equal-weight universe in 1 of the six (UK), with alphas of -6.2% to +2.5%, none past the gate. **What goes wrong (§10):** the main drags are costs of about 3.9% a year. None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Calendar & seasonality; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours Size, Momentum 12-1; after those neighbours and the market, nothing is left (alpha |t| < 2 everywhere): the signal is redundant.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 500 / 10 | -8.3% | -2.81 | -10.0% (-3.3) | 0.12 | +12.0% | 0.66 | -35% | +14.1% | 0.95 | +15.3% |
| EU | 238 / 10 | -10.9% | -3.60 | -9.5% (-3.1) | -0.13 | +5.9% | 0.42 | -34% | +10.8% | 0.78 | +10.1% |
| UK | 238 / 10 | +3.1% | 0.64 | +2.6% (0.5) | 0.05 | +13.5% | 0.78 | -35% | +9.8% | 0.74 | +8.5% |
| DK | 19 / 3 | -12.7% | -2.74 | -12.5% (-2.8) | -0.01 | +5.5% | 0.39 | -43% | +12.3% | 0.82 | +10.3% |
| SCANDI | 62 / 5 | -7.3% | -2.13 | -5.9% (-1.6) | -0.11 | +10.2% | 0.69 | -39% | +12.5% | 0.91 | +10.7% |
| World | 968 / 10 | -2.9% | -1.17 | -2.9% (-1.1) | -0.00 | +12.3% | 0.71 | -40% | +11.9% | 0.80 | +10.8% |

*Monthly, local currency (World in USD). L/S = equal-weighted stocks with the highest past returns in the coming calendar month minus stocks with the lowest, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS06_growth.png)

## 2. Strategy description

A stock that did well relative to others in, say, March tends to do well again in March in later years, at annual lags up to 20 years. Heston & Sadka (2008) found it in US stocks 1965–2002; Keloharju, Linnainmaa & Nyberg (2016) found the same across markets and asset classes.

**Why it might work.** Recurring demand and information flows tied to the calendar (earnings seasons, dividend timing, fund flows); Keloharju et al. (2016) argue it reflects seasonal variation in risk premia.

| Rule | Original (Heston & Sadka (2008)) | This factsheet |
|---|---|---|
| Signal | Average return in the same calendar month over the past 1–20 years | Average return in the coming calendar month over all prior years available (1 year in 2013, 13 by 2026) |
| Portfolio | Decile L/S, one month | Extreme quantile L/S, one month |
| Weighting | Equal weighted | Equal weighted |

## 3. Data load

| Universe | Prices | Membership | Names eligible (median) | Currency |
|---|---|---|---|---|
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: top 500 by market cap each month-end (Sharadar filings × price, A06 method) | ~499 | USD |
| EU | Project1 yfinance cache, Adj Close (TR) | **Point-in-time**: union of 11 national blue-chip indices (CAC 40, DAX, AEX, IBEX 35, FTSE MIB, OMXS30, OMXC25, OMXH25, BEL 20, PSI-20, WIG20), quarterly Wikipedia snapshots 2012–2026; 83% of member-quarters priced | ~238 | local (EUR, SEK, DKK, PLN) |
| UK | Project1 cache, Close + pence dividends (Yahoo under-adjusts LSE ~100×) | **Point-in-time**: FTSE 100 + FTSE 250, quarterly snapshots; 75% priced | ~242 | GBP |
| DK | Project1 cache, Adj Close | **Point-in-time**: OMX Copenhagen 25, quarterly snapshots; 91% priced | ~19 | DKK |
| SCANDI | Project1 cache, Adj Close | **Point-in-time**: OMXC25 + OMXS30 + OMXH25 (Oslo has no snapshot history); 88% priced | ~62 | local (DKK, SEK, EUR) |
| World | US Sharadar + UK + EU above | **Point-in-time** union of the three; local-currency returns summed, not converted | ~963 | mixed |

*Membership comes from Project2's cache of dated Wikipedia index pages (the same parsing as `run_wiki_pit.py` / `run_eu_pit.py`), with a short list of verified ticker renames (e.g. NZYM-B → NSIS-B, WDH → DEMANT, DAI → MBG). A name is eligible from the day after the snapshot that lists it, once it has 60 days of prices. Member-quarters without a price are mostly delisted names that Yahoo no longer serves, so some survivorship remains; see §13.*

- **Data gap:** Price history starts in 2011–2012, so the signal averages 1 prior year in 2013 and at most 13 by 2026; Heston & Sadka use up to 20. The early years test a much noisier signal than the paper's.

## 4. Signal creation

SEAS<sub>i,t</sub> = mean of r<sub>i,m</sub> over the months m with the same calendar month as t+1 in earlier years. Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = stocks with the highest past returns in the coming calendar month minus stocks with the lowest; **long-only** = stocks with the highest past returns in the coming calendar month; benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (top 500, point-in-time)**, median 500 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -8.3% | -8.7% | 12.5% | -0.67 [-1.14, -0.19] | -0.86 | -72% | 45% | -2.81 | 0.12 | -10.0% (-3.3) | 8.6% |
| Long-only (net) | +13.4% | +12.0% | 20.4% | 0.66 [0.22, 1.18] | 0.93 | -35% | 63% | 2.94 | 1.23 | -4.3% (-2.2) | 12.6% |
| Stocks with the highest past returns in the coming calendar month (gross) | +15.4% | +14.2% | 20.4% | 0.76 [0.31, 1.29] | 1.13 | -34% | 64% | 3.38 | 1.23 | -2.3% (-1.2) | 12.4% |
| Stocks with the lowest (gross) | +18.8% | +18.6% | 18.3% | 1.03 [0.57, 1.61] | 1.70 | -31% | 66% | 5.10 | 1.12 | +2.7% (1.6) | 10.6% |
| EW universe | +14.4% | +14.1% | 15.1% | 0.95 [0.52, 1.53] | 1.52 | -25% | 68% | 4.80 | 1.00 | – | 8.9% |
| Size-weighted universe | +15.4% | +15.3% | 14.4% | 1.07 [0.61, 1.64] | 1.79 | -24% | 69% | 5.27 | 0.90 | +2.4% (1.8) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -10.9% | -11.2% | 13.2% | -0.83 [-1.27, -0.41] | -0.98 | -83% | 44% | -3.60 | -0.13 | -9.5% (-3.1) | 9.7% |
| Long-only (net) | +7.2% | +5.9% | 17.2% | 0.42 [-0.07, 0.96] | 0.53 | -34% | 56% | 1.64 | 1.07 | -4.9% (-2.5) | 9.9% |
| Stocks with the highest past returns in the coming calendar month (gross) | +9.3% | +8.1% | 17.2% | 0.54 [0.05, 1.08] | 0.75 | -31% | 58% | 2.11 | 1.07 | -2.8% (-1.5) | 9.8% |
| Stocks with the lowest (gross) | +15.3% | +14.3% | 19.4% | 0.79 [0.33, 1.31] | 1.23 | -28% | 63% | 3.29 | 1.19 | +1.7% (0.8) | 10.5% |
| EW universe | +11.4% | +10.8% | 14.5% | 0.78 [0.33, 1.33] | 1.22 | -26% | 63% | 3.34 | 1.00 | – | 8.3% |
| Size-weighted universe | +10.7% | +10.1% | 14.3% | 0.75 [0.28, 1.28] | 1.14 | -26% | 60% | 3.12 | 0.95 | -0.1% (-0.1) | 8.3% |

**UK (FTSE 350, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +3.1% | +2.1% | 14.3% | 0.22 [-0.40, 0.86] | 0.22 | -50% | 53% | 0.64 | 0.05 | +2.6% (0.5) | 8.5% |
| Long-only (net) | +14.4% | +13.5% | 18.4% | 0.78 [0.29, 1.35] | 1.27 | -35% | 59% | 3.31 | 1.14 | +2.5% (0.8) | 9.7% |
| Stocks with the highest past returns in the coming calendar month (gross) | +16.4% | +15.8% | 18.4% | 0.90 [0.39, 1.48] | 1.53 | -34% | 60% | 3.78 | 1.14 | +4.6% (1.5) | 9.5% |
| Stocks with the lowest (gross) | +8.5% | +7.2% | 17.3% | 0.49 [0.00, 1.05] | 0.63 | -34% | 57% | 1.83 | 1.09 | -2.8% (-1.1) | 10.2% |
| EW universe | +10.4% | +9.8% | 14.1% | 0.74 [0.25, 1.34] | 1.07 | -29% | 60% | 3.21 | 1.00 | – | 8.7% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.71 [0.21, 1.31] | 1.01 | -27% | 62% | 2.94 | 0.82 | +0.4% (0.2) | 7.7% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -12.7% | -13.0% | 14.9% | -0.85 [-1.46, -0.27] | -1.04 | -85% | 37% | -2.74 | -0.01 | -12.5% (-2.8) | 9.7% |
| Long-only (net) | +7.1% | +5.5% | 18.3% | 0.39 [-0.13, 0.96] | 0.47 | -43% | 55% | 1.42 | 1.03 | -6.2% (-2.6) | 10.8% |
| Stocks with the highest past returns in the coming calendar month (gross) | +8.6% | +7.2% | 18.4% | 0.47 [-0.05, 1.06] | 0.62 | -42% | 56% | 1.73 | 1.03 | -4.6% (-2.0) | 10.7% |
| Stocks with the lowest (gross) | +17.3% | +16.8% | 18.4% | 0.94 [0.39, 1.59] | 1.55 | -32% | 62% | 3.48 | 1.05 | +3.9% (1.4) | 10.1% |
| EW universe | +12.8% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.26 | -33% | 64% | 3.20 | 1.00 | – | 9.3% |
| Size-weighted universe | +11.2% | +10.3% | 16.6% | 0.68 [0.11, 1.32] | 0.94 | -40% | 61% | 2.52 | 0.91 | -0.5% (-0.2) | 10.8% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -7.3% | -7.7% | 12.1% | -0.60 [-1.16, -0.04] | -0.80 | -69% | 41% | -2.13 | -0.11 | -5.9% (-1.6) | 7.7% |
| Long-only (net) | +11.0% | +10.2% | 15.8% | 0.69 [0.14, 1.32] | 1.06 | -39% | 62% | 2.47 | 1.01 | -2.0% (-0.9) | 8.5% |
| Stocks with the highest past returns in the coming calendar month (gross) | +12.8% | +12.3% | 15.8% | 0.81 [0.25, 1.45] | 1.32 | -38% | 62% | 2.90 | 1.01 | -0.1% (-0.0) | 8.4% |
| Stocks with the lowest (gross) | +15.6% | +15.0% | 17.6% | 0.89 [0.32, 1.56] | 1.35 | -33% | 65% | 3.35 | 1.12 | +1.2% (0.6) | 10.8% |
| EW universe | +12.8% | +12.5% | 14.1% | 0.91 [0.38, 1.54] | 1.42 | -29% | 67% | 3.62 | 1.00 | – | 8.3% |
| Size-weighted universe | +11.2% | +10.7% | 13.9% | 0.80 [0.31, 1.37] | 1.21 | -27% | 63% | 3.26 | 0.95 | -1.0% (-0.9) | 8.6% |

**World (US + UK + EU, point-in-time)**, median 968 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -2.9% | -3.3% | 9.6% | -0.30 [-0.79, 0.19] | -0.45 | -48% | 47% | -1.17 | -0.00 | -2.9% (-1.1) | 6.3% |
| Long-only (net) | +13.4% | +12.3% | 18.9% | 0.71 [0.22, 1.27] | 1.03 | -40% | 62% | 2.95 | 1.14 | -0.9% (-0.5) | 11.4% |
| Stocks with the highest past returns in the coming calendar month (gross) | +15.4% | +14.6% | 18.9% | 0.82 [0.33, 1.39] | 1.25 | -38% | 63% | 3.39 | 1.14 | +1.1% (0.6) | 11.2% |
| Stocks with the lowest (gross) | +13.5% | +12.3% | 18.8% | 0.71 [0.26, 1.26] | 1.05 | -34% | 63% | 3.10 | 1.15 | -0.9% (-0.7) | 11.1% |
| EW universe | +12.5% | +11.9% | 15.7% | 0.80 [0.33, 1.37] | 1.20 | -29% | 64% | 3.53 | 1.00 | – | 9.4% |
| Size-weighted universe | +11.4% | +10.8% | 15.0% | 0.76 [0.29, 1.33] | 1.14 | -28% | 63% | 3.23 | 0.94 | -0.4% (-0.4) | 9.0% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -12.6% | -15.0% | +14.9% | -28.0% | -24.9% | -11.9% |
| 2014 | -12.5% | -9.3% | +27.2% | +9.9% | +1.9% | -5.9% |
| 2015 | -2.6% | -0.7% | +31.3% | -17.2% | +0.6% | +0.6% |
| 2016 | -11.7% | -16.1% | -19.9% | -14.3% | -5.6% | -11.8% |
| 2017 | -20.3% | -8.5% | +4.8% | -24.6% | -11.3% | -10.8% |
| 2018 | -3.1% | -21.2% | -6.9% | -10.1% | -14.9% | +1.1% |
| 2019 | -12.7% | -1.8% | +0.9% | -6.1% | +10.3% | -3.4% |
| 2020 | +15.6% | -6.2% | +17.5% | +19.2% | +3.2% | +6.9% |
| 2021 | -2.7% | -20.5% | -0.7% | -30.5% | -18.4% | +0.5% |
| 2022 | -28.1% | -1.1% | -18.2% | -7.7% | -6.8% | -17.3% |
| 2023 | +12.8% | -4.3% | +2.3% | -19.0% | +6.6% | +15.6% |
| 2024 | +5.8% | -23.8% | -18.4% | -13.2% | -5.2% | +5.7% |
| 2025 | -20.6% | -12.6% | +6.3% | +7.2% | -17.9% | -6.9% |
| 2026 | -15.1% | -6.7% | +3.3% | -26.4% | -15.1% | -2.6% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +21.8% | +21.9% | +34.2% | +24.2% | +14.7% | +21.3% |
| 2014 | +10.1% | +1.8% | +25.6% | +18.4% | +18.1% | +5.0% |
| 2015 | +0.3% | +2.8% | +23.1% | +13.3% | +13.1% | +2.8% |
| 2016 | +2.6% | +7.2% | +12.8% | +8.1% | +28.5% | +0.6% |
| 2017 | +10.3% | +12.5% | +39.6% | +3.4% | +12.8% | +25.8% |
| 2018 | -9.2% | -24.9% | -9.2% | -15.5% | -15.9% | -9.8% |
| 2019 | +25.4% | +24.2% | +22.9% | +14.2% | +43.6% | +27.5% |
| 2020 | +34.5% | +11.8% | +20.3% | +55.3% | +32.6% | +26.5% |
| 2021 | +24.8% | +0.4% | +13.1% | +4.2% | +9.0% | +17.1% |
| 2022 | -30.7% | -15.0% | -24.3% | -25.9% | -22.8% | -27.5% |
| 2023 | +36.2% | +17.8% | +11.5% | -4.6% | +7.8% | +33.5% |
| 2024 | +28.3% | +1.4% | -8.0% | -5.0% | -0.9% | +19.1% |
| 2025 | +10.5% | +17.4% | +13.7% | +16.4% | +8.3% | +19.7% |
| 2026 | +19.3% | +14.1% | +27.5% | -8.4% | +7.5% | +23.8% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS06_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 50 / 50 | 83% | 87% | 45% | -13.7% | 2022-01 |
| EU | 163 | 24 / 23 | 86% | 83% | 44% | -12.9% | 2024-10 |
| UK | 163 | 24 / 23 | 85% | 84% | 53% | -16.3% | 2016-06 |
| DK | 163 | 7 / 6 | 65% | 71% | 37% | -12.4% | 2021-12 |
| SCANDI | 163 | 13 / 12 | 78% | 80% | 41% | -10.1% | 2025-04 |
| World | 163 | 97 / 96 | 85% | 85% | 47% | -10.3% | 2022-01 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks with the highest past returns in the coming calendar month | Short: stocks with the lowest |
|---|---|---|
| US | SNDK, GEV, APP, CEG, HOOD, PLTR, RDDT, TKO | CVNA, KVUE, DXCM, VTRS, EFX, THC, XYZ, INCY |
| EU | ZEAL.CO, JSW.WA, HM-B.ST, NKT.CO, BOL.ST, FORTUM.HE, BKT.MC, ITX.MC | PUIG.MC, DSFIR.AS, DTG.DE, BMPS.MI, BAVA.CO, ANE.MC, ORSTED.CO, EDEN.PA |
| UK | CWR.L, ALFA.L, GDWN.L, TRST.L, HWG.L, JD.L, AVON.L, EWG.L | MTLN.L, THG.L, OCDO.L, AML.L, MTRO.L, OXIG.L, DOCS.L, BCG.L |
| DK | ZEAL.CO, NKT.CO, NDA-DK.CO, JYSK.CO, GMAB.CO, TRYG.CO, VWS.CO, DSV.CO | BAVA.CO, ORSTED.CO, GN.CO, DEMANT.CO, AMBU-B.CO, ISS.CO, COLO-B.CO, NOVO-B.CO |
| SCANDI | ZEAL.CO, HM-B.ST, NKT.CO, BOL.ST, FORTUM.HE, SWED-A.ST, NOKIA.HE, SKA-B.ST | BAVA.CO, ORSTED.CO, METSO.HE, QTCOM.HE, EQT.ST, WRT1V.HE, GN.CO, DEMANT.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -8.4% | -3.29 | 0.25 | mkt +0.16 (+2.9), value -0.63 (-4.4), momentum -0.30 (-2.6) |
| EU | French Europe 5F + WML | -9.2% | -2.71 | 0.12 | HML -0.38 (-2.4) |
| UK | JKP GBR 7 themes | +0.8% | 0.16 | 0.20 | quality +0.78 (+2.6), short_term_reversal -0.57 (-2.9) |
| DK | JKP DNK 7 themes | -7.5% | -1.94 | 0.08 | none |t| ≥ 2 |
| SCANDI | French Europe 5F + WML | -4.2% | -1.35 | 0.14 | HML -0.41 (-2.5) |
| World | JKP World 7 themes | -0.5% | -0.21 | 0.27 | mkt +0.14 (+3.0), value -0.69 (-4.9), momentum -0.28 (-2.9), low_risk +0.33 (+2.2) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +1.0% | 0.54 | 0.90 | mkt +1.08 (+26.8), size -0.45 (-3.5), low_risk -0.35 (-2.2) |
| EU | French Europe 5F + WML | +2.4% | 0.79 | 0.68 | Mkt-RF +0.81 (+12.5), CMA -0.48 (-2.6) |
| UK | JKP GBR 7 themes | +7.4% | 2.30 | 0.71 | mkt +0.70 (+11.7), low_risk -0.71 (-3.1), quality +0.80 (+3.2) |
| DK | JKP DNK 7 themes | +2.1% | 0.68 | 0.64 | mkt +0.63 (+8.3), low_risk -0.69 (-4.4) |
| SCANDI | French Europe 5F + WML | +7.7% | 2.62 | 0.58 | Mkt-RF +0.67 (+10.1), WML -0.19 (-2.5) |
| World | JKP World 7 themes | +7.0% | 3.07 | 0.82 | mkt +0.89 (+14.5) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 1 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -12.5% to +2.6%, |t| past the gate in 2 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 1 of the six; alpha -6.2% to +2.5%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.01, EU 0.00, UK 0.79, DK 0.00, SCANDI 0.01, World 0.13.
- **Publication decay:** gross L/S -10.0% to +11.9% a year in 2013–19 against -7.3% to +5.2% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | -6.3% | -0.02 | -0.2% | -6.1% | -4.1% | -3.0% | -3.3% | 173% | 2013-05 -7%, 2019-06 -7%, 2016-01 -6% |
| EU | -5.6% | -0.06 | -0.7% | -4.8% | -4.0% | -3.1% | -2.5% | 168% | 2013-04 -10%, 2016-01 -10%, 2016-03 -9% |
| UK | +11.9% | 0.11 | +1.4% | +10.5% | -4.1% | +8.7% | +3.2% | 169% | 2016-06 -16%, 2016-09 -7%, 2018-08 -6% |
| DK | -10.0% | -0.16 | -2.4% | -7.6% | -3.3% | -4.3% | -5.7% | 137% | 2016-12 -11%, 2013-07 -8%, 2013-09 -8% |
| SCANDI | -2.0% | -0.27 | -4.2% | +2.2% | -3.8% | +1.6% | -3.6% | 159% | 2013-09 -9%, 2017-08 -7%, 2018-04 -7% |
| World | -1.2% | 0.04 | +0.5% | -1.6% | -4.1% | +0.2% | -1.3% | 171% | 2013-05 -6%, 2013-04 -6%, 2013-06 -5% |

On average across the six universes the gross spread was -2.2% a year, of which the market exposure (beta -0.06) contributed -0.9%; the beta-adjusted spread (CAPM alpha) was -1.2%. Costs took 3.9% a year at 163% monthly turnover across both legs. The long leg beat the universe by +0.0% and the short leg lagged it by -2.2% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages -1.8%, +1.1%, -0.4% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.69 | – | -0.62 | – | – | -6.1% | -46% | -6.3% (-1.5) | 3.9% |
| X1 beta-neutral legs | -0.72 | -0.10 (p 0.848) | -0.85 | -0.23 (p 0.916) | 0 of 6 | -7.7% | -51% | -7.8% (-2.0) | 3.8% |
| X2 + turnover buffer | -0.71 | +0.01 (p 0.453) | -0.66 | +0.19 (p 0.030) | 5 of 6 | -5.5% | -45% | -5.4% (-1.4) | 3.0% |
| X3 + volatility targeting | -0.62 | +0.00 (p 0.496) | -0.56 | +0.09 (p 0.170) | 3 of 6 | -5.0% | -45% | -4.8% (-1.1) | 3.0% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS06_ladder.png)

- **X1 beta-neutral legs:** -0.10 design, -0.23 holdout; hurts in both windows.
- **X2 + turnover buffer:** +0.01 design, +0.19 holdout; helps in both windows but does not pass the gate.
- **X3 + volatility targeting:** +0.00 design, +0.09 holdout; helps in both windows but does not pass the gate.

**Where it ends:** holdout Sharpe -0.62 → -0.56, return -6.1% → -5.0% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Same-month seasonality |
|---|---|
| Series family | **Calendar & seasonality** |
| Academic style | Return seasonality (cross-sectional) |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 163% of the two legs replaced monthly |
| Market exposure | L/S beta -0.13 to 0.12 |
| Payoff shape | Treynor–Mazuy γ -0.35 to 2.17 (t -0.4 to 1.9); worst 10% of market months -2.0% to +0.0% a month, best 10% -1.4% to +1.2% |
| Nearest factor theme | investment (4 of 6 universes), HML (2 of 6 universes) |
| Nearest library signals (returns) | Size (4 universes), 55-day breakout (3 universes), Last month return (3 universes) |
| Economic rationale | Recurring demand and information flows tied to the calendar (earnings seasons, dividend timing, fund flows); Keloharju et al. (2016) argue it reflects seasonal variation in risk premia. |
| Publication | Heston & Sadka 2008; Keloharju, Linnainmaa & Nyberg 2016 |
| Where it fits | In the **momentum** cluster of the library; fully explained by its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Momentum 12-1**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Same-month seasonality **(this strategy)** | seasonality | +1.00 | +1.00 | -1.8% | -8.5% to +7.2% | 0 / 0 |
| Last month return | short-term reversal | +0.02 | +0.12 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Momentum 12-1 (mirror) | momentum | +0.12 | +0.11 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| 55-day breakout | momentum | +0.01 | +0.11 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.00 | +0.08 | -1.0% | -5.3% to +4.2% | 0 / 0 |
| Near 52-week high | momentum | +0.01 | +0.08 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| MIN5 | low risk | -0.04 | +0.06 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| MIN (worst day) | low risk | -0.04 | +0.05 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| Idiosyncratic vol | low risk | +0.03 | -0.05 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| Residual momentum | momentum | +0.01 | -0.04 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| Beta | low risk | +0.11 | -0.04 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| Volatility | low risk | +0.06 | -0.04 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Range (MAX−MIN) | low risk | +0.05 | -0.04 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| Volatility (252 days) | low risk | +0.09 | -0.03 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| Size | size | +0.07 | +0.02 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Above 52-week low | momentum | +0.07 | +0.02 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Skewness | tail direction | +0.00 | +0.02 | -0.2% | -5.4% to +4.5% | 0 / 1 |
| MAX5 | low risk | +0.06 | -0.02 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| MAX (best day) | low risk | +0.05 | -0.01 | +1.9% | -9.3% to +1.0% | 0 / 2 |

![360 map](../figures/xs_FS06_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with |t| ≥ 2 |
|---|---|---|---|---|
| US | -5.7% | -1.90 | 0.06 |  |
| EU | -7.2% | -1.89 | 0.12 | Size +0.24 (+3.1) |
| UK | +3.1% | 0.68 | 0.14 | Momentum 12-1 +0.13 (+2.2), Size -0.22 (-2.4) |
| DK | -7.7% | -1.89 | 0.02 |  |
| SCANDI | +1.6% | 0.40 | 0.09 | Size -0.24 (-2.4), Residual momentum -0.16 (-2.5) |
| World | +0.3% | 0.12 | 0.07 |  |

![Double sort](../figures/xs_FS06_dsort.png)

Holding Momentum 12-1 fixed (down a column), moving from low to high Same-month seasonality changes the return by -0.7, -1.0 and -0.8 points a year; holding Same-month seasonality fixed (along a row), moving from low to high Momentum 12-1 changes it by +4.9, +3.0 and +4.8.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -1% vs -2% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages -1.8%, -1.8%, +1.1%, -0.4% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Data gap.** Price history starts in 2011–2012, so the signal averages 1 prior year in 2013 and at most 13 by 2026; Heston & Sadka use up to 20. The early years test a much noisier signal than the paper's.
5. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- Heston, S. & Sadka, R. (2008). Seasonality in the cross-section of stock returns. *Journal of Financial Economics*, 87(2), 418–445.
- Keloharju, M., Linnainmaa, J. & Nyberg, P. (2016). Return seasonalities. *Journal of Finance*, 71(4), 1557–1590.
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

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS06` → `build_xs.py FS06`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
