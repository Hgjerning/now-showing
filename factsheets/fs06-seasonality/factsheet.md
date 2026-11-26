# FACTSHEET FS06 · Same-month seasonality
<!-- FS06 version 3 -->

### Do stocks repeat their best calendar month?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Return seasonality (cross-sectional)</div>
<div><b>Origin</b>Heston & Sadka (2008)</div>
<div><b>Family</b>Calendar & seasonality</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, monthly, net of costs</div>
<div><b>Books</b>Long/short and long-only (stocks with the highest past returns in the coming calendar month)</div>
<div><b>Rebalance</b>Monthly</div>
<div><b>Status</b>Gate |t| &gt; 2.87 over 12 cells, fixed for the series; every cell in the programme trial ledger</div>
</div>

> **In two lines.** After costs, the strategy lost money in 5 of 6 markets in 2013–2026: significantly in Denmark, and at the edge of significance in the US and Europe (t -2.88 and -2.89 against a gate of 2.87). Before costs it earned nothing reliable (-0.7% a year across the US, UK and Europe, t -0.29), so most of the loss is trading costs on a signal with no reliable edge. Earlier data are mixed: in 1998–2013 the portfolio spread was small (t +0.4; US 1999–2012 t +1.16), although the cross-sectional slope was strongly positive (t +4.33).

> **The claim.** A stock that did well relative to others in, say, March tends to do well again in March in later years. Heston & Sadka (2008) found it in US stocks 1965–2002, averaging over annual lags of up to 20 years; Heston & Sadka (2010) and Keloharju, Linnainmaa & Nyberg (2016) found it across countries and asset classes. **What we find, 2013–2026, point-in-time blue-chip universes:** the long/short earned -14.0% to +1.4% a year after costs, positive only in the UK; no universe passes the 2.87 gate; Denmark is significantly negative, and the US and EU sit just past it (not past the 2.91 Student-t gate). Before costs the spread is -10.0% to +6.2% a year, with no t beyond the gate; Denmark is the most negative (t -2.43, on 7 long and 6 short names). The long-only book beat the equal-weight universe on Sharpe only in the UK; none is positively past the gate, and US and EU are significantly negative. None of the pre-declared fixes passes. The signal has a low correlation with the other library signals (0.16 or less on average across universes; up to 0.33 with Size in single universes). *Revision history at the end; version 3, 9 October 2026, after a hostile-referee stress test.*

## 1. Verdict and scorecard

> **Verdict.** Of the 12 registered cells (two books × six universes), **0 pass** the |t| > 2.87 gate and **5 are significantly negative** (L/S US, L/S EU, L/S DK, long-only US, long-only EU). Three of the five (L/S US and EU, long-only EU) are within 0.03 of the gate and would not be significant under the Student-t gate of 2.91. Programme-wide (825 trials): none of FS06's cells passes Bonferroni (|t| > 4.01); the five that pass Benjamini–Hochberg are all negative. Denmark rests on 7 long and 6 short names. US 1999–2012, a period the factsheet was not built on: L/S t +1.16, long-only alpha t +0.61.

| Universe | L/S t | L/S Sharpe | Long-only alpha t | Long-only Sharpe vs equal-weight | Long-only max DD |
|---|---|---|---|---|---|
| US | -2.88 ✖ (neg.) | -0.71 | -3.23 ✖ (neg.) | 0.48 vs 0.84 | -38% |
| EU | -2.89 ✖ (neg.) | -0.72 | -2.89 ✖ (neg.) | 0.38 vs 0.76 | -34% |
| UK | +0.34 | 0.11 | +0.89 | 0.75 vs 0.67 | -35% |
| DK | -3.40 ✖ (neg.) | -0.94 | -2.30 | 0.38 vs 0.83 | -46% |
| SCANDI | -2.06 | -0.61 | -1.09 | 0.70 vs 0.92 | -37% |
| World | -1.49 | -0.37 | -1.24 | 0.57 vs 0.71 | -41% |
| US 1999–2012 | +1.16 | 0.29 | +0.61 | 0.52 vs 0.49 | – |
*✔ passes the 2.87 gate (Bonferroni over 12 cells, two-sided, normal approximation); ✖ significantly negative. 2013–2026 unless stated.*

**Before and after costs (L/S).** Costs of 4–5% a year turn a weak, mostly insignificant gross spread into a clear net loss: in the US and EU about half of the net loss is costs, in Denmark under a third.

| Universe | Gross / yr (t) | Costs, borrow, financing / yr | Net / yr (t) | Holdout 2020–26 gross (t) | Names long / short |
|---|---|---|---|---|---|
| US | -3.9% (-1.26) | 5.0% | -9.0% (-2.88) | -3.9% (-0.71) | 51 / 50 |
| EU | -4.2% (-1.33) | 5.0% | -9.2% (-2.89) | -7.6% (-1.77) | 28 / 27 |
| UK | +6.2% (+1.50) | 4.8% | +1.4% (+0.34) | +4.1% (+0.81) | 33 / 32 |
| DK | -10.0% (-2.43) | 4.0% | -14.0% (-3.40) | -9.2% (-1.38) | 7 / 6 |
| SCANDI | -3.1% (-0.83) | 4.6% | -7.7% (-2.06) | -4.8% (-0.89) | 15 / 14 |
| World | +1.5% (+0.65) | 4.9% | -3.4% (-1.49) | +2.5% (+0.64) | 110 / 109 |
| Six universes pooled | -2.3% (-1.00) | 4.7% | -7.0% (-3.11) | -3.1% (-0.86) | |
| US + UK + EU pooled | -0.7% (-0.29) | 4.9% | -5.6% (-2.42) | -2.4% (-0.69) | |

*Newey-West t, 6 lags. The six universes are nested (DK ⊂ SCANDI ⊂ EU ⊂ World; US and UK ⊂ World), so they are not six independent tests; US, UK and continental Europe are the three independent regions.*

