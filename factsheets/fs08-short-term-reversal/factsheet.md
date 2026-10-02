# FACTSHEET FS08 · Short-term reversal

### Buy last month's losers, sell last month's winners

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

> **US, 1999–2012 (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time S&P
> 500 with delisted stocks, 1999–2012, a period this factsheet was not built on. L/S net: t -0.45 (2013–2026: -1.62),
> same sign, weaker. Long-only alpha vs the equal-weight universe: -5.8% a year, t -1.75 (2013–2026: -4.06), same sign,
> weaker. Registered verdicts are unchanged. Pre-registration, method and every result: `PREREG_US_1999_2012.md`.

<div class="kf" markdown="0">
<div><b>Strategy</b>One-month reversal (liquidity provision)</div>
<div><b>Origin</b>Jegadeesh (1990); Lehmann (1990)</div>
<div><b>Family</b>Reversal & bottom-fishing</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (last month's losers)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Registered gate |t| &gt; 2.87 over 12 cells; every cell in the programme trial ledger</div>
</div>

> **The claim.** Stocks with the worst returns last month outperform those with the best returns next month. Jegadeesh (1990) and Lehmann (1990) documented it for US stocks; it is large before costs and famously expensive to trade. **What we find, 2013–2026, point-in-time universes, after costs:** the long/short earned -12.4% to +0.7% a year and was positive in 1 of the six; no universe passes the 2.87 gate (significantly negative in EU). The long-only book (last month's losers) had a higher Sharpe than the equal-weight universe in none of the six, with alphas of -9.3% to -0.8%, none past the gate. **What goes wrong (§9):** the main drags are costs of about 3.9% a year, a weaker second half (2020–26). None of the pre-declared fixes passes the gate in both windows. **Classification (appendix C):** Reversal & bottom-fishing; its returns sit closest to the momentum cluster of the signal library. **360° view (appendix D):** nearest neighbours 55-day breakout, Net tail (MAX+MIN); after its closest neighbours and the market it keeps an alpha of -3.9% to +7.5% (largest |t| 2.7), so it carries some information of its own.

*Layout revised 2 October 2026 (verdict and scorecard, Sharpe anatomy, fit with the other strategies; detail moved to the appendix). No number changed.*

## 1. Verdict and scorecard

> **Verdict.** Of the 12 registered cells (two books × six universes), **0 pass** the |t| > 2.87 gate and **4 are significantly negative** (L/S EU, long-only US, long-only EU, long-only World). Programme-wide (772 trials, |t| > 3.99): long-only alpha vs EW, US t -4.06. US 1999–2012, a period the factsheet was not built on: L/S t -0.45, long-only alpha t -1.75.

| Universe | L/S t | L/S Sharpe | Long-only alpha t | Long-only Sharpe vs equal-weight | Long-only max DD |
|---|---|---|---|---|---|
| US | -1.62 | -0.31 | -4.06 ✖ (neg.) | 0.41 vs 0.85 | -44% |
| EU | -2.92 ✖ (neg.) | -0.79 | -3.30 ✖ (neg.) | 0.19 vs 0.75 | -41% |
| UK | -1.17 | -0.32 | -1.56 | 0.38 vs 0.68 | -49% |
| DK | -1.76 | -0.42 | -1.98 | 0.56 vs 0.83 | -34% |
| SCANDI | +0.19 | 0.05 | -0.38 | 0.74 vs 0.88 | -33% |
| World | -2.03 | -0.50 | -3.81 ✖ (neg.) | 0.33 vs 0.71 | -43% |
| US 1999–2012 | -0.45 | -0.11 | -1.75 | 0.26 vs 0.49 | – |
*✔ passes the 2.87 gate (Bonferroni over 12 cells); ✖ significantly negative. 2013–2026 unless stated.*

## 2. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 503 / 10 | -5.9% | -1.62 | -12.5% (-3.1) | 0.50 | +7.1% | 0.41 | -44% | +12.6% | 0.85 | +14.9% |
| EU | 264 / 10 | -12.4% | -2.92 | -15.7% (-3.6) | 0.30 | +1.9% | 0.19 | -41% | +10.2% | 0.75 | +10.2% |
| UK | 330 / 10 | -5.8% | -1.17 | -10.7% (-2.2) | 0.51 | +6.1% | 0.38 | -49% | +8.9% | 0.68 | +7.8% |
| DK | 20 / 3 | -6.3% | -1.76 | -7.1% (-1.8) | 0.07 | +9.0% | 0.56 | -34% | +12.1% | 0.83 | +10.2% |
| SCANDI | 70 / 5 | +0.7% | 0.19 | -0.7% (-0.2) | 0.11 | +12.3% | 0.74 | -33% | +12.1% | 0.88 | +11.0% |
| World | 1095 / 10 | -8.1% | -2.03 | -13.3% (-3.5) | 0.46 | +5.1% | 0.33 | -43% | +10.5% | 0.71 | +10.3% |

*Monthly, local currency (World in USD). L/S = equal-weighted last month's losers minus last month's winners, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS08_growth.png)

**Read with care.** A long/short book with a negative beta shows a large CAPM alpha in a rising market. The factor-model alpha in section 7, after momentum, value and the other themes, is the better guide: here the L/S CAPM alpha ranges -15.7% to -0.7% and the factor alpha -13.4% to +2.9%.

## 3. Where the Sharpe comes from

Sharpe = annual return ÷ annual volatility. The return splits into the part the market explains (beta × market return) and the rest (alpha, net of costs); the volatility into the market's share and the strategy's own. The last column is the Sharpe the book would have with its market exposure hedged out (before hedging costs).

| Universe | Book | Return / yr | = market part | + alpha | Costs / yr (inside the return) | Volatility | of which market | Sharpe | Sharpe, market hedged |
|---|---|---|---|---|---|---|---|---|---|
| US | L/S | -5.9% | +6.6% | -12.5% | -4.9% | 18.8% | 7.8% | -0.31 | -0.73 |
| US | Long-only | +9.6% | +17.8% | -8.2% | – | 23.4% | 21.0% | 0.41 | -0.79 |
| EU | L/S | -12.4% | +3.3% | -15.7% | -4.9% | 15.7% | 4.4% | -0.79 | -1.04 |
| EU | Long-only | +3.9% | +13.1% | -9.2% | – | 20.0% | 17.6% | 0.19 | -0.96 |
| UK | L/S | -5.8% | +4.9% | -10.7% | -4.7% | 18.3% | 7.3% | -0.32 | -0.64 |
| UK | Long-only | +8.7% | +13.7% | -5.1% | – | 22.9% | 20.3% | 0.38 | -0.47 |
| DK | L/S | -6.3% | +0.8% | -7.1% | -3.9% | 14.9% | 1.0% | -0.42 | -0.48 |
| DK | Long-only | +10.5% | +14.0% | -3.5% | – | 18.8% | 16.9% | 0.56 | -0.43 |
| SCANDI | L/S | +0.7% | +1.4% | -0.7% | -4.6% | 13.4% | 1.6% | 0.05 | -0.06 |
| SCANDI | Long-only | +13.2% | +14.1% | -0.9% | – | 17.9% | 15.9% | 0.74 | -0.11 |
| World | L/S | -8.1% | +5.2% | -13.3% | -4.9% | 16.1% | 7.4% | -0.50 | -0.93 |
| World | Long-only | +7.7% | +15.2% | -7.5% | – | 23.3% | 21.6% | 0.33 | -0.86 |
*Monthly, 2013–2026, market = equal-weight universe. Interactive version: the Strategy Cockpit.*

![Growth, drawdown and rolling Sharpe](../figures/xs_FS08_panel.png)

## 4. How it fits next to the market and the other strategies

A long/short book improves a market portfolio when its own Sharpe beats the hurdle: its correlation with the market × the market's Sharpe. A negative correlation makes the hurdle negative, so even a book with a small positive Sharpe diversifies; the size of the gain still depends on that Sharpe.

| Universe | Corr. with market | Avg corr. with the other strategies | Most similar strategy | Market Sharpe | Hurdle Sharpe | This L/S Sharpe | Verdict | L/S in the worst 10% of market months | Market in those months |
|---|---|---|---|---|---|---|---|---|---|
| US | +0.42 | -0.12 | 52-week high (-0.62) | 0.85 | +0.35 | -0.31 | dilutes | -3.4% | -7.3% |
| EU | +0.28 | -0.15 | Turtle Traders (-0.51) | 0.75 | +0.21 | -0.79 | dilutes | -2.1% | -6.5% |
| UK | +0.40 | -0.17 | Turtle Traders (-0.55) | 0.68 | +0.27 | -0.32 | dilutes | -3.0% | -6.6% |
| DK | +0.07 | -0.05 | 52-week high (-0.43) | 0.83 | +0.06 | -0.42 | dilutes | -2.3% | -7.2% |
| SCANDI | +0.12 | -0.08 | Buy at the 52-week low (+0.45) | 0.89 | +0.11 | 0.05 | dilutes | -0.7% | -6.9% |
| World | +0.46 | -0.16 | 52-week high (-0.65) | 0.71 | +0.33 | -0.50 | dilutes | -3.2% | -7.5% |
*Long/short (net), monthly, 2013–2026; market = equal-weight universe; other strategies = the long/short books of FS01–FS12. The Strategy Cockpit lets you build books of several strategies.*

## 5. Strategy description

Stocks with the worst returns last month outperform those with the best returns next month. Jegadeesh (1990) and Lehmann (1990) documented it for US stocks; it is large before costs and famously expensive to trade.

**Why it might work.** Compensation for providing liquidity to investors who trade on non-information (Nagel 2012); overreaction to short-term news.

| Rule | Original (Jegadeesh (1990); Lehmann (1990)) | This factsheet |
|---|---|---|
| Signal | Previous month's (or week's) return | Return in month t |
| Portfolio | Decile L/S, one month | Extreme quantile L/S, one month |
| Weighting | Equal or value weighted | Equal weighted |

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


### Signal creation

R1<sub>i,t</sub> = total return of stock i in month t. Signals use only information up to month-end t and are traded in month t+1. Eligibility: in the point-in-time universe on any of the last five trading days of month t.

### Model build

- Sort eligible stocks into equal-count groups (deciles ≥ 100 names, quintiles 50–99, terciles < 50; fixed per universe).
- **Long/short** = last month's losers minus last month's winners; **long-only** = last month's losers; benchmarks: equal-weight universe and size-weighted universe.
- Equal weights within each leg, rebalanced monthly.
- Costs: 10 bp per side on the one-way turnover of each leg; short-leg borrow fee 0.25% / 0.75% / 2% a year by size tier (largest 50% / next 30% / smallest 20% of the universe, `code/borrow.py`); net long cash financed at the USD risk-free rate + 0.5%. Code: `code/xs.py` (engine), `code/analyse_xs.py`, `code/build_xs.py`.

## 7. Risk and factor attribution

JKP 7 themes (US, UK, DK, World) or French Europe 5F + WML (EU, SCANDI); Newey-West t, 6 lags.

**Long/short**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -6.2% | -1.80 | 0.59 | low_risk -0.56 (-2.0), short_term_reversal +2.82 (+15.1) |
| EU | French Europe 5F + WML | -9.4% | -2.32 | 0.15 | SMB +0.57 (+2.9), WML -0.30 (-2.2) |
| UK | JKP GBR 7 themes | -7.7% | -2.07 | 0.56 | mkt +0.18 (+2.6), low_risk -0.75 (-2.1), short_term_reversal +2.11 (+7.6) |
| DK | JKP DNK 7 themes | -0.1% | -0.03 | 0.32 | momentum -0.34 (-2.9), short_term_reversal +0.85 (+6.7) |
| SCANDI | French Europe 5F + WML | +2.9% | 0.79 | 0.06 | none &#124;t&#124; ≥ 2 |
| World | JKP World 7 themes | -13.4% | -3.20 | 0.49 | mkt +0.25 (+3.2), short_term_reversal +1.86 (+5.6) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -0.7% | -0.39 | 0.91 | mkt +0.97 (+15.8), size -0.24 (-2.2), value +0.50 (+3.5), low_risk -0.66 (-3.2), quality -0.33 (-2.4), short_term_reversal +1.57 (+9.0) |
| EU | French Europe 5F + WML | +1.5% | 0.42 | 0.66 | Mkt-RF +0.88 (+9.6), WML -0.39 (-4.4) |
| UK | JKP GBR 7 themes | +2.5% | 0.71 | 0.82 | mkt +0.66 (+11.7), low_risk -1.44 (-4.7), short_term_reversal +1.26 (+4.8) |
| DK | JKP DNK 7 themes | +7.0% | 2.38 | 0.72 | mkt +0.69 (+8.8), momentum -0.31 (-3.3), low_risk -0.50 (-4.4), short_term_reversal +0.46 (+4.3) |
| SCANDI | French Europe 5F + WML | +10.1% | 3.02 | 0.55 | Mkt-RF +0.76 (+8.3), RMW +0.60 (+2.2), WML -0.30 (-2.7) |
| World | JKP World 7 themes | -2.2% | -0.67 | 0.85 | mkt +0.86 (+13.2), value +0.34 (+2.9), low_risk -0.45 (-3.1), short_term_reversal +1.09 (+4.4) |

## 8. Statistical detail

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided).
- **L/S mean:** positive in 1 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -15.7% to -0.7%, |t| past the gate in 3 of 6.
- **Long-only:** Sharpe above the equal-weight universe in none of the six; alpha -9.3% to -0.8%, passing in 0 of 6.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.12, EU 0.00, UK 0.12, DK 0.06, SCANDI 0.57, World 0.04.
- **Publication decay:** gross L/S -1.4% to +12.5% a year in 2013–19 against -13.9% to -2.2% in 2020–26.

