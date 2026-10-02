# FACTSHEET FS04 · Low volatility

### Do calm stocks beat exciting ones?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

<div class="kf" markdown="0">
<div><b>Strategy</b>Defensive / low-risk anomaly</div>
<div><b>Origin</b>Haugen & Heins (1975); Blitz & van Vliet (2007)</div>
<div><b>Family</b>Low risk</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (calmest stocks)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Low-volatility stocks earn about the same or more than high-volatility stocks, so their risk-adjusted return is far higher, contradicting the CAPM. Blitz & van Vliet (2007) documented it globally for 1986–2006; Ang, Hodrick, Xing & Zhang (2006) for idiosyncratic volatility. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -8.7% to +1.6% a year and was positive in 1 of the six; no universe passes the 2.87 gate. The long-only book (calmest stocks) had a higher Sharpe than the equal-weight universe in all six, with alphas of +2.7% to +5.0%, none past the gate. **What goes wrong (§10):** the main drags are a market bet (average beta -0.79, worth -10.0% a year in 2013–19). None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Low risk; its returns sit closest to the low risk cluster of the signal library. **360° view (§12):** nearest neighbours Volatility, Range (MAX−MIN); after its closest neighbours and the market it keeps an alpha of -3.0% to +5.4% (largest |t| 2.5), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 502 / 10 | -8.7% | -1.36 | +4.6% (1.1) | -1.01 | +10.4% | 0.89 | -21% | +12.6% | 0.85 | +14.9% |
| EU | 264 / 10 | +1.6% | 0.28 | +10.9% (2.4) | -0.87 | +11.0% | 1.07 | -21% | +10.2% | 0.75 | +10.2% |
| UK | 326 / 10 | -6.0% | -0.96 | +2.8% (0.6) | -0.92 | +8.3% | 0.93 | -20% | +8.9% | 0.68 | +7.8% |
| DK | 20 / 3 | -1.1% | -0.21 | +7.2% (1.8) | -0.66 | +13.3% | 1.07 | -19% | +12.0% | 0.83 | +10.2% |
| SCANDI | 70 / 5 | -3.1% | -0.63 | +6.1% (1.7) | -0.74 | +12.3% | 1.13 | -15% | +12.3% | 0.89 | +11.0% |
| World | 1088 / 10 | -5.7% | -1.05 | +4.3% (1.4) | -0.89 | +9.2% | 0.85 | -21% | +10.5% | 0.71 | +10.3% |

*Monthly, local currency (World in USD). L/S = equal-weighted calmest stocks (lowest 252-day volatility) minus most volatile stocks, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS04_growth.png)

## 2. Strategy description

Low-volatility stocks earn about the same or more than high-volatility stocks, so their risk-adjusted return is far higher, contradicting the CAPM. Blitz & van Vliet (2007) documented it globally for 1986–2006; Ang, Hodrick, Xing & Zhang (2006) for idiosyncratic volatility.

**Why it might work.** Leverage constraints push investors into high-beta, high-volatility stocks (Black 1972; Frazzini & Pedersen 2014); benchmarked managers cannot exploit it without tracking error (Baker, Bradley & Wurgler 2011); lottery preferences (Bali, Cakici & Whitelaw 2011).

| Rule | Original (Haugen & Heins (1975); Blitz & van Vliet (2007)) | This factsheet |
|---|---|---|
| Signal | Past 1–3 year volatility (weekly or daily returns) | 252-day volatility of daily total returns |
| Portfolio | Decile or quintile; often long-only low-vol | Extreme quantile L/S and the low-vol leg long-only, monthly |
| Weighting | Equal or value weighted | Equal weighted |

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

VOL<sub>i,t</sub> = standard deviation of daily returns over the 252 trading days to month-end t (at least 200 days). Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

## 5. Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = calmest stocks (lowest 252-day volatility) minus most volatile stocks; **long-only** = calmest stocks (lowest 252-day volatility); benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 6. Performance in detail

