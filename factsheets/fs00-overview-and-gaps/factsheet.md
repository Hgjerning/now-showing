# FACTSHEET FS00 · Overview and gap analysis

### Twelve famous strategies, six markets, one set of rules: what we know, and what is missing

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

> **US, 1999–2012 (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time S&P
> 500 with delisted stocks, 1999–2012, a period these factsheets were not built on. 65 trials. What holds: the Turtle
> loss (FS01) and the low-volatility long-only alpha (FS04). What does not: momentum in every form (FS03, FS11, FS13c),
> and the 2013–2026 US losses for seasonality and the 52-week low. The checklist (FS20) passes in 1999–2012 only. The
> live book's US leg does not replicate (alpha t +1.10, needed 2). The trial ledger now holds 772 trials (Bonferroni |t|
> > 3.99). Pre-registration, method and every result: `PREREG_US_1999_2012.md`.



> **In one paragraph.** Twelve strategies were run with the same code on six point-in-time universes (US, EU, UK, Denmark, Scandinavia, World), 2013–2026, after costs, each with a full factsheet: P&L, trade records, drawdowns, attribution, a pre-declared fix ladder, a classification and a 360° view. Only 0 of eleven long/short books (none) earn a **positive** return that passes the 2.87 gate in at least one market; 4 (FS01, FS06, FS08, FS12) pass it with a significantly **negative** return; long-only books beat the equal-weight universe's Sharpe most often in the momentum and low-risk families. Many signals are **redundant**: once their nearest library neighbours are in the model, 4 of eleven have no alpha left. The price-only battery collapses into a few roots: **momentum** (12-1, 52-week high, residual momentum), **low risk** (volatility, beta, MAX) and, weakly, **reversal** and **size**. The biggest gaps are data (fundamentals and delisted prices outside the US), models (no multivariate test yet) and implementation (capacity outside the US). Borrow fees, financing of leverage, World in one currency, a replication check, a programme-wide trial ledger and a market-impact cost model were added on 27 September 2026 (§3.0).

## 1. All strategies in one table

| Strategy | Family | L/S net return / yr (range over 6) | L/S positive | L/S passes &#124;t&#124; > 2.87 | L/S CAPM alpha range | Long-only beats EW Sharpe | Long-only alpha passes | Fixes: holdout Sharpe | Redundant in 360° view | Library cluster |
|---|---|---|---|---|---|---|---|---|---|---|
| FS01 Turtle Traders | Breakout & trend | -16.2% to -3.5% | 0 / 6 | US−, SCANDI−, World− | -12.3% to +2.7% | 0 / 6 | — | T0 -0.62 → T3 0.50 (drop shorts, 4N stop) | yes | momentum (time series) |
| FS02 Lottery (MAX) | Lottery & attention | -10.6% to +1.9% | 1 / 6 | — | -2.5% to +8.5% | 2 / 6 | — | L0 -0.41 → L1 -0.21 (beta-neutral legs) | yes | low risk |
| FS03 Momentum | Momentum & trend | -2.1% to +9.8% | 5 / 6 | — | +2.1% to +16.7% | 5 / 6 | UK, World | 0.18 → 0.56 (full ladder) | no | momentum |
| FS04 Low volatility | Low risk | -8.7% to +1.6% | 1 / 6 | — | +2.8% to +10.9% | 6 / 6 | — | -0.14 → 0.21 (full ladder) | no | low risk |
| FS05 Monkey portfolios | Portfolio folklore | beat the index: 3–83% of monkeys | — | — | — | — | — | no fix: a benchmark | — | size (equal weight) |
| FS06 Same-month seasonality | Calendar & seasonality | -14.0% to +3.4% | 1 / 6 | EU−, DK− | -13.5% to +2.0% | 1 / 6 | — | -0.89 → -0.68 (full ladder) | no | momentum |
| FS07 Size | Size | -4.3% to +4.3% | 1 / 6 | — | -10.4% to +3.1% | 1 / 6 | UK | -0.34 → -0.37 (full ladder) | yes | low risk |
| FS08 Short-term reversal | Reversal & bottom-fishing | -12.4% to +0.7% | 1 / 6 | EU− | -15.7% to -0.7% | 0 / 6 | — | -0.87 → -0.98 (full ladder) | no | momentum |
| FS09 52-week high | Momentum & trend | -5.8% to +8.8% | 2 / 6 | — | +6.3% to +18.6% | 5 / 6 | EU, DK | 0.04 → 0.52 (full ladder) | no | momentum |
| FS10 Betting against beta | Low risk | +1.7% to +9.1% | 6 / 6 | — | +1.1% to +7.7% | 6 / 6 | UK | 0.01 → 0.06 (full ladder) | no | low risk |
| FS11 Residual momentum | Momentum & trend | +2.2% to +6.9% | 6 / 6 | — | +4.7% to +9.8% | 6 / 6 | — | 0.50 → 0.58 (full ladder) | no | momentum |
| FS12 Buy at the 52-week low | Reversal & bottom-fishing | -14.7% to -5.8% | 0 / 6 | US−, EU−, World− | -15.8% to -7.3% | 0 / 6 | — | -0.78 → -0.57 (full ladder) | yes | momentum |

