# FACTSHEET FS20 · A Buffett-style checklist, made systematic

### Profitable, growing, low debt, cash-generating, cheap: does a mechanical version of a Danish value investor's public checklist beat the market?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · January 2013 – September 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

> **US, 1999–2012 (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time S&P
> 500 with delisted stocks, 1999–2012, a period this factsheet was not built on. Primary checklist: CAPM alpha +9.6% a
> year, t +2.67, positive in both halves (+12.1% in 1999–2005, +6.4% in 2006–2012): **passes the registered rule**
> (2013–2026: −0.6%, t −0.24). 10 of 12 variants have t > 2. Below the 2.87 gate used across these factsheets and below
> the programme-wide bar; it reads as value and quality recovering after the 2000 bubble, not as an edge that holds in
> every period. Pre-registration, method and every result: `PREREG_US_1999_2012.md`.





| Key facts | |
|---|---|
| What it is | A **proxy** built only from the public description of a Buffett-style checklist used by Danish value investors such as Beile Grünbaum (Grünbaum Value Invest, "Investeringsstrategi", 2024). **It is not Grünbaum's portfolio, his "Velstandsbyggeren" product or his track record, and it says nothing about them.** |
| Pre-registration | `planning/PREREG_FS20.md`, written 29 Sep 2026 before any FS20 number was computed; no deviations |
| Universe | US point-in-time S&P 500 members (Sharadar, incl. delisted); SF1 quarterly filings usable from their filing date, at most 200 days old |
| Checklist | TTM profit > 0 now and a year ago, ROE ≥ 15%; revenue and profit up on a year ago; debt/equity ≤ 1; free cash flow > 0 and share count up ≤ 2% |
| Portfolio | 12 stocks, equal weight, highest free-cash-flow yield among qualifiers; annual review each December; held buy-and-hold between reviews; incumbents kept while they qualify and rank in the top 24 |
| Costs | FS16 model at $10m: liquidity-dependent half-spread + square-root impact (Y = 0.7) on every trade |
| Primary test | CAPM alpha vs the size-weighted S&P 500 members, Newey–West t > 2, and positive alpha in both 2013–19 and 2020–26 |

> **In one paragraph.** **Not passed.** The 12-stock checklist portfolio compounded **11.7% a year** net of costs against **15.0%** for the size-weighted market and 12.5% for the equal-weight universe. Its CAPM alpha is **-0.6% a year (t -0.24)**, negative in both halves (-0.4% in 2013–19, -2.9% in 2020–26). **None of the 12 pre-registered variants passes; all but one have a negative alpha.** The portfolio is not bad: it earns roughly the market's return with a beta below one and held up better in 2022 (−7% vs −19%). But once the market is accounted for, the checklist adds nothing, and against the six JKP themes it is a **value tilt** (loading +0.76, t 3.9) with no alpha left (-1.3%, t -0.55). The lesson is the one the factor literature keeps teaching: a sensible checklist of good-company traits describes known factors, and in 2013–26 value was the wrong factor to own.

![FS20](../figures/fs20_checklist.png)

## 1. Headline performance (primary variant)

| Portfolio | CAGR | Volatility | Sharpe (excess of T-bills) [95% CI] | Max drawdown |
|---|---|---|---|---|
| Checklist, 12 stocks (net) | 11.7% | 16.6% | 0.64 [0.25, 1.07] | -22% |
| US market, size-weighted | 15.0% | 14.2% | 0.93 | -24% |
| Equal-weight S&P 500 members | 12.5% | 15.5% | 0.72 | -28% |


*Monthly returns, Jan 2013 – Sep 2026 (165 months). Sharpe confidence interval from a stationary block bootstrap (mean block 6 months, 5,000 draws). Trading costs average 0.17% a year; turnover is 75% of the book per annual review.*

## 2. Statistical verdict

| Test | Result | Bar | Verdict |
|---|---|---|---|
| CAPM alpha, full sample | -0.6% / yr, t -0.24, beta 0.84 | t > 2 | fail |
| Alpha 2013–19 | -0.4% (t -0.13), beta 1.10 | > 0 | fail |
| Alpha 2020–26 | -2.9% (t -0.92), beta 0.73 | > 0 | fail |
| Return minus market (not beta-adjusted) | -2.6% / yr, t -1.14 | reported | — |
| Probabilistic Sharpe ratio > 0 | 0.989 | reported | — |

## 3. All 12 pre-registered variants

| Variant | CAPM alpha / yr | t | Beta | Alpha 2013–19 | Alpha 2020–26 | CAGR | Sharpe | Cost / yr | Turnover per review | Passes |
|---|---|---|---|---|---|---|---|---|---|---|
| **12 stocks · annual · FCF yield** (primary) | -0.6% | -0.24 | 0.84 | -0.4% | -2.9% | 11.7% | 0.64 | 0.17% | 75% | no |
| 25 stocks · annual · FCF yield | -1.1% | -0.53 | 0.93 | -1.6% | -2.1% | 12.5% | 0.72 | 0.12% | 70% | no |
| 50 stocks · annual · FCF yield | -0.8% | -0.56 | 0.96 | -0.1% | -2.1% | 13.4% | 0.80 | 0.08% | 57% | no |
| 12 stocks · quarterly · FCF yield | -0.4% | -0.14 | 0.90 | -0.4% | -2.2% | 12.5% | 0.66 | 0.33% | 37% | no |
| 25 stocks · quarterly · FCF yield | -2.1% | -1.04 | 0.96 | -2.8% | -3.0% | 11.7% | 0.65 | 0.23% | 33% | no |
| 50 stocks · quarterly · FCF yield | -2.3% | -1.82 | 0.99 | -1.6% | -3.7% | 12.0% | 0.70 | 0.15% | 27% | no |
| 12 stocks · annual · earnings yield | -2.5% | -1.10 | 0.99 | -2.5% | -3.2% | 11.5% | 0.59 | 0.17% | 78% | no |
| 25 stocks · annual · earnings yield | -3.6% | -2.03 | 1.00 | -2.1% | -6.1% | 10.5% | 0.58 | 0.12% | 73% | no |
| 50 stocks · annual · earnings yield | -1.7% | -1.62 | 0.99 | -1.5% | -2.5% | 12.7% | 0.74 | 0.08% | 61% | no |
| 12 stocks · quarterly · earnings yield | -0.7% | -0.29 | 1.02 | +0.3% | -2.8% | 13.6% | 0.67 | 0.36% | 41% | no |
| 25 stocks · quarterly · earnings yield | -3.7% | -1.97 | 1.01 | -2.9% | -5.7% | 10.6% | 0.57 | 0.24% | 35% | no |
| 50 stocks · quarterly · earnings yield | -2.5% | -2.06 | 1.00 | -2.9% | -2.7% | 11.9% | 0.69 | 0.15% | 28% | no |


*Every variant was fixed in the pre-registration and every one enters the trial ledger. No variant is chosen after the fact. Bigger books (25 or 50 stocks) look more like the market and have alphas closer to zero; quarterly reviews and earnings-yield ranking do slightly worse.*

## 4. Calendar years

| Year | Checklist (net) | Market | Equal weight | Checklist − market |
|---|---|---|---|---|
| 2013 | +34.5% | +32.5% | +36.4% | +2.1% |
| 2014 | +26.5% | +13.7% | +14.4% | +12.8% |
| 2015 | +10.2% | +1.5% | -2.3% | +8.7% |
| 2016 | +15.3% | +11.8% | +15.2% | +3.5% |
| 2017 | +9.4% | +22.1% | +18.6% | -12.7% |
| 2018 | -10.3% | -4.4% | -7.7% | -5.9% |
| 2019 | +27.9% | +31.3% | +30.2% | -3.5% |
| 2020 | +12.2% | +18.8% | +11.8% | -6.6% |
| 2021 | +24.3% | +28.3% | +29.8% | -4.0% |
| 2022 | -11.1% | -18.2% | -11.3% | +7.1% |
| 2023 | +3.5% | +26.5% | +14.4% | -23.1% |
| 2024 | +12.0% | +25.6% | +12.6% | -13.6% |
| 2025 | +12.4% | +17.9% | +11.4% | -5.4% |
| 2026 | +4.2% | +12.1% | +9.1% | -7.9% |


*2026 is January to 25 September.*

The checklist beat the market in 2014, 2015, 2019 and 2022, all years when cheap, cash-generating companies did well, and lagged in 2017, 2018, 2020 and 2023–25, when the market was led by expensive growth and mega-cap technology stocks the checklist rarely buys (they fail the free-cash-flow-yield ranking even when they pass the quality tests).

## 5. What the checklist really buys: factor attribution

Regression of monthly excess returns on the market and six JKP US themes (equal-weight mean of each theme's signed factor legs; 2013-01 to 2025-12, 156 months; Newey–West, 6 lags).

| Factor | Loading | t | Equal-weight universe, loading |
|---|---|---|---|
| MKT | +0.95 | +11.5 | +0.98 |
| Value | +0.76 | +3.9 | +0.33 |
| Profitability | -0.69 | -2.2 | -0.12 |
| Quality | +0.76 | +2.4 | -0.35 |
| Investment | -0.39 | -1.5 | -0.32 |
| Momentum | +0.01 | +0.1 | +0.02 |
| Low risk | +0.02 | +0.2 | +0.03 |


*Alpha after the six themes: **-1.3% a year (t -0.55)**, R² 0.69. Themes: Value (book, earnings, cash-flow and sales yields), Profitability, Quality (QMJ, O-score, Z-score), Investment (low asset and capex growth), Momentum, Low risk.*

The strongest loading is **value**. Profitability and investment load *negatively* once value and the market are in the model: among stocks that are already cheap on free cash flow, the checklist ends up holding firms whose broader profitability and investment profile looks worse than the JKP long legs. The quality screens (ROE, growth, low debt) do their job as filters, but the free-cash-flow-yield ranking decides what is bought, and that makes it a value portfolio.

## 6. What it held

On average **81 of 500** stocks passed all four tests at a review (range 52–113). Average pass rates per test: profit 45%, growth 49%, debt 58%, management proxy 81%. Only 2.6 of 12 holdings are kept at a typical review, so "hold for years" does not happen mechanically: the FCF-yield ranking churns.

| Review (December) | Qualifiers | Kept | The 12 holdings |
|---|---|---|---|
| 2012 | 94 | 0 | AFL, STX, CF, CA1, DGX, CSCO, ORLY, GEN, TSS, GAP, AET, LH |
| 2013 | 85 | 2 | CSCO, GAP, PHM, PGR, HUM, ORCL, LLY, MSFT, MDT, GPC, FFIV, LOW |
| 2014 | 93 | 1 | PGR, LYB, MPC, EXPE, BCR, WDC, AAPL, SNDK1, DAL, EW, GILD, ANDV |
| 2015 | 63 | 2 | PGR, AAPL, AMG, FFIV, CPRI, CSCO, CMI, GPC, INTC, TROW, CHRW, CAH |
| 2016 | 67 | 2 | FFIV, CAH, MCK, BBY, DRI, UNH, ALK, UHS, TT, IPG, CTXS, SIG |
| 2017 | 74 | 5 | FFIV, MCK, BBY, DRI, UNH, PGR, RCL, CI, LRCX, GAP, TAP, SWKS |
| 2018 | 105 | 2 | PGR, LRCX, MU, AMG, PHM, ALL, M, WRK, GL, KSS, CPRI, LYB |
| 2019 | 71 | 2 | PGR, PHM, SCHW, AMP, ETFC, BIIB, CMI, CTRA, TTWO, HUM, COP, CSCO |
| 2020 | 52 | 4 | PGR, PHM, TTWO, HUM, ALL, INTC, DGX, CBRE, UNH, PNR, WMT, FBIN |
| 2021 | 113 | 2 | PHM, DGX, RJF, SYF, COF, WRB, HOLX, CINF, FOXA, WY, LH, AIZ |
| 2022 | 86 | 1 | WRB, CF, NUE, STLD, CTRA, PFG, MOS, FANG, HUM, PXD, COP, CVX |
| 2023 | 59 | 2 | WRB, HUM, ZION, ACGL, HIG, PHM, GL, MOH, PGR, CSCO, CMI, MCHP |
| 2024 | 81 | 6 | WRB, ACGL, HIG, PHM, GL, PGR, SYF, EG, TRV, CB, CINF, LEN |
| 2025 | 85 | 6 | WRB, HIG, GL, PGR, SYF, TRV, ALL, CF, AMP, PYPL, FOXA, RJF |


About 29% of holdings over the whole period, and 67% in the last three reviews, are insurers, brokers and card lenders (e.g. PGR, WRB, HIG, SYF). Free cash flow and debt/equity mean something different for financial firms, so the proxy drifts toward an insurance portfolio. The pre-registration did not exclude financials; this is reported here as a caveat, not fixed.

## 7. Caveats

- **Proxy, not the person.** The discretionary parts of the checklist (management quality, moat, intrinsic value) are replaced by crude accounting rules. A skilled human applying the same checklist can do better or worse. Nothing here measures Beile Grünbaum's or any other named investor's results.
- **Financials.** Free-cash-flow yield and debt/equity are poor measures for insurers and banks; a real value investor would treat them separately (§6).
- **Sample.** US large caps, 2013–26, one period dominated by expensive growth stocks; there is no out-of-sample period. Value has had one of its worst decades in this window, which works against any cheapness-ranked checklist.
- **Delistings.** A holding that stops trading is held as cash (0% return) until the next review; its last delisting return may be missing.
- **Costs** use the FS16 literature parameters at $10m; they are small here (0.17% a year) because the book trades once a year.
- **T-bill rate** after July 2026 carries the last French value forward.
- FS20 adds 12 trials to the programme ledger.

## 8. References

- Buffett, W. E. (various). Berkshire Hathaway shareholder letters.
- Grünbaum Value Invest (2024). *Investeringsstrategi*. Public description of the checklist that this proxy imitates.
- Frazzini, A., Kabiller, D. & Pedersen, L. H. (2018). Buffett's alpha. *Financial Analysts Journal* 74(4), 35–55.
- Asness, C. S., Frazzini, A. & Pedersen, L. H. (2019). Quality minus junk. *Review of Accounting Studies* 24(1), 34–112.
- Novy-Marx, R. (2013). The other side of value: the gross profitability premium. *Journal of Financial Economics* 108(1), 1–28.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Fama, E. F. & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics* 116(1), 1–22.

## 9. Reproduce

`planning/PREREG_FS20.md` → `code/fs20.py` (→ `results/fs20.json`, `fs20.pkl`) → `code/build_fs20.py`. Data: Sharadar `us_fundamentals.csv` and `us_master_universe_prices.csv` (licensed, not published; set `P10_DATA`), `US_tradedvalue.parquet` (`P10_PIT`), French US 5-factor daily and JKP US factors (`P10_FACTORS`).