**US (S&P 500 members, point-in-time)**, median 502 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -8.7% | -11.6% | 25.9% | -0.34 [-0.79, 0.14] | -0.55 | -84% | 45% | -1.36 | -1.01 | +4.6% (1.1) | 19.7% |
| Long-only (net) | +10.6% | +10.4% | 12.0% | 0.89 [0.51, 1.34] | 1.41 | -21% | 64% | 5.13 | 0.57 | +3.2% (1.7) | 6.9% |
| Calmest stocks (gross) | +10.9% | +10.7% | 12.0% | 0.91 [0.53, 1.36] | 1.45 | -21% | 64% | 5.25 | 0.57 | +3.4% (1.9) | 6.9% |
| Most volatile stocks (gross) | +18.0% | +14.9% | 28.6% | 0.63 [0.20, 1.11] | 0.89 | -44% | 61% | 2.72 | 1.58 | -2.8% (-0.9) | 15.0% |
| EW universe | +13.1% | +12.6% | 15.5% | 0.85 [0.41, 1.42] | 1.29 | -28% | 67% | 4.20 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.9% | +14.9% | 14.2% | 1.05 [0.60, 1.61] | 1.73 | -24% | 69% | 5.29 | 0.86 | +3.7% (2.4) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 264 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +1.6% | -0.4% | 19.9% | 0.08 [-0.45, 0.68] | -0.03 | -58% | 52% | 0.28 | -0.87 | +10.9% (2.4) | 13.1% |
| Long-only (net) | +11.0% | +11.0% | 10.3% | 1.07 [0.51, 1.76] | 1.69 | -21% | 67% | 4.53 | 0.56 | +5.0% (2.6) | 6.3% |
| Calmest stocks (gross) | +11.3% | +11.3% | 10.3% | 1.10 [0.54, 1.79] | 1.74 | -21% | 68% | 4.64 | 0.56 | +5.2% (2.8) | 6.2% |
| Most volatile stocks (gross) | +8.2% | +5.7% | 23.4% | 0.35 [-0.17, 0.87] | 0.40 | -51% | 53% | 1.27 | 1.43 | -7.1% (-2.1) | 11.7% |
| EW universe | +10.8% | +10.2% | 14.4% | 0.75 [0.29, 1.30] | 1.14 | -26% | 63% | 3.20 | 1.00 | – | 8.4% |
| Size-weighted universe | +10.6% | +10.2% | 13.7% | 0.77 [0.32, 1.29] | 1.21 | -25% | 58% | 3.37 | 0.92 | +0.8% (0.6) | 7.9% |

