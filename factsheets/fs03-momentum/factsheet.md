# FACTSHEET FS03 · Momentum

### Buy last year's winners, sell last year's losers

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

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

> **The claim.** Stocks that did best over the past year keep outperforming the worst over the next months. Jegadeesh & Titman (1993) found about 1% a month for US stocks in 1965–1989; Asness, Moskowitz & Pedersen (2013) found it in every major equity market and asset class. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -2.8% to +9.7% a year and was positive in 5 of the six; no universe passes the 2.87 gate. The long-only book (winners) had a higher Sharpe than the equal-weight universe in 5 of the six (US, EU, UK, DK, World), with alphas of +0.5% to +8.8%, passing the gate in UK, World. **What goes wrong (§10):** the main drags are a market bet (average beta -0.33, worth -4.3% a year in 2013–19). None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Momentum & trend; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours Near 52-week high, Above 52-week low; after its closest neighbours and the market it keeps an alpha of -4.5% to +7.3% (largest |t| 2.4), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 500 / 10 | +6.6% | 1.38 | +10.8% (2.5) | -0.29 | +21.4% | 1.08 | -21% | +14.1% | 0.95 | +15.3% |
| EU | 238 / 10 | +7.0% | 1.31 | +14.7% (3.0) | -0.67 | +14.4% | 0.96 | -33% | +10.8% | 0.78 | +10.1% |
| UK | 238 / 10 | +9.7% | 1.59 | +15.8% (2.9) | -0.59 | +18.3% | 1.15 | -28% | +9.9% | 0.74 | +8.5% |
| DK | 19 / 3 | +5.6% | 1.20 | +10.1% (2.2) | -0.35 | +16.7% | 1.05 | -30% | +12.3% | 0.82 | +10.3% |
| SCANDI | 62 / 5 | -2.8% | -0.71 | +1.8% (0.5) | -0.36 | +10.9% | 0.79 | -33% | +12.5% | 0.91 | +10.7% |
| World | 968 / 10 | +7.6% | 1.66 | +13.7% (3.9) | -0.48 | +18.9% | 1.10 | -26% | +11.9% | 0.80 | +10.8% |

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
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: top 500 by market cap each month-end (Sharadar filings × price, A06 method) | ~499 | USD |
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

**US (top 500, point-in-time)**, median 500 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +6.6% | +4.5% | 20.5% | 0.32 [-0.14, 0.76] | 0.33 | -36% | 57% | 1.38 | -0.29 | +10.8% (2.5) | 12.3% |
| Long-only (net) | +21.5% | +21.4% | 20.0% | 1.08 [0.64, 1.55] | 1.96 | -21% | 64% | 4.76 | 1.07 | +6.1% (2.3) | 10.7% |
| Winners (gross) | +22.2% | +22.3% | 20.0% | 1.11 [0.68, 1.59] | 2.05 | -21% | 66% | 4.92 | 1.07 | +6.8% (2.6) | 10.6% |
| Losers (gross) | +13.3% | +11.1% | 23.6% | 0.56 [0.15, 1.05] | 0.77 | -38% | 60% | 2.63 | 1.36 | -6.4% (-2.7) | 13.2% |
| EW universe | +14.4% | +14.1% | 15.1% | 0.95 [0.52, 1.53] | 1.52 | -25% | 68% | 4.80 | 1.00 | – | 8.9% |
| Size-weighted universe | +15.4% | +15.3% | 14.4% | 1.07 [0.61, 1.64] | 1.79 | -24% | 69% | 5.27 | 0.90 | +2.4% (1.8) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +7.0% | +4.8% | 20.8% | 0.34 [-0.15, 0.94] | 0.32 | -46% | 60% | 1.31 | -0.67 | +14.7% (3.0) | 14.0% |
| Long-only (net) | +14.7% | +14.4% | 15.3% | 0.96 [0.37, 1.64] | 1.55 | -33% | 62% | 3.19 | 0.82 | +5.4% (1.8) | 8.6% |
| Winners (gross) | +15.4% | +15.2% | 15.3% | 1.01 [0.41, 1.69] | 1.66 | -33% | 63% | 3.34 | 0.82 | +6.1% (2.0) | 8.5% |
| Losers (gross) | +6.2% | +3.4% | 24.5% | 0.25 [-0.21, 0.70] | 0.22 | -40% | 52% | 1.02 | 1.49 | -10.8% (-3.9) | 12.9% |
| EW universe | +11.4% | +10.8% | 14.5% | 0.78 [0.33, 1.33] | 1.22 | -26% | 63% | 3.34 | 1.00 | – | 8.3% |
| Size-weighted universe | +10.7% | +10.1% | 14.3% | 0.75 [0.28, 1.28] | 1.14 | -26% | 60% | 3.12 | 0.95 | -0.1% (-0.1) | 8.3% |

