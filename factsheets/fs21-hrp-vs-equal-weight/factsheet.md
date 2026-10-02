# FACTSHEET FS21 · Machine-learning portfolios: hierarchical risk parity vs equal weights

### Does clustering stocks with a machine-learning tree give a better portfolio than splitting the money equally?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · January 2013 – September 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS21.md`, written 30 Sep 2026 before any FS21 number; one deviation (a stale-quote filter), reported as a sensitivity |
| Universes | US (Sharadar, S&P 500 members), EU, UK, Denmark, SCANDI point-in-time universes; World left out (its USD conversion files are not in the folder) |
| Portfolios | Equal weight (EW); inverse variance (IVP); long-only minimum variance with Ledoit–Wolf shrinkage (MinVar, cap 5–10%); hierarchical risk parity (HRP, López de Prado 2016) |
| Rebalancing | monthly, 252 trading days of history, long only, fully invested; costs 10 bp per unit of one-way turnover (25 bp sensitivity) |
| Tests | T1 HRP beats EW, T2 HRP beats IVP: pooled Sharpe difference over five markets, joint block bootstrap, one-sided p < 0.025 |

> **In one paragraph.** **Neither test passes.** Pooled over five markets HRP's Sharpe ratio is +0.06 above equal weight (p 0.18) and -0.03 against simple inverse-variance weights (p 0.82). HRP does what it is built to do, cutting volatility from about 15% to 13% a year, but most of that comes from tilting towards quiet stocks, which inverse-variance weights do without any tree. In the EU the registered run exposed a data problem: a few **stale Yahoo quotes** (prices that never move) look riskless, so HRP put on average 42% of the EU book into a single stock (IVP 29%). With stale series removed (a deviation, reported as a sensitivity) HRP beats EW by +0.08 Sharpe (p 0.07) and IVP by +0.01 (p 0.43): still not significant. The plain long-only minimum-variance portfolio had the best average Sharpe (0.98 vs 0.78 for EW). The lesson matches FS14 and DeMiguel, Garlappi & Uppal (2009): the machine-learning tree is elegant, but on real stocks the gain over 1/N comes from owning less risky stocks, not from the clustering.

![FS21](../figures/fs21_hrp.png)

## 1. Market by market

| Market | Method | Sharpe (registered) | Sharpe (stale removed) | Volatility | Max drawdown | Effective no. of stocks | Largest weight (avg) | Turnover / month | Sharpe at 25 bp |
|---|---|---|---|---|---|---|---|---|---|
| US | EW | 0.84 | 0.95 | 15.5% | -28% | 501 | 0.2% | 3% | 0.84 |
|  | IVP | 0.88 | 0.94 | 13.7% | -24% | 377 | 0.9% | 4% | 0.87 |
|  | MinVar | 0.96 | 0.98 | 10.7% | -15% | 31 | 5.0% | 22% | 0.89 |
|  | HRP | 0.86 | 0.92 | 13.3% | -22% | 322 | 2.0% | 12% | 0.82 |
| EU | EW | 0.70 | 0.74 | 14.5% | -28% | 256 | 0.4% | 4% | 0.69 |
|  | IVP | 0.82 | 0.84 | 11.7% | -25% | 86 | 27.8% | 8% | 0.79 |
|  | MinVar | 0.88 | 0.77 | 9.7% | -19% | 28 | 5.0% | 16% | 0.82 |
|  | HRP | 0.61 | 0.81 | 16.3% | -23% | 38 | 42.5% | 13% | 0.58 |
| UK | EW | 0.66 | 0.72 | 14.2% | -30% | 310 | 0.3% | 4% | 0.65 |
|  | IVP | 0.77 | 0.80 | 11.3% | -24% | 130 | 4.6% | 5% | 0.76 |
|  | MinVar | 1.24 | 1.27 | 7.5% | -16% | 29 | 5.0% | 13% | 1.18 |
|  | HRP | 0.88 | 0.90 | 10.5% | -23% | 65 | 9.6% | 13% | 0.83 |
| Denmark | EW | 0.82 | 0.82 | 15.2% | -33% | 22 | 4.6% | 4% | 0.81 |
|  | IVP | 0.91 | 0.91 | 13.2% | -27% | 17 | 10.8% | 5% | 0.90 |
|  | MinVar | 0.88 | 0.86 | 12.5% | -18% | 12 | 10.0% | 8% | 0.86 |
|  | HRP | 0.92 | 0.90 | 12.9% | -24% | 16 | 12.7% | 11% | 0.89 |
| SCANDI | EW | 0.86 | 0.88 | 14.3% | -29% | 71 | 1.4% | 5% | 0.85 |
|  | IVP | 0.95 | 0.96 | 12.7% | -23% | 57 | 3.8% | 5% | 0.94 |
|  | MinVar | 0.95 | 0.89 | 10.8% | -14% | 16 | 9.9% | 14% | 0.91 |
|  | HRP | 0.94 | 0.95 | 11.9% | -22% | 48 | 5.4% | 12% | 0.90 |


