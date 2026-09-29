# Pre-registration · FS19 Robustness: engine tests, stress episodes, sector neutrality

Written 29 September 2026, before any FS19 result was computed.

## Question

Are the series' conclusions artefacts of (a) a bug or look-ahead in the engine, (b) a few lucky or unlucky episodes, or (c) hidden sector bets? These are the three remaining gaps from step 1 of the FS00 plan.

## A. Engine tests (pass/fail, fixed before running)

1. **Truncation test (look-ahead).** For US, EU and UK, rebuild all 19 library signals from daily returns cut off at month-end T for T = Dec 2015, Dec 2019, Dec 2023, and compare the signal at T with the full-sample signal at T. Pass: every signal identical (max absolute difference < 1e-9 on common names) for every T.
2. **Noise test.** Replace daily returns with iid normal noise (same missing-data pattern, 2% daily volatility), rebuild all 19 signals and run each through `xs.run` (deciles, gross). Five noise seeds, US and EU. Pass: the share of |t| > 1.96 across the 190 gross L/S t-statistics is between 1% and 10%, and no single |t| > 4.
3. **Cheat test (timing).** On the same noise, a signal equal to next month's return must earn a gross L/S t above 20 (the engine can see real predictability), and a signal equal to the month-t return (known at t) must pass the noise-test bar (it cannot predict iid noise).
4. **Cost accounting.** On real US data, for low beta (beta-neutral) and 12-1 momentum: ls_gross − ls_net equals cost + borrow + financing to 1e-12 each month; cost equals 10 bp × 2 × (turnover of both legs); with borrow and financing switched off, net = gross − cost.
5. **Beta neutrality.** Realised full-sample beta of the beta-neutral low-beta and momentum books on the equal-weight universe: reported per market; flagged if |beta| > 0.3.

## B. Stress episodes (descriptive, fixed windows)

Episodes: 2015–16 sell-off (Jun 2015–Feb 2016), Q4 2018 (Oct–Dec 2018), COVID crash (Feb–Mar 2020), COVID rebound (Apr–Dec 2020), 2022 rate shock (Jan–Sep 2022). Books: market (size-weighted), low beta and 12-1 momentum (beta-neutral, buffered, FS16 costs at $50m, as in FS18), FS18 overlay and FS18 market + overlay. Reported: cumulative return per episode and market.

**Momentum crash test (Daniel & Moskowitz 2016):** regress monthly momentum (beta-neutral, net) on the market, a bear-state dummy (market return over the past 24 months < 0), and bear × market. Run on 2013–26 per market and on the ART 1999–2013 regions (pooled). Reported: the bear × market coefficient and t; a negative coefficient means momentum crashes in rebounds.

## C. Sector neutrality (primary test of FS19)

- Sector map: static 11-sector Morningstar/Yahoo taxonomy (Sharadar TICKERS 2019 snapshot incl. delisted, plus Project1/Project2 Yahoo sector caches). Stocks without a sector form one "unclassified" group. Coverage reported per market (UK is expected to be low: many FTSE 250 investment trusts).
- Sector-neutral signal: percentile rank of the signal within its sector each month; the book then sorts on that rank (same deciles, beta-neutral, buffer off, standard 10 bp costs, borrow and financing).
- Books: low beta, 12-1 momentum; the shortlist = equal weight of the two.
- **Primary:** pooled (US, EU, UK, DK, SCANDI) sector-neutral shortlist, net: mean monthly return with Newey–West t > 2, and at least half of the unrestricted shortlist's pooled mean.
- Also reported: the sector component (sort on the sector-average signal) and the per-market difference sector-neutral minus unrestricted.

## Honesty note

A and C are tests of conclusions already published; B is descriptive. All gated tests enter the trial ledger. Sector labels are today's (static), which can bias against sector-changers.
