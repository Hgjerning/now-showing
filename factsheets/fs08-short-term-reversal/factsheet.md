# FACTSHEET FS08 · Short-term reversal

### Buy last month's losers, sell last month's winners

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>One-month reversal (liquidity provision)</div>
<div><b>Origin</b>Jegadeesh (1990); Lehmann (1990)</div>
<div><b>Family</b>Reversal & bottom-fishing</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (last month's losers)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Stocks with the worst returns last month outperform those with the best returns next month. Jegadeesh (1990) and Lehmann (1990) documented it for US stocks; it is large before costs and famously expensive to trade. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -9.7% to +0.1% a year and was positive in 1 of the six; no universe passes the 2.87 gate. The long-only book (last month's losers) had a higher Sharpe than the equal-weight universe in none of the six, with alphas of -7.1% to -0.8%, none past the gate. **What goes wrong (§10):** the main drags are costs of about 4.0% a year, a weaker second half (2020–26). None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Reversal & bottom-fishing; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours 55-day breakout, Net tail (MAX+MIN); after its closest neighbours and the market it keeps an alpha of -4.5% to +5.7% (largest |t| 2.2), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 503 / 10 | -6.6% | -1.58 | -12.1% (-2.7) | 0.39 | +9.8% | 0.53 | -39% | +14.2% | 0.96 | +15.3% |
| EU | 238 / 10 | -9.7% | -2.25 | -13.1% (-3.0) | 0.30 | +5.5% | 0.37 | -33% | +10.9% | 0.79 | +10.1% |
| UK | 242 / 10 | -3.0% | -0.58 | -7.2% (-1.4) | 0.40 | +7.4% | 0.44 | -49% | +9.9% | 0.74 | +8.5% |
| DK | 19 / 3 | -5.9% | -1.61 | -7.4% (-1.9) | 0.12 | +9.7% | 0.58 | -35% | +12.3% | 0.82 | +10.3% |
| SCANDI | 62 / 5 | +0.1% | 0.02 | -1.0% (-0.2) | 0.08 | +12.4% | 0.76 | -34% | +12.5% | 0.90 | +10.7% |
| World | 975 / 10 | -7.6% | -1.85 | -12.6% (-3.1) | 0.39 | +7.7% | 0.45 | -42% | +12.0% | 0.80 | +10.8% |

*Monthly, local currency (World in USD). L/S = equal-weighted last month's losers minus last month's winners, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS08_growth.png)

## 2. Strategy description

Stocks with the worst returns last month outperform those with the best returns next month. Jegadeesh (1990) and Lehmann (1990) documented it for US stocks; it is large before costs and famously expensive to trade.

**Why it might work.** Compensation for providing liquidity to investors who trade on non-information (Nagel 2012); overreaction to short-term news.

| Rule | Original (Jegadeesh (1990); Lehmann (1990)) | This factsheet |
|---|---|---|
| Signal | Previous month's (or week's) return | Return in month t |
| Portfolio | Decile L/S, one month | Extreme quantile L/S, one month |
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

