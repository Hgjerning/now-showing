# FACTSHEET FS11 · Residual momentum

### Momentum without the market's ups and downs

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Residual (idiosyncratic) momentum</div>
<div><b>Origin</b>Blitz, Huij & Martens (2011)</div>
<div><b>Family</b>Momentum & trend</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (stocks with the strongest stock-specific trend)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Ranking stocks on the part of their past return that the market does not explain gives a momentum strategy with about half the volatility and far smaller crashes than plain momentum (Blitz, Huij & Martens 2011, US 1930–2009). **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned +1.9% to +7.9% a year and was positive in all six; no universe passes the 2.87 gate. The long-only book (stocks with the strongest stock-specific trend) had a higher Sharpe than the equal-weight universe in all six, with alphas of +2.7% to +4.4%, none past the gate. **What goes wrong (§10):** the main drags are a market bet (average beta -0.26, worth -2.8% a year in 2013–19), costs of about 2.0% a year. None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Momentum & trend; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours Momentum 12-1, Above 52-week low; after those neighbours and the market, nothing is left (alpha |t| < 2 everywhere): the signal is redundant.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 497 / 10 | +2.8% | 0.79 | +5.2% (1.5) | -0.18 | +15.8% | 0.98 | -24% | +12.9% | 0.87 | +14.5% |
| EU | 238 / 10 | +3.1% | 0.85 | +6.0% (1.6) | -0.28 | +13.1% | 0.94 | -21% | +9.7% | 0.70 | +9.2% |
| UK | 235 / 10 | +2.0% | 0.57 | +4.6% (1.4) | -0.28 | +10.5% | 0.75 | -28% | +8.6% | 0.65 | +8.3% |
| DK | 19 / 3 | +7.9% | 1.64 | +10.7% (2.3) | -0.26 | +11.7% | 0.76 | -26% | +10.0% | 0.68 | +8.0% |
| SCANDI | 62 / 5 | +2.4% | 0.65 | +4.7% (1.2) | -0.20 | +13.7% | 0.94 | -24% | +11.4% | 0.82 | +9.7% |
| World | 965 / 10 | +1.9% | 0.68 | +4.3% (1.7) | -0.21 | +12.5% | 0.83 | -26% | +10.5% | 0.71 | +9.7% |

*Monthly, local currency (World in USD). L/S = equal-weighted stocks with the strongest stock-specific trend minus the weakest, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS11_growth.png)

## 2. Strategy description

Ranking stocks on the part of their past return that the market does not explain gives a momentum strategy with about half the volatility and far smaller crashes than plain momentum (Blitz, Huij & Martens 2011, US 1930–2009).

**Why it might work.** Same under-reaction story as momentum, but removing the market (and factor) component avoids the time-varying beta that makes plain momentum crash (Grundy & Martin 2001; Daniel & Moskowitz 2016).

| Rule | Original (Blitz, Huij & Martens (2011)) | This factsheet |
|---|---|---|
| Signal | Sum of Fama-French 3-factor residuals t−12..t−2, over a 36-month window, divided by their volatility | Market-model residuals over 24 months, same scaling |
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

- **Data gap:** Market-only residuals over 24 months (the paper uses Fama-French 3 factors over 36); stock-level factor loadings outside the US would need data we do not have. The first signals appear in early 2014.

## 4. Signal creation

