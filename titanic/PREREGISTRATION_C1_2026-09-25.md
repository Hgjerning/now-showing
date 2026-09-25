# Pre-registration: Case 1, "Every bubble rhymes. Does this one?" (2026-09-25)

**Written before any statistic below was computed.** Project10, theme T02 (Cycles, bubbles and
crashes). The question is whether the AI-led equity run-up of 2023–2026 is statistically a
bubble by the two best-established empirical definitions:

1. **Explosiveness** (Phillips, Shi & Yu, 2015): a price that grows faster than any random walk
   with drift can explain. Their GSADF test detects this, and its BSADF sequence dates it.
2. **The Greenwood–Shleifer–You (2019) facts**: after a 100% two-year run-up, the probability of
   a 40% crash rises sharply, but average future returns are *not* reliably negative.

## 1. Data (fixed; nothing downloaded, the sandbox has no market-data access)

- **S&P 500** `^GSPC` daily close, Project3 `Data/GSPC_daily_close.csv` (1927-12 → 2026-09-11).
- **Nikkei 225** `^N225` daily close, Project3 `Data/N225_daily_close.csv` (1965-01 → 2026-09-11).
- **Nasdaq Composite** `^IXIC` daily close 1971-02-05 → 2013-02-01
  (`Project10_Articles/T03_ML_AI_NLP/Case9_NLP_CompanyReports/Stanford/price_history/ixic.csv`).
- **US stock panel**: monthly adjusted closes of 2,504 US tickers (Project1 price cache, Yahoo), 2011-06
  → 2026-09 (September 2026 is partial, to the 18th). **These are today's listed names only:
  survivorship-biased.** Firms that crashed and were delisted are missing, so crash
  probabilities are *lower bounds*.
- All series converted to month-end closes. Price returns (the Nasdaq Composite, S&P 500 and Nikkei are
  price indices; the stock panel is dividend-adjusted).

## 2. Series tested

- **Nasdaq-100 (QQQ)**, 2005-01 → 2026-09.
- **AI-leaders basket**: equal-weight, rebalanced monthly: NVDA, AVGO, AMD, MSFT, META, GOOGL,
  AMZN, ORCL. Index = 100 at 2011-07; runs to 2026-09. The members are fixed here. They are
  chosen ex post as today's AI leaders, which *raises* the chance of finding explosiveness, and
  the article must say so.

## 3. Method

- **GSADF / BSADF** on the log monthly price. ADF regression with intercept and **1 lag**. Minimum
  window r0 = 0.01 + 1.8/√T. Critical values come from 2,000 Monte Carlo draws of the PSY null
  (random walk with asymptotically negligible drift, d·T^(−1), d = 1), one set per sample length,
  seed 42. The BSADF critical-value sequence is simulated position by position.
- **Explosive episode**: BSADF above its critical value for at least 3 consecutive months.
- **GSY events (stock panel)**: a stock's 24-month return crosses +100% (and, separately, +150%).
  After an event the stock is skipped for 24 months, so events do not overlap. **Crash** is a
  40% fall from any subsequent peak within the next 24 months, as in GSY. Controls are all
  stock-months with a complete 24-month past and 24-month future, sampled every 24 months per
  stock.

## 4. Legibility checks (not trials; the tool must pass these before anything else is read)

GSADF must reject at 95% **and** BSADF must flag an explosive episode that covers the month three
months before each known peak:
- S&P 500 1927-12 → 1934-12 (peak Sep 1929);
- Nikkei 225 1970-01 → 1992-12 (peak Dec 1989);
- Nasdaq Composite 1985-01 → 2002-12 (peak Mar 2000).

If two or more fail, the method cannot recognise known bubbles, and C1-1/C1-2 are not interpreted.

## 5. Trials (three; Bonferroni gate at 1 − 0.05/3 = 98.33%)

| trial | hypothesis | gate |
|---|---|---|
| **C1-1** | The Nasdaq-100 is in an explosive episode **now** | GSADF > its 98.33% critical value **and** BSADF in the last month (2026-09) > its 98.33% critical value |
| **C1-2** | The AI-leaders basket is in an explosive episode **now** | same |
| **C1-3** | After a 100% two-year run-up, the 24-month crash probability is higher than unconditionally (GSY replication, US panel 2011–2026) | one-sided two-proportion z-test p < 0.0167, **and** the same sign in 2013–2019 events and 2020–2024 events |

**Reported, not gated:** lag-0 GSADF; the list of dated explosive episodes for every series; GSY
at +150%; mean 12- and 24-month forward returns after run-ups (GSY's second fact); acceleration
(last-12-month share of the 24-month run-up) and volatility splits; the individual AI names
today (24-month run-up, drawdown from peak); and the "rhyme" chart, which aligns every episode
at its peak and places the AI basket's last month at "peak = today". That alignment assumes the
worst case for the AI basket, and the chart must say so.

## 6. Expected outcomes, stated before running

- Legibility: all three historic bubbles flagged. Nasdaq 1999–2000 is the textbook case. The 1929
  window is short, so it may be the marginal one.
- **C1-1 fail**: the Nasdaq-100 has risen strongly, but at the index level I expect the last
  month's BSADF to sit below the Bonferroni critical value.
- **C1-2 pass is plausible (about 50/50)**: the basket had a genuinely explosive phase in
  2023–2024. Whether it is *still* explosive in September 2026 is exactly the open question.
- **C1-3 pass**: the GSY crash result is robust. Survivorship biases against it, but the panel is
  large.
- Forward returns after run-ups: not significantly negative (GSY's point).

## 7. Ledger

C1-1, C1-2 and C1-3 go in `TRIAL_LEDGER.md` before the run. This case keeps its own count.
Programme total before this case: 17 run.
