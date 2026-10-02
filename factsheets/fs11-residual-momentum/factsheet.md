# FACTSHEET FS11 · Residual momentum

### Momentum without the market's ups and downs

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

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

> **The claim.** Ranking stocks on the part of their past return that the market does not explain gives a momentum strategy with about half the volatility and far smaller crashes than plain momentum (Blitz, Huij & Martens 2011, US 1930–2009). **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned +2.2% to +6.9% a year and was positive in all six; no universe passes the 2.87 gate. The long-only book (stocks with the strongest stock-specific trend) had a higher Sharpe than the equal-weight universe in all six, with alphas of +2.4% to +3.9%, none past the gate. **What goes wrong (§10):** the main drags are a market bet (average beta -0.25, worth -2.4% a year in 2013–19), costs of about 2.0% a year. None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Momentum & trend; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours Momentum 12-1, Above 52-week low; after its closest neighbours and the market it keeps an alpha of +0.8% to +6.8% (largest |t| 3.5), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 499 / 10 | +3.8% | 1.22 | +6.5% (2.2) | -0.22 | +14.3% | 0.90 | -26% | +11.3% | 0.76 | +14.0% |
| EU | 262 / 10 | +2.9% | 0.80 | +5.7% (1.5) | -0.28 | +11.8% | 0.86 | -22% | +9.0% | 0.66 | +9.4% |
| UK | 319 / 10 | +2.2% | 0.63 | +4.9% (1.4) | -0.31 | +9.3% | 0.68 | -29% | +7.7% | 0.59 | +7.6% |
| DK | 20 / 3 | +6.9% | 1.41 | +9.8% (2.2) | -0.28 | +12.1% | 0.80 | -24% | +9.8% | 0.69 | +7.8% |
| SCANDI | 70 / 5 | +3.4% | 0.92 | +5.8% (1.5) | -0.20 | +13.9% | 0.95 | -21% | +11.3% | 0.81 | +10.5% |
| World | 1078 / 10 | +2.2% | 0.83 | +4.7% (2.0) | -0.24 | +10.7% | 0.73 | -25% | +9.0% | 0.61 | +9.4% |

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
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: the S&P 500 members at each month-end (Sharadar add/remove history; corrected 2 Oct 2026) | ~503 | USD |
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

**US (S&P 500 members, point-in-time)**, median 499 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +3.8% | +2.9% | 13.8% | 0.28 [-0.15, 0.66] | 0.35 | -20% | 48% | 1.22 | -0.22 | +6.5% (2.2) | 7.6% |
| Long-only (net) | +14.7% | +14.3% | 16.3% | 0.90 [0.49, 1.39] | 1.46 | -26% | 64% | 4.50 | 0.92 | +3.7% (2.3) | 9.3% |
| Stocks with the strongest stock-specific trend (gross) | +15.8% | +15.5% | 16.3% | 0.97 [0.55, 1.46] | 1.61 | -26% | 64% | 4.85 | 0.92 | +4.8% (3.0) | 9.2% |
| The weakest (gross) | +8.9% | +7.2% | 19.5% | 0.46 [0.02, 0.98] | 0.56 | -32% | 60% | 2.04 | 1.13 | -4.7% (-2.6) | 11.9% |
| EW universe | +12.0% | +11.3% | 15.9% | 0.76 [0.32, 1.31] | 1.12 | -28% | 67% | 3.64 | 1.00 | – | 9.6% |
| Size-weighted universe | +14.3% | +14.0% | 14.5% | 0.98 [0.52, 1.55] | 1.59 | -24% | 69% | 4.72 | 0.85 | +4.0% (2.5) | 8.6% |

