# Pre-registration: A07 "Under Pressure": which distress score sees the crash coming? (2026-09-25)

**Written before any number below was computed.**

## 1. Data and universe (fixed)

- Sharadar ARQ fundamentals, 2009-09 → 2026-06. A filing is used only from its `date` onward.
  Flows are trailing-twelve-month (TTM) sums of four consecutive quarters.
- Daily split-adjusted prices, point-in-time S&P master universe, 2012-01 → 2026-09.
- **Formation dates:** quarter-ends 2012-12 → 2025-06 (51 dates). The universe is the top 500 by
  estimated market cap (same rule as A06). It **excludes firms without a classified balance sheet**
  (missing current assets or current liabilities), which removes most banks and insurers. Altman
  and Ohlson built their scores for industrial firms.
- The same survivorship caveat as A06 applies: the ticker list is every name ever in the S&P 500.

## 2. Scores (higher = more distressed after sign alignment)

- **Altman Z (1968):** 1.2·WC/TA + 1.4·RE/TA + 3.3·EBIT/TA + 0.6·MVE/TL + 1.0·Sales/TA (low = distressed).
- **Ohlson O (1980, model 1 coefficients):** −1.32 − 0.407·log(TA) + 6.03·TL/TA − 1.43·WC/TA +
  0.0757·CL/CA − 1.72·(TL>TA) − 2.37·NI/TA − 1.83·CFO/TL + 0.285·(NI<0 two years) − 0.521·ΔNI.
  log(TA) is not deflated. This does not change within-date rankings, and the primary statistic is
  computed within dates.
- **Piotroski F (2000):** nine binary signals (low = weak). Reported only.
- **Market benchmark:** trailing 252-day volatility of daily returns (Campbell, Hilscher & Szilagyi 2008).

## 3. Outcome

**Crash:** the lowest close in the 12 months after formation is ≤ 60% of the formation close,
i.e. a drawdown of 40% or more. If a price series ends inside the window, its available path is used.

## 4. Trials (three; one-sided gate p < 0.0167)

| trial | hypothesis | statistic |
|---|---|---|
| **A07-1** | Altman Z ranks future crashes better than chance | mean of per-date AUCs > 0.5; moving-block bootstrap over formation dates (block 4, 10,000 draws) |
| **A07-2** | Ohlson O (accounting) beats trailing volatility (market) | mean per-date AUC(O) − AUC(vol) > 0; same bootstrap |
| **A07-3** | The distress puzzle: safe firms out-earn distressed ones | lowest-O quintile minus highest-O quintile, equal-weighted, rebuilt quarterly and held 3 months; monthly returns 2013-01 → 2026-08; NW t (6 lags) > 0 |

**Reported:** Piotroski F AUC; AUC by year; crash base rate; quintile return table.

## 5. Expected outcomes, stated before running

- **A07-1: pass (about 85%).** Low Z flags leveraged and unprofitable firms.
- **A07-2: fail (about 25%).** Market prices move faster than quarterly accounts.
- **A07-3: fail (about 45%).** The puzzle is strongest in small, illiquid stocks.

## 6. Ledger

Three trials. Programme total before: 27. After: 30.
