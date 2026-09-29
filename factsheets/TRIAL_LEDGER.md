# Factsheet trial ledger (FS01–FS13)

Built 2026-09-29 by `code/ledger.py` from the results files; re-run after every rebuild. This ledger is separate from the article programme's `TRIAL_LEDGER.md` files (which count pre-registered hypotheses); here every gated cell of every factsheet is a trial.

**Trials: 682**: primary cells (6 markets × L/S and long-only per strategy), fix-ladder holdout tests, the FS13 battery (19 signals × raw/beta-neutral) the FS13b US fundamental battery (20 signals × raw, beta-neutral and long-only) the FS13c Fama-MacBeth slopes (multivariate, per market and averaged) the pre-registered FS14 multifactor tests the FS15 re-run on 1998–2013 the FS17 factor-level tests of non-US fundamentals the FS18 portfolio overlay and the FS19 robustness tests. The 153 JKP factors in FS13 are published factors, tested there with their own correction, and not counted here.

Programme-wide bars: Bonferroni at 5% over 682 trials needs |t| > 3.97; Benjamini–Hochberg at 5% controls the false-discovery rate instead.

## Trials per factsheet

| Factsheet | Trials | Passed the factsheet's own gate (|t| > 2.87) | Pass programme Bonferroni | Pass programme BH |
|---|---|---|---|---|
| FS01 | 18 | 3 | 0 | 3 |
| FS02 | 16 | 0 | 0 | 0 |
| FS03 | 15 | 2 | 0 | 2 |
| FS04 | 15 | 1 | 0 | 1 |
| FS06 | 15 | 1 | 0 | 2 |
| FS07 | 15 | 1 | 0 | 1 |
| FS08 | 15 | 2 | 0 | 2 |
| FS09 | 15 | 3 | 0 | 3 |
| FS10 | 13 | 2 | 1 | 2 |
| FS11 | 15 | 0 | 0 | 0 |
| FS12 | 15 | 5 | 1 | 5 |
| FS13 | 38 | 1 | 0 | 2 |
| FS13b | 60 | 1 | 0 | 1 |
| FS13c | 66 | 4 | 0 | 4 |
| FS14 | 78 | 0 | 0 | 0 |
| FS15 | 157 | 13 | 4 | 13 |
| FS17 | 58 | 27 | 18 | 28 |
| FS18 | 14 | 0 | 0 | 0 |
| FS19 | 44 | 5 | 0 | 5 |


## What survives the programme-wide correction

74 of 682 trials survive Benjamini–Hochberg: **53 positive** (21 also Bonferroni) and 21 negative. Every positive survivor is a long-only book beating its own equal-weight universe after beta, a single-market long/short, or a fix step; no pooled price signal in FS13 survives on the positive side.