*Net of 10 bp costs; Sharpe on returns without subtracting cash (local currency, as in the series' other long-only books). Effective number of stocks = 1/Σw², averaged over months.*

## 2. Tests

| Test | Registered | Stale quotes removed |
|---|---|---|
| T1 HRP − EW, pooled Sharpe | +0.061, p 0.181, 95% CI [-0.05, +0.19] → **fail** | +0.076, p 0.070 → fail |
| T2 HRP − IVP, pooled Sharpe | -0.028, p 0.823, 95% CI [-0.11, +0.04] → **fail** | +0.007, p 0.431 → fail |

Per market (Ledoit–Wolf 2008 test of the Sharpe difference, HAC, reported only):

| Market | HRP − EW (registered) | HRP − IVP (registered) | HRP − EW (stale removed) |
|---|---|---|---|
| US | +0.01 (t +0.24) | -0.03 (t -1.01) | -0.02 (t -0.42) |
| EU | -0.10 (t -0.55) | -0.21 (t -1.59) | +0.07 (t +1.24) |
| UK | +0.21 (t +2.63) | +0.10 (t +1.92) | +0.18 (t +2.20) |
| Denmark | +0.09 (t +1.19) | +0.00 (t +0.06) | +0.08 (t +1.04) |
| SCANDI | +0.08 (t +1.26) | -0.01 (t -0.23) | +0.07 (t +1.33) |


## 3. What the tree does and does not add

- **Volatility:** HRP is 1.8% a year less volatile than EW on average, and IVP 2.2%. Most of the risk reduction is the inverse-variance tilt; the clustering adds little.
- **Concentration:** HRP holds the equivalent of far fewer stocks than EW, and in thin or dirty data it can concentrate heavily (EU). That fragility is a known criticism of risk-based weights: an estimation error in one variance becomes a big position.
- **Turnover:** 10–14% of the book a month for HRP against 3–5% for EW; costs matter at 25 bp but do not change the ranking.
- **Minimum variance:** the unglamorous optimiser with shrinkage and a weight cap did best in the UK and on average, consistent with the low-risk anomaly (FS04, FS10).

## 4. Caveats

- Local-currency, long-only, large and mid caps; 2013–2026 only.
- The stale-quote filter (more than 20% zero daily returns in the 252-day window) was added after seeing the EU result and is reported only as a sensitivity; the registered test is the verdict.
- Stocks without a return in a month contribute 0 (delisting returns may be missing), identical for all four methods.
- FS21 adds two trials to the ledger.

## 5. References

- DeMiguel, V., Garlappi, L. & Uppal, R. (2009). Optimal versus naive diversification: how inefficient is the 1/N portfolio strategy? *Review of Financial Studies* 22(5), 1915–1953.
- Ledoit, O. & Wolf, M. (2004). A well-conditioned estimator for large-dimensional covariance matrices. *Journal of Multivariate Analysis* 88(2), 365–411.
- Ledoit, O. & Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. *Journal of Empirical Finance* 15(5), 850–859.
- López de Prado, M. (2016). Building diversified portfolios that outperform out of sample. *Journal of Portfolio Management* 42(4), 59–69.
- Raffinot, T. (2017). Hierarchical clustering-based asset allocation. *Journal of Portfolio Management* 44(2), 89–99.

## 6. Reproduce

`planning/PREREG_FS21.md` → `code/fs21.py` (registered) and `code/fs21.py clean` (sensitivity) → `code/build_fs21.py`. Uses `code/data.py` (point-in-time universes) and `code/perf.py`.
