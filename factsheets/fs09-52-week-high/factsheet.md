# FACTSHEET FS09 · 52-week high

### Do stocks near their high keep going?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

> **US, 1999–2012 (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time S&P
> 500 with delisted stocks, 1999–2012, a period this factsheet was not built on. L/S net: t -0.98 (2013–2026: -1.00),
> same sign, weaker. Long-only alpha vs the equal-weight universe: -1.6% a year, t -0.64 (2013–2026: +0.05), no
> 2013–2026 effect to test. Registered verdicts are unchanged. Pre-registration, method and every result:
> `PREREG_US_1999_2012.md`.



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

> **The claim.** Stocks trading close to their 52-week high outperform those far below it, and this nearness explains much of momentum. George & Hwang (2004) found it for US stocks 1963–2001; investors anchor on the high and under-react to good news near it. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -5.8% to +8.8% a year and was positive in 2 of the six; no universe passes the 2.87 gate. The long-only book (stocks closest to their 52-week high) had a higher Sharpe than the equal-weight universe in 5 of the six (EU, UK, DK, SCANDI, World), with alphas of +0.1% to +6.9%, passing the gate in EU, DK. **What goes wrong (§10):** the main drags are a market bet (average beta -0.66, worth -8.1% a year in 2013–19), costs of about 2.0% a year. None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Momentum & trend; its returns sit closest to the momentum cluster of the signal library. **360° view (§12):** nearest neighbours 55-day breakout, MIN5; after its closest neighbours and the market it keeps an alpha of -1.2% to +3.8% (largest |t| 2.6), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 502 / 10 | -5.8% | -1.00 | +6.8% (1.7) | -0.97 | +8.1% | 0.70 | -21% | +12.6% | 0.85 | +14.9% |
| EU | 264 / 10 | +8.8% | 1.78 | +18.6% (4.5) | -0.91 | +13.4% | 1.25 | -20% | +10.1% | 0.75 | +10.2% |
| UK | 327 / 10 | -0.9% | -0.13 | +9.5% (1.9) | -1.09 | +9.1% | 0.90 | -20% | +8.9% | 0.68 | +7.8% |
| DK | 20 / 3 | +6.1% | 1.56 | +11.0% (3.0) | -0.39 | +17.1% | 1.16 | -31% | +12.0% | 0.83 | +10.2% |
| SCANDI | 70 / 5 | -1.2% | -0.29 | +6.3% (1.9) | -0.59 | +12.9% | 1.04 | -23% | +12.2% | 0.89 | +11.0% |
| World | 1089 / 10 | -1.9% | -0.34 | +8.6% (2.3) | -0.93 | +8.4% | 0.74 | -21% | +10.5% | 0.71 | +10.3% |

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
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: the S&P 500 members at each month-end (Sharadar add/remove history; corrected 2 Oct 2026) | ~503 | USD |
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

**US (S&P 500 members, point-in-time)**, median 502 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -5.8% | -8.5% | 24.3% | -0.24 [-0.69, 0.20] | -0.45 | -78% | 50% | -1.00 | -0.97 | +6.8% (1.7) | 18.2% |
| Long-only (net) | +8.5% | +8.1% | 12.3% | 0.70 [0.28, 1.16] | 1.03 | -21% | 61% | 3.64 | 0.65 | +0.1% (0.0) | 7.4% |
| Stocks closest to their 52-week high (gross) | +10.3% | +9.9% | 12.3% | 0.84 [0.41, 1.31] | 1.31 | -20% | 63% | 4.34 | 0.65 | +1.8% (1.2) | 7.3% |
| Stocks furthest below it (gross) | +12.6% | +8.8% | 28.5% | 0.44 [0.00, 0.96] | 0.50 | -50% | 56% | 1.89 | 1.61 | -8.6% (-2.8) | 15.9% |
| EW universe | +13.1% | +12.6% | 15.5% | 0.85 [0.41, 1.42] | 1.29 | -28% | 67% | 4.20 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.9% | +14.9% | 14.2% | 1.05 [0.60, 1.61] | 1.73 | -24% | 69% | 5.29 | 0.86 | +3.7% (2.4) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 264 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +8.8% | +6.6% | 20.9% | 0.42 [-0.03, 0.99] | 0.43 | -41% | 55% | 1.78 | -0.91 | +18.6% (4.5) | 13.6% |
| Long-only (net) | +13.2% | +13.4% | 10.5% | 1.25 [0.70, 1.90] | 2.31 | -20% | 65% | 4.57 | 0.59 | +6.9% (4.1) | 5.7% |
| Stocks closest to their 52-week high (gross) | +14.8% | +15.2% | 10.5% | 1.40 [0.84, 2.06] | 2.70 | -19% | 66% | 5.09 | 0.59 | +8.4% (5.0) | 5.5% |
| Stocks furthest below it (gross) | +2.9% | -0.0% | 24.8% | 0.12 [-0.37, 0.57] | -0.00 | -54% | 49% | 0.47 | 1.50 | -13.3% (-4.0) | 12.6% |
| EW universe | +10.7% | +10.1% | 14.3% | 0.75 [0.29, 1.30] | 1.14 | -26% | 62% | 3.18 | 1.00 | – | 8.4% |
| Size-weighted universe | +10.6% | +10.2% | 13.7% | 0.77 [0.32, 1.29] | 1.21 | -25% | 58% | 3.37 | 0.92 | +0.8% (0.6) | 7.9% |

**UK (FTSE 350, point-in-time)**, median 327 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -0.9% | -4.2% | 24.9% | -0.04 [-0.51, 0.48] | -0.22 | -70% | 55% | -0.13 | -1.09 | +9.5% (1.9) | 18.0% |
| Long-only (net) | +9.2% | +9.1% | 10.3% | 0.90 [0.42, 1.45] | 1.39 | -20% | 60% | 3.74 | 0.57 | +3.7% (1.9) | 6.5% |
| Stocks closest to their 52-week high (gross) | +10.9% | +10.8% | 10.3% | 1.06 [0.56, 1.62] | 1.71 | -17% | 62% | 4.38 | 0.57 | +5.3% (2.8) | 6.4% |
| Stocks furthest below it (gross) | +8.9% | +5.2% | 28.0% | 0.32 [-0.15, 0.80] | 0.31 | -50% | 52% | 1.22 | 1.66 | -7.0% (-1.8) | 15.7% |
| EW universe | +9.6% | +8.9% | 14.2% | 0.68 [0.20, 1.28] | 0.96 | -30% | 58% | 2.87 | 1.00 | – | 8.8% |
| Size-weighted universe | +8.4% | +7.8% | 12.9% | 0.65 [0.16, 1.25] | 0.90 | -28% | 62% | 2.68 | 0.84 | +0.3% (0.2) | 7.8% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +6.1% | +4.7% | 17.1% | 0.36 [-0.08, 0.82] | 0.43 | -28% | 53% | 1.56 | -0.39 | +11.0% (3.0) | 9.3% |
| Long-only (net) | +17.0% | +17.1% | 14.6% | 1.16 [0.63, 1.70] | 2.18 | -31% | 63% | 4.40 | 0.81 | +6.8% (3.8) | 7.0% |
| Stocks closest to their 52-week high (gross) | +17.7% | +18.0% | 14.7% | 1.21 [0.67, 1.76] | 2.31 | -30% | 63% | 4.57 | 0.81 | +7.5% (4.2) | 7.0% |
| Stocks furthest below it (gross) | +9.6% | +7.7% | 20.9% | 0.46 [-0.06, 1.07] | 0.55 | -44% | 59% | 1.72 | 1.21 | -5.5% (-2.2) | 12.4% |
| EW universe | +12.6% | +12.0% | 15.2% | 0.83 [0.31, 1.44] | 1.27 | -33% | 66% | 3.31 | 1.00 | – | 8.8% |
| Size-weighted universe | +11.1% | +10.2% | 16.4% | 0.68 [0.11, 1.33] | 0.94 | -40% | 62% | 2.55 | 0.93 | -0.6% (-0.2) | 10.7% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -1.2% | -2.5% | 16.2% | -0.07 [-0.54, 0.40] | -0.21 | -54% | 52% | -0.29 | -0.59 | +6.3% (1.9) | 9.6% |
| Long-only (net) | +12.9% | +12.9% | 12.4% | 1.04 [0.52, 1.61] | 1.77 | -23% | 66% | 4.21 | 0.76 | +3.4% (2.3) | 6.6% |
| Stocks closest to their 52-week high (gross) | +14.1% | +14.1% | 12.4% | 1.13 [0.61, 1.70] | 1.98 | -22% | 66% | 4.55 | 0.76 | +4.5% (3.0) | 6.5% |
| Stocks furthest below it (gross) | +12.7% | +11.0% | 21.4% | 0.59 [0.12, 1.13] | 0.82 | -44% | 59% | 2.42 | 1.35 | -4.3% (-1.8) | 12.6% |
| EW universe | +12.6% | +12.2% | 14.2% | 0.89 [0.37, 1.52] | 1.38 | -29% | 66% | 3.63 | 1.00 | – | 8.4% |
| Size-weighted universe | +11.4% | +11.0% | 13.5% | 0.84 [0.37, 1.41] | 1.32 | -26% | 63% | 3.59 | 0.90 | -0.0% (-0.0) | 8.1% |

**World (US + UK + EU, point-in-time)**, median 1089 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -1.9% | -4.5% | 22.3% | -0.09 [-0.54, 0.39] | -0.26 | -65% | 53% | -0.34 | -0.93 | +8.6% (2.3) | 16.7% |
| Long-only (net) | +8.8% | +8.4% | 12.0% | 0.74 [0.29, 1.28] | 1.09 | -21% | 63% | 3.39 | 0.64 | +1.6% (1.1) | 7.6% |
| Stocks closest to their 52-week high (gross) | +10.5% | +10.2% | 12.0% | 0.88 [0.41, 1.44] | 1.37 | -20% | 63% | 4.01 | 0.64 | +3.2% (2.4) | 7.5% |
| Stocks furthest below it (gross) | +9.2% | +5.6% | 27.8% | 0.33 [-0.13, 0.81] | 0.33 | -47% | 54% | 1.32 | 1.58 | -8.6% (-3.2) | 15.0% |
| EW universe | +11.3% | +10.5% | 16.0% | 0.71 [0.25, 1.28] | 1.02 | -30% | 63% | 3.07 | 1.00 | – | 9.7% |
| Size-weighted universe | +11.0% | +10.3% | 14.8% | 0.74 [0.28, 1.31] | 1.10 | -28% | 61% | 3.19 | 0.91 | +0.7% (0.8) | 8.9% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -1.3% | -4.4% | +20.8% | -2.9% | +15.4% | +4.2% |
| 2014 | +3.6% | +49.8% | -3.1% | +8.7% | +7.4% | +16.7% |
| 2015 | +24.7% | +38.3% | +19.3% | +10.2% | +11.8% | +20.0% |
| 2016 | -33.2% | -10.7% | -47.0% | -20.4% | -20.2% | -29.3% |
| 2017 | +4.6% | -6.5% | -2.7% | +7.1% | -3.5% | -0.4% |
| 2018 | +6.9% | +9.7% | -8.9% | +7.6% | +11.8% | -1.2% |
| 2019 | -21.8% | -14.2% | +2.0% | +11.3% | -21.8% | -10.7% |
| 2020 | -27.3% | -11.1% | -23.1% | +10.2% | -19.1% | -23.1% |
| 2021 | -24.4% | +7.8% | -10.7% | +0.9% | -10.6% | -12.4% |
| 2022 | +8.6% | +0.3% | +39.2% | +10.2% | +12.5% | +10.6% |
| 2023 | -22.9% | +3.9% | -13.3% | -15.5% | -14.0% | -18.9% |
| 2024 | +13.2% | +9.3% | -0.7% | +8.8% | +9.0% | +8.2% |
| 2025 | -12.3% | +30.7% | +24.5% | +31.8% | +18.0% | +3.4% |
| 2026 | -12.8% | +7.8% | -18.8% | +6.2% | -15.3% | -13.0% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +26.2% | +21.9% | +15.8% | +41.0% | +34.5% | +26.5% |
| 2014 | +14.5% | +8.8% | +5.9% | +20.0% | +12.1% | +7.3% |
| 2015 | -1.8% | +16.0% | +13.0% | +24.3% | +29.1% | -1.8% |
| 2016 | +4.2% | +14.0% | -0.2% | -0.8% | +16.9% | +1.7% |
| 2017 | +11.1% | +7.1% | +19.3% | +25.6% | +17.5% | +19.8% |
| 2018 | -1.9% | +4.7% | -11.3% | -3.1% | -0.3% | -9.9% |
| 2019 | +15.6% | +14.4% | +10.2% | +33.0% | +15.3% | +17.6% |
| 2020 | +12.2% | +9.5% | +9.0% | +53.5% | +14.4% | +13.8% |
| 2021 | +19.9% | +26.0% | +16.6% | +19.7% | +12.1% | +15.6% |
| 2022 | -11.9% | -12.8% | -0.9% | -12.3% | -8.7% | -12.3% |
| 2023 | +0.3% | +17.6% | +7.7% | +6.5% | +2.9% | +4.5% |
| 2024 | +15.0% | +2.6% | +9.2% | +9.2% | +5.0% | +9.6% |
| 2025 | +6.6% | +43.7% | +31.3% | +23.3% | +25.1% | +25.0% |
| 2026 | +5.9% | +17.8% | +3.5% | +10.1% | +6.6% | +5.1% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS09_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 71% | 24% | 50% | -30.9% | 2020-11 |
| EU | 163 | 27 / 26 | 65% | 22% | 55% | -39.8% | 2020-11 |
| UK | 163 | 33 / 32 | 68% | 24% | 55% | -44.2% | 2020-11 |
| DK | 163 | 7 / 6 | 29% | 21% | 53% | -11.8% | 2023-11 |
| SCANDI | 163 | 14 / 14 | 47% | 24% | 52% | -12.3% | 2020-11 |
| World | 163 | 109 / 108 | 70% | 23% | 53% | -37.6% | 2020-11 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks closest to their 52-week high | Short: stocks furthest below it |
|---|---|---|
| US | VLO, PSX, SLB, CRWD, MPC, GEN, TECH, PFE | TTD, CSGP, FISV, PODD, APP, BLDR, BSX, ORCL |
| EU | ASRNL.AS, RAND.AS, SKF-B.ST, ABN.AS, DSFIR.AS, JYSK.CO, KESKOB.HE, PUIG.MC | ONTEX.BR, FCT.MI, AVIO.MI, STLAM.MI, AGFB.BR, STLAP.PA, NYR.BR, UMG.AS |
| UK | ASL.L, RS1.L, ATYM.L, HAS.L, GCP.L, AAL.L, VCT.L, INVP.L | AML.L, VTY.L, CWR.L, TEP.L, RPI.L, DATA.L, OXB.L, SMWH.L |
| DK | JYSK.CO, NDA-DK.CO, NSIS-B.CO, PNDORA.CO, VWS.CO, DANSKE.CO, ISS.CO, DEMANT.CO | ZEAL.CO, AMBU-B.CO, ORSTED.CO, RBREW.CO, DSV.CO, COLO-B.CO, NOVO-B.CO, GN.CO |
| SCANDI | KESKOB.HE, JYSK.CO, SKF-B.ST, NDA-SE.ST, NDA-DK.CO, NSIS-B.CO, NDA-FI.HE, SHB-A.ST | NOKIA.HE, ORSTED.CO, RBREW.CO, AMBU-B.CO, QTCOM.HE, WRT1V.HE, ERIC-B.ST, COLO-B.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -9.3% | -4.49 | 0.87 | value -0.70 (-5.4), momentum +1.09 (+7.4), low_risk +1.29 (+6.7), quality +0.85 (+3.2), short_term_reversal -1.07 (-4.9) |
| EU | French Europe 5F + WML | -0.7% | -0.19 | 0.62 | Mkt-RF -0.41 (-4.5), WML +1.19 (+6.6) |
| UK | JKP GBR 7 themes | -6.6% | -1.49 | 0.78 | momentum +1.09 (+6.9), low_risk +1.66 (+5.7), quality +0.75 (+2.4), short_term_reversal -0.94 (-4.6) |
| DK | JKP DNK 7 themes | -3.0% | -1.20 | 0.60 | momentum +1.00 (+10.7), low_risk +0.65 (+5.7) |
| SCANDI | French Europe 5F + WML | -9.0% | -2.93 | 0.45 | Mkt-RF -0.25 (-3.0), HML +0.46 (+2.4), WML +0.87 (+9.0) |
| World | JKP World 7 themes | -2.5% | -0.57 | 0.72 | mkt -0.16 (-2.1), value -0.51 (-3.1), momentum +0.97 (+7.4), low_risk +1.02 (+5.5), short_term_reversal -0.99 (-4.1) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -2.4% | -1.79 | 0.86 | mkt +0.92 (+26.1), momentum +0.32 (+3.6), low_risk +0.48 (+6.0), short_term_reversal -0.36 (-4.8) |
| EU | French Europe 5F + WML | +5.8% | 2.73 | 0.55 | Mkt-RF +0.51 (+10.8), HML +0.30 (+2.7), WML +0.25 (+4.4) |
| UK | JKP GBR 7 themes | +3.4% | 1.80 | 0.57 | mkt +0.42 (+9.7), value +0.19 (+2.6), momentum +0.31 (+4.2), quality +0.46 (+4.5) |
| DK | JKP DNK 7 themes | +6.4% | 2.52 | 0.64 | mkt +0.73 (+16.2), momentum +0.26 (+3.6), quality +0.20 (+2.5), short_term_reversal -0.19 (-2.4) |
| SCANDI | French Europe 5F + WML | +5.5% | 2.15 | 0.49 | Mkt-RF +0.58 (+9.9), RMW +0.37 (+2.4), WML +0.21 (+2.7) |
| World | JKP World 7 themes | +3.2% | 1.32 | 0.67 | mkt +0.66 (+13.2), momentum +0.27 (+3.1), low_risk +0.35 (+3.0), short_term_reversal -0.33 (-2.2) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 2 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** +6.3% to +18.6%, |t| past the gate in 2 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 5 of the six; alpha +0.1% to +6.9%, passing in 2 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.19, EU 0.91, UK 0.45, DK 0.90, SCANDI 0.39, World 0.37.
- **Publication decay:** gross L/S -0.9% to +11.0% a year in 2013–19 against -5.8% to +12.8% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +1.1% | -0.83 | -10.9% | +12.0% | -2.3% | -1.9% | +3.0% | 97% | 2015-04 -15%, 2019-01 -13%, 2016-04 -11% |
| EU | +11.0% | -0.91 | -9.7% | +20.7% | -2.0% | +3.1% | +7.9% | 85% | 2015-02 -12%, 2016-03 -11%, 2019-04 -9% |
| UK | -0.9% | -0.75 | -8.7% | +7.8% | -2.2% | -2.7% | +1.7% | 93% | 2016-02 -17%, 2016-04 -17%, 2015-04 -14% |
| DK | +5.6% | -0.16 | -2.4% | +8.0% | -1.4% | +4.0% | +1.6% | 57% | 2016-08 -7%, 2016-07 -7%, 2013-02 -7% |
| SCANDI | +2.8% | -0.52 | -8.0% | +10.7% | -1.8% | +2.9% | -0.1% | 75% | 2019-06 -10%, 2015-04 -9%, 2019-01 -9% |
| World | +3.3% | -0.81 | -8.9% | +12.2% | -2.3% | -0.9% | +4.2% | 94% | 2016-04 -14%, 2015-04 -13%, 2015-02 -10% |

On average across the six universes the gross spread was +3.8% a year, of which the market exposure (beta -0.66) contributed -8.1%; the beta-adjusted spread (CAPM alpha) was +11.9%. Costs took 2.0% a year at 83% monthly turnover across both legs. The long leg beat the universe by +0.8% and the short leg lagged it by +3.1% a year, so most of the spread comes from the short side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +3.5%, +4.0%, +0.3% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.06 | – | 0.04 | – | – | +0.8% | -42% | +10.4% (2.5) | 2.0% |
| X1 beta-neutral legs | 0.37 | +0.40 (p 0.001) | 0.18 | +0.14 (p 0.179) | 4 of 6 | +2.6% | -31% | +5.9% (1.3) | 2.2% |
| X2 + turnover buffer | 0.50 | +0.19 (p 0.032) | 0.22 | +0.04 (p 0.274) | 3 of 6 | +2.8% | -26% | +5.6% (1.5) | 1.1% |
| X3 + volatility targeting | 0.44 | -0.05 (p 0.545) | 0.52 | +0.30 (p 0.002) ✔ | 5 of 6 | +5.4% | -16% | +7.4% (2.3) | 1.1% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS09_ladder.png)

