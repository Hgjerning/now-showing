# FACTSHEET FS07 · Size

### Do smaller companies beat bigger ones?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Size premium (Fama-French SMB)</div>
<div><b>Origin</b>Banz (1981)</div>
<div><b>Family</b>Size</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (smallest names in the universe)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Small companies earn higher returns than large ones. Banz (1981) found it in US stocks 1936–1975; it became Fama & French's SMB factor, but has been weak since the early 1980s unless junk stocks are controlled for (Asness et al. 2018). **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -3.0% to +4.9% a year and was positive in 4 of the six; no universe passes the 2.87 gate. The long-only book (smallest names in the universe) had a higher Sharpe than the equal-weight universe in 1 of the six (UK), with alphas of -2.6% to +5.8%, passing the gate in UK. **What goes wrong (§10):** the main drags are a weaker second half (2020–26). None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Size; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours Near 52-week high, 55-day breakout; after those neighbours and the market, nothing is left (alpha |t| < 2 everywhere): the signal is redundant.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 503 / 10 | +0.4% | 0.17 | -5.5% (-1.7) | 0.41 | +14.3% | 0.77 | -38% | +14.2% | 0.96 | +15.3% |
| EU | 236 / 10 | -2.2% | -0.64 | -3.6% (-1.0) | 0.12 | +8.4% | 0.57 | -30% | +10.9% | 0.78 | +10.1% |
| UK | 242 / 10 | +4.9% | 1.43 | +2.9% (0.7) | 0.20 | +15.5% | 1.06 | -26% | +10.0% | 0.74 | +8.5% |
| DK | 19 / 3 | -3.0% | -0.79 | -4.0% (-1.0) | 0.08 | +10.6% | 0.64 | -42% | +12.3% | 0.82 | +10.3% |
| SCANDI | 62 / 5 | +2.7% | 1.07 | +1.5% (0.6) | 0.09 | +14.4% | 0.91 | -26% | +12.5% | 0.91 | +10.7% |
| World | 979 / 10 | +0.2% | 0.07 | -3.1% (-1.5) | 0.26 | +11.7% | 0.70 | -34% | +12.0% | 0.80 | +10.8% |

*Monthly, local currency (World in USD). L/S = equal-weighted smallest names in the universe minus largest names, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS07_growth.png)

## 2. Strategy description

Small companies earn higher returns than large ones. Banz (1981) found it in US stocks 1936–1975; it became Fama & French's SMB factor, but has been weak since the early 1980s unless junk stocks are controlled for (Asness et al. 2018).

**Why it might work.** Risk (distress, illiquidity; Fama & French 1993) or mispricing; much of the historical premium came from the smallest, least liquid stocks and January.

| Rule | Original (Banz (1981)) | This factsheet |
|---|---|---|
| Signal | Market capitalisation | US: market cap (Sharadar). Elsewhere: 63-day average traded value (price × volume), a proxy |
| Portfolio | Size deciles or SMB (2×3) | Extreme quantile L/S within the universe, monthly |
| Weighting | Value weighted | Equal weighted |

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

- **Data gap:** No shares outstanding outside the US: size is proxied by traded value, which also measures liquidity and turnover.
- **Data gap:** The universes are blue chips; the classic size premium lives in micro and small caps, which are excluded by construction.

## 4. Signal creation

