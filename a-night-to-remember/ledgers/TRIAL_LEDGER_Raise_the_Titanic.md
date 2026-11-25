# Trial ledger: A52 Raise the Titanic

| # | registered | hypothesis | pre-registration | outcome |
|---|---|---|---|---|
| A52-1 | 2026-10-14 | US large, price-path analogs beat the historical mean (12-month return, out of sample, 1950–2024) | `PREREGISTRATION_A52_2026-10-14.md` | **failed**: Clark–West t +0.36, p 0.358 (gate 0.003125); out-of-sample R² -0.21; Diebold–Mariano t -4.44. Prediction (fail) held. |
| A52-2 | 2026-10-14 | US large, key-figure analogs | same | **failed**: Clark–West t -0.35, p 0.636 (gate 0.003125); out-of-sample R² -0.32; Diebold–Mariano t -3.20. Prediction (fail) held. |
| A52-3 | 2026-10-14 | US large, macro analogs | same | **failed**: Clark–West t +1.34, p 0.091 (gate 0.003125); out-of-sample R² -0.07; Diebold–Mariano t -1.16. Prediction (fail) held. |
| A52-4 | 2026-10-14 | US small, price-path analogs | same | **failed**: Clark–West t +1.03, p 0.151 (gate 0.003125); out-of-sample R² -0.26; Diebold–Mariano t -3.54. Prediction (fail) held. |
| A52-5 | 2026-10-14 | US small, key-figure analogs | same | **failed**: Clark–West t +1.25, p 0.105 (gate 0.003125); out-of-sample R² -0.29; Diebold–Mariano t -2.73. Prediction (fail) held. |
| A52-6 | 2026-10-14 | US small, macro analogs | same | **failed**: Clark–West t -0.77, p 0.780 (gate 0.003125); out-of-sample R² -0.19; Diebold–Mariano t -3.06. Prediction (fail) held. |
| A52-7 | 2026-10-14 | Europe large, price-path analogs (2000–2024) | same | **failed** (valid run on ECB Euro STOXX 50, 2000–2024, n 300): Clark–West t +0.07, p 0.471 (gate 0.003125); out-of-sample R² -0.14; Diebold–Mariano t -1.99. Prediction (fail) held. First run invalid (data error, see below) |
| A52-8 | 2026-10-14 | Europe large, reduced key-figure analogs | same | **failed** (valid run on ECB Euro STOXX 50, 2000–2024, n 300): Clark–West t +0.81, p 0.210 (gate 0.003125); out-of-sample R² -0.08; Diebold–Mariano t -0.95. Prediction (fail) held. First run invalid (data error, see below) |

Gate: one-sided Clark–West p < 0.003125 (0.025 / 8). **Programme total before: 204 run, 12 registered.**

## Implementation rules, fixed 14 Oct 2026 before the run (where the pre-registration left a detail open)

- If fewer than 5 eligible analogs exist (early months, mostly for the macro set, which starts in 1949), the forecast is the
  benchmark. Those months count in the score and add nothing either way. The share of months with real analogs is reported.
- US small caps use the US economy-wide K features (CAPE, real rate, credit spread) and their own price features
  (drawdown, trailing return, volatility). The macro set is the same for US large and small; only the outcomes differ.
- CPI is lagged one month wherever it is used, including the real rate in K.
- Shiller dividends are carried forward after the last reported month (May 2026); this touches only months after the scored window.
- Bear-market months (reported subset): the market is 20% or more below its previous peak, on the log price path built
  from the same monthly returns.
- Europe small caps (reported only): French Europe market + SMB, USD, from July 1990; set P only.
- Data downloaded 14 Oct 2026, 06:51 CEST: FRED (BAA, AAA, GS10, TB3MS, UNRATE, INDPRO, CPIAUCNS), Ken French size
  portfolios (CRSP 202608) and Europe 3 factors. Shiller `ie_data.xls` as on file (prices to October 2026).

## Run, 14 October 2026 (`code/run_analogs.py`, log `results/_run_log.txt`)

