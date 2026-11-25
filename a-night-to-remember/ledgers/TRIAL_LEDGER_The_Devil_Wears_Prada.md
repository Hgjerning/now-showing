# A62 The Devil Wears Prada: trial ledger

Pre-registration: `results/PREREGISTRATION_TH1_THEME_CYCLES.md` (TH-1; original in `Research/themes/`), signed by Henrik in chat
on 27 Oct 2026 ("th-1 signed") before any theme return was computed. Run once on 27 Oct 2026 (`Research/themes/th1_run.py`).
Holm over two trials at 5% (first gate 0.025); circular block bootstrap of formation months (blocks 24 / 12, 10,000 draws,
seed 20261027). Added to the article ledgers on 28 Oct 2026: the pre-registration's §6 asked for a TRIAL_LOG row before the
run, and none was found; the trials are entered here so the programme gate counts them.

| Trial | Hypothesis | Horizon | Mean excess | Bootstrap SE | p | Verdict |
|---|---|---|---:|---:|---:|---|
| A62-1 | TH-1 H1: after a HOT month the theme trails the developed-market index | 24 months | −4.4% | 5.5% | 0.2076 | fail |
| A62-2 | TH-1 H2: after a RISING month the theme beats the developed-market index | 12 months | −4.1% | 2.2% | 0.98 | fail |

**0 of 2 passed.** Registered predictions (Claude): H1 40%, H2 25%. Reported, not gated: 12/24/36-month horizons, by theme,
Ben-David et al. (2023) first-60-month replication (36 ETFs, mean −5.1 points, t −0.4), today's signal (Sep 2026: AI, space,
defence HOT). Attention description extended on 28 Oct 2026 with the NYT 1980-1997 backfill and an environment_1990s word list;
these are description only and do not touch the trials (frozen input `v2_2026-10-27_rebuilt`).

**28 October 2026, stress test (passed after fixes; `STRESS_TEST_2026-10-28.md`).** No verdict changed. Reported, not gated:
per HOT month 60% trailed the index (median 24-month excess −7.9%); without cannabis the H1 mean is +2.1%; the RISING
shortfall is about 1.9 standard errors from zero in the unregistered direction (a lead, not a finding). Tested formation
months: H1 Apr 2005–Aug 2024, H2 Oct 2002–Aug 2025.