*Net of costs, local currency, Feb 2013 – Aug 2026 (FS01 daily from Jan 2013). In the gate column + marks a significantly positive return, − a significantly negative one. The gate is Bonferroni over 12 cells per factsheet; fix ladders are judged on the 2020–26 holdout. Redundant = alpha |t| < 2 in every universe after the signal's closest library neighbours and the market.*

![Heatmap](../figures/fs00_heatmap.png)

![Battery map](../figures/battery_map.png)

## 2. What the twelve factsheets say together

1. **Two roots carry almost everything.** The momentum family (FS03, FS09, FS11, and the breakout inside FS01) and the low-risk family (FS02, FS04, FS10) are where the beta-adjusted alphas are. Within each family the signals are close substitutes.
2. **Raw long/short numbers mislead in a bull market.** The long/short books of FS03, FS04, FS09 carry market betas of -1.09 to -0.28 against the equal-weight universe; in a rising market that short beta alone cost 3–13% a year (beta × universe return). Beta-neutral legs remove most of this drag, but the neutralised books rarely pass the gate.
3. **Costs matter most for the fast signals.** Trading costs take 3.9–4.9% a year from short-term reversal (FS08) and 4.0–5.0% from seasonality (FS06), against 1.7–2.5% for 12-1 momentum and 1.0–1.6% for low volatility; both fast signals are negative after costs in most markets.
4. **Folklore fails where it contradicts momentum.** Buying at the 52-week low (FS12) and buying breakouts with tight stops on single stocks (FS01) both lose; the monkeys (FS05) only reflect whether small beat big.
5. **Survivorship was worth 2–5 percentage points a year** on the equal-weight universes outside the US; moving to point-in-time membership changed several conclusions (FS02).
6. **Six markets are not six tests.** The long/short books co-move strongly across universes (World contains the US; EU contains the Nordic blue chips), so the six markets are worth only 1.4–1.8 independent tests (effective number = 36 / sum of the 6×6 correlation matrix). "Positive in all six" is weaker evidence than it sounds.

| Strategy (L/S net) | Mean pairwise correlation | US–World | EU–SCANDI | Effective number of markets |
|---|---|---|---|---|
| FS03 Momentum | 0.55 | 0.89 | 0.59 | 1.6 |
| FS04 Low volatility | 0.61 | 0.92 | 0.61 | 1.5 |
| FS09 52-week high | 0.63 | 0.92 | 0.61 | 1.4 |
| FS10 Betting against beta | 0.59 | 0.90 | 0.72 | 1.5 |
| FS11 Residual momentum | 0.47 | 0.84 | 0.52 | 1.8 |
| FS12 Buy at the 52-week low | 0.48 | 0.85 | 0.63 | 1.8 |