**UK (FTSE 350, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +9.7% | +7.2% | 22.5% | 0.43 [-0.07, 1.02] | 0.44 | -49% | 63% | 1.59 | -0.59 | +15.8% (2.9) | 16.0% |
| Long-only (net) | +18.2% | +18.3% | 15.8% | 1.15 [0.59, 1.83] | 1.95 | -28% | 61% | 4.63 | 0.90 | +8.8% (3.7) | 9.5% |
| Winners (gross) | +18.8% | +19.1% | 15.8% | 1.19 [0.63, 1.88] | 2.04 | -28% | 61% | 4.79 | 0.90 | +9.5% (3.9) | 9.4% |
| Losers (gross) | +7.3% | +4.2% | 25.3% | 0.29 [-0.21, 0.82] | 0.26 | -49% | 51% | 1.07 | 1.48 | -8.2% (-2.2) | 14.5% |
| EW universe | +10.4% | +9.9% | 14.1% | 0.74 [0.25, 1.34] | 1.07 | -29% | 60% | 3.21 | 1.00 | – | 8.7% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.71 [0.21, 1.31] | 1.01 | -27% | 62% | 2.94 | 0.82 | +0.4% (0.2) | 7.7% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +5.6% | +4.0% | 18.2% | 0.31 [-0.18, 0.79] | 0.33 | -43% | 53% | 1.20 | -0.35 | +10.1% (2.2) | 11.4% |
| Long-only (net) | +16.8% | +16.7% | 16.0% | 1.05 [0.49, 1.64] | 1.90 | -30% | 63% | 4.01 | 0.86 | +5.8% (2.7) | 8.1% |
| Winners (gross) | +17.3% | +17.2% | 16.0% | 1.08 [0.51, 1.67] | 1.96 | -30% | 63% | 4.12 | 0.86 | +6.2% (2.9) | 8.0% |
| Losers (gross) | +10.0% | +7.9% | 21.7% | 0.46 [-0.01, 1.02] | 0.54 | -44% | 60% | 1.86 | 1.21 | -5.6% (-1.8) | 13.6% |
| EW universe | +12.8% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.26 | -33% | 64% | 3.20 | 1.00 | – | 9.3% |
| Size-weighted universe | +11.2% | +10.3% | 16.6% | 0.68 [0.11, 1.32] | 0.94 | -40% | 61% | 2.52 | 0.91 | -0.5% (-0.2) | 10.8% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -2.8% | -3.9% | 15.0% | -0.19 [-0.67, 0.30] | -0.35 | -59% | 46% | -0.71 | -0.36 | +1.8% (0.5) | 9.9% |
| Long-only (net) | +11.4% | +10.9% | 14.5% | 0.79 [0.24, 1.38] | 1.23 | -33% | 62% | 2.95 | 0.86 | +0.5% (0.2) | 7.8% |
| Winners (gross) | +12.0% | +11.5% | 14.5% | 0.83 [0.28, 1.43] | 1.31 | -32% | 62% | 3.10 | 0.86 | +1.0% (0.5) | 7.8% |
| Losers (gross) | +12.9% | +11.7% | 19.2% | 0.67 [0.17, 1.23] | 0.98 | -42% | 58% | 2.63 | 1.21 | -2.6% (-1.1) | 11.5% |
| EW universe | +12.8% | +12.5% | 14.1% | 0.91 [0.38, 1.54] | 1.42 | -29% | 67% | 3.62 | 1.00 | – | 8.3% |
| Size-weighted universe | +11.2% | +10.7% | 13.9% | 0.80 [0.31, 1.37] | 1.21 | -27% | 63% | 3.26 | 0.95 | -1.0% (-0.9) | 8.6% |

**World (US + UK + EU, point-in-time)**, median 968 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +7.6% | +6.0% | 18.4% | 0.41 [-0.06, 0.95] | 0.45 | -38% | 60% | 1.66 | -0.48 | +13.7% (3.9) | 12.6% |
| Long-only (net) | +18.8% | +18.9% | 17.1% | 1.10 [0.61, 1.67] | 1.93 | -26% | 66% | 4.71 | 0.94 | +7.1% (3.7) | 9.5% |
| Winners (gross) | +19.5% | +19.7% | 17.1% | 1.14 [0.65, 1.71] | 2.02 | -25% | 66% | 4.89 | 0.94 | +7.8% (4.0) | 9.5% |
| Losers (gross) | +9.7% | +7.0% | 24.5% | 0.40 [-0.06, 0.89] | 0.46 | -43% | 55% | 1.60 | 1.42 | -8.1% (-3.9) | 13.6% |
| EW universe | +12.5% | +11.9% | 15.7% | 0.80 [0.34, 1.38] | 1.20 | -29% | 64% | 3.53 | 1.00 | – | 9.4% |
| Size-weighted universe | +11.4% | +10.8% | 15.0% | 0.76 [0.29, 1.33] | 1.14 | -28% | 63% | 3.23 | 0.94 | -0.4% (-0.5) | 9.0% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +16.0% | +14.7% | +59.7% | -9.4% | +0.6% | +21.4% |
| 2014 | +2.5% | -6.1% | +32.5% | +11.8% | +4.8% | +12.8% |
| 2015 | +23.8% | +27.3% | +56.5% | +19.3% | +3.5% | +28.3% |
| 2016 | -23.0% | -12.1% | -26.7% | -17.4% | -6.0% | -16.6% |
| 2017 | +1.4% | -2.6% | -3.5% | -4.8% | +0.5% | -0.0% |
| 2018 | +10.9% | -3.1% | -8.6% | +8.8% | -0.7% | +6.3% |
| 2019 | -10.3% | +0.1% | +22.1% | +44.2% | -13.8% | +0.5% |
| 2020 | +3.8% | -9.8% | +1.7% | +14.6% | -19.1% | -4.3% |
| 2021 | -16.1% | -2.9% | -16.1% | -5.0% | -7.3% | -11.0% |
| 2022 | +26.8% | -6.4% | +11.0% | -2.5% | -6.4% | +17.0% |
| 2023 | -23.3% | -7.5% | -6.8% | -10.3% | -18.1% | -12.7% |
| 2024 | +55.1% | +24.1% | +2.2% | -19.3% | +10.0% | +28.6% |
| 2025 | +1.1% | +73.5% | +17.3% | +22.2% | +9.9% | +19.3% |
| 2026 | +20.8% | +2.1% | -7.0% | +22.4% | -4.7% | +5.6% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +38.5% | +35.1% | +58.6% | +39.0% | +27.4% | +41.9% |
| 2014 | +20.8% | -6.1% | +19.5% | +15.3% | +8.4% | +12.1% |
| 2015 | +5.6% | +13.8% | +33.2% | +41.9% | +17.0% | +10.2% |
| 2016 | +3.5% | +28.3% | +28.3% | +1.3% | +27.3% | +8.6% |
| 2017 | +20.9% | +13.7% | +35.0% | +15.4% | +17.8% | +29.9% |
| 2018 | -2.2% | -10.0% | -8.6% | -0.6% | -3.3% | -5.4% |
| 2019 | +30.9% | +29.2% | +29.1% | +43.8% | +26.6% | +29.8% |
| 2020 | +38.7% | +6.5% | +12.4% | +43.4% | +9.6% | +26.4% |
| 2021 | +15.9% | +11.5% | +13.1% | +24.6% | +18.6% | +12.1% |
| 2022 | -4.5% | -20.7% | -14.7% | -19.1% | -22.8% | -11.8% |
| 2023 | +16.0% | +17.8% | +5.1% | +9.1% | -2.8% | +16.9% |
| 2024 | +58.4% | +17.3% | +10.9% | -7.2% | +4.0% | +30.3% |
| 2025 | +22.3% | +74.5% | +31.1% | +15.4% | +20.7% | +44.2% |
| 2026 | +43.3% | +11.8% | +15.0% | +27.4% | +12.1% | +25.2% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS03_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 50 / 50 | 29% | 29% | 57% | -22.9% | 2026-07 |
| EU | 163 | 24 / 23 | 29% | 24% | 60% | -34.5% | 2020-11 |
| UK | 163 | 24 / 23 | 27% | 26% | 63% | -35.2% | 2020-11 |
| DK | 163 | 7 / 6 | 18% | 20% | 53% | -14.5% | 2020-11 |
| SCANDI | 163 | 13 / 12 | 24% | 24% | 46% | -13.5% | 2018-11 |
| World | 163 | 97 / 96 | 28% | 27% | 60% | -28.1% | 2020-11 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: winners | Short: losers |
|---|---|---|
| US | SNDK, MU, WDC, LITE, STX, CIEN, INTC, DELL | CSGP, FISV, BSX, INTU, COIN, PODD, ZTS, TSCO |
| EU | KGH.WA, ASML.AS, MT.AS, MTS.MC, REP.MC, ASM.AS, TYRES.HE, NOKIA.HE | ONTEX.BR, AGFB.BR, QTCOM.HE, UMG.AS, GTC.WA, BAR.BR, ADYEN.AS, STLAM.MI |
| UK | SAGA.L, CMCX.L, CWR.L, KLR.L, WOSG.L, SSIT.L, CCC.L, APN.L | VTY.L, AML.L, TEP.L, MEGP.L, BCG.L, DATA.L, ONT.L, ENT.L |
| DK | DANSKE.CO, ISS.CO, JYSK.CO, NKT.CO, VWS.CO, MAERSK-B.CO, NDA-DK.CO, MAERSK-A.CO | ZEAL.CO, COLO-B.CO, ORSTED.CO, BAVA.CO, AMBU-B.CO, GN.CO, ROCK-B.CO, NOVO-B.CO |
| SCANDI | NOKIA.HE, TYRES.HE, NESTE.HE, DANSKE.CO, SWED-A.ST, JYSK.CO, ISS.CO, SAND.ST | QTCOM.HE, ORSTED.CO, COLO-B.CO, BAVA.CO, PNDORA.CO, AMBU-B.CO, ELISA.HE, GN.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -1.6% | -0.68 | 0.78 | mkt +0.11 (+2.0), value -0.38 (-2.8), momentum +1.71 (+9.6) |
| EU | French Europe 5F + WML | -7.8% | -2.67 | 0.66 | WML +1.58 (+13.5) |
| UK | JKP GBR 7 themes | +2.0% | 0.54 | 0.64 | momentum +1.18 (+7.2), low_risk +0.83 (+2.3), quality +1.10 (+2.8), short_term_reversal -0.42 (-2.1) |
| DK | JKP DNK 7 themes | -3.0% | -0.94 | 0.51 | momentum +1.12 (+11.1), quality +0.24 (+2.0) |
| SCANDI | French Europe 5F + WML | -11.3% | -3.16 | 0.35 | WML +0.86 (+7.6) |
| World | JKP World 7 themes | +3.7% | 0.98 | 0.62 | value -0.43 (-3.6), momentum +1.37 (+10.6) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +5.7% | 3.32 | 0.90 | mkt +1.02 (+27.7), size -0.46 (-4.0), momentum +0.92 (+8.3), low_risk -0.58 (-4.9) |
| EU | French Europe 5F + WML | +2.8% | 0.89 | 0.58 | Mkt-RF +0.78 (+13.2), CMA -0.48 (-2.2), WML +0.56 (+6.7) |
| UK | JKP GBR 7 themes | +8.5% | 3.61 | 0.69 | mkt +0.59 (+11.1), momentum +0.67 (+5.6), low_risk -0.64 (-4.1), quality +0.80 (+4.6) |
| DK | JKP DNK 7 themes | +5.4% | 2.30 | 0.69 | mkt +0.68 (+14.8), size -0.18 (-2.7), momentum +0.38 (+4.0), low_risk -0.49 (-5.0), quality +0.28 (+3.1) |
| SCANDI | French Europe 5F + WML | +3.0% | 0.91 | 0.49 | Mkt-RF +0.65 (+9.5), WML +0.26 (+3.2) |
| World | JKP World 7 themes | +10.0% | 4.59 | 0.76 | mkt +0.69 (+11.6), momentum +0.70 (+6.2), low_risk -0.35 (-2.1) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 5 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** +1.8% to +15.8%, |t| past the gate in 3 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 5 of the six; alpha +0.5% to +8.8%, passing in 2 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.88, EU 0.88, UK 0.93, DK 0.87, SCANDI 0.25, World 0.92.
- **Publication decay:** gross L/S +1.0% to +18.1% a year in 2013–19 against -3.0% to +12.7% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +5.7% | -0.30 | -4.2% | +9.9% | -1.4% | +2.8% | +2.9% | 60% | 2015-04 -11%, 2019-09 -9%, 2018-06 -8% |
| EU | +5.9% | -0.61 | -7.1% | +13.0% | -1.3% | +3.1% | +2.8% | 54% | 2015-02 -12%, 2016-04 -12%, 2016-12 -11% |
| UK | +18.1% | -0.43 | -5.6% | +23.8% | -1.3% | +12.2% | +5.9% | 52% | 2016-02 -19%, 2016-04 -13%, 2017-02 -11% |
| DK | +8.6% | -0.02 | -0.4% | +8.9% | -0.9% | +5.7% | +2.9% | 37% | 2018-11 -12%, 2013-08 -10%, 2013-02 -10% |
| SCANDI | +1.0% | -0.21 | -3.2% | +4.3% | -1.2% | +1.9% | -0.8% | 49% | 2018-11 -14%, 2018-07 -9%, 2019-04 -9% |
| World | +9.8% | -0.44 | -5.4% | +15.2% | -1.4% | +5.4% | +4.5% | 57% | 2016-04 -9%, 2015-04 -8%, 2016-02 -7% |

On average across the six universes the gross spread was +8.2% a year, of which the market exposure (beta -0.33) contributed -4.3%; the beta-adjusted spread (CAPM alpha) was +12.5%. Costs took 1.2% a year at 52% monthly turnover across both legs. The long leg beat the universe by +5.2% and the short leg lagged it by +3.0% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +7.4%, +7.6%, +6.1% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.34 | – | 0.29 | – | – | +5.1% | -34% | +11.3% (2.2) | 1.2% |
| X1 beta-neutral legs | 0.46 | +0.17 (p 0.060) | 0.40 | +0.11 (p 0.219) | 5 of 6 | +5.3% | -28% | +8.1% (1.6) | 1.3% |
| X2 + turnover buffer | 0.44 | -0.02 (p 0.585) | 0.45 | +0.05 (p 0.324) | 4 of 6 | +5.2% | -24% | +7.5% (1.7) | 0.7% |
| X3 + volatility targeting | 0.40 | -0.07 (p 0.581) | 0.55 | +0.10 (p 0.078) | 3 of 6 | +5.6% | -18% | +7.5% (2.0) | 0.6% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS03_ladder.png)