**EU (11 national blue-chip indices, point-in-time)**, median 262 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.9% | +2.2% | 12.6% | 0.23 [-0.34, 0.81] | 0.25 | -28% | 55% | 0.80 | -0.28 | +5.7% (1.5) | 7.6% |
| Long-only (net) | +12.2% | +11.8% | 14.2% | 0.86 [0.36, 1.46] | 1.42 | -22% | 60% | 3.22 | 0.86 | +3.9% (1.9) | 7.6% |
| Stocks with the strongest stock-specific trend (gross) | +13.3% | +13.0% | 14.2% | 0.94 [0.43, 1.54] | 1.60 | -21% | 60% | 3.51 | 0.86 | +4.9% (2.4) | 7.5% |
| The weakest (gross) | +7.3% | +5.9% | 18.3% | 0.40 [-0.05, 0.88] | 0.52 | -37% | 56% | 1.62 | 1.14 | -3.7% (-1.7) | 10.4% |
| EW universe | +9.7% | +9.0% | 14.6% | 0.66 [0.21, 1.19] | 0.98 | -26% | 60% | 2.72 | 1.00 | – | 8.7% |
| Size-weighted universe | +10.0% | +9.4% | 14.0% | 0.72 [0.25, 1.24] | 1.09 | -25% | 58% | 2.96 | 0.91 | +1.2% (0.8) | 8.1% |

**UK (FTSE 350, point-in-time)**, median 319 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.2% | +1.1% | 14.6% | 0.15 [-0.33, 0.63] | 0.11 | -25% | 52% | 0.63 | -0.31 | +4.9% (1.4) | 8.6% |
| Long-only (net) | +10.1% | +9.3% | 14.8% | 0.68 [0.18, 1.29] | 1.01 | -29% | 57% | 2.65 | 0.89 | +2.5% (1.2) | 9.1% |
| Stocks with the strongest stock-specific trend (gross) | +11.2% | +10.5% | 14.8% | 0.76 [0.25, 1.37] | 1.15 | -27% | 58% | 2.94 | 0.89 | +3.6% (1.7) | 9.0% |
| The weakest (gross) | +6.0% | +4.2% | 19.3% | 0.31 [-0.14, 0.81] | 0.33 | -37% | 57% | 1.28 | 1.20 | -4.2% (-2.2) | 12.1% |
| EW universe | +8.5% | +7.7% | 14.4% | 0.59 [0.11, 1.18] | 0.80 | -30% | 58% | 2.38 | 1.00 | – | 9.2% |
| Size-weighted universe | +8.2% | +7.6% | 13.0% | 0.63 [0.12, 1.29] | 0.87 | -28% | 62% | 2.43 | 0.83 | +1.2% (0.6) | 8.1% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +6.9% | +5.7% | 16.4% | 0.42 [-0.13, 1.02] | 0.53 | -31% | 54% | 1.41 | -0.28 | +9.8% (2.2) | 9.7% |
| Long-only (net) | +12.8% | +12.1% | 16.0% | 0.80 [0.32, 1.28] | 1.25 | -24% | 58% | 3.62 | 0.89 | +3.4% (1.6) | 9.1% |
| Stocks with the strongest stock-specific trend (gross) | +13.4% | +12.8% | 16.0% | 0.84 [0.36, 1.33] | 1.33 | -24% | 58% | 3.81 | 0.89 | +4.0% (1.9) | 9.1% |
| The weakest (gross) | +4.4% | +2.3% | 20.4% | 0.22 [-0.36, 0.82] | 0.16 | -56% | 58% | 0.73 | 1.16 | -7.9% (-2.7) | 12.6% |
| EW universe | +10.6% | +9.8% | 15.4% | 0.69 [0.18, 1.25] | 0.99 | -33% | 65% | 2.70 | 1.00 | – | 9.2% |
| Size-weighted universe | +8.9% | +7.8% | 16.6% | 0.54 [-0.02, 1.16] | 0.69 | -40% | 59% | 2.00 | 0.93 | -0.9% (-0.3) | 11.0% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +3.4% | +2.6% | 13.1% | 0.26 [-0.30, 0.79] | 0.30 | -37% | 53% | 0.92 | -0.20 | +5.8% (1.5) | 7.2% |
| Long-only (net) | +14.2% | +13.9% | 15.0% | 0.95 [0.44, 1.53] | 1.64 | -21% | 60% | 3.90 | 0.91 | +3.5% (2.0) | 7.8% |
| Stocks with the strongest stock-specific trend (gross) | +15.1% | +15.0% | 15.0% | 1.01 [0.50, 1.60] | 1.79 | -20% | 60% | 4.14 | 0.91 | +4.5% (2.6) | 7.7% |
| The weakest (gross) | +9.2% | +7.9% | 17.8% | 0.52 [-0.04, 1.11] | 0.66 | -46% | 62% | 1.90 | 1.11 | -3.9% (-1.6) | 11.5% |
| EW universe | +11.8% | +11.3% | 14.5% | 0.81 [0.28, 1.42] | 1.22 | -29% | 65% | 3.16 | 1.00 | – | 8.7% |
| Size-weighted universe | +10.9% | +10.5% | 13.9% | 0.79 [0.28, 1.35] | 1.21 | -26% | 62% | 3.18 | 0.90 | +0.3% (0.2) | 8.3% |