- **X1 beta-neutral legs:** +0.40 design, +0.14 holdout; helps in both windows but does not pass the gate.
- **X2 + turnover buffer:** +0.19 design, +0.04 holdout; helps in both windows but does not pass the gate.
- **X3 + volatility targeting:** -0.05 design, +0.30 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe 0.04 → 0.52, return +0.8% → +5.4% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | 52-week high |
|---|---|
| Series family | **Momentum & trend** |
| Academic style | Anchoring momentum |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 83% of the two legs replaced monthly |
| Market exposure | L/S beta -1.09 to -0.39 |
| Payoff shape | Treynor–Mazuy γ -4.59 to 0.59 (t -3.3 to 0.7); worst 10% of market months +4.3% to +5.5% a month, best 10% -10.1% to -2.5% |
| Nearest factor theme | momentum (2 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | 55-day breakout (6 universes), MIN5 (4 universes), Momentum 12-1 (4 universes) |
| Economic rationale | Anchoring: traders use the 52-week high as a reference and are reluctant to bid prices above it, so good news is absorbed slowly (George & Hwang 2004). |
| Publication | George & Hwang 2004 |
| Where it fits | In the **momentum** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Above 52-week low**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Near 52-week high **(this strategy)** | momentum | +1.00 | +1.00 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| 55-day breakout | momentum | +0.73 | +0.83 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| Momentum 12-1 | momentum | +0.59 | +0.80 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| MIN5 | low risk | +0.58 | +0.79 | -0.9% | +2.3% to +13.7% | 4 / 0 |
| Volatility | low risk | -0.48 | -0.78 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| MIN (worst day) | low risk | +0.49 | +0.74 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| Volatility (252 days) | low risk | -0.44 | -0.74 | +2.4% | -12.9% to -4.8% | 0 / 3 |
| Range (MAX−MIN) | low risk | -0.39 | -0.74 | -0.7% | -15.4% to -4.8% | 0 / 4 |
| Beta | low risk | -0.29 | -0.69 | +4.4% | -12.6% to -4.2% | 0 / 4 |
| Idiosyncratic vol | low risk | -0.37 | -0.62 | -3.6% | -15.5% to -4.8% | 0 / 4 |
| MAX (best day) | low risk | -0.18 | -0.62 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| MAX5 | low risk | -0.19 | -0.58 | +0.6% | -11.3% to -3.5% | 0 / 2 |
| Last month return | short-term reversal | +0.43 | +0.52 | +1.8% | -3.2% to +11.0% | 2 / 0 |
| Residual momentum | momentum | +0.30 | +0.46 | +6.4% | +8.0% to +12.2% | 6 / 0 |
| Above 52-week low (mirror) | momentum | +0.51 | +0.46 | +7.5% | +5.2% to +13.6% | 4 / 0 |
| Size | size | +0.11 | +0.36 | +0.1% | -3.8% to +9.9% | 1 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.24 | +0.18 | -0.9% | -5.2% to +5.2% | 0 / 0 |
| Same-month seasonality | seasonality | +0.01 | +0.11 | -1.9% | -9.4% to +6.6% | 0 / 1 |
| Skewness | tail direction | +0.13 | -0.03 | -0.4% | -6.7% to +3.9% | 0 / 2 |

![360 map](../figures/xs_FS09_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | -1.2% | -1.03 | 0.95 | 55-day breakout +0.53 (+7.1), Momentum 12-1 +0.41 (+12.5), Volatility -0.23 (-6.3) |
| EU | +3.8% | 2.58 | 0.93 | MIN5 +0.24 (+3.9), 55-day breakout +0.33 (+7.7), Momentum 12-1 +0.45 (+12.2), Volatility -0.22 (-2.9) |
| UK | +1.0% | 0.32 | 0.88 | 55-day breakout +0.55 (+6.2), Volatility -0.22 (-2.0), Range -0.24 (-2.4) |
| DK | +1.8% | 0.76 | 0.74 | Momentum 12-1 +0.36 (+4.8), 55-day breakout +0.32 (+4.4), Volatility -0.33 (-4.1), Above 52-week low +0.19 (+2.2) |
| SCANDI | +3.5% | 1.69 | 0.82 | Momentum 12-1 +0.49 (+11.6), 55-day breakout +0.32 (+5.5), Volatility -0.18 (-2.0) |
| World | -0.9% | -0.92 | 0.97 | 55-day breakout +0.48 (+8.9), Momentum 12-1 +0.45 (+14.9), Volatility -0.15 (-3.7) |

![Double sort](../figures/xs_FS09_dsort.png)

Holding Above 52-week low fixed (down a column), moving from low to high Near 52-week high changes the return by +0.5, -0.1 and +1.2 points a year; holding Near 52-week high fixed (along a row), moving from low to high Above 52-week low changes it by +2.9, +6.1 and +3.7.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -15% vs +38% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +3.7%, +3.5%, +4.0%, +0.3% a year.

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
