# FACTSHEET FS04 · Low volatility

### Do calm stocks beat exciting ones?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

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

> **The claim.** Low-volatility stocks earn about the same or more than high-volatility stocks, so their risk-adjusted return is far higher, contradicting the CAPM. Blitz & van Vliet (2007) documented it globally for 1986–2006; Ang, Hodrick, Xing & Zhang (2006) for idiosyncratic volatility. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -15.3% to -1.6% a year and was positive in none of the six; no universe passes the 2.87 gate. The long-only book (calmest stocks) had a higher Sharpe than the equal-weight universe in 5 of the six (EU, UK, DK, SCANDI, World), with alphas of +2.1% to +4.3%, passing the gate in UK. **What goes wrong (§10):** the main drags are a market bet (average beta -0.75, worth -10.0% a year in 2013–19). None of the pre-declared fixes passes the gate in both windows. **Classification (§11):** Low risk; its returns sit closest to the low risk cluster of the signal library. **360° view (§12):** nearest neighbours Volatility, Range (MAX−MIN); after its closest neighbours and the market it keeps an alpha of -2.1% to +6.6% (largest |t| 3.0), so it carries some information of its own.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 501 / 10 | -15.3% | -2.29 | -1.6% (-0.3) | -0.95 | +10.3% | 0.89 | -21% | +14.1% | 0.95 | +15.3% |
| EU | 238 / 10 | -1.6% | -0.29 | +8.4% (2.2) | -0.88 | +10.8% | 1.03 | -22% | +10.9% | 0.78 | +10.1% |
| UK | 239 / 10 | -6.3% | -1.05 | +3.5% (0.8) | -0.94 | +9.3% | 1.02 | -19% | +9.9% | 0.74 | +8.5% |
| DK | 19 / 3 | -1.6% | -0.29 | +7.5% (1.8) | -0.71 | +12.2% | 0.98 | -20% | +12.3% | 0.82 | +10.3% |
| SCANDI | 62 / 5 | -4.2% | -0.92 | +4.3% (1.2) | -0.67 | +11.1% | 1.02 | -16% | +12.5% | 0.91 | +10.7% |
| World | 971 / 10 | -9.7% | -1.86 | +0.9% (0.3) | -0.84 | +9.7% | 0.89 | -21% | +11.9% | 0.80 | +10.8% |

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
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: top 500 by market cap each month-end (Sharadar filings × price, A06 method) | ~499 | USD |
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

**US (top 500, point-in-time)**, median 501 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -15.3% | -17.2% | 25.5% | -0.60 [-1.08, -0.08] | -0.80 | -93% | 46% | -2.29 | -0.95 | -1.6% (-0.3) | 19.9% |
| Long-only (net) | +10.6% | +10.3% | 12.0% | 0.89 [0.51, 1.33] | 1.40 | -21% | 64% | 5.12 | 0.59 | +2.1% (1.1) | 6.8% |
| Calmest stocks (gross) | +10.9% | +10.6% | 12.0% | 0.91 [0.53, 1.36] | 1.45 | -21% | 64% | 5.25 | 0.59 | +2.4% (1.2) | 6.8% |
| Most volatile stocks (gross) | +24.7% | +23.1% | 27.8% | 0.89 [0.42, 1.40] | 1.51 | -37% | 63% | 3.68 | 1.53 | +2.5% (0.8) | 14.6% |
| EW universe | +14.4% | +14.1% | 15.1% | 0.95 [0.52, 1.53] | 1.52 | -25% | 68% | 4.79 | 1.00 | – | 8.9% |
| Size-weighted universe | +15.4% | +15.3% | 14.4% | 1.07 [0.61, 1.64] | 1.79 | -24% | 69% | 5.27 | 0.90 | +2.4% (1.8) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -1.6% | -3.8% | 20.6% | -0.08 [-0.56, 0.47] | -0.24 | -63% | 50% | -0.29 | -0.88 | +8.4% (2.2) | 14.6% |
| Long-only (net) | +10.8% | +10.8% | 10.5% | 1.03 [0.47, 1.73] | 1.58 | -22% | 65% | 4.40 | 0.58 | +4.3% (2.1) | 6.5% |
| Calmest stocks (gross) | +11.1% | +11.0% | 10.5% | 1.05 [0.49, 1.76] | 1.62 | -22% | 66% | 4.50 | 0.58 | +4.5% (2.2) | 6.5% |
| Most volatile stocks (gross) | +11.3% | +8.8% | 24.2% | 0.47 [-0.01, 0.96] | 0.61 | -37% | 54% | 1.83 | 1.45 | -5.2% (-2.0) | 11.6% |
| EW universe | +11.4% | +10.9% | 14.5% | 0.78 [0.33, 1.33] | 1.22 | -26% | 64% | 3.34 | 1.00 | – | 8.3% |
| Size-weighted universe | +10.7% | +10.1% | 14.3% | 0.75 [0.28, 1.28] | 1.14 | -26% | 60% | 3.12 | 0.95 | -0.2% (-0.1) | 8.3% |

