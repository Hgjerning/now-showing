# Pre-registration · FS21 Machine-learning portfolios: hierarchical risk parity vs equal weights

Written 30 September 2026, before any FS21 number was computed.

## Question

López de Prado (2016) proposed hierarchical risk parity (HRP): cluster stocks by correlation with a machine-learning tree, then split risk down the tree. He showed it beats classic optimisers out of sample in simulations. DeMiguel, Garlappi & Uppal (2009) showed that plain 1/N is hard to beat. FS14 found the same for factor books. Does HRP beat equal weights, and does the clustering add anything over simple inverse-volatility weights, on real stocks?

## Universes and data

US (Sharadar top 500), EU, UK, Denmark, SCANDI: the point-in-time universes of the factsheet series (`code/data.py`, `load` / `load_pit`). **World is left out**: its USD conversion needs FX files that are not in the Factsheets folder. Local-currency total returns.

## Portfolios (long only, fully invested, rebalanced each month-end, formed from data up to that day)

1. **EW**: 1/N over eligible stocks.
2. **IVP**: weights ∝ 1 / variance (252-day daily returns).
3. **MinVar**: long-only minimum variance with Ledoit–Wolf (2004) shrinkage covariance (252 days); weight cap 10% (5% for US, EU, UK where N > 100).
4. **HRP**: López de Prado (2016): correlation distance √(½(1−ρ)), single-linkage tree, quasi-diagonal ordering, recursive bisection with inverse-variance cluster weights; 252-day sample covariance.

Eligible: in the universe at the month-end and at least 240 of the last 252 daily returns present. Costs: 10 bp per unit of one-way turnover (drifted weights to new weights). Months: formation December 2012 to August 2026 (returns January 2013 – September 2026).

## Tests (gate 0.05/2 = 0.025, one-sided)

- **T1: HRP beats EW.** Pooled over the five markets, the mean of (Sharpe HRP − Sharpe EW) is positive; p-value from a joint stationary block bootstrap of monthly returns (mean block 6 months, 10,000 draws, markets resampled on the same dates).
- **T2: the tree adds something.** Same test for Sharpe HRP − Sharpe IVP.
- Reported, not gated: each market separately (with the Ledoit–Wolf 2008 Sharpe-difference test), volatility, maximum drawdown, turnover, effective number of stocks (1/Σw²), the MinVar portfolio, and a sensitivity at 25 bp costs.

## Expected outcome

HRP should have lower volatility than EW and similar Sharpe; the literature's gains are mostly against unconstrained optimisers, not against 1/N. A null for T1 is expected.

## Trial ledger

Two trials (FS21-1, FS21-2).
