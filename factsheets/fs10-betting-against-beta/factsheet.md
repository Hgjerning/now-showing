# FACTSHEET FS10 · Betting against beta

### Lever up the low-beta stocks, short the high-beta ones

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

> **US, 1999–2012 (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time S&P
> 500 with delisted stocks, 1999–2012, a period this factsheet was not built on. L/S net: t +0.39 (2013–2026: +1.17),
> same sign, weaker. Long-only alpha vs the equal-weight universe: +2.4% a year, t +1.41 (2013–2026: +1.93), same sign,
> weaker. Registered verdicts are unchanged. Pre-registration, method and every result: `PREREG_US_1999_2012.md`.

<div class="kf" markdown="0">
<div><b>Strategy</b>Defensive / betting against beta</div>
<div><b>Origin</b>Frazzini & Pedersen (2014)</div>
<div><b>Family</b>Low risk</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (low-beta stocks)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Registered gate |t| &gt; 2.87 over 12 cells; every cell in the programme trial ledger</div>
</div>

> **The claim.** Low-beta stocks have higher risk-adjusted returns than high-beta stocks. A portfolio that is long leveraged low-beta stocks and short de-leveraged high-beta stocks, beta-neutral, earned a large positive return in the US 1926–2012 and in 19 other markets (Frazzini & Pedersen 2014). **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned +1.7% to +9.1% a year and was positive in all six; no universe passes the 2.87 gate. The long-only book (low-beta stocks) had a higher Sharpe than the equal-weight universe in all six, with alphas of +2.4% to +3.7%, passing the gate in UK. **What goes wrong (§9):** the main drags are a weaker second half (2020–26). None of the pre-declared fixes passes the gate in both windows. **Classification (appendix C):** Low risk; its returns sit closest to the low risk cluster of the signal library. **360° view (appendix D):** nearest neighbours Volatility (252 days), Volatility; after its closest neighbours and the market it keeps an alpha of -5.9% to +4.3% (largest |t| 2.2), so it carries some information of its own.

*Layout revised 2 October 2026 (verdict and scorecard, Sharpe anatomy, fit with the other strategies; detail moved to the appendix). No number changed.*

## 1. Verdict and scorecard

> **Verdict.** Of the 12 registered cells (two books × six universes), **1 pass** the |t| > 2.87 gate (long-only UK). Programme-wide (772 trials, |t| > 3.99): nothing survives. US 1999–2012, a period the factsheet was not built on: L/S t +0.39, long-only alpha t +1.41.

| Universe | L/S t | L/S Sharpe | Long-only alpha t | Long-only Sharpe vs equal-weight | Long-only max DD |
|---|---|---|---|---|---|
| US | +1.17 | 0.25 | +1.93 | 0.94 vs 0.85 | -20% |
| EU | +1.59 | 0.36 | +2.28 | 0.91 vs 0.75 | -18% |
| UK | +2.80 | 0.78 | +3.79 ✔ | 1.01 vs 0.68 | -19% |
| DK | +0.39 | 0.10 | +1.23 | 0.87 vs 0.83 | -19% |
| SCANDI | +1.23 | 0.31 | +2.44 | 1.05 vs 0.89 | -18% |
| World | +2.12 | 0.44 | +2.36 | 0.85 vs 0.71 | -21% |
| US 1999–2012 | +0.39 | 0.11 | +1.41 | 0.62 vs 0.49 | – |
*✔ passes the 2.87 gate (Bonferroni over 12 cells); ✖ significantly negative. 2013–2026 unless stated.*

## 2. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 502 / 10 | +4.3% | 1.17 | +2.4% (0.6) | 0.14 | +10.9% | 0.94 | -20% | +12.6% | 0.85 | +14.9% |
| EU | 264 / 10 | +4.6% | 1.59 | +3.6% (1.2) | 0.09 | +9.1% | 0.91 | -18% | +10.2% | 0.75 | +10.2% |
| UK | 326 / 10 | +9.1% | 2.80 | +7.7% (2.5) | 0.14 | +9.6% | 1.01 | -19% | +8.9% | 0.68 | +7.8% |
| DK | 20 / 3 | +1.7% | 0.39 | +1.1% (0.3) | 0.04 | +10.4% | 0.87 | -19% | +12.0% | 0.83 | +10.2% |
| SCANDI | 70 / 5 | +3.8% | 1.23 | +3.3% (1.1) | 0.04 | +11.2% | 1.05 | -18% | +12.3% | 0.89 | +11.0% |
| World | 1088 / 10 | +5.9% | 2.12 | +3.2% (1.1) | 0.24 | +9.6% | 0.85 | -21% | +10.5% | 0.71 | +10.3% |

*Monthly, local currency (World in USD). L/S = equal-weighted low-beta stocks minus high-beta stocks (rank-weighted, each leg scaled to beta 1), net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS10_growth.png)