RESMOM<sub>i,t</sub> = Σ ε<sub>i,t−11..t−1</sub> / σ(ε), from monthly regressions of r<sub>i</sub> on the equal-weight universe over the last 24 months. Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = stocks with the strongest stock-specific trend minus the weakest; **long-only** = stocks with the strongest stock-specific trend; benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (top 500, point-in-time)**, median 497 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.8% | +1.8% | 14.1% | 0.20 [-0.27, 0.63] | 0.20 | -25% | 46% | 0.79 | -0.18 | +5.2% (1.5) | 8.1% |
| Long-only (net) | +16.1% | +15.8% | 16.5% | 0.98 [0.55, 1.46] | 1.67 | -24% | 64% | 4.42 | 0.94 | +3.5% (2.0) | 9.2% |
| Stocks with the strongest stock-specific trend (gross) | +17.2% | +17.1% | 16.5% | 1.05 [0.61, 1.54] | 1.83 | -24% | 66% | 4.72 | 0.94 | +4.6% (2.6) | 9.1% |
| The weakest (gross) | +11.4% | +10.0% | 19.0% | 0.60 [0.17, 1.13] | 0.82 | -32% | 62% | 2.78 | 1.12 | -3.6% (-1.9) | 11.4% |
| EW universe | +13.4% | +12.9% | 15.5% | 0.87 [0.43, 1.42] | 1.34 | -25% | 68% | 4.23 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.7% | +14.5% | 14.7% | 1.00 [0.53, 1.57] | 1.64 | -24% | 69% | 4.69 | 0.90 | +2.6% (1.9) | 8.6% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +3.1% | +2.4% | 12.3% | 0.25 [-0.33, 0.84] | 0.29 | -29% | 55% | 0.85 | -0.28 | +6.0% (1.6) | 6.7% |
| Long-only (net) | +13.3% | +13.1% | 14.2% | 0.94 [0.44, 1.54] | 1.63 | -21% | 62% | 3.48 | 0.85 | +4.4% (2.1) | 7.5% |
| Stocks with the strongest stock-specific trend (gross) | +14.4% | +14.3% | 14.1% | 1.02 [0.51, 1.62] | 1.81 | -21% | 62% | 3.77 | 0.85 | +5.5% (2.6) | 7.4% |
| The weakest (gross) | +8.3% | +6.9% | 18.3% | 0.45 [-0.01, 0.94] | 0.61 | -37% | 56% | 1.82 | 1.13 | -3.5% (-1.6) | 10.5% |
| EW universe | +10.4% | +9.7% | 14.8% | 0.70 [0.24, 1.24] | 1.06 | -26% | 62% | 2.88 | 1.00 | – | 8.6% |
| Size-weighted universe | +9.9% | +9.2% | 14.5% | 0.68 [0.20, 1.22] | 1.01 | -26% | 58% | 2.70 | 0.95 | +0.0% (0.0) | 8.6% |

**UK (FTSE 350, point-in-time)**, median 235 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.0% | +1.0% | 14.0% | 0.14 [-0.35, 0.63] | 0.10 | -25% | 54% | 0.57 | -0.28 | +4.6% (1.4) | 8.8% |
| Long-only (net) | +11.1% | +10.5% | 14.9% | 0.75 [0.22, 1.38] | 1.12 | -28% | 59% | 2.89 | 0.91 | +2.7% (1.3) | 9.0% |
| Stocks with the strongest stock-specific trend (gross) | +12.2% | +11.7% | 14.9% | 0.82 [0.29, 1.46] | 1.26 | -28% | 59% | 3.18 | 0.91 | +3.8% (1.8) | 8.9% |
| The weakest (gross) | +7.2% | +5.6% | 19.1% | 0.38 [-0.07, 0.89] | 0.45 | -35% | 58% | 1.57 | 1.19 | -3.8% (-2.0) | 11.5% |
| EW universe | +9.3% | +8.6% | 14.4% | 0.65 [0.17, 1.23] | 0.90 | -29% | 58% | 2.70 | 1.00 | – | 9.2% |
| Size-weighted universe | +8.8% | +8.3% | 12.9% | 0.69 [0.17, 1.33] | 0.97 | -27% | 62% | 2.66 | 0.82 | +1.2% (0.6) | 8.0% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +7.9% | +6.6% | 17.3% | 0.46 [-0.09, 1.02] | 0.57 | -35% | 55% | 1.64 | -0.26 | +10.7% (2.3) | 11.1% |
| Long-only (net) | +12.5% | +11.7% | 16.5% | 0.76 [0.26, 1.25] | 1.18 | -26% | 60% | 3.23 | 0.88 | +2.9% (1.4) | 8.7% |
| Stocks with the strongest stock-specific trend (gross) | +13.2% | +12.5% | 16.5% | 0.80 [0.30, 1.30] | 1.27 | -25% | 60% | 3.40 | 0.88 | +3.6% (1.7) | 8.6% |
| The weakest (gross) | +3.2% | +1.1% | 20.8% | 0.16 [-0.38, 0.73] | 0.07 | -55% | 56% | 0.56 | 1.14 | -9.1% (-3.2) | 14.1% |
| EW universe | +10.9% | +10.0% | 15.9% | 0.68 [0.17, 1.26] | 0.98 | -33% | 62% | 2.62 | 1.00 | – | 9.6% |
| Size-weighted universe | +9.1% | +8.0% | 16.8% | 0.54 [-0.01, 1.17] | 0.70 | -40% | 59% | 2.01 | 0.91 | -0.8% (-0.3) | 11.2% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.4% | +1.5% | 13.1% | 0.18 [-0.35, 0.71] | 0.18 | -38% | 48% | 0.65 | -0.20 | +4.7% (1.2) | 7.4% |
| Long-only (net) | +14.0% | +13.7% | 14.9% | 0.94 [0.42, 1.53] | 1.65 | -24% | 61% | 3.75 | 0.90 | +3.3% (1.8) | 7.6% |
| Stocks with the strongest stock-specific trend (gross) | +14.9% | +14.8% | 14.9% | 1.00 [0.48, 1.60] | 1.80 | -22% | 61% | 3.99 | 0.90 | +4.2% (2.3) | 7.5% |
| The weakest (gross) | +10.0% | +8.8% | 17.7% | 0.57 [0.01, 1.16] | 0.76 | -46% | 61% | 2.08 | 1.10 | -3.1% (-1.3) | 11.2% |
| EW universe | +11.9% | +11.4% | 14.5% | 0.82 [0.29, 1.43] | 1.25 | -29% | 66% | 3.14 | 1.00 | – | 8.5% |
| Size-weighted universe | +10.3% | +9.7% | 14.2% | 0.73 [0.22, 1.30] | 1.07 | -27% | 62% | 2.80 | 0.94 | -0.9% (-0.8) | 8.9% |

