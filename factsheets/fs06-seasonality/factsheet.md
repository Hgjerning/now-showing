# FACTSHEET FS06 · Same-month seasonality

### Do stocks repeat their best calendar month?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`. On the corrected universe the pooled holdout spread is more clearly negative (t −2.21): beyond 2, though not past this factsheet's 2.87 gate.

> **US, 1999–2012 (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time S&P
> 500 with delisted stocks, 1999–2012, a period this factsheet was not built on. L/S net: t +1.16 (2013–2026: -2.83),
> reversed. Long-only alpha vs the equal-weight universe: +2.2% a year, t +0.61 (2013–2026: -3.17), reversed. The
> 2013–2026 US loss did not repeat; it reads as specific to that period. Registered verdicts are unchanged.
> Pre-registration, method and every result: `PREREG_US_1999_2012.md`.

<div class="kf" markdown="0">
<div><b>Strategy</b>Return seasonality (cross-sectional)</div>
<div><b>Origin</b>Heston & Sadka (2008)</div>
<div><b>Family</b>Calendar & seasonality</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (stocks with the highest past returns in the coming calendar month)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Registered gate |t| &gt; 2.87 over 12 cells; every cell in the programme trial ledger</div>
</div>

> **The claim.** A stock that did well relative to others in, say, March tends to do well again in March in later years, at annual lags up to 20 years. Heston & Sadka (2008) found it in US stocks 1965–2002; Keloharju, Linnainmaa & Nyberg (2016) found the same across markets and asset classes. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -14.0% to +3.4% a year and was positive in 1 of the six; no universe passes the 2.87 gate (significantly negative in EU, DK). The long-only book (stocks with the highest past returns in the coming calendar month) had a higher Sharpe than the equal-weight universe in 1 of the six (UK), with alphas of -5.8% to +3.0%, none past the gate. **What goes wrong (§9):** the main drags are costs of about 3.9% a year, a weaker second half (2020–26). None of the pre-declared fixes passes the gate in both windows. **Classification (appendix C):** Calendar & seasonality; its returns sit closest to the momentum cluster of the signal library. **360° view (appendix D):** nearest neighbours Size, 55-day breakout; after its closest neighbours and the market it keeps an alpha of -8.2% to +3.0% (largest |t| 2.3), so it carries some information of its own.

*Layout revised 2 October 2026 (verdict and scorecard, Sharpe anatomy, fit with the other strategies; detail moved to the appendix). No number changed.*

## 1. Verdict and scorecard

> **Verdict.** Of the 12 registered cells (two books × six universes), **0 pass** the |t| > 2.87 gate and **4 are significantly negative** (L/S EU, L/S DK, long-only US, long-only EU). Programme-wide (772 trials, |t| > 3.99): nothing survives. US 1999–2012, a period the factsheet was not built on: L/S t +1.16, long-only alpha t +0.61.

| Universe | L/S t | L/S Sharpe | Long-only alpha t | Long-only Sharpe vs equal-weight | Long-only max DD |
|---|---|---|---|---|---|
| US | -2.83 | -0.70 | -3.17 ✖ (neg.) | 0.49 vs 0.85 | -38% |
| EU | -3.14 ✖ (neg.) | -0.76 | -2.92 ✖ (neg.) | 0.36 vs 0.75 | -34% |
| UK | +0.79 | 0.24 | +0.99 | 0.76 vs 0.68 | -37% |
| DK | -3.40 ✖ (neg.) | -0.94 | -2.30 | 0.38 vs 0.83 | -46% |
| SCANDI | -2.22 | -0.63 | -1.25 | 0.65 vs 0.89 | -38% |
| World | -1.07 | -0.27 | -1.04 | 0.58 vs 0.71 | -41% |
| US 1999–2012 | +1.16 | 0.29 | +0.61 | 0.52 vs 0.49 | – |
*✔ passes the 2.87 gate (Bonferroni over 12 cells); ✖ significantly negative. 2013–2026 unless stated.*

## 2. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 501 / 10 | -8.9% | -2.83 | -9.1% (-2.8) | 0.02 | +7.9% | 0.49 | -38% | +12.6% | 0.85 | +14.9% |
| EU | 264 / 10 | -9.6% | -3.14 | -8.1% (-2.6) | -0.14 | +4.8% | 0.36 | -34% | +10.2% | 0.75 | +10.2% |
| UK | 324 / 10 | +3.4% | 0.79 | +2.0% (0.5) | 0.14 | +13.3% | 0.76 | -37% | +9.0% | 0.68 | +7.8% |
| DK | 20 / 3 | -14.0% | -3.40 | -13.5% (-3.2) | -0.04 | +5.3% | 0.38 | -46% | +12.0% | 0.83 | +10.2% |
| SCANDI | 70 / 5 | -7.8% | -2.22 | -6.4% (-1.7) | -0.11 | +9.5% | 0.65 | -38% | +12.2% | 0.89 | +11.0% |
| World | 1087 / 10 | -2.6% | -1.07 | -2.1% (-0.8) | -0.05 | +9.6% | 0.58 | -41% | +10.5% | 0.71 | +10.3% |

*Monthly, local currency (World in USD). L/S = equal-weighted stocks with the highest past returns in the coming calendar month minus stocks with the lowest, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS06_growth.png)