**UK (FTSE 350, point-in-time)**, median 239 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -6.3% | -8.4% | 21.2% | -0.30 [-0.85, 0.23] | -0.49 | -82% | 47% | -1.05 | -0.94 | +3.5% (0.8) | 15.5% |
| Long-only (net) | +9.4% | +9.3% | 9.2% | 1.02 [0.50, 1.66] | 1.56 | -19% | 67% | 4.97 | 0.57 | +3.4% (3.0) | 6.0% |
| Calmest stocks (gross) | +9.6% | +9.5% | 9.2% | 1.04 [0.52, 1.68] | 1.59 | -19% | 67% | 5.07 | 0.57 | +3.6% (3.1) | 6.0% |
| Most volatile stocks (gross) | +14.7% | +12.0% | 26.0% | 0.57 [0.08, 1.13] | 0.77 | -40% | 57% | 2.16 | 1.51 | -1.2% (-0.3) | 14.1% |
| EW universe | +10.5% | +9.9% | 14.1% | 0.74 [0.26, 1.34] | 1.08 | -29% | 60% | 3.23 | 1.00 | – | 8.8% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.71 [0.21, 1.31] | 1.01 | -27% | 62% | 2.94 | 0.82 | +0.4% (0.2) | 7.7% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -1.6% | -3.3% | 19.1% | -0.08 [-0.71, 0.49] | -0.24 | -64% | 52% | -0.29 | -0.71 | +7.5% (1.8) | 12.0% |
| Long-only (net) | +12.4% | +12.2% | 12.6% | 0.98 [0.52, 1.48] | 1.67 | -20% | 60% | 4.13 | 0.65 | +4.0% (2.0) | 6.7% |
| Calmest stocks (gross) | +12.6% | +12.4% | 12.7% | 0.99 [0.53, 1.49] | 1.70 | -19% | 61% | 4.20 | 0.65 | +4.2% (2.1) | 6.6% |
| Most volatile stocks (gross) | +13.1% | +10.9% | 23.5% | 0.56 [0.00, 1.21] | 0.73 | -49% | 60% | 2.01 | 1.36 | -4.3% (-1.6) | 14.0% |
| EW universe | +12.8% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.25 | -33% | 64% | 3.20 | 1.00 | – | 9.3% |
| Size-weighted universe | +11.2% | +10.3% | 16.6% | 0.68 [0.11, 1.32] | 0.94 | -40% | 61% | 2.52 | 0.92 | -0.5% (-0.2) | 10.8% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -4.2% | -5.4% | 16.2% | -0.26 [-0.88, 0.30] | -0.44 | -73% | 47% | -0.92 | -0.67 | +4.3% (1.2) | 9.7% |
| Long-only (net) | +11.2% | +11.1% | 10.9% | 1.02 [0.54, 1.60] | 1.65 | -16% | 65% | 4.31 | 0.67 | +2.6% (1.7) | 6.5% |
| Calmest stocks (gross) | +11.4% | +11.4% | 10.9% | 1.04 [0.56, 1.63] | 1.70 | -16% | 65% | 4.40 | 0.67 | +2.9% (1.8) | 6.5% |
| Most volatile stocks (gross) | +14.4% | +13.0% | 21.0% | 0.69 [0.13, 1.32] | 1.01 | -46% | 61% | 2.49 | 1.33 | -2.7% (-1.1) | 11.7% |
| EW universe | +12.8% | +12.5% | 14.1% | 0.91 [0.39, 1.54] | 1.42 | -29% | 67% | 3.62 | 1.00 | – | 8.3% |
| Size-weighted universe | +11.2% | +10.7% | 13.9% | 0.80 [0.31, 1.37] | 1.21 | -27% | 63% | 3.26 | 0.95 | -1.0% (-0.9) | 8.6% |