## 2. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Long-only CAGR | Long-only Sharpe | Long-only max DD | EW CAGR | EW Sharpe | Size-weighted CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 501 / 10 | -9.0% | -2.88 | -9.2% (-2.8) | 0.02 | +7.8% | 0.48 | -38% | +12.6% | 0.84 | +14.9% |
| EU | 271 / 10 | -9.2% | -2.89 | -7.8% (-2.4) | -0.13 | +5.1% | 0.38 | -34% | +10.4% | 0.76 | +10.6% |
| UK | 327 / 10 | +1.4% | 0.34 | +0.9% (0.2) | 0.05 | +12.4% | 0.75 | -35% | +8.8% | 0.67 | +8.5% |
| DK | 20 / 3 | -14.0% | -3.40 | -13.5% (-3.2) | -0.04 | +5.3% | 0.38 | -46% | +12.0% | 0.83 | +10.2% |
| SCANDI | 72 / 5 | -7.7% | -2.06 | -6.5% (-1.6) | -0.09 | +10.4% | 0.70 | -37% | +12.7% | 0.92 | +11.6% |
| World | 1095 / 10 | -3.4% | -1.49 | -2.8% (-1.2) | -0.06 | +9.2% | 0.57 | -41% | +10.5% | 0.71 | +10.8% |

*Monthly, local currency (World: local-currency returns summed, not converted). L/S = equal-weighted stocks with the highest past returns in the coming calendar month minus stocks with the lowest, net of 10 bp per side on turnover, a size-tiered borrow fee on the short leg and, where the book is net long cash, financing at the USD risk-free rate + 0.5%. Newey-West t (6 lags). CAPM vs the equal-weight universe. Size-weighted universe = market-cap weights in the US, traded-value weights elsewhere (a proxy for the index).*

![Growth](../figures/xs_FS06_growth.png)

## 3. Where the Sharpe comes from

Sharpe = annual return ÷ annual volatility. The return splits into the part the market explains (beta × market return) and the rest (alpha, net of costs); the volatility into the market's share and the strategy's own. The last column is the Sharpe the book would have with its market exposure hedged out (before hedging costs).

| Universe | Book | Return / yr | = market part | + alpha | Costs / yr (inside the return) | Volatility | of which market | Sharpe | Sharpe, market hedged |
|---|---|---|---|---|---|---|---|---|---|
| US | L/S | -9.0% | +0.2% | -9.2% | -5.0% | 12.6% | 0.2% | -0.71 | -0.73 |
| US | Long-only | +9.5% | +15.3% | -5.9% | – | 19.6% | 18.1% | 0.48 | -0.78 |
| EU | L/S | -9.2% | -1.4% | -7.8% | -5.0% | 12.7% | 1.9% | -0.72 | -0.62 |
| EU | Long-only | +6.4% | +11.4% | -5.0% | – | 16.9% | 15.4% | 0.38 | -0.71 |
| UK | L/S | +1.4% | +0.5% | +0.9% | -4.8% | 12.9% | 0.8% | 0.11 | 0.07 |
| UK | Long-only | +13.3% | +10.5% | +2.8% | – | 17.9% | 15.8% | 0.75 | 0.33 |
| DK | L/S | -14.0% | -0.5% | -13.5% | -4.0% | 14.9% | 0.6% | -0.94 | -0.91 |
| DK | Long-only | +6.7% | +12.5% | -5.8% | – | 17.5% | 15.1% | 0.38 | -0.66 |
| SCANDI | L/S | -7.7% | -1.2% | -6.5% | -4.6% | 12.7% | 1.3% | -0.61 | -0.52 |
| SCANDI | Long-only | +11.2% | +12.9% | -1.7% | – | 16.0% | 14.6% | 0.70 | -0.26 |
| World | L/S | -3.4% | -0.7% | -2.8% | -4.9% | 9.4% | 1.0% | -0.37 | -0.30 |
| World | Long-only | +10.6% | +12.4% | -1.8% | – | 18.5% | 17.6% | 0.57 | -0.32 |
*Monthly, 2013–2026, market = equal-weight universe. Sharpe ratios in this factsheet do not subtract a risk-free rate. §3 and §4 use the Strategy Cockpit's market series, which for the European universes predates the 5 October total-return correction, so market Sharpes and long-only alphas here differ slightly from appendix A (Sharpe by up to 0.03, long-only alpha by up to 0.6 points a year). Interactive version: the Strategy Cockpit.*

![Growth, drawdown and rolling Sharpe](../figures/xs_FS06_panel.png)

## 4. How it fits next to the market and the other strategies

A long/short book improves a market portfolio when its own Sharpe beats the hurdle: its correlation with the market × the market's Sharpe. A negative correlation makes the hurdle negative, so even a book with a small positive Sharpe diversifies; the size of the gain still depends on that Sharpe.

| Universe | Corr. with market | Avg corr. with the other strategies | Most similar strategy | Market Sharpe | Hurdle Sharpe | This L/S Sharpe | Verdict | L/S in the worst 10% of market months | Market in those months |
|---|---|---|---|---|---|---|---|---|---|
| US | +0.02 | +0.02 | Size (-0.21) | 0.85 | +0.02 | -0.71 | dilutes | -1.9% | -7.3% |
| EU | -0.15 | +0.08 | Size (-0.30) | 0.74 | -0.11 | -0.72 | dilutes | +0.2% | -6.5% |
| UK | +0.06 | +0.04 | Size (+0.22) | 0.67 | +0.04 | 0.11 | adds | +0.4% | -6.6% |
| DK | -0.04 | -0.00 | Residual momentum (-0.13) | 0.83 | -0.03 | -0.94 | dilutes | -1.5% | -7.2% |
| SCANDI | -0.10 | +0.04 | Short-term reversal (-0.15) | 0.89 | -0.09 | -0.61 | dilutes | -0.4% | -6.9% |
| World | -0.10 | +0.04 | Size (-0.33) | 0.70 | -0.07 | -0.37 | dilutes | -0.7% | -7.5% |
*Long/short (net), monthly, 2013–2026; market = equal-weight universe; other strategies = the long/short books of FS01–FS12. The Strategy Cockpit lets you build books of several strategies.*

## 5. Strategy description

A stock that did well relative to others in, say, March tends to do well again in March in later years, at annual lags up to 20 years. Heston & Sadka (2008) found it in US stocks 1965–2002; Keloharju, Linnainmaa & Nyberg (2016) found the same across markets and asset classes.