**Read with care.** A long/short book with a negative beta shows a large CAPM alpha in a rising market. The factor-model alpha in section 7, after momentum, value and the other themes, is the better guide: here the L/S CAPM alpha ranges -13.5% to +2.0% and the factor alpha -9.5% to +1.1%.

## 3. Where the Sharpe comes from

Sharpe = annual return ÷ annual volatility. The return splits into the part the market explains (beta × market return) and the rest (alpha, net of costs); the volatility into the market's share and the strategy's own. The last column is the Sharpe the book would have with its market exposure hedged out (before hedging costs).

| Universe | Book | Return / yr | = market part | + alpha | Costs / yr (inside the return) | Volatility | of which market | Sharpe | Sharpe, market hedged |
|---|---|---|---|---|---|---|---|---|---|
| US | L/S | -8.9% | +0.2% | -9.1% | -5.0% | 12.6% | 0.2% | -0.70 | -0.72 |
| US | Long-only | +9.6% | +15.3% | -5.8% | – | 19.6% | 18.1% | 0.49 | -0.77 |
| EU | L/S | -9.6% | -1.5% | -8.1% | -4.9% | 12.7% | 2.0% | -0.76 | -0.65 |
| EU | Long-only | +6.1% | +11.5% | -5.4% | – | 16.9% | 15.4% | 0.36 | -0.76 |
| UK | L/S | +3.4% | +1.4% | +2.0% | -4.8% | 13.8% | 2.0% | 0.24 | 0.15 |
| UK | Long-only | +14.3% | +11.3% | +3.0% | – | 18.7% | 16.6% | 0.76 | 0.35 |
| DK | L/S | -14.0% | -0.5% | -13.5% | -4.0% | 14.9% | 0.6% | -0.94 | -0.91 |
| DK | Long-only | +6.7% | +12.5% | -5.8% | – | 17.5% | 15.1% | 0.38 | -0.66 |
| SCANDI | L/S | -7.8% | -1.4% | -6.4% | -4.6% | 12.4% | 1.6% | -0.63 | -0.52 |
| SCANDI | Long-only | +10.3% | +12.9% | -2.5% | – | 15.9% | 14.5% | 0.65 | -0.39 |
| World | L/S | -2.6% | -0.5% | -2.0% | -4.9% | 9.6% | 0.7% | -0.27 | -0.21 |
| World | Long-only | +10.9% | +12.6% | -1.7% | – | 18.8% | 17.9% | 0.58 | -0.29 |
*Monthly, 2013–2026, market = equal-weight universe. Interactive version: the Strategy Cockpit.*

![Growth, drawdown and rolling Sharpe](../figures/xs_FS06_panel.png)

## 4. How it fits next to the market and the other strategies

A long/short book improves a market portfolio when its own Sharpe beats the hurdle: its correlation with the market × the market's Sharpe. A negative correlation makes the hurdle negative, so even a book with a small positive Sharpe diversifies; the size of the gain still depends on that Sharpe.

| Universe | Corr. with market | Avg corr. with the other strategies | Most similar strategy | Market Sharpe | Hurdle Sharpe | This L/S Sharpe | Verdict | L/S in the worst 10% of market months | Market in those months |
|---|---|---|---|---|---|---|---|---|---|
| US | +0.02 | +0.02 | Size (-0.21) | 0.85 | +0.02 | -0.70 | dilutes | -2.0% | -7.3% |
| EU | -0.16 | +0.08 | Size (-0.29) | 0.75 | -0.12 | -0.76 | dilutes | +0.2% | -6.5% |
| UK | +0.15 | +0.04 | Size (+0.28) | 0.68 | +0.10 | 0.24 | adds | -0.7% | -6.6% |
| DK | -0.04 | -0.00 | Residual momentum (-0.13) | 0.83 | -0.03 | -0.94 | dilutes | -1.5% | -7.2% |
| SCANDI | -0.13 | +0.03 | Short-term reversal (-0.15) | 0.89 | -0.11 | -0.63 | dilutes | -0.0% | -6.9% |
| World | -0.08 | +0.04 | Size (-0.31) | 0.71 | -0.05 | -0.27 | dilutes | -0.6% | -7.5% |
*Long/short (net), monthly, 2013–2026; market = equal-weight universe; other strategies = the long/short books of FS01–FS12. The Strategy Cockpit lets you build books of several strategies.*

