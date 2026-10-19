# A03 trial ledger

Programme total before: 30 run.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| A03-1 | 2026-09-25 | Top-10 underperform the rest over 12m | `PREREGISTRATION_A03_2026-09-25.md` | **failed, opposite sign**: top-10 beat the rest by +5.7% per 12 months, NW t +2.07. Prediction (fail, opposite sign) held. |
| A03-2 | 2026-09-25 | Rising concentration predicts EW catch-up | `PREREGISTRATION_A03_2026-09-25.md` | **failed**: slope +0.32, NW t 0.72, R² 0.03. Prediction (fail) held. |

**Programme total: 32 run, 1 registered (C31-3).**


## Universe correction re-run, 2026-10-01 (not a new trial)

On the point-in-time S&P 500: no change of substance. A03-1 top-10 beat the rest by +6.2% per 12 months (t 2.11; published +5.7%, t 2.07); A03-2 slope 0.43, t 0.70. Verdicts stand.

Same code, seeds and specification; only the universe changed (`lib10/panel.py`, `P10_UNIVERSE=sp500_pit`; membership from
Sharadar's S&P 500 add/remove history). A re-run with the published rule on today's data files reproduces the published
numbers (`results_rerun_top500/`). Files: `results_pit/`, `rerun_comparison.csv`. The pre-registration named this bias in
advance, so this is a correction of the test setup, not a new test.