**Why it might work.** Heston & Sadka (2008) report that the pattern is not explained by earnings announcements, dividends, size or industry; Keloharju et al. (2016) argue it reflects seasonal variation in risk premia.

| Rule | Original (Heston & Sadka (2008)) | This factsheet |
|---|---|---|
| Signal | Average return in the same calendar month over annual lags 1–20 | Average return in the coming calendar month over all prior years available (1 in 2013, 14 by 2026), no minimum history |
| Portfolio | Decile L/S, one month | Extreme quantile L/S, one month |
| Weighting | Equal weighted | Equal weighted |

## 6. Method: data, signal and portfolio

### Data load

| Universe | Prices | Membership | Names eligible (median) | Currency |
|---|---|---|---|---|
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: the S&P 500 members at each month-end (Sharadar add/remove history; corrected 2 Oct 2026) | ~503 | USD |
| EU | Project1 yfinance cache, Adj Close (TR); EODHD (cleaned) for members that stopped trading | **Point-in-time**: union of 11 national blue-chip indices (CAC 40, DAX, AEX, IBEX 35, FTSE MIB, OMXS30, OMXC25, OMXH25, BEL 20, PSI-20, WIG20), quarterly Wikipedia snapshots 2012–2026; 89% of member-quarters priced (v2 panel, total-return corrected 5 Oct 2026) | ~272 | local (EUR, SEK, DKK, PLN) |
| UK | Project1 cache, Close + pence dividends (Yahoo under-adjusts LSE ~100×); EODHD (cleaned) for members that stopped trading | **Point-in-time**: FTSE 100 + FTSE 250, quarterly snapshots; 92% priced (v2 panel, total-return corrected 5 Oct 2026) | ~333 | GBP |
| DK | Project1 cache, Adj Close | **Point-in-time**: OMX Copenhagen 25, quarterly snapshots; 99% priced (v2 panel, total-return corrected 5 Oct 2026) | ~20 | DKK |
| SCANDI | Project1 cache, Adj Close | **Point-in-time**: OMXC25 + OMXS30 + OMXH25 (Oslo has no snapshot history; v2 panel, total-return corrected 5 Oct 2026) | ~72 | local (DKK, SEK, EUR) |
| World | US Sharadar + UK + EU above | **Point-in-time** union of the three; local-currency returns summed, not converted | ~1,105 | mixed |

*Membership comes from Project2's cache of dated Wikipedia index pages (the same parsing as `run_wiki_pit.py` / `run_eu_pit.py`), with a short list of verified ticker renames (e.g. NZYM-B → NSIS-B, WDH → DEMANT, DAI → MBG). A name is eligible from the day after the snapshot that lists it, once it has 60 days of prices. Since 2 October 2026 members that stopped trading are priced from EODHD after a vendor-glitch filter (v2 panel). The member-quarters still without a price are mostly delisted names, so some survivorship remains; see Caveats.*

- **Design choice:** every factsheet in this series starts its universes in 2012 for comparability, so the signal averages 1 prior year in 2013 and 14 by 2026 (Heston & Sadka use up to 20). The early years test a much noisier signal than the paper's; the 2020–26 holdout (8 to 14 years of history) is the fairer test, and its pooled gross spread is -3.1% (t -0.86). Longer US history is used in the separate 1999–2012 test.

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
| US | JKP USA 7 themes | -8.4% | -2.90 | 0.29 | mkt +0.18 (+2.7), value -0.78 (-5.1), momentum -0.34 (-2.6), low_risk +0.37 (+2.2) |
| EU | French Europe 5F + WML | -7.3% | -2.02 | 0.14 | CMA -0.44 (-2.1) |
| UK | JKP GBR 7 themes | -0.3% | -0.09 | 0.18 | quality +0.70 (+2.5), short_term_reversal -0.52 (-2.8) |
| DK | JKP DNK 7 themes | -9.5% | -2.60 | 0.06 | none &#124;t&#124; ≥ 2 |
| SCANDI | French Europe 5F + WML | -4.9% | -1.36 | 0.08 | none &#124;t&#124; ≥ 2 |
| World | JKP World 7 themes | +0.1% | 0.02 | 0.29 | mkt +0.10 (+2.3), value -0.70 (-4.4), momentum -0.31 (-3.0), low_risk +0.33 (+2.4) |

**Long-only**

| Universe | Factor model | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|
| US | JKP USA 7 themes | -2.3% | -1.35 | 0.90 | mkt +1.10 (+24.2), size -0.31 (-2.7), momentum -0.18 (-2.2) |
| EU | French Europe 5F + WML | +1.8% | 0.63 | 0.69 | Mkt-RF +0.80 (+12.9), CMA -0.51 (-2.7), WML -0.15 (-2.0) |
| UK | JKP GBR 7 themes | +6.8% | 2.26 | 0.72 | mkt +0.66 (+12.5), low_risk -0.75 (-4.0), quality +0.77 (+3.2) |
| DK | JKP DNK 7 themes | +1.8% | 0.62 | 0.60 | mkt +0.61 (+8.0), low_risk -0.57 (-3.9), quality +0.23 (+2.2) |
| SCANDI | French Europe 5F + WML | +7.5% | 2.58 | 0.57 | Mkt-RF +0.69 (+10.6), WML -0.19 (-2.6) |
| World | JKP World 7 themes | +4.2% | 1.82 | 0.83 | mkt +0.87 (+14.9), momentum -0.20 (-2.3) |

## 8. Statistical detail

- **Gate:** |t| > 2.87 (2 books × 6 universes, Bonferroni 0.05/12, two-sided, normal approximation; Student-t with 162 degrees of freedom gives 2.91; under it L/S US and EU and long-only EU would not be significant).
- **L/S mean:** positive in 1 of the six; passes in 0 of 6.
- **L/S CAPM alpha:** -13.5% to +0.9%, past the gate in 1 of 6 (Denmark, negative).
- **Long-only:** Sharpe above the equal-weight universe in 1 of the six (UK); alpha -5.8% to +2.6%; none positively past the gate, US and EU significantly negative.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.01, EU 0.00, UK 0.66, DK 0.00, SCANDI 0.01, World 0.09.
- **Sub-periods (both after publication):** gross L/S -10.8% to +8.2% a year in 2013–19 against -9.2% to +4.1% in 2020–26. Pooled: -1.4% and -3.1%. The comparison with the paper's era is the 1999–2013 evidence: 1998–2013 (FS15, ART liquidity universe): the portfolio spread was small, +1.0% a year (t +0.4), while the cross-sectional Fama-MacBeth slope was strongly positive (t +4.33 averaged across markets; UK +4.04, World +3.66); the pre-registered US 1999–2012 test gave L/S t +1.16.

