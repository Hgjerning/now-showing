> **Note added 14 October 2026, not part of the signed text below.** The articles were renumbered to match the Now Showing feature numbers. This pre-registration keeps the codes it was signed with: A08 is now A03 (trial IDs follow, e.g. A08-1 is now A03-1). Full map: `Articles/RENUMBERING_2026-10-14.md`.

# Pre-registration: A08 "The Magnificent Seven": does concentration come back to bite? (2026-09-25)

**Written before any number below was computed.**

## 1. Data (fixed)

- Monthly market cap estimate per ticker. It is the latest Sharadar `marketcap` filed on or before
  the month-end, scaled by the split-adjusted price change since that filing. Point-in-time S&P
  master universe, 2012-01 → 2026-08. Top 500 by this estimate each month.
- Price returns only (no dividends). This slightly understates the returns of large, high-dividend
  names.

## 2. Measures

- **Concentration C(t):** the top-10 share of the top-500 total market cap.
- **Top-10 portfolio:** the ten largest at t, cap-weighted, held 12 months. **Rest:** the other 490,
  cap-weighted.

## 3. Trials (two; one-sided gate p < 0.025)

| trial | hypothesis | statistic |
|---|---|---|
| **A08-1** | "Top dog": the ten largest underperform the rest over the next 12 months | mean overlapping 12m spread (top-10 − rest) < 0; NW t (12 lags) |
| **A08-2** | Rising concentration predicts a catch-up by the average stock | slope of next-12m (EW − CW) on the prior 12m change in C(t) > 0; NW t (12 lags) |

**Reported:** Bessembinder (2018)-style dollar wealth creation (share from the top 10 / top 2% of
names); top-10 membership turnover; C(t) now vs 2012; stationary-bootstrap check of both trials.

## 4. Expected outcomes, stated before running

- **A08-1: fail (about 15% pass).** 2012–2026 is the decade in which the giants kept winning.
  I expect the sign to be the opposite of the lore.
- **A08-2: fail (about 20%).** About 14 non-overlapping years is too little to detect this.

## 5. Ledger

Two trials. Programme total before: 30. After: 32.