SIZE<sub>i,t</sub> = log market cap (US) or log 63-day average traded value (elsewhere) at month-end t; World ranks within each region first. Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = smallest names in the universe minus largest names; **long-only** = smallest names in the universe; benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (top 500, point-in-time)**, median 503 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +0.4% | -0.3% | 11.7% | 0.04 [-0.40, 0.50] | -0.03 | -39% | 50% | 0.17 | 0.41 | -5.5% (-1.7) | 6.9% |
| Long-only (net) | +15.4% | +14.3% | 20.0% | 0.77 [0.37, 1.34] | 1.14 | -38% | 65% | 4.01 | 1.25 | -2.6% (-1.3) | 11.4% |
| Smallest names in the universe (gross) | +16.0% | +14.9% | 20.0% | 0.80 [0.39, 1.38] | 1.20 | -38% | 65% | 4.16 | 1.25 | -2.1% (-1.0) | 11.3% |
| Largest names (gross) | +14.7% | +14.6% | 13.8% | 1.06 [0.62, 1.60] | 1.78 | -25% | 68% | 5.37 | 0.84 | +2.5% (1.8) | 7.7% |
| EW universe | +14.5% | +14.2% | 15.1% | 0.96 [0.52, 1.53] | 1.52 | -25% | 67% | 4.79 | 1.00 | – | 8.9% |
| Size-weighted universe | +15.4% | +15.3% | 14.4% | 1.07 [0.61, 1.64] | 1.79 | -24% | 69% | 5.27 | 0.90 | +2.3% (1.8) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 236 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -2.2% | -2.9% | 11.9% | -0.18 [-0.76, 0.29] | -0.37 | -46% | 44% | -0.64 | 0.12 | -3.6% (-1.0) | 5.7% |
| Long-only (net) | +9.5% | +8.4% | 16.6% | 0.57 [0.13, 1.08] | 0.85 | -30% | 59% | 2.37 | 1.00 | -2.0% (-0.8) | 9.1% |
| Smallest names in the universe (gross) | +9.6% | +8.6% | 16.6% | 0.58 [0.14, 1.09] | 0.87 | -30% | 59% | 2.41 | 1.00 | -1.8% (-0.8) | 9.1% |
| Largest names (gross) | +11.3% | +10.7% | 14.3% | 0.79 [0.31, 1.36] | 1.19 | -28% | 64% | 3.24 | 0.87 | +1.3% (0.6) | 8.6% |
| EW universe | +11.4% | +10.9% | 14.6% | 0.78 [0.33, 1.33] | 1.22 | -26% | 64% | 3.33 | 1.00 | – | 8.4% |
| Size-weighted universe | +10.7% | +10.1% | 14.3% | 0.75 [0.28, 1.28] | 1.14 | -26% | 60% | 3.12 | 0.95 | -0.1% (-0.1) | 8.3% |

**UK (FTSE 350, point-in-time)**, median 242 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +4.9% | +4.4% | 10.9% | 0.45 [-0.24, 1.20] | 0.65 | -51% | 53% | 1.43 | 0.20 | +2.9% (0.7) | 5.6% |
| Long-only (net) | +15.6% | +15.5% | 14.7% | 1.06 [0.52, 1.81] | 1.79 | -26% | 67% | 4.32 | 0.93 | +5.8% (3.0) | 8.3% |
| Smallest names in the universe (gross) | +15.9% | +15.9% | 14.7% | 1.08 [0.54, 1.84] | 1.84 | -26% | 67% | 4.41 | 0.93 | +6.1% (3.1) | 8.3% |
| Largest names (gross) | +10.3% | +9.9% | 13.2% | 0.78 [0.23, 1.40] | 1.19 | -24% | 63% | 2.93 | 0.74 | +2.6% (0.9) | 7.5% |
| EW universe | +10.6% | +10.0% | 14.2% | 0.74 [0.26, 1.35] | 1.08 | -30% | 59% | 3.23 | 1.00 | – | 8.8% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.71 [0.21, 1.31] | 1.01 | -27% | 62% | 2.94 | 0.82 | +0.4% (0.2) | 7.7% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -3.0% | -4.0% | 14.4% | -0.21 [-0.71, 0.33] | -0.37 | -53% | 47% | -0.79 | 0.08 | -4.0% (-1.0) | 9.1% |
| Long-only (net) | +11.8% | +10.6% | 18.3% | 0.64 [0.13, 1.28] | 0.85 | -42% | 58% | 2.52 | 1.05 | -1.7% (-0.6) | 11.9% |
| Smallest names in the universe (gross) | +12.0% | +10.8% | 18.3% | 0.66 [0.14, 1.29] | 0.87 | -42% | 58% | 2.57 | 1.05 | -1.5% (-0.6) | 11.9% |
| Largest names (gross) | +14.5% | +13.7% | 17.7% | 0.82 [0.30, 1.39] | 1.32 | -29% | 61% | 3.18 | 0.97 | +1.9% (0.8) | 9.7% |
| EW universe | +12.9% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.26 | -33% | 64% | 3.21 | 1.00 | – | 9.3% |
| Size-weighted universe | +11.2% | +10.3% | 16.6% | 0.68 [0.11, 1.32] | 0.94 | -40% | 61% | 2.52 | 0.91 | -0.6% (-0.2) | 10.8% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.7% | +2.2% | 10.7% | 0.25 [-0.22, 0.72] | 0.31 | -33% | 53% | 1.07 | 0.09 | +1.5% (0.6) | 5.9% |
| Long-only (net) | +14.9% | +14.4% | 16.4% | 0.91 [0.42, 1.46] | 1.47 | -26% | 60% | 3.80 | 1.05 | +1.4% (0.8) | 9.4% |
| Smallest names in the universe (gross) | +15.0% | +14.5% | 16.4% | 0.91 [0.42, 1.47] | 1.48 | -26% | 60% | 3.82 | 1.05 | +1.5% (0.9) | 9.4% |
| Largest names (gross) | +11.8% | +11.2% | 14.6% | 0.80 [0.35, 1.35] | 1.19 | -26% | 66% | 3.59 | 0.96 | -0.5% (-0.3) | 9.2% |
| EW universe | +12.8% | +12.5% | 14.1% | 0.91 [0.39, 1.54] | 1.42 | -29% | 67% | 3.62 | 1.00 | – | 8.3% |
| Size-weighted universe | +11.2% | +10.7% | 13.9% | 0.80 [0.31, 1.37] | 1.21 | -27% | 63% | 3.26 | 0.95 | -1.0% (-0.9) | 8.6% |

