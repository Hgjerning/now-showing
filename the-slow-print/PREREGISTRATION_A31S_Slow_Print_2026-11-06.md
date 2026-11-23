# Pre-registration: A31-S "Slow Print": can the small-cap machine signal be traded slowly enough? (2026-11-06)

**SIGNED by Henrik Gjerning in chat, 6 November 2026 18:53 Copenhagen ("ok i will sign"), before any slow variant was computed. Nothing below has been run.** Part 2 of the combined *Minority Report* (Now Showing No. 8,
24 Nov 2026; this study is planned as No. 8½, 1 Dec 2026).

## 0. Why
A31 (signed 6 Oct 2026) found the A06 machine-learning ensemble earns **+15.4% a year before costs in US small caps
(2004–2026, NW t 2.82)** but turns over **179% of capital a month**; at 0.50% one-way that leaves **+4.7% net (t 0.86):
fail.** The signal is there; the trading kills it. This study asks one question: do three standard ways of trading more
slowly keep enough of the signal to leave a positive net return? Every number from A31 above is known; no result of any
slower variant has been computed or looked at.

## 1. Held fixed (A31 U1 exactly)
Universe U1 (US ranks 1,001–3,000, point in time), the 12 features, eight models, hyperparameters, expanding walk-forward
retrained each January, ensemble = mean of the eight within-month prediction ranks, out-of-sample formation months
2004-01 → 2026-07, cost 0.50% one-way on the traded weight of both legs after drift, momentum as the benchmark.
**Integrity check before anything else:** A31's walk-forward is re-run with its own code to regenerate the per-stock
ensemble scores (the A31 run did not keep them). The base book rebuilt from them must reproduce A31's saved monthly
gross and net series (`results/U1/gross_monthly.csv`, `net_monthly.csv`) to within 1e-10 per month. The rebuild uses the panels A31 ran on (`pit/USS98_pit_adjclose_pre20261008.parquet`,
`pit/USS_pit_adjclose_pre20261008.parquet` and the same-dated traded-value panels), not the panels refreshed since.
If it does not reproduce, stop and report; no slow variant is computed.

## 1b. Costs that decide the trials: the ART live-fill model (decided 6 Nov 2026, Henrik)
Every trial is judged net of the cost model fitted on ART's 65,920 live fills (2009–13), the same model as FS32
Amendment 1, applied stock by stock and month by month:
  cost (bp, one-way) = 6.2 + 8.9 × sqrt(participation %, capped at 50) + 36.5 × illiquidity + 1.5 (fees),
  participation = traded value / 63-day average traded value in USD, at a book of DKK 10m (USD at month-end FX);
  illiquidity = (100 − rank) / 100, rank = percentile of 63-day average traded value in USD pooled across US, EU and UK
  stocks that month (FS32 definition; for US-only months before EU/UK data exist, the US ranks 1–3,000).
Traded weight per stock is the same drift-aware change of weight as A31; the month's cost is the sum over stocks of
|weight change| × that stock's cost. Known before signing: the ART fit gives about 0.37–0.40% one-way for typical
US ranks 1,001–3,000 at this book size; A31's flat 0.50% leaves the base ensemble at +4.7% a year net (2004–2026), a
flat 0.40% at about +6.8%. No slow variant has been computed under any cost.
Reported alongside, not gated: flat 0.50% (A31's signed rate), flat 0.40% (costs.py us_small tier), the ART model at
half and double, and book sizes DKK 1m and 100m.
**The base ensemble under the ART model is also reported (not a trial): A31's verdict at 0.50% is not revisited.**

## 2. The three slow variants (settings fixed now; no tuning)
Each starts from the same monthly ensemble scores and is long the chosen long names and short the chosen short names,
equal weight within each leg, one-month holding, costs by the ART model in §1b.
- **S1 Partial trading.** Each month the book moves halfway from its drifted current weights to A31's decile target:
  w_t = w_drift + 0.5 × (target_t − w_drift). (An exponential average of the target book.)
- **S2 Buffer.** A stock enters the long leg when its score is in the top 10%, and stays until it falls out of the top
  30%; the short leg mirrors this (enter bottom 10%, leave above the bottom 30%). Delisted or missing names leave.
- **S3 Smoothed signal.** Score = mean of the stock's ensemble rank this month and the two months before (fewer if fewer
  exist); then A31's plain top-minus-bottom decile book.

## 3. Trials (three; Holm across them at 5%, one-sided)
| trial | hypothesis | statistic |
|---|---|---|
| **S-1** | S1's net long-short return (ART costs) is positive | mean monthly net, Newey-West t (3 lags) |
| **S-2** | S2's net long-short return (ART costs) is positive | same |
| **S-3** | S3's net long-short return (ART costs) is positive | same |
Added to `FACTSHEET_TRIAL_LEDGER.md`/`TRIAL_LEDGER.md` before the run.

## 4. Reported, not gated (decided now, reported whatever they show)
- For each variant: gross and net return, Sharpe, turnover, **alpha kept** (gross_variant / gross_base) against
  **turnover kept**, break-even cost, both halves, 2017–2026 sub-period (A06's window).
- The difference variant − base (net), NW t.
- **Alpha decay curve:** rank IC of month-t scores against returns in months t+1 … t+6.
- Grids: S1 at 25%, 50%, 75% (Henrik's idea); S2 with exit at top/bottom 20% and 40%; S3 over 2 and 6 months.
  Grids are descriptive only; the gated settings are the ones in §2.
- Cost sensitivity: see §1b.
- The same three treatments applied to the momentum benchmark.
- U3 (European small and mid caps) with the same settings when A31-U3 runs (deadline 31 Dec 2026).

## 5. Priors, stated now
S-1 pass 35%; S-2 pass 40%; S-3 pass 30% (raised by 5 points each from the first draft when the ART cost model,
about 0.40% instead of 0.50%, was chosen on 6 Nov). Most likely outcome: turnover halves, gross falls by a quarter to
a half, net moves to about +7–9% a year with t around 1.5–2 — "better, borderline". A pass would need the signal to
decay slowly (rank IC at month 3 at least half of month 1).

## 6. What will not be done
No other slowing methods, settings or universes are added to the gate after the run. No retraining on a slower target
in this study (that would be a new study). A fail is reported as a fail, in Part 2 on 1 Dec.

Signature: Henrik Gjerning ("ok i will sign", in the Claude session)   Date: 2026-11-06 18:53 Europe/Copenhagen