### 8.1 Sensitivity checks (added 9 October 2026; reported, not gated, not trials)

Gross L/S return a year (Newey-West t), same universes and portfolio rules; only the signal changes (the 5-year and 2–5-year variants start later, in 2017 and 2014). Code and results: `sens.py` and `sens_<universe>.json` (in `results/sensitivity/` of the published folder).

| Signal | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| As published (rebuilt) | -3.9% (-1.25) | -4.2% (-1.30) | +6.0% (+1.43) | -10.0% (-2.43) | -3.4% (-0.90) | +1.4% (+0.62) |
| At least 5 years of history (from 2017) | -5.4% (-1.35) | -6.7% (-1.88) | +6.0% (+1.52) | -9.6% (-1.95) | -3.8% (-0.82) | +2.2% (+0.74) |
| Lag 12 months only | -0.2% (-0.05) | +1.3% (+0.32) | +3.6% (+0.98) | -5.6% (-1.21) | -6.8% (-1.75) | +2.1% (+0.77) |
| Lags 2–5 years | -3.8% (-1.00) | -2.8% (-0.88) | +1.5% (+0.35) | -3.2% (-0.64) | -2.3% (-0.65) | -1.5% (-0.57) |
| Placebo: wrong month (t, not t+1) | -1.1% (-0.36) | +2.8% (+1.00) | -3.9% (-0.97) | +0.5% (+0.10) | -7.0% (-1.65) | -2.9% (-1.35) |
| Placebo: wrong month (t+2) | +3.1% (+0.82) | +2.0% (+0.60) | +4.9% (+1.33) | +2.2% (+0.52) | +0.0% (+0.00) | +2.0% (+0.69) |

- **No variant earns a reliable premium.** Requiring five years of history does not help, so the result is not driven by short-history stocks (recent listings and spin-offs) landing in the extreme groups. Lag 12 alone, Heston & Sadka's cleanest test, is close to zero in the US, EU and World, positive but not significant in the UK and negative in DK and SCANDI.
- **The month alignment is as specified.** The code averages the coming calendar month in earlier years (`signals2.py`). Shifting the signal one month either way gives no reliable premium either (every |t| below 2).
- The rebuilt baseline matches the published gross numbers to within 0.3 points a year (monthly returns are recomputed from daily data; US net t −2.87 against −2.88).

## 9. What goes wrong, and how to fix it

**Method.** Diagnose on the design window (2013–2019); apply the same pre-declared fix ladder used for every sort strategy in FS03–FS12; judge on the holdout (Jan 2020 – Aug 2026) with a pooled six-universe paired bootstrap of the Sharpe difference against the previous step. 25 fix trials across FS03–FS12, gate p < 0.0020.

### 9.1 Diagnosis (design window 2013–2019)

| Universe | L/S gross / yr | Beta | Beta drag / yr | CAPM alpha (gross) | Costs / yr | Long leg vs EW / yr | EW vs short leg / yr | Turnover / month | Worst months |
|---|---|---|---|---|---|---|---|---|---|
| US | -4.0% | -0.13 | -1.7% | -2.3% | -4.1% | -3.2% | -0.8% | 172% | 2013-05 -9%, 2019-06 -7%, 2016-11 -7% |
| EU | -1.0% | -0.12 | -1.3% | +0.3% | -4.0% | -2.2% | +1.3% | 168% | 2013-04 -9%, 2016-03 -9%, 2013-09 -8% |
| UK | +8.2% | 0.13 | +1.5% | +6.7% | -4.0% | +7.1% | +1.1% | 165% | 2016-06 -15%, 2016-09 -6%, 2018-08 -6% |
| DK | -10.8% | -0.17 | -2.6% | -8.2% | -3.2% | -4.0% | -6.8% | 135% | 2016-12 -11%, 2013-07 -8%, 2013-09 -7% |
| SCANDI | -1.5% | -0.31 | -4.7% | +3.3% | -3.8% | +0.5% | -1.9% | 157% | 2013-09 -13%, 2017-08 -8%, 2018-02 -7% |
| World | +0.5% | -0.00 | -0.1% | +0.6% | -4.0% | +0.3% | +0.2% | 169% | 2013-04 -7%, 2013-05 -5%, 2016-03 -5% |

On average across the six universes the gross spread was -1.4% a year, of which the market exposure (beta -0.10) contributed -1.5%; the beta-adjusted spread (CAPM alpha) was +0.1%. Costs took 3.9% a year at 161% monthly turnover across both legs. The long leg trailed the universe by 0.3% a year and the short leg beat it by 1.1%. Holding longer does not change the picture much: over the full sample, the gross spread 2, 3 and 6 months after formation averages -1.9%, +0.7%, -0.9% a year.

### 9.2 The fix ladder

X0 baseline → X1 **beta-neutral legs** (each leg scaled by 1/its ex-ante beta) → X2 **+ turnover buffer** (enter the extreme 1/q, keep a name until it leaves the extreme 3/q) → X3 **+ volatility targeting** (scale the L/S to 10% a year using its trailing 6-month volatility, lagged; Barroso & Santa-Clara 2015; Moreira & Muir 2017).

