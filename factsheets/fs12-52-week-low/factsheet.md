# FACTSHEET FS12 · Buy at the 52-week low

### Should you buy stocks at their yearly low?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

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

> **The claim.** Folklore says stocks at their yearly low are bargains: 'buy low'. The academic evidence points the other way: stocks near their lows tend to keep underperforming (George & Hwang 2004), and in the series A10 Free Fallin' found knives rebound only in market-wide crashes. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -14.7% to -5.8% a year and was positive in none of the six; no universe passes the 2.87 gate (significantly negative in US, EU, World). The long-only book (stocks closest to their 52-week low) had a higher Sharpe than the equal-weight universe in none of the six, with alphas of -9.7% to -2.5%, none past the gate. **What goes wrong (§10):** no single dominant drag. None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Reversal & bottom-fishing; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours Momentum 12-1, Residual momentum; after those neighbours and the market, nothing is left (alpha |t| < 2 everywhere): the signal is redundant.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 502 / 10 | -10.8% | -3.07 | -12.4% (-3.9) | 0.13 | +7.5% | 0.47 | -34% | +12.6% | 0.85 | +14.9% |
| EU | 264 / 10 | -14.7% | -3.47 | -15.8% (-3.7) | 0.10 | +0.3% | 0.11 | -34% | +10.1% | 0.75 | +10.2% |
| UK | 327 / 10 | -10.4% | -2.64 | -13.2% (-3.5) | 0.30 | +6.8% | 0.44 | -35% | +8.9% | 0.68 | +7.8% |
| DK | 20 / 3 | -7.9% | -1.96 | -9.0% (-2.2) | 0.09 | +9.7% | 0.60 | -31% | +12.0% | 0.83 | +10.2% |
| SCANDI | 70 / 5 | -5.8% | -1.62 | -7.3% (-2.0) | 0.12 | +7.5% | 0.51 | -29% | +12.2% | 0.89 | +11.0% |
| World | 1089 / 10 | -11.0% | -3.27 | -13.0% (-4.2) | 0.18 | +4.7% | 0.33 | -36% | +10.5% | 0.71 | +10.3% |

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
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: the S&P 500 members at each month-end (Sharadar add/remove history; corrected 2 Oct 2026) | ~503 | USD |
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

**US (S&P 500 members, point-in-time)**, median 502 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -10.8% | -11.6% | 17.3% | -0.62 [-1.03, -0.21] | -0.84 | -84% | 42% | -3.07 | 0.13 | -12.4% (-3.9) | 11.8% |
| Long-only (net) | +9.2% | +7.5% | 19.4% | 0.47 [0.10, 0.92] | 0.61 | -34% | 60% | 2.54 | 1.14 | -5.7% (-2.9) | 11.3% |
| Stocks closest to their 52-week low (gross) | +10.3% | +8.7% | 19.5% | 0.53 [0.16, 0.98] | 0.71 | -33% | 60% | 2.87 | 1.14 | -4.6% (-2.4) | 11.1% |
| Stocks furthest above it (gross) | +18.6% | +18.2% | 19.2% | 0.97 [0.56, 1.41] | 1.72 | -23% | 61% | 4.85 | 1.01 | +5.4% (2.6) | 10.1% |
| EW universe | +13.1% | +12.6% | 15.5% | 0.85 [0.41, 1.42] | 1.29 | -28% | 67% | 4.20 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.9% | +14.9% | 14.2% | 1.05 [0.60, 1.61] | 1.73 | -24% | 69% | 5.29 | 0.86 | +3.7% (2.4) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 264 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -14.7% | -14.8% | 15.3% | -0.96 [-1.59, -0.42] | -1.13 | -91% | 38% | -3.47 | 0.10 | -15.8% (-3.7) | 9.4% |
| Long-only (net) | +1.8% | +0.3% | 17.3% | 0.11 [-0.32, 0.56] | 0.03 | -34% | 53% | 0.47 | 1.08 | -9.7% (-5.0) | 10.3% |
| Stocks closest to their 52-week low (gross) | +3.0% | +1.5% | 17.2% | 0.17 [-0.26, 0.63] | 0.13 | -34% | 53% | 0.76 | 1.07 | -8.6% (-4.4) | 10.2% |
| Stocks furthest above it (gross) | +15.2% | +14.7% | 17.1% | 0.89 [0.37, 1.47] | 1.48 | -32% | 63% | 3.28 | 0.98 | +4.7% (1.6) | 8.6% |
| EW universe | +10.7% | +10.1% | 14.3% | 0.75 [0.29, 1.30] | 1.14 | -26% | 62% | 3.18 | 1.00 | – | 8.4% |
| Size-weighted universe | +10.6% | +10.2% | 13.7% | 0.77 [0.32, 1.29] | 1.21 | -25% | 58% | 3.37 | 0.92 | +0.8% (0.6) | 7.9% |

