# FACTSHEET FS19 · Robustness

### Is it a bug, a few lucky episodes, or a sector bet?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · 2013–2026, momentum crashes also 1999–2013*

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS19.md`, saved to the Factsheets folder before any FS19 number was computed; no deviations |
| A. Engine tests | truncation (look-ahead), iid-noise, cheat-timing, cost accounting, beta neutrality |
| B. Stress episodes | 2015–16 sell-off, Q4 2018, COVID crash, COVID rebound, 2022 rate shock; momentum-crash regression (Daniel & Moskowitz 2016) |
| C. Sector neutrality | low beta and 12-1 momentum ranked within 11 sectors (static Morningstar/Yahoo map); **primary test** of FS19 |
| Primary test | pooled sector-neutral shortlist (US, EU, UK, Denmark, SCANDI): NW t > 2 and at least half the unrestricted return |

> **In one paragraph.** **The engine is clean and the result is not a sector bet, but "beta-neutral" low beta is not market-neutral.** The signals are identical when rebuilt from truncated data, they earn nothing on random noise, and the cost arithmetic adds up to the last decimal. Ranked within sectors, the shortlist keeps **+5.3% a year (t 2.96)** of its unrestricted +8.0%, so the primary test is **passed**. The warning is in the crash tests. The low-beta book, scaled to beta-neutral with estimated betas, still carries a realised market beta of about +0.3 to +0.6 in the US, UK, EU and World, because low betas drift up and high betas drift down. It lost 29% in the US in the COVID crash and 24% in 2022. Momentum did the hedging. The FS18 overlay as a whole stayed within a few per cent in every episode.

## A. Engine tests

| Test | What | Result | Verdict |
|---|---|---|---|
| 1. Truncation (look-ahead) | 19 signals rebuilt from data cut at Dec 2015, 2019, 2023 (US, EU, UK): 171 comparisons | identical signal values and name counts | **pass** |
| 2. Noise | 19 signals on iid noise, 5 seeds × US, EU: 190 gross L/S t-statistics | 4.2% have |t| > 1.96 (expected 5%); max |t| 2.65 | **pass** |
| 3. Cheat (timing) | next month's return as the signal vs this month's return | next month: t ≥ 189; this month: |t| ≤ 1.9 | **pass** |
| 4. Cost accounting | gross − net = cost + borrow + financing; cost = 10 bp × 2 × turnover | largest error 3e-17 | **pass** |
| 5. Beta neutrality | realised beta of the 'beta-neutral' books on the equal-weight universe | flagged if |beta| > 0.3: US low beta (+0.48), EU 12-1 momentum (-0.33), UK low beta (+0.35), World low beta (+0.58) | **flag** |


| Market | Low beta (beta-neutral): realised beta | 12-1 momentum (beta-neutral): realised beta |
|---|---|---|
| US | +0.48 | -0.14 |
| EU | +0.28 | -0.33 |
| UK | +0.35 | -0.23 |
| Denmark | +0.02 | -0.17 |
| SCANDI | +0.07 | -0.17 |
| World | +0.58 | -0.22 |


*Realised beta: full-sample regression of the gross book return on the equal-weight universe, 2013–2026. The legs are scaled with 12-month ex-ante betas, clipped to 0.2–3. Frazzini & Pedersen (2014) shrink betas towards 1 for exactly this reason; our books do not, so "beta-neutral" means ex ante, not realised.*

## B. Stress episodes

![Episodes](../figures/fs19_episodes.png)

| Market | Book | 2015–16 sell-off | Q4 2018 | COVID crash | COVID rebound | 2022 rate shock |
|---|---|---|---|---|---|---|
| US | market | -7% | -13% | -19% | +51% | -24% |
|  | low beta | +27% | +4% | -29% | -12% | -24% |
|  | 12-1 momentum | +9% | -4% | +9% | +2% | +10% |
|  | overlay | +8% | +2% | +2% | -4% | +4% |
|  | market + overlay | +1% | -11% | -17% | +45% | -21% |
| EU | market | -13% | -12% | -21% | +38% | -26% |
|  | low beta | +8% | +10% | -16% | -6% | -28% |
|  | 12-1 momentum | +29% | -8% | +8% | -3% | -6% |
|  | overlay | +8% | +1% | -1% | -1% | -6% |
|  | market + overlay | -5% | -11% | -22% | +37% | -30% |
| UK | market | -15% | -10% | -25% | +25% | -8% |
|  | low beta | +12% | -13% | -12% | -2% | -17% |
|  | 12-1 momentum | +5% | -5% | +2% | -3% | +1% |
|  | overlay | +5% | -5% | -2% | +1% | -2% |
|  | market + overlay | -11% | -14% | -26% | +28% | -10% |
| Denmark | market | +3% | -12% | -13% | +53% | -24% |
|  | low beta | +0% | -16% | -5% | -21% | +12% |
|  | 12-1 momentum | +19% | -4% | +8% | +1% | -17% |
|  | overlay | +5% | -6% | -0% | -5% | -1% |
|  | market + overlay | +8% | -18% | -13% | +47% | -24% |
| SCANDI | market | -10% | -14% | -17% | +40% | -27% |
|  | low beta | +4% | -2% | -11% | -8% | +1% |
|  | 12-1 momentum | +15% | -4% | +5% | -2% | -9% |
|  | overlay | +8% | -3% | -2% | -2% | -3% |
|  | market + overlay | -2% | -16% | -18% | +37% | -29% |
| World | market | -14% | -13% | -23% | +49% | -28% |
|  | low beta | +16% | +1% | -24% | +8% | -25% |
|  | 12-1 momentum | +11% | -4% | +7% | +1% | +7% |
|  | overlay | +7% | -2% | -2% | +2% | -2% |
|  | market + overlay | -8% | -14% | -25% | +52% | -30% |


*Books as in FS18: beta-neutral with the turnover buffer, FS16 costs at $50m per book, borrow and financing; overlay at 5% volatility; market = size-weighted universe (World in USD).*

- **Low beta** protects in slow sell-offs (2015–16) but not in fast crashes or rate shocks: it fell with the market in the COVID crash and in 2022 in the US, EU and World.
- **Momentum** was positive in the COVID crash in all six markets and mostly lost only a few per cent in the rebound.
- **The overlay** kept every episode within ±8%. It adds little protection to a market portfolio; its job is return per unit of risk (FS18).

### Momentum crashes (Daniel & Moskowitz 2016)

| Sample | Bear months | Bear × market coefficient (t) | Market coefficient |
|---|---|---|---|
| US | 3 | -1.24 (t -12.3) * | -0.15 |
| EU | 5 | +1.51 (t +2.4) * | -0.35 |
| UK | 20 | -0.09 (t -0.3) | -0.21 |
| Denmark | 21 | -0.13 (t -0.7) | -0.12 |
| SCANDI | 8 | -0.11 (t -1.3) * | -0.12 |
| World | 6 | +0.16 (t +1.2) * | -0.23 |
| America 1999–2013 | 51 | -0.47 (t -1.6) | +0.12 |
| Europe 1999–2013 | 68 | -0.42 (t -1.6) | -0.10 |
| UK 1999–2013 | 47 | +0.17 (t +0.4) | -0.17 |
| Denmark 1999–2013 | 43 | -0.23 (t -1.3) | -0.01 |
| ART pooled | 209 | -0.28 (t -1.9) | -0.02 |


*Momentum (beta-neutral, net) regressed on the equal-weight market, a bear dummy (market down over the previous 24 months) and their product; Newey–West t (ART pooled: White). A negative bear × market coefficient means momentum loses when markets rebound after a bear market. \* fewer than 12 bear months: not interpretable (the US t of −12 rests on 3 months).*

2013–2026 has almost no bear-market states, so the crash risk cannot be tested there. In 1999–2013 the sign is the one Daniel & Moskowitz report (pooled coefficient -0.28, t -1.9), and FS15 showed the spring-2009 momentum loss of −42%. The risk is real, it just did not show up in our main sample.

## C. Sector neutrality

| Market | Sector coverage | Shortlist, unrestricted | Shortlist, within sectors (t) | Sector component | Correlation within vs unrestricted | Low beta, within sectors | Momentum, within sectors |
|---|---|---|---|---|---|---|---|
| US | 95% | +4.8% | +3.4% (t +1.4) | +1.2% | 0.88 | +2.8% | +4.0% |
| EU | 85% | +12.8% | +8.2% (t +3.2) | +2.6% | 0.80 | +10.3% | +6.0% |
| UK | 34% | +19.5% | +15.5% (t +3.7) | +1.1% | 0.89 | +18.4% | +12.5% |
| Denmark | 82% | +2.9% | -1.8% (t -0.8) | +0.2% | 0.70 | +1.0% | -4.5% |
| SCANDI | 84% | +0.1% | +1.1% (t +0.5) | +2.2% | 0.69 | +1.2% | +0.9% |
| World | 76% | +8.7% | +8.2% (t +3.3) | -1.0% | 0.93 | +9.1% | +7.3% |


*Net of 10 bp per side, borrow and financing; beta-neutral legs, no buffer. Coverage: share of stocks with a sector label; the rest form one "unclassified" group. UK coverage is low because many FTSE 250 members are investment trusts missing from the sector caches. Sector component: book sorted on the sector-average signal.*

Across the five markets, about two thirds of the shortlist's return comes from picking stocks within sectors, and the sector bets add the rest. The within-sector book is highly correlated with the unrestricted one. The exception is Denmark, where 19 stocks spread over 11 sectors leave nothing to rank within a sector.

## Caveats

- Sector labels are today's, applied to all years.
- The truncation test covers the price library, not the US fundamental composites (their point-in-time logic is the filing-date lag in FS13b).
- The noise test checks the engine's timing and statistics, not the economic content of any signal.
- FS19 adds 44 trials to the ledger (now 682).

## References

- Daniel, K. & Moskowitz, T. J. (2016). Momentum crashes. *Journal of Financial Economics* 122(2), 221–247.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics* 111(1), 1–25.
- Moskowitz, T. J. & Grinblatt, M. (1999). Do industries explain momentum? *Journal of Finance* 54(4), 1249–1290.
- Asness, C. S., Frazzini, A. & Pedersen, L. H. (2014). Low-risk investing without industry bets. *Financial Analysts Journal* 70(4), 24–41.
- Bailey, D. H., Borwein, J., López de Prado, M. & Zhu, Q. J. (2014). Pseudo-mathematics and financial charlatanism. *Notices of the AMS* 61(5), 458–471.

## Reproduce

`planning/PREREG_FS19.md` → `code/fs19_engine.py` (→ `results/fs19_engine.json`), `code/fs19.py` (→ `results/fs19.json`; uses `sectors.py`, `fs18.py`) → `code/build_fs19.py`. Sector source files are private.