R1<sub>i,t</sub> = total return of stock i in month t. Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = last month's losers minus last month's winners; **long-only** = last month's losers; benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (top 500, point-in-time)**, median 503 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -6.6% | -7.9% | 18.2% | -0.36 [-0.85, 0.12] | -0.57 | -74% | 40% | -1.58 | 0.39 | -12.1% (-2.7) | 12.7% |
| Long-only (net) | +12.0% | +9.8% | 22.5% | 0.53 [0.14, 1.03] | 0.68 | -39% | 61% | 2.64 | 1.32 | -7.1% (-3.1) | 13.2% |
| Last month's losers (gross) | +14.0% | +12.1% | 22.5% | 0.62 [0.22, 1.14] | 0.85 | -39% | 64% | 3.10 | 1.32 | -5.1% (-2.2) | 13.0% |
| Last month's winners (gross) | +15.7% | +15.2% | 17.0% | 0.92 [0.37, 1.52] | 1.52 | -28% | 63% | 3.47 | 0.93 | +2.2% (0.8) | 9.8% |
| EW universe | +14.5% | +14.2% | 15.1% | 0.96 [0.52, 1.53] | 1.52 | -25% | 67% | 4.79 | 1.00 | – | 8.9% |
| Size-weighted universe | +15.4% | +15.3% | 14.4% | 1.07 [0.61, 1.64] | 1.79 | -24% | 69% | 5.27 | 0.90 | +2.3% (1.8) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -9.7% | -10.4% | 15.9% | -0.61 [-1.11, -0.08] | -0.81 | -80% | 44% | -2.25 | 0.30 | -13.1% (-3.0) | 10.7% |
| Long-only (net) | +7.3% | +5.5% | 19.9% | 0.37 [-0.07, 0.85] | 0.42 | -33% | 58% | 1.54 | 1.20 | -6.4% (-2.6) | 11.8% |
| Last month's losers (gross) | +9.3% | +7.6% | 19.9% | 0.47 [0.03, 0.96] | 0.60 | -32% | 58% | 1.97 | 1.20 | -4.4% (-1.8) | 11.6% |
| Last month's winners (gross) | +14.1% | +13.7% | 15.6% | 0.91 [0.41, 1.46] | 1.53 | -25% | 60% | 3.61 | 0.91 | +3.8% (1.5) | 8.6% |
| EW universe | +11.4% | +10.9% | 14.5% | 0.79 [0.33, 1.33] | 1.22 | -26% | 64% | 3.35 | 1.00 | – | 8.3% |
| Size-weighted universe | +10.7% | +10.1% | 14.3% | 0.75 [0.28, 1.28] | 1.14 | -26% | 60% | 3.12 | 0.95 | -0.2% (-0.2) | 8.3% |

**UK (FTSE 350, point-in-time)**, median 242 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -3.0% | -4.5% | 17.6% | -0.17 [-0.82, 0.40] | -0.36 | -58% | 48% | -0.58 | 0.40 | -7.2% (-1.4) | 10.1% |
| Long-only (net) | +9.7% | +7.4% | 22.1% | 0.44 [-0.06, 1.10] | 0.50 | -49% | 53% | 1.63 | 1.36 | -4.6% (-1.3) | 12.8% |
| Last month's losers (gross) | +11.8% | +9.6% | 22.1% | 0.53 [0.03, 1.21] | 0.66 | -48% | 55% | 1.96 | 1.36 | -2.6% (-0.7) | 12.6% |
| Last month's winners (gross) | +10.0% | +9.0% | 16.4% | 0.61 [0.16, 1.13] | 0.86 | -26% | 60% | 2.74 | 0.96 | -0.1% (-0.1) | 9.7% |
| EW universe | +10.5% | +9.9% | 14.2% | 0.74 [0.26, 1.35] | 1.08 | -30% | 59% | 3.24 | 1.00 | – | 8.8% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.71 [0.21, 1.31] | 1.01 | -27% | 62% | 2.94 | 0.82 | +0.4% (0.2) | 7.7% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -5.9% | -7.0% | 15.8% | -0.38 [-0.85, 0.10] | -0.56 | -63% | 47% | -1.61 | 0.12 | -7.4% (-1.9) | 10.5% |
| Long-only (net) | +11.3% | +9.7% | 19.6% | 0.58 [0.09, 1.21] | 0.72 | -35% | 61% | 2.38 | 1.13 | -3.3% (-1.7) | 13.2% |
| Last month's losers (gross) | +12.8% | +11.4% | 19.6% | 0.66 [0.16, 1.30] | 0.86 | -34% | 61% | 2.70 | 1.13 | -1.8% (-0.9) | 13.1% |
| Last month's winners (gross) | +14.9% | +14.1% | 18.3% | 0.81 [0.31, 1.37] | 1.29 | -32% | 63% | 3.24 | 1.02 | +1.8% (0.8) | 9.7% |
| EW universe | +12.9% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.26 | -33% | 64% | 3.21 | 1.00 | – | 9.3% |
| Size-weighted universe | +11.2% | +10.3% | 16.6% | 0.68 [0.11, 1.32] | 0.94 | -40% | 61% | 2.52 | 0.91 | -0.6% (-0.2) | 10.8% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +0.1% | -0.8% | 13.5% | 0.01 [-0.53, 0.57] | -0.09 | -51% | 52% | 0.02 | 0.08 | -1.0% (-0.2) | 7.7% |
| Long-only (net) | +13.3% | +12.4% | 17.5% | 0.76 [0.23, 1.37] | 1.11 | -34% | 65% | 2.97 | 1.09 | -0.8% (-0.4) | 10.3% |
| Last month's losers (gross) | +15.1% | +14.5% | 17.5% | 0.87 [0.33, 1.49] | 1.33 | -33% | 66% | 3.39 | 1.09 | +1.1% (0.5) | 10.2% |
| Last month's winners (gross) | +10.5% | +9.6% | 16.2% | 0.65 [0.16, 1.18] | 0.94 | -28% | 54% | 2.71 | 1.01 | -2.5% (-1.2) | 9.9% |
| EW universe | +12.8% | +12.5% | 14.2% | 0.90 [0.38, 1.54] | 1.41 | -29% | 68% | 3.59 | 1.00 | – | 8.5% |
| Size-weighted universe | +11.2% | +10.7% | 13.9% | 0.80 [0.31, 1.37] | 1.21 | -27% | 63% | 3.26 | 0.94 | -0.9% (-0.8) | 8.6% |