| Step | Design Sharpe (avg) | Δ design (p) | Holdout Sharpe (book) | Δ holdout (p) | Universes improved | Holdout return / yr | Holdout max DD | Holdout alpha vs EW (t) | Costs / yr |
|---|---|---|---|---|---|---|---|---|---|
| X0 baseline | -0.55 | – | -0.87 | – | – | -7.9% | -49% | -7.8% (-2.0) | 3.9% |
| X1 beta-neutral legs | -0.55 | -0.07 (p 0.763) | -1.04 | -0.18 (p 0.843) | 0 of 6 | -8.8% | -51% | -8.7% (-2.4) | 3.7% |
| X2 + turnover buffer | -0.55 | +0.03 (p 0.379) | -0.84 | +0.20 (p 0.029) | 5 of 6 | -6.6% | -45% | -6.2% (-1.7) | 2.9% |
| X3 + volatility targeting | -0.41 | +0.17 (p 0.330) | -0.78 | +0.06 (p 0.297) | 4 of 6 | -7.1% | -50% | -6.2% (-1.4) | 2.9% |

*No step passes (a pass would be marked ✔). Design Sharpe = average across the six universes; Δ, p and the holdout columns use the pooled six-universe book. p is one-sided, from a paired bootstrap; gate 0.05/25 = 0.0020.*

![Ladder](../figures/xs_FS06_ladder.png)

- **X1 beta-neutral legs:** -0.07 design, -0.18 holdout; point estimate, not past the 0.0020 gate.
- **X2 + turnover buffer:** +0.03 design, +0.20 holdout; point estimate, not past the 0.0020 gate.
- **X3 + volatility targeting:** +0.17 design, +0.06 holdout; point estimate, not past the 0.0020 gate.

**Where it ends:** holdout Sharpe -0.87 → -0.78, return -7.9% → -7.1% a year (six-universe book). The book still loses money.

## 10. Caveats

1. **Residual survivorship.** Point-in-time membership everywhere, but about 8% (UK), 11% (EU) and 1% (DK) of member-quarters have no price (mostly delisted names); long books are flattered and short books penalised by an unknown amount.
2. **Currency.** Local currency; World sums local-currency returns without conversion.
3. **Equal weighting and flat trading costs.** 10 bp per side for every stock and a size-tiered borrow fee, but no market impact; blue-chip universes only.
4. **Start date.** All universes start in 2012 (a design choice for the series): the signal uses 1 to 14 years of history, against up to 20 in the paper.
5. **Trials.** Every gated cell is in the factsheet trial ledger; the fix ladder is counted inside FS03–FS12 (25 trials).
6. **Low breadth in Denmark.** 7 long and 6 short names a month; one stock moves the result.
7. **Nested universes.** DK ⊂ SCANDI ⊂ EU ⊂ World and US, UK ⊂ World; the pooled tests count Danish stocks several times.
8. **Factor attribution (§7).** French Europe factors are in USD while EU and SCANDI books are in local currency; the JKP themes end in December 2025. Read the long-only factor alphas (UK +6.8%, SCANDI +7.5%) with this in mind.
9. **Financing and delistings.** Net cash is financed at the USD rate in every universe; a stock's missing months count as a zero return, with no delisting return.
10. **Partial years.** 2013 is February–December and 2026 January–August in the calendar-year tables.

## 11. Academic references

- Heston, S. & Sadka, R. (2008). Seasonality in the cross-section of stock returns. *Journal of Financial Economics*, 87(2), 418–445.
- Heston, S. & Sadka, R. (2010). Seasonality in the cross section of stock returns: the international evidence. *Journal of Financial and Quantitative Analysis*, 45(5), 1133–1160.
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
| L/S (net) | -9.0% | -9.3% | 12.6% | -0.71 [-1.19, -0.23] | -0.92 | -74% | 37% | -2.88 | 0.02 | -9.2% (-2.8) | 8.8% |
| Long-only (net) | +9.5% | +7.8% | 19.6% | 0.48 [0.09, 0.98] | 0.60 | -38% | 60% | 2.42 | 1.17 | -5.8% (-3.2) | 12.5% |
| Stocks with the highest past returns in the coming calendar month (gross) | +11.5% | +10.0% | 19.6% | 0.59 [0.18, 1.10] | 0.78 | -36% | 61% | 2.94 | 1.17 | -3.8% (-2.1) | 12.3% |
| Stocks with the lowest (gross) | +15.5% | +14.4% | 19.5% | 0.79 [0.34, 1.36] | 1.20 | -33% | 62% | 3.85 | 1.15 | +0.3% (0.2) | 11.4% |
| EW universe | +13.1% | +12.6% | 15.5% | 0.84 [0.41, 1.42] | 1.29 | -28% | 67% | 4.20 | 1.00 | – | 9.2% |
| Size-weighted universe | +14.9% | +14.9% | 14.2% | 1.05 [0.60, 1.61] | 1.73 | -24% | 70% | 5.29 | 0.86 | +3.7% (2.4) | 8.3% |

**EU (11 national blue-chip indices, point-in-time)**, median 271 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -9.2% | -9.5% | 12.7% | -0.72 [-1.20, -0.25] | -0.89 | -78% | 43% | -2.89 | -0.13 | -7.8% (-2.4) | 9.1% |
| Long-only (net) | +6.4% | +5.1% | 16.9% | 0.38 [-0.11, 0.92] | 0.46 | -34% | 55% | 1.46 | 1.07 | -5.3% (-2.9) | 10.2% |
| Stocks with the highest past returns in the coming calendar month (gross) | +8.5% | +7.3% | 16.9% | 0.50 [0.00, 1.05] | 0.67 | -33% | 57% | 1.93 | 1.07 | -3.2% (-1.8) | 10.0% |
| Stocks with the lowest (gross) | +12.7% | +11.4% | 19.3% | 0.66 [0.18, 1.18] | 0.97 | -30% | 60% | 2.63 | 1.20 | -0.4% (-0.2) | 10.6% |
| EW universe | +10.9% | +10.4% | 14.3% | 0.76 [0.30, 1.32] | 1.17 | -26% | 61% | 3.22 | 1.00 | – | 8.3% |
| Size-weighted universe | +11.1% | +10.6% | 13.7% | 0.80 [0.35, 1.33] | 1.28 | -25% | 58% | 3.50 | 0.92 | +1.1% (0.8) | 7.8% |

