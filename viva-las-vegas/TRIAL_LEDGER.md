# A04 trial ledger

Programme total before: 46 run.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| A04-1 | 2026-09-25 | Low-MAX beats high-MAX post-publication (JKP US) | `PREREGISTRATION_A04_2026-09-25.md` | **failed**: +2.0% a year, NW t 0.55. Prediction (fail) held. |
| A04-2 | 2026-09-25 | Low-MAX beats high-MAX in the 500 largest | `PREREGISTRATION_A04_2026-09-25.md` | **failed, opposite sign**: low-minus-high MAX -9.2% a year (t -1.93); but Sharpe of both deciles 0.95 vs 0.96, betas 0.64 vs 1.22. Prediction (fail) held. |

**Programme total: 48 run, 1 registered (C31-3).**


## Universe correction re-run, 2026-10-01 (not a new trial)

A04-2 on the point-in-time S&P 500: low-minus-high MAX -9.2% a year (t -1.93) -> -5.9% (t -1.30); still failed, opposite sign. The equal-Sharpe finding does not survive: Sharpe D1 0.95 -> 0.92, D10 0.96 -> 0.77. Under the corrected universe the low-MAX decile has the better risk-adjusted return. A04-1 (JKP) is unaffected.

Same code, seeds and specification; only the universe changed (`lib10/panel.py`, `P10_UNIVERSE=sp500_pit`; membership from
Sharadar's S&P 500 add/remove history). A re-run with the published rule on today's data files reproduces the published
numbers (`results_rerun_top500/`). Files: `results_pit/`, `rerun_comparison.csv`. The pre-registration named this bias in
advance, so this is a correction of the test setup, not a new test.

## Review additions, 2026-10-14 (reported, not gated; no new trials)

After an external review: CAPM, Fama–French five-factor and five-factor-plus-momentum alphas for D1, D10 and D1−D10; 95% confidence intervals and minimum detectable effects for A04-1 and A04-2; up- vs down-market months and 2022; cumulative D1 vs D10 (figure 3). Code `code/reported_factor.py`, output `results_pit/reported_factor.json`, factor data from the Ken French library (`data/french_us_5f_daily.csv`, `data/french_us_mom_daily.csv`). On the corrected universe, D1−D10 alpha: CAPM +3.4% (t 0.94), FF5 +0.5% (t 0.17), FF5+Mom −1.7% (t −0.58). Verdicts unchanged. Programme count unchanged.

## Deutsche Bank additions, 2026-10-22 (reported, not gated; no new trials)

Henrik asked to answer the three questions of Deutsche Bank's "Lottery factor with new faces" (DB Quant Handbook, 10 Dec 2010, pp. 678–683) before release. Code `code/reported_db2010.py` (P10_UNIVERSE=sp500_pit), output `results_pit/reported_db2010.json`, article section 5 and figure 4. Same panel and code path as run_max.py on today's data files; the baseline D1−D10 on those files is −6.4% a year (t −1.42) against the published −5.9% (t −1.30), and every comparison in the section is made against that same-run baseline. Findings: short-term reversal −1.2% (t −0.29), correlation with the MAX spread −0.08, signal persistence 0.35 (MAX) vs −0.01 (past return); MAX quintiles −3.4% (t −0.93), within past-return quintiles −1.9% (t −0.56), within volatility quintiles −1.6% (t −1.05), residual MAX after volatility +0.2% (t 0.10); legs: D1 − EW −1.7% (t −0.91), EW − D10 −4.7% (t −1.55); rank IC of MAX 0.04%. Verdicts unchanged. Programme count unchanged.

**22 October 2026, stress test (passed after fixes; `STRESS_TEST_2026-10-22.md`).** No verdict changed. Corrections to
the notes above, which stay as written: (1) the "equal Sharpe" figures were raw-return Sharpe ratios; with returns in
excess of T-bills they are 0.82 vs 0.86 (first list) and 0.79 vs 0.67 (corrected), and neither difference is
distinguishable from zero (block-bootstrap 95% intervals include 0; `code/reported_stress.py`). (2) The hindsight bias
was named in A06's pre-registration, whose list A04 adopted, not in A04's own. (3) The original-list re-run reproduced
the published numbers on the 1 October data files; later updates move both universes by 0.2–0.4 points. The folder
`results_rerun_top500/` cited above was not kept; `results_rep/` and `results_rep2/` hold corrected-universe re-runs.