| Factsheet | Strategy | Test | t | p | Bonferroni | BH |
|---|---|---|---|---|---|---|
| FS01 | Turtle Traders | L/S net mean, US | -3.59 | 0.0003 |  | ✓ |
| FS01 | Turtle Traders | L/S net mean, SCANDI | -3.32 | 0.0009 |  | ✓ |
| FS01 | Turtle Traders | L/S net mean, World | -3.00 | 0.0027 |  | ✓ |
| FS03 | Momentum | long-only alpha vs EW, UK | +3.68 | 0.0002 |  | ✓ |
| FS03 | Momentum | long-only alpha vs EW, World | +3.66 | 0.0002 |  | ✓ |
| FS04 | Low volatility | long-only alpha vs EW, UK | +2.96 | 0.0030 |  | ✓ |
| FS06 | Same-month seasonality | L/S net mean, US | -2.81 | 0.0050 |  | ✓ |
| FS06 | Same-month seasonality | L/S net mean, EU | -3.60 | 0.0003 |  | ✓ |
| FS07 | Size | long-only alpha vs EW, UK | +2.95 | 0.0032 |  | ✓ |
| FS08 | Short-term reversal | long-only alpha vs EW, US | -3.13 | 0.0017 |  | ✓ |
| FS08 | Short-term reversal | long-only alpha vs EW, World | -3.15 | 0.0016 |  | ✓ |
| FS09 | 52-week high | long-only alpha vs EW, EU | +3.85 | 0.0001 |  | ✓ |
| FS09 | 52-week high | long-only alpha vs EW, DK | +3.10 | 0.0020 |  | ✓ |
| FS09 | 52-week high | X3 + volatility targeting vs previous step, pooled holdout Sharpe | +3.35 | 0.0008 |  | ✓ |
| FS10 | Betting against beta | L/S net mean, UK | +3.16 | 0.0016 |  | ✓ |
| FS10 | Betting against beta | long-only alpha vs EW, UK | +4.14 | 0.0000 | ✓ | ✓ |
| FS12 | Buy at the 52-week low | L/S net mean, US | -3.40 | 0.0007 |  | ✓ |
| FS12 | Buy at the 52-week low | L/S net mean, EU | -3.37 | 0.0008 |  | ✓ |
| FS12 | Buy at the 52-week low | long-only alpha vs EW, EU | -4.78 | 0.0000 | ✓ | ✓ |
| FS12 | Buy at the 52-week low | L/S net mean, World | -3.58 | 0.0003 |  | ✓ |
| FS12 | Buy at the 52-week low | long-only alpha vs EW, World | -3.81 | 0.0001 |  | ✓ |
| FS13 | Low skewness | beta-neutral, financed, 6-market average | -2.82 | 0.0048 |  | ✓ |
| FS13 | Same-month seasonality | beta-neutral, financed, 6-market average | -3.39 | 0.0007 |  | ✓ |
| FS13b | Profit growth (composite) | long-only alpha vs EW, US | +3.43 | 0.0006 |  | ✓ |
| FS13c | Debt issuance (fund.) | multivariate slope, US | +2.90 | 0.0038 |  | ✓ |
| FS13c | Momentum 12-1 | multivariate slope, EU | +3.65 | 0.0003 |  | ✓ |
| FS13c | Low volatility (252d) | multivariate slope, UK | -3.50 | 0.0005 |  | ✓ |
| FS13c | Momentum 12-1 | multivariate slope, World | +3.14 | 0.0017 |  | ✓ |
| FS15 | Low net tail | L/S net, 4-market average, 1999-2013 | -2.92 | 0.0035 |  | ✓ |
| FS15 | Low skewness | L/S net, 4-market average, 1999-2013 | -4.23 | 0.0000 | ✓ | ✓ |
| FS15 | Low skewness | beta-neutral, financed, 4-market average, 1999-2013 | -5.10 | 0.0000 | ✓ | ✓ |
| FS15 | Small size | Fama-MacBeth slope, US, 1999-2013 | +3.19 | 0.0014 |  | ✓ |
| FS15 | Low MAX (1 day) | Fama-MacBeth slope, EU, 1999-2013 | +2.89 | 0.0039 |  | ✓ |
| FS15 | Same-month seasonality | Fama-MacBeth slope, UK, 1999-2013 | +4.04 | 0.0001 | ✓ | ✓ |
| FS15 | Low skewness | Fama-MacBeth slope, UK, 1999-2013 | -3.22 | 0.0013 |  | ✓ |
| FS15 | Same-month seasonality | Fama-MacBeth slope, World, 1999-2013 | +3.66 | 0.0003 |  | ✓ |
| FS15 | Low skewness | Fama-MacBeth slope, World, 1999-2013 | -3.14 | 0.0017 |  | ✓ |
| FS15 | Low MAX (1 day) | Fama-MacBeth slope, market average, 1999-2013 | +3.22 | 0.0013 |  | ✓ |
| FS15 | Same-month seasonality | Fama-MacBeth slope, market average, 1999-2013 | +4.33 | 0.0000 | ✓ | ✓ |
| FS15 | Low skewness | Fama-MacBeth slope, market average, 1999-2013 | -3.75 | 0.0002 |  | ✓ |
| FS15 | Small size | Fama-MacBeth slope, market average, 1999-2013 | +3.40 | 0.0007 |  | ✓ |
| FS17 | Issuance | alpha on the shortlist, UK, 2013-2025, JKP | +4.34 | 0.0000 | ✓ | ✓ |
| FS17 | Value | alpha on the shortlist, UK, 2013-2025, JKP | +3.42 | 0.0006 |  | ✓ |
| FS17 | Issuance | alpha on the shortlist, Denmark, 2013-2025, JKP | +3.42 | 0.0006 |  | ✓ |
| FS17 | Fundamental pair | alpha on the shortlist, EU (World ex US), 2013-2025, JKP | +3.26 | 0.0011 |  | ✓ |
| FS17 | Fundamental pair (primary) | alpha on the shortlist, non-US average, 2013-2025, JKP (pre-registered) | +4.73 | 0.0000 | ✓ | ✓ |
| FS17 | Issuance | alpha on the shortlist, non-US average, 2013-2025, JKP | +6.04 | 0.0000 | ✓ | ✓ |
| FS17 | Profit growth | alpha on the shortlist, Europe, 1999-2013, ART | +6.88 | 0.0000 | ✓ | ✓ |
| FS17 | Issuance | alpha on the shortlist, Europe, 1999-2013, ART | +3.89 | 0.0001 |  | ✓ |
| FS17 | Value | alpha on the shortlist, Europe, 1999-2013, ART | +4.00 | 0.0001 | ✓ | ✓ |
| FS17 | Profitability | alpha on the shortlist, Europe, 1999-2013, ART | +4.34 | 0.0000 | ✓ | ✓ |
| FS17 | Fundamental pair | alpha on the shortlist, Europe, 1999-2013, ART | +7.08 | 0.0000 | ✓ | ✓ |
| FS17 | Shortlist + fundamental pair | minus shortlist, Europe, 1999-2013, ART | +4.63 | 0.0000 | ✓ | ✓ |
| FS17 | Profit growth | alpha on the shortlist, UK, 1999-2013, ART | +4.70 | 0.0000 | ✓ | ✓ |
| FS17 | Issuance | alpha on the shortlist, UK, 1999-2013, ART | +4.07 | 0.0000 | ✓ | ✓ |
| FS17 | Value | alpha on the shortlist, UK, 1999-2013, ART | +2.94 | 0.0033 |  | ✓ |
| FS17 | Profitability | alpha on the shortlist, UK, 1999-2013, ART | +3.64 | 0.0003 |  | ✓ |
| FS17 | Fundamental pair | alpha on the shortlist, UK, 1999-2013, ART | +6.40 | 0.0000 | ✓ | ✓ |
| FS17 | Profit growth | alpha on the shortlist, America, 1999-2013, ART | +3.66 | 0.0002 |  | ✓ |
| FS17 | Issuance | alpha on the shortlist, America, 1999-2013, ART | +3.29 | 0.0010 |  | ✓ |
| FS17 | Value | alpha on the shortlist, America, 1999-2013, ART | +4.19 | 0.0000 | ✓ | ✓ |
| FS17 | Profitability | alpha on the shortlist, America, 1999-2013, ART | +2.83 | 0.0047 |  | ✓ |
| FS17 | Fundamental pair | alpha on the shortlist, America, 1999-2013, ART | +4.60 | 0.0000 | ✓ | ✓ |
| FS17 | Shortlist + fundamental pair | minus shortlist, America, 1999-2013, ART | +3.07 | 0.0021 |  | ✓ |
| FS17 | Fundamental pair (primary) | alpha on the shortlist, non-US average, 1999-2013, ART (pre-registered) | +7.00 | 0.0000 | ✓ | ✓ |
| FS17 | Profit growth | alpha on the shortlist, non-US average, 1999-2013, ART | +6.18 | 0.0000 | ✓ | ✓ |
| FS17 | Issuance | alpha on the shortlist, non-US average, 1999-2013, ART | +4.34 | 0.0000 | ✓ | ✓ |
| FS17 | Value | alpha on the shortlist, non-US average, 1999-2013, ART | +4.02 | 0.0001 | ✓ | ✓ |
| FS17 | Profitability | alpha on the shortlist, non-US average, 1999-2013, ART | +4.23 | 0.0000 | ✓ | ✓ |
| FS19 | shortlist (within sectors) | net return, EU | +3.20 | 0.0014 |  | ✓ |
| FS19 | low beta (within sectors) | net return, UK | +2.95 | 0.0032 |  | ✓ |
| FS19 | shortlist (within sectors) | net return, UK | +3.74 | 0.0002 |  | ✓ |
| FS19 | shortlist (within sectors) | net return, WD | +3.31 | 0.0009 |  | ✓ |
| FS19 | Shortlist within sectors (primary) | net return, 5-market average (pre-registered) | +2.96 | 0.0031 |  | ✓ |


