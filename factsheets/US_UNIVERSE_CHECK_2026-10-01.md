# Factsheets: the US universe on true S&P 500 membership (2026-10-01)

The US books in the factsheets draw each month from the 500 largest of every company that was **ever** in the S&P 500
between 2012 and 2026 (`code/data.py: us_membership`). A company that joined in 2020 can therefore sit in the 2014
universe: the same survivor-list bias as the Season 1 articles. `FS_US_UNIVERSE=sp500_pit` replaces it with the actual
S&P 500 members at each month-end (Sharadar add/remove history, `Project2/archive/sharadar_sp500_full_history.csv`).
Each rule has its own cache folder. Not a new trial.

Check: each factsheet's baseline book (X0, `xs.run`, pre-declared signal and direction), US only, Feb 2013 – Aug 2026,
net of costs (`code/us_universe_check.py`). The published rule reproduces the published US numbers (momentum +6.6%,
low volatility −15.3%, size +0.4%, 52-week low −17.0% a year).

| Factsheet | L/S net, % a year (t): published rule | point-in-time S&P 500 | Long-only Sharpe: published | point-in-time | EW universe Sharpe: published | point-in-time |
|---|---:|---:|---:|---:|---:|---:|
| FS03 Momentum | +6.6 (1.18) | **+1.5 (0.26)** | 1.08 | 0.87 | 0.95 | 0.85 |
| FS04 Low volatility | −15.3 (−2.20) | **−8.7 (−1.24)** | 0.89 | 0.89 | 0.95 | 0.85 |
| FS06 Same-month seasonality | −8.3 (−2.46) | −8.8 (−2.60) | 0.66 | 0.49 | 0.95 | 0.85 |
| FS07 Size | +0.4 (0.14) | −2.1 (−0.48) | 0.77 | 0.53 | 0.96 | 0.85 |
| FS08 Short-term reversal | −6.6 (−1.32) | −5.9 (−1.15) | 0.53 | 0.41 | 0.96 | 0.85 |
| FS09 52-week high | −5.9 (−1.02) | −5.5 (−0.83) | 0.79 | 0.71 | 0.95 | 0.85 |
| FS10 Betting against beta | +2.0 (0.44) | +4.2 (0.93) | 0.95 | 0.94 | 0.95 | 0.85 |
| FS11 Residual momentum | +2.8 (0.70) | +3.9 (0.99) | 0.98 | 0.91 | 0.87 | 0.76 |
| FS12 Buy at the 52-week low | −17.0 (−3.21) | **−10.4 (−2.21)** | 0.52 | 0.48 | 0.95 | 0.85 |

## Reading
- **The whole US universe looked better than it was:** the equal-weight benchmark's Sharpe falls from 0.95 to 0.85, and
  most long-only books lose 0.1–0.2 of Sharpe. The list "knew" which companies would make it.
- **Momentum's US spread mostly disappears** (+6.6% → +1.5% a year): on a list of future winners, last year's winners
  are disproportionately the ones that kept winning.
- **The anti-winner books (low volatility, 52-week low) lose about half their losses.** Buying calm or beaten-down stocks
  looked worse than it was, because the list was full of volatile names that later boomed.
- **Significance changes in two places:** low volatility (t −2.20 → −1.24) and the 52-week low (−3.21 → −2.21) are
  weaker; size changes sign (+0.4% → −2.1%) but is insignificant either way. Seasonality is unchanged.
- The factsheets' headline numbers pool six universes; US is one of them (and a part of World), so pooled figures move
  less than the US column.

## Status
Code is in place (`data.py`, `signals.py`, `signals2.py` follow `FS_US_UNIVERSE`; default unchanged = published rule).
Making `sp500_pit` the default and rebuilding FS01–FS21 is the next step. World (WD) also needs
`factors/fx_daily_datasets.csv`, which is not on this PC; the French and JKP factor files were copied into `factors/`
from `Project2/reporting/style_cache` on 2026-10-01.