**UK (FTSE 350, point-in-time)**, median 327 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | +1.4% | +0.6% | 12.9% | 0.11 [-0.52, 0.71] | 0.07 | -48% | 48% | 0.34 | 0.05 | +0.9% (0.2) | 7.2% |
| Long-only (net) | +13.3% | +12.4% | 17.9% | 0.75 [0.23, 1.30] | 1.22 | -35% | 60% | 3.12 | 1.13 | +2.6% (0.9) | 9.5% |
| Stocks with the highest past returns in the coming calendar month (gross) | +15.3% | +14.7% | 17.9% | 0.86 [0.35, 1.43] | 1.49 | -33% | 61% | 3.60 | 1.13 | +4.7% (1.6) | 9.3% |
| Stocks with the lowest (gross) | +9.2% | +8.0% | 17.1% | 0.54 [0.04, 1.14] | 0.69 | -33% | 60% | 2.02 | 1.08 | -1.0% (-0.4) | 10.8% |
| EW universe | +9.4% | +8.8% | 14.1% | 0.67 [0.18, 1.28] | 0.95 | -30% | 59% | 2.82 | 1.00 | – | 8.7% |
| Size-weighted universe | +9.0% | +8.5% | 12.7% | 0.70 [0.21, 1.32] | 1.01 | -28% | 63% | 2.91 | 0.84 | +1.1% (0.6) | 7.8% |

**DK (OMXC25, point-in-time)**, median 20 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -14.0% | -14.1% | 14.9% | -0.94 [-1.52, -0.41] | -1.12 | -88% | 37% | -3.40 | -0.04 | -13.5% (-3.2) | 9.0% |
| Long-only (net) | +6.7% | +5.3% | 17.5% | 0.38 [-0.13, 0.96] | 0.45 | -46% | 55% | 1.40 | 0.99 | -5.8% (-2.3) | 10.6% |
| Stocks with the highest past returns in the coming calendar month (gross) | +8.2% | +6.9% | 17.5% | 0.47 [-0.04, 1.06] | 0.60 | -45% | 56% | 1.73 | 1.00 | -4.3% (-1.7) | 10.4% |
| Stocks with the lowest (gross) | +18.2% | +18.0% | 17.7% | 1.03 [0.51, 1.66] | 1.76 | -25% | 62% | 4.17 | 1.04 | +5.2% (2.1) | 9.4% |
| EW universe | +12.6% | +12.0% | 15.2% | 0.83 [0.31, 1.44] | 1.27 | -33% | 66% | 3.31 | 1.00 | – | 8.8% |
| Size-weighted universe | +11.1% | +10.2% | 16.4% | 0.68 [0.11, 1.33] | 0.94 | -40% | 62% | 2.55 | 0.93 | -0.6% (-0.2) | 10.7% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 72 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -7.7% | -8.2% | 12.7% | -0.61 [-1.17, -0.03] | -0.79 | -71% | 44% | -2.06 | -0.09 | -6.5% (-1.6) | 8.3% |
| Long-only (net) | +11.2% | +10.4% | 16.0% | 0.70 [0.17, 1.30] | 1.05 | -37% | 59% | 2.55 | 1.03 | -2.3% (-1.1) | 9.0% |
| Stocks with the highest past returns in the coming calendar month (gross) | +13.0% | +12.4% | 16.0% | 0.82 [0.29, 1.43] | 1.30 | -35% | 62% | 2.98 | 1.03 | -0.4% (-0.2) | 8.9% |
| Stocks with the lowest (gross) | +16.1% | +15.6% | 17.8% | 0.91 [0.39, 1.54] | 1.42 | -28% | 62% | 3.69 | 1.12 | +1.5% (0.7) | 11.1% |
| EW universe | +13.0% | +12.7% | 14.1% | 0.92 [0.41, 1.55] | 1.45 | -28% | 66% | 3.77 | 1.00 | – | 8.4% |
| Size-weighted universe | +11.9% | +11.6% | 13.5% | 0.88 [0.41, 1.45] | 1.41 | -26% | 63% | 3.78 | 0.90 | +0.2% (0.1) | 8.0% |

**World (US + UK + EU, point-in-time)**, median 1095 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S (net) | -3.4% | -3.8% | 9.4% | -0.37 [-0.81, 0.10] | -0.53 | -48% | 46% | -1.49 | -0.06 | -2.8% (-1.2) | 6.1% |
| Long-only (net) | +10.6% | +9.2% | 18.5% | 0.57 [0.09, 1.12] | 0.76 | -41% | 59% | 2.41 | 1.11 | -2.0% (-1.2) | 11.6% |
| Stocks with the highest past returns in the coming calendar month (gross) | +12.6% | +11.5% | 18.5% | 0.68 [0.20, 1.25] | 0.97 | -40% | 60% | 2.87 | 1.11 | +0.1% (0.0) | 11.4% |
| Stocks with the lowest (gross) | +11.1% | +9.6% | 19.5% | 0.57 [0.11, 1.11] | 0.78 | -36% | 60% | 2.42 | 1.17 | -2.1% (-1.6) | 11.5% |
| EW universe | +11.3% | +10.5% | 15.9% | 0.71 [0.25, 1.28] | 1.03 | -30% | 64% | 3.10 | 1.00 | – | 9.6% |
| Size-weighted universe | +11.4% | +10.8% | 14.7% | 0.77 [0.31, 1.34] | 1.17 | -28% | 62% | 3.36 | 0.91 | +1.1% (1.2) | 8.8% |

*Sharpe CI: stationary bootstrap (mean block 6 months, 5,000 draws). Max drawdown on monthly returns.*

