# Factsheets re-run: what moved, and why (2 October 2026)

Two things changed since the factsheets were built (26–27 Sep 2026):

- **A. US universe fix.** Actual S&P 500 members at each month-end, instead of the top 500 of every company *ever* in the
  index 2012–2026 (`US_UNIVERSE_CHECK_2026-10-01.md`).
- **B. Price-panel refresh (pit v2, 1 Oct).** Fresh Yahoo prices for every index member, and Oslo (OBX) added to SCANDI.
  The September panels are kept in `_data_private/pit/archive_2026-09-26`.

`code/decompose.py` re-ran FS03–FS12 and FS18 on all four combinations. The September data with the September US list
reproduces the published numbers (FS18 t 1.86 vs 1.85 published; every FS03–FS12 t within 0.04), so nothing else changed.

## FS18, the portfolio I would actually run (pooled, 50m)

| | ann | t | Sharpe | gate passed |
|---|---:|---:|---:|---|
| Published | +1.91% | 1.85 | 0.46 | no |
| A only (US fix) | +1.98% | 1.91 | 0.47 | no |
| B only (price refresh) | +2.17% | 2.08 | 0.52 | **yes** |
| A + B | +2.23% | 2.11 | 0.53 | **yes** |

**The pass comes from the price refresh, not the US fix, and within the refresh from Oslo (see the Oslo split below).** The record keeps the pre-registered verdict (fail, on the
data it was registered on). The refreshed result is reported, not counted. Before it can be quoted, the refresh itself
needs a check (next section), because a data change that turns a fail into a pass is exactly what has to be explained.

## FS03–FS12, six-universe holdout, baseline book (t of the spread / t of the CAPM alpha)

| | Published | A only | B only | A + B |
|---|---|---|---|---|
| FS03 Momentum | +0.76 / +2.16 | +0.41 / +1.94 | +0.90 / +2.50 | +0.53 / +2.27 |
| FS04 Low volatility | −0.70 / +1.06 | −0.41 / +1.68 | −0.76 / +1.19 | −0.46 / +1.79 |
| FS06 Seasonality | −1.52 / −1.48 | −1.78 / −1.69 | −2.02 / −1.99 | **−2.26 / −2.17** |
| FS07 Size | −1.30 / −2.21 | −1.02 / −2.05 | −1.03 / −2.07 | −0.82 / −1.95 |
| FS08 Short-term reversal | −2.44 / −3.43 | −2.48 / −3.63 | −2.89 / −3.79 | **−3.00 / −3.99** |
| FS09 52-week high | +0.06 / +2.29 | −0.01 / +2.18 | +0.25 / +2.73 | +0.18 / +2.62 |
| FS10 Betting against beta | +0.01 / −0.42 | +0.20 / −0.19 | +0.15 / −0.19 | +0.31 / +0.02 |
| FS11 Residual momentum | +1.33 / +2.28 | +1.31 / +2.36 | +1.32 / +2.61 | +1.30 / +2.71 |
| FS12 Buy at the 52-week low | −2.29 / −2.62 | −1.96 / −2.47 | −2.60 / −2.95 | −2.28 / −2.79 |

Reading:
- **The US fix (A) makes the US look less good and the anti-winner strategies less bad**, as expected: momentum's
  alpha t falls (2.16 → 1.94), low volatility's rises (1.06 → 1.68), the 52-week-low loss shrinks.
- **The price refresh (B) moves more than the US fix does**, and mostly in one direction: the negative results get
  more negative (seasonality, short-term reversal) and the alpha t-values rise.
- **Where |t| crosses 2:** seasonality becomes significantly negative (t −2.26) and FS18 passes its gate (t > 2, every
  sub-period positive). The other way, size's alpha t slips from −2.21 to −1.95 (A + B), and momentum's alpha t falls
  below 2 with the US fix alone (1.94) but is back at 2.27 once the refresh is added.

## What the price refresh (B) actually is: checked 2 Oct

Compared the September panels (`pit/archive_2026-09-26`) with pit v2, name by name and day by day:

| | names priced, Sep → Oct | share of index-member quarters with a price | new names still trading today | daily returns that differ on names in both |
|---|---|---|---:|---:|
| UK | 426 → 578 (+152) | 71% → 92% | **0%** (median last price Jul 2022) | 0.05% |
| EU | 394 → 464 (+70) | 81% → 89% | 17% (median last price Mar 2022) | 0.00% |
| SCANDI | 96 → 162 (+66, of which 49 Oslo) | 87% → 95% | 61% (Oslo, current) | 0.00% |
| DK | 28 → 33 (+5) | 91% → 99% | | 0.00% |

- **Nothing was re-priced.** On names in both panels the daily returns are identical (one UK name, CPG.L, differs on one
  day). There is no pence/pound or spike problem: days with a move beyond ±50% go from 109 to 111 in the UK and from 71
  to 72 in the EU, so the new series add almost none.
- **The refresh is a survivorship fix.** In the UK and the EU it adds the index members that had **stopped trading**:
  the companies the September panels could not price. In SCANDI it is mostly Oslo, which also changes what "SCANDI"
  means (now four exchanges).
- So B is a correction in the same direction as A for the UK and the EU. For SCANDI it is mostly a change of universe
  (Oslo), and the Oslo split below shows that this is what moves FS18.
- Still unpriced in v2: 27 UK, 52 EU and 10 SCANDI members, none of them in the EODHD delisted set.

## Oslo split (2 Oct): the FS18 pass is Oslo

Same data and US fix, with SCANDI either as in September (OMXC25 + OMXS30 + OMXH25, 119 names) or with Oslo added:

| FS18 pooled (50m) | t | Sharpe | sub-periods, % a year | gate |
|---|---:|---:|---|---|
| Published | 1.85 | 0.46 | +3.0 / +0.9 | fail |
| Both corrections, **SCANDI as registered** | **1.72** | 0.43 | +3.1 / +0.7 | **fail** |
| Both corrections, SCANDI with Oslo | 2.11 | 0.53 | +3.4 / +1.2 | pass |

- **On the like-for-like universe the two corrections lower FS18 slightly** (t 1.85 → 1.72). The whole move to a pass
  comes from adding Oslo, a change of universe made after the test was registered. It cannot count, and the factsheet
  should not suggest it: FS18 stays a fail, and is a little weaker than published.
- Oslo also drives most of SCANDI's swings in the sort factsheets (e.g. short-term reversal +0.7% → −6.8% a year,
  betting against beta +3.8% → +9.7%); the pooled t-values move much less.
- Like-for-like (no Oslo), the changes in the pooled holdout from published are: seasonality significantly negative
  (t −1.52 → −2.21), short-term reversal more negative (−2.44 → −2.73), 52-week-high alpha up (2.29 → 2.48), size alpha
  −2.21 → −2.04; the rest within ±0.35.

**Recommendation for the rebuild:** use the corrected US universe and the European panels that include the delisted
members, but keep SCANDI as registered (no Oslo) for every factsheet with a registered test. Oslo can appear as a
separate, labelled extension where it is useful (it is a fifth market, not a correction).

## Before the factsheets are rebuilt

1. Done: Oslo split (above).
2. Rebuild every factsheet on A + B **without Oslo**, with a dated "what changed" box (as in Season 1): "US universe
   corrected; European panels now include the members that stopped trading". FS18: fail, t 1.72 (published 1.85).
3. FS19 not re-run (needs the ART battery file); FS15 and FS17 do not use these universes.
