# FACTSHEET FS10 · Betting against beta

### Lever up the low-beta stocks, short the high-beta ones

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Defensive / betting against beta</div>
<div><b>Origin</b>Frazzini & Pedersen (2014)</div>
<div><b>Family</b>Low risk</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (low-beta stocks)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Low-beta stocks have higher risk-adjusted returns than high-beta stocks. A portfolio that is long leveraged low-beta stocks and short de-leveraged high-beta stocks, beta-neutral, earned a large positive return in the US 1926–2012 and in 19 other markets (Frazzini & Pedersen 2014). **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned +2.0% to +9.5% a year and was positive in all six; it passes the 2.87 gate in UK. The long-only book (low-beta stocks) had a higher Sharpe than the equal-weight universe in 5 of the six (EU, UK, DK, SCANDI, World), with alphas of +1.6% to +3.8%, passing the gate in UK. **What goes wrong (§10):** the main drags are a weaker second half (2020–26). None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Low risk; its returns sit closest to the low risk cluster of the signal library. **360° view (§12):** nearest neighbours Volatility (252 days), Volatility; after its closest neighbours and the market it keeps an alpha of -9.6% to +3.9% (largest |t| 3.6), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 501 / 10 | +2.0% | 0.54 | -0.8% (-0.2) | 0.19 | +11.0% | 0.95 | -19% | +14.1% | 0.95 | +15.3% |
| EU | 238 / 10 | +4.4% | 1.55 | +3.6% (1.2) | 0.07 | +9.4% | 0.93 | -19% | +10.9% | 0.78 | +10.1% |
| UK | 239 / 10 | +9.5% | 3.16 | +7.9% (2.7) | 0.16 | +10.4% | 1.07 | -19% | +9.9% | 0.74 | +8.5% |
| DK | 19 / 3 | +2.9% | 0.66 | +2.6% (0.6) | 0.02 | +11.1% | 0.91 | -18% | +12.3% | 0.82 | +10.3% |
| SCANDI | 62 / 5 | +2.5% | 0.87 | +1.9% (0.6) | 0.05 | +10.9% | 1.02 | -20% | +12.5% | 0.91 | +10.7% |
| World | 971 / 10 | +5.1% | 1.84 | +1.9% (0.6) | 0.26 | +10.2% | 0.90 | -21% | +11.9% | 0.80 | +10.8% |

*Monthly, local currency (World in USD). L/S = equal-weighted low-beta stocks minus high-beta stocks (rank-weighted, each leg scaled to beta 1), net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS10_growth.png)

## 2. Strategy description

Low-beta stocks have higher risk-adjusted returns than high-beta stocks. A portfolio that is long leveraged low-beta stocks and short de-leveraged high-beta stocks, beta-neutral, earned a large positive return in the US 1926–2012 and in 19 other markets (Frazzini & Pedersen 2014).

**Why it might work.** Leverage-constrained investors buy high-beta stocks instead of levering the market, bidding them up (Black 1972; Frazzini & Pedersen 2014); lottery demand (Bali, Brown, Murray & Tang 2017).

| Rule | Original (Frazzini & Pedersen (2014)) | This factsheet |
|---|---|---|
| Signal | Shrunk beta from 1-year volatility and 5-year correlation | 252-day beta vs the equal-weight universe (no shrinkage) |
| Portfolio | Rank-weighted legs above/below median beta, each scaled to beta 1 | Same construction |
| Weighting | Rank weights | Rank weights |

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

- **Data gap:** Financing uses the USD risk-free rate for all markets, which overstates the cost in EU and Denmark while their rates were negative (2015–21). Betas are raw, not shrunk.

## 4. Signal creation