- **X1 beta-neutral legs:** +0.17 design, +0.11 holdout; helps in both windows but does not pass the gate.
- **X2 + turnover buffer:** -0.02 design, +0.05 holdout; helps in one window and hurts in the other: not reliable.
- **X3 + volatility targeting:** -0.07 design, +0.10 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe 0.29 → 0.55, return +5.1% → +5.6% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Momentum |
|---|---|
| Series family | **Momentum & trend** |
| Academic style | Cross-sectional momentum (Carhart's UMD, AQR's momentum) |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 52% of the two legs replaced monthly |
| Market exposure | L/S beta -0.67 to -0.29 |
| Payoff shape | Treynor–Mazuy γ -3.60 to 1.07 (t -2.1 to 0.8); worst 10% of market months +1.8% to +4.5% a month, best 10% -4.7% to -2.7% |
| Nearest factor theme | momentum (3 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | Near 52-week high (6 universes), Above 52-week low (4 universes), Residual momentum (4 universes) |
| Economic rationale | Behavioural: investors under-react to news and then herd (Barberis, Shleifer & Vishny 1998; Hong & Stein 1999); the disposition effect slows the price response (Grinblatt & Han 2005). Risk stories exist but explain little. |
| Publication | Jegadeesh & Titman 1993 (data to 1989); Carhart 1997 factor; known crash risk after market rebounds (Daniel & Moskowitz 2016) |
| Where it fits | In the **momentum** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Last month return**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Momentum 12-1 **(this strategy)** | momentum | +1.00 | +1.00 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Near 52-week high | momentum | +0.57 | +0.77 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| Above 52-week low | momentum | +0.64 | +0.65 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Residual momentum | momentum | +0.66 | +0.63 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| 55-day breakout | momentum | +0.19 | +0.54 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Volatility | low risk | -0.15 | -0.44 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| MIN5 | low risk | +0.10 | +0.44 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| Volatility (252 days) | low risk | -0.12 | -0.41 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| Range (MAX−MIN) | low risk | -0.12 | -0.40 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| Beta | low risk | -0.09 | -0.39 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| MIN (worst day) | low risk | +0.08 | +0.38 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| MAX (best day) | low risk | -0.11 | -0.33 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| Last month return (mirror) | short-term reversal | -0.02 | +0.32 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Idiosyncratic vol | low risk | -0.10 | -0.32 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| MAX5 | low risk | -0.12 | -0.30 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| Size | size | +0.08 | +0.25 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Same-month seasonality | seasonality | +0.12 | +0.11 | -1.8% | -8.5% to +7.2% | 0 / 0 |
| Skewness | tail direction | -0.04 | -0.08 | -0.2% | -5.4% to +4.5% | 0 / 1 |
| Net tail (MAX+MIN) | tail direction | -0.04 | +0.06 | -1.0% | -5.3% to +4.2% | 0 / 0 |

![360 map](../figures/xs_FS03_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | -1.0% | -0.47 | 0.87 | Above 52-week low +0.50 (+11.0), Near 52-week high +0.91 (+11.2), Residual momentum +0.15 (+2.3), Size +0.26 (+3.2), 55-day breakout -0.61 (-7.8) |
| EU | -4.5% | -1.74 | 0.85 | Near 52-week high +0.78 (+6.1), 55-day breakout -0.46 (-5.3), Residual momentum +0.26 (+3.3), Above 52-week low +0.48 (+5.1) |
| UK | +7.3% | 2.37 | 0.77 | Near 52-week high +1.23 (+11.8), 55-day breakout -0.26 (-2.7), MIN5 -0.26 (-2.0) |
| DK | +0.7% | 0.27 | 0.76 | Near 52-week high +0.35 (+5.7), Residual momentum +0.41 (+9.8), Above 52-week low +0.40 (+6.0), Volatility -0.16 (-3.0), MIN5 -0.16 (-2.8) |
| SCANDI | -3.7% | -1.42 | 0.69 | Near 52-week high +0.54 (+6.1), Residual momentum +0.33 (+5.4), Above 52-week low +0.30 (+3.1) |
| World | +1.8% | 1.14 | 0.90 | Near 52-week high +1.04 (+10.0), Above 52-week low +0.42 (+6.9), Residual momentum +0.21 (+3.7), 55-day breakout -0.60 (-9.1) |

![Double sort](../figures/xs_FS03_dsort.png)

Holding Last month return fixed (down a column), moving from low to high Momentum 12-1 changes the return by +2.4, +5.0 and +4.1 points a year; holding Momentum 12-1 fixed (along a row), moving from low to high Last month return changes it by -1.4, +1.2 and +0.3.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -2% vs +25% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +7.7%, +7.4%, +7.6%, +6.1% a year.

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
