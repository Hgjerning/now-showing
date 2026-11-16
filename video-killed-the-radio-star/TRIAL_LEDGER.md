# A08 trial ledger

Programme total before: 42 run.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| A08-1 | 2026-09-25 | Factor returns fall after publication (29 factors) | `PREREGISTRATION_A08_2026-09-25.md` | **PASSED**: post-publication coefficient -2.1% a year (t -2.70), a 51% decline; random-year placebo -0.6%, no placebo draw as low. Prediction (pass) held. |
| A08-2 | 2026-09-25 | Post-publication factor returns still > 0 | `PREREGISTRATION_A08_2026-09-25.md` | **PASSED**: post-publication average +2.5% a year, NW t 2.31; 90% of factors still positive. Prediction (pass) held. |

**Programme total: 44 run, 1 registered (C31-3).**

## Check after the run (25 Sep 2026, reported, not a trial)

Publication years checked against JKP's `Factor Details.xlsx` (github.com/bkelly-lab/ReplicationCrisis): 26 of 29 match.
Differences, all by paper choice or date convention: earnings/price (Basu 1977 here, JKP cite Basu 1983),
quality-minus-junk (journal 2019 here, JKP 2018 online), cash-based profitability (JKP give no citation; Ball et al. 2016).
Re-run with JKP's years (`results/pubyear_sensitivity.json`): A08-1 −2.1% a year, t −2.62; A08-2 +2.7% a year, t 2.51.
Both verdicts unchanged. No trial added.

- 2026-10-23 (stress test, no trial): reported robustness checks in results/robustness_2026-10-23.json (shuffled real years,
  2,000 draws: mean decline 1.66% a year, 3.75% of draws as low as the real 2.12%; month fixed effects: −1.44% a year,
  t −1.40). Verdicts unchanged (2 of 2); interpretation softened: part of the decline is a general slump. Programme-wide
  BH q: A08-1 0.066, A08-2 0.133 (PROGRAMME_GATE.csv). The registered run is the record (JKP factors; the 23 Oct
  point-in-time rule does not apply).