BAB<sub>t+1</sub> = r<sub>L</sub>/β<sub>L</sub> − r<sub>H</sub>/β<sub>H</sub>, with rank-weighted low- and high-beta legs (the net long cash is financed at the USD risk-free rate + 0.5% a year; the high-beta leg pays a size-tiered borrow fee). Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = low-beta stocks minus high-beta stocks; **long-only** = low-beta stocks; benchmarks: equal-weight universe and size-weighted universe.
- Frazzini & Pedersen construction: betas ranked, each leg weighted by rank distance from the median and scaled to an ex-ante beta of 1; no risk-free rate is subtracted.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (top 500, point-in-time)**, median 501 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.0% | +0.6% | 16.6% | 0.12 [-0.32, 0.58] | 0.05 | -46% | 52% | 0.54 | 0.19 | -0.8% (-0.2) | 9.9% |
| Long-only (net) | +11.1% | +11.0% | 11.8% | 0.95 [0.55, 1.43] | 1.51 | -19% | 64% | 5.38 | 0.66 | +1.6% (1.1) | 7.0% |
| Low-beta stocks (gross) | +11.3% | +11.2% | 11.8% | 0.96 [0.56, 1.45] | 1.54 | -19% | 64% | 5.47 | 0.66 | +1.8% (1.3) | 7.0% |
| High-beta stocks (gross) | +18.8% | +17.7% | 21.8% | 0.86 [0.40, 1.40] | 1.36 | -34% | 63% | 3.82 | 1.36 | -0.8% (-0.4) | 12.5% |
| EW universe | +14.4% | +14.1% | 15.1% | 0.95 [0.52, 1.53] | 1.52 | -25% | 68% | 4.79 | 1.00 | – | 8.9% |
| Size-weighted universe | +15.4% | +15.3% | 14.4% | 1.07 [0.61, 1.64] | 1.79 | -24% | 69% | 5.27 | 0.90 | +2.4% (1.8) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +4.4% | +3.6% | 12.9% | 0.34 [-0.12, 0.83] | 0.42 | -31% | 55% | 1.55 | 0.07 | +3.6% (1.2) | 7.8% |
| Long-only (net) | +9.5% | +9.4% | 10.3% | 0.93 [0.45, 1.50] | 1.46 | -19% | 63% | 4.20 | 0.62 | +2.5% (2.2) | 6.3% |
| Low-beta stocks (gross) | +9.7% | +9.6% | 10.3% | 0.95 [0.47, 1.52] | 1.50 | -19% | 63% | 4.29 | 0.62 | +2.6% (2.3) | 6.3% |
| High-beta stocks (gross) | +13.0% | +11.2% | 21.6% | 0.60 [0.15, 1.07] | 0.85 | -36% | 58% | 2.50 | 1.41 | -3.1% (-2.1) | 11.8% |
| EW universe | +11.4% | +10.9% | 14.5% | 0.78 [0.33, 1.33] | 1.22 | -26% | 64% | 3.34 | 1.00 | – | 8.3% |
| Size-weighted universe | +10.7% | +10.1% | 14.3% | 0.75 [0.28, 1.28] | 1.14 | -26% | 60% | 3.12 | 0.95 | -0.2% (-0.1) | 8.3% |

**UK (FTSE 350, point-in-time)**, median 239 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +9.5% | +9.2% | 11.8% | 0.81 [0.29, 1.36] | 1.27 | -23% | 63% | 3.16 | 0.16 | +7.9% (2.7) | 7.4% |
| Long-only (net) | +10.4% | +10.4% | 9.7% | 1.07 [0.53, 1.76] | 1.68 | -19% | 66% | 4.81 | 0.63 | +3.8% (4.1) | 6.2% |
| Low-beta stocks (gross) | +10.6% | +10.6% | 9.7% | 1.09 [0.55, 1.78] | 1.73 | -19% | 66% | 4.92 | 0.63 | +4.0% (4.3) | 6.2% |
| High-beta stocks (gross) | +10.2% | +8.2% | 21.0% | 0.48 [0.02, 1.03] | 0.60 | -41% | 56% | 1.97 | 1.42 | -4.7% (-3.2) | 12.3% |
| EW universe | +10.5% | +9.9% | 14.1% | 0.74 [0.26, 1.34] | 1.08 | -29% | 60% | 3.23 | 1.00 | – | 8.8% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.71 [0.21, 1.31] | 1.01 | -27% | 62% | 2.94 | 0.82 | +0.4% (0.2) | 7.7% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.9% | +1.4% | 17.1% | 0.17 [-0.29, 0.64] | 0.12 | -34% | 55% | 0.66 | 0.02 | +2.6% (0.6) | 10.7% |
| Long-only (net) | +11.4% | +11.1% | 12.5% | 0.91 [0.42, 1.44] | 1.49 | -18% | 61% | 3.61 | 0.64 | +3.2% (1.6) | 6.8% |
| Low-beta stocks (gross) | +11.6% | +11.4% | 12.5% | 0.93 [0.44, 1.46] | 1.53 | -17% | 61% | 3.68 | 0.64 | +3.4% (1.7) | 6.7% |
| High-beta stocks (gross) | +16.0% | +14.3% | 22.6% | 0.71 [0.17, 1.34] | 1.04 | -49% | 60% | 2.60 | 1.32 | -1.0% (-0.4) | 13.4% |
| EW universe | +12.9% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.26 | -33% | 64% | 3.21 | 1.00 | – | 9.3% |
| Size-weighted universe | +11.2% | +10.3% | 16.6% | 0.68 [0.11, 1.32] | 0.94 | -40% | 61% | 2.52 | 0.91 | -0.6% (-0.2) | 10.8% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +2.5% | +1.8% | 12.2% | 0.21 [-0.28, 0.68] | 0.22 | -28% | 53% | 0.87 | 0.05 | +1.9% (0.6) | 6.8% |
| Long-only (net) | +11.0% | +10.9% | 10.8% | 1.02 [0.49, 1.61] | 1.71 | -20% | 64% | 4.18 | 0.67 | +2.4% (2.1) | 6.0% |
| Low-beta stocks (gross) | +11.2% | +11.2% | 10.8% | 1.04 [0.51, 1.63] | 1.75 | -20% | 64% | 4.25 | 0.67 | +2.6% (2.2) | 6.0% |
| High-beta stocks (gross) | +14.7% | +13.5% | 20.2% | 0.73 [0.21, 1.36] | 1.06 | -43% | 63% | 2.84 | 1.35 | -2.7% (-1.9) | 12.0% |
| EW universe | +12.8% | +12.5% | 14.1% | 0.91 [0.39, 1.54] | 1.42 | -29% | 67% | 3.62 | 1.00 | – | 8.3% |
| Size-weighted universe | +11.2% | +10.7% | 13.9% | 0.80 [0.31, 1.37] | 1.21 | -27% | 63% | 3.26 | 0.95 | -1.0% (-0.9) | 8.6% |