A52-1 to A52-6: run as registered, 0 of 6 passed. **A52-7 and A52-8: data error, run not valid.** The pre-registration
names the Euro STOXX 50 from December 1987; the file used (`SX5E_daily_close.csv`) starts in March 2007 (the data
inventory's 1987 date belongs to the DAX file in the same group). With a library of only a few years, 39% and 35% of
months fell back to the benchmark. The numbers from that run are recorded above and will be shown in the article. The
two trials stay registered and run once on the registered series when it is on file; if it cannot be obtained, they are
reported as not run. No substitute index is used without a new, signed amendment.
**Programme total: 210 run, 14 registered and not yet run** (12 before, plus A52-7 and A52-8).

**Re-run of A52-7 and A52-8, 14 Oct 2026, on the registered series** (ECB Data Portal FM.M.U2.EUR.DS.EI.DJES50I.HSTA, monthly average, from Dec 1987; downloaded 14 Oct 2026): both failed. The invalid first run's files are kept in `results/invalid_run_SX5E_2007/`. Part I: 8 run, 0 passed. **Programme total: 212 run, 12 registered and not yet run.**

# Part II (A52-9 to A52-21), signed 14 Oct 2026, 07:33 CEST

| # | registered | hypothesis | pre-registration | outcome |
|---|---|---|---|---|
| A52-9 | 2026-10-14 | US large, price path, scored 1900–1949 | `PREREGISTRATION_A52_PART2_2026-10-14.md` | **failed**: t -0.74, p 0.7714 (gate 0.0050); out-of-sample R² -0.18; Diebold–Mariano t -2.21. Prediction (fail) held. |
| A52-10 | 2026-10-14 | US large, key figures without credit spread, 1900–1949 | same | **failed**: t +0.15, p 0.4404 (gate 0.0050); out-of-sample R² -0.06; Diebold–Mariano t -0.87. Prediction (fail) held. |
| A52-11 | 2026-10-14 | US small, price path, 1935–1949 | same | **failed**: t -0.13, p 0.5516 (gate 0.0050); out-of-sample R² -0.19; Diebold–Mariano t -1.93. Prediction (fail) held. |
| A52-12 | 2026-10-14 | Sweden, price path, 1921–2011 | same | **failed**: t +1.10, p 0.1357 (gate 0.0050); out-of-sample R² -0.10; Diebold–Mariano t -2.48. Prediction (fail) held. |
| A52-13 | 2026-10-14 | 16 countries (JST), annual, pooled analogs, 1900–2019 | same | **PASSED** on Clark–West (t +3.03, p 0.0012, gate 0.0050), but as a forecast it loses to each country's own average (out-of-sample R² −0.08; Diebold–Mariano t −2.16). Prediction (fail) wrong. |
| A52-14 | 2026-10-14 | US large K, ½ analog + ½ mean | same | **failed**: t -0.35, p 0.6356 (gate 0.0050); out-of-sample R² -0.09; Diebold–Mariano t -1.90. Prediction (fail) held. |
| A52-15 | 2026-10-14 | US large K, relevance-based prediction | same | **failed**: t +0.46, p 0.3243 (gate 0.0050); out-of-sample R² -0.79; Diebold–Mariano t -3.31. Prediction (fail) held. |
| A52-16 | 2026-10-14 | US large K, 5-year horizon | same | **failed**: t +0.75, p 0.2253 (gate 0.0050); out-of-sample R² -0.32; Diebold–Mariano t -1.48. Prediction (fail) held. |
| A52-17 | 2026-10-14 | US large K, economic value (certainty equivalent) | same | **failed**: t -3.08, p 0.9989 (gate 0.0050). Prediction (fail) held. |
| A52-18 | 2026-10-14 | US large P, dynamic time warping | same | **failed**: t -0.34, p 0.6315 (gate 0.0050); out-of-sample R² -0.26; Diebold–Mariano t -4.82. Prediction (fail) held. |
| A52-19 | 2026-10-14 | US large K, next-12-month volatility vs trailing volatility | same | **PASSED** against last year's volatility (t +4.35, p < 0.0001; R² +0.22), but a 50/50 mix of last year's and the long-run average volatility does better (R² +0.34): mean reversion, not the analogs. Prediction (fail) wrong. |
| A52-20 | 2026-10-14 | US small K, same | same | **PASSED** against last year's volatility (t +4.75, p < 0.0001; R² +0.23), but a 50/50 mix of last year's and the long-run average volatility does better (R² +0.30): mean reversion, not the analogs. Prediction (fail) wrong. |
| A52-21 | 2026-10-14 | US large K, next-12-month maximum drawdown vs historical average | same | **failed**: t -0.21, p 0.5838 (gate 0.0083); out-of-sample R² -0.31; Diebold–Mariano t -3.20. Prediction (fail) held. |

Gates: family B (9–13) p < 0.005; family C (14–18) p < 0.005; family D (19–21) p < 0.0083. Stricter check (reported): p < 0.0012 across all 21.

## Part II implementation rules, fixed before the run (details the pre-registration left open)

- **Sweden (A52-12):** Riksbank *Historical Monetary Statistics* vol. II, table II.A6.6, nominal stock returns index, monthly, Oct 1901 → Feb 2013. Last full data year 2012, so scored Jan 1921 → Dec 2011.
- **JST (A52-13):** R6; 16 countries with equity returns (Canada and Ireland have none). Real return = log(1 + eq_tr) − log(CPI_t / CPI_t−1). Features at year t: real returns t, t−1, t−2; drawdown of the real equity index from its running peak; real bill rate (log(1 + bill_rate) − inflation); inflation. Analog pool: every country-year s ≤ t − 1; no two analogs from the same country within one year of each other. Standardised on all country-years up to t. Benchmark: each country's own mean real return up to t − 1. Score: Clark–West terms averaged across countries within each year, then NW (2 lags) over years.
- **Relevance (A52-15):** Czasonis–Kritzman–Turkington partial-sample regression: relevance r = −½·Mahalanobis(x_i, x_t) + ½·[Mahalanobis(x_i, μ) + Mahalanobis(x_t, μ)], with μ and the covariance from data up to t; retained set r ≥ r*; prediction ȳ + λ²/(n−1)·Σ δ_i (r_i − φ r̄_ret)(y_i − ȳ), φ = share retained, λ² = var(r, all) / var(r, retained); r* = the {0, 20, 40, 60, 80}th percentile with the highest fit (squared correlation between the weights and past outcomes), all on data up to t.
- **5 years (A52-16):** scored to the last month with a known 5-year outcome (data end, Oct 2026, minus 60 months).
- **Economic value (A52-17):** forecast excess return = analog (or mean) 12-month log-return forecast minus the 3-month T-bill rate; variance = trailing 60 months of monthly returns, annualised; weight = clip(excess / (3 × variance), 0, 1.5), held for the next month; utility per month u = r_p − 1.5·r_p²; test the mean of u(analog) − u(mean) > 0.
- **DTW (A52-18):** distance = √(DTW² of the standardised 12-return shape, Sakoe–Chiba band 3 + squared standardised drawdown difference).
- **Maximum drawdown (A52-21):** the largest peak-to-trough fall of the log price within months t … t + 12.

## Part II run, 14 October 2026 (`code/run_part2.py`, log `results/_run_log.txt`)

13 run, **3 passed their family gate: A52-13, A52-19, A52-20.** None passes the stricter check across all 21 A52 trials except
A52-19 and A52-20 (A52-13: p 0.00123 against 0.00119). Read with the checks below (reported, not gated, run after the result):

- **A52-13 (17 countries, annual):** passes on Clark–West, but the analog forecast's squared error is still *higher* than each
  country's own average (out-of-sample R² −0.08; Diebold–Mariano t −2.16). The analogs carry some information about next
  year's real return, but used directly as a forecast they lose to the average.
- **A52-19 and A52-20 (volatility):** the analogs beat last year's volatility carried forward (R² +0.22 and +0.23). A simple
  50/50 mix of last year's volatility and the long-run average does better still (R² +0.34 and +0.30 against the same
  benchmark), and the analogs lose to that mix (R² −0.18 and −0.10). The pass reflects volatility drifting back to normal,
  not information in the analogs beyond that.
- **A52-14 (shrinkage):** a design point found in the run: the Clark–West statistic is unchanged by a fixed blend weight
  (t −0.35, identical to A52-2), so this trial could not differ from A52-2 on its gate. Shrinkage does improve squared error
  (R² −0.32 to −0.09 at ½, −0.03 at ¼) but never above zero.
- **A52-17 (economic value):** timing the equity weight with analogs gave significantly *lower* utility than timing with the
  historical mean (t −3.08).

**Programme total: 225 run, 12 registered and not yet run.**