**World (US + UK + EU, point-in-time)**, median 979 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +0.2% | -0.1% | 7.6% | 0.02 [-0.53, 0.56] | -0.03 | -33% | 50% | 0.07 | 0.26 | -3.1% (-1.5) | 4.4% |
| Long-only (net) | +12.8% | +11.7% | 18.2% | 0.70 [0.25, 1.26] | 1.02 | -34% | 63% | 3.03 | 1.12 | -1.3% (-1.0) | 10.7% |
| Smallest names in the universe (gross) | +13.1% | +12.1% | 18.2% | 0.72 [0.27, 1.29] | 1.06 | -34% | 63% | 3.12 | 1.12 | -1.0% (-0.7) | 10.7% |
| Largest names (gross) | +12.2% | +11.9% | 14.0% | 0.87 [0.39, 1.46] | 1.36 | -27% | 67% | 3.80 | 0.86 | +1.4% (1.2) | 8.4% |
| EW universe | +12.6% | +12.0% | 15.7% | 0.80 [0.33, 1.38] | 1.20 | -29% | 64% | 3.53 | 1.00 | – | 9.4% |
| Size-weighted universe | +11.4% | +10.8% | 15.0% | 0.76 [0.29, 1.33] | 1.14 | -28% | 63% | 3.23 | 0.94 | -0.4% (-0.5) | 9.0% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +1.7% | +5.8% | +27.9% | -0.1% | +4.0% | +11.3% |
| 2014 | +4.7% | -12.1% | +16.8% | -12.4% | -0.1% | -4.7% |
| 2015 | -3.5% | -2.6% | +26.0% | -22.5% | +4.6% | +3.6% |
| 2016 | +9.7% | -5.0% | +3.5% | +2.3% | +15.7% | +7.0% |
| 2017 | +3.5% | +1.4% | +30.7% | +14.0% | +0.5% | +9.3% |
| 2018 | +1.1% | -2.5% | +17.5% | +15.1% | +7.5% | -0.6% |
| 2019 | +6.0% | -3.0% | +11.0% | -23.9% | +14.1% | +5.3% |
| 2020 | -0.6% | -10.1% | +9.5% | -20.6% | +8.0% | +0.2% |
| 2021 | +1.9% | -12.4% | -8.1% | +11.0% | -8.1% | -6.4% |
| 2022 | +6.8% | +12.4% | -19.2% | -12.5% | -3.1% | +1.1% |
| 2023 | -1.6% | -2.4% | -4.3% | +1.5% | -11.6% | -0.4% |
| 2024 | -7.7% | -3.6% | -14.6% | +10.5% | -10.7% | -11.4% |
| 2025 | -13.5% | +7.3% | -13.8% | +2.3% | +14.8% | -6.2% |
| 2026 | -9.2% | -8.5% | -5.3% | -6.3% | -0.8% | -6.8% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +28.2% | +24.6% | +37.0% | +34.1% | +18.7% | +34.1% |
| 2014 | +18.8% | -3.6% | +12.3% | +13.4% | +11.3% | -1.7% |
| 2015 | +0.3% | +8.5% | +12.1% | +10.5% | +11.6% | +2.0% |
| 2016 | +19.8% | +19.7% | +42.9% | +12.4% | +39.3% | +19.3% |
| 2017 | +23.2% | +14.2% | +48.2% | +20.8% | +13.8% | +33.5% |
| 2018 | -0.7% | -11.5% | +7.9% | -7.4% | -1.7% | -9.3% |
| 2019 | +35.0% | +27.0% | +31.6% | -0.5% | +43.8% | +31.6% |
| 2020 | +14.8% | -5.0% | +2.8% | +13.9% | +22.1% | +11.1% |
| 2021 | +29.5% | +7.3% | +12.1% | +31.2% | +18.4% | +12.7% |
| 2022 | -11.4% | -0.9% | -11.5% | -18.4% | -11.5% | -13.9% |
| 2023 | +19.6% | +8.6% | +4.5% | +7.2% | +2.9% | +18.9% |
| 2024 | +12.8% | +2.5% | +2.8% | +3.7% | -4.0% | +2.0% |
| 2025 | +3.7% | +28.2% | +16.4% | +23.8% | +31.1% | +23.6% |
| 2026 | +10.2% | +4.1% | +7.2% | +10.8% | +13.7% | +8.6% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS07_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 23% | 4% | 50% | -19.7% | 2020-03 |
| EU | 163 | 24 / 23 | 6% | 6% | 44% | -9.0% | 2020-07 |
| UK | 163 | 25 / 24 | 13% | 4% | 53% | -9.6% | 2022-01 |
| DK | 163 | 7 / 6 | 9% | 4% | 47% | -14.3% | 2020-03 |
| SCANDI | 163 | 13 / 12 | 4% | 6% | 53% | -9.1% | 2024-10 |
| World | 163 | 98 / 97 | 16% | 5% | 50% | -11.8% | 2020-03 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: smallest names in the universe | Short: largest names |
|---|---|---|
| US | AAL, VIAV, APTV, WYNN, PNR, ZION, AYI, FRT | NVDA, AAPL, GOOGL, MSFT, AMZN, AVGO, META, TSLA |
| EU | NYR.BR, OBEL.BR, AGFB.BR, GTC.WA, KER.WA, TESB.BR, BPOST.BR, ONTEX.BR | NOVO-B.CO, ASML.AS, VOLV-B.ST, INVE-B.ST, ERIC-B.ST, SAAB-B.ST, AZN.ST, ATCO-A.ST |
| UK | RTW.L, BPCR.L, PEY.L, MNTN.L, MTLN.L, HANA.L, PRN.L, NAS.L | AZN.L, HSBA.L, RR.L, SHEL.L, GLEN.L, AAL.L, RIO.L, BP.L |
| DK | NDA-DK.CO, BAVA.CO, GN.CO, RBREW.CO, AMBU-B.CO, ISS.CO, MAERSK-A.CO, JYSK.CO | NOVO-B.CO, DSV.CO, VWS.CO, MAERSK-B.CO, DANSKE.CO, NSIS-B.CO, GMAB.CO, PNDORA.CO |
| SCANDI | KALMAR.HE, QTCOM.HE, KEMIRA.HE, HIAB.HE, TYRES.HE, TIETO.HE, MANTA.HE, HUH1V.HE | NOVO-B.CO, VOLV-B.ST, INVE-B.ST, ERIC-B.ST, SAAB-B.ST, AZN.ST, ATCO-A.ST, DSV.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -1.6% | -0.78 | 0.59 | mkt +0.25 (+3.6), size +0.43 (+3.2), value +0.44 (+4.3), short_term_reversal +0.44 (+2.2) |
| EU | French Europe 5F + WML | -2.0% | -0.64 | 0.21 | SMB +0.49 (+3.7), HML +0.36 (+2.2) |
| UK | JKP GBR 7 themes | +6.4% | 2.07 | 0.39 | size +0.94 (+6.9), value -0.53 (-3.1), momentum -0.23 (-2.0), quality +0.41 (+2.1) |
| DK | JKP DNK 7 themes | -5.4% | -1.35 | 0.15 | size +0.49 (+3.0), low_risk +0.32 (+2.1) |
| SCANDI | French Europe 5F + WML | +1.7% | 0.70 | 0.06 | none &#124;t&#124; ≥ 2 |
| World | JKP World 7 themes | -4.1% | -2.06 | 0.44 | mkt +0.15 (+4.2), size +0.52 (+4.3), value +0.27 (+3.0), short_term_reversal +0.26 (+2.2) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +3.3% | 2.47 | 0.93 | mkt +1.10 (+23.6), value +0.38 (+4.1), quality +0.24 (+2.1), short_term_reversal +0.47 (+2.8) |
| EU | French Europe 5F + WML | +4.4% | 1.73 | 0.64 | Mkt-RF +0.71 (+10.5), HML +0.39 (+2.3) |
| UK | JKP GBR 7 themes | +13.1% | 4.34 | 0.69 | mkt +0.51 (+7.6), low_risk -0.49 (-3.0) |
| DK | JKP DNK 7 themes | +2.7% | 0.69 | 0.62 | mkt +0.76 (+9.9), value +0.27 (+2.9), low_risk -0.28 (-2.6) |
| SCANDI | French Europe 5F + WML | +9.1% | 3.01 | 0.51 | Mkt-RF +0.72 (+8.8) |
| World | JKP World 7 themes | +4.7% | 1.74 | 0.83 | mkt +0.80 (+14.4), value +0.33 (+3.1) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 4 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -5.5% to +2.9%, |t| past the gate in 0 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 1 of the six; alpha -2.6% to +5.8%, passing in 1 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.55, EU 0.26, UK 0.95, DK 0.22, SCANDI 0.82, World 0.53.
- **Publication decay:** gross L/S -3.8% to +18.6% a year in 2013–19 against -7.9% to -1.0% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +4.4% | 0.25 | +3.5% | +0.9% | -0.7% | +3.6% | +0.8% | 30% | 2015-07 -5%, 2015-09 -4%, 2014-09 -4% |
| EU | -1.9% | -0.01 | -0.1% | -1.8% | -0.3% | -0.6% | -1.2% | 13% | 2014-05 -6%, 2019-02 -4%, 2014-10 -4% |
| UK | +18.6% | -0.10 | -1.4% | +19.9% | -0.4% | +11.4% | +7.2% | 16% | 2016-06 -6%, 2019-03 -4%, 2016-09 -3% |
| DK | -3.8% | -0.02 | -0.3% | -3.5% | -0.3% | -3.2% | -0.6% | 14% | 2014-02 -9%, 2019-05 -9%, 2015-02 -8% |
| SCANDI | +7.3% | 0.05 | +0.8% | +6.5% | -0.3% | +2.9% | +4.3% | 11% | 2017-02 -4%, 2018-09 -4%, 2019-04 -4% |
| World | +5.2% | 0.17 | +2.2% | +3.0% | -0.5% | +2.6% | +2.6% | 22% | 2016-06 -3%, 2018-09 -2%, 2014-07 -2% |