**World (US + UK + EU, point-in-time)**, median 1078 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.2% | +1.6% | 11.1% | 0.20 [-0.24, 0.66] | 0.22 | -17% | 51% | 0.83 | -0.24 | +4.7% (2.0) | 6.4% |
| Long-only (net) | +11.4% | +10.7% | 15.7% | 0.73 [0.27, 1.24] | 1.07 | -25% | 64% | 3.23 | 0.90 | +2.4% (1.8) | 9.8% |
| Stocks with the strongest stock-specific trend (gross) | +12.5% | +11.9% | 15.7% | 0.80 [0.34, 1.32] | 1.21 | -25% | 65% | 3.55 | 0.90 | +3.5% (2.6) | 9.7% |
| The weakest (gross) | +7.3% | +5.5% | 19.6% | 0.37 [-0.09, 0.88] | 0.43 | -40% | 58% | 1.53 | 1.14 | -4.1% (-3.1) | 11.9% |
| EW universe | +10.0% | +9.0% | 16.3% | 0.61 [0.15, 1.16] | 0.84 | -30% | 62% | 2.58 | 1.00 | – | 10.1% |
| Size-weighted universe | +10.2% | +9.4% | 15.0% | 0.68 [0.19, 1.25] | 0.98 | -28% | 61% | 2.77 | 0.90 | +1.1% (1.2) | 9.2% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2014 | -2.5% | -18.3% | -13.0% | -14.8% | -4.5% | -6.8% |
| 2015 | +21.1% | +11.3% | +5.2% | +14.9% | +12.1% | +8.1% |
| 2016 | -4.1% | -2.2% | +7.8% | -1.9% | +11.5% | -1.3% |
| 2017 | -1.8% | -7.9% | +9.1% | -6.7% | -10.7% | -1.0% |
| 2018 | +4.1% | -11.4% | -2.6% | +23.5% | +4.4% | -2.1% |
| 2019 | -1.0% | -4.6% | -12.1% | +38.5% | -4.2% | -3.0% |
| 2020 | -5.0% | +2.7% | +2.4% | -23.1% | -27.0% | -1.4% |
| 2021 | -3.5% | +6.3% | -4.2% | +9.0% | +12.0% | -3.0% |
| 2022 | +21.8% | +13.0% | +17.8% | +33.3% | +18.7% | +22.1% |
| 2023 | +3.3% | -1.1% | -2.1% | -2.5% | -7.7% | +6.1% |
| 2024 | +1.9% | +15.9% | +1.3% | -10.9% | +17.6% | +5.2% |
| 2025 | -10.4% | +19.0% | +13.0% | +10.4% | +11.7% | -4.8% |
| 2026 | +19.1% | +11.9% | -3.7% | +21.3% | +9.3% | +5.5% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2014 | +12.9% | -10.9% | -5.4% | -0.6% | +6.4% | -0.9% |
| 2015 | +3.0% | +13.3% | +8.8% | +29.1% | +19.4% | +3.0% |
| 2016 | +9.1% | +24.9% | +21.8% | +12.9% | +35.9% | +8.8% |
| 2017 | +19.0% | +13.4% | +28.9% | +17.5% | +13.3% | +25.8% |
| 2018 | -3.5% | -16.0% | -15.0% | -4.5% | -3.6% | -15.2% |
| 2019 | +30.4% | +21.8% | +16.7% | +41.7% | +32.8% | +24.0% |
| 2020 | +15.5% | +13.1% | +1.4% | +19.6% | +5.4% | +14.2% |
| 2021 | +26.1% | +16.6% | +11.8% | +16.1% | +24.9% | +15.7% |
| 2022 | -1.1% | -4.1% | -5.6% | -13.3% | -10.8% | -5.6% |
| 2023 | +13.8% | +15.0% | +5.2% | +10.7% | +6.3% | +17.7% |
| 2024 | +14.1% | +13.6% | +11.1% | -6.6% | +10.0% | +10.1% |
| 2025 | +9.4% | +31.1% | +32.8% | +18.2% | +23.8% | +23.8% |
| 2026 | +35.9% | +26.2% | +13.8% | +22.1% | +18.6% | +21.0% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS11_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 150 | 50 / 50 | 46% | 46% | 48% | -10.2% | 2020-11 |
| EU | 149 | 27 / 26 | 44% | 45% | 55% | -13.1% | 2020-11 |
| UK | 149 | 33 / 32 | 46% | 46% | 52% | -23.7% | 2020-11 |
| DK | 149 | 8 / 7 | 28% | 28% | 54% | -18.9% | 2020-11 |
| SCANDI | 149 | 15 / 14 | 38% | 37% | 53% | -13.7% | 2020-11 |
| World | 150 | 109 / 108 | 46% | 46% | 51% | -14.2% | 2020-11 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks with the strongest stock-specific trend | Short: the weakest |
|---|---|---|
| US | HST, PFG, FRT, TGT, IEX, EIX, BIIB, CSX | VST, PLTR, UBER, CSGP, NFLX, META, BSX, TSCO |
| EU | DANSKE.CO, INVE-B.ST, DHL.DE, MRK.DE, SWED-A.ST, INDU-C.ST, NESTE.HE, LOG.MC | BAR.BR, CTT.LS, AGFB.BR, IVG.MI, RMS.PA, G24.DE, CBK.DE, RHM.DE |
| UK | KLR.L, EMG.L, MRCH.L, BLND.L, RTW.L, CRDA.L, ROSE.L, LAND.L | RNK.L, ENT.L, RMV.L, STJ.L, HWG.L, AVON.L, FCSS.L, AGT.L |
| DK | DANSKE.CO, NKT.CO, NOVO-B.CO, CARL-B.CO, JYSK.CO, ORSTED.CO, RBREW.CO, VWS.CO | BAVA.CO, TRYG.CO, MAERSK-A.CO, MAERSK-B.CO, COLO-B.CO, NSIS-B.CO, DSV.CO, AMBU-B.CO |
| SCANDI | DANSKE.CO, INVE-B.ST, SWED-A.ST, NESTE.HE, INDU-C.ST, ATCO-A.ST, TYRES.HE, JYSK.CO | BAVA.CO, MANTA.HE, KEMIRA.HE, SKF-B.ST, KNEBV.HE, VALMT.HE, TEL2-B.ST, ORNBV.HE |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +0.7% | 0.29 | 0.54 | value -0.29 (-2.3), momentum +0.91 (+8.7), low_risk +0.51 (+3.0), short_term_reversal +0.49 (+2.2) |
| EU | French Europe 5F + WML | -4.0% | -1.35 | 0.42 | HML +0.40 (+2.4), WML +0.77 (+8.8) |
| UK | JKP GBR 7 themes | +0.3% | 0.11 | 0.51 | momentum +0.95 (+5.4), short_term_reversal +0.41 (+2.3) |
| DK | JKP DNK 7 themes | +1.0% | 0.25 | 0.34 | momentum +0.80 (+5.4), short_term_reversal +0.53 (+3.7) |
| SCANDI | French Europe 5F + WML | -2.2% | -0.63 | 0.22 | HML +0.33 (+2.2), WML +0.55 (+5.5) |
| World | JKP World 7 themes | +2.0% | 0.63 | 0.40 | value -0.32 (-2.5), momentum +0.65 (+6.8), low_risk +0.30 (+2.3), quality -0.70 (-2.9) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +3.0% | 2.22 | 0.88 | mkt +1.03 (+25.1), momentum +0.39 (+5.8), low_risk +0.32 (+2.6), quality -0.36 (-2.2) |
| EU | French Europe 5F + WML | +5.2% | 2.06 | 0.62 | Mkt-RF +0.71 (+13.1), HML +0.33 (+2.5) |
| UK | JKP GBR 7 themes | +4.0% | 1.94 | 0.69 | mkt +0.55 (+7.8), momentum +0.44 (+5.6), low_risk -0.55 (-2.6), short_term_reversal +0.37 (+2.2) |
| DK | JKP DNK 7 themes | +5.6% | 2.22 | 0.59 | mkt +0.67 (+9.1), size -0.29 (-2.0), short_term_reversal +0.28 (+2.4) |
| SCANDI | French Europe 5F + WML | +7.6% | 2.14 | 0.49 | Mkt-RF +0.67 (+8.5) |
| World | JKP World 7 themes | +5.7% | 2.61 | 0.80 | mkt +0.71 (+13.5), momentum +0.22 (+2.5) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in all six; passes in 0 of 6.
- **L/S CAPM alpha:** +4.7% to +9.8%, |t| past the gate in 0 of 6.
- **Long-only:** Sharpe above the equal-weight universe in all six; alpha +2.4% to +3.9%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.84, EU 0.79, UK 0.70, DK 0.93, SCANDI 0.82, World 0.76.
- **Publication decay:** gross L/S -2.6% to +10.5% a year in 2013–19 against +7.5% to +13.3% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +6.1% | -0.41 | -4.4% | +10.5% | -2.2% | +2.0% | +4.1% | 91% | 2015-04 -6%, 2016-02 -6%, 2019-11 -5% |
| EU | -2.6% | -0.34 | -2.9% | +0.2% | -2.1% | -0.1% | -2.6% | 89% | 2018-11 -9%, 2015-02 -8%, 2014-04 -7% |
| UK | +2.5% | -0.33 | -3.2% | +5.7% | -2.2% | +0.3% | +2.1% | 94% | 2016-08 -8%, 2015-06 -6%, 2019-04 -5% |
| DK | +10.5% | -0.06 | -0.7% | +11.2% | -1.4% | +4.6% | +5.9% | 59% | 2014-11 -8%, 2016-04 -7%, 2016-10 -5% |
| SCANDI | +4.2% | -0.05 | -0.8% | +4.9% | -1.8% | +3.8% | +0.3% | 73% | 2018-11 -6%, 2018-07 -6%, 2016-04 -5% |
| World | +2.4% | -0.33 | -2.6% | +5.0% | -2.3% | +0.4% | +2.0% | 94% | 2016-02 -6%, 2019-04 -5%, 2015-02 -4% |