**UK (FTSE 350, point-in-time)**, median 326 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -6.0% | -8.2% | 21.5% | -0.28 [-0.82, 0.30] | -0.46 | -79% | 52% | -0.96 | -0.92 | +2.8% (0.6) | 16.5% |
| Long-only (net) | +8.4% | +8.3% | 9.1% | 0.93 [0.41, 1.58] | 1.37 | -20% | 64% | 4.38 | 0.57 | +2.9% (2.8) | 6.1% |
| Calmest stocks (gross) | +8.6% | +8.5% | 9.1% | 0.94 [0.43, 1.60] | 1.40 | -20% | 64% | 4.48 | 0.57 | +3.1% (3.0) | 6.0% |
| Most volatile stocks (gross) | +13.4% | +10.6% | 26.2% | 0.51 [0.01, 1.06] | 0.70 | -46% | 53% | 1.87 | 1.50 | -0.9% (-0.2) | 13.8% |
| EW universe | +9.6% | +8.9% | 14.2% | 0.68 [0.19, 1.28] | 0.95 | -30% | 58% | 2.87 | 1.00 | – | 8.8% |
| Size-weighted universe | +8.4% | +7.8% | 12.9% | 0.65 [0.16, 1.25] | 0.90 | -28% | 62% | 2.68 | 0.84 | +0.3% (0.2) | 7.8% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -1.1% | -2.7% | 18.1% | -0.06 [-0.66, 0.50] | -0.20 | -57% | 51% | -0.21 | -0.66 | +7.2% (1.8) | 11.1% |
| Long-only (net) | +13.3% | +13.3% | 12.4% | 1.07 [0.58, 1.58] | 1.85 | -19% | 63% | 4.53 | 0.68 | +4.8% (2.4) | 6.5% |
| Calmest stocks (gross) | +13.5% | +13.5% | 12.4% | 1.08 [0.60, 1.60] | 1.89 | -19% | 63% | 4.60 | 0.68 | +5.0% (2.5) | 6.5% |
| Most volatile stocks (gross) | +13.5% | +11.6% | 22.4% | 0.60 [0.05, 1.25] | 0.82 | -46% | 63% | 2.18 | 1.34 | -3.3% (-1.3) | 13.3% |
| EW universe | +12.6% | +12.0% | 15.2% | 0.83 [0.31, 1.44] | 1.27 | -33% | 66% | 3.31 | 1.00 | – | 8.8% |
| Size-weighted universe | +11.1% | +10.2% | 16.4% | 0.68 [0.11, 1.33] | 0.94 | -40% | 62% | 2.55 | 0.93 | -0.6% (-0.2) | 10.7% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -3.1% | -4.5% | 16.9% | -0.19 [-0.79, 0.38] | -0.35 | -71% | 49% | -0.63 | -0.74 | +6.1% (1.7) | 10.1% |
| Long-only (net) | +12.2% | +12.3% | 10.8% | 1.13 [0.65, 1.70] | 1.89 | -15% | 67% | 5.05 | 0.66 | +3.9% (2.6) | 6.4% |
| Calmest stocks (gross) | +12.4% | +12.5% | 10.8% | 1.15 [0.67, 1.73] | 1.93 | -15% | 67% | 5.15 | 0.66 | +4.1% (2.7) | 6.4% |
| Most volatile stocks (gross) | +14.2% | +12.5% | 21.9% | 0.65 [0.10, 1.28] | 0.92 | -45% | 61% | 2.35 | 1.39 | -3.3% (-1.4) | 12.4% |
| EW universe | +12.6% | +12.3% | 14.2% | 0.89 [0.37, 1.51] | 1.38 | -29% | 66% | 3.63 | 1.00 | – | 8.4% |
| Size-weighted universe | +11.4% | +11.0% | 13.5% | 0.84 [0.37, 1.41] | 1.32 | -26% | 63% | 3.59 | 0.90 | -0.0% (-0.0) | 8.1% |