7. **Across the whole programme, few winners survive.** The factsheet trial ledger holds 682 gated tests. Under a programme-wide Benjamini–Hochberg correction 53 positive results survive (21 also Bonferroni, |t| > 3.97) against 21 reliable losers; the best positive candidates have a deflated Sharpe ratio of 0.68 at most even on the lenient bound, below the usual 0.95 (`planning/FACTSHEET_TRIAL_LEDGER.md`).

## 3. Gap analysis

![Coverage](../figures/fs00_coverage.png)

### 3.0 Closed since the first edition (27 Sep 2026)

| Category | Gap | What was done |
|---|---|---|
| Data | No company fundamentals outside the US | Partly closed. US stock level (FS13b); outside the US at factor level (FS17): the fundamental pair (profit growth + issuance) adds to low beta and momentum in the UK, Denmark and Europe in both 2013–25 (JKP) and 1999–2013 (ART). Stock-level non-US history still needs a data source. |
| Data | No FX conversion; World sums local-currency returns | World converted to USD, unhedged, with Fed H.10 daily rates (EUR, GBP, DKK, SEK) and Yahoo PLN from 2015; the 21 Polish names stay in PLN before 2015 (`data.to_usd`). |
| Model | Programme-level multiple testing not yet consolidated | One ledger of every gated test in FS01–FS13 with programme-wide Bonferroni, Benjamini–Hochberg and deflated Sharpe (`code/ledger.py`, `planning/FACTSHEET_TRIAL_LEDGER.md`). |
| Implementation | Flat 10 bp per side; no size- or liquidity-dependent costs, no market impact | FS16: half-spread from traded value plus square-root market impact, at $1m to $10bn per book; the shortlist holds a positive Sharpe ratio to about $1bn in the US, $130m in World and $13–29m in the EU, UK and Denmark (`code/impact.py`). |
| Implementation | Short side: no borrow fees or availability in the sorts (50 bp flat in FS01 only) | Every short leg pays a size-tiered borrow fee: 0.25% a year for the largest half of the universe, 0.75% for the next 30%, 2% for the smallest 20% (`code/borrow.py`); FS01 keeps its flat 0.5%. |
| Implementation | Leverage without financing: BAB (rf = 0, no spread), vol targeting up to 3× | Net long cash in beta-neutral and BAB books is charged at the USD risk-free rate + 0.5% (`borrow.financing`). Volatility targeting scales a dollar-neutral book and is not charged for cash; its margin cost is still missing. |
| Validation | No replication check against published factor returns | FS13: our US signals correlate 0.8 or more with the matching JKP factor for 8 of 12. |
| Validation | No sector or industry neutrality | FS19 (pre-registered, passed): ranked within 11 sectors the shortlist keeps +5.3% a year (t 3.0), two thirds of its unrestricted return; UK sector coverage only 34%. |
| Validation | No stress tests of named episodes (2015–16, COVID crash and rebound, 2022 rate shock) and no crash-risk analysis for momentum | FS19: five episodes 2015–2022 for market, low beta, momentum and the FS18 overlay; the overlay stays within ±8% in every episode; low beta lost 24–29% in the US and World in the COVID crash and in 2022. Momentum-crash regression: sign as in Daniel & Moskowitz before 2013 (t −1.9), untestable after (too few bear months). |
| Validation | No unit tests of the engine (look-ahead, signal lags, cost accounting) | FS19: signals identical when rebuilt from truncated data (171 comparisons), iid-noise t-statistics behave as expected (4.2% beyond 1.96), a next-month cheat signal is caught (t > 180), cost arithmetic exact. Flag: 'beta-neutral' low beta keeps a realised beta of +0.3 to +0.6 in the US, UK, EU and World. |
| Process | Factsheet trials outside the programme ledger | All factsheet trials are now in the factsheet trial ledger; FS14 will be pre-registered there. |


### 3.1 Priority gaps still open (impact high, effort lowest first)

