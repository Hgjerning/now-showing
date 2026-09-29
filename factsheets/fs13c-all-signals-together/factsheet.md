# FACTSHEET FS13c · All signals together

### Which signals still matter once the others are in the model?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

| Key facts | |
|---|---|
| Method | Fama-MacBeth: every month, next-month stock returns regressed on all signals at once; slopes averaged over time, Newey–West t (6 lags) |
| Signals | one representative per FS13 cluster (10 price signals) in all markets; plus the six US fundamental composites from FS13b in the US |
| Scaling | each signal is a signed percentile rank from −0.5 to +0.5 (high = the literature's good end), so a slope reads as the top-minus-bottom return the signal adds with the others held fixed |
| Universe | the point-in-time universes of FS01–FS13, eligible stocks only, Feb 2013 – Aug 2026; Denmark (about 19 stocks) is too small for a joint regression and gets univariate slopes only |
| Returns | raw next-month returns in local currency (World in USD), no costs; this measures information, not an implementable book |

> **In one paragraph.** Put all signals into one regression and **12-1 momentum is the only price signal that keeps a clear marginal return**: +10.8% a year top-minus-bottom on average across the five markets with a joint regression (t 2.7), positive in 5 of 5. Its close cousins, residual momentum and near 52-week high, look useful alone but add nothing once momentum is in: they are the same bet. Low beta and low volatility have negative raw slopes: they lower risk but do not raise the return, which is why FS13 needed beta-neutral, leveraged books to make them pay. In the US, **debt issuance** keeps its return next to all price signals and the other fundamentals (t 2.9); **profit growth** does not (t 0.9 jointly, +1.1 with the price signals only), although it survived the price signals in FS13b's beta-neutral decile books. Programme-wide, 4 of the FS13c slopes survive the Benjamini–Hochberg correction: Debt issuance (fund.) (US, t +2.9); Momentum 12-1 (EU, t +3.7); Low volatility (252d) (UK, t -3.5); Momentum 12-1 (World, t +3.1).

![Fama-MacBeth](../figures/fs13c_fmb.png)

## 1. Price signals, all markets

| Signal | Alone: average t | Together: average t | Together: marginal return / yr, market average (t) | Markets positive | Effective markets |
|---|---|---|---|---|---|
| Momentum 12-1 | +1.5 | +2.3 | +10.8% (t +2.7) | 5 / 5 | 1.7 |
| Small size | +1.0 | +0.8 | +2.0% (t +1.4) | 3 / 5 | 2.3 |
| Low skewness | +0.5 | +0.4 | +1.3% (t +0.7) | 4 / 5 | 2.5 |
| Low MAX (1 day) | -0.4 | +0.2 | +1.5% (t +0.7) | 2 / 5 | 2.3 |
| Near 52-week high | +0.5 | -0.1 | +0.5% (t +0.2) | 1 / 5 | 1.8 |
| Residual momentum | +1.7 | -0.3 | -1.0% (t -0.4) | 1 / 5 | 2.0 |
| Short-term reversal | +0.1 | -0.3 | -1.4% (t -0.4) | 0 / 5 | 1.9 |
| Same-month seasonality | +0.1 | -0.5 | -0.9% (t -0.6) | 2 / 5 | 2.2 |
| Low beta | -0.9 | -0.7 | -3.9% (t -0.9) | 1 / 5 | 1.4 |
| Low volatility (252d) | -1.0 | -1.0 | -3.6% (t -1.2) | 0 / 5 | 2.2 |


*Averages over the markets with a joint regression (US, EU, UK, SCANDI, World). Market average = the mean of the monthly slopes across those markets. Effective markets = n² / sum of the correlation matrix of the slope series.*

**Reading it.**

1. **Momentum is the price signal to keep.** Its average t rises from 1.5 alone to 2.3 together: once the other signals soak up the parts of past returns that do not pay (short-term reversal, the low-risk tilt), what remains of momentum pays more clearly.
2. **Momentum's cousins are redundant.** Residual momentum and the 52-week high each earn a positive slope alone and about zero together. In FS14 the momentum block needs one representative, not three.
3. **Low risk does not raise returns.** Beta and volatility have negative raw slopes in most markets. Their value is lower risk at similar return, which a beta-neutral or leveraged construction turns into return (FS10, FS13); a raw-return regression cannot see that.
4. **Seasonality, reversal, tail direction and size** are unreliable: signs flip between markets.

## 2. US fundamentals

| Composite | Alone: t | With the 10 price signals: t | With price signals and the other fundamentals: t | Marginal return / yr (joint) | Momentum t in the same regression |
|---|---|---|---|---|---|
| Debt issuance (fund.) | +3.1 | +2.6 | +2.9 | +5.1% | +2.7 |
| Profit growth (fund.) | +1.6 | +1.1 | +0.9 | +1.6% | +2.8 |
| Value (fund.) | -0.8 | -0.6 | -0.6 | -2.4% | +2.5 |
| Profitability (fund.) | +0.6 | +1.2 | +0.6 | +1.2% | +2.6 |
| Investment (fund.) | -0.7 | -0.5 | -1.2 | -2.0% | +2.8 |
| Accruals (fund.) | +1.8 | +1.4 | +1.6 | +2.8% | +2.8 |


**Debt issuance is the fundamental that adds most**: its slope stays at t 2.9 next to every other signal, stronger than its decile long/short in FS13b (t 1.9), because the regression uses the whole cross-section rather than the two extreme deciles. **Profit growth** is weaker here than in FS13b: most of its linear information overlaps with momentum (firms whose earnings rise also see their prices rise), while its extremes (the top and bottom deciles FS13b trades) keep an edge. The two tests measure different things; FS14 will test profit growth as a decile book, where it worked. Value and investment stay negative; accruals and profitability are positive but weak.

## 3. What goes into the multifactor model (FS14)

- **Momentum block:** 12-1 momentum as the representative (residual momentum and the 52-week high as alternatives, never all three).
- **Low-risk block:** low beta, but only as a beta-neutral, financed book; it is a risk reducer, not a return source in raw terms.
- **US fundamentals:** debt issuance (strongest marginal contribution) and profit growth (decile book).
- **Out:** seasonality, reversal, tail direction, size, and the redundant momentum cousins.

## 4. Caveats

- Raw returns, no costs, no borrow or financing: slopes show information, not what a book would earn (the factsheets' books do that).
- Linear in ranks: a signal that works only in the extremes (profit growth) is understated.
- Collinearity: value, investment and profit growth are strongly correlated in the US (FS13b), so their joint slopes are imprecise.
- Denmark is too small for a joint regression; its univariate slopes are in `results/fmb.json`.
- Multiple testing: the multivariate slopes add 66 trials to the factsheet ledger (`planning/FACTSHEET_TRIAL_LEDGER.md`), now 331 in all.

## 5. References

- Fama, E. F. & MacBeth, J. D. (1973). Risk, return, and equilibrium: empirical tests. *Journal of Political Economy* 81(3), 607–636.
- Newey, W. K. & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica* 55(3), 703–708.
- Green, J., Hand, J. R. M. & Zhang, X. F. (2017). The characteristics that provide independent information about average U.S. monthly stock returns. *Review of Financial Studies* 30(12), 4389–4436.
- Lewellen, J. (2015). The cross-section of expected stock returns. *Critical Finance Review* 4(1), 1–44.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.

## 6. Reproduce

`code/fmb.py` (regressions → `results/fmb.json`, slope series in `results/fmb.pkl`) → `code/build_fs13c.py`.