**World (US + UK + EU, point-in-time)**, median 971 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +5.1% | +4.3% | 13.2% | 0.39 [-0.04, 0.87] | 0.48 | -24% | 56% | 1.84 | 0.26 | +1.9% (0.6) | 8.5% |
| Long-only (net) | +10.4% | +10.2% | 11.6% | 0.90 [0.46, 1.45] | 1.37 | -21% | 67% | 4.57 | 0.67 | +1.9% (1.9) | 7.1% |
| Low-beta stocks (gross) | +10.6% | +10.4% | 11.6% | 0.92 [0.47, 1.47] | 1.41 | -21% | 67% | 4.67 | 0.67 | +2.1% (2.1) | 7.1% |
| High-beta stocks (gross) | +14.8% | +13.1% | 21.8% | 0.68 [0.21, 1.23] | 0.96 | -38% | 60% | 2.78 | 1.34 | -2.1% (-1.5) | 12.7% |
| EW universe | +12.5% | +11.9% | 15.7% | 0.80 [0.33, 1.38] | 1.20 | -29% | 64% | 3.53 | 1.00 | – | 9.4% |
| Size-weighted universe | +11.4% | +10.8% | 15.0% | 0.76 [0.29, 1.33] | 1.14 | -28% | 63% | 3.23 | 0.94 | -0.4% (-0.5) | 9.0% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +11.4% | +6.7% | +39.8% | -12.4% | +4.7% | +21.4% |
| 2014 | +13.6% | +15.9% | +7.9% | -5.9% | +15.9% | +11.3% |
| 2015 | +6.7% | +12.5% | +30.0% | -7.0% | +7.1% | +12.3% |
| 2016 | -0.7% | +5.0% | +5.0% | -12.8% | -21.1% | -6.3% |
| 2017 | +7.8% | +13.3% | +22.4% | +26.3% | +10.7% | +18.6% |
| 2018 | -1.3% | +5.0% | -1.1% | -19.4% | +0.6% | -5.5% |
| 2019 | +16.1% | +11.8% | +18.6% | +58.9% | +18.0% | +20.8% |
| 2020 | -15.8% | -6.9% | +0.5% | -19.8% | -9.4% | -1.9% |
| 2021 | +16.8% | +5.3% | +15.3% | +31.8% | +10.9% | +14.7% |
| 2022 | +3.0% | -18.1% | -9.8% | +4.6% | -5.5% | -10.7% |
| 2023 | -24.1% | -6.7% | -13.1% | -12.9% | -17.4% | -13.0% |
| 2024 | +2.3% | +2.3% | +11.0% | -1.6% | +2.5% | +8.9% |
| 2025 | -14.1% | +2.9% | +5.5% | +8.2% | +6.0% | -4.5% |
| 2026 | -3.3% | +5.8% | +5.1% | +9.7% | +11.4% | +1.4% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +22.2% | +14.4% | +25.7% | +18.1% | +16.7% | +24.6% |
| 2014 | +17.5% | +10.3% | +6.6% | +8.3% | +16.2% | +9.6% |
| 2015 | +2.4% | +11.8% | +16.8% | +13.7% | +11.5% | +5.0% |
| 2016 | +9.7% | +11.7% | +14.9% | +3.4% | +11.6% | +3.1% |
| 2017 | +14.6% | +14.8% | +21.3% | +25.8% | +21.5% | +20.4% |
| 2018 | -2.4% | -3.5% | -3.8% | -14.2% | -3.6% | -6.8% |
| 2019 | +27.9% | +23.1% | +22.8% | +41.7% | +31.2% | +26.0% |
| 2020 | +10.5% | +3.5% | +1.6% | +15.2% | +10.4% | +12.3% |
| 2021 | +23.9% | +14.7% | +14.6% | +27.8% | +19.9% | +18.1% |
| 2022 | -3.7% | -11.6% | -11.0% | -7.5% | -12.5% | -10.7% |
| 2023 | +2.3% | +9.7% | +2.4% | +4.3% | +0.9% | +7.3% |
| 2024 | +13.9% | +6.5% | +10.5% | +3.1% | +4.2% | +11.7% |
| 2025 | +6.1% | +16.0% | +14.0% | +14.8% | +16.0% | +13.7% |
| 2026 | +8.9% | +10.8% | +11.3% | +8.7% | +11.9% | +10.6% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS10_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 249 / 249 | 13% | 6% | 52% | -12.5% | 2021-02 |
| EU | 163 | 117 / 117 | 14% | 5% | 55% | -11.6% | 2021-09 |
| UK | 163 | 119 / 119 | 16% | 6% | 63% | -11.2% | 2021-02 |
| DK | 163 | 9 / 9 | 15% | 6% | 55% | -13.6% | 2022-05 |
| SCANDI | 163 | 31 / 31 | 13% | 6% | 53% | -7.8% | 2021-02 |
| World | 163 | 483 / 483 | 16% | 6% | 56% | -11.0% | 2021-02 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: low-beta stocks | Short: high-beta stocks |
|---|---|---|
| US | CF, OXY, XOM, EOG, APA, FANG, CVX, DVN | MRNA, SMCI, SNDK, CCL, COIN, HOOD, UAL, Q |
| EU | REP.MC, NESTE.HE, GALP.LS, ENI.MI, TTE.PA, SHELL.AS, JSW.WA, KPN.AS | MTS.MC, MT.AS, IFX.DE, KGH.WA, ENR.DE, IAG.MC, BOL.ST, GLE.PA |
| UK | HBR.L, ITH.L, BP.L, SHEL.L, ENOG.L, BEZ.L, BHMG.L, IMB.L | RPI.L, GDWN.L, RHIM.L, WIZZ.L, ANTO.L, FRES.L, HOC.L, PAF.L |
| DK | TRYG.CO, NSIS-B.CO, JYSK.CO, ISS.CO, NDA-DK.CO, CARL-B.CO, DANSKE.CO, RBREW.CO | ZEAL.CO, GN.CO, NOVO-B.CO, AMBU-B.CO, ROCK-B.CO, ORSTED.CO, DEMANT.CO, DSV.CO |
| SCANDI | NESTE.HE, ELISA.HE, TELIA.ST, TRYG.CO, TEL2-B.ST, EVO.ST, MAERSK-B.CO, ESSITY-B.ST | KCR.HE, METSO.HE, BOL.ST, ROCK-B.CO, GN.CO, ZEAL.CO, QTCOM.HE, SAND.ST |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -6.1% | -2.86 | 0.63 | mkt +0.85 (+9.0), value -0.44 (-2.9), low_risk +1.70 (+8.8) |
| EU | French Europe 5F + WML | -2.3% | -0.73 | 0.29 | Mkt-RF +0.24 (+4.0), RMW +1.15 (+4.1), CMA +0.56 (+2.4), WML +0.32 (+2.7) |
| UK | JKP GBR 7 themes | +3.9% | 1.28 | 0.48 | mkt +0.39 (+7.0), momentum +0.26 (+2.7), low_risk +0.93 (+5.5), quality +0.64 (+4.0) |
| DK | JKP DNK 7 themes | +0.1% | 0.03 | 0.40 | mkt +0.43 (+5.9), size -0.33 (-2.2), low_risk +1.22 (+8.5) |
| SCANDI | French Europe 5F + WML | -3.1% | -1.03 | 0.12 | Mkt-RF +0.13 (+2.4), RMW +0.57 (+2.3), WML +0.33 (+3.5) |
| World | JKP World 7 themes | +0.8% | 0.32 | 0.45 | mkt +0.67 (+7.8), momentum +0.31 (+2.4), low_risk +1.24 (+7.7) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +1.7% | 1.73 | 0.88 | mkt +0.91 (+31.5), size -0.24 (-3.5), value -0.14 (-2.5), low_risk +0.71 (+8.8) |
| EU | French Europe 5F + WML | +4.0% | 2.09 | 0.65 | Mkt-RF +0.54 (+15.5), RMW +0.44 (+3.1) |
| UK | JKP GBR 7 themes | +5.0% | 2.67 | 0.68 | mkt +0.46 (+12.3), quality +0.40 (+4.0) |
| DK | JKP DNK 7 themes | +5.9% | 2.45 | 0.58 | mkt +0.62 (+12.6), value +0.10 (+2.0), low_risk +0.25 (+3.1), quality +0.15 (+2.4) |
| SCANDI | French Europe 5F + WML | +6.2% | 2.72 | 0.51 | Mkt-RF +0.50 (+10.2), RMW +0.46 (+3.6) |
| World | JKP World 7 themes | +5.0% | 3.07 | 0.77 | mkt +0.70 (+15.3), low_risk +0.49 (+6.7) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in all six; passes in 1 of 6 (UK).
- **L/S CAPM alpha:** -0.8% to +7.9%, |t| past the gate in 0 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 5 of the six; alpha +1.6% to +3.8%, passing in 1 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.67, EU 0.89, UK 1.00, DK 0.73, SCANDI 0.78, World 0.92.
- **Publication decay:** gross L/S +4.2% to +18.6% a year in 2013–19 against +0.7% to +8.1% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +10.2% | 0.01 | +0.1% | +10.1% | -0.5% | -1.3% | -0.7% | 19% | 2013-05 -7%, 2018-02 -6%, 2016-08 -6% |
| EU | +12.2% | -0.03 | -0.4% | +12.6% | -0.4% | +0.1% | +0.4% | 18% | 2016-10 -6%, 2019-04 -5%, 2017-06 -4% |
| UK | +18.6% | 0.38 | +5.0% | +13.6% | -0.6% | +1.1% | -0.3% | 23% | 2016-11 -6%, 2016-06 -5%, 2018-12 -4% |
| DK | +4.2% | 0.19 | +2.9% | +1.4% | -0.5% | -2.2% | -5.6% | 21% | 2016-10 -11%, 2018-10 -11%, 2013-05 -11% |
| SCANDI | +7.1% | -0.00 | -0.0% | +7.1% | -0.5% | -1.0% | -3.3% | 20% | 2016-11 -7%, 2016-10 -7%, 2013-08 -6% |
| World | +12.3% | 0.13 | +1.6% | +10.7% | -0.6% | -1.0% | -0.1% | 23% | 2018-05 -6%, 2018-02 -5%, 2016-08 -5% |

