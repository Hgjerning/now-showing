# FACTSHEET FS09 · 52-week high

### Do stocks near their high keep going?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Anchoring momentum</div>
<div><b>Origin</b>George & Hwang (2004)</div>
<div><b>Family</b>Momentum & trend</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (stocks closest to their 52-week high)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Stocks trading close to their 52-week high outperform those far below it, and this nearness explains much of momentum. George & Hwang (2004) found it for US stocks 1963–2001; investors anchor on the high and under-react to good news near it. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -5.9% to +5.8% a year and was positive in 2 of the six; no universe passes the 2.87 gate. The long-only book (stocks closest to their 52-week high) had a higher Sharpe than the equal-weight universe in 5 of the six (EU, UK, DK, SCANDI, World), with alphas of -0.1% to +6.1%, passing the gate in EU, DK. **What goes wrong (§10):** the main drags are a market bet (average beta -0.61, worth -8.0% a year in 2013–19), costs of about 2.1% a year. None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Momentum & trend; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours 55-day breakout, MIN5; after its closest neighbours and the market it keeps an alpha of -2.1% to +3.6% (largest |t| 2.6), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 501 / 10 | -5.9% | -1.19 | +5.3% (1.4) | -0.77 | +9.8% | 0.79 | -20% | +14.1% | 0.95 | +15.3% |
| EU | 238 / 10 | +4.3% | 0.84 | +15.2% (4.0) | -0.95 | +13.2% | 1.21 | -21% | +10.9% | 0.78 | +10.1% |
| UK | 239 / 10 | -0.8% | -0.13 | +9.6% (2.0) | -1.00 | +9.7% | 0.93 | -20% | +9.9% | 0.74 | +8.5% |
| DK | 19 / 3 | +5.8% | 1.39 | +11.1% (2.8) | -0.42 | +16.6% | 1.09 | -33% | +12.3% | 0.82 | +10.3% |
| SCANDI | 62 / 5 | -1.6% | -0.44 | +5.4% (1.7) | -0.55 | +13.3% | 1.05 | -23% | +12.5% | 0.91 | +10.7% |
| World | 971 / 10 | -4.0% | -0.78 | +6.5% (1.9) | -0.84 | +9.6% | 0.80 | -21% | +11.9% | 0.80 | +10.8% |

*Monthly, local currency (World in USD). L/S = equal-weighted stocks closest to their 52-week high minus stocks furthest below it, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS09_growth.png)

## 2. Strategy description

Stocks trading close to their 52-week high outperform those far below it, and this nearness explains much of momentum. George & Hwang (2004) found it for US stocks 1963–2001; investors anchor on the high and under-react to good news near it.

**Why it might work.** Anchoring: traders use the 52-week high as a reference and are reluctant to bid prices above it, so good news is absorbed slowly (George & Hwang 2004).

| Rule | Original (George & Hwang (2004)) | This factsheet |
|---|---|---|
| Signal | Price / 52-week high | Total-return price / 252-day high at month-end t |
| Portfolio | Top 30% minus bottom 30%, 6-month holding | Extreme quantile L/S, one-month holding |
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

- **Data gap:** We hold for one month; George & Hwang hold for six. A longer holding period would cut turnover.

## 4. Signal creation

