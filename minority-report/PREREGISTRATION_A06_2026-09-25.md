# Pre-registration: A06 "Minority Report": can machine-learning precogs see next month's winners? (2026-09-25)

**Written before any number below was computed.** Eight standard machine-learning models, one
old rule (12-1 momentum), the same features and the same stocks. Every model's hyperparameters
are fixed below. There is no tuning, so there are no hidden trials.

## 1. Data and universe (fixed)

- Prices: Sharadar-based point-in-time S&P master universe, daily split-adjusted closes,
  2012-01-03 → 2026-09-18, 803 tickers including delisted names (Project1 cache). Price returns only.
- Fundamentals: Sharadar ARQ (as-reported quarterly), used only from its filing `date` onward.
- **Universe at each month-end t:** the 500 largest tickers by estimated market cap. The estimate is
  the latest Sharadar `marketcap` filed on or before t, scaled by the price change since that
  filing date. A ticker also needs a valid price at t.
- Known bias (stated now): the master list holds every name that was *ever* in the S&P 500
  between 2012 and 2026. Later additions are present before they joined, which tilts the list
  toward winners. The top-500 filter reduces this bias but does not remove it. It affects all
  models equally, so it matters less for the comparison between models than for the absolute
  levels.

## 2. Features (12, each rank-scaled to [-0.5, 0.5] within the month; missing → 0)

Price: 1-month return; 3-month return; 12-1 momentum; 60-day volatility; maximum daily return in
the month; price / 252-day high; 252-day beta against the equal-weighted universe.
Fundamentals (last filing ≤ t): log size; book/market; TTM earnings/price; TTM gross profit/assets;
year-on-year asset growth.

**Target (training only):** next-month return, cross-sectionally ranked.

## 3. Walk-forward

Features start in 2013-01. The first model is trained on 2013-01 → 2016-12 formation months and
predicts 2017. Each January the model is retrained on all months whose targets are known
(expanding window). Out-of-sample formation months run 2017-01 → 2026-07, with the last target
month August 2026.

## 4. Models (hyperparameters fixed now, scikit-learn 1.8)

OLS; Ridge (α 10); Lasso (α 1e-4); ElasticNet (α 1e-4, l1 0.5); Random forest (300 trees, depth 6,
min leaf 200, max_features 0.5); Gradient boosting (HistGradientBoosting, 200 iterations, lr 0.05,
depth 3, min leaf 200); MLP (32-16, ReLU, α 1e-3, early stopping, average of 3 seeds); kNN (k = 500).
**Ensemble** = the average of the eight models' within-month prediction ranks.
**Benchmark** = sorting on 12-1 momentum alone (Jegadeesh & Titman 1993).

Portfolio: equal-weighted top decile minus bottom decile (about 50 stocks per side), held one month.

## 5. Trials (three; one-sided gate p < 0.0167 = 0.05/3)

| trial | hypothesis | statistic |
|---|---|---|
| **A06-1** | The ensemble's long-short earns a positive return | mean monthly L/S, Newey-West t (3 lags) |
| **A06-2** | The ensemble beats momentum | mean of (ensemble L/S − momentum L/S), NW t (3 lags) |
| **A06-3** | The best of the nine (eight models + momentum), picked after the fact, survives the selection | deflated Sharpe ratio (Bailey & López de Prado 2014), N = 9 trials, > 0.9833 |

**Reported, not gated:** each model's Sharpe, IC, turnover; placebo (Ridge and gradient boosting
retrained on month-shuffled targets, 50 runs each); Sharpe by sub-period.

## 6. Expected outcomes, stated before running

- **A06-1: fail (about 35% pass).** These are large caps after 2017, and most of the published ML
  gains come from small, illiquid stocks (Gu, Kelly & Xiu 2020; Avramov, Cheng & Metzker 2023).
- **A06-2: fail (about 20%).**
- **A06-3: fail (about 10%).**

## 7. Ledger

Three trials. Programme total before: 24 run (+1 registered, C31-3). After: 27.