**Read with care.** A long/short book with a negative beta shows a large CAPM alpha in a rising market. The factor-model alpha in section 7, after momentum, value and the other themes, is the better guide: here the L/S CAPM alpha ranges +1.1% to +7.7% and the factor alpha -4.2% to +3.7%.

## 3. Where the Sharpe comes from

Sharpe = annual return ÷ annual volatility. The return splits into the part the market explains (beta × market return) and the rest (alpha, net of costs); the volatility into the market's share and the strategy's own. The last column is the Sharpe the book would have with its market exposure hedged out (before hedging costs).

| Universe | Book | Return / yr | = market part | + alpha | Costs / yr (inside the return) | Volatility | of which market | Sharpe | Sharpe, market hedged |
|---|---|---|---|---|---|---|---|---|---|
| US | L/S | +4.3% | +1.9% | +2.4% | -3.5% | 16.8% | 2.2% | 0.25 | 0.14 |
| US | Long-only | +11.1% | +8.4% | +2.6% | – | 11.8% | 10.0% | 0.94 | 0.42 |
| EU | L/S | +4.6% | +1.0% | +3.6% | -3.4% | 12.8% | 1.3% | 0.36 | 0.28 |
| EU | Long-only | +9.3% | +6.7% | +2.6% | – | 10.2% | 8.9% | 0.91 | 0.54 |
| UK | L/S | +9.1% | +1.4% | +7.7% | -3.4% | 11.7% | 2.0% | 0.78 | 0.67 |
| UK | Long-only | +9.6% | +5.9% | +3.7% | – | 9.6% | 8.7% | 1.01 | 0.94 |
| DK | L/S | +1.7% | +0.5% | +1.1% | -3.2% | 16.5% | 0.6% | 0.10 | 0.07 |
| DK | Long-only | +10.7% | +8.3% | +2.4% | – | 12.4% | 10.0% | 0.87 | 0.33 |
| SCANDI | L/S | +3.8% | +0.5% | +3.3% | -3.4% | 12.5% | 0.6% | 0.31 | 0.27 |
| SCANDI | Long-only | +11.2% | +8.2% | +3.0% | – | 10.6% | 9.2% | 1.05 | 0.57 |
| World | L/S | +5.9% | +2.7% | +3.2% | -3.5% | 13.3% | 3.8% | 0.44 | 0.25 |
| World | Long-only | +9.9% | +7.5% | +2.4% | – | 11.6% | 10.6% | 0.85 | 0.51 |
*Monthly, 2013–2026, market = equal-weight universe. Interactive version: the Strategy Cockpit.*

![Growth, drawdown and rolling Sharpe](../figures/xs_FS10_panel.png)

## 4. How it fits next to the market and the other strategies

A long/short book improves a market portfolio when its own Sharpe beats the hurdle: its correlation with the market × the market's Sharpe. A negative correlation makes the hurdle negative, so even a book with a small positive Sharpe diversifies; the size of the gain still depends on that Sharpe.

| Universe | Corr. with market | Avg corr. with the other strategies | Most similar strategy | Market Sharpe | Hurdle Sharpe | This L/S Sharpe | Verdict | L/S in the worst 10% of market months | Market in those months |
|---|---|---|---|---|---|---|---|---|---|
| US | +0.13 | +0.19 | Low volatility (+0.60) | 0.85 | +0.11 | 0.25 | adds | -2.9% | -7.3% |
| EU | +0.10 | +0.15 | Low volatility (+0.45) | 0.75 | +0.08 | 0.36 | adds | -1.7% | -6.5% |
| UK | +0.17 | +0.19 | Momentum (+0.41) | 0.68 | +0.12 | 0.78 | adds | -2.5% | -6.6% |
| DK | +0.04 | +0.20 | Low volatility (+0.66) | 0.83 | +0.03 | 0.10 | adds | -0.1% | -7.2% |
| SCANDI | +0.05 | +0.13 | Low volatility (+0.46) | 0.89 | +0.04 | 0.31 | adds | -0.5% | -6.9% |
| World | +0.29 | +0.14 | Low volatility (+0.38) | 0.71 | +0.20 | 0.44 | adds | -3.4% | -7.5% |
*Long/short (net), monthly, 2013–2026; market = equal-weight universe; other strategies = the long/short books of FS01–FS12. The Strategy Cockpit lets you build books of several strategies.*