HI52<sub>i,t</sub> = P<sub>i,t</sub> / max(P<sub>i,t−251..t</sub>). Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = stocks closest to their 52-week high minus stocks furthest below it; **long-only** = stocks closest to their 52-week high; benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (top 500, point-in-time)**, median 501 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -5.9% | -8.0% | 21.5% | -0.28 [-0.71, 0.15] | -0.47 | -72% | 47% | -1.19 | -0.77 | +5.3% (1.4) | 16.5% |
| Long-only (net) | +10.2% | +9.8% | 12.9% | 0.79 [0.37, 1.25] | 1.26 | -20% | 58% | 3.97 | 0.72 | -0.1% (-0.1) | 7.6% |
| Stocks closest to their 52-week high (gross) | +12.0% | +11.7% | 12.9% | 0.93 [0.50, 1.40] | 1.55 | -19% | 60% | 4.63 | 0.71 | +1.7% (1.1) | 7.4% |
| Stocks furthest below it (gross) | +14.4% | +11.7% | 26.0% | 0.56 [0.13, 1.09] | 0.73 | -43% | 61% | 2.50 | 1.49 | -7.1% (-2.4) | 14.6% |
| EW universe | +14.4% | +14.1% | 15.1% | 0.95 [0.52, 1.53] | 1.52 | -25% | 68% | 4.79 | 1.00 | – | 8.9% |
| Size-weighted universe | +15.4% | +15.3% | 14.4% | 1.07 [0.61, 1.64] | 1.79 | -24% | 69% | 5.27 | 0.90 | +2.4% (1.8) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +4.3% | +1.7% | 21.8% | 0.20 [-0.23, 0.73] | 0.10 | -50% | 54% | 0.84 | -0.95 | +15.2% (4.0) | 14.3% |
| Long-only (net) | +13.0% | +13.2% | 10.8% | 1.21 [0.66, 1.85] | 2.20 | -21% | 64% | 4.63 | 0.61 | +6.1% (3.9) | 5.8% |
| Stocks closest to their 52-week high (gross) | +14.6% | +15.0% | 10.8% | 1.36 [0.80, 2.01] | 2.58 | -20% | 66% | 5.17 | 0.61 | +7.7% (4.8) | 5.7% |
| Stocks furthest below it (gross) | +7.3% | +4.1% | 26.0% | 0.28 [-0.17, 0.70] | 0.27 | -41% | 50% | 1.16 | 1.56 | -10.5% (-3.7) | 13.0% |
| EW universe | +11.4% | +10.9% | 14.5% | 0.78 [0.33, 1.33] | 1.22 | -26% | 64% | 3.34 | 1.00 | – | 8.3% |
| Size-weighted universe | +10.7% | +10.1% | 14.3% | 0.75 [0.28, 1.28] | 1.14 | -26% | 60% | 3.12 | 0.95 | -0.2% (-0.1) | 8.3% |

**UK (FTSE 350, point-in-time)**, median 239 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -0.8% | -3.8% | 24.0% | -0.03 [-0.50, 0.48] | -0.21 | -70% | 58% | -0.13 | -1.00 | +9.6% (2.0) | 17.1% |
| Long-only (net) | +9.8% | +9.7% | 10.6% | 0.93 [0.44, 1.49] | 1.46 | -20% | 61% | 3.77 | 0.59 | +3.7% (1.9) | 6.4% |
| Stocks closest to their 52-week high (gross) | +11.5% | +11.5% | 10.6% | 1.09 [0.58, 1.66] | 1.79 | -17% | 63% | 4.39 | 0.59 | +5.3% (2.7) | 6.3% |
| Stocks furthest below it (gross) | +9.4% | +6.0% | 27.1% | 0.35 [-0.12, 0.84] | 0.37 | -46% | 53% | 1.35 | 1.58 | -7.2% (-1.9) | 14.9% |
| EW universe | +10.5% | +9.9% | 14.1% | 0.74 [0.26, 1.34] | 1.08 | -29% | 60% | 3.23 | 1.00 | – | 8.8% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.71 [0.21, 1.31] | 1.01 | -27% | 62% | 2.94 | 0.82 | +0.4% (0.2) | 7.7% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +5.8% | +4.3% | 17.6% | 0.33 [-0.13, 0.80] | 0.38 | -36% | 55% | 1.39 | -0.42 | +11.1% (2.8) | 9.4% |
| Long-only (net) | +16.6% | +16.6% | 15.2% | 1.09 [0.53, 1.68] | 1.96 | -33% | 63% | 4.01 | 0.83 | +6.0% (3.1) | 7.8% |
| Stocks closest to their 52-week high (gross) | +17.3% | +17.5% | 15.2% | 1.14 [0.57, 1.74] | 2.08 | -32% | 63% | 4.17 | 0.83 | +6.7% (3.5) | 7.8% |
| Stocks furthest below it (gross) | +9.6% | +7.4% | 22.1% | 0.44 [-0.07, 1.03] | 0.49 | -45% | 60% | 1.67 | 1.24 | -6.4% (-2.6) | 14.4% |
| EW universe | +12.8% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.25 | -33% | 64% | 3.20 | 1.00 | – | 9.3% |
| Size-weighted universe | +11.2% | +10.3% | 16.6% | 0.68 [0.11, 1.32] | 0.94 | -40% | 61% | 2.52 | 0.92 | -0.5% (-0.2) | 10.8% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -1.6% | -2.8% | 15.8% | -0.10 [-0.56, 0.34] | -0.25 | -49% | 47% | -0.44 | -0.55 | +5.4% (1.7) | 9.1% |
| Long-only (net) | +13.4% | +13.3% | 12.8% | 1.05 [0.52, 1.63] | 1.77 | -23% | 67% | 4.15 | 0.78 | +3.3% (2.3) | 6.8% |
| Stocks closest to their 52-week high (gross) | +14.5% | +14.6% | 12.8% | 1.14 [0.60, 1.73] | 1.98 | -22% | 68% | 4.48 | 0.78 | +4.5% (3.1) | 6.7% |
| Stocks furthest below it (gross) | +13.7% | +12.1% | 21.1% | 0.65 [0.15, 1.21] | 0.92 | -44% | 58% | 2.63 | 1.33 | -3.4% (-1.5) | 12.4% |
| EW universe | +12.8% | +12.5% | 14.1% | 0.91 [0.39, 1.54] | 1.42 | -29% | 67% | 3.62 | 1.00 | – | 8.3% |
| Size-weighted universe | +11.2% | +10.7% | 13.9% | 0.80 [0.31, 1.37] | 1.21 | -27% | 63% | 3.26 | 0.95 | -1.0% (-0.9) | 8.6% |