## 9. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 9.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | +5.1% | 0.41 | +5.3% | -0.2% | -4.2% | +0.0% | +5.1% | 175% | 2014-11 -10%, 2016-04 -8%, 2017-05 -8% |
| EU | -1.4% | 0.25 | +2.6% | -4.0% | -4.1% | -2.3% | +0.9% | 172% | 2015-01 -13%, 2015-09 -9%, 2013-03 -7% |
| UK | +2.1% | 0.22 | +2.6% | -0.4% | -4.0% | +1.8% | +0.4% | 169% | 2013-03 -10%, 2016-04 -10%, 2015-07 -10% |
| DK | +3.8% | -0.16 | -2.4% | +6.3% | -3.3% | +1.9% | +1.9% | 137% | 2019-08 -8%, 2013-07 -8%, 2015-03 -6% |
| SCANDI | +12.5% | 0.04 | +0.7% | +11.8% | -3.9% | +6.9% | +5.6% | 161% | 2017-04 -7%, 2017-10 -7%, 2015-09 -6% |
| World | +2.4% | 0.28 | +3.1% | -0.7% | -4.1% | -0.6% | +2.9% | 173% | 2013-03 -9%, 2014-11 -8%, 2017-04 -7% |

On average across the six universes the gross spread was +4.1% a year, of which the market exposure (beta +0.17) contributed +2.0%; the beta-adjusted spread (CAPM alpha) was +2.1%. Costs took 3.9% a year at 164% monthly turnover across both legs. The long leg beat the universe by +1.3% and the short leg lagged it by +2.8% a year, so most of the spread comes from the short side. Holding longer does not change the picture much: the gross spread 2, 3 and 6 months after formation averages +0.5%, +3.0%, +0.9% a year.