**World (US + UK + EU, point-in-time)**, median 1088 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -5.7% | -7.7% | 20.8% | -0.27 [-0.75, 0.22] | -0.46 | -75% | 47% | -1.05 | -0.89 | +4.3% (1.4) | 14.9% |
| Long-only (net) | +9.4% | +9.2% | 11.0% | 0.85 [0.40, 1.43] | 1.25 | -21% | 65% | 4.48 | 0.60 | +2.7% (2.1) | 7.2% |
| Calmest stocks (gross) | +9.6% | +9.4% | 11.0% | 0.87 [0.42, 1.46] | 1.29 | -21% | 65% | 4.59 | 0.60 | +2.9% (2.3) | 7.2% |
| Most volatile stocks (gross) | +13.9% | +11.0% | 26.4% | 0.53 [0.05, 1.06] | 0.70 | -43% | 55% | 2.10 | 1.49 | -2.9% (-1.1) | 13.8% |
| EW universe | +11.3% | +10.5% | 16.0% | 0.71 [0.25, 1.28] | 1.02 | -30% | 61% | 3.07 | 1.00 | – | 9.7% |
| Size-weighted universe | +11.0% | +10.3% | 14.8% | 0.74 [0.28, 1.31] | 1.10 | -28% | 61% | 3.19 | 0.91 | +0.7% (0.8) | 8.9% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -13.0% | -25.9% | +4.8% | -30.1% | -14.3% | -9.4% |
| 2014 | +0.5% | +58.0% | +6.5% | -17.7% | +11.7% | +17.3% |
| 2015 | +22.6% | +22.0% | +3.6% | -12.5% | -10.5% | +16.5% |
| 2016 | -17.0% | -30.0% | -53.5% | -19.9% | -34.8% | -31.0% |
| 2017 | +0.3% | -11.0% | -23.8% | +18.6% | -5.0% | -17.2% |
| 2018 | +6.1% | +22.5% | -2.4% | -4.3% | +8.4% | +7.0% |
| 2019 | -8.8% | -16.7% | +18.5% | +33.8% | -17.7% | -8.3% |
| 2020 | -36.0% | -22.1% | -33.3% | -30.1% | -30.9% | -29.6% |
| 2021 | -18.4% | +11.4% | -1.4% | +10.7% | -7.1% | -9.1% |
| 2022 | +10.5% | +1.9% | +19.3% | +17.1% | +24.8% | +14.9% |
| 2023 | -25.9% | +0.7% | -12.2% | -11.0% | -8.5% | -16.2% |
| 2024 | +6.4% | +8.9% | +2.0% | +14.3% | +31.8% | +5.8% |
| 2025 | -28.8% | -0.1% | +2.1% | +26.5% | +22.5% | -12.7% |
| 2026 | -32.8% | +7.0% | -7.7% | -3.2% | -4.0% | -14.7% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +17.9% | +14.1% | +15.8% | +22.0% | +17.9% | +20.2% |
| 2014 | +18.4% | +19.4% | +8.6% | +9.3% | +19.8% | +10.8% |
| 2015 | +6.1% | +11.6% | +7.7% | +27.1% | +5.7% | +4.3% |
| 2016 | +10.7% | +2.1% | +8.6% | +0.6% | +13.4% | +2.7% |
| 2017 | +14.0% | +14.0% | +15.6% | +24.2% | +13.5% | +16.6% |
| 2018 | +3.5% | +5.6% | -4.6% | -13.9% | +2.1% | -2.8% |
| 2019 | +24.8% | +18.8% | +21.9% | +43.3% | +25.0% | +21.4% |
| 2020 | +7.4% | -12.6% | -2.3% | +17.9% | +1.2% | +3.9% |
| 2021 | +19.7% | +24.6% | +11.9% | +25.6% | +17.1% | +12.8% |
| 2022 | -2.1% | -7.8% | -9.6% | -9.0% | -4.3% | -7.8% |
| 2023 | -0.6% | +15.5% | +4.9% | +2.6% | +7.3% | +4.8% |
| 2024 | +14.0% | +13.6% | +9.8% | +10.2% | +12.4% | +11.2% |
| 2025 | +5.9% | +19.2% | +16.5% | +25.7% | +23.2% | +19.6% |
| 2026 | +4.9% | +18.5% | +12.6% | +8.7% | +16.4% | +11.3% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS04_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 10% | 9% | 45% | -29.9% | 2020-11 |
| EU | 163 | 27 / 26 | 10% | 10% | 52% | -29.1% | 2020-11 |
| UK | 163 | 33 / 32 | 8% | 10% | 52% | -33.7% | 2020-11 |
| DK | 163 | 7 / 6 | 9% | 8% | 51% | -14.0% | 2020-11 |
| SCANDI | 163 | 14 / 14 | 9% | 9% | 49% | -13.3% | 2020-11 |
| World | 163 | 109 / 108 | 9% | 9% | 47% | -28.4% | 2020-11 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: calmest stocks | Short: most volatile stocks |
|---|---|---|
| US | BRK.B, ATO, REG, DUK, FE, WEC, EVRG, O | MRNA, SNDK, LITE, SMCI, COHR, MU, MRVL, WDC |
| EU | IVG.MI, OBEL.BR, INGA.BR, IBE.MC, TRYG.CO, SRG.MI, SAMPO.HE, LOG.MC | NYR.BR, AVIO.MI, ZEAL.CO, ORSTED.CO, NOKIA.HE, BESI.AS, STMMI.MI, STMPA.PA |
| UK | CGT.L, PNL.L, TFIF.L, RICA.L, SAIN.L, BHMG.L, ALW.L, MYI.L | CWR.L, RPI.L, GDWN.L, ROR.L, TRST.L, SPI.L, SSIT.L, OCDO.L |
| DK | TRYG.CO, JYSK.CO, NDA-DK.CO, DANSKE.CO, ISS.CO, CARL-B.CO, NSIS-B.CO, COLO-B.CO | ZEAL.CO, ORSTED.CO, NOVO-B.CO, GN.CO, VWS.CO, PNDORA.CO, MAERSK-B.CO, AMBU-B.CO |
| SCANDI | TRYG.CO, SAMPO.HE, SHB-A.ST, INVE-B.ST, SWED-A.ST, NDA-SE.ST, SEB-A.ST, KESKOB.HE | ZEAL.CO, ORSTED.CO, NOKIA.HE, QTCOM.HE, NOVO-B.CO, GN.CO, BOL.ST, VWS.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -6.8% | -3.06 | 0.86 | value -0.98 (-11.0), low_risk +2.39 (+16.0), short_term_reversal -0.53 (-2.6) |
| EU | French Europe 5F + WML | -1.4% | -0.29 | 0.53 | Mkt-RF -0.51 (-5.7), RMW +1.32 (+4.4), WML +0.47 (+2.9) |
| UK | JKP GBR 7 themes | -11.5% | -2.51 | 0.70 | value +0.45 (+2.0), momentum +0.37 (+2.4), low_risk +2.13 (+8.6), quality +0.81 (+2.9) |
| DK | JKP DNK 7 themes | +0.4% | 0.12 | 0.63 | momentum +0.22 (+2.1), low_risk +1.38 (+9.8) |
| SCANDI | French Europe 5F + WML | -5.3% | -1.57 | 0.34 | Mkt-RF -0.41 (-4.8), SMB -0.60 (-3.5), HML +0.37 (+2.1), WML +0.43 (+3.7) |
| World | JKP World 7 themes | -5.3% | -1.52 | 0.74 | value -0.45 (-2.7), low_risk +1.66 (+9.9), short_term_reversal -0.72 (-2.6) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +1.9% | 1.39 | 0.82 | mkt +0.92 (+24.6), size -0.26 (-3.3), value -0.22 (-3.2), low_risk +0.95 (+9.6) |
| EU | French Europe 5F + WML | +4.4% | 1.57 | 0.55 | Mkt-RF +0.52 (+11.0), RMW +0.54 (+2.6), WML +0.15 (+2.6) |
| UK | JKP GBR 7 themes | +3.5% | 2.03 | 0.62 | mkt +0.40 (+9.5), momentum +0.17 (+2.6), quality +0.23 (+2.4) |
| DK | JKP DNK 7 themes | +7.3% | 2.80 | 0.59 | mkt +0.63 (+13.7), low_risk +0.23 (+2.9), quality +0.18 (+2.4) |
| SCANDI | French Europe 5F + WML | +7.7% | 2.97 | 0.50 | Mkt-RF +0.51 (+11.2) |
| World | JKP World 7 themes | +4.0% | 2.15 | 0.74 | mkt +0.68 (+13.8), low_risk +0.61 (+5.9) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 1 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** +2.8% to +10.9%, |t| past the gate in 0 of 6.
- **Long-only:** Sharpe above the equal-weight universe in all six; alpha +2.7% to +5.0%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.10, EU 0.62, UK 0.14, DK 0.41, SCANDI 0.25, World 0.15.
- **Publication decay:** gross L/S -8.2% to +2.0% a year in 2013–19 against -15.8% to +5.1% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +1.3% | -0.94 | -12.3% | +13.6% | -0.5% | +0.4% | +1.0% | 20% | 2013-05 -13%, 2016-04 -12%, 2015-04 -9% |
| EU | +2.0% | -1.00 | -10.7% | +12.7% | -0.5% | +1.5% | +0.5% | 19% | 2015-02 -13%, 2016-03 -12%, 2016-10 -11% |
| UK | -7.9% | -0.74 | -8.6% | +0.7% | -0.4% | -1.3% | -6.5% | 16% | 2016-04 -18%, 2016-02 -17%, 2016-06 -11% |
| DK | -4.9% | -0.53 | -8.1% | +3.2% | -0.4% | -0.5% | -4.4% | 18% | 2013-05 -10%, 2013-02 -9%, 2016-04 -8% |
| SCANDI | -8.2% | -0.70 | -10.7% | +2.4% | -0.4% | -1.6% | -6.6% | 18% | 2019-06 -10%, 2016-06 -10%, 2016-11 -9% |
| World | -2.5% | -0.86 | -9.3% | +6.8% | -0.4% | -0.6% | -2.0% | 18% | 2016-04 -13%, 2016-03 -9%, 2015-02 -8% |

