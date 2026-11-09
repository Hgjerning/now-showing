# Pre-registration: A07 revisited: does the balance sheet add anything to the price chart? (2026-10-08)

**SIGNED by Henrik Gjerning, 8 October 2026, before any number in it was computed.** The ledger rows were entered at signing, before the run. Follows
`PREREGISTRATION_A07_2026-09-25.md` and the v2 article. It does not change A07-1, A07-2 or A07-3.

## 0. Why, and what is already known

A07 showed that trailing volatility ranks next-year crashes far better than any accounting score:

- **Volatility:** AUC 0.79 on the corrected universe.
- **Altman Z:** 0.60.
- **Ohlson O:** 0.53.

It did not test whether the accounts add anything **on top of** volatility. The critique (ver2/ver3)
called this the missing analysis, and v2 lists it as the most valuable next step.

**What is seen:** the single-score AUCs above, by date and by year.

**What is not seen:** any model that combines the scores, and any correlation between them and
volatility.

## 1. Data, universe, outcome (fixed, as A07 unless stated)

- **Inputs.** Sharadar fundamentals and prices, with scores and crash definition exactly as in A07 §2–3:
  - Altman Z, Ohlson O (model 1), Piotroski F, and trailing 252-day volatility;
  - crash = 12-month low ≤ 60% of the formation close.
- **Primary universe:** the point-in-time S&P 500 (`P10_UNIVERSE=sp500_pit`), excluding firms without
  a classified balance sheet. Why: after the 2026-10-01 correction this is the universe the
  programme treats as right. The published ever-member top-500 universe is reported alongside.
- **Formation dates:** quarter-ends 2012-12 to 2025-06 (51).

## 2. Method (out of sample by construction)

- **Transform.** At each formation date, each score is turned into a within-date percentile rank
  (0–1), sign-aligned so that higher means more distressed. The sample is observations with all four
  scores present. Both models in a comparison use the same observations.
- **Training window.** For test date t, the training set is every observation from formation dates
  s with s ≤ t − 4 quarters, whose 12-month outcome was known at t. The window expands.
- **Test dates.** The first test date needs at least 8 training dates, so test dates run
  2015-09 to 2025-06 (40 dates).
- **Models.** Two unpenalised logits are fitted on the training set and scored on date t:
  - **V:** crash ~ vol;
  - **V+A:** crash ~ vol + Z + O + F.
- **Statistic.** Per-date AUC of each model on date t. Dates with no crash are skipped, as in A07.

## 3. Trials (two; Bonferroni 2 → one-sided gate p < 0.025 each)

| trial | hypothesis | statistic | gate |
|---|---|---|---|
| **A07-4** | Accounting scores add to volatility | mean over test dates of AUC(V+A) − AUC(V) > 0 | moving-block bootstrap over test dates (block 4, 10,000 draws, seed 42), one-sided p < 0.025 |
| **A07-5** | Altman Z alone adds to volatility | mean over test dates of AUC(V+Z) − AUC(V) > 0 | same |

**Reported, not gated:**

- **Other model pairs:** AUC(V+O) − AUC(V) and AUC(V+F) − AUC(V).
- **Pooled in-sample logit** on all 51 dates, standardised scores, date fixed effects. Coefficients
  with standard errors clustered by firm and date.
- **Crash thresholds:** both trials with 30% and 50% crash thresholds.
- **ROC curves** for the four single scores (corrected universe).
- **Crash rate by volatility decile.**
- **Altman without MVE/TL.** Altman Z without its market term (MVE/TL), to see whether Altman's
  signal is the market-value part.
- **Published universe:** all of the above on the published top-500 universe.

## 4. Known weaknesses (stated now)

- **Overlapping outcomes.** Quarterly formation dates with 12-month outcomes overlap. The block
  bootstrap (block 4 = one year) is meant to handle this.
- **Clustered crashes.** Crashes cluster in time (about 30% of A07's crashes are on 2019 dates).
  A few dates carry much of the weight.
- **Limited universe.** Large caps only. The accounting scores were built for a broader universe,
  where they may add more.

## 5. My expected outcomes (to be scored)

- **A07-4: fail (pass about 25%).** Expected AUC gain +0.005 to +0.02. Accounting signals are partly
  in the price already. A logit with four inputs fitted on few crashes also pays an estimation cost
  out of sample.
- **A07-5: fail (pass about 20%).** Altman's market term (MVE/TL) overlaps with volatility.
- **Reported:** in the pooled logit, Z will keep a significant coefficient next to volatility. O and
  F will not.

Henrik's expectation: not stated.

## 6. Ledger rows (entered in `TRIAL_LEDGER.md` at signing, before the run)

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| A07-4 | 2026-10-08 (signed …) | Out-of-sample crash AUC: volatility + Z + O + F beats volatility alone (point-in-time S&P 500) | `PREREGISTRATION_A07_R_2026-10-08.md` | *registered* |
| A07-5 | 2026-10-08 (signed …) | Out-of-sample crash AUC: volatility + Z beats volatility alone | same | *registered* |

Family-wide gate across the three revisited pre-registrations (six trials): 0.0083, reported.

**Signed:** Henrik Gjerning, 2026-10-08. The sha256 of this file is recorded in `TRIAL_LEDGER.md`.

## Clarification 1 (2026-10-08, written after signing and before any computation)

1. **Scores and sample.** Scores, volatility and crash flags come from the A07 code (`run_distress.py`,
   unchanged), run with `P10_UNIVERSE=sp500_pit`. The primary sample is observations with Z, O, F, vol
   and a crash flag all present. Piotroski F needs prior-year data, so it is the binding constraint.
2. **Logits.** The logits are unpenalised maximum likelihood (statsmodels). If a fit fails (separation
   or no convergence), it falls back to sklearn `LogisticRegression(C=1e6)` and the fallback is
   logged. Percentile ranks are computed within each date on the common sample.
3. **AUC.** A test date's AUC is computed only if it has at least one crash and one non-crash. The
   bootstrap is over test dates in calendar order.