### 9.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.04 | – | -0.87 | – | – | -12.2% | -62% | -16.6% (-3.9) | 3.9% |
| X1 beta-neutral legs | -0.16 | -0.13 (p 0.889) | -1.15 | -0.29 (p 0.926) | 0 of 6 | -12.1% | -61% | -14.7% (-4.2) | 3.8% |
| X2 + turnover buffer | -0.14 | +0.01 (p 0.435) | -0.95 | +0.20 (p 0.029) | 6 of 6 | -9.5% | -55% | -12.0% (-3.6) | 3.0% |
| X3 + volatility targeting | -0.14 | -0.04 (p 0.533) | -0.98 | -0.03 (p 0.639) | 2 of 6 | -9.9% | -54% | -12.7% (-3.8) | 3.0% |

*✔ = passes the gate in the holdout. Design Sharpe = average across universes; tests and holdout columns use the six-universe equal-weighted book.*

![Ladder](../figures/xs_FS08_ladder.png)

- **X1 beta-neutral legs:** -0.13 design, -0.29 holdout; hurts in both windows.
- **X2 + turnover buffer:** +0.01 design, +0.20 holdout; helps in both windows but does not pass the gate.
- **X3 + volatility targeting:** -0.04 design, -0.03 holdout; hurts in both windows.