## 5. Strategy description

Low-beta stocks have higher risk-adjusted returns than high-beta stocks. A portfolio that is long leveraged low-beta stocks and short de-leveraged high-beta stocks, beta-neutral, earned a large positive return in the US 1926–2012 and in 19 other markets (Frazzini & Pedersen 2014).

**Why it might work.** Leverage-constrained investors buy high-beta stocks instead of levering the market, bidding them up (Black 1972; Frazzini & Pedersen 2014); lottery demand (Bali, Brown, Murray & Tang 2017).

| Rule | Original (Frazzini & Pedersen (2014)) | This factsheet |
|---|---|---|
| Signal | Shrunk beta from 1-year volatility and 5-year correlation | 252-day beta vs the equal-weight universe (no shrinkage) |
| Portfolio | Rank-weighted legs above/below median beta, each scaled to beta 1 | Same construction |
| Weighting | Rank weights | Rank weights |

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

- **Data gap:** Financing uses the USD risk-free rate for all markets, which overstates the cost in EU and Denmark while their rates were negative (2015–21). Betas are raw, not shrunk.

### Signal creation

BAB<sub>t+1</sub> = r<sub>L</sub>/β<sub>L</sub> − r<sub>H</sub>/β<sub>H</sub>, with rank-weighted low- and high-beta legs (the net long cash is financed at the USD risk-free rate + 0.5% a year; the high-beta leg pays a size-tiered borrow fee). Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

### Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = low-beta stocks minus high-beta stocks; **long-only** = low-beta stocks; benchmarks: equal-weight universe and size-weighted universe.
- Frazzini & Pedersen construction: betas ranked, each leg weighted by rank distance from the median and scaled to an ex-ante beta of 1; no risk-free rate is subtracted.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 7. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -4.2% | -1.84 | 0.64 | mkt +0.86 (+8.3), value -0.63 (-4.0), low_risk +1.72 (+10.3) |
| EU | French Europe 5F + WML | -2.4% | -0.70 | 0.29 | Mkt-RF +0.25 (+3.9), RMW +1.15 (+4.2), CMA +0.55 (+2.4), WML +0.33 (+2.8) |
| UK | JKP GBR 7 themes | +3.7% | 1.13 | 0.50 | mkt +0.39 (+7.5), momentum +0.25 (+2.9), low_risk +0.96 (+5.5), quality +0.62 (+4.2) |
| DK | JKP DNK 7 themes | -0.7% | -0.20 | 0.38 | mkt +0.38 (+4.9), low_risk +1.16 (+7.6) |
| SCANDI | French Europe 5F + WML | -1.7% | -0.55 | 0.12 | Mkt-RF +0.13 (+2.2), RMW +0.55 (+2.2), WML +0.33 (+3.5) |
| World | JKP World 7 themes | +1.1% | 0.47 | 0.47 | mkt +0.69 (+8.5), value -0.37 (-2.4), momentum +0.35 (+2.9), low_risk +1.24 (+8.5) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | +1.7% | 1.59 | 0.87 | mkt +0.91 (+30.4), size -0.23 (-3.3), value -0.14 (-2.4), low_risk +0.71 (+9.1) |
| EU | French Europe 5F + WML | +3.7% | 1.94 | 0.65 | Mkt-RF +0.54 (+15.0), RMW +0.46 (+3.3) |
| UK | JKP GBR 7 themes | +4.4% | 2.27 | 0.69 | mkt +0.45 (+13.5), quality +0.39 (+4.1) |
| DK | JKP DNK 7 themes | +5.3% | 2.25 | 0.56 | mkt +0.61 (+11.9), low_risk +0.25 (+2.8), quality +0.13 (+2.3) |
| SCANDI | French Europe 5F + WML | +6.3% | 2.93 | 0.50 | Mkt-RF +0.49 (+10.3), RMW +0.47 (+4.0) |
| World | JKP World 7 themes | +4.3% | 2.79 | 0.78 | mkt +0.70 (+15.7), low_risk +0.48 (+6.9) |

