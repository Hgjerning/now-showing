# A07 trial ledger

Programme total before: 27 run.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| A07-1 | 2026-09-25 | Altman Z crash AUC > 0.5 | `PREREGISTRATION_A07_2026-09-25.md` | **failed**: mean per-date AUC 0.536 [0.481, 0.597], p 0.118. Prediction (pass) was wrong. |
| A07-2 | 2026-09-25 | Ohlson O AUC beats trailing volatility | `PREREGISTRATION_A07_2026-09-25.md` | **failed, decisively**: AUC(O) 0.480 vs AUC(volatility) 0.772; volatility wins on all 49 dates with a crash (96% was a share of all 51 dates, two of which have no AUC; corrected 23 Oct 2026). Prediction (fail) held. |
| A07-3 | 2026-09-25 | Safe minus distressed quintile > 0 | `PREREGISTRATION_A07_2026-09-25.md` | **failed**: safe minus distressed -1.2% a year, NW t -0.55. Prediction (fail) held. |

**Programme total: 30 run, 1 registered (C31-3).**


## Universe correction re-run, 2026-10-01 (not a new trial)

On the point-in-time S&P 500: **A07-1 would pass** -- Altman Z crash AUC 0.536 (p 0.118) -> 0.598 [0.541, 0.659], p 0.0006, below the 0.0167 gate. The record keeps the pre-registered verdict (failed) and the article must say plainly that the corrected universe reverses it. A07-2 unchanged in substance (AUC O 0.527 vs volatility 0.791; volatility wins on all 50 dates with a crash). A07-3 still fails (-2.1% a year, t -0.92). Crash base rate 7.9% -> 8.7%: the corrected universe keeps smaller members that later fell out of the index, which the ever-member top 500 had dropped.

Same code, seeds and specification; only the universe changed (`lib10/panel.py`, `P10_UNIVERSE=sp500_pit`; membership from
Sharadar's S&P 500 add/remove history). A re-run with the published rule on today's data files reproduces the published
numbers (`results_rerun_top500/`). Files: `results_pit/`, `rerun_comparison.csv`. The pre-registration named this bias in
advance, so this is a correction of the test setup, not a new test.

## Revisited trials (signed 2026-10-08, `PREREGISTRATION_A07_R_2026-10-08.md`, sha256 68a301df189cd7cd…)

Entered at signing, before the run. These do not change any earlier trial. Family-wide gate across the six revisited trials (C31-4/5, A07-4/5, A10-3/4): 0.0083, reported alongside.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| A07-4 | 2026-10-08 | Out-of-sample crash AUC: volatility + Z + O + F beats volatility alone (point-in-time S&P 500); bootstrap p < 0.025 | `PREREGISTRATION_A07_R_2026-10-08.md` | **failed.** Out-of-sample AUC, volatility + Z + O + F 0.762 vs volatility alone 0.783; difference −0.021 [−0.039, +0.001], p 0.98, 39 test dates (2015-09 – 2025-06), point-in-time S&P 500. Prediction (fail) held; adding the accounts did not improve the ranking out of sample (the point estimate was slightly lower; the interval includes zero). |
| A07-5 | 2026-10-08 | Out-of-sample crash AUC: volatility + Z beats volatility alone; bootstrap p < 0.025 | `PREREGISTRATION_A07_R_2026-10-08.md` | **failed.** Volatility + Z 0.771 vs 0.783; −0.012, p 0.91. Prediction (fail) held. Reported: pooled in-sample logit with date effects, two-way clustered: vol z 13.0, Z +0.30 (z 2.9), O −0.12 (z −1.9), F +0.08 (z 1.4). Same sign at 30% and 50% crash thresholds and on the published universe (−0.032 / −0.017). Altman without MVE/TL: AUC 0.603 vs 0.597 (the signal is not the market term). `results_a07r/`. |

Clarification 1 (2026-10-08, before any computation): complete-case sample, logit fallback rule, AUC dates rule; see prereg.

Revisited family (6 trials, 2026-10-08): 6 run, 2 pass (C31-4 p 0.0002 and A10-3 p 0.002, both below the family gate 0.0083). A07 harness note: the run used `run_distress.py` with the `/home/claude/lib10` path insert removed, because it shadowed the point-in-time library; the corrected run reproduced the 2026-10-01 numbers (A07-1 AUC 0.598) before A07-4/5 were run.

## Verdict of record changed, 2026-10-23 (Henrik's decision; `../SEASON1_RERUN_SCOPE_2026-10-01.md`, amendment of 23 Oct)

From 23 Oct 2026 the corrected point-in-time list is the verdict of record for Season 1. Decided after the corrected
numbers were known. For A07: **A07-1 passes on the record** (AUC 0.598 [0.541, 0.659], p 0.0006 < 0.0167); A07-2 and A07-3
fail; A07 = 1 of 3 on the record, 0 of 3 as registered. Follow-ups A07-4/5: 0 of 2 (already run on the corrected list).
The article states both counts and that the switch came after the numbers were seen. No new trial; programme count unchanged.