**Where it ends:** holdout Sharpe -0.87 → -0.98, return -12.2% → -9.9% a year (six-universe book).

## 10. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but 9–25% of member-quarters outside the US have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Trials.** Every gated cell is in the factsheet trial ledger; the fix ladder is counted inside FS03–FS12 (25 trials).

## 11. Academic references

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

## 12. Reproduce

`code/data.py` → `signals.py`, `signals2.py`, `library.py` → `xs.py` + `analyse_xs.py FS08` → `build_xs.py FS08`. Metrics use Project1 `InvestmentLibrary`. Licensed and cached prices are not included.

## Appendix

### A. Performance in detail

**US (S&P 500 members, point-in-time)**, median 503 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -5.9% | -7.4% | 18.8% | -0.31 [-0.77, 0.10] | -0.53 | -70% | 45% | -1.62 | 0.50 | -12.5% (-3.1) | 12.3% |
| Long-only (net) | +9.6% | +7.1% | 23.4% | 0.41 [0.02, 0.90] | 0.46 | -44% | 58% | 2.13 | 1.36 | -8.2% (-4.1) | 13.2% |
| Last month's losers (gross) | +11.7% | +9.3% | 23.4% | 0.50 [0.11, 1.00] | 0.62 | -43% | 60% | 2.58 | 1.35 | -6.1% (-3.0) | 13.0% |
| Last month's winners (gross) | +12.6% | +11.9% | 16.2% | 0.78 [0.25, 1.37] | 1.19 | -28% | 63% | 3.01 | 0.85 | +1.4% (0.6) | 9.6% |
| EW universe | +13.1% | +12.6% | 15.5% | 0.85 [0.41, 1.42] | 1.29 | -28% | 67% | 4.21 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.9% | +14.9% | 14.2% | 1.05 [0.60, 1.61] | 1.73 | -24% | 69% | 5.29 | 0.86 | +3.7% (2.4) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 264 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -12.4% | -12.8% | 15.7% | -0.79 [-1.30, -0.30] | -0.97 | -87% | 43% | -2.92 | 0.30 | -15.7% (-3.6) | 10.9% |
| Long-only (net) | +3.9% | +1.9% | 20.0% | 0.19 [-0.26, 0.68] | 0.13 | -41% | 58% | 0.79 | 1.22 | -9.3% (-3.3) | 12.3% |
| Last month's losers (gross) | +5.9% | +4.0% | 20.0% | 0.29 [-0.17, 0.79] | 0.29 | -39% | 58% | 1.20 | 1.22 | -7.3% (-2.6) | 12.2% |
| Last month's winners (gross) | +13.4% | +12.9% | 15.6% | 0.86 [0.37, 1.41] | 1.45 | -24% | 61% | 3.43 | 0.92 | +3.5% (1.4) | 8.4% |
| EW universe | +10.8% | +10.2% | 14.4% | 0.75 [0.29, 1.30] | 1.14 | -26% | 62% | 3.19 | 1.00 | – | 8.4% |
| Size-weighted universe | +10.6% | +10.2% | 13.7% | 0.77 [0.32, 1.29] | 1.21 | -25% | 58% | 3.37 | 0.91 | +0.8% (0.6) | 7.9% |

