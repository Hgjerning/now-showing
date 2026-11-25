# FR-AI-1: forward record after the November 2026 AI sell-off. PRE-REGISTRATION, DRAFT, NOT SIGNED

Drafted 21 Nov 2026 (Saturday; US markets closed since the close of Fri 20 Nov 2026). Nothing below has been computed.
To be signed by Henrik before the US open on Mon 23 Nov 2026; a signature after that open must say so in a dated note.

## Start and data
- Start: close of Fri 20 Nov 2026. All returns are total returns in US dollars.
- AI-leaders basket: the eight names fixed in `A01/PREREGISTRATION_C1_2026-09-25.md` (NVDA, AVGO, AMD, MSFT, META,
  GOOGL, AMZN, ORCL), equal weight, rebalanced monthly. No name is added or dropped.
- Market: S&P 500 total return (SPY). Stock panel for line 3: Sharadar, US top 1,500 by market value as defined in A01.

## Line 1, the fallen favourite (one observation, a recorded call, not a significance test)
- Measured: basket return minus market return, close 20 Nov 2026 to close 19 Nov 2027.
- Call: NONE. Record only (Henrik 21 Nov 2026 12:09 left the call open with "?"; Claude took the option that claims least).
- Reported, not scored: the two returns and their difference. One observation cannot be tested; the article will say so.

## Line 2, the analog forecast (Henrik's method, rule fixed here)
- Series: S&P 500 daily closes from 3 Jan 1950 to 20 Nov 2026.
- Pattern: the last 60 trading days to 20 Nov 2026, z-normalised. Distance: Euclidean on z-normalised windows.
- Candidates: every window ending before 20 Nov 2025; windows closer than 120 trading days to a better match are dropped.
- Forecast: the median and the range of the 10 nearest windows' forward returns at 3, 6 and 12 months.
- Baseline: the unconditional median return over the same horizons, 1950 to 2025.
- Scored at each horizon: the analog forecast beats the baseline if its absolute error is smaller. Three scores.
- 60 days, 120 days apart and the 10 nearest are Claude's proposals, accepted by Henrik 21 Nov 2026 12:09 ("go with your proposal"). Henrik's earlier piece used the three nearest; the three nearest are named in the article as illustration, and are not scored.

## Line 3, the finding that held, out of sample (the only line with real statistics)
- Event stocks: members of the US top 1,500 on 30 Oct 2026 whose two-year total return to that date was 100% or more.
  Control: the other members. (C1-3's definition, on stocks, at one new date.)
- Crash: a fall of 40% or more from the 30 Oct 2026 close at any month-end up to 31 Oct 2028.
- Hypothesis: the crash share of event stocks exceeds that of control stocks. One-sided, p < 0.05, test of two
  proportions with standard errors clustered by sector group. Interim read, reported and not gated: 30 Oct 2027.
- Known weakness, stated now: one start date, so the stocks share one market path; a pass is weaker than it looks.

## What is NOT tested
No backward test of whether anything "would have warned". No new bubble test. No change to A01 or to C31-3 (No. 2).

## Trial count and ledger
Adds 2 gated lines (line 2 as one family of three scores, line 3) to the programme count. Line 1 is a record, not a trial.
Ledger: `TRIAL_LEDGER.md` in this folder, opened at signature with the file hash.

Signature: ______________________   Date and time: ______________

## Decisions recorded before signature (21 Nov 2026 12:09)
Title: A Night to Remember (working code A68). Publication: off-calendar, aimed at Wed 25 or Thu 26 Nov 2026.