On average across the six universes the gross spread was +10.8% a year, of which the market exposure (beta +0.11) contributed +1.5%; the beta-adjusted spread (CAPM alpha) was +9.2%. Costs took 0.5% a year at 21% monthly turnover across both legs. The long leg beat the universe by -0.7% and the short leg lagged it by -1.6% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +5.2%, +5.6%, +6.0% a year.

### 10.2 The fix ladder

X0 baseline → X3 volatility targeting (BAB is beta-neutral and rank-weighted by construction, so the beta-neutral and buffer steps do not apply).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.81 | – | 0.00 | – | – | +0.0% | -22% | -1.5% (-0.4) | 0.5% |
| X3 + volatility targeting | 0.70 | +0.03 (p 0.467) | 0.07 | +0.07 (p 0.329) | 4 of 6 | +0.8% | -22% | -0.4% (-0.2) | 0.5% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS10_ladder.png)

- **X3 + volatility targeting:** +0.03 design, +0.07 holdout; helps in both windows but does not pass the gate.

**Where it ends:** holdout Sharpe 0.00 → 0.07, return +0.0% → +0.8% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Betting against beta |
|---|---|
| Series family | **Low risk** |
| Academic style | Defensive / betting against beta |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 21% of the two legs replaced monthly |
| Market exposure | L/S beta 0.02 to 0.26 |
| Payoff shape | Treynor–Mazuy γ -2.25 to -0.59 (t -5.1 to -0.7); worst 10% of market months -3.2% to -0.2% a month, best 10% -0.8% to +0.8% |
| Nearest factor theme | low_risk (2 of 6 universes), RMW (1 of 6 universes) |
| Nearest library signals (returns) | Volatility (252 days) (6 universes), Volatility (6 universes), Range (MAX−MIN) (5 universes) |
| Economic rationale | Leverage-constrained investors buy high-beta stocks instead of levering the market, bidding them up (Black 1972; Frazzini & Pedersen 2014); lottery demand (Bali, Brown, Murray & Tang 2017). |
| Publication | Black, Jensen & Scholes 1972; Frazzini & Pedersen 2014; critique by Novy-Marx & Velikov (2022) on construction and costs |
| Where it fits | In the **low risk** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **MAX**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Beta **(this strategy)** | low risk | +1.00 | +1.00 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| Volatility (252 days) | low risk | +0.66 | +0.85 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| Volatility | low risk | +0.58 | +0.83 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Range (MAX−MIN) | low risk | +0.43 | +0.75 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| MIN5 | low risk | -0.43 | -0.73 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| MAX5 | low risk | +0.47 | +0.71 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| MAX (best day) (mirror) | low risk | +0.39 | +0.70 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| MIN (worst day) | low risk | -0.36 | -0.68 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| Near 52-week high | momentum | -0.28 | -0.65 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| Idiosyncratic vol | low risk | +0.27 | +0.59 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| 55-day breakout | momentum | -0.21 | -0.56 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Momentum 12-1 | momentum | -0.09 | -0.39 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Residual momentum | momentum | -0.05 | -0.25 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| Last month return | short-term reversal | +0.02 | -0.22 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Size | size | +0.04 | -0.21 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Skewness | tail direction | +0.03 | +0.10 | -0.2% | -5.4% to +4.5% | 0 / 1 |
| Same-month seasonality | seasonality | +0.11 | -0.04 | -1.8% | -8.5% to +7.2% | 0 / 0 |
| Above 52-week low | momentum | +0.19 | +0.04 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.03 | +0.01 | -1.0% | -5.3% to +4.2% | 0 / 0 |