**UK (FTSE 350, point-in-time)**, median 330 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -5.8% | -7.2% | 18.3% | -0.32 [-0.94, 0.23] | -0.54 | -68% | 43% | -1.17 | 0.51 | -10.7% (-2.2) | 11.1% |
| Long-only (net) | +8.7% | +6.1% | 22.9% | 0.38 [-0.10, 1.00] | 0.39 | -49% | 56% | 1.44 | 1.42 | -5.0% (-1.6) | 13.3% |
| Last month's losers (gross) | +10.7% | +8.2% | 22.9% | 0.47 [-0.02, 1.10] | 0.54 | -49% | 59% | 1.78 | 1.42 | -3.0% (-0.9) | 13.2% |
| Last month's winners (gross) | +11.7% | +11.0% | 15.8% | 0.74 [0.26, 1.29] | 1.13 | -22% | 63% | 3.07 | 0.92 | +2.9% (1.2) | 8.9% |
| EW universe | +9.6% | +8.9% | 14.2% | 0.68 [0.19, 1.29] | 0.95 | -30% | 58% | 2.87 | 1.00 | – | 8.8% |
| Size-weighted universe | +8.4% | +7.8% | 12.9% | 0.65 [0.16, 1.25] | 0.90 | -28% | 62% | 2.68 | 0.83 | +0.4% (0.2) | 7.8% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -6.3% | -7.1% | 14.9% | -0.42 [-0.90, 0.07] | -0.62 | -64% | 45% | -1.76 | 0.07 | -7.1% (-1.8) | 9.1% |
| Long-only (net) | +10.5% | +9.0% | 18.8% | 0.56 [0.09, 1.17] | 0.69 | -34% | 61% | 2.50 | 1.11 | -3.6% (-2.0) | 12.8% |
| Last month's losers (gross) | +12.0% | +10.7% | 18.8% | 0.64 [0.17, 1.27] | 0.83 | -33% | 63% | 2.86 | 1.11 | -2.0% (-1.1) | 12.7% |
| Last month's winners (gross) | +14.3% | +13.5% | 18.0% | 0.80 [0.29, 1.34] | 1.23 | -31% | 63% | 3.12 | 1.05 | +1.1% (0.5) | 10.0% |
| EW universe | +12.6% | +12.1% | 15.2% | 0.83 [0.31, 1.44] | 1.28 | -33% | 66% | 3.31 | 1.00 | – | 8.8% |
| Size-weighted universe | +11.1% | +10.2% | 16.4% | 0.68 [0.11, 1.33] | 0.94 | -40% | 62% | 2.55 | 0.93 | -0.6% (-0.2) | 10.7% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +0.7% | -0.2% | 13.4% | 0.05 [-0.47, 0.59] | -0.02 | -46% | 53% | 0.19 | 0.11 | -0.7% (-0.2) | 8.1% |
| Long-only (net) | +13.2% | +12.3% | 17.9% | 0.74 [0.24, 1.32] | 1.09 | -33% | 64% | 3.02 | 1.12 | -0.8% (-0.4) | 10.5% |
| Last month's losers (gross) | +15.2% | +14.4% | 17.8% | 0.85 [0.34, 1.44] | 1.31 | -31% | 64% | 3.45 | 1.12 | +1.1% (0.6) | 10.4% |
| Last month's winners (gross) | +9.9% | +8.9% | 16.0% | 0.62 [0.14, 1.12] | 0.88 | -27% | 55% | 2.66 | 1.01 | -2.8% (-1.3) | 9.6% |
| EW universe | +12.5% | +12.1% | 14.2% | 0.88 [0.36, 1.50] | 1.35 | -29% | 66% | 3.59 | 1.00 | – | 8.5% |
| Size-weighted universe | +11.4% | +11.0% | 13.5% | 0.84 [0.37, 1.41] | 1.32 | -26% | 63% | 3.59 | 0.90 | +0.1% (0.1) | 8.1% |