**World (US + UK + EU, point-in-time)**, median 971 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -9.7% | -11.1% | 20.1% | -0.48 [-0.95, 0.02] | -0.68 | -83% | 45% | -1.86 | -0.84 | +0.9% (0.3) | 14.4% |
| Long-only (net) | +9.9% | +9.7% | 11.1% | 0.89 [0.43, 1.46] | 1.32 | -21% | 66% | 4.82 | 0.61 | +2.2% (1.6) | 7.1% |
| Calmest stocks (gross) | +10.2% | +10.0% | 11.2% | 0.91 [0.45, 1.48] | 1.36 | -21% | 66% | 4.93 | 0.61 | +2.5% (1.7) | 7.1% |
| Most volatile stocks (gross) | +18.5% | +16.4% | 25.4% | 0.73 [0.24, 1.26] | 1.12 | -41% | 59% | 2.94 | 1.45 | +0.3% (0.1) | 13.2% |
| EW universe | +12.5% | +11.9% | 15.7% | 0.80 [0.33, 1.38] | 1.20 | -29% | 64% | 3.53 | 1.00 | – | 9.4% |
| Size-weighted universe | +11.4% | +10.8% | 15.0% | 0.76 [0.29, 1.33] | 1.14 | -28% | 63% | 3.23 | 0.94 | -0.4% (-0.5) | 9.0% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -17.8% | -28.7% | +1.8% | -34.5% | -18.8% | -13.5% |
| 2014 | -5.9% | +27.8% | +10.7% | -28.5% | +0.4% | +5.2% |
| 2015 | +12.4% | +5.1% | +20.4% | -14.0% | -13.4% | +11.7% |
| 2016 | -6.0% | -31.5% | -55.4% | -18.1% | -27.8% | -23.8% |
| 2017 | -10.5% | -4.9% | -24.8% | +17.1% | -2.6% | -18.3% |
| 2018 | +7.1% | +21.5% | -7.8% | +3.5% | +0.0% | +6.8% |
| 2019 | -15.3% | -7.8% | +0.2% | +27.2% | -13.3% | -11.9% |
| 2020 | -48.1% | -28.6% | -28.6% | -29.8% | -34.7% | -35.8% |
| 2021 | -14.4% | +1.9% | -2.0% | +16.3% | -2.7% | -12.0% |
| 2022 | +29.6% | +1.2% | +17.2% | +18.4% | +26.4% | +20.2% |
| 2023 | -38.4% | +1.0% | -7.8% | -9.9% | -8.7% | -24.1% |
| 2024 | -18.9% | +9.4% | +3.0% | +17.4% | +27.5% | -4.5% |
| 2025 | -35.7% | -1.3% | +3.4% | +25.0% | +22.6% | -18.0% |
| 2026 | -36.8% | +5.7% | -9.5% | -3.1% | -4.8% | -16.3% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +17.1% | +15.4% | +18.9% | +18.5% | +20.5% | +19.9% |
| 2014 | +17.2% | +16.1% | +9.0% | -2.7% | +15.0% | +12.1% |
| 2015 | +5.7% | +11.2% | +12.0% | +24.7% | +4.4% | +5.1% |
| 2016 | +11.4% | +2.8% | +8.5% | +2.4% | +12.5% | +5.1% |
| 2017 | +14.1% | +16.5% | +18.0% | +22.3% | +13.1% | +16.5% |
| 2018 | +3.9% | +5.0% | -2.8% | -9.4% | -1.6% | -1.6% |
| 2019 | +25.3% | +21.4% | +24.4% | +34.8% | +21.9% | +24.3% |
| 2020 | +7.9% | -14.0% | -1.3% | +20.6% | -1.1% | +4.3% |
| 2021 | +19.5% | +17.7% | +10.2% | +33.3% | +18.8% | +11.2% |
| 2022 | -2.4% | -7.0% | -8.8% | -10.7% | -6.0% | -7.5% |
| 2023 | -0.3% | +16.3% | +4.6% | +0.9% | +6.4% | +4.2% |
| 2024 | +14.3% | +13.8% | +9.3% | +11.1% | +11.9% | +11.1% |
| 2025 | +5.9% | +19.3% | +17.0% | +24.3% | +24.2% | +19.8% |
| 2026 | +4.6% | +18.5% | +12.8% | +8.7% | +16.3% | +11.7% |

