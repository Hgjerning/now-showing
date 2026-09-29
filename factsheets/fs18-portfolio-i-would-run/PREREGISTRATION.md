# Pre-registration · FS18 The portfolio I would actually run

Written 27 September 2026, before any FS18 result was computed.

## Question

Put the series' surviving conclusions together, with realistic costs, as an overlay next to a market portfolio. Does it improve on holding the market alone?

## Portfolio (fixed, no selection, no tuning)

Per market (US, EU, UK, DK, SCANDI, World), 2013–2026:
- **Overlay books**, all beta-neutral with the turnover buffer (FS16): low beta, 12-1 momentum; in the US also the profit-growth and debt-issuance composites (FS13b). Outside the US no stock-level fundamentals exist, so the overlay is price-only there.
- **Costs:** the FS16 model (spread + square-root impact, Y = 0.7) at **$50m per book**, plus borrow fees and financing. Sensitivity: $250m per book.
- **Overlay weights:** inverse 36-month volatility of each book (equal risk), re-set monthly; equal weights until 36 months of history exist.
- **Overlay size:** scaled to a 5% annual volatility target with its own trailing 12-month volatility (ex ante, cap 3×).
- **Market:** the size-weighted universe (US market cap; traded value elsewhere), long-only.
- **Portfolio:** 100% market + the scaled overlay.

## Tests

- **Primary:** Sharpe ratio of market + overlay minus Sharpe of the market alone; the pooled test is the mean of the monthly overlay return (the added return, since the market leg is identical) across US, EU, UK, DK and SCANDI, Newey–West t > 2, and positive in both 2013–19 and 2020–26.
- Reported per market: overlay Sharpe, correlation with the market, maximum drawdown of market vs market + overlay, and the $250m sensitivity.

## Honesty note

The overlay's books were chosen from 2013–2026 results, so this is not out of sample for the US fundamental legs; FS15 gave the out-of-sample evidence for the price legs (1999–2013). All tests enter the trial ledger.
