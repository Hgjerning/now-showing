# Case 31 trial ledger

Rows are added **before** the run. Same rules as Project3's `TRIAL_LEDGER.md`: every
pre-registered hypothesis that decides something is a trial, whether it passes or fails. A
re-run after fixing a harness bug is the same trial. Project3 stood at 15 trials when this
ledger opened. Related earlier trial: **P3-4**, midterm post [+1,+90] against an unconditional
placebo, +7.6% vs +2.9%, p 0.039 (suggestive, failed the 0.0083 gate).

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| C31-1 | 2026-09-25 | Midterm [+1,+90] beats the same-date window in non-midterm years (1930–2022 vs 74 control years) | `PREREGISTRATION_C31_2026-09-25.md` | **PASSED.** Midterm +7.59% vs control +1.86%, difference +5.72 pts, permutation p 0.0056 (Welch t 2.78, p 0.0039), bootstrap 95% CI [+1.7, +9.6] pts. Both halves positive: +5.4 pts (1930–74) and +6.1 pts (1978–2022). **My prediction (fail, p 0.03–0.20) was WRONG**, and for a specific reason: I expected the same-season control to be strong (+4% to +5%). It was +1.9%, weaker than the unconditional placebo (+2.9%). The November explanation does not just fail, it points the other way. **Caveats:** these are the same 24 events P3-4 had already seen. Only the control is new, so this is not out-of-sample. Across Project3 + Case 31 (17 trials), a family-wide one-sided Bonferroni gate would be 0.0029, and 0.0056 does not clear it. |
| C31-2 | 2026-09-25 | Midterm [−119,0] is weaker than the same-date window in non-midterm years | same | **failed.** Midterm +1.19% vs control +3.58%, difference −2.39 pts, permutation p 0.21. Negative in both halves (−1.9 and −2.9 pts). My prediction (fail, p > 0.10) held. |
| C31-3 | 2026-09-25 (registered) / run ~2027-03-16 | C31-1 re-run once with 2026 added (25 midterms) | same, §4 | *registered, not yet observable* |

**Spent in this ledger: 2 run, 1 registered (C31-3). Running total with Project3: 17 run.**

**Version 2 (2026-10-07), after external review:** `code/v2_checks.py` adds era-blocked permutation, NBER recession matching/exclusion, control-weakness decomposition, decay splits and rolling 26-year gaps, an international placebo (Nikkei; FTSE 100, DAX) and a dividend check (Shiller). These are **reported, not gated** and are **not trials**: none can change C31-1 or C31-2. Spent count unchanged (17 run, 1 registered). Notable: with recession-at-the-vote years left out, the gap is +3.2 pts, p 0.079.

## Revisited trials (signed 2026-10-08, `PREREGISTRATION_C31_R_2026-10-08.md`, sha256 a646210058ad8d06… of the signed text, i.e. the file up to the line before "## Clarification 1"; the full file with its clarification hashes to 3af961cce351353d…)

Entered at signing, before the run. These do not change any earlier trial. Family-wide gate across the six revisited trials (C31-4/5, A07-4/5, A12-3/4): 0.0083, reported alongside.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| C31-4 | 2026-10-08 | Midterm gap > 0 after macro controls (recession at vote, prior-year return, CAPE, inflation), 1928–2025; Freedman–Lane p < 0.025 | `PREREGISTRATION_C31_R_2026-10-08.md` | **PASSED.** Midterm coefficient +7.4 pts with controls (recession at vote, prior 250-day return, log CAPE Oct, CPI inflation Sep y/y); Freedman–Lane permutation p 0.0002 (HC3 t 3.38); 97 years (24 midterms, 73 controls; 1928 dropped, no prior-year prices before 1927-12-30). Also below the family gate 0.0083. Prediction (narrow fail) was WRONG: the controls did not absorb the gap, and the prior-year return control made it larger. Caveat: the same 24 events as C31-1, so not out of sample; the one out-of-sample test (C31-5, pre-1928) found a gap of zero. Reported: each control alone b +5.8 to +7.4; recession-in-window +7.3; interaction midterm +5.6 (t 2.35), midterm×recession +9.6 (t 1.73); decomposition full +5.9 (p 0.005), without recession years +3.5 (p 0.063), post-1945 +6.7 (p 0.002), post-2003 +2.6 (p 0.33). `results_r/summary_c31_4.json`. |
| C31-5 | 2026-10-08 | Midterm gap > 0 in the unseen pre-1928 sample (Shiller monthly, Nov→Mar, 1871–1927); permutation p < 0.025 | `PREREGISTRATION_C31_R_2026-10-08.md` | **failed.** Pre-1928 midterms (14) Nov→Mar +1.10% vs controls (43) +1.24%; gap −0.14 pts, permutation p 0.52 (Welch t −0.06). Prediction (fail) held, but the gap is not just small, it is zero. Reported: the same monthly proxy on 1928–2025 reproduces C31-1 (+5.4 pts, p 0.004; correlation 0.96 with the daily window; 71 controls because the Shiller file ends 2023-09). 9 of 14 pre-1928 midterms had a recession at the vote; excluding them: +0.3 pts (5 midterms). Pooled 1871–2025 (reported): +3.4 pts, p 0.014. `results_r/summary_c31_5.json`. |

Clarification 1 (2026-10-08, before any computation): C31-4 deferred until ie_data.xls (CAPE, CPI) is saved by Henrik (download blocked); C31-5 uses Shiller P from data/shiller_dividends.csv (sha256 7ca61a86…).

Revisited family (6 trials, 2026-10-08): 6 run, 2 pass (C31-4 p 0.0002 and A12-3 p 0.002, both below the family gate 0.0083). A07 harness note: the run used `run_distress.py` with the `/home/claude/lib10` path insert removed, because it shadowed the point-in-time library; the corrected run reproduced the 2026-10-01 numbers (A07-1 AUC 0.598) before A07-4/5 were run.

Data for C31-4 (8 Oct 2026, recorded before any computation): `data/ie_data.xls` saved by Henrik from shillerdata.com, sha256 98a54927942e842e…, last saved by Shiller's office 5 Oct 2026.

**Version 3 (2026-10-09), after the hostile-referee stress test:** `code/v3_checks.py` adds a studentized permutation p (0.0069), the Monte Carlo SE of the primary p (±0.0007), a Holm table within Case 31 (C31-4 and C31-1 survive), the four cycle positions, a drop-five-best-years comparison (+3.0 pts), a post-2003 CI and the C31-5 power. **Reported, not gated, not trials.** Running total corrected: Project3 15 + Case 31 four (C31-1, -2, -4, -5) = **19 run**, one-sided Bonferroni gate 0.0026 (the "17" above predates C31-4/5). C31-3 gets a scoring rule for the 2026 forecast in `PREREGISTRATION_C31_3_scoring_2026-10-09.md` (scores, not trials). Volatility prediction (registered 25 Sep, reported): falls more after midterms, extra fall 0.5 pts, Welch t −0.25: **not supported**.