**World (US + UK + EU, point-in-time)**, median 971 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -4.0% | -6.1% | 20.6% | -0.20 [-0.63, 0.26] | -0.37 | -68% | 51% | -0.78 | -0.84 | +6.5% (1.9) | 15.3% |
| Long-only (net) | +9.9% | +9.6% | 12.4% | 0.80 [0.35, 1.33] | 1.23 | -21% | 62% | 3.83 | 0.68 | +1.4% (1.1) | 7.7% |
| Stocks closest to their 52-week high (gross) | +11.6% | +11.4% | 12.4% | 0.94 [0.48, 1.48] | 1.52 | -20% | 63% | 4.46 | 0.68 | +3.1% (2.4) | 7.6% |
| Stocks furthest below it (gross) | +12.5% | +9.5% | 26.3% | 0.47 [0.03, 0.97] | 0.60 | -43% | 56% | 1.96 | 1.52 | -6.6% (-2.7) | 14.1% |
| EW universe | +12.5% | +11.9% | 15.7% | 0.80 [0.33, 1.38] | 1.20 | -29% | 64% | 3.53 | 1.00 | – | 9.4% |
| Size-weighted universe | +11.4% | +10.8% | 15.0% | 0.76 [0.29, 1.33] | 1.14 | -28% | 63% | 3.23 | 0.94 | -0.4% (-0.5) | 9.0% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -2.0% | -7.2% | +15.3% | -4.9% | +3.9% | +0.9% |
| 2014 | +0.8% | +25.3% | +0.6% | +6.4% | -2.4% | +8.7% |
| 2015 | +11.3% | +22.5% | +29.7% | +11.7% | +13.7% | +11.6% |
| 2016 | -27.4% | -10.3% | -45.9% | -18.1% | -12.8% | -27.9% |
| 2017 | -1.4% | -6.7% | -7.9% | +2.1% | -4.5% | -7.5% |
| 2018 | +4.2% | +10.3% | -10.2% | +11.5% | +3.5% | -1.2% |
| 2019 | -18.8% | -13.2% | -6.4% | +18.6% | -17.9% | -13.4% |
| 2020 | -20.2% | -24.3% | -13.5% | +19.0% | -12.7% | -21.8% |
| 2021 | -21.4% | -4.3% | -12.3% | -4.0% | -14.8% | -14.0% |
| 2022 | +24.6% | -3.1% | +28.4% | +1.3% | +15.4% | +11.7% |
| 2023 | -32.5% | +2.0% | -7.5% | -18.6% | -11.7% | -21.8% |
| 2024 | +14.6% | +10.9% | -0.0% | +7.4% | +8.2% | +11.6% |
| 2025 | -15.5% | +29.8% | +26.1% | +31.9% | +18.1% | +2.8% |
| 2026 | -5.1% | +6.6% | -18.1% | +6.2% | -14.5% | -10.0% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +26.0% | +21.3% | +22.6% | +43.2% | +33.3% | +27.2% |
| 2014 | +14.9% | +7.6% | +4.1% | +17.9% | +12.3% | +7.3% |
| 2015 | -2.2% | +17.2% | +15.6% | +25.7% | +27.7% | -0.2% |
| 2016 | +1.4% | +15.2% | +5.9% | +1.1% | +24.4% | +0.6% |
| 2017 | +11.2% | +7.7% | +17.5% | +19.7% | +17.4% | +19.0% |
| 2018 | -1.7% | +5.1% | -10.1% | +0.2% | -3.3% | -7.9% |
| 2019 | +18.1% | +15.3% | +7.6% | +35.3% | +19.7% | +18.8% |
| 2020 | +18.6% | +9.1% | +14.1% | +55.7% | +16.2% | +17.0% |
| 2021 | +24.8% | +19.6% | +13.9% | +23.3% | +11.1% | +15.6% |
| 2022 | -9.9% | -13.3% | -3.7% | -20.0% | -9.7% | -11.6% |
| 2023 | +1.5% | +18.9% | +6.8% | +1.6% | +4.6% | +5.8% |
| 2024 | +21.1% | +3.1% | +7.3% | +9.6% | +3.4% | +13.4% |
| 2025 | +7.8% | +43.5% | +32.2% | +23.4% | +25.3% | +26.2% |
| 2026 | +8.8% | +17.9% | +4.2% | +10.1% | +7.3% | +7.1% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS09_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 73% | 28% | 47% | -23.2% | 2020-04 |
| EU | 163 | 24 / 23 | 66% | 22% | 54% | -42.2% | 2020-11 |
| UK | 163 | 24 / 23 | 69% | 23% | 58% | -40.7% | 2020-11 |
| DK | 163 | 7 / 6 | 30% | 21% | 55% | -12.9% | 2023-11 |
| SCANDI | 163 | 13 / 12 | 48% | 24% | 47% | -12.6% | 2020-11 |
| World | 163 | 98 / 97 | 71% | 26% | 51% | -34.8% | 2020-11 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks closest to their 52-week high | Short: stocks furthest below it |
|---|---|---|
| US | MPC, SLB, VLO, DINO, CRWD, PSX, GEN, UNM | CSGP, FISV, PODD, APP, BSX, ORCL, COIN, ZTS |
| EU | SKF-B.ST, RAND.AS, PUIG.MC, PZU.WA, ABN.AS, DSFIR.AS, INGA.BR, JYSK.CO | ONTEX.BR, FCT.MI, AVIO.MI, STLAM.MI, AGFB.BR, STLAP.PA, NYR.BR, UMG.AS |
| UK | VCT.L, AAL.L, ASL.L, RS1.L, CCC.L, BRWM.L, BUT.L, BYIT.L | AML.L, VTY.L, CWR.L, TEP.L, RPI.L, DATA.L, OXB.L, SMWH.L |
| DK | JYSK.CO, NDA-DK.CO, NSIS-B.CO, PNDORA.CO, VWS.CO, DANSKE.CO, ISS.CO, DEMANT.CO | ZEAL.CO, AMBU-B.CO, ORSTED.CO, RBREW.CO, DSV.CO, COLO-B.CO, NOVO-B.CO, GN.CO |
| SCANDI | KESKOB.HE, JYSK.CO, SKF-B.ST, NDA-SE.ST, NDA-DK.CO, NSIS-B.CO, NDA-FI.HE, SHB-A.ST | NOKIA.HE, ORSTED.CO, RBREW.CO, QTCOM.HE, WRT1V.HE, AMBU-B.CO, DSV.CO, ERIC-B.ST |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -9.9% | -5.58 | 0.84 | size +0.25 (+2.2), value -0.41 (-2.4), momentum +1.04 (+5.7), low_risk +1.28 (+6.3), quality +0.48 (+2.1), short_term_reversal -1.14 (-6.5) |
| EU | French Europe 5F + WML | -5.3% | -1.54 | 0.64 | Mkt-RF -0.42 (-4.6), RMW +0.58 (+2.4), WML +1.21 (+6.8) |
| UK | JKP GBR 7 themes | -6.8% | -1.55 | 0.76 | momentum +1.08 (+7.6), low_risk +1.57 (+5.2), quality +0.80 (+2.9), short_term_reversal -0.78 (-4.0) |
| DK | JKP DNK 7 themes | -3.5% | -1.30 | 0.58 | momentum +1.04 (+10.6), low_risk +0.59 (+4.6) |
| SCANDI | French Europe 5F + WML | -9.3% | -3.02 | 0.44 | Mkt-RF -0.23 (-3.2), WML +0.85 (+9.2) |
| World | JKP World 7 themes | -5.0% | -1.25 | 0.70 | mkt -0.15 (-2.0), value -0.34 (-2.5), momentum +0.96 (+8.2), low_risk +0.92 (+5.5), short_term_reversal -0.91 (-4.0) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -1.3% | -0.97 | 0.86 | mkt +0.94 (+30.0), momentum +0.34 (+3.5), low_risk +0.39 (+4.5), quality +0.25 (+2.4), short_term_reversal -0.36 (-3.7) |
| EU | French Europe 5F + WML | +5.7% | 2.61 | 0.56 | Mkt-RF +0.53 (+11.4), HML +0.29 (+2.5), WML +0.23 (+4.0) |
| UK | JKP GBR 7 themes | +3.9% | 1.90 | 0.56 | mkt +0.44 (+11.1), value +0.17 (+2.0), momentum +0.33 (+4.1), quality +0.41 (+3.7) |
| DK | JKP DNK 7 themes | +5.3% | 1.85 | 0.66 | mkt +0.75 (+16.9), value +0.17 (+2.8), momentum +0.31 (+3.7), quality +0.23 (+2.4) |
| SCANDI | French Europe 5F + WML | +5.9% | 2.22 | 0.50 | Mkt-RF +0.60 (+11.0), RMW +0.39 (+2.7), WML +0.21 (+2.6) |
| World | JKP World 7 themes | +4.1% | 1.70 | 0.67 | mkt +0.67 (+13.5), momentum +0.30 (+3.2), low_risk +0.31 (+2.8), quality +0.23 (+2.1) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 2 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** +5.3% to +15.2%, |t| past the gate in 1 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 5 of the six; alpha -0.1% to +6.1%, passing in 2 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.15, EU 0.75, UK 0.45, DK 0.89, SCANDI 0.35, World 0.23.
- **Publication decay:** gross L/S -1.8% to +6.7% a year in 2013–19 against -3.9% to +9.1% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | -1.1% | -0.65 | -9.2% | +8.1% | -2.5% | -2.8% | +1.7% | 104% | 2015-04 -13%, 2019-01 -12%, 2019-06 -11% |
| EU | +6.7% | -0.94 | -10.9% | +17.7% | -2.1% | +2.5% | +4.3% | 87% | 2015-02 -13%, 2016-04 -11%, 2016-03 -11% |
| UK | -1.8% | -0.74 | -9.7% | +8.0% | -2.3% | -2.8% | +1.0% | 95% | 2016-02 -19%, 2016-04 -14%, 2015-02 -11% |
| DK | +6.4% | -0.16 | -2.5% | +8.8% | -1.3% | +4.6% | +1.8% | 56% | 2017-08 -8%, 2013-08 -7%, 2016-08 -7% |
| SCANDI | +0.6% | -0.44 | -6.8% | +7.4% | -1.8% | +3.4% | -2.8% | 77% | 2018-07 -9%, 2013-08 -8%, 2019-01 -8% |
| World | -0.7% | -0.75 | -9.1% | +8.4% | -2.4% | -1.7% | +1.0% | 99% | 2016-04 -10%, 2019-01 -10%, 2015-04 -10% |