**World (US + UK + EU, point-in-time)**, median 975 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -7.6% | -8.5% | 15.5% | -0.49 [-1.07, 0.06] | -0.69 | -72% | 42% | -1.85 | 0.39 | -12.6% (-3.1) | 10.9% |
| Long-only (net) | +9.9% | +7.7% | 22.3% | 0.45 [0.00, 0.96] | 0.53 | -42% | 57% | 1.91 | 1.31 | -6.6% (-3.1) | 13.0% |
| Last month's losers (gross) | +12.0% | +9.9% | 22.3% | 0.54 [0.09, 1.07] | 0.70 | -41% | 60% | 2.30 | 1.31 | -4.5% (-2.2) | 12.8% |
| Last month's winners (gross) | +14.8% | +14.3% | 16.3% | 0.91 [0.38, 1.52] | 1.47 | -28% | 63% | 3.53 | 0.92 | +3.2% (1.3) | 9.2% |
| EW universe | +12.6% | +12.0% | 15.7% | 0.80 [0.34, 1.38] | 1.20 | -29% | 64% | 3.54 | 1.00 | – | 9.4% |
| Size-weighted universe | +11.4% | +10.8% | 15.0% | 0.76 [0.29, 1.33] | 1.14 | -28% | 63% | 3.23 | 0.94 | -0.4% (-0.5) | 9.0% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -4.8% | +0.1% | -2.5% | -0.2% | +0.4% | -8.1% |
| 2014 | -14.5% | -18.2% | -8.3% | -17.8% | +0.1% | -17.1% |
| 2015 | +7.6% | -10.7% | -2.3% | -16.6% | +5.0% | +6.0% |
| 2016 | -1.5% | -13.0% | +30.6% | +19.5% | +7.2% | +5.2% |
| 2017 | -6.0% | -6.4% | -3.8% | -2.0% | -4.7% | -8.2% |
| 2018 | +1.8% | +4.4% | +3.7% | -11.5% | +1.5% | +1.6% |
| 2019 | +24.5% | +24.8% | -5.7% | +40.5% | +57.7% | +12.3% |
| 2020 | -14.6% | -16.0% | +0.7% | -31.2% | -17.5% | -3.5% |
| 2021 | +3.0% | +3.4% | +1.2% | +13.8% | +7.6% | +4.9% |
| 2022 | -13.0% | -17.7% | -19.3% | -4.2% | -8.1% | -22.7% |
| 2023 | -0.6% | -19.0% | +6.1% | -16.3% | -6.2% | -0.8% |
| 2024 | -22.4% | -4.5% | -7.2% | -21.6% | -8.4% | -17.6% |
| 2025 | -32.0% | -38.5% | -25.6% | -12.7% | -17.8% | -36.1% |
| 2026 | -21.0% | -15.0% | -16.5% | -12.5% | -10.1% | -17.9% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +30.2% | +25.2% | +21.9% | +45.8% | +27.3% | +24.4% |
| 2014 | +2.8% | -11.4% | -4.3% | +4.5% | +12.9% | -8.3% |
| 2015 | -3.8% | +0.5% | -3.7% | +11.8% | +12.0% | -1.1% |
| 2016 | +14.2% | +6.7% | +63.9% | +18.3% | +32.0% | +15.0% |
| 2017 | +11.1% | +17.6% | +26.1% | +17.5% | +14.2% | +20.2% |
| 2018 | -5.8% | -2.2% | -7.8% | -16.9% | -9.1% | -7.1% |
| 2019 | +47.9% | +37.6% | +17.7% | +51.7% | +73.8% | +37.1% |
| 2020 | +12.7% | -8.2% | -10.0% | +17.3% | +11.9% | +11.7% |
| 2021 | +35.5% | +20.0% | +25.5% | +32.1% | +25.3% | +27.8% |
| 2022 | -29.5% | -17.1% | -24.9% | -19.6% | -19.6% | -32.7% |
| 2023 | +27.0% | +5.4% | +15.4% | +1.7% | +3.7% | +27.1% |
| 2024 | +3.2% | +2.0% | -3.1% | -9.9% | -8.5% | -1.7% |
| 2025 | +3.4% | -1.5% | +2.3% | +3.6% | +9.2% | +3.2% |
| 2026 | +7.4% | +13.3% | +8.3% | +0.1% | +9.1% | +11.0% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS08_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 86% | 88% | 40% | -22.8% | 2020-03 |
| EU | 163 | 24 / 23 | 85% | 87% | 44% | -13.3% | 2024-02 |
| UK | 163 | 25 / 24 | 84% | 87% | 48% | -22.4% | 2020-03 |
| DK | 163 | 7 / 6 | 65% | 69% | 47% | -14.2% | 2020-02 |
| SCANDI | 163 | 13 / 12 | 79% | 80% | 52% | -11.9% | 2026-01 |
| World | 163 | 98 / 97 | 85% | 87% | 42% | -20.3% | 2020-03 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: last month's losers | Short: last month's winners |
|---|---|---|
| US | DVA, EIX, PCG, APP, APTV, TPR, NRG, WDC | MRNA, PLTR, VEEV, CRM, PSKY, NEM, NOW, SMCI |
| EU | BPOST.BR, ZAL.DE, RBREW.CO, ANA.MC, FME.DE, FER.MC, MRL.MC, GLE.PA | QTCOM.HE, JSW.WA, MAERSK-B.CO, MAERSK-A.CO, AGFB.BR, VWS.CO, BAVA.CO, SAP.DE |
| UK | GBG.L, TRN.L, RPI.L, BATS.L, PRN.L, IMB.L, CCH.L, PRU.L | ONT.L, HOC.L, PAF.L, KNOS.L, HAS.L, HWG.L, EDV.L, FRES.L |
| DK | RBREW.CO, CARL-B.CO, ORSTED.CO, DSV.CO, NOVO-B.CO, AMBU-B.CO, ZEAL.CO, GN.CO | MAERSK-B.CO, MAERSK-A.CO, VWS.CO, BAVA.CO, GMAB.CO, NSIS-B.CO, COLO-B.CO, JYSK.CO |
| SCANDI | RBREW.CO, CARL-B.CO, ORSTED.CO, VOLV-B.ST, WRT1V.HE, AZN.ST, DSV.CO, NOVO-B.CO | QTCOM.HE, MAERSK-B.CO, MAERSK-A.CO, VWS.CO, BAVA.CO, BOL.ST, EVO.ST, GMAB.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -5.3% | -1.44 | 0.56 | short_term_reversal +2.84 (+11.1) |
| EU | French Europe 5F + WML | -5.7% | -1.44 | 0.15 | Mkt-RF +0.20 (+2.0), SMB +0.52 (+2.8), WML -0.33 (-2.4) |
| UK | JKP GBR 7 themes | -2.8% | -0.72 | 0.50 | mkt +0.18 (+3.0), short_term_reversal +1.99 (+6.2) |
| DK | JKP DNK 7 themes | -0.6% | -0.16 | 0.33 | momentum -0.35 (-2.5), short_term_reversal +0.88 (+7.4) |
| SCANDI | French Europe 5F + WML | +2.2% | 0.61 | 0.06 | none |t| ≥ 2 |
| World | JKP World 7 themes | -11.8% | -2.59 | 0.45 | mkt +0.23 (+3.1), quality -0.41 (-2.2), short_term_reversal +1.85 (+6.2) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +1.4% | 0.69 | 0.90 | mkt +0.97 (+17.3), size -0.23 (-2.6), low_risk -0.65 (-3.4), short_term_reversal +1.53 (+7.4) |
| EU | French Europe 5F + WML | +5.3% | 1.73 | 0.67 | Mkt-RF +0.86 (+10.1), WML -0.39 (-4.5) |
| UK | JKP GBR 7 themes | +3.7% | 0.98 | 0.81 | mkt +0.67 (+14.0), low_risk -1.30 (-5.5), short_term_reversal +1.14 (+4.2) |
| DK | JKP DNK 7 themes | +6.8% | 2.15 | 0.73 | mkt +0.76 (+10.6), value +0.16 (+2.0), momentum -0.28 (-2.7), low_risk -0.47 (-3.8), short_term_reversal +0.48 (+4.4) |
| SCANDI | French Europe 5F + WML | +10.1% | 3.04 | 0.56 | Mkt-RF +0.75 (+9.2), RMW +0.57 (+2.3), WML -0.30 (-3.0) |
| World | JKP World 7 themes | +0.6% | 0.19 | 0.85 | mkt +0.85 (+13.3), low_risk -0.39 (-3.0), short_term_reversal +1.07 (+4.7) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 1 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -13.1% to -1.0%, |t| past the gate in 2 of 6.
- **Long-only:** Sharpe above the equal-weight universe in none of the six; alpha -7.1% to -0.8%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.10, EU 0.01, UK 0.27, DK 0.08, SCANDI 0.51, World 0.03.
- **Publication decay:** gross L/S +2.2% to +13.4% a year in 2013–19 against -12.0% to -3.9% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +6.0% | 0.32 | +4.5% | +1.5% | -4.2% | +1.2% | +4.8% | 175% | 2014-11 -8%, 2017-05 -7%, 2019-08 -5% |
| EU | +2.2% | 0.22 | +2.6% | -0.4% | -4.2% | +1.1% | +1.1% | 173% | 2015-01 -13%, 2015-09 -9%, 2013-03 -7% |
| UK | +7.3% | 0.09 | +1.2% | +6.1% | -4.1% | +3.2% | +4.1% | 171% | 2016-04 -10%, 2015-07 -9%, 2016-10 -9% |
| DK | +5.0% | -0.10 | -1.6% | +6.6% | -3.3% | +3.2% | +1.8% | 137% | 2019-08 -11%, 2014-02 -9%, 2013-05 -8% |
| SCANDI | +13.4% | 0.01 | +0.2% | +13.2% | -3.9% | +7.1% | +6.2% | 161% | 2017-10 -6%, 2017-04 -6%, 2018-06 -6% |
| World | +3.8% | 0.24 | +2.9% | +0.9% | -4.2% | +0.9% | +3.0% | 174% | 2013-03 -8%, 2017-04 -7%, 2014-11 -5% |