## 5. Strategy description

A stock that did well relative to others in, say, March tends to do well again in March in later years, at annual lags up to 20 years. Heston & Sadka (2008) found it in US stocks 1965–2002; Keloharju, Linnainmaa & Nyberg (2016) found the same across markets and asset classes.

**Why it might work.** Recurring demand and information flows tied to the calendar (earnings seasons, dividend timing, fund flows); Keloharju et al. (2016) argue it reflects seasonal variation in risk premia.

| Rule | Original (Heston & Sadka (2008)) | This factsheet |
|---|---|---|
| Signal | Average return in the same calendar month over the past 1–20 years | Average return in the coming calendar month over all prior years available (1 year in 2013, 13 by 2026) |
| Portfolio | Decile L/S, one month | Extreme quantile L/S, one month |
| Weighting | Equal weighted | Equal weighted |

## 6. Method: data, signal and portfolio

### Data load

| Universe | Prices | Membership | Names eligible (median) | Currency |
|---|---|---|---|---|
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: the S&P 500 members at each month-end (Sharadar add/remove history; corrected 2 Oct 2026) | ~503 | USD |
| EU | Project1 yfinance cache, Adj Close (TR) | **Point-in-time**: union of 11 national blue-chip indices (CAC 40, DAX, AEX, IBEX 35, FTSE MIB, OMXS30, OMXC25, OMXH25, BEL 20, PSI-20, WIG20), quarterly Wikipedia snapshots 2012–2026; 83% of member-quarters priced | ~238 | local (EUR, SEK, DKK, PLN) |
| UK | Project1 cache, Close + pence dividends (Yahoo under-adjusts LSE ~100×) | **Point-in-time**: FTSE 100 + FTSE 250, quarterly snapshots; 75% priced | ~242 | GBP |
| DK | Project1 cache, Adj Close | **Point-in-time**: OMX Copenhagen 25, quarterly snapshots; 91% priced | ~19 | DKK |
| SCANDI | Project1 cache, Adj Close | **Point-in-time**: OMXC25 + OMXS30 + OMXH25 (Oslo has no snapshot history); 88% priced | ~62 | local (DKK, SEK, EUR) |
| World | US Sharadar + UK + EU above | **Point-in-time** union of the three; local-currency returns summed, not converted | ~963 | mixed |

*Membership comes from Project2's cache of dated Wikipedia index pages (the same parsing as `run_wiki_pit.py` / `run_eu_pit.py`), with a short list of verified ticker renames (e.g. NZYM-B → NSIS-B, WDH → DEMANT, DAI → MBG). A name is eligible from the day after the snapshot that lists it, once it has 60 days of prices. Member-quarters without a price are mostly delisted names that Yahoo no longer serves, so some survivorship remains; see §13.*

- **Data gap:** Price history starts in 2011–2012, so the signal averages 1 prior year in 2013 and at most 13 by 2026; Heston & Sadka use up to 20. The early years test a much noisier signal than the paper's.

### Signal creation

SEAS<sub>i,t</sub> = mean of r<sub>i,m</sub> over the months m with the same calendar month as t+1 in earlier years. Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

### Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = stocks with the highest past returns in the coming calendar month minus stocks with the lowest; **long-only** = stocks with the highest past returns in the coming calendar month; benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 7. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -8.3% | -2.84 | 0.29 | mkt +0.18 (+2.7), value -0.78 (-5.1), momentum -0.34 (-2.6), low_risk +0.37 (+2.2) |
| EU | French Europe 5F + WML | -7.9% | -2.40 | 0.15 | HML -0.31 (-2.1) |
| UK | JKP GBR 7 themes | +0.7% | 0.20 | 0.22 | mkt +0.19 (+2.9), quality +0.80 (+2.8), short_term_reversal -0.53 (-3.0) |
| DK | JKP DNK 7 themes | -9.5% | -2.60 | 0.06 | none &#124;t&#124; ≥ 2 |
| SCANDI | French Europe 5F + WML | -4.9% | -1.45 | 0.09 | HML -0.34 (-2.2) |
| World | JKP World 7 themes | +1.1% | 0.47 | 0.30 | mkt +0.12 (+2.6), value -0.76 (-5.4), momentum -0.33 (-3.2), low_risk +0.38 (+2.9) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -2.3% | -1.31 | 0.90 | mkt +1.10 (+24.2), size -0.31 (-2.7), momentum -0.18 (-2.2) |
| EU | French Europe 5F + WML | +1.5% | 0.49 | 0.68 | Mkt-RF +0.80 (+12.3), CMA -0.47 (-2.5) |
| UK | JKP GBR 7 themes | +7.4% | 2.61 | 0.74 | mkt +0.70 (+13.3), low_risk -0.82 (-3.9), quality +0.86 (+3.5) |
| DK | JKP DNK 7 themes | +1.8% | 0.62 | 0.60 | mkt +0.61 (+8.0), low_risk -0.57 (-3.9), quality +0.23 (+2.2) |
| SCANDI | French Europe 5F + WML | +6.8% | 2.25 | 0.58 | Mkt-RF +0.69 (+10.8), WML -0.19 (-2.7) |
| World | JKP World 7 themes | +4.8% | 1.97 | 0.82 | mkt +0.89 (+13.9), momentum -0.22 (-2.4) |

## 8. Statistical detail

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 1 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -13.5% to +2.0%, |t| past the gate in 1 of 6.
- **Long-only:** Sharpe above the equal-weight universe in 1 of the six; alpha -5.8% to +3.0%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.01, EU 0.00, UK 0.82, DK 0.00, SCANDI 0.01, World 0.16.
- **Publication decay:** gross L/S -10.8% to +15.0% a year in 2013–19 against -9.2% to +2.8% in 2020–26.

## 9. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 9.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | -4.0% | -0.13 | -1.7% | -2.3% | -4.1% | -3.2% | -0.8% | 172% | 2013-05 -9%, 2019-06 -7%, 2016-11 -7% |
| EU | -2.2% | -0.11 | -1.2% | -1.1% | -4.0% | -2.4% | +0.1% | 167% | 2013-04 -9%, 2016-03 -8%, 2016-01 -8% |
| UK | +15.0% | 0.19 | +2.3% | +12.7% | -4.0% | +10.5% | +4.5% | 166% | 2016-06 -14%, 2016-09 -7%, 2016-08 -6% |
| DK | -10.8% | -0.17 | -2.6% | -8.2% | -3.2% | -4.0% | -6.8% | 135% | 2016-12 -11%, 2013-07 -8%, 2013-09 -7% |
| SCANDI | -1.6% | -0.30 | -4.6% | +3.0% | -3.8% | +0.4% | -2.0% | 158% | 2013-09 -8%, 2017-08 -7%, 2018-02 -6% |
| World | +1.9% | 0.00 | +0.0% | +1.8% | -4.1% | +1.0% | +0.9% | 169% | 2013-04 -6%, 2016-06 -6%, 2013-05 -5% |

On average across the six universes the gross spread was -0.3% a year, of which the market exposure (beta -0.09) contributed -1.3%; the beta-adjusted spread (CAPM alpha) was +1.0%. Costs took 3.9% a year at 161% monthly turnover across both legs. The long leg beat the universe by +0.4% and the short leg lagged it by -0.7% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages -1.7%, +0.9%, -0.6% a year.

### 9.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.47 | – | -0.89 | – | – | -8.2% | -50% | -8.3% (-2.1) | 3.9% |
| X1 beta-neutral legs | -0.46 | -0.05 (p 0.705) | -1.07 | -0.18 (p 0.840) | 0 of 6 | -9.2% | -53% | -9.2% (-2.6) | 3.7% |
| X2 + turnover buffer | -0.46 | +0.02 (p 0.406) | -0.82 | +0.25 (p 0.007) | 6 of 6 | -6.6% | -45% | -6.3% (-1.7) | 2.9% |
| X3 + volatility targeting | -0.32 | +0.18 (p 0.323) | -0.68 | +0.13 (p 0.110) | 5 of 6 | -6.3% | -48% | -5.9% (-1.3) | 2.9% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS06_ladder.png)

- **X1 beta-neutral legs:** -0.05 design, -0.18 holdout; hurts in both windows.
- **X2 + turnover buffer:** +0.02 design, +0.25 holdout; helps in both windows but does not pass the gate.
- **X3 + volatility targeting:** +0.18 design, +0.13 holdout; helps in both windows but does not pass the gate.

**Where it ends:** holdout Sharpe -0.89 → -0.68, return -8.2% → -6.3% a year (six-universe book).