## 8. Statistical detail

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in all six; passes in 0 of 6.
- **L/S CAPM alpha:** +1.1% to +7.7%, |t| past the gate in 0 of 6.
- **Long-only:** Sharpe above the equal-weight universe in all six; alpha +2.4% to +3.7%, passing in 1 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.82, EU 0.90, UK 1.00, DK 0.64, SCANDI 0.87, World 0.94.
- **Publication decay:** gross L/S +4.7% to +17.8% a year in 2013–19 against +3.2% to +6.9% in 2020–26.

## 9. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 9.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +11.6% | -0.08 | -1.0% | +12.6% | -0.4% | -0.4% | +0.3% | 18% | 2013-05 -7%, 2016-04 -7%, 2016-11 -6% |
| EU | +12.7% | -0.02 | -0.2% | +12.9% | -0.4% | +0.7% | +0.6% | 19% | 2019-04 -5%, 2016-10 -5%, 2016-04 -4% |
| UK | +17.8% | 0.38 | +4.4% | +13.4% | -0.6% | +1.4% | +0.7% | 24% | 2016-11 -7%, 2019-04 -4%, 2018-12 -4% |
| DK | +4.7% | 0.20 | +3.0% | +1.6% | -0.5% | -2.0% | -4.9% | 22% | 2013-05 -10%, 2018-10 -10%, 2016-10 -9% |
| SCANDI | +10.0% | -0.01 | -0.1% | +10.2% | -0.5% | -0.1% | -2.2% | 20% | 2016-11 -8%, 2019-06 -7%, 2016-10 -6% |
| World | +12.8% | 0.11 | +1.2% | +11.6% | -0.5% | -0.3% | +0.7% | 23% | 2018-05 -5%, 2018-02 -5%, 2016-04 -5% |

On average across the six universes the gross spread was +11.6% a year, of which the market exposure (beta +0.10) contributed +1.2%; the beta-adjusted spread (CAPM alpha) was +10.4%. Costs took 0.5% a year at 21% monthly turnover across both legs. The long leg beat the universe by -0.1% and the short leg lagged it by -0.8% a year, so most of the spread comes from the long side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +3.4%, +4.0%, +4.9% a year.

### 9.2 The fix ladder

X0 baseline → X3 volatility targeting (BAB is beta-neutral and rank-weighted by construction, so the beta-neutral and buffer steps do not apply).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | 0.90 | – | 0.01 | – | – | +0.2% | -22% | -1.2% (-0.3) | 0.5% |
| X3 + volatility targeting | 0.75 | -0.03 (p 0.518) | 0.06 | +0.05 (p 0.382) | 4 of 6 | +0.6% | -22% | -0.4% (-0.1) | 0.5% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS10_ladder.png)

- **X3 + volatility targeting:** -0.03 design, +0.05 holdout; helps in one window and hurts in the other: not reliable.

**Where it ends:** holdout Sharpe 0.01 → 0.06, return +0.2% → +0.6% a year (six-universe book).

## 10. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Data gap.** Financing uses the USD risk-free rate for all markets, which overstates the cost in EU and Denmark while their rates were negative (2015–21). Betas are raw, not shrunk.
5. **Trials.** Every gated cell is in the factsheet trial ledger; the fix ladder is counted inside FS03–FS12 (25 trials).

## 11. Academic references

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