On average across the six universes the gross spread was +3.8% a year, of which the market exposure (beta -0.25) contributed -2.4%; the beta-adjusted spread (CAPM alpha) was +6.3%. Costs took 2.0% a year at 83% monthly turnover across both legs. The long leg beat the universe by +1.8% and the short leg lagged it by +2.0% a year, so most of the spread comes from the short side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +6.8%, +4.4%, +4.2% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.08 | – | 0.50 | – | – | +5.8% | -16% | +8.9% (2.4) | 2.0% |
| X1 beta-neutral legs | 0.12 | +0.09 (p 0.202) | 0.46 | -0.04 (p 0.618) | 2 of 6 | +4.5% | -18% | +6.2% (1.6) | 2.1% |
| X2 + turnover buffer | 0.14 | +0.04 (p 0.387) | 0.57 | +0.11 (p 0.063) | 6 of 6 | +4.9% | -13% | +6.4% (2.0) | 1.1% |
| X3 + volatility targeting | 0.07 | -0.10 (p 0.593) | 0.58 | +0.00 (p 0.495) | 1 of 6 | +5.7% | -17% | +7.1% (2.0) | 1.0% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS11_ladder.png)

- **X1 beta-neutral legs:** +0.09 design, -0.04 holdout; helps in one window and hurts in the other: not reliable.
- **X2 + turnover buffer:** +0.04 design, +0.11 holdout; helps in both windows but does not pass the gate.
- **X3 + volatility targeting:** -0.10 design, +0.00 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe 0.50 → 0.58, return +5.8% → +5.7% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Residual momentum |
|---|---|
| Series family | **Momentum & trend** |
| Academic style | Residual (idiosyncratic) momentum |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 83% of the two legs replaced monthly |
| Market exposure | L/S beta -0.31 to -0.20 |
| Payoff shape | Treynor–Mazuy γ -1.66 to -0.25 (t -3.4 to -0.2); worst 10% of market months +0.7% to +3.5% a month, best 10% -2.6% to -0.9% |
| Nearest factor theme | momentum (4 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | Momentum 12-1 (6 universes), Near 52-week high (6 universes), Above 52-week low (5 universes) |
| Economic rationale | Same under-reaction story as momentum, but removing the market (and factor) component avoids the time-varying beta that makes plain momentum crash (Grundy & Martin 2001; Daniel & Moskowitz 2016). |
| Publication | Grundy & Martin 2001; Gutierrez & Pirinsky 2007; Blitz, Huij & Martens 2011 |
| Where it fits | In the **momentum** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Last month return**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Residual momentum **(this strategy)** | momentum | +1.00 | +1.00 | +6.4% | +8.0% to +12.2% | 6 / 0 |
| Momentum 12-1 | momentum | +0.66 | +0.64 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| Near 52-week high | momentum | +0.30 | +0.46 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| Above 52-week low | momentum | +0.41 | +0.44 | +7.5% | +5.2% to +13.6% | 4 / 0 |
| MAX5 | low risk | -0.15 | -0.31 | +0.6% | -11.3% to -3.5% | 0 / 2 |
| Volatility | low risk | -0.08 | -0.31 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| MAX (best day) | low risk | -0.13 | -0.29 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| Range (MAX−MIN) | low risk | -0.06 | -0.29 | -0.7% | -15.4% to -4.8% | 0 / 4 |
| Beta | low risk | -0.05 | -0.28 | +4.4% | -12.6% to -4.2% | 0 / 4 |
| Volatility (252 days) | low risk | -0.05 | -0.26 | +2.4% | -12.9% to -4.8% | 0 / 3 |
| 55-day breakout | momentum | +0.01 | +0.24 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| MIN5 | low risk | -0.02 | +0.24 | -0.9% | +2.3% to +13.7% | 4 / 0 |
| Idiosyncratic vol | low risk | -0.05 | -0.23 | -3.6% | -15.5% to -4.8% | 0 / 4 |
| MIN (worst day) | low risk | -0.02 | +0.23 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| Skewness | tail direction | -0.09 | -0.13 | -0.4% | -6.7% to +3.9% | 0 / 2 |
| Size | size | +0.02 | +0.11 | +0.1% | -3.8% to +9.9% | 1 / 0 |
| Net tail (MAX+MIN) | tail direction | -0.12 | -0.07 | -0.9% | -5.2% to +5.2% | 0 / 0 |
| Same-month seasonality | seasonality | +0.01 | -0.03 | -1.9% | -9.4% to +6.6% | 0 / 1 |
| Last month return (mirror) | short-term reversal | -0.16 | +0.01 | +1.8% | -3.2% to +11.0% | 2 / 0 |

![360 map](../figures/xs_FS11_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | +6.8% | 3.54 | 0.51 | Momentum 12-1 +0.39 (+3.3), Near 52-week high +0.31 (+2.2), Size -0.30 (-2.8), 55-day breakout -0.36 (-3.6) |
| EU | +0.9% | 0.29 | 0.42 | Momentum 12-1 +0.42 (+4.4) |
| UK | +1.8% | 0.59 | 0.51 | Momentum 12-1 +0.39 (+3.9), Above 52-week low +0.22 (+2.4) |
| DK | +6.0% | 1.65 | 0.41 | Momentum 12-1 +0.62 (+8.2), MAX5 -0.18 (-2.2) |
| SCANDI | +4.5% | 1.50 | 0.41 | Momentum 12-1 +0.51 (+5.6), Above 52-week low +0.33 (+3.4), Near 52-week high -0.34 (-2.9) |
| World | +0.8% | 0.37 | 0.61 | Momentum 12-1 +0.38 (+4.0), Above 52-week low +0.31 (+3.6), 55-day breakout -0.39 (-4.0), Volatility -0.24 (-4.1) |

![Double sort](../figures/xs_FS11_dsort.png)

Holding Last month return fixed (down a column), moving from low to high Residual momentum changes the return by +4.4, +4.5 and +3.3 points a year; holding Residual momentum fixed (along a row), moving from low to high Last month return changes it by +1.2, -2.3 and +0.0.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -1% vs +19% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +6.4%, +6.8%, +4.4%, +4.2% a year.

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