| Category | Gap | Impact | Effort | Remedy |
|---|---|---|---|---|
| Validation | The six universes overlap and co-move: World contains US, UK and EU; EU contains the Danish, Swedish and Finnish blue chips | High | Low | Report the effective number of markets; judge on pooled evidence; treat World as a summary, not a seventh market; run EU ex-Nordics |
| Data | Residual survivorship outside the US: 9–25% of index member-quarters have no price (mostly delisted names) | High | Medium | Buy delisted-inclusive history for Europe, or lengthen with the ART archive (1996–2013) |
| Model | Sort-based tests only; no multivariate (Fama-MacBeth) regressions | High | Medium | Monthly cross-sectional regressions on all library signals, per universe |
| Coverage | Missing factor families: value, quality, investment, earnings momentum, analyst revisions, payout, liquidity | High | Medium (US) / High (non-US) | US stock-level from Sharadar now; JKP factor-level for UK, DK, World |
| Data | Oslo missing from SCANDI; DK has ~19 names | Medium | Low | Add OBX history; report DK only as a robustness market |
| Model | Raw 252-day betas, no shrinkage | Medium | Low | Vasicek or Frazzini-Pedersen shrinkage |
| Model | No factor model for Europe or SCANDI inside JKP; French Europe used, in USD | Medium | Low | Build local-currency factor returns from the library itself |
| Model | Equal weighting and one-month holding everywhere | Medium | Low | Add value-weighted (US) and overlapping 3/6/12-month holdings |


### 3.2 Data

| Gap | Where it bites | Impact | Effort | Remedy | Source we already have |
|---|---|---|---|---|---|
| Residual survivorship outside the US: 9–25% of index member-quarters have no price (mostly delisted names) | all non-US results; short legs penalised, long legs flattered | High | Medium | Buy delisted-inclusive history for Europe, or lengthen with the ART archive (1996–2013) | ART PIT database (Project1, to 2013); none for 2013–26 |
| No shares outstanding outside the US | FS07 size and the FS05 index benchmark use traded value as a proxy | Medium | Medium | Shares-outstanding history or free-float index weights | none |
| Short history (from 2012) | FS06 seasonality averages 1–13 years (paper: 20); FS11 starts 2014; holdout only 6.7 years | Medium | Medium | Extend back with ART (1996–2013) for EU, UK, DK, US | ART PIT database |
| Oslo missing from SCANDI; DK has ~19 names | SCANDI and DK sorts use 3–5 groups of 6–12 stocks; noisy | Medium | Low | Add OBX history; report DK only as a robustness market | none |
| US prices without high/low or volume in our Sharadar extract | FS01 true-range N; US size-independent liquidity signals | Low | Low | Re-pull Sharadar SEP with OHLCV | Sharadar subscription |
| Event and positioning data not used: earnings dates, analyst revisions, short interest, options, news | 360° gaps in FS02 (news vs no-news jumps, implied skew, borrow) | Medium | Medium–High | Check coverage of the Project2 caches, start with the US | Project2 pit_short_positions, pit_options, pit_headlines, pit_13f; ART IBES (to 2013) |

### 3.3 Model

| Gap | Where it bites | Impact | Effort | Remedy | Source we already have |
|---|---|---|---|---|---|
| Sort-based tests only; no multivariate (Fama-MacBeth) regressions | overlapping signals (momentum family, low-risk family) are judged one at a time | High | Medium | Monthly cross-sectional regressions on all library signals, per universe | code/signals*.py library |
| Raw 252-day betas, no shrinkage | FS10 BAB, beta-neutral fixes, attribution | Medium | Low | Vasicek or Frazzini-Pedersen shrinkage | — |
| Residual momentum on a market-only model, 24 months | FS11 | Low | Low | Fama-French 3-factor residuals (US), 36 months when history allows | French factors (Project2 cache) |
| No factor model for Europe or SCANDI inside JKP; French Europe used, in USD | attribution alphas for EU and SCANDI | Medium | Low | Build local-currency factor returns from the library itself | library L/S returns |
| Equal weighting and one-month holding everywhere | turnover-heavy strategies (FS08, FS06); comparability with papers that value-weight or hold 6–12 months | Medium | Low | Add value-weighted (US) and overlapping 3/6/12-month holdings | — |