On average across the six universes the gross spread was +5.0% a year, of which the market exposure (beta +0.06) contributed +0.8%; the beta-adjusted spread (CAPM alpha) was +4.2%. Costs took 0.4% a year at 17% monthly turnover across both legs. The long leg beat the universe by +2.8% and the short leg lagged it by +2.2% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages -1.3%, -1.9%, -2.1% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.55 | – | -0.44 | – | – | -3.4% | -28% | -6.2% (-2.2) | 0.4% |
| X1 beta-neutral legs | 0.65 | +0.38 (p 0.029) | -0.66 | -0.23 (p 0.979) | 1 of 6 | -5.4% | -35% | -7.6% (-2.4) | 0.5% |
| X2 + turnover buffer | 0.69 | +0.06 (p 0.379) | -0.25 | +0.41 (p 0.061) | 5 of 6 | -1.4% | -17% | -2.6% (-1.2) | 0.2% |
| X3 + volatility targeting | 0.63 | -0.22 (p 0.718) | -0.45 | -0.20 (p 0.963) | 1 of 6 | -3.7% | -24% | -5.9% (-1.7) | 0.1% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS07_ladder.png)

- **X1 beta-neutral legs:** +0.38 design, -0.23 holdout; helps in one window and hurts in the other: not reliable.
- **X2 + turnover buffer:** +0.06 design, +0.41 holdout; helps in both windows but does not pass the gate.
- **X3 + volatility targeting:** -0.22 design, -0.20 holdout; hurts in both windows.