**Calendar-year returns, L/S (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -15.9% | -17.1% | +29.3% | -27.1% | -27.3% | -9.4% |
| 2014 | -11.2% | +1.5% | +6.3% | +7.7% | +3.8% | -5.9% |
| 2015 | +3.9% | +11.3% | +34.5% | -20.5% | +1.5% | +9.2% |
| 2016 | -7.4% | -12.0% | -28.0% | -18.7% | +1.8% | -12.0% |
| 2017 | -16.5% | -6.5% | -3.3% | -19.6% | -6.8% | -7.9% |
| 2018 | -2.9% | -18.4% | -10.6% | -8.1% | -16.3% | -2.4% |
| 2019 | -11.9% | -0.1% | +3.9% | -9.9% | +2.4% | -2.3% |
| 2020 | +1.7% | -14.6% | +27.0% | +12.2% | -1.0% | +0.0% |
| 2021 | -11.0% | -15.3% | -5.7% | -24.1% | -17.9% | -5.7% |
| 2022 | -28.4% | -6.5% | -9.5% | -21.9% | -4.7% | -16.8% |
| 2023 | +15.6% | -2.4% | -4.2% | -18.3% | +5.4% | +14.5% |
| 2024 | +9.5% | -22.2% | -17.3% | -12.3% | -3.8% | +5.7% |
| 2025 | -21.8% | -12.6% | +2.5% | +6.4% | -20.2% | -7.9% |
| 2026 | -19.9% | -9.2% | +3.1% | -26.4% | -19.9% | -6.2% |

**Calendar-year returns, long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +17.6% | +16.9% | +33.9% | +21.8% | +11.9% | +21.3% |
| 2014 | +8.9% | -1.0% | +10.8% | +17.4% | +13.6% | -0.7% |
| 2015 | +0.2% | +3.7% | +26.1% | +11.4% | +13.8% | +5.1% |
| 2016 | +9.9% | +5.7% | +16.6% | +6.4% | +28.1% | +4.7% |
| 2017 | +5.5% | +16.2% | +27.5% | +10.5% | +13.4% | +22.6% |
| 2018 | -11.5% | -24.1% | -13.2% | -12.2% | -15.2% | -13.0% |
| 2019 | +21.3% | +27.9% | +26.7% | +12.7% | +39.5% | +26.4% |
| 2020 | +11.1% | +1.9% | +26.0% | +48.1% | +30.2% | +13.2% |
| 2021 | +20.8% | +2.2% | +7.0% | +4.0% | +10.2% | +11.2% |
| 2022 | -27.6% | -17.8% | -23.8% | -30.5% | -18.8% | -28.4% |
| 2023 | +26.3% | +17.2% | +8.1% | -1.4% | +12.1% | +27.2% |
| 2024 | +18.7% | +2.8% | -3.0% | -5.0% | +3.7% | +14.5% |
| 2025 | +3.8% | +17.5% | +16.1% | +17.9% | +9.1% | +17.5% |
| 2026 | +15.1% | +13.4% | +28.0% | -8.4% | +3.8% | +20.5% |

### B. Trading record and current book

The rebalance log per universe is in `results/xs_FS06_record_<universe>.csv` (names per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names long / short | Turnover long leg / month | Turnover short leg / month | L/S months positive | Worst L/S month | When |
|---|---|---|---|---|---|---|---|
| US | 163 | 51 / 50 | 85% | 87% | 37% | -11.9% | 2026-04 |
| EU | 163 | 28 / 27 | 86% | 82% | 43% | -12.3% | 2024-10 |
| UK | 163 | 33 / 32 | 85% | 81% | 48% | -15.0% | 2016-06 |
| DK | 163 | 7 / 6 | 64% | 72% | 37% | -11.1% | 2016-12 |
| SCANDI | 163 | 15 / 14 | 79% | 80% | 44% | -12.8% | 2013-09 |
| World | 163 | 110 / 109 | 85% | 84% | 46% | -8.5% | 2022-01 |

**Current book** (signal at 31 August 2026; first 8 names per leg)

| Universe | Long: stocks with the highest past returns in the coming calendar month | Short: stocks with the lowest |
|---|---|---|
| US | SNDK, GEV, APP, CEG, HOOD, PLTR, TKO, MU | CVNA, KVUE, DXCM, VTRS, EFX, SWKS, XYZ, INCY |
| EU | ZEAL.CO, JSW.WA, HM-B.ST, NKT.CO, BOL.ST, FORTUM.HE, BKT.MC, ITX.MC | PUIG.MC, DSFIR.AS, DTG.DE, BMPS.MI, BAVA.CO, ANE.MC, ORSTED.CO, EDEN.PA |
| UK | CWR.L, GDWN.L, ALFA.L, TRST.L, HWG.L, JD.L, AVON.L, GFRD.L | MTLN.L, THG.L, OCDO.L, AML.L, MTRO.L, OXIG.L, DOCS.L, BCG.L |
| DK | ZEAL.CO, NKT.CO, NDA-DK.CO, JYSK.CO, GMAB.CO, TRYG.CO, VWS.CO, DSV.CO | BAVA.CO, ORSTED.CO, GN.CO, DEMANT.CO, AMBU-B.CO, ISS.CO, COLO-B.CO, NOVO-B.CO |
| SCANDI | ZEAL.CO, HM-B.ST, NKT.CO, BOL.ST, FORTUM.HE, SWED-A.ST, NOKIA.HE, SKA-B.ST | BAVA.CO, ORSTED.CO, METSO.HE, QTCOM.HE, EQT.ST, WRT1V.HE, GN.CO, DEMANT.CO |

### C. Classification: where does it fit?

| Dimension | Same-month seasonality |
|---|---|
| Series family | **Calendar & seasonality** |
| Academic style | Return seasonality (cross-sectional) |
| Signal | Price only (daily total returns) |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other each month |
| Horizon and turnover | One month; about 80% of each leg replaced every month |
| Market exposure | L/S beta -0.13 to 0.05 |
| Payoff shape | Treynor–Mazuy γ -0.54 to 2.42 (t -0.7 to 3.3); worst 10% of market months -1.9% to +0.8% a month, best 10% -1.9% to +1.8% |
| Nearest factor theme | investment (4 of 6 universes), HML (2 of 6 universes) |
| Nearest library signals (returns) | Size (4 universes), 55-day breakout (4 universes), Last month return (3 universes) |
| Economic rationale | Heston & Sadka (2008): not explained by earnings announcements, dividends, size or industry; Keloharju et al. (2016): seasonal variation in risk premia. |
| Publication | Heston & Sadka 2008; Keloharju, Linnainmaa & Nyberg 2016 |
| Where it fits | Low correlation with the other library signals (0.16 or less on average; up to 0.33 with Size in single universes; nominally the momentum cluster). What is left after its neighbours is a negative return, not an edge. |

![Classification map](../figures/battery_map.png)

### D. 360° view

The signal among the 19 price signals of the shared library (`code/library.py`), on the same universes and months (equal-weighted top minus bottom quantile, gross). Its natural mirror here is **Momentum 12-1**.

| Signal (top minus bottom, raw sign) | Cluster | Likeness: stocks | Likeness: returns | Raw L/S, avg of 6 | CAPM alpha range | Universes alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Same-month seasonality **(this strategy)** | seasonality | +1.00 | +1.00 | -2.3% | -9.4% to +5.6% | 0 / 1 |
| 55-day breakout | momentum | +0.01 | +0.16 | +1.8% | +4.8% to +13.9% | 5 / 0 |
| Last month return | short-term reversal | +0.01 | +0.16 | +2.1% | -3.3% to +11.6% | 2 / 0 |
| MIN5 | low risk | -0.04 | +0.14 | -1.0% | +2.5% to +13.7% | 3 / 0 |
| Momentum 12-1 (mirror) | momentum | +0.12 | +0.13 | +6.9% | +5.9% to +20.1% | 5 / 0 |
| Near 52-week high | momentum | +0.01 | +0.13 | +4.1% | +9.9% to +22.5% | 6 / 0 |
| Volatility (252 days) | low risk | +0.08 | -0.12 | +2.0% | -12.1% to -6.3% | 0 / 3 |
| Net tail (MAX+MIN) | tail direction | +0.00 | +0.12 | -1.2% | -5.9% to +5.5% | 0 / 0 |
| MIN (worst day) | low risk | -0.03 | +0.12 | -0.8% | +3.4% to +11.2% | 3 / 0 |
| Volatility | low risk | +0.05 | -0.11 | +0.9% | -13.8% to -7.9% | 0 / 5 |
| Idiosyncratic vol | low risk | +0.03 | -0.11 | -3.3% | -15.3% to -4.8% | 0 / 4 |
| Beta | low risk | +0.10 | -0.10 | +4.4% | -12.7% to -4.2% | 0 / 3 |
| Size | size | +0.09 | +0.10 | +1.0% | -1.3% to +9.9% | 3 / 0 |
| Range (MAX−MIN) | low risk | +0.04 | -0.09 | -0.3% | -14.9% to -4.7% | 0 / 3 |
| MAX5 | low risk | +0.05 | -0.08 | +1.1% | -10.2% to -3.5% | 0 / 2 |
| Residual momentum | momentum | +0.01 | -0.04 | +6.8% | +8.7% to +12.2% | 6 / 0 |
| Skewness | tail direction | +0.00 | +0.04 | -0.4% | -6.1% to +3.9% | 0 / 1 |
| MAX (best day) | low risk | +0.04 | -0.03 | +0.4% | -13.8% to -2.0% | 0 / 2 |
| Above 52-week low | momentum | +0.06 | -0.01 | +7.7% | +5.6% to +14.5% | 4 / 0 |

![360 map](../figures/xs_FS06_map.png)

**Spanning.** Regressing the L/S on its five closest library neighbours (by return correlation) and the market:

| Universe | Alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 |
|---|---|---|---|---|
| US | -7.0% | -2.27 | 0.09 |  |
| EU | -7.7% | -2.06 | 0.13 | Size +0.26 (+3.0) |
| UK | +3.0% | 0.73 | 0.11 | Size -0.27 (-3.3) |
| DK | -8.2% | -2.05 | 0.03 |  |
| SCANDI | -2.4% | -0.52 | 0.04 |  |
| World | +0.5% | 0.22 | 0.16 | Size +0.42 (+3.3), Near 52-week high -0.23 (-2.2) |

![Double sort](../figures/xs_FS06_dsort.png)

Holding Momentum 12-1 fixed (down a column), moving from low to high Same-month seasonality changes the return by -0.2, -1.5 and -0.9 points a year; holding Same-month seasonality fixed (along a row), moving from low to high Momentum 12-1 changes it by +4.5, +3.2 and +3.8.
**Market direction.** Top-minus-bottom return in rising vs falling market months (six-universe average): -3% vs -1% a year. **Horizon:** the gross spread at 1, 2, 3 and 6 months after formation averages -2.3%, -1.9%, +0.7%, -0.9% a year.

The full library, with the CAPM alpha of every signal in every universe:

![Library alpha grid](../figures/lib_alpha.png)

## Revision history

- **9 October 2026 (version 3, stress test).** Re-run on the total-return-corrected European panels that became the default on 5 October 2026 (`DataCockpit/TOTAL_RETURN_CHECK_2026-10-05.md`); the monthly panels were rebuilt from daily data for all six universes (the US source data did not change). L/S net t against 3 October: US −2.83 → -2.88, EU −2.99 → -2.89, UK +0.70 → +0.34 (return +3.0% → +1.4%), DK −3.40 → -3.40, SCANDI −2.04 → -2.06, World −1.15 → -1.49. Long-only alpha t: US −3.17 → −3.23, EU −2.95 → −2.89. Positive passes unchanged (0 of 12); significantly negative cells 4 → 5, because US L/S crosses the gate by 0.01 (it would not under the Student-t gate of 2.91). Fix ladder: X2's holdout change is now +0.20 (p 0.029), still not past 0.0020. Sections 3 and 4 had not been refreshed on 3 October; they are now, with the caveat in the §3 note. Added: the before/after-cost table, the sensitivity checks (§8.1), the 1998–2013 evidence, caveats 6–10. Old results: `results/_archive_2026-10-03_FS06/`.
- **3 October 2026.** European panels passed through the vendor-glitch filter; three series dropped (TIFS.L, WTAN.L, SCV-B.ST). `planning/RECHECK_2026-10-03_EODHD_CLEAN.md`.
- **2 October 2026.** US universe = actual S&P 500 members at each month-end (before: the 500 largest of every company ever in the index 2012–2026). UK and EU panels include members that stopped trading (coverage UK 71% → 92%, EU 81% → 89%). Pre-registered US 1999–2012 test run: L/S t +1.16, long-only alpha t +0.61; the 2013–2026 US loss did not repeat. `FACTSHEETS_RERUN_2026-10-02.md`, `PREREG_US_1999_2012.md`.

*Not investment advice. The current book in appendix B is shown to document the method, not as a recommendation.*