**UK (FTSE 350, point-in-time)**, median 327 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -10.4% | -11.1% | 16.2% | -0.64 [-1.16, -0.16] | -0.91 | -83% | 38% | -2.64 | 0.30 | -13.2% (-3.5) | 9.6% |
| Long-only (net) | +8.3% | +6.8% | 18.9% | 0.44 [0.01, 0.92] | 0.59 | -35% | 53% | 1.87 | 1.18 | -3.0% (-1.4) | 10.7% |
| Stocks closest to their 52-week low (gross) | +9.5% | +8.1% | 18.9% | 0.50 [0.07, 0.98] | 0.71 | -34% | 53% | 2.15 | 1.18 | -1.8% (-0.8) | 10.6% |
| Stocks furthest above it (gross) | +17.5% | +17.5% | 16.1% | 1.09 [0.57, 1.69] | 1.86 | -23% | 64% | 4.21 | 0.88 | +9.0% (3.3) | 9.0% |
| EW universe | +9.6% | +8.9% | 14.2% | 0.68 [0.20, 1.28] | 0.96 | -30% | 58% | 2.87 | 1.00 | – | 8.8% |
| Size-weighted universe | +8.4% | +7.8% | 12.9% | 0.65 [0.16, 1.25] | 0.90 | -28% | 62% | 2.68 | 0.84 | +0.3% (0.2) | 7.8% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -7.9% | -8.7% | 15.5% | -0.51 [-1.02, 0.02] | -0.71 | -75% | 46% | -1.96 | 0.09 | -9.0% (-2.2) | 10.0% |
| Long-only (net) | +10.9% | +9.7% | 18.2% | 0.60 [0.16, 1.08] | 0.84 | -31% | 61% | 2.70 | 1.07 | -2.5% (-1.2) | 10.7% |
| Stocks closest to their 52-week low (gross) | +11.5% | +10.2% | 18.2% | 0.63 [0.19, 1.11] | 0.89 | -30% | 61% | 2.83 | 1.07 | -2.0% (-1.0) | 10.7% |
| Stocks furthest above it (gross) | +17.7% | +17.5% | 17.5% | 1.01 [0.41, 1.67] | 1.82 | -35% | 65% | 3.49 | 0.98 | +5.4% (2.2) | 9.0% |
| EW universe | +12.6% | +12.0% | 15.2% | 0.83 [0.31, 1.44] | 1.27 | -33% | 66% | 3.31 | 1.00 | – | 8.8% |
| Size-weighted universe | +11.1% | +10.2% | 16.4% | 0.68 [0.11, 1.33] | 0.94 | -40% | 62% | 2.55 | 0.93 | -0.6% (-0.2) | 10.7% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -5.8% | -6.6% | 14.1% | -0.41 [-0.88, 0.08] | -0.60 | -64% | 42% | -1.62 | 0.12 | -7.3% (-2.0) | 9.4% |
| Long-only (net) | +8.7% | +7.5% | 17.0% | 0.51 [0.07, 1.00] | 0.69 | -29% | 57% | 2.34 | 1.07 | -4.9% (-2.4) | 9.8% |
| Stocks closest to their 52-week low (gross) | +9.4% | +8.3% | 17.0% | 0.55 [0.11, 1.05] | 0.77 | -28% | 57% | 2.55 | 1.07 | -4.1% (-2.0) | 9.8% |
| Stocks furthest above it (gross) | +13.1% | +12.5% | 15.9% | 0.82 [0.25, 1.43] | 1.32 | -33% | 60% | 3.06 | 0.95 | +1.1% (0.5) | 8.5% |
| EW universe | +12.6% | +12.2% | 14.2% | 0.89 [0.37, 1.52] | 1.38 | -29% | 66% | 3.63 | 1.00 | – | 8.4% |
| Size-weighted universe | +11.4% | +11.0% | 13.5% | 0.84 [0.37, 1.41] | 1.32 | -26% | 63% | 3.59 | 0.90 | -0.0% (-0.0) | 8.1% |