On average across the six universes the gross spread was +1.7% a year, of which the market exposure (beta -0.61) contributed -8.0%; the beta-adjusted spread (CAPM alpha) was +9.7%. Costs took 2.1% a year at 86% monthly turnover across both legs. The long leg beat the universe by +0.5% and the short leg lagged it by +1.2% a year, so most of the spread comes from the short side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +1.9%, +3.4%, -0.3% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.07 | – | 0.02 | – | – | +0.5% | -39% | +10.0% (2.3) | 2.0% |
| X1 beta-neutral legs | 0.22 | +0.40 (p 0.001) | 0.15 | +0.13 (p 0.203) | 5 of 6 | +2.2% | -33% | +5.4% (1.2) | 2.3% |
| X2 + turnover buffer | 0.37 | +0.20 (p 0.006) | 0.22 | +0.07 (p 0.144) | 4 of 6 | +2.8% | -27% | +5.6% (1.4) | 1.2% |
| X3 + volatility targeting | 0.28 | -0.09 (p 0.582) | 0.59 | +0.36 (p 0.001) ✔ | 6 of 6 | +6.0% | -17% | +8.0% (2.3) | 1.2% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS09_ladder.png)

- **X1 beta-neutral legs:** +0.40 design, +0.13 holdout; helps in both windows but does not pass the gate.
- **X2 + turnover buffer:** +0.20 design, +0.07 holdout; helps in both windows but does not pass the gate.
- **X3 + volatility targeting:** -0.09 design, +0.36 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe 0.02 → 0.59, return +0.5% → +6.0% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | 52-week high |
|---|---|
| Series family | **Momentum & trend** |
| Academic style | Anchoring momentum |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 86% of the two legs replaced monthly |
| Market exposure | L/S beta -1.00 to -0.42 |
| Payoff shape | Treynor–Mazuy γ -4.37 to 1.22 (t -3.0 to 1.2); worst 10% of market months +4.0% to +5.9% a month, best 10% -8.5% to -2.6% |
| Nearest factor theme | momentum (2 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | 55-day breakout (6 universes), MIN5 (4 universes), Volatility (3 universes) |
| Economic rationale | Anchoring: traders use the 52-week high as a reference and are reluctant to bid prices above it, so good news is absorbed slowly (George & Hwang 2004). |
| Publication | George & Hwang 2004 |
| Where it fits | In the **momentum** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Above 52-week low**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Near 52-week high **(this strategy)** | momentum | +1.00 | +1.00 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| 55-day breakout | momentum | +0.73 | +0.83 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Momentum 12-1 | momentum | +0.57 | +0.77 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| MIN5 | low risk | +0.57 | +0.76 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| Volatility | low risk | -0.47 | -0.74 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Volatility (252 days) | low risk | -0.43 | -0.70 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| MIN (worst day) | low risk | +0.48 | +0.70 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| Range (MAX−MIN) | low risk | -0.38 | -0.69 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| Beta | low risk | -0.28 | -0.65 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| Idiosyncratic vol | low risk | -0.36 | -0.58 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| MAX (best day) | low risk | -0.17 | -0.55 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| MAX5 | low risk | -0.17 | -0.52 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| Last month return | short-term reversal | +0.44 | +0.51 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Residual momentum | momentum | +0.30 | +0.47 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| Above 52-week low (mirror) | momentum | +0.50 | +0.46 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Size | size | +0.07 | +0.31 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.25 | +0.17 | -1.0% | -5.3% to +4.2% | 0 / 0 |
| Same-month seasonality | seasonality | +0.01 | +0.08 | -1.8% | -8.5% to +7.2% | 0 / 0 |
| Skewness | tail direction | +0.13 | -0.03 | -0.2% | -5.4% to +4.5% | 0 / 1 |

![360 map](../figures/xs_FS09_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with |t| ≥ 2 |
|---|---|---|---|---|
| US | -1.6% | -1.22 | 0.94 | 55-day breakout +0.54 (+10.6), Momentum 12-1 +0.43 (+18.7), Volatility -0.24 (-6.2) |
| EU | +3.6% | 2.61 | 0.95 | MIN5 +0.26 (+4.3), 55-day breakout +0.33 (+9.0), Momentum 12-1 +0.43 (+14.2), Volatility -0.22 (-3.2) |
| UK | +1.9% | 0.62 | 0.87 | 55-day breakout +0.53 (+7.6) |
| DK | +0.5% | 0.18 | 0.73 | Momentum 12-1 +0.35 (+4.9), 55-day breakout +0.25 (+2.6), Above 52-week low +0.27 (+3.3), Volatility -0.35 (-4.1) |
| SCANDI | +2.0% | 1.10 | 0.81 | 55-day breakout +0.44 (+5.9), Momentum 12-1 +0.42 (+10.1), Volatility -0.23 (-2.7) |
| World | -2.1% | -2.37 | 0.96 | 55-day breakout +0.48 (+7.5), Momentum 12-1 +0.46 (+13.9), Volatility -0.15 (-3.3) |

![Double sort](../figures/xs_FS09_dsort.png)

Holding Above 52-week low fixed (down a column), moving from low to high Near 52-week high changes the return by +0.6, -0.5 and +0.6 points a year; holding Near 52-week high fixed (along a row), moving from low to high Above 52-week low changes it by +3.5, +6.9 and +3.6.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -15% vs +34% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +2.5%, +1.9%, +3.4%, -0.3% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Data gap.** We hold for one month; George & Hwang hold for six. A longer holding period would cut turnover.
5. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- George, T. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance*, 59(5), 2145–2176.
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

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS09` → `build_xs.py FS09`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