*Negative t = significantly worse than zero (a strategy that reliably loses).*

## Deflated Sharpe ratio of the best positive candidates

The deflated Sharpe ratio (Bailey & López de Prado 2014) asks how likely the best Sharpe is to be real given 682 trials, the spread of Sharpe ratios across them (estimated as t/√T) and the candidate's skewness and fat tails. For long-only tests the Sharpe is that of the beta-adjusted return over the equal-weight universe, which is what the test measures. SR₀ is the Sharpe ratio the best of 682 worthless strategies would show by luck. DSR > 0.95 is the usual bar.

| Factsheet | Strategy | Test | t | Sharpe (annual) | SR₀, observed spread | DSR, observed spread | SR₀, null spread | DSR, null spread |
|---|---|---|---|---|---|---|---|---|
| FS10 | Betting against beta | long-only alpha vs EW, UK | +4.14 | 0.97 | 1.51 | 0.04 | 0.85 | 0.65 |
| FS09 | 52-week high | long-only alpha vs EW, EU | +3.85 | 0.99 | 1.51 | 0.04 | 0.85 | 0.68 |
| FS03 | Momentum | long-only alpha vs EW, UK | +3.68 | 0.94 | 1.51 | 0.02 | 0.85 | 0.61 |
| FS03 | Momentum | long-only alpha vs EW, World | +3.66 | 0.81 | 1.51 | 0.01 | 0.85 | 0.44 |
| FS13b | Profit growth (composite) | long-only alpha vs EW, US | +3.43 | 0.90 | 1.51 | 0.01 | 0.85 | 0.56 |
| FS10 | Betting against beta | L/S net mean, UK | +3.16 | 0.81 | 1.51 | 0.01 | 0.85 | 0.44 |


*Two versions of SR₀. "Observed spread" uses the dispersion of all 682 trials, which is wide because many trials measure strategies that reliably lose; it is conservative. "Null spread" assumes every trial is noise (variance 1/T); it is the lenient bound. The truth lies between: a candidate that fails the lenient bound is not credible, one that passes only the lenient bound is promising but unproven.*

## Rules from now on

1. Every new factsheet adds its gated cells here before its results are written up.
2. The multifactor battery (FS14) is pre-registered: filters, correlation cut-off, windows and weights are fixed in writing before the run, and its selection counts as trials in this ledger.
3. Headline claims in posts use the programme-wide result, not only the factsheet's own gate.
