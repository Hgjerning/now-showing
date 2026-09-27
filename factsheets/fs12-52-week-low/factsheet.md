# FACTSHEET FS12 · Buy at the 52-week low

### Should you buy stocks at their yearly low?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Contrarian / bottom-fishing</div>
<div><b>Origin</b>Market folklore (bottom-fishing); tested against George & Hwang (2004)</div>
<div><b>Family</b>Reversal & bottom-fishing</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (stocks closest to their 52-week low)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Folklore says stocks at their yearly low are bargains: 'buy low'. The academic evidence points the other way: stocks near their lows tend to keep underperforming (George & Hwang 2004), and in the series A10 Free Fallin' found knives rebound only in market-wide crashes. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -17.0% to -5.2% a year and was positive in none of the six; no universe passes the 2.87 gate (significantly negative in US, EU, World). The long-only book (stocks closest to their 52-week low) had a higher Sharpe than the equal-weight universe in none of the six, with alphas of -9.7% to -2.3%, none past the gate. **What goes wrong (§10):** no single dominant drag. None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Reversal & bottom-fishing; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours Momentum 12-1, Residual momentum; after those neighbours and the market, nothing is left (alpha |t| < 2 everywhere): the signal is redundant.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 501 / 10 | -17.0% | -3.40 | -15.8% (-3.4) | -0.08 | +8.1% | 0.52 | -33% | +14.1% | 0.95 | +15.3% |
| EU | 238 / 10 | -15.1% | -3.37 | -16.6% (-3.7) | 0.13 | +1.4% | 0.16 | -34% | +10.9% | 0.78 | +10.1% |
| UK | 239 / 10 | -11.0% | -2.70 | -14.0% (-3.6) | 0.29 | +8.6% | 0.53 | -32% | +9.9% | 0.74 | +8.5% |
| DK | 19 / 3 | -7.3% | -1.76 | -8.5% (-1.9) | 0.10 | +10.1% | 0.60 | -32% | +12.3% | 0.82 | +10.3% |
| SCANDI | 62 / 5 | -5.2% | -1.49 | -6.4% (-1.8) | 0.09 | +8.6% | 0.58 | -27% | +12.5% | 0.91 | +10.7% |
| World | 971 / 10 | -13.5% | -3.58 | -15.0% (-4.4) | 0.13 | +6.4% | 0.42 | -33% | +11.9% | 0.80 | +10.8% |

*Monthly, local currency (World in USD). L/S = equal-weighted stocks closest to their 52-week low minus stocks furthest above it, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS12_growth.png)

## 2. Strategy description

Folklore says stocks at their yearly low are bargains: 'buy low'. The academic evidence points the other way: stocks near their lows tend to keep underperforming (George & Hwang 2004), and in the series A10 Free Fallin' found knives rebound only in market-wide crashes.

**Why it might work.** Folklore: mean reversion and value. Evidence: momentum and anchoring (George & Hwang 2004) predict continued weakness; losers carry high beta and volatility.

| Rule | Original (Market folklore (bottom-fishing); tested against George & Hwang (2004)) | This factsheet |
|---|---|---|
| Signal | Folklore: buy at or near the 52-week low | Total-return price / 252-day low; lowest = at the low |
| Portfolio | No standard rule | Extreme quantile L/S (at the low minus far above), one month |
| Weighting | — | Equal weighted |

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


## 4. Signal creation

