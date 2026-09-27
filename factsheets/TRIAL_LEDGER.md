# Factsheet trial ledger (FS01–FS13)

Built 2026-09-27 by `code/ledger.py` from the results files; re-run after every rebuild. This ledger is separate from the article programme's `TRIAL_LEDGER.md` files (which count pre-registered hypotheses); here every gated cell of every factsheet is a trial.

**Trials: 205**: primary cells (6 markets × L/S and long-only per strategy), fix-ladder holdout tests, and the FS13 battery (19 signals × raw/beta-neutral). The 153 JKP factors in FS13 are published factors, tested there with their own correction, and not counted here.

Programme-wide bars: Bonferroni at 5% over 205 trials needs |t| > 3.67; Benjamini–Hochberg at 5% controls the false-discovery rate instead.

## Trials per factsheet

| Factsheet | Trials | Passed the factsheet's own gate (|t| > 2.87) | Pass programme Bonferroni | Pass programme BH |
|---|---|---|---|---|
| FS01 | 18 | 3 | 0 | 3 |
| FS02 | 16 | 0 | 0 | 1 |
| FS03 | 15 | 2 | 1 | 2 |
| FS04 | 15 | 1 | 0 | 1 |
| FS06 | 15 | 1 | 0 | 3 |
| FS07 | 15 | 1 | 0 | 1 |
| FS08 | 15 | 2 | 0 | 2 |
| FS09 | 15 | 3 | 1 | 3 |
| FS10 | 13 | 2 | 1 | 2 |
| FS11 | 15 | 0 | 0 | 0 |
| FS12 | 15 | 5 | 2 | 6 |
| FS13 | 38 | 1 | 0 | 2 |


## What survives the programme-wide correction

26 of 205 trials survive Benjamini–Hochberg: **9 positive** (3 also Bonferroni) and 17 negative. Every positive survivor is a long-only book beating its own equal-weight universe after beta, a single-market long/short, or a fix step; no pooled price signal in FS13 survives on the positive side.

| Factsheet | Strategy | Test | t | p | Bonferroni | BH |
|---|---|---|---|---|---|---|
| FS01 | Turtle Traders | L/S net mean, US | -3.59 | 0.0003 |  | ✓ |
| FS02 | Lottery (MAX) | L/S net mean, US | -2.75 | 0.0060 |  | ✓ |
| FS01 | Turtle Traders | L/S net mean, SCANDI | -3.32 | 0.0009 |  | ✓ |
| FS01 | Turtle Traders | L/S net mean, World | -3.00 | 0.0027 |  | ✓ |
| FS03 | Momentum | long-only alpha vs EW, UK | +3.68 | 0.0002 | ✓ | ✓ |
| FS03 | Momentum | long-only alpha vs EW, World | +3.66 | 0.0002 |  | ✓ |
| FS04 | Low volatility | long-only alpha vs EW, UK | +2.96 | 0.0030 |  | ✓ |
| FS06 | Same-month seasonality | L/S net mean, US | -2.81 | 0.0050 |  | ✓ |
| FS06 | Same-month seasonality | L/S net mean, EU | -3.60 | 0.0003 |  | ✓ |
| FS06 | Same-month seasonality | L/S net mean, DK | -2.74 | 0.0062 |  | ✓ |
| FS07 | Size | long-only alpha vs EW, UK | +2.95 | 0.0032 |  | ✓ |
| FS08 | Short-term reversal | long-only alpha vs EW, US | -3.13 | 0.0017 |  | ✓ |
| FS08 | Short-term reversal | long-only alpha vs EW, World | -3.15 | 0.0016 |  | ✓ |
| FS09 | 52-week high | long-only alpha vs EW, EU | +3.85 | 0.0001 | ✓ | ✓ |
| FS09 | 52-week high | long-only alpha vs EW, DK | +3.10 | 0.0020 |  | ✓ |
| FS09 | 52-week high | X3 + volatility targeting vs previous step, pooled holdout Sharpe | +3.35 | 0.0008 |  | ✓ |
| FS10 | Betting against beta | L/S net mean, UK | +3.16 | 0.0016 |  | ✓ |
| FS10 | Betting against beta | long-only alpha vs EW, UK | +4.14 | 0.0000 | ✓ | ✓ |
| FS12 | Buy at the 52-week low | L/S net mean, US | -3.40 | 0.0007 |  | ✓ |
| FS12 | Buy at the 52-week low | long-only alpha vs EW, US | -2.76 | 0.0058 |  | ✓ |
| FS12 | Buy at the 52-week low | L/S net mean, EU | -3.37 | 0.0008 |  | ✓ |
| FS12 | Buy at the 52-week low | long-only alpha vs EW, EU | -4.78 | 0.0000 | ✓ | ✓ |
| FS12 | Buy at the 52-week low | L/S net mean, World | -3.58 | 0.0003 |  | ✓ |
| FS12 | Buy at the 52-week low | long-only alpha vs EW, World | -3.81 | 0.0001 | ✓ | ✓ |
| FS13 | Low skewness | beta-neutral, financed, 6-market average | -2.82 | 0.0048 |  | ✓ |
| FS13 | Same-month seasonality | beta-neutral, financed, 6-market average | -3.39 | 0.0007 |  | ✓ |


*Negative t = significantly worse than zero (a strategy that reliably loses).*

## Deflated Sharpe ratio of the best positive candidates

The deflated Sharpe ratio (Bailey & López de Prado 2014) asks how likely the best Sharpe is to be real given 205 trials, the spread of Sharpe ratios across them (estimated as t/√T) and the candidate's skewness and fat tails. For long-only tests the Sharpe is that of the beta-adjusted return over the equal-weight universe, which is what the test measures. SR₀ is the Sharpe ratio the best of 205 worthless strategies would show by luck. DSR > 0.95 is the usual bar.

| Factsheet | Strategy | Test | t | Sharpe (annual) | SR₀, observed spread | DSR, observed spread | SR₀, null spread | DSR, null spread |
|---|---|---|---|---|---|---|---|---|
| FS10 | Betting against beta | long-only alpha vs EW, UK | +4.14 | 0.97 | 1.39 | 0.08 | 0.75 | 0.77 |
| FS09 | 52-week high | long-only alpha vs EW, EU | +3.85 | 0.99 | 1.39 | 0.08 | 0.75 | 0.79 |
| FS03 | Momentum | long-only alpha vs EW, UK | +3.68 | 0.94 | 1.39 | 0.06 | 0.75 | 0.74 |
| FS03 | Momentum | long-only alpha vs EW, World | +3.66 | 0.81 | 1.39 | 0.02 | 0.75 | 0.58 |
| FS10 | Betting against beta | L/S net mean, UK | +3.16 | 0.81 | 1.39 | 0.02 | 0.75 | 0.57 |
| FS09 | 52-week high | long-only alpha vs EW, DK | +3.10 | 0.75 | 1.39 | 0.01 | 0.75 | 0.50 |


*Two versions of SR₀. "Observed spread" uses the dispersion of all 205 trials, which is wide because many trials measure strategies that reliably lose; it is conservative. "Null spread" assumes every trial is noise (variance 1/T); it is the lenient bound. The truth lies between: a candidate that fails the lenient bound is not credible, one that passes only the lenient bound is promising but unproven.*

## Rules from now on

1. Every new factsheet adds its gated cells here before its results are written up.
2. The multifactor battery (FS14) is pre-registered: filters, correlation cut-off, windows and weights are fixed in writing before the run, and its selection counts as trials in this ledger.
3. Headline claims in posts use the programme-wide result, not only the factsheet's own gate.