On average across the six universes the gross spread was +6.3% a year, of which the market exposure (beta +0.13) contributed +1.6%; the beta-adjusted spread (CAPM alpha) was +4.6%. Costs took 4.0% a year at 165% monthly turnover across both legs. The long leg beat the universe by +2.8% and the short leg lagged it by +3.5% a year, so most of the spread comes from the short side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +0.3%, +2.7%, +1.8% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.11 | – | -0.91 | – | – | -12.7% | -63% | -16.9% (-3.4) | 3.9% |
| X1 beta-neutral legs | 0.01 | -0.11 (p 0.838) | -1.15 | -0.23 (p 0.880) | 1 of 6 | -12.5% | -62% | -15.0% (-3.7) | 3.8% |
| X2 + turnover buffer | -0.03 | -0.08 (p 0.881) | -0.98 | +0.17 (p 0.074) | 6 of 6 | -10.2% | -57% | -12.7% (-3.3) | 3.0% |
| X3 + volatility targeting | -0.08 | -0.12 (p 0.600) | -0.87 | +0.11 (p 0.231) | 4 of 6 | -9.0% | -55% | -11.9% (-3.5) | 3.0% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS08_ladder.png)

- **X1 beta-neutral legs:** -0.11 design, -0.23 holdout; hurts in both windows.
- **X2 + turnover buffer:** -0.08 design, +0.17 holdout; helps in one window and hurts in the other: not reliable.
- **X3 + volatility targeting:** -0.12 design, +0.11 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe -0.91 → -0.87, return -12.7% → -9.0% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Short-term reversal |
|---|---|
| Series family | **Reversal & bottom-fishing** |
| Academic style | One-month reversal (liquidity provision) |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 165% of the two legs replaced monthly |
| Market exposure | L/S beta 0.08 to 0.40 |
| Payoff shape | Treynor–Mazuy γ -2.88 to 0.37 (t -2.5 to 0.5); worst 10% of market months -3.3% to -0.6% a month, best 10% -1.6% to +3.8% |
| Nearest factor theme | short_term_reversal (3 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | 55-day breakout (6 universes), Net tail (MAX+MIN) (6 universes), Near 52-week high (2 universes) |
| Economic rationale | Compensation for providing liquidity to investors who trade on non-information (Nagel 2012); overreaction to short-term news. |
| Publication | Jegadeesh 1990; Lehmann 1990; Nagel 2012 (reversal as liquidity provision) |
| Where it fits | In the **momentum** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Momentum 12-1**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Last month return **(this strategy)** | short-term reversal | +1.00 | +1.00 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| 55-day breakout | momentum | +0.68 | +0.69 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.62 | +0.62 | -1.0% | -5.3% to +4.2% | 0 / 0 |
| Near 52-week high | momentum | +0.44 | +0.51 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| MIN5 | low risk | +0.46 | +0.49 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| MIN (worst day) | low risk | +0.38 | +0.47 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| Above 52-week low | momentum | +0.39 | +0.46 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Momentum 12-1 (mirror) | momentum | -0.02 | +0.32 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Skewness | tail direction | +0.36 | +0.27 | -0.2% | -5.4% to +4.5% | 0 / 1 |
| Range (MAX−MIN) | low risk | -0.03 | -0.25 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| Volatility (252 days) | low risk | +0.00 | -0.24 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| Volatility | low risk | -0.01 | -0.24 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Beta | low risk | +0.02 | -0.22 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| Size | size | +0.02 | +0.21 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Idiosyncratic vol | low risk | -0.03 | -0.17 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| Same-month seasonality | seasonality | +0.02 | +0.12 | -1.8% | -8.5% to +7.2% | 0 / 0 |
| MAX5 | low risk | +0.41 | +0.09 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| Residual momentum | momentum | -0.16 | +0.05 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| MAX (best day) | low risk | +0.32 | +0.01 | +1.9% | -9.3% to +1.0% | 0 / 2 |

![360 map](../figures/xs_FS08_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with |t| ≥ 2 |
|---|---|---|---|---|
| US | +1.6% | 0.64 | 0.80 | 55-day breakout +0.74 (+7.7), Net tail +0.85 (+8.9) |
| EU | +5.7% | 2.05 | 0.67 | 55-day breakout +0.39 (+3.6), Net tail +0.62 (+6.6), MIN5 +0.46 (+3.9), MIN -0.27 (-2.2) |
| UK | -3.6% | -1.42 | 0.73 | Net tail +0.74 (+9.3), 55-day breakout +0.59 (+6.2), MIN5 +0.44 (+4.0), Near 52-week high -0.23 (-2.2), MIN -0.44 (-3.4) |
| DK | -4.2% | -1.56 | 0.56 | 55-day breakout +0.44 (+5.3), Net tail +0.30 (+4.2), Above 52-week low +0.16 (+2.5) |
| SCANDI | -4.5% | -1.58 | 0.51 | 55-day breakout +0.28 (+3.3), Net tail +0.34 (+4.2), Above 52-week low +0.23 (+3.7) |
| World | +4.3% | 2.18 | 0.85 | 55-day breakout +0.58 (+7.0), Net tail +1.00 (+11.8), MIN5 +0.39 (+2.9), MIN -0.56 (-3.4) |

![Double sort](../figures/xs_FS08_dsort.png)

Holding Momentum 12-1 fixed (down a column), moving from low to high Last month return changes the return by -1.4, +1.2 and +0.3 points a year; holding Last month return fixed (along a row), moving from low to high Momentum 12-1 changes it by +2.4, +5.0 and +4.1.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -4% vs +10% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +0.9%, +0.3%, +2.7%, +1.8% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns. *Journal of Finance*, 45(3), 881–898.
- Lehmann, B. (1990). Fads, martingales, and market efficiency. *Quarterly Journal of Economics*, 105(1), 1–28.
- Nagel, S. (2012). Evaporating liquidity. *Review of Financial Studies*, 25(7), 2005–2039.
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

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS08` → `build_xs.py FS08`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