## 10. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Data gap.** Price history starts in 2011–2012, so the signal averages 1 prior year in 2013 and at most 13 by 2026; Heston & Sadka use up to 20. The early years test a much noisier signal than the paper's.
5. **Trials.** Every gated cell is in the factsheet trial ledger; the fix ladder is counted inside FS03–FS12 (25 trials).

## 11. Academic references

- Heston, S. & Sadka, R. (2008). Seasonality in the cross-section of stock returns. *Journal of Financial Economics*, 87(2), 418–445.
- Keloharju, M., Linnainmaa, J. & Nyberg, P. (2016). Return seasonalities. *Journal of Finance*, 71(4), 1557–1590.
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

## 12. Reproduce

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS06` → `build_xs.py FS06`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.

## Appendix

### A. Performance in detail

**US (S&P 500 members, point-in-time)**, median 501 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -8.9% | -9.2% | 12.6% | -0.70 [-1.18, -0.22] | -0.91 | -74% | 37% | -2.83 | 0.02 | -9.1% (-2.8) | 8.8% |
| Long-only (net) | +9.6% | +7.9% | 19.6% | 0.49 [0.09, 0.98] | 0.61 | -38% | 60% | 2.43 | 1.17 | -5.8% (-3.2) | 12.5% |
| Stocks with the highest past returns in the coming calendar month (gross) | +11.6% | +10.1% | 19.6% | 0.59 [0.19, 1.11] | 0.79 | -36% | 61% | 2.95 | 1.17 | -3.7% (-2.0) | 12.3% |
| Stocks with the lowest (gross) | +15.4% | +14.4% | 19.5% | 0.79 [0.34, 1.36] | 1.20 | -33% | 62% | 3.84 | 1.15 | +0.3% (0.1) | 11.4% |
| EW universe | +13.1% | +12.6% | 15.5% | 0.85 [0.41, 1.42] | 1.29 | -28% | 67% | 4.20 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.9% | +14.9% | 14.2% | 1.05 [0.60, 1.61] | 1.73 | -24% | 69% | 5.29 | 0.86 | +3.7% (2.4) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 264 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -9.6% | -9.9% | 12.7% | -0.76 [-1.22, -0.31] | -0.93 | -79% | 40% | -3.14 | -0.14 | -8.1% (-2.6) | 9.0% |
| Long-only (net) | +6.1% | +4.8% | 16.9% | 0.36 [-0.12, 0.89] | 0.43 | -34% | 55% | 1.42 | 1.07 | -5.4% (-2.9) | 10.2% |
| Stocks with the highest past returns in the coming calendar month (gross) | +8.2% | +7.0% | 16.9% | 0.48 [-0.00, 1.02] | 0.64 | -32% | 56% | 1.90 | 1.07 | -3.3% (-1.8) | 10.0% |
| Stocks with the lowest (gross) | +12.8% | +11.6% | 19.5% | 0.66 [0.19, 1.19] | 0.96 | -30% | 61% | 2.72 | 1.21 | -0.2% (-0.1) | 10.8% |
| EW universe | +10.7% | +10.2% | 14.3% | 0.75 [0.29, 1.30] | 1.14 | -26% | 61% | 3.19 | 1.00 | – | 8.4% |
| Size-weighted universe | +10.6% | +10.2% | 13.7% | 0.77 [0.32, 1.29] | 1.21 | -25% | 58% | 3.37 | 0.92 | +0.8% (0.6) | 7.9% |

**UK (FTSE 350, point-in-time)**, median 324 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +3.4% | +2.4% | 13.8% | 0.24 [-0.34, 0.86] | 0.28 | -46% | 50% | 0.79 | 0.14 | +2.0% (0.5) | 7.5% |
| Long-only (net) | +14.3% | +13.3% | 18.7% | 0.76 [0.25, 1.34] | 1.22 | -37% | 60% | 3.16 | 1.17 | +3.0% (1.0) | 10.3% |
| Stocks with the highest past returns in the coming calendar month (gross) | +16.3% | +15.6% | 18.7% | 0.87 [0.35, 1.46] | 1.47 | -36% | 61% | 3.60 | 1.17 | +5.0% (1.7) | 10.2% |
| Stocks with the lowest (gross) | +8.2% | +7.0% | 16.6% | 0.49 [0.02, 1.02] | 0.64 | -34% | 59% | 1.93 | 1.03 | -1.7% (-0.7) | 10.3% |
| EW universe | +9.6% | +9.0% | 14.2% | 0.68 [0.20, 1.28] | 0.96 | -30% | 58% | 2.88 | 1.00 | – | 8.8% |
| Size-weighted universe | +8.4% | +7.8% | 12.9% | 0.65 [0.16, 1.25] | 0.90 | -28% | 62% | 2.68 | 0.84 | +0.3% (0.2) | 7.8% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -14.0% | -14.1% | 14.9% | -0.94 [-1.52, -0.41] | -1.12 | -88% | 37% | -3.40 | -0.04 | -13.5% (-3.2) | 9.0% |
| Long-only (net) | +6.7% | +5.3% | 17.5% | 0.38 [-0.13, 0.96] | 0.45 | -46% | 55% | 1.40 | 0.99 | -5.8% (-2.3) | 10.6% |
| Stocks with the highest past returns in the coming calendar month (gross) | +8.2% | +6.9% | 17.5% | 0.47 [-0.04, 1.06] | 0.60 | -45% | 56% | 1.73 | 1.00 | -4.3% (-1.7) | 10.4% |
| Stocks with the lowest (gross) | +18.2% | +18.0% | 17.7% | 1.03 [0.51, 1.66] | 1.76 | -25% | 62% | 4.17 | 1.04 | +5.2% (2.1) | 9.4% |
| EW universe | +12.6% | +12.0% | 15.2% | 0.83 [0.31, 1.44] | 1.27 | -33% | 66% | 3.31 | 1.00 | – | 8.8% |
| Size-weighted universe | +11.1% | +10.2% | 16.4% | 0.68 [0.11, 1.33] | 0.94 | -40% | 62% | 2.55 | 0.93 | -0.6% (-0.2) | 10.7% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -7.8% | -8.3% | 12.4% | -0.63 [-1.20, -0.06] | -0.83 | -72% | 40% | -2.22 | -0.11 | -6.4% (-1.7) | 7.5% |
| Long-only (net) | +10.3% | +9.5% | 15.9% | 0.65 [0.12, 1.26] | 0.96 | -38% | 56% | 2.36 | 1.02 | -2.6% (-1.2) | 9.0% |
| Stocks with the highest past returns in the coming calendar month (gross) | +12.3% | +11.6% | 15.9% | 0.77 [0.23, 1.39] | 1.20 | -37% | 61% | 2.80 | 1.02 | -0.6% (-0.3) | 8.9% |
| Stocks with the lowest (gross) | +15.4% | +14.7% | 17.9% | 0.86 [0.34, 1.49] | 1.29 | -30% | 64% | 3.55 | 1.14 | +1.1% (0.5) | 11.4% |
| EW universe | +12.6% | +12.2% | 14.2% | 0.89 [0.37, 1.51] | 1.38 | -29% | 66% | 3.63 | 1.00 | – | 8.4% |
| Size-weighted universe | +11.4% | +11.0% | 13.5% | 0.84 [0.37, 1.41] | 1.32 | -26% | 63% | 3.59 | 0.90 | +0.0% (0.0) | 8.1% |

**World (US + UK + EU, point-in-time)**, median 1087 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -2.6% | -3.0% | 9.6% | -0.27 [-0.71, 0.21] | -0.41 | -43% | 47% | -1.07 | -0.05 | -2.1% (-0.8) | 6.2% |
| Long-only (net) | +10.9% | +9.6% | 18.8% | 0.58 [0.10, 1.14] | 0.78 | -41% | 60% | 2.44 | 1.12 | -1.7% (-1.0) | 11.8% |
| Stocks with the highest past returns in the coming calendar month (gross) | +13.0% | +11.8% | 18.8% | 0.69 [0.21, 1.27] | 0.98 | -40% | 61% | 2.90 | 1.12 | +0.4% (0.2) | 11.6% |
| Stocks with the lowest (gross) | +10.6% | +9.1% | 19.5% | 0.55 [0.08, 1.10] | 0.72 | -37% | 59% | 2.26 | 1.16 | -2.5% (-1.9) | 11.7% |
| EW universe | +11.3% | +10.5% | 16.0% | 0.71 [0.25, 1.28] | 1.02 | -30% | 63% | 3.07 | 1.00 | – | 9.7% |
| Size-weighted universe | +11.0% | +10.3% | 14.8% | 0.74 [0.28, 1.31] | 1.10 | -28% | 61% | 3.19 | 0.91 | +0.7% (0.8) | 8.9% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -15.9% | -15.9% | +28.7% | -27.1% | -22.7% | -8.1% |
| 2014 | -11.2% | -2.4% | +11.0% | +7.7% | -2.7% | -6.0% |
| 2015 | +3.9% | +4.5% | +45.0% | -20.5% | -0.4% | +8.7% |
| 2016 | -7.4% | -10.7% | -21.0% | -18.7% | +1.1% | -9.4% |
| 2017 | -16.5% | -7.8% | +9.7% | -19.6% | -9.0% | -7.5% |
| 2018 | -2.9% | -17.5% | -6.2% | -8.1% | -15.3% | -0.0% |
| 2019 | -11.9% | -0.6% | +12.4% | -9.9% | +5.9% | +0.2% |
| 2020 | +1.7% | -11.7% | +17.9% | +12.2% | -1.5% | +2.1% |
| 2021 | -11.0% | -16.9% | -8.4% | -24.1% | -19.7% | -5.8% |
| 2022 | -28.5% | -5.0% | -17.1% | -21.9% | -5.9% | -16.1% |
| 2023 | +16.1% | -2.9% | -7.0% | -18.3% | +4.0% | +12.9% |
| 2024 | +9.9% | -23.9% | -16.1% | -12.3% | -2.1% | +5.9% |
| 2025 | -21.0% | -12.0% | +0.2% | +6.4% | -19.7% | -8.3% |
| 2026 | -19.8% | -7.6% | +4.8% | -26.4% | -17.5% | -5.0% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +17.6% | +16.0% | +39.2% | +21.8% | +10.8% | +22.4% |
| 2014 | +8.9% | +1.3% | +13.7% | +17.4% | +12.2% | +0.1% |
| 2015 | +0.2% | +2.5% | +35.0% | +11.4% | +13.3% | +4.1% |
| 2016 | +9.9% | +7.0% | +14.1% | +6.4% | +31.3% | +3.6% |
| 2017 | +5.5% | +14.6% | +37.1% | +10.5% | +12.0% | +25.4% |
| 2018 | -11.5% | -24.4% | -14.3% | -12.2% | -14.7% | -13.2% |
| 2019 | +21.3% | +27.1% | +30.1% | +12.7% | +38.3% | +27.8% |
| 2020 | +11.1% | +1.6% | +23.0% | +48.1% | +27.8% | +13.4% |
| 2021 | +20.8% | +0.3% | +6.6% | +4.0% | +7.5% | +11.1% |
| 2022 | -27.8% | -17.2% | -25.6% | -30.5% | -20.7% | -28.1% |
| 2023 | +26.6% | +15.5% | +10.7% | -1.4% | +8.9% | +27.4% |
| 2024 | +19.0% | +1.1% | -5.1% | -5.0% | +3.1% | +14.7% |
| 2025 | +4.0% | +19.5% | +12.5% | +17.9% | +9.1% | +17.8% |
| 2026 | +15.7% | +13.3% | +27.3% | -8.4% | +4.9% | +20.7% |

### B. Trading record and current book

The rebalance log per universe is in `results/xs_FS06_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 85% | 87% | 37% | -11.9% | 2026-04 |
| EU | 163 | 27 / 26 | 86% | 82% | 40% | -12.9% | 2024-10 |
| UK | 163 | 33 / 32 | 85% | 82% | 50% | -14.2% | 2016-06 |
| DK | 163 | 7 / 6 | 64% | 72% | 37% | -11.1% | 2016-12 |
| SCANDI | 163 | 14 / 14 | 79% | 80% | 40% | -11.6% | 2025-04 |
| World | 163 | 109 / 108 | 85% | 84% | 47% | -9.1% | 2022-01 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks with the highest past returns in the coming calendar month | Short: stocks with the lowest |
|---|---|---|
| US | SNDK, GEV, APP, CEG, HOOD, PLTR, TKO, MU | CVNA, KVUE, DXCM, VTRS, EFX, SWKS, XYZ, INCY |
| EU | ZEAL.CO, JSW.WA, HM-B.ST, NKT.CO, BOL.ST, FORTUM.HE, BKT.MC, ITX.MC | PUIG.MC, DSFIR.AS, DTG.DE, BMPS.MI, BAVA.CO, ANE.MC, ORSTED.CO, EDEN.PA |
| UK | CWR.L, ALFA.L, GDWN.L, TRST.L, HWG.L, JD.L, AVON.L, EWG.L | MTLN.L, THG.L, OCDO.L, AML.L, MTRO.L, OXIG.L, DOCS.L, BCG.L |
| DK | ZEAL.CO, NKT.CO, NDA-DK.CO, JYSK.CO, GMAB.CO, TRYG.CO, VWS.CO, DSV.CO | BAVA.CO, ORSTED.CO, GN.CO, DEMANT.CO, AMBU-B.CO, ISS.CO, COLO-B.CO, NOVO-B.CO |
| SCANDI | ZEAL.CO, HM-B.ST, NKT.CO, BOL.ST, FORTUM.HE, SWED-A.ST, NOKIA.HE, SKA-B.ST | BAVA.CO, ORSTED.CO, METSO.HE, QTCOM.HE, EQT.ST, WRT1V.HE, GN.CO, DEMANT.CO |