LO52<sub>i,t</sub> = P<sub>i,t</sub> / min(P<sub>i,t−251..t</sub>); the long leg holds the stocks with the lowest value (at the low). Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = stocks closest to their 52-week low minus stocks furthest above it; **long-only** = stocks closest to their 52-week low; benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (top 500, point-in-time)**, median 501 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -17.0% | -17.4% | 19.5% | -0.87 [-1.35, -0.39] | -1.06 | -94% | 36% | -3.40 | -0.08 | -15.8% (-3.4) | 14.1% |
| Long-only (net) | +9.5% | +8.1% | 18.3% | 0.52 [0.15, 0.98] | 0.69 | -33% | 60% | 2.86 | 1.08 | -6.1% (-2.8) | 10.7% |
| Stocks closest to their 52-week low (gross) | +10.6% | +9.3% | 18.3% | 0.58 [0.21, 1.05] | 0.80 | -32% | 61% | 3.21 | 1.08 | -5.0% (-2.3) | 10.6% |
| Stocks furthest above it (gross) | +25.2% | +25.4% | 21.8% | 1.15 [0.70, 1.62] | 2.23 | -20% | 65% | 4.90 | 1.16 | +8.4% (2.7) | 10.9% |
| EW universe | +14.4% | +14.1% | 15.1% | 0.95 [0.52, 1.53] | 1.52 | -25% | 68% | 4.79 | 1.00 | – | 8.9% |
| Size-weighted universe | +15.4% | +15.3% | 14.4% | 1.07 [0.61, 1.64] | 1.79 | -24% | 69% | 5.27 | 0.90 | +2.4% (1.8) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -15.1% | -15.2% | 15.7% | -0.96 [-1.61, -0.40] | -1.13 | -92% | 37% | -3.37 | 0.13 | -16.6% (-3.7) | 9.6% |
| Long-only (net) | +2.9% | +1.4% | 17.9% | 0.16 [-0.29, 0.64] | 0.11 | -34% | 52% | 0.69 | 1.11 | -9.7% (-4.8) | 10.3% |
| Stocks closest to their 52-week low (gross) | +4.1% | +2.5% | 17.9% | 0.23 [-0.22, 0.70] | 0.21 | -34% | 52% | 0.97 | 1.11 | -8.6% (-4.2) | 10.2% |
| Stocks furthest above it (gross) | +16.7% | +16.3% | 17.4% | 0.96 [0.42, 1.54] | 1.65 | -35% | 63% | 3.45 | 0.98 | +5.5% (1.8) | 8.7% |
| EW universe | +11.4% | +10.9% | 14.5% | 0.78 [0.33, 1.33] | 1.22 | -26% | 64% | 3.34 | 1.00 | – | 8.3% |
| Size-weighted universe | +10.7% | +10.1% | 14.3% | 0.75 [0.28, 1.28] | 1.14 | -26% | 60% | 3.12 | 0.95 | -0.2% (-0.1) | 8.3% |

**UK (FTSE 350, point-in-time)**, median 239 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -11.0% | -11.6% | 16.4% | -0.67 [-1.21, -0.19] | -0.93 | -84% | 38% | -2.70 | 0.29 | -14.0% (-3.6) | 9.8% |
| Long-only (net) | +10.0% | +8.6% | 18.9% | 0.53 [0.12, 0.97] | 0.78 | -32% | 56% | 2.35 | 1.18 | -2.3% (-1.1) | 9.7% |
| Stocks closest to their 52-week low (gross) | +11.1% | +9.8% | 18.9% | 0.59 [0.18, 1.03] | 0.92 | -32% | 57% | 2.64 | 1.18 | -1.2% (-0.6) | 9.6% |
| Stocks furthest above it (gross) | +19.7% | +20.1% | 16.0% | 1.23 [0.71, 1.85] | 2.19 | -25% | 64% | 4.97 | 0.88 | +10.4% (4.0) | 9.0% |
| EW universe | +10.5% | +9.9% | 14.1% | 0.74 [0.26, 1.34] | 1.08 | -29% | 60% | 3.23 | 1.00 | – | 8.8% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.71 [0.21, 1.31] | 1.01 | -27% | 62% | 2.94 | 0.82 | +0.4% (0.2) | 7.7% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -7.3% | -8.4% | 16.9% | -0.43 [-0.89, 0.06] | -0.62 | -71% | 46% | -1.76 | 0.10 | -8.5% (-1.9) | 11.9% |
| Long-only (net) | +11.5% | +10.1% | 19.1% | 0.60 [0.17, 1.10] | 0.82 | -32% | 60% | 2.68 | 1.08 | -2.4% (-1.1) | 11.6% |
| Stocks closest to their 52-week low (gross) | +12.0% | +10.7% | 19.1% | 0.63 [0.21, 1.13] | 0.88 | -31% | 60% | 2.82 | 1.08 | -1.8% (-0.9) | 11.5% |
| Stocks furthest above it (gross) | +17.6% | +17.2% | 18.3% | 0.96 [0.36, 1.63] | 1.70 | -35% | 63% | 3.27 | 0.98 | +5.0% (1.8) | 9.2% |
| EW universe | +12.8% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.25 | -33% | 64% | 3.20 | 1.00 | – | 9.3% |
| Size-weighted universe | +11.2% | +10.3% | 16.6% | 0.68 [0.11, 1.32] | 0.94 | -40% | 61% | 2.52 | 0.92 | -0.5% (-0.2) | 10.8% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -5.2% | -6.0% | 14.3% | -0.36 [-0.81, 0.10] | -0.55 | -63% | 44% | -1.49 | 0.09 | -6.4% (-1.8) | 9.5% |
| Long-only (net) | +9.7% | +8.6% | 16.9% | 0.58 [0.12, 1.09] | 0.81 | -27% | 58% | 2.56 | 1.06 | -3.9% (-2.0) | 9.6% |
| Stocks closest to their 52-week low (gross) | +10.5% | +9.4% | 16.9% | 0.62 [0.17, 1.14] | 0.90 | -26% | 58% | 2.77 | 1.06 | -3.1% (-1.6) | 9.6% |
| Stocks furthest above it (gross) | +13.5% | +12.9% | 16.2% | 0.83 [0.28, 1.42] | 1.37 | -34% | 58% | 3.16 | 0.96 | +1.1% (0.5) | 8.3% |
| EW universe | +12.8% | +12.5% | 14.1% | 0.91 [0.39, 1.54] | 1.42 | -29% | 67% | 3.62 | 1.00 | – | 8.3% |
| Size-weighted universe | +11.2% | +10.7% | 13.9% | 0.80 [0.31, 1.37] | 1.21 | -27% | 63% | 3.26 | 0.95 | -1.0% (-0.9) | 8.6% |