**World (US + UK + EU, point-in-time)**, median 1089 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -11.0% | -11.3% | 14.2% | -0.78 [-1.32, -0.30] | -1.02 | -84% | 39% | -3.27 | 0.18 | -13.0% (-4.2) | 8.5% |
| Long-only (net) | +6.5% | +4.7% | 19.7% | 0.33 [-0.09, 0.78] | 0.37 | -36% | 57% | 1.50 | 1.15 | -6.5% (-4.2) | 11.2% |
| Stocks closest to their 52-week low (gross) | +7.7% | +5.9% | 19.7% | 0.39 [-0.03, 0.84] | 0.47 | -35% | 58% | 1.78 | 1.15 | -5.3% (-3.4) | 11.0% |
| Stocks furthest above it (gross) | +16.1% | +15.6% | 17.6% | 0.92 [0.43, 1.49] | 1.51 | -27% | 58% | 3.76 | 0.97 | +5.2% (2.7) | 9.9% |
| EW universe | +11.3% | +10.5% | 16.0% | 0.71 [0.25, 1.28] | 1.02 | -30% | 63% | 3.07 | 1.00 | – | 9.7% |
| Size-weighted universe | +11.0% | +10.3% | 14.8% | 0.74 [0.28, 1.31] | 1.10 | -28% | 61% | 3.19 | 0.91 | +0.7% (0.8) | 8.9% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -16.8% | -15.6% | -25.7% | -28.2% | -21.9% | -16.2% |
| 2014 | -2.1% | -9.1% | -11.1% | -17.8% | -9.1% | -9.5% |
| 2015 | -16.4% | -17.9% | -3.5% | -27.4% | +3.0% | -5.9% |
| 2016 | -2.8% | -20.3% | -21.9% | +1.3% | -17.0% | -14.8% |
| 2017 | -8.2% | -10.5% | -29.8% | -2.0% | -3.2% | -17.6% |
| 2018 | -15.1% | -7.6% | -1.6% | -14.4% | -17.0% | -9.8% |
| 2019 | +18.3% | +2.5% | -7.6% | +8.2% | +26.8% | +9.0% |
| 2020 | -12.0% | -26.5% | -4.1% | -25.3% | -15.0% | -5.3% |
| 2021 | -8.4% | +2.5% | +5.1% | -13.1% | +4.5% | -0.7% |
| 2022 | -1.1% | +4.4% | -15.1% | +23.7% | +0.6% | -7.1% |
| 2023 | -9.6% | -12.3% | +0.1% | +12.7% | +4.6% | -11.5% |
| 2024 | -18.7% | -15.7% | -3.0% | +12.2% | +0.8% | -11.6% |
| 2025 | -26.4% | -46.9% | -21.4% | -18.5% | -22.5% | -30.9% |
| 2026 | -29.0% | -13.6% | -2.1% | -11.4% | -12.1% | -16.0% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +20.5% | +11.7% | -0.7% | +24.3% | +11.4% | +14.9% |
| 2014 | +14.6% | -8.7% | -2.8% | +4.8% | +5.8% | -4.3% |
| 2015 | -10.1% | -5.4% | +19.1% | +14.4% | +23.4% | -4.5% |
| 2016 | +18.6% | +10.8% | +20.2% | +5.6% | +14.2% | +4.2% |
| 2017 | +8.8% | +5.7% | +15.2% | +19.7% | +16.0% | +16.2% |
| 2018 | -17.1% | -14.5% | -8.2% | -20.1% | -20.4% | -14.7% |
| 2019 | +38.2% | +29.6% | +20.2% | +29.3% | +42.9% | +31.6% |
| 2020 | +11.2% | -13.2% | +8.2% | +18.5% | +6.0% | +8.0% |
| 2021 | +22.2% | +16.8% | +17.1% | +8.9% | +14.4% | +16.3% |
| 2022 | -3.6% | -11.4% | -22.9% | -5.4% | -18.5% | -18.2% |
| 2023 | +5.7% | -0.1% | +6.8% | +23.9% | +7.2% | +8.3% |
| 2024 | +4.0% | -6.7% | +8.8% | +8.4% | +5.2% | +1.3% |
| 2025 | -3.1% | -4.1% | +3.8% | +1.0% | +1.2% | +5.3% |
| 2026 | +4.6% | +4.4% | +17.6% | +8.5% | +7.7% | +9.6% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS12_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 47% | 25% | 42% | -21.1% | 2026-04 |
| EU | 163 | 27 / 26 | 47% | 25% | 38% | -12.0% | 2022-03 |
| UK | 163 | 33 / 32 | 50% | 23% | 38% | -15.3% | 2016-04 |
| DK | 163 | 7 / 6 | 22% | 20% | 46% | -14.1% | 2013-05 |
| SCANDI | 163 | 14 / 14 | 31% | 24% | 42% | -14.7% | 2026-01 |
| World | 163 | 109 / 108 | 49% | 25% | 39% | -11.9% | 2026-04 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks closest to their 52-week low | Short: stocks furthest above it |
|---|---|---|
| US | VICI, APTV, LII, MLM, LVS, PCG, PNR, NRG | SNDK, MU, LITE, MRNA, WDC, STX, DELL, CIEN |
| EU | AD.AS, BPOST.BR, EL.PA, VNA.DE, UMG.AS, BAR.BR, ELISA.HE, KER.WA | KGH.WA, ASML.AS, MT.AS, MTS.MC, TYRES.HE, STMPA.PA, NOKIA.HE, STMMI.MI |
| UK | AML.L, SN.L, BAG.L, ENT.L, RTO.L, IMB.L, PRN.L, SAFE.L | CWR.L, CMCX.L, SAGA.L, SSIT.L, HAS.L, CCC.L, KLR.L, TRST.L |
| DK | TRYG.CO, DSV.CO, RBREW.CO, GN.CO, AMBU-B.CO, COLO-B.CO, CARL-B.CO, BAVA.CO | PNDORA.CO, VWS.CO, MAERSK-B.CO, MAERSK-A.CO, JYSK.CO, DEMANT.CO, ISS.CO, DANSKE.CO |
| SCANDI | ELISA.HE, AZN.ST, TRYG.CO, KEMIRA.HE, GN.CO, RBREW.CO, KNEBV.HE, KALMAR.HE | TYRES.HE, NOKIA.HE, NESTE.HE, MAERSK-B.CO, QTCOM.HE, MAERSK-A.CO, VWS.CO, ZEAL.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -5.6% | -2.32 | 0.64 | momentum -1.35 (-11.2), low_risk +0.65 (+5.9), short_term_reversal +0.68 (+2.6) |
| EU | French Europe 5F + WML | -5.2% | -1.39 | 0.33 | RMW +0.70 (+2.2), WML -0.95 (-6.6) |
| UK | JKP GBR 7 themes | -7.7% | -2.22 | 0.54 | mkt +0.18 (+3.5), momentum -1.11 (-7.0), low_risk +0.67 (+3.5), short_term_reversal +0.78 (+5.7) |
| DK | JKP DNK 7 themes | +1.2% | 0.34 | 0.48 | momentum -1.02 (-8.7), low_risk +0.63 (+5.8) |
| SCANDI | French Europe 5F + WML | +0.7% | 0.17 | 0.15 | WML -0.60 (-3.6) |
| World | JKP World 7 themes | -9.7% | -2.70 | 0.34 | mkt +0.17 (+3.2), momentum -0.83 (-6.7), low_risk +0.43 (+2.3) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +1.0% | 0.61 | 0.92 | mkt +0.95 (+19.2), size -0.24 (-3.1), value +0.33 (+3.8), momentum -0.57 (-7.8), short_term_reversal +0.54 (+3.6) |
| EU | French Europe 5F + WML | +0.8% | 0.32 | 0.76 | Mkt-RF +0.74 (+9.3), WML -0.57 (-8.0) |
| UK | JKP GBR 7 themes | +4.2% | 1.53 | 0.77 | mkt +0.64 (+14.8), momentum -0.49 (-3.2), low_risk -0.41 (-2.1), short_term_reversal +0.77 (+4.7) |
| DK | JKP DNK 7 themes | +7.2% | 2.45 | 0.68 | mkt +0.74 (+11.1), momentum -0.56 (-5.7) |
| SCANDI | French Europe 5F + WML | +7.8% | 2.46 | 0.59 | Mkt-RF +0.68 (+7.6), RMW +0.48 (+2.1), WML -0.44 (-3.7) |
| World | JKP World 7 themes | +0.0% | 0.01 | 0.82 | mkt +0.81 (+15.8), value +0.29 (+2.5), momentum -0.39 (-4.7) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in none of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -15.8% to -7.3%, |t| past the gate in 4 of 6.
- **Long-only:** Sharpe above the equal-weight universe in none of the six; alpha -9.7% to -2.5%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.01, EU 0.00, UK 0.02, DK 0.03, SCANDI 0.07, World 0.01.
- **Publication decay:** gross L/S -12.8% to -3.8% a year in 2013–19 against -15.9% to -1.6% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | -3.8% | 0.27 | +3.5% | -7.4% | -1.7% | -1.9% | -2.0% | 70% | 2017-10 -8%, 2017-05 -8%, 2019-08 -7% |
| EU | -8.7% | -0.06 | -0.6% | -8.1% | -1.7% | -5.3% | -3.5% | 72% | 2016-11 -9%, 2016-09 -8%, 2013-10 -7% |
| UK | -12.8% | 0.18 | +2.1% | -14.9% | -1.7% | -1.4% | -11.4% | 71% | 2016-04 -15%, 2016-06 -10%, 2017-01 -9% |
| DK | -10.9% | -0.10 | -1.5% | -9.4% | -0.9% | -4.2% | -6.7% | 37% | 2013-05 -14%, 2018-06 -9%, 2015-12 -8% |
| SCANDI | -3.8% | 0.03 | +0.4% | -4.2% | -1.3% | -2.1% | -1.7% | 54% | 2013-09 -11%, 2016-11 -11%, 2017-04 -8% |
| World | -7.0% | 0.21 | +2.3% | -9.3% | -1.8% | -3.5% | -3.5% | 74% | 2016-04 -8%, 2017-08 -7%, 2016-06 -7% |

