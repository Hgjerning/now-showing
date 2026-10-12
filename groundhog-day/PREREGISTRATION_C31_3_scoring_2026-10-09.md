# Case 31, C31-3: how the 2026 forecast is scored (clarification)

**Status: DRAFT, 9 October 2026. To be signed by Henrik before the article is published (13 October 2026), and in any case before the vote on 3 November 2026.**

This adds a scoring rule to the forward test C31-3 registered in `PREREGISTRATION_C31_2026-09-25.md` §4. It changes nothing in C31-3 itself: the re-run of C31-1 with 2026 added, same code, same seed, once, on or after 16 March 2027. It was written after the hostile-referee stress test of 9 October 2026 pointed out that C31-3 is close to a certain pass (it fails only if the 2026 window falls about 20% or more), so on its own it tests very little.

## The forecast (from `results/summary.json`, computed 25 September 2026)

- Window: S&P 500 price index (`^GSPC`), close on Tuesday 3 November 2026 to close on Tuesday 16 March 2027 (trading days +1 to +90, NYSE calendar).
- Point forecast: **+4.72%** (midterm mean shrunk halfway to the control mean).
- 80% interval: **−8.93% to +18.20%**.
- Season-only comparison forecast: **+1.86%** (the control mean, 74 non-midterm years).

## Scoring, fixed now

1. **Hit or miss.** A hit if the realised return lies inside the 80% interval (endpoints included).
2. **Head-to-head.** Squared error of +4.72% against squared error of +1.86%. The midterm forecast wins if the realised return is above **+3.29%** (the midpoint), the season-only forecast wins if below.
3. **Reporting.** Both results are reported on 16 March 2027 or the first trading day after, whatever they are, together with C31-3. One election cannot tell the two forecasts apart, and no claim will be made that it does. The scores are kept so that a record across elections can.
4. **No trial is added.** These are scores, not hypothesis tests, and do not change the programme's trial count.

**Signed:** ____________________ (Henrik Gjerning), date __________