On average across the six universes the gross spread was -3.4% a year, of which the market exposure (beta -0.79) contributed -10.0%; the beta-adjusted spread (CAPM alpha) was +6.6%. Costs took 0.4% a year at 18% monthly turnover across both legs. The long leg beat the universe by -0.4% and the short leg lagged it by -3.0% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +2.7%, +4.1%, +4.1% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.29 | – | -0.14 | – | – | -2.9% | -49% | +6.3% (1.7) | 0.4% |
| X1 beta-neutral legs | 0.48 | +1.04 (p 0.000) | 0.24 | +0.38 (p 0.071) | 6 of 6 | +3.6% | -29% | +2.9% (0.7) | 0.6% |
| X2 + turnover buffer | 0.50 | +0.01 (p 0.495) | 0.08 | -0.15 (p 0.979) | 0 of 6 | +1.1% | -29% | +0.9% (0.3) | 0.3% |
| X3 + volatility targeting | 0.59 | +0.14 (p 0.384) | 0.21 | +0.12 (p 0.206) | 4 of 6 | +2.0% | -22% | +1.9% (0.6) | 0.2% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS04_ladder.png)

- **X1 beta-neutral legs:** +1.04 design, +0.38 holdout; helps in both windows but does not pass the gate.
- **X2 + turnover buffer:** +0.01 design, -0.15 holdout; helps in one window and hurts in the other: not reliable.
- **X3 + volatility targeting:** +0.14 design, +0.12 holdout; helps in both windows but does not pass the gate.