On average across the six universes the gross spread was -7.8% a year, of which the market exposure (beta +0.09) contributed +1.0%; the beta-adjusted spread (CAPM alpha) was -8.9%. Costs took 1.5% a year at 63% monthly turnover across both legs. The long leg beat the universe by -3.0% and the short leg lagged it by -4.8% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +9.8%, +9.6%, +8.8% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.72 | – | -0.78 | – | – | -10.1% | -57% | -12.3% (-2.6) | 1.6% |
| X1 beta-neutral legs | -0.58 | +0.18 (p 0.081) | -0.45 | +0.33 (p 0.075) | 6 of 6 | -6.0% | -52% | -9.3% (-1.9) | 1.7% |
| X2 + turnover buffer | -0.67 | -0.13 (p 0.908) | -0.47 | -0.02 (p 0.547) | 3 of 6 | -5.1% | -42% | -8.0% (-2.0) | 0.8% |
| X3 + volatility targeting | -0.56 | +0.17 (p 0.354) | -0.57 | -0.11 (p 0.942) | 3 of 6 | -6.0% | -43% | -8.8% (-2.3) | 0.8% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS12_ladder.png)

- **X1 beta-neutral legs:** +0.18 design, +0.33 holdout; helps in both windows but does not pass the gate.
- **X2 + turnover buffer:** -0.13 design, -0.02 holdout; hurts in both windows.
- **X3 + volatility targeting:** +0.17 design, -0.11 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe -0.78 → -0.57, return -10.1% → -6.0% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Buy at the 52-week low |
|---|---|
| Series family | **Reversal & bottom-fishing** |
| Academic style | Contrarian / bottom-fishing |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 63% of the two legs replaced monthly |
| Market exposure | L/S beta 0.09 to 0.30 |
| Payoff shape | Treynor–Mazuy γ -1.14 to 1.93 (t -1.3 to 1.2); worst 10% of market months -2.2% to -0.6% a month, best 10% -0.8% to +1.6% |
| Nearest factor theme | momentum (4 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | Momentum 12-1 (6 universes), Last month return (4 universes), Residual momentum (3 universes) |
| Economic rationale | Folklore: mean reversion and value. Evidence: momentum and anchoring (George & Hwang 2004) predict continued weakness; losers carry high beta and volatility. |
| Publication | No academic origin; George & Hwang 2004 as the counter-claim; series A10 (Free Fallin') |
| Where it fits | In the **momentum** cluster of the library; fully explained by its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Near 52-week high**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Above 52-week low **(this strategy)** | momentum | +1.00 | +1.00 | +7.5% | +5.2% to +13.6% | 4 / 0 |
| Momentum 12-1 | momentum | +0.63 | +0.60 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| Near 52-week high (mirror) | momentum | +0.51 | +0.46 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| Last month return | short-term reversal | +0.40 | +0.46 | +1.8% | -3.2% to +11.0% | 2 / 0 |
| Residual momentum | momentum | +0.41 | +0.44 | +6.4% | +8.0% to +12.2% | 6 / 0 |
| 55-day breakout | momentum | +0.37 | +0.41 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.25 | +0.33 | -0.9% | -5.2% to +5.2% | 0 / 0 |
| MAX5 | low risk | +0.27 | +0.16 | +0.6% | -11.3% to -3.5% | 0 / 2 |
| Size | size | +0.07 | +0.15 | +0.1% | -3.8% to +9.9% | 1 / 0 |
| MIN5 | low risk | +0.09 | +0.14 | -0.9% | +2.3% to +13.7% | 4 / 0 |
| MAX (best day) | low risk | +0.22 | +0.12 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| Skewness | tail direction | +0.14 | +0.12 | -0.4% | -6.7% to +3.9% | 0 / 2 |
| MIN (worst day) | low risk | +0.06 | +0.12 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| Idiosyncratic vol | low risk | +0.09 | +0.07 | -3.6% | -15.5% to -4.8% | 0 / 4 |
| Volatility (252 days) | low risk | +0.23 | +0.04 | +2.4% | -12.9% to -4.8% | 0 / 3 |
| Volatility | low risk | +0.14 | -0.02 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| Range (MAX−MIN) | low risk | +0.08 | -0.02 | -0.7% | -15.4% to -4.8% | 0 / 4 |
| Same-month seasonality | seasonality | +0.06 | +0.01 | -1.9% | -9.4% to +6.6% | 0 / 1 |
| Beta | low risk | +0.18 | -0.01 | +4.4% | -12.6% to -4.2% | 0 / 4 |

![360 map](../figures/xs_FS12_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | +0.0% | 0.02 | 0.70 | Momentum 12-1 +0.69 (+7.6), Residual momentum +0.28 (+2.5), Last month return +0.34 (+4.6), Net tail +0.36 (+2.9), Near 52-week high -0.45 (-5.0) |
| EU | +2.8% | 1.07 | 0.59 | Momentum 12-1 +0.61 (+5.6), Last month return +0.46 (+6.2), Residual momentum +0.28 (+2.5), Near 52-week high -0.54 (-4.7) |
| UK | -0.2% | -0.06 | 0.52 | Momentum 12-1 +0.43 (+3.8), Residual momentum +0.43 (+2.9), Near 52-week high -0.31 (-2.3), Last month return +0.43 (+4.4) |
| DK | -1.3% | -0.49 | 0.55 | Momentum 12-1 +0.42 (+4.8), Last month return +0.34 (+3.7), Size +0.24 (+3.1) |
| SCANDI | +1.5% | 0.53 | 0.46 | Momentum 12-1 +0.30 (+2.4), 55-day breakout +0.22 (+2.0), Last month return +0.28 (+4.0), Residual momentum +0.30 (+2.5) |
| World | -0.7% | -0.31 | 0.63 | Momentum 12-1 +0.66 (+4.9), Last month return +0.55 (+7.4), Near 52-week high -0.48 (-3.8) |

![Double sort](../figures/xs_FS12_dsort.png)

Holding Near 52-week high fixed (down a column), moving from low to high Above 52-week low changes the return by +2.9, +6.1 and +3.7 points a year; holding Above 52-week low fixed (along a row), moving from low to high Near 52-week high changes it by +0.5, -0.1 and +1.2.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): +5% vs +12% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +7.5%, +9.8%, +9.6%, +8.8% a year.

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