**Where it ends:** holdout Sharpe -0.44 → -0.45, return -3.4% → -3.7% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Size |
|---|---|
| Series family | **Size** |
| Academic style | Size premium (Fama-French SMB) |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 17% of the two legs replaced monthly |
| Market exposure | L/S beta 0.08 to 0.41 |
| Payoff shape | Treynor–Mazuy γ -2.04 to 1.84 (t -2.0 to 1.1); worst 10% of market months -2.5% to -0.4% a month, best 10% -0.5% to +2.6% |
| Nearest factor theme | mkt (2 of 6 universes), HML (1 of 6 universes) |
| Nearest library signals (returns) | Near 52-week high (3 universes), 55-day breakout (3 universes), Momentum 12-1 (2 universes) |
| Economic rationale | Risk (distress, illiquidity; Fama & French 1993) or mispricing; much of the historical premium came from the smallest, least liquid stocks and January. |
| Publication | Banz 1981; Fama & French 1992–93; 'Is size dead?' (van Dijk 2011); 'Size matters, if you control your junk' (Asness et al. 2018) |
| Where it fits | In the **momentum** cluster of the library; fully explained by its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Idiosyncratic vol**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Size **(this strategy)** | size | +1.00 | +1.00 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Near 52-week high | momentum | +0.07 | +0.31 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| 55-day breakout | momentum | +0.04 | +0.27 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Momentum 12-1 | momentum | +0.08 | +0.25 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Volatility (252 days) | low risk | -0.05 | -0.24 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| MIN5 | low risk | +0.02 | +0.23 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| MIN (worst day) | low risk | +0.01 | +0.22 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| Volatility | low risk | -0.02 | -0.22 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Last month return | short-term reversal | +0.02 | +0.21 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Beta | low risk | +0.04 | -0.21 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| Range (MAX−MIN) | low risk | +0.00 | -0.20 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| Idiosyncratic vol (mirror) | low risk | -0.01 | -0.19 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| MAX (best day) | low risk | +0.01 | -0.14 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| MAX5 | low risk | +0.01 | -0.14 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| Above 52-week low | momentum | +0.05 | +0.14 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.01 | +0.12 | -1.0% | -5.3% to +4.2% | 0 / 0 |
| Residual momentum | momentum | +0.01 | +0.11 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| Same-month seasonality | seasonality | +0.07 | +0.02 | -1.8% | -8.5% to +7.2% | 0 / 0 |
| Skewness | tail direction | -0.00 | -0.01 | -0.2% | -5.4% to +4.5% | 0 / 1 |

