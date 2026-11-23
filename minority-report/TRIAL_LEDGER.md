# A06 trial ledger

Programme total before: 24 run.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| A06-1 | 2026-09-25 | Ensemble ML long-short > 0 | `PREREGISTRATION_A06_2026-09-25.md` | **failed**: ensemble long-short +3.5% a year, Sharpe 0.21, NW t 0.72, p 0.235. Prediction (fail) held. |
| A06-2 | 2026-09-25 | Ensemble beats 12-1 momentum | `PREREGISTRATION_A06_2026-09-25.md` | **failed, wrong sign**: ensemble minus momentum -6.4% a year, NW t -0.93. Prediction (fail) held. |
| A06-3 | 2026-09-25 | Best of nine survives deflated Sharpe | `PREREGISTRATION_A06_2026-09-25.md` | **failed**: best of nine = RandomForest (Sharpe 0.47); deflated Sharpe 0.81 < 0.983. Prediction (fail) held. |

**Programme total: 27 run, 1 registered (C31-3).**

## Universe correction re-run, 2026-10-01 (not a new trial)

On the point-in-time S&P 500 (actual members at each month-end) instead of the top 500 among ever-members, every
verdict stands and every model gets worse. A06-1: ensemble long-short Sharpe 0.21 -> -0.12 (t -0.37). A06-2: ensemble
minus momentum t -0.93 -> -0.72. A06-3: the best of nine becomes plain momentum (Sharpe 0.14); deflated Sharpe 0.48.
Long-short Sharpe by model, published rule (`results/scoreboard.csv`) -> corrected: OLS 0.17 -> 0.03, Ridge 0.17 -> 0.02,
Lasso 0.24 -> -0.04, ElasticNet 0.16 -> 0.00, RandomForest 0.47 -> 0.08, GradBoost 0.22 -> -0.20, MLP 0.39 -> 0.11,
kNN 0.36 -> 0.07, momentum 0.45 -> 0.14. (Corrected 23 Oct 2026: the left-hand values previously quoted the
`results_rerun_top500/` re-run, not the published scoreboard.) The modest ML edges in the published table were mostly the survivor list.

Same code, seeds and specification; only the universe changed (`lib10/panel.py`, `P10_UNIVERSE=sp500_pit`). The re-run
with the published rule on today's data (`results_rerun_top500/`) is close to the published numbers (ensemble Sharpe 0.25
vs 0.21; small drift from the 26 Sep price-file refresh). Placebo not re-run. Files: `results_pit/`, `rerun_comparison.csv`.

**Revision 2026-10-07 (after external review):** `code/ablation.py` (corrected universe) adds a feature ablation (without 12-1 momentum; without the trend family) and six simple one-characteristic sorts. **Reported, not gated, not trials**; programme count unchanged. Ensemble Sharpe: all features -0.12, without momentum +0.06, without trend family +0.11; all inside the placebo band. Simple sorts: only momentum positive (0.14).

**Stress test 2026-10-23** (`STRESS_TEST_2026-10-23.md`): two referees; every gated statistic recomputed independently and matched on both universes. No trial added; verdicts unchanged, 0 of 3. Disclosed: gradient boosting ran with scikit-learn's default early stopping (registered: 200 iterations); turnover registered as reported but not computed.