## 7. Trading record

The rebalance log per universe is in `results/xs_FS04_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 11% | 11% | 46% | -26.9% | 2020-04 |
| EU | 163 | 24 / 23 | 10% | 10% | 50% | -30.0% | 2020-11 |
| UK | 163 | 24 / 23 | 8% | 10% | 47% | -31.7% | 2020-11 |
| DK | 163 | 7 / 6 | 8% | 8% | 52% | -13.9% | 2023-11 |
| SCANDI | 163 | 13 / 12 | 10% | 8% | 47% | -14.1% | 2020-11 |
| World | 163 | 98 / 97 | 10% | 10% | 45% | -26.3% | 2020-11 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: calmest stocks | Short: most volatile stocks |
|---|---|---|
| US | BRK.B, ATO, REG, DUK, FE, WEC, EVRG, L | MRNA, SNDK, LITE, SMCI, COHR, MU, MRVL, WDC |
| EU | IVG.MI, OBEL.BR, INGA.BR, IBE.MC, TRYG.CO, SRG.MI, SAMPO.HE, LOG.MC | NYR.BR, AVIO.MI, ZEAL.CO, ORSTED.CO, NOKIA.HE, BESI.AS, STMMI.MI, STMPA.PA |
| UK | CGT.L, PNL.L, TFIF.L, RICA.L, SAIN.L, BHMG.L, ALW.L, MYI.L | CWR.L, RPI.L, GDWN.L, ROR.L, TRST.L, SPI.L, SSIT.L, OCDO.L |
| DK | TRYG.CO, JYSK.CO, NDA-DK.CO, DANSKE.CO, ISS.CO, CARL-B.CO, NSIS-B.CO, COLO-B.CO | ZEAL.CO, ORSTED.CO, NOVO-B.CO, GN.CO, VWS.CO, PNDORA.CO, MAERSK-B.CO, AMBU-B.CO |
| SCANDI | TRYG.CO, SAMPO.HE, SHB-A.ST, INVE-B.ST, SWED-A.ST, NDA-SE.ST, SEB-A.ST, KESKOB.HE | ZEAL.CO, ORSTED.CO, NOKIA.HE, QTCOM.HE, NOVO-B.CO, GN.CO, BOL.ST, VWS.CO |

## 8. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -11.9% | -5.48 | 0.86 | value -0.54 (-4.7), low_risk +2.57 (+15.3) |
| EU | French Europe 5F + WML | -4.8% | -1.18 | 0.54 | Mkt-RF -0.49 (-5.6), SMB -0.41 (-2.0), RMW +1.39 (+4.4), CMA +0.65 (+2.1), WML +0.49 (+3.0) |
| UK | JKP GBR 7 themes | -10.3% | -2.35 | 0.74 | low_risk +2.13 (+7.5), quality +0.80 (+2.8) |
| DK | JKP DNK 7 themes | +1.1% | 0.28 | 0.62 | low_risk +1.48 (+9.8) |
| SCANDI | French Europe 5F + WML | -6.7% | -2.10 | 0.34 | Mkt-RF -0.37 (-4.2), SMB -0.49 (-3.0), HML +0.38 (+2.2), WML +0.42 (+3.6) |
| World | JKP World 7 themes | -9.9% | -3.36 | 0.74 | low_risk +1.79 (+10.8) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +1.8% | 1.33 | 0.82 | mkt +0.92 (+24.3), size -0.26 (-3.3), value -0.22 (-3.3), low_risk +0.94 (+9.5) |
| EU | French Europe 5F + WML | +4.2% | 1.41 | 0.56 | Mkt-RF +0.53 (+10.4), RMW +0.57 (+2.5), WML +0.13 (+2.0) |
| UK | JKP GBR 7 themes | +4.3% | 2.43 | 0.61 | mkt +0.41 (+9.6), momentum +0.20 (+3.2), quality +0.22 (+2.2) |
| DK | JKP DNK 7 themes | +6.9% | 2.62 | 0.57 | mkt +0.63 (+15.4), value +0.10 (+2.1), low_risk +0.25 (+3.3), quality +0.16 (+2.1) |
| SCANDI | French Europe 5F + WML | +6.8% | 2.62 | 0.50 | Mkt-RF +0.51 (+10.4) |
| World | JKP World 7 themes | +4.4% | 2.23 | 0.73 | mkt +0.69 (+13.2), momentum +0.15 (+2.1), low_risk +0.65 (+5.9) |

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in none of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -1.6% to +8.4%, |t| past the gate in 0 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 5 of the six; alpha +2.1% to +4.3%, passing in 1 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.01, EU 0.38, UK 0.13, DK 0.38, SCANDI 0.17, World 0.03.
- **Publication decay:** gross L/S -9.9% to -1.8% a year in 2013–19 against -25.0% to +6.7% in 2020–26.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 10.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | -3.1% | -0.84 | -11.7% | +8.7% | -0.6% | -0.6% | -2.4% | 23% | 2013-05 -12%, 2019-11 -9%, 2019-01 -8% |
| EU | -1.8% | -0.99 | -11.4% | +9.7% | -0.5% | +0.9% | -2.7% | 19% | 2013-04 -14%, 2015-02 -14%, 2016-03 -13% |
| UK | -9.5% | -0.70 | -9.2% | -0.3% | -0.4% | -1.1% | -8.4% | 17% | 2016-02 -18%, 2016-04 -15%, 2016-06 -13% |
| DK | -7.5% | -0.55 | -8.4% | +0.9% | -0.4% | -2.8% | -4.7% | 18% | 2013-05 -12%, 2013-02 -12%, 2014-05 -9% |
| SCANDI | -9.9% | -0.56 | -8.7% | -1.2% | -0.5% | -3.3% | -6.6% | 20% | 2013-09 -9%, 2018-02 -9%, 2013-02 -8% |
| World | -4.9% | -0.84 | -10.4% | +5.4% | -0.5% | -0.8% | -4.1% | 20% | 2016-04 -9%, 2016-07 -8%, 2013-05 -8% |

On average across the six universes the gross spread was -6.1% a year, of which the market exposure (beta -0.75) contributed -10.0%; the beta-adjusted spread (CAPM alpha) was +3.9%. Costs took 0.5% a year at 20% monthly turnover across both legs. The long leg beat the universe by -1.3% and the short leg lagged it by -4.8% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +5.0%, +6.5%, +6.2% a year.

### 10.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.47 | – | -0.27 | – | – | -5.4% | -50% | +4.2% (1.1) | 0.5% |
| X1 beta-neutral legs | 0.34 | +1.13 (p 0.000) | 0.11 | +0.38 (p 0.074) | 6 of 6 | +1.7% | -35% | +1.0% (0.2) | 0.6% |
| X2 + turnover buffer | 0.34 | -0.02 (p 0.586) | 0.01 | -0.10 (p 0.928) | 0 of 6 | +0.1% | -30% | -0.1% (-0.0) | 0.3% |
| X3 + volatility targeting | 0.50 | +0.23 (p 0.295) | 0.18 | +0.17 (p 0.102) | 4 of 6 | +1.8% | -23% | +1.6% (0.5) | 0.2% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS04_ladder.png)

- **X1 beta-neutral legs:** +1.13 design, +0.38 holdout; helps in both windows but does not pass the gate.
- **X2 + turnover buffer:** -0.02 design, -0.10 holdout; hurts in both windows.
- **X3 + volatility targeting:** +0.23 design, +0.17 holdout; helps in both windows but does not pass the gate.

**Where it ends:** holdout Sharpe -0.27 → 0.18, return -5.4% → +1.8% a year (six-universe book).

## 11. Classification: where does it fit?

| Dimension | Low volatility |
|---|---|
| Series family | **Low risk** |
| Academic style | Defensive / low-risk anomaly |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 20% of the two legs replaced monthly |
| Market exposure | L/S beta -0.95 to -0.67 |
| Payoff shape | Treynor–Mazuy γ -3.34 to -0.95 (t -9.0 to -1.1); worst 10% of market months +3.6% to +6.5% a month, best 10% -9.2% to -6.1% |
| Nearest factor theme | low_risk (4 of 6 universes), Mkt-RF (2 of 6 universes) |
| Nearest library signals (returns) | Volatility (6 universes), Range (MAX−MIN) (6 universes), Beta (3 universes) |
| Economic rationale | Leverage constraints push investors into high-beta, high-volatility stocks (Black 1972; Frazzini & Pedersen 2014); benchmarked managers cannot exploit it without tracking error (Baker, Bradley & Wurgler 2011); lottery preferences (Bali, Cakici & Whitelaw 2011). |
| Publication | Haugen & Heins 1975; Ang et al. 2006; Blitz & van Vliet 2007; widely sold as min-vol ETFs since 2011 |
| Where it fits | In the **low risk** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **MAX**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Volatility (252 days) **(this strategy)** | low risk | +1.00 | +1.00 | +5.1% | -10.3% to -0.2% | 0 / 1 |
| Volatility | low risk | +0.85 | +0.91 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Beta | low risk | +0.66 | +0.85 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| Range (MAX−MIN) | low risk | +0.61 | +0.83 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| MIN5 | low risk | -0.58 | -0.81 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| MAX5 | low risk | +0.62 | +0.78 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| MAX (best day) (mirror) | low risk | +0.54 | +0.77 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| MIN (worst day) | low risk | -0.50 | -0.75 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| Idiosyncratic vol | low risk | +0.60 | +0.75 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| Near 52-week high | momentum | -0.43 | -0.70 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| 55-day breakout | momentum | -0.31 | -0.61 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Momentum 12-1 | momentum | -0.12 | -0.41 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Size | size | -0.05 | -0.24 | -1.5% | -3.8% to +4.6% | 0 / 0 |
| Last month return | short-term reversal | +0.00 | -0.24 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Residual momentum | momentum | -0.05 | -0.23 | +6.1% | +7.3% to +13.0% | 5 / 0 |
| Skewness | tail direction | +0.05 | +0.10 | -0.2% | -5.4% to +4.5% | 0 / 1 |
| Above 52-week low | momentum | +0.24 | +0.08 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Same-month seasonality | seasonality | +0.09 | -0.03 | -1.8% | -8.5% to +7.2% | 0 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.05 | +0.03 | -1.0% | -5.3% to +4.2% | 0 / 0 |

![360 map](../figures/xs_FS04_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with |t| ≥ 2 |
|---|---|---|---|---|
| US | +3.1% | 1.64 | 0.95 | Volatility +0.65 (+6.4), Beta +0.30 (+6.3) |
| EU | -0.4% | -0.21 | 0.88 | Volatility +0.77 (+9.0) |
| UK | +6.6% | 3.00 | 0.89 | Volatility +0.55 (+5.6), Beta +0.25 (+5.3) |
| DK | -2.1% | -0.85 | 0.81 | Beta +0.49 (+10.3), Volatility +0.31 (+4.0) |
| SCANDI | -0.1% | -0.08 | 0.79 | Volatility +0.64 (+7.4), MIN5 -0.20 (-3.3) |
| World | +3.7% | 2.52 | 0.94 | Volatility +0.58 (+7.5), Beta +0.35 (+7.7), Range -0.35 (-3.2), Idiosyncratic vol +0.43 (+5.1) |

![Double sort](../figures/xs_FS04_dsort.png)

Holding MAX fixed (down a column), moving from low to high Volatility changes the return by +4.4, +3.8 and +5.1 points a year; holding Volatility fixed (along a row), moving from low to high MAX changes it by -2.4, +0.6 and -1.7.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): +26% vs -33% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +5.1%, +5.0%, +6.5%, +6.2% a year.

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