**World (US + UK + EU, point-in-time)**, median 1095 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -8.1% | -9.0% | 16.1% | -0.50 [-1.09, 0.00] | -0.71 | -74% | 44% | -2.03 | 0.46 | -13.3% (-3.5) | 10.7% |
| Long-only (net) | +7.7% | +5.1% | 23.3% | 0.33 [-0.12, 0.83] | 0.34 | -43% | 55% | 1.42 | 1.35 | -7.5% (-3.8) | 13.5% |
| Last month's losers (gross) | +9.7% | +7.2% | 23.3% | 0.42 [-0.03, 0.93] | 0.49 | -43% | 55% | 1.80 | 1.35 | -5.5% (-2.8) | 13.3% |
| Last month's winners (gross) | +12.9% | +12.3% | 16.0% | 0.81 [0.28, 1.41] | 1.24 | -28% | 63% | 3.12 | 0.89 | +2.9% (1.3) | 9.2% |
| EW universe | +11.3% | +10.5% | 16.0% | 0.71 [0.25, 1.28] | 1.02 | -30% | 62% | 3.07 | 1.00 | – | 9.7% |
| Size-weighted universe | +11.0% | +10.3% | 14.8% | 0.74 [0.28, 1.31] | 1.10 | -28% | 61% | 3.19 | 0.91 | +0.7% (0.8) | 8.9% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -6.3% | -0.4% | -8.0% | -3.6% | -3.2% | -6.8% |
| 2014 | -18.2% | -29.1% | -3.4% | -13.5% | -6.3% | -20.4% |
| 2015 | +1.7% | -13.8% | -2.8% | -19.3% | +9.4% | +1.4% |
| 2016 | +4.6% | -7.3% | +20.5% | +17.5% | +19.1% | +7.0% |
| 2017 | -8.2% | -6.5% | -18.5% | -6.7% | -8.4% | -11.5% |
| 2018 | -1.6% | -5.4% | -2.5% | -14.8% | +0.1% | -2.4% |
| 2019 | +29.2% | +22.1% | -8.6% | +46.9% | +49.4% | +14.7% |
| 2020 | -11.7% | -25.3% | -0.6% | -32.3% | -14.1% | -0.7% |
| 2021 | -1.9% | +2.2% | +1.5% | +8.3% | +8.8% | -1.0% |
| 2022 | -9.8% | -16.9% | -21.8% | -2.3% | -7.1% | -22.2% |
| 2023 | -15.0% | -18.0% | +10.7% | -10.1% | -4.3% | -6.7% |
| 2024 | -14.2% | -4.6% | -8.7% | -20.9% | -5.4% | -13.4% |
| 2025 | -25.7% | -39.2% | -28.5% | -10.9% | -17.4% | -34.4% |
| 2026 | -13.2% | -15.8% | -16.2% | -12.6% | -7.5% | -13.7% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +25.6% | +22.3% | +13.9% | +37.5% | +20.3% | +21.7% |
| 2014 | -1.9% | -25.8% | +0.8% | +9.7% | +7.9% | -13.2% |
| 2015 | -10.2% | -7.0% | -1.6% | +14.2% | +17.6% | -7.4% |
| 2016 | +22.0% | +11.6% | +50.1% | +17.1% | +41.5% | +16.1% |
| 2017 | +6.4% | +15.6% | +16.0% | +15.8% | +14.1% | +17.8% |
| 2018 | -9.2% | -7.1% | -14.0% | -17.1% | -10.6% | -11.7% |
| 2019 | +48.6% | +38.2% | +19.7% | +42.6% | +67.5% | +37.2% |
| 2020 | +5.9% | -19.3% | -9.1% | +13.6% | +12.7% | +7.3% |
| 2021 | +31.9% | +17.6% | +24.1% | +22.8% | +25.5% | +23.5% |
| 2022 | -24.9% | -17.6% | -27.9% | -19.8% | -18.8% | -32.3% |
| 2023 | +9.5% | +5.2% | +19.9% | +9.2% | +6.9% | +17.6% |
| 2024 | -1.5% | +2.7% | +3.6% | -9.7% | -8.7% | -2.3% |
| 2025 | +5.0% | -2.2% | +0.1% | +6.1% | +9.5% | +3.8% |
| 2026 | +9.7% | +11.5% | +8.8% | +0.0% | +6.7% | +13.2% |