**World (US + UK + EU, point-in-time)**, median 971 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -13.5% | -13.6% | 14.7% | -0.91 [-1.46, -0.42] | -1.12 | -88% | 39% | -3.58 | 0.13 | -15.0% (-4.4) | 9.5% |
| Long-only (net) | +8.1% | +6.4% | 19.3% | 0.42 [0.00, 0.87] | 0.53 | -33% | 58% | 1.93 | 1.14 | -6.3% (-3.8) | 10.8% |
| Stocks closest to their 52-week low (gross) | +9.2% | +7.6% | 19.3% | 0.48 [0.07, 0.93] | 0.64 | -33% | 58% | 2.22 | 1.14 | -5.1% (-3.1) | 10.7% |
| Stocks furthest above it (gross) | +20.2% | +20.2% | 18.3% | 1.10 [0.61, 1.67] | 1.96 | -27% | 64% | 4.45 | 1.02 | +7.5% (3.4) | 10.1% |
| EW universe | +12.5% | +11.9% | 15.7% | 0.80 [0.33, 1.38] | 1.20 | -29% | 64% | 3.53 | 1.00 | – | 9.4% |
| Size-weighted universe | +11.4% | +10.8% | 15.0% | 0.76 [0.29, 1.33] | 1.14 | -28% | 63% | 3.23 | 0.94 | -0.4% (-0.5) | 9.0% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -15.6% | -18.3% | -25.4% | -35.5% | -20.3% | -14.0% |
| 2014 | -4.9% | -6.0% | -20.2% | -23.7% | -10.8% | -13.1% |
| 2015 | -12.0% | -17.4% | -8.8% | -20.0% | -0.1% | -5.7% |
| 2016 | +1.6% | -23.4% | -20.9% | +6.3% | -16.7% | -8.4% |
| 2017 | -10.9% | -10.8% | -23.6% | -3.5% | -4.2% | -13.9% |
| 2018 | -18.2% | -9.8% | -8.6% | -5.5% | -15.1% | -13.2% |
| 2019 | +10.4% | +6.9% | -9.5% | +16.4% | +24.8% | +8.6% |
| 2020 | -39.0% | -26.1% | +2.6% | -31.7% | -16.8% | -17.8% |
| 2021 | -3.6% | +1.9% | +0.2% | -0.1% | +14.5% | -3.4% |
| 2022 | +0.7% | +5.2% | -10.2% | +17.7% | -0.1% | -3.6% |
| 2023 | -10.4% | -14.4% | -0.0% | +6.4% | +3.3% | -10.7% |
| 2024 | -36.9% | -17.0% | +1.0% | +11.0% | +1.8% | -24.0% |
| 2025 | -36.1% | -47.4% | -24.4% | -18.3% | -23.7% | -36.1% |
| 2026 | -39.2% | -13.5% | -2.3% | -11.3% | -6.5% | -21.0% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +20.5% | +15.8% | +9.8% | +19.1% | +18.0% | +20.6% |
| 2014 | +19.8% | -3.2% | -7.9% | +1.5% | +5.2% | +0.0% |
| 2015 | -7.5% | -0.6% | +15.8% | +16.4% | +18.4% | -2.4% |
| 2016 | +13.7% | +9.2% | +24.9% | +10.0% | +15.0% | +7.3% |
| 2017 | +9.5% | +6.3% | +15.0% | +17.9% | +17.7% | +16.3% |
| 2018 | -14.4% | -15.6% | -5.8% | -17.4% | -17.8% | -12.8% |
| 2019 | +40.2% | +32.6% | +22.1% | +35.0% | +42.3% | +35.9% |
| 2020 | +3.8% | -11.5% | +11.3% | +18.8% | +6.1% | +11.4% |
| 2021 | +22.8% | +17.4% | +17.3% | +22.0% | +23.1% | +14.3% |
| 2022 | -5.2% | -13.3% | -16.5% | -11.1% | -18.5% | -16.9% |
| 2023 | +15.6% | -0.8% | +9.8% | +16.4% | +4.8% | +13.6% |
| 2024 | +5.6% | -6.9% | +10.2% | +8.4% | +4.5% | +0.5% |
| 2025 | -4.2% | -4.4% | +1.6% | +2.7% | +1.2% | +2.6% |
| 2026 | +2.5% | +4.5% | +17.5% | +8.5% | +12.0% | +8.1% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS12_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 45% | 24% | 36% | -23.8% | 2026-04 |
| EU | 163 | 24 / 23 | 47% | 25% | 37% | -12.2% | 2022-03 |
| UK | 163 | 24 / 23 | 49% | 22% | 38% | -11.7% | 2016-04 |
| DK | 163 | 7 / 6 | 24% | 21% | 46% | -18.5% | 2020-03 |
| SCANDI | 163 | 13 / 12 | 32% | 25% | 44% | -14.7% | 2026-01 |
| World | 163 | 98 / 97 | 47% | 25% | 39% | -12.9% | 2026-04 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks closest to their 52-week low | Short: stocks furthest above it |
|---|---|---|
| US | WYNN, APTV, TJX, PNR, PCG, MLM, NRG, LII | SNDK, MU, LITE, MRNA, WDC, STX, DELL, CIEN |
| EU | AD.AS, BPOST.BR, EL.PA, VNA.DE, UMG.AS, BAR.BR, ELISA.HE, KER.WA | KGH.WA, ASML.AS, MT.AS, MTS.MC, TYRES.HE, STMPA.PA, NOKIA.HE, STMMI.MI |
| UK | AML.L, SN.L, BAG.L, ENT.L, RTO.L, IMB.L, PRN.L, SAFE.L | CWR.L, CMCX.L, SAGA.L, SSIT.L, HAS.L, CCC.L, KLR.L, TRST.L |
| DK | TRYG.CO, DSV.CO, RBREW.CO, GN.CO, AMBU-B.CO, COLO-B.CO, CARL-B.CO, BAVA.CO | PNDORA.CO, VWS.CO, MAERSK-B.CO, MAERSK-A.CO, JYSK.CO, DEMANT.CO, ISS.CO, DANSKE.CO |
| SCANDI | ELISA.HE, AZN.ST, TRYG.CO, KEMIRA.HE, DSV.CO, RBREW.CO, KNEBV.HE, GN.CO | TYRES.HE, NOKIA.HE, NESTE.HE, MAERSK-B.CO, QTCOM.HE, MAERSK-A.CO, VWS.CO, ZEAL.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -9.6% | -3.52 | 0.72 | momentum -1.53 (-11.0), low_risk +1.00 (+6.6), short_term_reversal +0.65 (+2.5) |
| EU | French Europe 5F + WML | -5.0% | -1.25 | 0.36 | RMW +0.68 (+2.1), CMA +0.71 (+2.6), WML -1.01 (-7.3) |
| UK | JKP GBR 7 themes | -6.9% | -2.30 | 0.54 | mkt +0.19 (+3.5), momentum -1.20 (-8.5), low_risk +0.70 (+3.0), short_term_reversal +0.75 (+4.8) |
| DK | JKP DNK 7 themes | +1.7% | 0.51 | 0.46 | momentum -1.06 (-8.0), low_risk +0.67 (+5.3) |
| SCANDI | French Europe 5F + WML | +1.2% | 0.31 | 0.16 | WML -0.61 (-3.7) |
| World | JKP World 7 themes | -11.3% | -3.47 | 0.43 | mkt +0.19 (+3.2), momentum -0.96 (-7.8), low_risk +0.68 (+3.7) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +1.2% | 0.66 | 0.91 | mkt +0.95 (+21.0), size -0.25 (-3.1), value +0.22 (+2.8), momentum -0.56 (-8.4), short_term_reversal +0.44 (+3.4) |
| EU | French Europe 5F + WML | +2.3% | 0.81 | 0.78 | Mkt-RF +0.76 (+9.7), WML -0.62 (-7.3) |
| UK | JKP GBR 7 themes | +6.6% | 2.38 | 0.77 | mkt +0.64 (+13.7), momentum -0.55 (-3.3), short_term_reversal +0.64 (+3.8) |
| DK | JKP DNK 7 themes | +7.2% | 2.40 | 0.68 | mkt +0.78 (+10.2), momentum -0.57 (-5.6) |
| SCANDI | French Europe 5F + WML | +9.0% | 2.78 | 0.59 | Mkt-RF +0.66 (+7.1), RMW +0.52 (+2.1), WML -0.46 (-3.8) |
| World | JKP World 7 themes | +2.1% | 0.76 | 0.81 | mkt +0.82 (+15.7), momentum -0.42 (-5.0) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in none of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -16.6% to -6.4%, |t| past the gate in 4 of 6.
- **Long-only:** Sharpe above the equal-weight universe in none of the six; alpha -9.7% to -2.3%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.00, EU 0.00, UK 0.01, DK 0.05, SCANDI 0.09, World 0.00.
- **Publication decay:** gross L/S -14.9% to -4.1% a year in 2013–19 against -24.9% to -1.9% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | -4.7% | 0.12 | +1.7% | -6.4% | -1.6% | -1.8% | -2.8% | 68% | 2018-08 -8%, 2017-10 -8%, 2018-01 -8% |
| EU | -8.9% | -0.01 | -0.1% | -8.8% | -1.7% | -4.1% | -4.8% | 72% | 2013-04 -9%, 2016-07 -9%, 2016-09 -8% |
| UK | -14.9% | 0.28 | +3.7% | -18.6% | -1.7% | -1.5% | -13.4% | 70% | 2016-04 -12%, 2014-12 -11%, 2016-06 -10% |
| DK | -8.9% | -0.18 | -2.7% | -6.2% | -1.0% | -3.4% | -5.5% | 40% | 2013-05 -18%, 2018-06 -11%, 2013-09 -10% |
| SCANDI | -4.1% | -0.03 | -0.5% | -3.6% | -1.3% | -1.5% | -2.7% | 54% | 2013-09 -11%, 2016-11 -10%, 2013-05 -7% |
| World | -6.2% | 0.19 | +2.4% | -8.5% | -1.7% | -2.1% | -4.1% | 72% | 2018-08 -8%, 2017-10 -6%, 2017-08 -6% |