**Where it ends:** holdout Sharpe -0.14 → 0.21, return -2.9% → +2.0% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Low volatility |
|---|---|
| Series family | **Low risk** |
| Academic style | Defensive / low-risk anomaly |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 18% of the two legs replaced monthly |
| Market exposure | L/S beta -1.01 to -0.66 |
| Payoff shape | Treynor–Mazuy γ -3.38 to -0.83 (t -7.9 to -0.8); worst 10% of market months +4.4% to +5.8% a month, best 10% -11.0% to -6.3% |
| Nearest factor theme | low_risk (4 of 6 universes), Mkt-RF (2 of 6 universes) |
| Nearest library signals (returns) | Volatility (6 universes), Range (MAX−MIN) (5 universes), Beta (3 universes) |
| Economic rationale | Leverage constraints push investors into high-beta, high-volatility stocks (Black 1972; Frazzini & Pedersen 2014); benchmarked managers cannot exploit it without tracking error (Baker, Bradley & Wurgler 2011); lottery preferences (Bali, Cakici & Whitelaw 2011). |
| Publication | Haugen & Heins 1975; Ang et al. 2006; Blitz & van Vliet 2007; widely sold as min-vol ETFs since 2011 |
| Where it fits | In the **low risk** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **MAX**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Volatility (252 days) **(this strategy)** | low risk | +1.00 | +1.00 | +2.4% | -12.9% to -4.8% | 0 / 3 |
| Volatility | low risk | +0.84 | +0.92 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| Beta | low risk | +0.66 | +0.86 | +4.4% | -12.6% to -4.2% | 0 / 4 |
| Range (MAX−MIN) | low risk | +0.61 | +0.84 | -0.7% | -15.4% to -4.8% | 0 / 4 |
| MIN5 | low risk | -0.58 | -0.82 | -0.9% | +2.3% to +13.7% | 4 / 0 |
| MAX5 | low risk | +0.61 | +0.79 | +0.6% | -11.3% to -3.5% | 0 / 2 |
| MAX (best day) (mirror) | low risk | +0.54 | +0.78 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| MIN (worst day) | low risk | -0.50 | -0.78 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| Idiosyncratic vol | low risk | +0.59 | +0.77 | -3.6% | -15.5% to -4.8% | 0 / 4 |
| Near 52-week high | momentum | -0.44 | -0.74 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| 55-day breakout | momentum | -0.31 | -0.63 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| Momentum 12-1 | momentum | -0.15 | -0.50 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| Size | size | -0.07 | -0.33 | +0.1% | -3.8% to +9.9% | 1 / 0 |
| Last month return | short-term reversal | +0.00 | -0.28 | +1.8% | -3.2% to +11.0% | 2 / 0 |
| Residual momentum | momentum | -0.05 | -0.26 | +6.4% | +8.0% to +12.2% | 6 / 0 |
| Same-month seasonality | seasonality | +0.08 | -0.10 | -1.9% | -9.4% to +6.6% | 0 / 1 |
| Skewness | tail direction | +0.06 | +0.10 | -0.4% | -6.7% to +3.9% | 0 / 2 |
| Above 52-week low | momentum | +0.23 | +0.04 | +7.5% | +5.2% to +13.6% | 4 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.05 | -0.01 | -0.9% | -5.2% to +5.2% | 0 / 0 |