![360 map](../figures/xs_FS10_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | -1.7% | -0.68 | 0.86 | Volatility +0.93 (+7.1) |
| EU | -4.3% | -1.20 | 0.72 | Volatility +0.47 (+2.5), Volatility +0.37 (+2.0) |
| UK | -9.6% | -3.62 | 0.83 | Volatility +0.59 (+4.9) |
| DK | +3.9% | 1.27 | 0.76 | Volatility +0.69 (+8.3), Volatility +0.17 (+2.2) |
| SCANDI | -0.6% | -0.24 | 0.64 | Volatility +0.38 (+2.4) |
| World | -2.5% | -1.16 | 0.86 | Volatility +0.87 (+7.1) |

![Double sort](../figures/xs_FS10_dsort.png)

Holding MAX fixed (down a column), moving from low to high Beta changes the return by +3.6, +3.9 and +2.6 points a year; holding Beta fixed (along a row), moving from low to high MAX changes it by +0.5, -1.5 and -0.5.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): +32% vs -42% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +5.5%, +5.2%, +5.6%, +6.0% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Data gap.** Financing uses the USD risk-free rate for all markets, which overstates the cost in EU and Denmark while their rates were negative (2015–21). Betas are raw, not shrunk.
5. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics*, 111(1), 1–25.
- Black, F. (1972). Capital market equilibrium with restricted borrowing. *Journal of Business*, 45(3), 444–455.
- Bali, T. G., Brown, S., Murray, S. & Tang, Y. (2017). A lottery-demand-based explanation of the beta anomaly. *Journal of Financial and Quantitative Analysis*, 52(6), 2369–2397.
- Novy-Marx, R. & Velikov, M. (2022). Betting against betting against beta. *Journal of Financial Economics*, 143(1), 80–106.
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

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS10` → `build_xs.py FS10`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