On average across the six universes the gross spread was -7.9% a year, of which the market exposure (beta +0.06) contributed +0.7%; the beta-adjusted spread (CAPM alpha) was -8.7%. Costs took 1.5% a year at 63% monthly turnover across both legs. The long leg beat the universe by -2.4% and the short leg lagged it by -5.5% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +10.8%, +11.0%, +10.1% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.70 | – | -0.96 | – | – | -12.8% | -64% | -14.9% (-2.6) | 1.5% |
| X1 beta-neutral legs | -0.53 | +0.22 (p 0.046) | -0.58 | +0.37 (p 0.053) | 6 of 6 | -8.0% | -55% | -11.4% (-2.1) | 1.7% |
| X2 + turnover buffer | -0.60 | -0.09 (p 0.879) | -0.63 | -0.05 (p 0.632) | 4 of 6 | -6.9% | -46% | -9.7% (-2.1) | 0.8% |
| X3 + volatility targeting | -0.55 | +0.11 (p 0.406) | -0.78 | -0.15 (p 0.931) | 4 of 6 | -8.1% | -48% | -10.8% (-2.5) | 0.8% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS12_ladder.png)

- **X1 beta-neutral legs:** +0.22 design, +0.37 holdout; helps in both windows but does not pass the gate.
- **X2 + turnover buffer:** -0.09 design, -0.05 holdout; hurts in both windows.
- **X3 + volatility targeting:** +0.11 design, -0.15 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe -0.96 → -0.78, return -12.8% → -8.1% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Buy at the 52-week low |
|---|---|
| Series family | **Reversal & bottom-fishing** |
| Academic style | Contrarian / bottom-fishing |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 63% of the two legs replaced monthly |
| Market exposure | L/S beta -0.08 to 0.29 |
| Payoff shape | Treynor–Mazuy γ -2.07 to 2.99 (t -1.3 to 2.0); worst 10% of market months -2.0% to +0.2% a month, best 10% -1.6% to +1.4% |
| Nearest factor theme | momentum (4 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | Momentum 12-1 (6 universes), Last month return (5 universes), Residual momentum (3 universes) |
| Economic rationale | Folklore: mean reversion and value. Evidence: momentum and anchoring (George & Hwang 2004) predict continued weakness; losers carry high beta and volatility. |
| Publication | No academic origin; George & Hwang 2004 as the counter-claim; series A10 (Free Fallin') |
| Where it fits | In the **momentum** cluster of the library; fully explained by its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Near 52-week high**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Above 52-week low **(this strategy)** | momentum | +1.00 | +1.00 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Momentum 12-1 | momentum | +0.64 | +0.65 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Near 52-week high (mirror) | momentum | +0.50 | +0.46 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| Last month return | short-term reversal | +0.39 | +0.46 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Residual momentum | momentum | +0.41 | +0.46 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| 55-day breakout | momentum | +0.36 | +0.40 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.25 | +0.30 | -1.0% | -5.3% to +4.2% | 0 / 0 |
| MAX5 | low risk | +0.29 | +0.21 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| MAX (best day) | low risk | +0.23 | +0.17 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| Size | size | +0.05 | +0.14 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Idiosyncratic vol | low risk | +0.10 | +0.12 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| Skewness | tail direction | +0.14 | +0.11 | -0.2% | -5.4% to +4.5% | 0 / 1 |
| MIN5 | low risk | +0.07 | +0.11 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| Volatility (252 days) | low risk | +0.24 | +0.08 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| MIN (worst day) | low risk | +0.05 | +0.08 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| Beta | low risk | +0.19 | +0.04 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| Volatility | low risk | +0.16 | +0.04 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Range (MAX−MIN) | low risk | +0.10 | +0.03 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| Same-month seasonality | seasonality | +0.07 | +0.02 | -1.8% | -8.5% to +7.2% | 0 / 0 |

![360 map](../figures/xs_FS12_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with |t| ≥ 2 |
|---|---|---|---|---|
| US | +3.0% | 1.51 | 0.83 | Momentum 12-1 +0.63 (+18.2), Last month return +0.21 (+3.7) |
| EU | +4.5% | 1.51 | 0.61 | Momentum 12-1 +0.62 (+4.8), Last month return +0.42 (+5.3), 55-day breakout +0.26 (+2.1), Near 52-week high -0.54 (-3.5) |
| UK | +1.2% | 0.36 | 0.56 | Momentum 12-1 +0.44 (+3.1), Residual momentum +0.53 (+2.7), Last month return +0.44 (+4.6) |
| DK | -3.9% | -1.63 | 0.53 | Momentum 12-1 +0.53 (+6.5), Last month return +0.24 (+2.5) |
| SCANDI | +1.4% | 0.54 | 0.49 | Momentum 12-1 +0.39 (+3.5), Last month return +0.36 (+4.5) |
| World | -0.5% | -0.21 | 0.73 | Momentum 12-1 +0.85 (+8.5), Last month return +0.47 (+7.5), Near 52-week high -0.61 (-4.9) |

![Double sort](../figures/xs_FS12_dsort.png)

Holding Near 52-week high fixed (down a column), moving from low to high Above 52-week low changes the return by +3.5, +6.9 and +3.6 points a year; holding Above 52-week low fixed (along a row), moving from low to high Near 52-week high changes it by +0.6, -0.5 and +0.6.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): +7% vs +11% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +8.8%, +10.8%, +11.0%, +10.1% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- George, T. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance*, 59(5), 2145–2176.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1), 65–91.
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

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS12` → `build_xs.py FS12`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
