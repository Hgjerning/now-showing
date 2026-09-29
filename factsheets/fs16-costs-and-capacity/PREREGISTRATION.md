# Pre-registration · FS16 Costs that grow with size

Written 27 September 2026, before any cost-model result was computed.

## Question

How much of the factsheet results survives realistic trading costs that grow with the size of the portfolio, and how much money can the books hold (capacity)?

## Cost model (fixed now)

For every stock traded at month-end t, the one-way cost as a fraction of the value traded is

    cost = half-spread + Y × σ × sqrt(q / ADV)

- **ADV:** 63-day average daily traded value in USD (local currency converted with Fed H.10 rates). US: Close × Volume from the Project1 price cache where available; for US stocks without volume data (mostly delisted names), market cap × the median ADV/market-cap ratio of stocks in the same size quintile that month.
- **Half-spread:** 5 bp × (ADV / $50m)^−0.3, bounded to 2–50 bp (about 2.5 bp for a $500m-a-day stock, 10 bp for $5m a day).
- **Impact:** square-root law (Almgren et al. 2005; Frazzini, Israel & Moskowitz 2018), Y = 0.7, σ = 63-day daily volatility, q = portfolio capital × change in the stock's weight. Sensitivity: Y = 1.0.
- The model replaces the flat 10 bp per side; borrow fees and financing stay as before.

## Portfolio sizes

Capital per book of $1m, $10m, $100m, $1bn and $10bn (the long side's gross value equals capital; beta-neutral books scale their legs as before).

## Books

In all six markets, 2013–2026: the shortlist legs (low beta, 12-1 momentum, both beta-neutral) and their equal-weight combination; plus the raw long/short books of 12-1 momentum, low volatility (252d), short-term reversal and low MAX to show fast versus slow signals.

## Outputs

Net return and Sharpe ratio at each size; cost per year; median participation (q/ADV); capacity = the size at which the net Sharpe ratio halves relative to $1m and the size at which the net return reaches zero (log-linear interpolation on the grid). No new significance tests are claimed; the net Sharpe ratios are descriptive.
