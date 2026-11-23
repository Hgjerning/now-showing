# A31 trial ledger

Rows are added **before** the run. Same rules as the other Project 10 ledgers: every pre-registered hypothesis that
decides something is a trial, pass or fail; a re-run after fixing a harness bug is the same trial.
Pre-registration: `PREREGISTRATION_A31_2026-10-06.md` (signed 6 October 2026). Gate: one-sided p < 0.0056 and the
same sign in both halves; all trials net of costs (0.50% one-way U1/U3, 0.15% U2).

| # | registered | hypothesis | outcome |
|---|---|---|---|
| A31-U1.1 | 2026-10-06 | US small caps: ensemble L/S net > 0 | **fail**: net +4.7%/yr, Sharpe 0.20, NW t 0.86, p 0.19, both halves positive (gross +15.4%, t 2.83; turnover 179%/month of capital, break-even cost 0.7% one-way). Prediction (35% chance of a pass) held. |
| A31-U1.2 | 2026-10-06 | US small caps: ensemble net beats momentum net | **fail**: +10.0%/yr difference, NW t 1.76, p 0.039 against a gate of 0.0056; momentum itself loses 5.3%/yr net in small caps. Prediction (20%) held. |
| A31-U1.3 | 2026-10-06 | US small caps: best of nine survives deflated Sharpe (net) | **fail**: best = Random Forest, net Sharpe 0.18, DSR 0.50 (bar 0.9944). Prediction (15%) held. |
| A31-U2.1 | 2026-10-06 | European blue chips: ensemble L/S net > 0 | **fail**: net +1.7%/yr, Sharpe 0.11, NW t 0.37, p 0.35 (gross +6.5%, t 1.48; turnover 268%/month of capital, break-even cost 0.2% one-way). Prediction (fail) held. |
| A31-U2.2 | 2026-10-06 | European blue chips: ensemble net beats momentum net | **fail**: -4.4%/yr, t -0.84 (momentum net +6.0%/yr). Prediction held. |
| A31-U2.3 | 2026-10-06 | European blue chips: best of nine survives deflated Sharpe (net) | **fail**: best = momentum, net Sharpe 0.29, DSR 0.60 (bar 0.9944). Prediction held. |
| A31-U3.1 | 2026-10-06 | European small/mid caps: ensemble L/S net > 0 | *registered; runs when data pass coverage, deadline 2026-12-31* |
| A31-U3.2 | 2026-10-06 | European small/mid caps: ensemble net beats momentum net | *registered* |
| A31-U3.3 | 2026-10-06 | European small/mid caps: best of nine survives deflated Sharpe (net) | *registered* |

Article programme total before: 152 run, 1 registered (C31-3).

**Coverage check (6 Oct 2026, before running):** U1 2,000 names a month, price features 93-100%, fundamentals 93-99%: passed. U2 about 270 names a month (Polish members absent 2012-14 for lack of PLN rates, training years only), price features 99%, fundamentals 81-85% (gross profit taken from the raw EODHD statements): passed. Run U2 on 6 Oct 2026 (3.9 minutes).

Run U1 on 6 Oct 2026 (157 minutes, 271 out-of-sample months 2004-01 to 2026-07). Six of six trials run so far fail; U3 pending (deadline 31 Dec 2026).

**Reported extension (not gated, not trials), requested 6 Oct 2026:** wider feature set (44 features in U2, 50 in U1) with three collinearity treatments, specified in REPORTED_EXTENSION_WIDE_FEATURES_2026-10-06.md before running. Adds no trials to the ledger; any positive result is a hypothesis for a separate pre-registration.
| A31-S-1 | 2026-11-06 | US small caps: slow variant 1 (partial trading 50%) net of ART live-fill costs > 0 | **fail**: net +8.0%/yr, NW t 1.49, p 0.068 against a Holm bar of 0.017 (gross +11.8%; turnover 100%/month, 56% of the base's; alpha kept 76%). 0.2 pp/yr below the base book under the same costs (+8.2%, t 1.50). Prior (35% pass) held. |
| A31-S-2 | 2026-11-06 | US small caps: slow variant 2 (buffer 10%/30%) net of ART live-fill costs > 0 | **fail**: net +6.8%/yr, NW t 1.33, p 0.092 (Holm stopped at S-1; bar 0.025) (gross +9.9%; turnover 81%/month, 45% of base; alpha kept 65%). 1.4 pp/yr below the base. Prior (40% pass) held. |
| A31-S-3 | 2026-11-06 | US small caps: slow variant 3 (3-month smoothed score) net of ART live-fill costs > 0 | **fail**: net +7.1%/yr, NW t 1.27, p 0.103 (Holm stopped at S-1; bar 0.05) (gross +11.5%; turnover 106%/month, 60% of base; alpha kept 75%). 1.1 pp/yr below the base. Prior (30% pass) held. |

Run A31-S on 8 Nov 2026 07:15 (Henrik's PC; 2.7 minutes after the checkpointed walk-forward). Integrity check passed with kNN from the Linux re-run and the Ensemble built in A31's table layout (`NOTE_A31S_IMPLEMENTATION_2026-11-07.md`, addenda of 8 Nov). Results: `_data_private/a31_runs/out_U1_slow/slow_print_results.json`. Three of three trials fail.
