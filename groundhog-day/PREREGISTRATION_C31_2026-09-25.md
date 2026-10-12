# Pre-registration: Case 31, the midterm rally (2026-09-25)

**Written before any number in this file's trials was computed.** Project10, theme T01 (Calendar
and event anomalies). This case continues Project3 trial P3-4, which found the 90-day S&P 500
return after US midterm elections (1930–2022) at +7.6% against an unconditional placebo of
+2.9%, p 0.039. That missed the P3 gate (0.0083) and was filed as *suggestive*.

## 0. Why a new test, not a re-run of P3-4

P3-4 compared the post-midterm window with windows opened on **any** day of the year. But every
post-midterm window opens in early November and runs to mid-March. That is the "winter half"
of the Sell-in-May effect (Bouman & Jacobsen, 2002), historically the stronger half of the
year. So P3-4 cannot separate *the midterm* from *November*. The question here is narrower
and harder: **is a midterm November better than any other November?**

## 1. Data (fixed)

- S&P 500 price index, Yahoo `^GSPC`, daily close 1927-12-30 to 2026-09-11 (copied from
  Project3 `Data/GSPC_daily_close.csv`, identical file). Price returns, no dividends.
- Election day rule: first Tuesday after the first Monday of November (`core.us_election_day`).
- **Midterm years:** 24, 1930–2022 (even years not divisible by 4).
- **Control years (same date, no midterm):** every other year 1928–2025 whose window fits the
  data: 74 years (25 presidential years + 49 odd years). The election-day date rule is applied to
  every year, so the control window opens on the same calendar day.
- President's party at each midterm: the winner's party at the preceding presidential election
  (`data/us_presidential_elections.csv`). This holds for every case, including 1974 (Ford, R).

## 2. Conventions (unchanged from Project3)

Day 0 = first trading day on or after the date. Window (a, b) = close of day a−1 to close of
day b. Post windows start at +1 (results arrive after the close).

## 3. Trials and gates (two trials, Bonferroni 2 → one-sided gate p < 0.025)

| trial | hypothesis | statistic | test | gate |
|---|---|---|---|---|
| **C31-1** | After a midterm, the next 90 trading days beat the same 90 days in other years | mean ret[+1,+90], midterm minus control | one-sided label-permutation test (10,000 shuffles, seed 42), Welch t reported alongside | permutation p < 0.025 **and** the difference positive in both halves (1930–1974 and 1978–2022 midterms, each against all controls) |
| **C31-2** | The 120 trading days *into* a midterm are weaker than the same days in other years | mean ret[−119,0], midterm minus control | one-sided permutation (less), seed 42 | permutation p < 0.025 **and** negative in both halves |

**Reported, not gated** (no verdict can be drawn from any of them): the P3-4 replication
against the unconditional placebo; horizons +20, +60, +125 and +250; the control split into
presidential and odd years; the president's party; hit rates with a binomial test against the
control hit rate; bootstrap 95% CIs; the change in 20-day realised volatility across election
day (the uncertainty-resolution mechanism, Pástor & Veronesi 2013; Kelly, Pástor & Veronesi
2016); and the average path from −120 to +90 with a same-season placebo band.

**No other window, index or definition after seeing the data.** A result that "looks better at
+60" is a new trial and goes in the ledger first.

## 4. The forward test: 2026 (the pre-registered prediction)

The 2026 midterm is on **Tuesday 3 November 2026**. Day +90 falls around mid-March 2027. Before
the vote I will publish:

1. the **historical distribution** of the midterm and control windows,
2. **the 2026 return needed** for the pooled C31-1 test (25 midterms) to clear p < 0.025,
   and the return below which it would move away from the gate,
3. a point prediction and an 80% interval for 2026, taken from the pooled history (the
   midterm mean shrunk halfway to the control mean, and the control distribution's spread).

In March 2027 the observed 2026 return is added, and C31-1 is re-run **once**, on 25 midterms,
same code, same seed. That re-run is logged as trial C31-3 *now*, before the observation exists.

## 5. My expected outcomes (to be scored)

- **C31-1: fail at the gate, p between 0.03 and 0.20.** The winter half is strong on its own
  (my guess for the control mean is +4% to +5% over 90 days), so the midterm's excess shrinks
  from about +4.7 points (against the unconditional placebo) to roughly +3 points. With a
  90-day sd of about 10% and 24 against 74 observations, the standard error is about 2.3
  points, so t is about 1.3.
- **C31-2: fail.** "Midterm years are weak" is mostly a claim about the full calendar year.
  The 120 days into November are a noisy slice of it. I expect p > 0.10.
- **Volatility (reported):** realised volatility falls more after a midterm than after the same
  date in other years. This is weak evidence, since it has only 24 observations.

Henrik's expectation: not stated.

## 6. Ledger

C31-1, C31-2 and C31-3 (the forward re-run) are entered in `TRIAL_LEDGER.md` before the run.
The Project3 count stands at 15. This case keeps its own count and cross-references P3-4.