### 3.4 Implementation

| Gap | Where it bites | Impact | Effort | Remedy | Source we already have |
|---|---|---|---|---|---|
| No taxes, dividend withholding or currency hedging costs | Danish and cross-border investors | Medium | Medium | Investor-specific net-of-tax layer | Project1 art_measured_taxes |
| Close-to-close execution, monthly rebalance at month-end | all strategies; month-end crowding | Low | Low | Next-day VWAP proxy; staggered rebalance days | — |

### 3.5 Coverage

| Gap | Where it bites | Impact | Effort | Remedy | Source we already have |
|---|---|---|---|---|---|
| Missing factor families: value, quality, investment, earnings momentum, analyst revisions, payout, liquidity | the multifactor battery would be price-only | High | Medium (US) / High (non-US) | US stock-level from Sharadar now; JKP factor-level for UK, DK, World | Sharadar US fundamentals; JKP |

### 3.6 Validation

| Gap | Where it bites | Impact | Effort | Remedy | Source we already have |
|---|---|---|---|---|---|
| The six universes overlap and co-move: World contains US, UK and EU; EU contains the Danish, Swedish and Finnish blue chips | every 'positive in k of six' count; six markets are worth fewer than two independent tests | High | Low | Report the effective number of markets; judge on pooled evidence; treat World as a summary, not a seventh market; run EU ex-Nordics | the L/S series already on disk |
| No capacity estimate | which books survive at realistic AUM, above all DK and SCANDI | Medium | Medium | Capacity at a participation cap (e.g. 5% of daily traded value) per book | traded-value panels (PIT) |

### 3.7 Process

| Gap | Where it bites | Impact | Effort | Remedy | Source we already have |
|---|---|---|---|---|---|
| Repo assembly script does not know the factsheets | publishing | Low | Low | Add factsheets to assemble_repo.py | — |

## 4. Where the series ended up (FS13–FS19)

Steps 1–5 of the first edition's plan are done, including the remaining cheap gaps (FS16 costs, FS19 engine tests, stress episodes and sector neutrality). In short:

| Step | Result | Factsheet |
|---|---|---|
| Signal battery across all six markets | Low beta (beta-neutral) is positive in 6 of 6 markets and 12-1 momentum in 5 of 6; no price signal survives the correction on its own | FS13 |
| US fundamentals, stock level | Profit growth and debt issuance add alpha; value and investment do not | FS13b |
| Multivariate test | Residual momentum and 52-week high are redundant next to 12-1 momentum | FS13c |
| Pre-registered multifactor model | No selection rule beats equal weights (t 1.4) | FS14 |
| ART history, 1999–2013 | The shortlist holds out of sample (Sharpe 0.8); selection rules fail again | FS15 |
| Costs that grow with size | Positive to about $1bn in the US, tens of millions in Europe and the UK, never in the Nordics | FS16 |
| Fundamentals outside the US | Profit growth + issuance add to the shortlist at factor level (t 4.7) | FS17 |
| The portfolio I would run | Market + 5%-vol overlay: Sharpe +0.15–0.21 in the US, EU, UK and World at $50m per book; pooled t 1.85, not passed | FS18 |
| Robustness | Engine clean; within-sector shortlist keeps two thirds (t 3.0); "beta-neutral" low beta is not market-neutral in crashes | FS19 |

**Still open:** stock-level fundamentals outside the US (data request in `planning/DATA_REQUEST_LETTER.md`); realised-beta control for the low-beta book (shrunk betas, as in Frazzini & Pedersen); cost-model calibration to real spreads; UK sector labels for investment trusts.

## 5. Reproduce

`code/build_overview.py` reads `results/xs_*.json`, `turtle_summary.json`, `lottery_summary.json`, `fix_summary.json`, `monkey_summary.json` and the neighbourhood files.