![360 map](../figures/xs_FS07_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | +0.8% | 0.32 | 0.53 | Momentum 12-1 +0.23 (+3.6) |
| EU | -1.5% | -0.47 | 0.15 |  |
| UK | -2.1% | -0.61 | 0.12 | Same-month seasonality -0.15 (-3.1) |
| DK | +1.6% | 0.45 | 0.15 | Momentum 12-1 +0.29 (+2.1), Residual momentum -0.15 (-2.0) |
| SCANDI | +0.9% | 0.32 | 0.12 | Net tail +0.19 (+2.3), Same-month seasonality -0.20 (-2.4) |
| World | +1.1% | 0.58 | 0.43 |  |

![Double sort](../figures/xs_FS07_dsort.png)

Holding Idiosyncratic vol fixed (down a column), moving from low to high Size changes the return by -0.6, -1.6 and -2.4 points a year; holding Size fixed (along a row), moving from low to high Idiosyncratic vol changes it by +0.5, +1.0 and -1.3.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -6% vs +7% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages -1.5%, -1.3%, -1.9%, -2.1% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Data gap.** No shares outstanding outside the US: size is proxied by traded value, which also measures liquidity and turnover.
5. **Data gap.** The universes are blue chips; the classic size premium lives in micro and small caps, which are excluded by construction.
6. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- Banz, R. (1981). The relationship between return and market value of common stocks. *Journal of Financial Economics*, 9(1), 3–18.
- Fama, E. & French, K. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33(1), 3–56.
- van Dijk, M. (2011). Is size dead? A review of the size effect in equity returns. *Journal of Banking & Finance*, 35(12), 3263–3274.
- Asness, C., Frazzini, A., Israel, R., Moskowitz, T. & Pedersen, L. H. (2018). Size matters, if you control your junk. *Journal of Financial Economics*, 129(3), 479–509.
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

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS07` → `build_xs.py FS07`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