### C. Classification: where does it fit?

| Dimension | Same-month seasonality |
|---|---|
| Series family | **Calendar & seasonality** |
| Academic style | Return seasonality (cross-sectional) |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 161% of the two legs replaced monthly |
| Market exposure | L/S beta -0.14 to 0.14 |
| Payoff shape | Treynor–Mazuy γ -0.31 to 1.74 (t -0.5 to 1.7); worst 10% of market months -2.0% to +0.2% a month, best 10% -1.9% to +2.0% |
| Nearest factor theme | investment (4 of 6 universes), HML (2 of 6 universes) |
| Nearest library signals (returns) | Size (4 universes), 55-day breakout (3 universes), MIN5 (2 universes) |
| Economic rationale | Recurring demand and information flows tied to the calendar (earnings seasons, dividend timing, fund flows); Keloharju et al. (2016) argue it reflects seasonal variation in risk premia. |
| Publication | Heston & Sadka 2008; Keloharju, Linnainmaa & Nyberg 2016 |
| Where it fits | In the **momentum** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

### D. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Momentum 12-1**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Same-month seasonality **(this strategy)** | seasonality | +1.00 | +1.00 | -1.9% | -9.4% to +6.6% | 0 / 1 |
| Last month return | short-term reversal | +0.01 | +0.15 | +1.8% | -3.2% to +11.0% | 2 / 0 |
| 55-day breakout | momentum | +0.01 | +0.14 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| Momentum 12-1 (mirror) | momentum | +0.12 | +0.14 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.00 | +0.12 | -0.9% | -5.2% to +5.2% | 0 / 0 |
| MIN5 | low risk | -0.04 | +0.12 | -0.9% | +2.3% to +13.7% | 4 / 0 |
| Near 52-week high | momentum | +0.01 | +0.11 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| Volatility (252 days) | low risk | +0.08 | -0.10 | +2.4% | -12.9% to -4.8% | 0 / 3 |
| Idiosyncratic vol | low risk | +0.03 | -0.10 | -3.6% | -15.5% to -4.8% | 0 / 4 |
| MIN (worst day) | low risk | -0.03 | +0.10 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| Beta | low risk | +0.10 | -0.09 | +4.4% | -12.6% to -4.2% | 0 / 4 |
| Volatility | low risk | +0.05 | -0.09 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| Range (MAX−MIN) | low risk | +0.04 | -0.08 | -0.7% | -15.4% to -4.8% | 0 / 4 |
| Size | size | +0.08 | +0.08 | +0.1% | -3.8% to +9.9% | 1 / 0 |
| MAX5 | low risk | +0.05 | -0.07 | +0.6% | -11.3% to -3.5% | 0 / 2 |
| Skewness | tail direction | +0.00 | +0.04 | -0.4% | -6.7% to +3.9% | 0 / 2 |
| Residual momentum | momentum | +0.01 | -0.03 | +6.4% | +8.0% to +12.2% | 6 / 0 |
| MAX (best day) | low risk | +0.04 | -0.02 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| Above 52-week low | momentum | +0.06 | +0.01 | +7.5% | +5.2% to +13.6% | 4 / 0 |

![360 map](../figures/xs_FS06_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | -7.0% | -2.28 | 0.09 |  |
| EU | -7.8% | -2.10 | 0.12 | Size +0.23 (+2.8) |
| UK | +3.0% | 0.74 | 0.14 | Size -0.25 (-2.7), Momentum 12-1 +0.18 (+2.5) |
| DK | -8.2% | -2.05 | 0.03 |  |
| SCANDI | -2.0% | -0.48 | 0.05 |  |
| World | +0.6% | 0.25 | 0.12 | Size +0.32 (+2.7) |

![Double sort](../figures/xs_FS06_dsort.png)

Holding Momentum 12-1 fixed (down a column), moving from low to high Same-month seasonality changes the return by -0.0, -1.4 and -0.3 points a year; holding Same-month seasonality fixed (along a row), moving from low to high Momentum 12-1 changes it by +4.2, +3.4 and +3.9.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -1% vs -2% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages -1.9%, -1.7%, +0.9%, -0.6% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