## 12. Reproduce

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS10` → `build_xs.py FS10`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.

## Appendix

### A. Performance in detail

**US (S&P 500 members, point-in-time)**, median 502 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +4.3% | +2.9% | 16.8% | 0.25 [-0.17, 0.70] | 0.26 | -33% | 55% | 1.17 | 0.14 | +2.4% (0.6) | 9.7% |
| Long-only (net) | +11.1% | +10.9% | 11.8% | 0.94 [0.54, 1.42] | 1.48 | -20% | 66% | 5.35 | 0.64 | +2.6% (1.9) | 7.0% |
| Low-beta stocks (gross) | +11.2% | +11.1% | 11.8% | 0.95 [0.56, 1.44] | 1.51 | -20% | 66% | 5.43 | 0.64 | +2.8% (2.0) | 7.0% |
| High-beta stocks (gross) | +15.7% | +14.0% | 22.8% | 0.69 [0.24, 1.22] | 1.00 | -39% | 60% | 3.08 | 1.39 | -2.5% (-1.4) | 13.0% |
| EW universe | +13.1% | +12.6% | 15.5% | 0.85 [0.41, 1.42] | 1.29 | -28% | 67% | 4.20 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.9% | +14.9% | 14.2% | 1.05 [0.60, 1.61] | 1.73 | -24% | 69% | 5.29 | 0.86 | +3.7% (2.4) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 264 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +4.6% | +3.8% | 12.8% | 0.36 [-0.10, 0.89] | 0.44 | -31% | 55% | 1.59 | 0.09 | +3.6% (1.2) | 8.0% |
| Long-only (net) | +9.3% | +9.1% | 10.2% | 0.91 [0.44, 1.47] | 1.42 | -18% | 64% | 4.33 | 0.62 | +2.6% (2.3) | 6.5% |
| Low-beta stocks (gross) | +9.5% | +9.3% | 10.2% | 0.93 [0.46, 1.50] | 1.45 | -18% | 64% | 4.43 | 0.62 | +2.8% (2.4) | 6.5% |
| High-beta stocks (gross) | +12.1% | +10.3% | 21.4% | 0.57 [0.12, 1.05] | 0.79 | -36% | 56% | 2.32 | 1.42 | -3.2% (-2.2) | 11.8% |
| EW universe | +10.8% | +10.2% | 14.4% | 0.75 [0.29, 1.30] | 1.14 | -26% | 63% | 3.20 | 1.00 | – | 8.4% |
| Size-weighted universe | +10.6% | +10.2% | 13.7% | 0.77 [0.32, 1.29] | 1.21 | -25% | 58% | 3.37 | 0.92 | +0.8% (0.6) | 7.9% |

**UK (FTSE 350, point-in-time)**, median 326 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +9.1% | +8.7% | 11.7% | 0.78 [0.22, 1.37] | 1.21 | -24% | 58% | 2.80 | 0.14 | +7.7% (2.5) | 7.4% |
| Long-only (net) | +9.6% | +9.6% | 9.6% | 1.01 [0.45, 1.68] | 1.55 | -19% | 63% | 4.25 | 0.62 | +3.7% (3.8) | 6.1% |
| Low-beta stocks (gross) | +9.9% | +9.8% | 9.6% | 1.03 [0.47, 1.71] | 1.60 | -19% | 63% | 4.35 | 0.62 | +3.9% (4.0) | 6.1% |
| High-beta stocks (gross) | +9.0% | +6.9% | 21.3% | 0.42 [-0.04, 0.95] | 0.49 | -42% | 55% | 1.71 | 1.44 | -4.8% (-3.3) | 12.6% |
| EW universe | +9.6% | +8.9% | 14.2% | 0.68 [0.19, 1.28] | 0.95 | -30% | 58% | 2.87 | 1.00 | – | 8.8% |
| Size-weighted universe | +8.4% | +7.8% | 12.9% | 0.65 [0.16, 1.25] | 0.90 | -28% | 62% | 2.68 | 0.84 | +0.3% (0.2) | 7.8% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +1.7% | +0.3% | 16.5% | 0.10 [-0.38, 0.56] | 0.03 | -34% | 55% | 0.39 | 0.04 | +1.1% (0.3) | 9.8% |
| Long-only (net) | +10.7% | +10.4% | 12.4% | 0.87 [0.40, 1.37] | 1.39 | -19% | 60% | 3.62 | 0.66 | +2.4% (1.2) | 6.9% |
| Low-beta stocks (gross) | +10.9% | +10.7% | 12.4% | 0.88 [0.42, 1.39] | 1.43 | -19% | 60% | 3.70 | 0.66 | +2.6% (1.4) | 6.9% |
| High-beta stocks (gross) | +15.8% | +14.2% | 22.1% | 0.72 [0.17, 1.36] | 1.04 | -49% | 61% | 2.62 | 1.32 | -0.9% (-0.4) | 13.3% |
| EW universe | +12.6% | +12.0% | 15.2% | 0.83 [0.31, 1.44] | 1.27 | -33% | 66% | 3.31 | 1.00 | – | 8.8% |
| Size-weighted universe | +11.1% | +10.2% | 16.4% | 0.68 [0.11, 1.33] | 0.94 | -40% | 62% | 2.55 | 0.93 | -0.6% (-0.2) | 10.7% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +3.8% | +3.1% | 12.5% | 0.31 [-0.22, 0.82] | 0.37 | -26% | 56% | 1.23 | 0.04 | +3.3% (1.1) | 6.9% |
| Long-only (net) | +11.2% | +11.2% | 10.6% | 1.05 [0.57, 1.58] | 1.83 | -18% | 63% | 4.73 | 0.65 | +3.0% (2.4) | 5.8% |
| Low-beta stocks (gross) | +11.4% | +11.4% | 10.6% | 1.07 [0.59, 1.60] | 1.87 | -18% | 63% | 4.81 | 0.65 | +3.2% (2.6) | 5.8% |
| High-beta stocks (gross) | +14.2% | +12.7% | 20.7% | 0.69 [0.18, 1.31] | 0.97 | -43% | 61% | 2.66 | 1.39 | -3.3% (-2.3) | 12.6% |
| EW universe | +12.6% | +12.3% | 14.2% | 0.89 [0.37, 1.51] | 1.38 | -29% | 66% | 3.63 | 1.00 | – | 8.4% |
| Size-weighted universe | +11.4% | +11.0% | 13.5% | 0.84 [0.37, 1.41] | 1.32 | -26% | 63% | 3.59 | 0.90 | -0.0% (-0.0) | 8.1% |

**World (US + UK + EU, point-in-time)**, median 1088 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +5.9% | +5.1% | 13.3% | 0.44 [0.02, 0.93] | 0.57 | -23% | 57% | 2.12 | 0.24 | +3.2% (1.1) | 8.7% |
| Long-only (net) | +9.9% | +9.6% | 11.6% | 0.85 [0.41, 1.40] | 1.28 | -21% | 66% | 4.31 | 0.67 | +2.4% (2.4) | 7.2% |
| Low-beta stocks (gross) | +10.1% | +9.9% | 11.6% | 0.87 [0.43, 1.42] | 1.31 | -21% | 67% | 4.41 | 0.67 | +2.6% (2.6) | 7.2% |
| High-beta stocks (gross) | +12.7% | +10.6% | 22.7% | 0.56 [0.10, 1.10] | 0.74 | -41% | 58% | 2.25 | 1.37 | -2.8% (-2.0) | 13.0% |
| EW universe | +11.3% | +10.5% | 16.0% | 0.71 [0.25, 1.28] | 1.02 | -30% | 61% | 3.07 | 1.00 | – | 9.7% |
| Size-weighted universe | +11.0% | +10.3% | 14.8% | 0.74 [0.28, 1.31] | 1.10 | -28% | 61% | 3.19 | 0.91 | +0.7% (0.8) | 8.9% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +10.6% | +6.2% | +43.3% | -10.8% | +7.8% | +22.6% |
| 2014 | +17.3% | +21.5% | +7.9% | -1.5% | +24.1% | +16.0% |
| 2015 | +9.8% | +14.1% | +27.3% | -5.4% | +13.0% | +14.4% |
| 2016 | -4.5% | +2.1% | +8.6% | -12.7% | -22.5% | -9.1% |
| 2017 | +11.3% | +14.4% | +21.5% | +30.6% | +11.6% | +18.7% |
| 2018 | +3.2% | +7.8% | -8.0% | -17.9% | +7.0% | -3.3% |
| 2019 | +16.3% | +8.3% | +17.7% | +45.0% | +16.7% | +17.6% |
| 2020 | -14.1% | -7.6% | -0.6% | -25.9% | -8.6% | +0.1% |
| 2021 | +24.8% | +2.3% | +18.4% | +13.3% | +5.6% | +16.0% |
| 2022 | -3.5% | -15.0% | -9.4% | +8.2% | -0.9% | -12.6% |
| 2023 | -17.3% | -6.8% | -15.3% | -11.0% | -17.2% | -10.3% |
| 2024 | +10.1% | +2.7% | +11.4% | -3.7% | +2.1% | +11.4% |
| 2025 | -10.7% | +2.8% | +4.6% | +9.9% | +5.9% | -4.4% |
| 2026 | -3.4% | +5.0% | +5.2% | +7.8% | +8.2% | +1.7% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +21.8% | +13.0% | +25.1% | +17.1% | +14.3% | +24.1% |
| 2014 | +18.9% | +10.6% | +5.8% | +11.2% | +18.7% | +9.5% |
| 2015 | +1.9% | +11.4% | +15.3% | +15.6% | +16.6% | +4.6% |
| 2016 | +9.5% | +10.9% | +15.8% | +2.3% | +10.6% | +2.2% |
| 2017 | +14.0% | +15.5% | +19.8% | +29.1% | +21.7% | +19.5% |
| 2018 | -1.4% | -2.0% | -8.4% | -13.3% | -0.9% | -7.0% |
| 2019 | +27.5% | +20.8% | +20.9% | +36.6% | +28.4% | +24.2% |
| 2020 | +8.4% | +2.6% | +0.9% | +10.0% | +9.9% | +10.6% |
| 2021 | +26.0% | +12.6% | +15.3% | +15.5% | +15.9% | +17.9% |
| 2022 | -4.6% | -9.7% | -11.1% | -5.0% | -9.1% | -10.9% |
| 2023 | +3.0% | +9.3% | +1.5% | +5.8% | +1.4% | +7.5% |
| 2024 | +13.7% | +6.6% | +11.5% | +2.0% | +4.1% | +11.4% |
| 2025 | +6.0% | +15.9% | +13.6% | +15.8% | +15.8% | +13.1% |
| 2026 | +8.7% | +10.3% | +11.1% | +7.8% | +10.1% | +10.4% |

### B. Trading record and current book

The rebalance log per universe is in `results/xs_FS10_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 250 / 250 | 13% | 5% | 55% | -13.8% | 2021-02 |
| EU | 163 | 130 / 130 | 14% | 5% | 55% | -11.8% | 2021-02 |
| UK | 163 | 162 / 162 | 17% | 6% | 58% | -11.0% | 2020-11 |
| DK | 163 | 10 / 10 | 15% | 6% | 55% | -12.0% | 2026-03 |
| SCANDI | 163 | 35 / 35 | 13% | 6% | 56% | -9.6% | 2021-02 |
| World | 163 | 541 / 541 | 16% | 6% | 57% | -12.0% | 2021-09 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: low-beta stocks | Short: high-beta stocks |
|---|---|---|
| US | CF, OXY, EOG, FANG, XOM, APA, CVX, DVN | MRNA, SMCI, BLDR, CCL, NCLH, COIN, UAL, HOOD |
| EU | REP.MC, NESTE.HE, GALP.LS, ENI.MI, TTE.PA, SHELL.AS, JSW.WA, KPN.AS | MTS.MC, MT.AS, IFX.DE, KGH.WA, ENR.DE, IAG.MC, BOL.ST, GLE.PA |
| UK | HBR.L, ITH.L, BP.L, SHEL.L, ENOG.L, BEZ.L, BHMG.L, IMB.L | RPI.L, GDWN.L, RHIM.L, WIZZ.L, ANTO.L, FRES.L, HOC.L, PAF.L |
| DK | TRYG.CO, NSIS-B.CO, JYSK.CO, ISS.CO, NDA-DK.CO, CARL-B.CO, DANSKE.CO, RBREW.CO | ZEAL.CO, GN.CO, NOVO-B.CO, AMBU-B.CO, ROCK-B.CO, ORSTED.CO, DEMANT.CO, DSV.CO |
| SCANDI | NESTE.HE, ELISA.HE, TELIA.ST, TRYG.CO, TEL2-B.ST, EVO.ST, ESSITY-B.ST, MAERSK-B.CO | KCR.HE, METSO.HE, BOL.ST, ROCK-B.CO, ZEAL.CO, GN.CO, QTCOM.HE, KALMAR.HE |

