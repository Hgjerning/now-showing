# FR-AI-1 dated notes (the signed text is not edited; clarifications go here)

## Dated note 1, 21 Nov 2026, about 12:16 (after signature; before any outcome exists, since line 3 starts 30 Oct 2026 and ends 2028)

Two errors of Claude's in the signed wording of line 3, found when the groups were frozen. Neither changes a result,
because there is no result yet. Henrik to confirm.

1. **Universe.** The text says "US top 1,500 by market value as defined in A01". A01 defines no such universe; its test
   C1-3 used a survivor panel of 2,504 stocks. What is used: the point-in-time US top 1,500 member list of 30 Oct 2026
   (`members_USS1500.csv`, the list the DuPont study used). It is the better universe: it is fixed at the start date and
   stocks that later die stay in.
2. **Crash definition.** The text calls the test "C1-3's definition" but defines the crash as a fall of 40% from the
   30 Oct 2026 close at a month-end. C1-3 measured the fall from any later peak. The signed definition stands. It is
   stricter, so both crash shares will be lower than C1-3's 48.0% and 38.3%; the hypothesis is about the difference.

One gap filled: a member with no price on or within 7 days before 30 Oct 2024 has no two-year return and is left out of
both groups (C1-3 also required a complete 24-month past).

Frozen 21 Nov 2026 about 12:16 from prices to 30 Oct 2026: 179 event stocks (two-year return of 100% or more), 1,254 control,
67 left out. File `results/fr_ai_1_line3_freeze_2026-10-30.csv`, sha256 begins a39c10fa278de359 (tickers, group, two-year
return; no prices). Of the eight AI-leaders only AMD is an event stock.

## Dated note 2, 21 Nov 2026, 12:19 [entered as 12:20] (prices to 20 Nov 2026 downloaded 12:18; line 2 not yet run: it was run by the same command, directly after this note was written)

Details the signed text of line 2 leaves open, fixed before the run:
- Source: EODHD's S&P 500 index (GSPC.INDX), 1927-12-30 to 2026-11-20; identical to the Yahoo series A01 used wherever
  the two overlap (largest difference under 0.0001%). Price index, no dividends, for forecast and baseline alike.
- The pattern is the 60 daily closes themselves (not returns), z-normalised within the window.
- "3, 6 and 12 months" for the analogs and the baseline: 63, 126 and 252 trading days after the window's last day.
- Scoring days: the S&P 500 close on the last trading day on or before 20 Feb 2027, 20 May 2027 and 19 Nov 2027,
  as a return from the close of 20 Nov 2026 (6,910.39).
- Baseline: the median 63, 126 and 252-day return over every start day from 3 Jan 1950 whose horizon ends by 31 Dec 2025.
- "Range" of the ten: lowest and highest.

## Dated note 3, 21 Nov 2026, about 12:35 [entered as 12:45] (line 2 forecast known since 12:19; no outcome exists before 19 Feb 2027)

A gap in Claude's preparation, found while building the article. Before proposing line 2, Claude did not check the
programme for earlier tests of analog forecasting. There is one: **A52 Raise the Titanic**, signed and run 14 Oct 2026,
21 trials. A52-1 tested price-path analogs for the US large-cap 12-month return, out of sample 1950 to 2024: failed
(Clark-West p 0.358), and the analog forecast was worse than the historical mean (out-of-sample R² -0.21,
Diebold-Mariano t -4.44). None of the 21 gave a usable return forecast.

Consequences, recorded now:
- Line 2 stands as signed and run. It is the popular method, registered so that it is scored in public.
- **Expectation, stated after the forecast and before any outcome:** on our own evidence the analog forecast loses to the
  baseline. We expect the baseline to win at least two of the three horizons. This is an expectation, not a gate.
- The article must show A52's verdict next to the analog table. A forecast shown without it would mislead.
- Line 2's rule (daily closes, 60 days, 10 matches) is not A52's rule (monthly features). The two are not the same test.

**Confirmed by Henrik, 21 Nov 2026 12:40 ("confirmed"): dated note 1 stands as written.**

## Dated note 4, 21 Nov 2026, 13:05 (after the independent stress test; before the first scored month-end, 30 Nov 2026)

Written by Claude from the stress test's findings 2, 3, 19 and 23. For Henrik to confirm.

**Line 3, disclosures.**
- The groups and the starting prices are those of the close of 30 Oct 2026, three weeks BEFORE the signature of 21 Nov.
  Reason: 30 Oct is the last month-end in the point-in-time price file on hand. The sell-off of 30 Oct to 20 Nov is inside
  the measurement. At signature no price after 30 Oct was on file for the 1,433 stocks; what was known was the index
  (SPY -8.7% from 30 Oct to 20 Nov) and the eight leaders (Nvidia -38.7%, Oracle -22.6%, AMD -15.9% over the same days).
  The statement in note 1 that no outcome existed is therefore too strong: no stock-level outcome had been computed.
- "Up to 31 Oct 2028" means month-ends from 30 Nov 2026 to 31 Oct 2028, both included.

**Line 3, details the signed text left open.**
- Sector for the clustered standard errors: the Sharadar sector of each stock (11 sectors) as on file at 30 Oct 2026.
- A stock that stops trading: it is scored on its last available month-end price. If it is acquired, that is the last
  traded price. If it is delisted for bankruptcy or by the exchange and no later price is available, it counts as a crash.
- Reported beside the gated result, not gated: the same comparison within quintiles of 12-month daily volatility measured
  at 30 Oct 2026 (event stocks against control stocks in the same volatility quintile). Reason: the programme's own check
  of 14 Oct 2026 found the original finding (C1-3) to be mostly a volatility effect.

**Line 2, description.**
- Three scores and no pass mark. One outcome cannot confirm or refute a method; the three horizons overlap.
- The scoring days are calendar dates (19 Feb, 20 May and 19 Nov 2027); they fall a few trading days short of the 63, 126
  and 252 trading days used for the analogs and the baseline. This is left as signed.
- Reported in the article, computed after the run and not scored: the forecast with one setting changed.