### B. Trading record and current book

The rebalance log per universe is in `results/xs_FS08_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 86% | 88% | 45% | -28.5% | 2020-03 |
| EU | 163 | 27 / 26 | 85% | 87% | 43% | -13.4% | 2020-03 |
| UK | 163 | 33 / 33 | 84% | 86% | 43% | -26.7% | 2020-03 |
| DK | 163 | 7 / 6 | 65% | 70% | 45% | -10.6% | 2025-03 |
| SCANDI | 163 | 14 / 14 | 79% | 80% | 53% | -12.3% | 2026-01 |
| World | 163 | 110 / 109 | 85% | 88% | 44% | -23.1% | 2020-03 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: last month's losers | Short: last month's winners |
|---|---|---|
| US | DVA, EIX, TTD, PCG, HONA, APP, APTV, TPR | MRNA, PLTR, VEEV, CRM, PSKY, NEM, NOW, SMCI |
| EU | BPOST.BR, ZAL.DE, RBREW.CO, ANA.MC, FME.DE, FER.MC, MRL.MC, GLE.PA | QTCOM.HE, JSW.WA, MAERSK-B.CO, MAERSK-A.CO, AGFB.BR, VWS.CO, BAVA.CO, SAP.DE |
| UK | GBG.L, TRN.L, RPI.L, BATS.L, PRN.L, IMB.L, CCH.L, PRU.L | ONT.L, HOC.L, PAF.L, KNOS.L, HAS.L, HWG.L, EDV.L, FRES.L |
| DK | RBREW.CO, CARL-B.CO, ORSTED.CO, DSV.CO, NOVO-B.CO, AMBU-B.CO, ZEAL.CO, GN.CO | MAERSK-B.CO, MAERSK-A.CO, VWS.CO, BAVA.CO, GMAB.CO, NSIS-B.CO, COLO-B.CO, JYSK.CO |
| SCANDI | RBREW.CO, CARL-B.CO, ORSTED.CO, VOLV-B.ST, WRT1V.HE, AZN.ST, DSV.CO, NOVO-B.CO | QTCOM.HE, MAERSK-B.CO, MAERSK-A.CO, VWS.CO, BAVA.CO, BOL.ST, EVO.ST, GMAB.CO |

### C. Classification: where does it fit?

| Dimension | Short-term reversal |
|---|---|
| Series family | **Reversal & bottom-fishing** |
| Academic style | One-month reversal (liquidity provision) |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; 164% of the two legs replaced monthly |
| Market exposure | L/S beta 0.07 to 0.51 |
| Payoff shape | Treynor–Mazuy γ -2.96 to 0.37 (t -2.3 to 0.3); worst 10% of market months -3.4% to -0.7% a month, best 10% -1.9% to +4.6% |
| Nearest factor theme | short_term_reversal (3 of 6 universes), WML (2 of 6 universes) |
| Nearest library signals (returns) | 55-day breakout (6 universes), Net tail (MAX+MIN) (6 universes), MIN5 (3 universes) |
| Economic rationale | Compensation for providing liquidity to investors who trade on non-information (Nagel 2012); overreaction to short-term news. |
| Publication | Jegadeesh 1990; Lehmann 1990; Nagel 2012 (reversal as liquidity provision) |
| Where it fits | In the **momentum** cluster of the library; with some information beyond its neighbours. |

![Classification map](../figures/battery_map.png)

### D. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Momentum 12-1**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Last month return **(this strategy)** | short-term reversal | +1.00 | +1.00 | +1.8% | -3.2% to +11.0% | 2 / 0 |
| 55-day breakout | momentum | +0.68 | +0.70 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| Net tail (MAX+MIN) | tail direction | +0.62 | +0.63 | -0.9% | -5.2% to +5.2% | 0 / 0 |
| MIN5 | low risk | +0.47 | +0.53 | -0.9% | +2.3% to +13.7% | 4 / 0 |
| Near 52-week high | momentum | +0.43 | +0.52 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| MIN (worst day) | low risk | +0.38 | +0.49 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| Above 52-week low | momentum | +0.40 | +0.46 | +7.5% | +5.2% to +13.6% | 4 / 0 |
| Momentum 12-1 (mirror) | momentum | -0.01 | +0.33 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| Range (MAX−MIN) | low risk | -0.03 | -0.29 | -0.7% | -15.4% to -4.8% | 0 / 4 |
| Volatility | low risk | -0.02 | -0.29 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| Volatility (252 days) | low risk | +0.00 | -0.28 | +2.4% | -12.9% to -4.8% | 0 / 3 |
| Skewness | tail direction | +0.36 | +0.28 | -0.4% | -6.7% to +3.9% | 0 / 2 |
| Beta | low risk | +0.01 | -0.27 | +4.4% | -12.6% to -4.2% | 0 / 4 |
| Idiosyncratic vol | low risk | -0.03 | -0.22 | -3.6% | -15.5% to -4.8% | 0 / 4 |
| Size | size | +0.03 | +0.22 | +0.1% | -3.8% to +9.9% | 1 / 0 |
| Same-month seasonality | seasonality | +0.01 | +0.15 | -1.9% | -9.4% to +6.6% | 0 / 1 |
| MAX (best day) | low risk | +0.32 | -0.05 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| MAX5 | low risk | +0.40 | +0.03 | +0.6% | -11.3% to -3.5% | 0 / 2 |
| Residual momentum | momentum | -0.16 | +0.01 | +6.4% | +8.0% to +12.2% | 6 / 0 |

![360 map](../figures/xs_FS08_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | +1.0% | 0.35 | 0.80 | 55-day breakout +0.91 (+7.7), Net tail +0.80 (+10.4), Near 52-week high -0.27 (-2.6) |
| EU | +7.5% | 2.66 | 0.72 | 55-day breakout +0.51 (+5.4), Net tail +0.63 (+8.4), MIN5 +0.57 (+5.7), MIN -0.47 (-4.1) |
| UK | -0.7% | -0.27 | 0.72 | Net tail +0.66 (+7.3), 55-day breakout +0.70 (+5.9) |
| DK | -3.8% | -1.41 | 0.56 | 55-day breakout +0.43 (+5.5), Net tail +0.29 (+4.1), Above 52-week low +0.18 (+3.3) |
| SCANDI | -3.9% | -1.63 | 0.56 | 55-day breakout +0.27 (+3.5), Net tail +0.40 (+4.4), MIN5 +0.28 (+2.7), Above 52-week low +0.20 (+3.5) |
| World | +3.4% | 1.75 | 0.86 | 55-day breakout +0.71 (+7.8), Net tail +0.99 (+14.2), MIN5 +0.41 (+2.7), MIN -0.58 (-3.2) |

![Double sort](../figures/xs_FS08_dsort.png)

Holding Momentum 12-1 fixed (down a column), moving from low to high Last month return changes the return by -2.8, +0.9 and +0.0 points a year; holding Last month return fixed (along a row), moving from low to high Momentum 12-1 changes it by +2.2, +4.7 and +4.9.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -4% vs +13% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages +1.8%, +0.5%, +3.0%, +0.9% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