**World (US + UK + EU, point-in-time)**, median 965 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +1.9% | +1.3% | 10.8% | 0.18 [-0.30, 0.65] | 0.18 | -21% | 48% | 0.68 | -0.21 | +4.3% (1.7) | 6.3% |
| Long-only (net) | +13.1% | +12.5% | 15.7% | 0.83 [0.37, 1.35] | 1.28 | -26% | 66% | 3.66 | 0.92 | +2.7% (2.0) | 9.6% |
| Stocks with the strongest stock-specific trend (gross) | +14.1% | +13.7% | 15.7% | 0.90 [0.44, 1.43] | 1.43 | -25% | 67% | 3.97 | 0.92 | +3.8% (2.8) | 9.5% |
| The weakest (gross) | +9.2% | +7.7% | 19.0% | 0.49 [0.01, 1.02] | 0.63 | -40% | 60% | 2.00 | 1.13 | -3.5% (-2.4) | 11.7% |
| EW universe | +11.3% | +10.5% | 16.0% | 0.71 [0.25, 1.27] | 1.02 | -28% | 63% | 3.03 | 1.00 | – | 9.8% |
| Size-weighted universe | +10.5% | +9.7% | 15.2% | 0.69 [0.20, 1.26] | 1.00 | -28% | 62% | 2.80 | 0.93 | -0.1% (-0.1) | 9.3% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2014 | -2.6% | -15.8% | -11.5% | -11.0% | -0.9% | -4.1% |
| 2015 | +14.5% | +5.8% | +7.3% | +7.9% | +11.8% | +6.5% |
| 2016 | -5.7% | -1.2% | +14.3% | -6.5% | +5.2% | -1.5% |
| 2017 | -3.1% | -8.5% | +8.4% | -1.9% | -14.0% | -2.1% |
| 2018 | +3.3% | -7.8% | -4.3% | +23.3% | +2.3% | +1.1% |
| 2019 | -5.6% | -4.7% | -9.7% | +34.9% | -9.9% | -6.3% |
| 2020 | -0.6% | +4.9% | -1.0% | -10.5% | -19.6% | -3.6% |
| 2021 | -6.0% | +2.9% | -6.8% | +23.9% | +8.0% | -5.3% |
| 2022 | +20.8% | +13.9% | +9.3% | +33.3% | +16.2% | +20.6% |
| 2023 | +5.4% | -1.6% | +1.2% | -16.3% | -8.7% | +7.1% |
| 2024 | +4.8% | +16.7% | -0.5% | -10.3% | +17.7% | +8.0% |
| 2025 | -18.3% | +19.5% | +12.4% | +11.6% | +15.5% | -8.3% |
| 2026 | +23.8% | +11.9% | -2.7% | +21.3% | +4.4% | +8.2% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2014 | +15.3% | -7.7% | +0.4% | +2.5% | +8.6% | +3.5% |
| 2015 | +5.1% | +12.9% | +9.0% | +23.0% | +17.7% | +5.1% |
| 2016 | +8.5% | +26.6% | +24.9% | +7.1% | +30.3% | +8.9% |
| 2017 | +19.6% | +15.7% | +34.6% | +15.5% | +12.5% | +26.6% |
| 2018 | -2.6% | -13.1% | -13.5% | -3.0% | -1.8% | -10.9% |
| 2019 | +28.0% | +21.6% | +21.1% | +38.1% | +28.8% | +25.9% |
| 2020 | +24.8% | +14.9% | -0.3% | +30.2% | +11.1% | +18.2% |
| 2021 | +24.1% | +16.5% | +10.9% | +29.1% | +25.1% | +14.5% |
| 2022 | -2.7% | -3.8% | -9.8% | -15.1% | -11.6% | -6.8% |
| 2023 | +17.1% | +16.6% | +6.5% | -0.9% | +3.0% | +19.2% |
| 2024 | +21.8% | +14.3% | +11.0% | -6.1% | +9.1% | +15.2% |
| 2025 | +7.9% | +31.6% | +33.0% | +17.4% | +27.9% | +22.4% |
| 2026 | +38.2% | +26.2% | +14.1% | +22.1% | +18.0% | +22.0% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS11_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 150 | 50 / 49 | 46% | 47% | 46% | -9.9% | 2025-06 |
| EU | 149 | 24 / 23 | 44% | 46% | 55% | -10.3% | 2020-11 |
| UK | 149 | 25 / 24 | 45% | 46% | 54% | -22.3% | 2020-11 |
| DK | 149 | 7 / 7 | 28% | 28% | 55% | -20.7% | 2020-11 |
| SCANDI | 149 | 13 / 12 | 38% | 38% | 48% | -11.9% | 2020-11 |
| World | 150 | 98 / 97 | 46% | 47% | 48% | -10.1% | 2020-11 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks with the strongest stock-specific trend | Short: the weakest |
|---|---|---|
| US | PFG, HST, FRT, TGT, EIX, IEX, CSX, BIIB | VST, UBER, PLTR, CSGP, RDDT, NFLX, META, BSX |
| EU | DANSKE.CO, INVE-B.ST, DHL.DE, MRK.DE, SWED-A.ST, INDU-C.ST, NESTE.HE, LOG.MC | BAR.BR, CTT.LS, AGFB.BR, IVG.MI, RMS.PA, G24.DE, CBK.DE, RHM.DE |
| UK | KLR.L, EMG.L, MRCH.L, BLND.L, RTW.L, ROSE.L, CRDA.L, LAND.L | RNK.L, ENT.L, STJ.L, RMV.L, HWG.L, AVON.L, FCSS.L, AGT.L |
| DK | DANSKE.CO, NKT.CO, NOVO-B.CO, CARL-B.CO, JYSK.CO, ORSTED.CO, RBREW.CO, NDA-DK.CO | BAVA.CO, TRYG.CO, MAERSK-A.CO, MAERSK-B.CO, COLO-B.CO, NSIS-B.CO, DSV.CO, AMBU-B.CO |
| SCANDI | DANSKE.CO, INVE-B.ST, SWED-A.ST, NESTE.HE, INDU-C.ST, ATCO-A.ST, TYRES.HE, NOVO-B.CO | BAVA.CO, KEMIRA.HE, MANTA.HE, SKF-B.ST, KNEBV.HE, VALMT.HE, ORNBV.HE, TEL2-B.ST |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -0.6% | -0.21 | 0.51 | size +0.31 (+2.7), value -0.31 (-2.5), momentum +0.92 (+8.7), low_risk +0.54 (+3.0), quality -0.68 (-2.3) |
| EU | French Europe 5F + WML | -4.2% | -1.40 | 0.43 | HML +0.42 (+2.6), WML +0.78 (+9.9) |
| UK | JKP GBR 7 themes | +0.3% | 0.09 | 0.51 | momentum +0.97 (+5.9) |
| DK | JKP DNK 7 themes | +1.0% | 0.26 | 0.32 | momentum +0.86 (+5.5), short_term_reversal +0.44 (+2.3) |
| SCANDI | French Europe 5F + WML | -2.6% | -0.78 | 0.18 | WML +0.51 (+5.2) |
| World | JKP World 7 themes | +1.1% | 0.37 | 0.42 | value -0.31 (-2.3), momentum +0.67 (+7.6), low_risk +0.35 (+2.5), quality -0.72 (-3.6) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +4.1% | 2.80 | 0.87 | mkt +1.05 (+24.7), momentum +0.45 (+6.0), low_risk +0.32 (+2.3), quality -0.34 (-2.2) |
| EU | French Europe 5F + WML | +6.5% | 2.50 | 0.64 | Mkt-RF +0.71 (+14.0), HML +0.35 (+2.9) |
| UK | JKP GBR 7 themes | +4.7% | 2.15 | 0.71 | mkt +0.59 (+8.9), momentum +0.47 (+6.2), low_risk -0.56 (-2.9) |
| DK | JKP DNK 7 themes | +4.5% | 1.65 | 0.58 | mkt +0.67 (+8.5), momentum +0.25 (+2.1), low_risk -0.31 (-2.5), short_term_reversal +0.30 (+2.3) |
| SCANDI | French Europe 5F + WML | +8.0% | 2.28 | 0.49 | Mkt-RF +0.65 (+8.6) |
| World | JKP World 7 themes | +7.2% | 3.35 | 0.79 | mkt +0.74 (+13.3), momentum +0.30 (+3.1) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in all six; passes in 0 of 6.
- **L/S CAPM alpha:** +4.3% to +10.7%, |t| past the gate in 0 of 6.
- **Long-only:** Sharpe above the equal-weight universe in all six; alpha +2.7% to +4.4%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.76, EU 0.81, UK 0.69, DK 0.94, SCANDI 0.74, World 0.73.
- **Publication decay:** gross L/S -2.3% to +9.6% a year in 2013–19 against +5.7% to +13.3% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +3.7% | -0.35 | -4.1% | +7.8% | -2.2% | +1.5% | +2.1% | 93% | 2016-02 -8%, 2019-11 -7%, 2015-10 -7% |
| EU | -2.3% | -0.37 | -3.5% | +1.2% | -2.2% | +0.6% | -2.9% | 91% | 2015-02 -9%, 2018-11 -6%, 2014-11 -6% |
| UK | +4.1% | -0.36 | -4.0% | +8.1% | -2.2% | +1.9% | +2.3% | 93% | 2014-05 -8%, 2016-08 -7%, 2019-04 -6% |
| DK | +9.6% | -0.05 | -0.6% | +10.2% | -1.4% | +3.1% | +6.5% | 58% | 2014-11 -8%, 2016-04 -7%, 2015-04 -5% |
| SCANDI | +1.7% | -0.09 | -1.2% | +2.9% | -1.8% | +2.8% | -1.1% | 73% | 2018-07 -6%, 2017-10 -6%, 2018-11 -6% |
| World | +2.3% | -0.33 | -3.1% | +5.4% | -2.3% | +1.1% | +1.2% | 95% | 2016-02 -7%, 2019-04 -6%, 2015-02 -5% |

