# A05 trial ledger

Programme total before: 20 run.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| A05-1 | 2026-09-25 | At least one of 16 guru recipes has a robust FF5+Mom alpha (|t|>2.955, same sign both halves) | `PREREGISTRATION_A05_2026-09-25.md` | **PASSED**: 5 of 16 recipes clear |t| > 2.955 with the same sign in both halves: Greenblatt (α +2.1%/yr, t 3.2), P. O'Shaughnessy millennial (+1.8%, t 5.4), Buffett quality (+3.4%, t 5.8), Graham (+2.2%, t 5.5), Mohanram (+2.5%, t 5.0). The other 11 leave no robust alpha (all 16: median R² 0.74, median |α| 0.5%/yr against a median |raw premium| 2.8%/yr; the 11 alone: R² 0.80, |α| 0.39%, |raw| 2.7%). **Prediction (1–3 pass) was WRONG: 5 passed**, all with quality/profitability/safety content. Since 2012 every passer's α is smaller than its full-sample α. |

**Programme total: 21 run.** A reported (non-gated) 7th factor, AQR QMJ, is examined afterwards in `code/seventh_suspect.py`. It decides nothing.

**Revision 2026-10-07 (after external review):** `code/fake_gurus.py` adds a fake-guru placebo (10,000 random recipes from 153 JKP factors, plus 2,000 from the legends' own 29 ingredients, same A05-1 procedure) and a step-by-step decomposition. **Reported, not gated, not a trial**; programme count unchanged. Result: fakes pass 48% (own ingredients 46%) against the legends' 31% (5 of 16); P(5 or fewer of 16) = 0.14. The A05-1 verdict stands; its interpretation narrows: surviving the six factors is not unusual.

**Stress test 2026-10-23 (two referees, then a third; `STRESS_TEST_2026-10-23.md`).** A05-1 reproduced exactly by an
independent re-implementation (α, t, halves, R² to about 1e-14); no code bug; verdict unchanged (PASSED, 5 of 16). Added
(reported, not gated, no trial): `code/a05_stress_checks.py` → `results/a05_stress.json`. The fake-guru P(5 or fewer)
= 0.14 assumed independent recipes; the real recipes share legs, so a structure-preserving placebo (each of the 27 distinct
legs mapped to a random factor, all 16 recipes rebuilt with the real overlaps, 1,000 panels per variant) gives mean 7.8
(SD 2.6), P(≤ 5) = 0.20 with every leg in its published direction, and mean 6.7 (SD 2.5), P(≤ 5) = 0.33 with the real
recipes' signs. Newey–West lags 0/3/6/12: 5 passes; 24 lags: 6 (Carlisle t 3.06).

**Pre-registered expectations, scored (added 2026-10-23):** (1) R² above 0.6 for the value-type recipes and O'Neil: right
except Graham (0.587). (2) One to three pass, the rest |α| < 2%/yr: WRONG (5 pass; Carlisle +2.4%). (3) α since 2012
smaller for almost every recipe: WRONG (7 of 16; all 5 passers smaller, 9 of the 11 others larger). Developed markets
start 1990-11 (French developed momentum), not the pre-registered 1990-07.
