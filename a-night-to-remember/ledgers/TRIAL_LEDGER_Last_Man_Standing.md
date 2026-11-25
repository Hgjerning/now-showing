# A58 "Last Man Standing": trial ledger

Pre-registration: `PREREGISTRATION_A58_2026-10-22.md` (signed 22 Oct 2026, 20:24 CEST). First run 22 Oct 2026, re-run the same evening after three code fixes (below) (`code/a58_run.py`)
in Claude's cloud workspace on byte-identical copies of the signed files (the 20 SHA-256 hashes were checked first; the
Linux workspace on Henrik's PC was out of disk space). Sample 1 Jul 1963 – 31 Aug 2026. Gate 0.05/5 = 0.01, one-sided.

| Trial | Hypothesis | Result | p | Verdict |
|---|---|---:|---:|---|
| A58-1 | Contestants that do best in the fall do worst in the aftermath | mean within-episode Spearman −0.65 (15 episodes, all negative) | 0.0001 | **pass** |
| A58-2 | At least one contestant beats buy-and-hold over full cycles | best: 60% stocks / 40% cash, max t 4.30 | 0.0008 (FWER, 32,768 sign patterns) | **pass, built in (see reading)** |
| A58-3 | In range-bound days, put writing + volatility target beat buy-and-hold | −0.15% a year, NW t −0.03 (539 days; 95% CI −9% to +9%) | 0.51 | fail (inconclusive) |
| A58-4a | 200-day SMA alarm flags crashes/bears before half the fall, more than chance | 6 of 15 (40%) vs 30% for shifted alarms | 0.28 | fail |
| A58-4b | Same with the 200-day EMA | 6 of 15 (40%) vs 37% | 0.51 | fail |

**2 of 5 passed.** Programme ledger after A58: 262 run (all-in 285), with A59 (3) still registered and not run.

## Reading A58-2 (stated before anything else is written)

A full cycle runs from a peak to the day buy-and-hold regains that peak, so buy-and-hold earns about zero over every
full cycle by construction (+0.1% to +1.6% here, because the regain day closes slightly above the old peak). Any contestant with market exposure below 1
therefore wins inside these windows if it is a fixed mix (timing rules and options can lose: puts won 4 of 9 cycles,
trend 5 of 15): 60% stocks / 40% cash won 15 of 15 cycles, 90% / 10% scores t 4.46 and 1.2× leverage
−4.61 (`results/a58_stress.json`); the test could hardly fail. The registered test passes, but it measures "who did best over the bad
stretches", not "who did best". Over the whole sample buy-and-hold earned 10.9% a year against 8.5% for 60% stocks / 40%
cash: the hedges won the crash cycles and paid for it in the bull markets between them. This flaw is in the design (by
Claude), not the data; the article says so and leads with the whole-sample comparison next to the registered result.

## Implementation details fixed in code, not spelled out in the pre-registration (chosen before any return was seen)

- After the fix: contestants 1, 2 and 10 drift within the month and are rebalanced monthly, with 10 bp on the turnover;
  timing contestants (5, 6, 7, 11, 12) pay 10 bp on every change in the equity weight. Not charged anything: the Cboe
  indices (3, 4; as published), the quality tilt (8; a paper long-short factor), and hence part of 9. Conventions differ
  slightly: fixed mixes pay on both legs of the rebalance, timing rules on the stock weight only; the diversified hedge
  (9), the volatility target (6) and the half-exit alarm (12) hold their weights constant day by day without a drift
  charge. The effect is under 0.05 points a year (Referee 3).
- Bond returns: DGS10 forward-filled over missing days; duration and convexity from a 10-year semi-annual par bond.
- Cboe index returns are used as published (no extra cost). PUTY/PPUT returns are matched to French trading days.
- Turbulence: Mahalanobis distance of each month's 12-industry (value-weighted) return vector from the previous 120
  months; threshold = 90th percentile of all distances to date, including the current one, with at least 120 months.
- A58-1 uses contestants 1–12 with data for the whole window (8–9 before 1985–86, up to 12 after); an episode's
  aftermath may overlap the next episode's fall. A58-2's studentised mean uses each contestant's available episodes.
- A58-3: range-bound days where both contestants 4 and 6 exist (from 1986); the first range-bound day is 30 Jan 1990.
- A58-4: an alarm counts if any alarm day falls between the peak and the day before the fall first reaches half its
  final depth; circular shifts are over the days with a valid alarm (from May 1964).
- The 2000–02 bear is classed as a crash by the registered rule: its first −15% came 15 trading days after the March 2000
  peak.
- Seeds: 58001 (A58-1), 58002 (unused, exact enumeration), 58004/58005 (A58-4a/b).

## Data notes

- Non-US price indices (reported only): the Brazilian index starts in 1995 (hyperinflation-era zero and redenominated
  prints before); the Korean index has suspect prints in late July 2026 (−11%, +18% days). Both are flagged in the article.

## Results files

`results/a58_result.json`, `a58_episodes.csv`, `a58_episode_returns.csv`, `a58_contestants_daily.csv.gz`,
`a58_regimes.csv.gz`, `a58_reported.json`, `a58_stress.json` (reported, not gated); first-run files `*_firstrun_2026-10-22.json`.

## Stress test of 22 Oct 2026: code fixes and re-run (same trials; first-run files kept)

1. **Cboe dates.** Cboe's files skip a few US trading days (PPUT 5, PUTY 3); returns were computed on Cboe's own dates
   and then matched, leaving gaps that silently dropped puts, put writing and the diversified hedge from some episode
   windows (2018 fall and cycle; 1990, 2018, 2020 aftermaths). Fixed by carrying the index level forward to French dates.
2. **Trend start.** A masking error put the trend rule in cash from Aug 1963 instead of starting it in May 1964. Fixed.
3. **Rebalancing costs.** The registered 10 bp per unit of turnover was not charged on monthly rebalancing of 1, 2 and
   10. Fixed (above).
Re-run results: A58-1 −0.649 (p 0.0001), A58-2 t 4.30 (p 0.0008), A58-3 and A58-4 unchanged. No verdict changed. First
run: `results/a58_result_firstrun_2026-10-22.json` (−0.664; t 4.51, p 0.0005). The full daily file with Cboe columns now
lives outside the article folder (`Factsheets/_data_private/a58/`). Checks added after review: `code/a58_stress_checks.py`.