On average across the six universes the gross spread was +3.2% a year, of which the market exposure (beta -0.26) contributed -2.8%; the beta-adjusted spread (CAPM alpha) was +5.9%. Costs took 2.0% a year at 84% monthly turnover across both legs. The long leg beat the universe by +1.9% and the short leg lagged it by +1.3% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +6.6%, +4.0%, +4.0% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.02 | – | 0.52 | – | – | +5.9% | -15% | +9.0% (2.3) | 2.0% |
| X1 beta-neutral legs | 0.06 | +0.08 (p 0.224) | 0.50 | -0.02 (p 0.567) | 2 of 6 | +4.7% | -13% | +6.2% (1.6) | 2.1% |
| X2 + turnover buffer | 0.08 | +0.05 (p 0.388) | 0.56 | +0.06 (p 0.272) | 5 of 6 | +4.6% | -13% | +5.7% (1.7) | 1.1% |
| X3 + volatility targeting | 0.04 | -0.09 (p 0.576) | 0.57 | +0.02 (p 0.415) | 3 of 6 | +5.5% | -16% | +6.5% (1.9) | 1.0% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS11_ladder.png)

- **X1 beta-neutral legs:** +0.08 design, -0.02 holdout; helps in one window and hurts in the other: not reliable.
- **X2 + turnover buffer:** +0.05 design, +0.06 holdout; helps in both windows but does not pass the gate.
- **X3 + volatility targeting:** -0.09 design, +0.02 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe 0.52 → 0.57, return +5.9% → +5.5% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Residual momentum |
|---|---|
| Series family | **Momentum & trend** |
| Academic style | Residual (idiosyncratic) momentum |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 84% of the two legs replaced monthly |
| Market exposure | L/S beta -0.28 to -0.18 |
| Payoff shape | Treynor–Mazuy γ -2.00 to 0.06 (t -3.3 to 0.1); worst 10% of market months +0.5% to +3.1% a month, best 10% -2.0% to -1.2% |
| Nearest factor theme | momentum (4 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | Momentum 12-1 (6 universes), Above 52-week low (6 universes), Near 52-week high (6 universes) |
| Economic rationale | Same under-reaction story as momentum, but removing the market (and factor) component avoids the time-varying beta that makes plain momentum crash (Grundy & Martin 2001; Daniel & Moskowitz 2016). |
| Publication | Grundy & Martin 2001; Gutierrez & Pirinsky 2007; Blitz, Huij & Martens 2011 |
| Where it fits | In the **momentum** cluster of the library; fully explained by its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Last month return**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Residual momentum **(this strategy)** | momentum | +1.00 | +1.00 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| Momentum 12-1 | momentum | +0.66 | +0.63 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Near 52-week high | momentum | +0.30 | +0.47 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| Above 52-week low | momentum | +0.41 | +0.46 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Volatility | low risk | -0.07 | -0.28 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| MAX5 | low risk | -0.14 | -0.26 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| Range (MAX−MIN) | low risk | -0.06 | -0.26 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| 55-day breakout | momentum | +0.00 | +0.26 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Beta | low risk | -0.05 | -0.25 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| MAX (best day) | low risk | -0.12 | -0.25 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| MIN5 | low risk | -0.03 | +0.23 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| Volatility (252 days) | low risk | -0.05 | -0.23 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| Idiosyncratic vol | low risk | -0.05 | -0.20 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| MIN (worst day) | low risk | -0.03 | +0.20 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| Skewness | tail direction | -0.09 | -0.12 | -0.2% | -5.4% to +4.5% | 0 / 1 |
| Size | size | +0.01 | +0.11 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Net tail (MAX+MIN) | tail direction | -0.13 | -0.07 | -1.0% | -5.3% to +4.2% | 0 / 0 |
| Last month return (mirror) | short-term reversal | -0.16 | +0.05 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Same-month seasonality | seasonality | +0.01 | -0.04 | -1.8% | -8.5% to +7.2% | 0 / 0 |

![360 map](../figures/xs_FS11_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | +3.8% | 1.43 | 0.40 | Momentum 12-1 +0.31 (+2.3) |
| EU | +2.0% | 0.61 | 0.43 | Momentum 12-1 +0.36 (+3.6), MAX -0.25 (-2.6) |
| UK | +2.9% | 0.86 | 0.47 | Above 52-week low +0.32 (+2.6) |
| DK | +4.9% | 1.45 | 0.48 | Momentum 12-1 +0.77 (+7.1) |
| SCANDI | +5.4% | 1.75 | 0.38 | Momentum 12-1 +0.47 (+4.9) |
| World | -0.1% | -0.02 | 0.55 | Momentum 12-1 +0.28 (+2.9), Above 52-week low +0.34 (+3.1), 55-day breakout -0.34 (-3.2), Volatility -0.30 (-4.7) |

![Double sort](../figures/xs_FS11_dsort.png)

Holding Last month return fixed (down a column), moving from low to high Residual momentum changes the return by +3.7, +4.1 and +2.5 points a year; holding Residual momentum fixed (along a row), moving from low to high Last month return changes it by +1.1, -0.6 and -0.1.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -1% vs +18% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +6.1%, +6.6%, +4.0%, +4.0% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Data gap.** Market-only residuals over 24 months (the paper uses Fama-French 3 factors over 36); stock-level factor loadings outside the US would need data we do not have. The first signals appear in early 2014.
5. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- Blitz, D., Huij, J. & Martens, M. (2011). Residual momentum. *Journal of Empirical Finance*, 18(3), 506–521.
- Grundy, B. & Martin, J. S. (2001). Understanding the nature of the risks and the source of the rewards to momentum investing. *Review of Financial Studies*, 14(1), 29–78.
- Daniel, K. & Moskowitz, T. (2016). Momentum crashes. *Journal of Financial Economics*, 122(2), 221–247.
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

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS11` → `build_xs.py FS11`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
