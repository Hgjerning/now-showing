# Pre-registration · FS20 A Buffett-style checklist, made systematic (proxy)

Written 29 September 2026, before any FS20 result was computed.

## Question

Danish value investors such as Beile Grünbaum describe a Buffett-style checklist: profitable companies, growth, good management, reasonable debt, bought below intrinsic value, 10–12 holdings kept for years (public source: Grünbaum Value Invest, "Investeringsstrategi", 2024). Does a mechanical version of that public checklist beat the market, net of costs? **This is a proxy built from the public description only. It is not Grünbaum's portfolio, his "Velstandsbyggeren" product or his track record, and it must never be presented as such.**

## Universe and data

US point-in-time top 500 by market cap (Sharadar, incl. delisted), Sharadar SF1 ARQ filings usable from their filing date and at most 200 days old. TTM = sum of the last four quarters. 2013–2026. Outside the US there are no stock-level fundamentals, so FS20 is US only.

## Checklist (all must hold at the review date; thresholds fixed here, not tuned)

1. **Profit:** TTM net income > 0 now and four quarters ago; TTM return on equity ≥ 15%.
2. **Growth:** TTM revenue and TTM net income both higher than four quarters ago.
3. **Reasonable debt:** debt / equity ≤ 1.
4. **Management (proxy):** TTM free cash flow (operating cash flow − capex) > 0 and basic shares outstanding up by at most 2% over four quarters (no heavy dilution).
5. **Price below value (proxy):** among the stocks that pass 1–4, rank by free-cash-flow yield (TTM FCF / market cap).

## Portfolio

- **12 stocks**, equal weight, the highest FCF yield among qualifiers.
- **Annual review** at each December month-end (first review December 2012). A holding is kept if it still passes 1–4 and ranks in the top 24 by FCF yield; the rest of the 12 is filled from the top of the ranking. Weights drift between reviews (buy and hold).
- If fewer than 12 qualify, the rest is held in the size-weighted market.
- **Costs:** the FS16 model at $10m (liquidity-dependent half-spread + square-root impact, Y = 0.7) on every trade, including drift-free rebalancing at reviews.

## Tests

- **Primary:** annualised CAPM alpha of the checklist portfolio against the size-weighted US universe (excess returns over T-bills), Newey–West t > 2, and positive alpha in both 2013–19 and 2020–26.
- Reported: return, volatility, Sharpe, maximum drawdown and calendar-year returns vs the market and the equal-weight universe; factor attribution on the JKP US themes (value, profitability, quality, investment, momentum, low risk) to see how much is known factors; turnover and the number of qualifiers over time.
- **Sensitivity (all reported and in the ledger, none chosen):** 12 / 25 / 50 stocks × annual / quarterly review × FCF yield / earnings yield ranking = 12 variants including the primary.

## Honesty notes

- The discretionary parts of the checklist (management quality, moat, intrinsic value) are crude proxies.
- The US large-cap universe and 2013–2026 are the only sample; there is no out-of-sample period.
- All tests enter the trial ledger.