### C. Classification: where does it fit?

| Dimension | Betting against beta |
|---|---|
| Series family | **Low risk** |
| Academic style | Defensive / betting against beta |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 21% of the two legs replaced monthly |
| Market exposure | L/S beta 0.04 to 0.24 |
| Payoff shape | Treynor–Mazuy γ -2.38 to -0.58 (t -5.0 to -0.6); worst 10% of market months -3.4% to -0.1% a month, best 10% -1.0% to +0.7% |
| Nearest factor theme | size (1 of 6 universes), RMW (1 of 6 universes) |
| Nearest library signals (returns) | Volatility (252 days) (6 universes), Volatility (6 universes), Range (MAX−MIN) (5 universes) |
| Economic rationale | Leverage-constrained investors buy high-beta stocks instead of levering the market, bidding them up (Black 1972; Frazzini & Pedersen 2014); lottery demand (Bali, Brown, Murray & Tang 2017). |
| Publication | Black, Jensen & Scholes 1972; Frazzini & Pedersen 2014; critique by Novy-Marx & Velikov (2022) on construction and costs |
| Where it fits | In the **low risk** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

### D. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **MAX**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Beta **(this strategy)** | low risk | +1.00 | +1.00 | +4.4% | -12.6% to -4.2% | 0 / 4 |
| Volatility (252 days) | low risk | +0.66 | +0.86 | +2.4% | -12.9% to -4.8% | 0 / 3 |
| Volatility | low risk | +0.57 | +0.85 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| Range (MAX−MIN) | low risk | +0.42 | +0.77 | -0.7% | -15.4% to -4.8% | 0 / 4 |
| MIN5 | low risk | -0.43 | -0.75 | -0.9% | +2.3% to +13.7% | 4 / 0 |
| MAX5 | low risk | +0.46 | +0.73 | +0.6% | -11.3% to -3.5% | 0 / 2 |
| MAX (best day) (mirror) | low risk | +0.39 | +0.72 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| MIN (worst day) | low risk | -0.36 | -0.71 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| Near 52-week high | momentum | -0.29 | -0.69 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| Idiosyncratic vol | low risk | +0.27 | +0.61 | -3.6% | -15.5% to -4.8% | 0 / 4 |
| 55-day breakout | momentum | -0.21 | -0.60 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| Momentum 12-1 | momentum | -0.11 | -0.47 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| Size | size | +0.02 | -0.28 | +0.1% | -3.8% to +9.9% | 1 / 0 |
| Residual momentum | momentum | -0.05 | -0.28 | +6.4% | +8.0% to +12.2% | 6 / 0 |
| Last month return | short-term reversal | +0.01 | -0.27 | +1.8% | -3.2% to +11.0% | 2 / 0 |
| Skewness | tail direction | +0.03 | +0.10 | -0.4% | -6.7% to +3.9% | 0 / 2 |
| Same-month seasonality | seasonality | +0.10 | -0.09 | -1.9% | -9.4% to +6.6% | 0 / 1 |
| Net tail (MAX+MIN) | tail direction | +0.03 | -0.02 | -0.9% | -5.2% to +5.2% | 0 / 0 |
| Above 52-week low | momentum | +0.18 | -0.01 | +7.5% | +5.2% to +13.6% | 4 / 0 |

![360 map](../figures/xs_FS10_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | -0.3% | -0.13 | 0.88 | Volatility +1.01 (+7.2), Range -0.51 (-2.6) |
| EU | -1.9% | -0.54 | 0.73 | Volatility +0.45 (+2.6), Volatility +0.41 (+2.2) |
| UK | -5.9% | -2.19 | 0.84 | Volatility +0.43 (+3.7), Near 52-week high -0.17 (-2.2) |
| DK | +4.3% | 1.43 | 0.78 | Volatility +0.71 (+11.5), Volatility +0.18 (+2.7) |
| SCANDI | -2.6% | -0.90 | 0.68 |  |
| World | -0.7% | -0.37 | 0.90 | Volatility +0.85 (+7.4) |

![Double sort](../figures/xs_FS10_dsort.png)

Holding MAX fixed (down a column), moving from low to high Beta changes the return by +3.5, +3.5 and +1.5 points a year; holding Beta fixed (along a row), moving from low to high MAX changes it by -0.3, -2.7 and -2.2.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): +32% vs -45% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +4.4%, +3.4%, +4.0%, +4.9% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

