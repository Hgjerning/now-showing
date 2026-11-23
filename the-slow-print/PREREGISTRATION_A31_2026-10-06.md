# Pre-registration: A31 "Minority Report 2: the small print" (2026-10-06)

**SIGNED by Henrik Gjerning, 6 October 2026, before any return in these universes was computed for this study.**

**Sequel to A06 *Minority Report*.** A06 found that eight off-the-shelf machine-learning models added nothing over 12-1
momentum in 500 large US stocks, 2017–2026, and named its own limit: the published machine-learning gains are largest
in small, illiquid stocks (Gu, Kelly & Xiu 2020; Avramov, Cheng & Metzker 2023). This study takes the same models,
features and rules to the places A06 left out: US small caps over a long sample, European blue chips, and European
small and mid caps.

**Written before any return in these universes was computed for this purpose.** Coverage checks (counts of stocks and
of available features per month, no returns) are allowed before signing and will be reported. Nothing below changes
after signing; anything added later is labelled *reported, not gated*.

## 1. What is held fixed from A06 (identical code)

- **Features (12)**, rank-scaled to [-0.5, 0.5] within the month, missing → 0: 1-month return; 3-month return; 12-1
  momentum; 60-day volatility; maximum daily return in the month; price / 252-day high; 252-day beta against the
  equal-weighted universe; log size; book/market; TTM earnings/price; TTM gross profit/assets; year-on-year asset growth.
  Fundamentals are used only from their filing date (or, where a filing date is missing, period end + 120 days).
- **Target (training only):** next-month return, ranked within the month.
- **Models and hyperparameters**, exactly as A06 §4: OLS; Ridge (α 10); Lasso (α 1e-4); ElasticNet (α 1e-4, l1 0.5);
  random forest (300 trees, depth 6, min leaf 200, max_features 0.5); HistGradientBoosting (200 iterations, lr 0.05,
  depth 3, min leaf 200); MLP (32-16, α 1e-3, early stopping, mean of 3 seeds); kNN (k = 500).
  **Ensemble** = mean of the eight models' within-month prediction ranks. **Benchmark** = 12-1 momentum alone.
- **Walk-forward:** expanding window, retrained every January on all months whose targets are known.
- **Portfolio:** equal-weighted top decile minus bottom decile, held one month.
- **Costs (new in A31, decided before running): every trial is judged net of trading costs.** Each month the cost is
  the one-way rate times the traded weight of both legs (the sum of absolute weight changes, long and short, after
  drift), deducted from that month's long-short return. One-way rates: **0.50% for U1 and U3, 0.15% for U2.**
  Momentum, the benchmark, pays the same costs on its own trades. Gross results are reported alongside.

## 2. The three universes (fixed)

| | Universe at each month-end | Data | Features from | Out-of-sample formation months |
|---|---|---|---|---|
| **U1 US small caps** | ranks 1,001–3,000 by market cap, point in time (the Russell 2000 range) | Sharadar: `members_USS98` (1998–2011) joined to `members_USS` (2011–2026), daily adjusted closes, ARQ fundamentals | 1999-12 | 2004-01 → 2026-07 (first training 1999-12 → 2003-11) |
| **U2 European blue chips** | members of 11 national blue-chip indices at the date (CAC 40, DAX, AEX, IBEX 35, FTSE MIB, OMXS30, OMXC25, OMXH25, BEL 20, PSI 20, WIG 20), quarterly point-in-time membership | Season 2 EU panel (total-return fix on), EODHD fundamentals | 2013-01 | 2017-01 → 2026-07, the same window as A06 |
| **U3 European small and mid caps** | stocks on the European exchanges of the EODHD universe (incl. UK, Switzerland and the Nordics; listed and delisted), excluding each country's blue-chip index members, with market cap EUR 50m–5bn and median 60-day traded value ≥ EUR 100k at the date; at most 2,000 names, largest first | EODHD prices from 2012 and fundamentals (Project 10 Annox download) | 2013-01 | 2017-01 → 2026-07 |

Returns: U1 in USD; U2 and U3 in EUR (local prices converted at the daily ECB/EODHD rate), so that every stock in a
cross-section is measured in one currency. U3 runs only when its data pass the coverage check in §6; if they do not
by **31 December 2026**, its three trials are recorded as *not run* and do not count.

## 3. Trials (nine; one-sided Bonferroni gate p < 0.0056 = 0.05/9)

For each universe u ∈ {U1, U2, U3}:

| trial | hypothesis | statistic |
|---|---|---|
| **A31-u.1** | The ensemble's long-short earns a positive return net of costs | mean monthly net L/S, Newey-West t (3 lags) |
| **A31-u.2** | The ensemble beats 12-1 momentum net of costs | mean of (ensemble net L/S − momentum net L/S), NW t (3 lags) |
| **A31-u.3** | The best of nine (eight models + momentum) on net returns, picked after the fact, survives the selection | deflated Sharpe ratio of net returns, N = 9, > 0.9944 |

A trial passes only if it clears the gate **and** its effect has the same sign in the first and second half of the
out-of-sample months.

## 4. Reported, not gated

Each model's Sharpe, IC, hit rate and turnover; Sharpe by halves; every result gross of costs; break-even one-way
trading cost of the ensemble; U1 restricted to 2017–2026 for a like-for-like comparison with
A06; shuffled-target placebo (Ridge and gradient boosting, 20 runs each per universe); feature ablation without 12-1
momentum; simple one-characteristic sorts (value, earnings yield, profitability, low volatility, size, momentum).

## 5. Expected outcomes, stated before running

- **U1 US small caps:** A31-U1.1 pass about 35% (small caps are where the literature finds the gains, and 270 months
  give power, but a monthly decile book in small caps turns over heavily and 0.50% a side takes a large bite);
  U1.2 about 20%; U1.3 about 15%.
- **U2 European blue chips:** fail, fail, fail (about 20%, 15%, 10%): large caps again, and only about 300 names.
- **U3 European small and mid caps:** U3.1 about 25%; U3.2 about 15%; U3.3 about 10%.
- Overall: none out of nine is my central case.

## 6. Coverage check before running (no returns)

Per universe and month: number of stocks; share with each of the 12 features; for U3, also the share of the European
small/mid-cap market value covered. Minimum to run: on average 100 stocks per decile side in U1 and U3, 25 in U2, and
at least 80% coverage of each price feature and 60% of each fundamental feature.

## 7. Known biases, stated now

- U1: Sharadar ranks are computed from Sharadar's own market caps; the 1998–2011 and 2011–2026 panels are joined at
  2011-06. Small caps are costly to trade; the trials are net of a flat 0.50% one-way rate, which is a simplification (real costs vary with size and liquidity).
- U2: about 300 names, so deciles hold about 30 stocks a side; membership is quarterly.
- U3: built from an exchange screen, not an index; EODHD fundamentals have shorter and patchier histories than Sharadar.
- All: one fixed set of hyperparameters, twelve features. This tests these models as specified, not machine learning
  in general.

## 8. Ledger

Nine trials (three per universe). Article programme total before: 152 run, 1 registered (C31-3), at the end of Season 2 (the factsheet ledger is kept separately). After: 161 when all nine have run.

