# Pre-registration · FS14 The multifactor model

Written 27 September 2026, before any FS14 code was run. The rules below are fixed; any change after the first run is reported as a deviation in the factsheet and counted as extra trials.

## Question

Does a transparent, dynamic selection and weighting of the factor battery beat (a) owning all candidate books equally and (b) the fixed FS13/FS13c shortlist, out of sample, in each market?

## Building blocks (the battery)

- Every price signal from FS13 (19) as its **beta-neutral long/short book, net of trading costs, size-tiered borrow fees and financing of net long cash** (`results/battery_price.pkl`, column `bn_net`), in all six markets.
- In the US, also the six fundamental theme composites from FS13b, same construction (`results/fund_battery.pkl`).
- Monthly returns, Feb 2013 – Aug 2026. No other signals are added after the run.

## Walk-forward

At every month-end t, using only returns up to and including month t, the rules below choose weights for month t+1. The first portfolio month is the first month with 36 months of history (Feb 2016). Out-of-sample period: Feb 2016 – Aug 2026. Reporting splits it into 2016–2019 and 2020–2026.

## Step 1 · Filter (per market, trailing 36 months)

A book passes when all three hold:
1. trailing mean net return > 0;
2. probabilistic Sharpe ratio PSR(SR > 0) ≥ 0.80 (Bailey & López de Prado 2012), using the trailing skewness and kurtosis;
3. trading costs below 50% of the gross spread over the same window (books whose gross spread is not positive fail).

If no book passes, the portfolio holds cash (return 0) that month.

## Step 2 · Correlation pruning (trailing 36 months)

Rank the survivors by trailing Sharpe ratio. Walk down the list and keep a book only if its absolute correlation with every book already kept is at most 0.70.

## Step 3 · Weighting

Eleven variants, all applied to the pruned set:

| Code | Rule |
|---|---|
| EQ | equal weights |
| RP | inverse volatility (risk parity), 36-month equal-weighted volatility — **the primary specification** |
| W12-E, W12-L, W12-X | w ∝ max(μ, 0) / σ² over the last 12 months, with equal (E), linearly declining (L) or exponential (X, half-life = window/3) observation weights |
| W36-E, W36-L, W36-X | same, 36 months |
| W60-E, W60-L, W60-X | same, 60 months (fewer months used while history is shorter) |

Weights sum to one (a book with μ ≤ 0 gets zero; if all are zero, fall back to equal weights). Changing weights costs 10 bp per unit of one-way weight turnover.

**Volatility scaling.** Every variant is reported unscaled and scaled to a 10% annual target using its own trailing 12-month volatility, capped at 3× (ex ante; no look-ahead).

## Benchmarks

- **ALL-EQ:** all candidate books, equal weights, no filter.
- **SHORT:** the fixed shortlist from FS13/FS13c, equal weights: low beta and 12-1 momentum in every market; plus debt issuance and profit growth in the US.
- The equal-weight universe (the market), for reference only.

## Statistics and decision rule

- Sharpe ratio, annual return and volatility, maximum drawdown, turnover, Newey–West t of the mean.
- **Primary test:** RP versus ALL-EQ, paired difference in monthly returns, pooled across the five markets other than World (World overlaps US, UK and EU), Newey–West t. The claim "the selection process adds value" requires t > 2 on this test **and** a positive difference in both sub-periods.
- The other ten variants and the volatility-scaled versions are reported with a deflated Sharpe ratio over all FS14 trials.
- Trials added to the factsheet ledger: 11 variants × 6 markets (Sharpe vs zero) + the primary paired test + 11 pooled variant tests = 78.

## What would change the plan

Nothing in this document is changed after seeing results. If a bug is found, the fix and its effect are reported.