![360 map](../figures/xs_FS04_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | +1.2% | 0.92 | 0.96 | Volatility +0.51 (+5.8), Range +0.24 (+3.1), Beta +0.31 (+6.4) |
| EU | -0.6% | -0.27 | 0.88 | Volatility +0.77 (+9.1), Beta +0.12 (+2.1) |
| UK | +5.4% | 2.47 | 0.89 | Volatility +0.46 (+5.3), Idiosyncratic vol +0.43 (+4.4), Range -0.27 (-2.5), Beta +0.28 (+5.8) |
| DK | -3.0% | -1.49 | 0.85 | Beta +0.52 (+8.4), Volatility +0.29 (+4.7), Idiosyncratic vol +0.18 (+2.4) |
| SCANDI | -0.7% | -0.38 | 0.82 | Volatility +0.64 (+7.9) |
| World | +2.6% | 2.17 | 0.95 | Volatility +0.56 (+6.7), Beta +0.33 (+7.1), Range -0.26 (-2.4), Idiosyncratic vol +0.32 (+4.3) |

![Double sort](../figures/xs_FS04_dsort.png)

Holding MAX fixed (down a column), moving from low to high Volatility changes the return by +3.4, +3.8 and +3.7 points a year; holding Volatility fixed (along a row), moving from low to high MAX changes it by -3.2, +0.6 and -3.0.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): +24% vs -36% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +2.4%, +2.7%, +4.1%, +4.1% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## 13. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Not a registered trial.** Descriptive; the fix ladder is counted inside FS03–FS12 (25 trials).

## 14. Academic references

- Haugen, R. & Heins, A. J. (1975). Risk and the rate of return on financial assets: Some old wine in new bottles. *Journal of Financial and Quantitative Analysis*, 10(5), 775–784.
- Ang, A., Hodrick, R., Xing, Y. & Zhang, X. (2006). The cross-section of volatility and expected returns. *Journal of Finance*, 61(1), 259–299.
- Blitz, D. & van Vliet, P. (2007). The volatility effect. *Journal of Portfolio Management*, 34(1), 102–113.
- Baker, M., Bradley, B. & Wurgler, J. (2011). Benchmarks as limits to arbitrage: Understanding the low-volatility anomaly. *Financial Analysts Journal*, 67(1), 40–54.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics*, 111(1), 1–25.
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

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS04` → `build_xs.py FS04`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.
