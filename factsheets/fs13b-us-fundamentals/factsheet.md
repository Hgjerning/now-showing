# FACTSHEET FS13b · US fundamentals, stock by stock

### Do the published fundamental themes work in our own US engine?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

> **US, 1999–2012 (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time S&P
> 500 with delisted stocks, 1999–2012, a period this factsheet was not built on. 15 of 20 fundamental signals keep their
> long-only sign (the pass mark was 15): passes exactly at the bar, and the six composites are built from the fourteen
> single signals, so this is weaker evidence than 20 independent tests. Profit growth, this factsheet's strongest US
> result: t +0.76 (2013–2026: +3.42). Pre-registration, method and every result: `PREREG_US_1999_2012.md`.



| Key facts | |
|---|---|
| Universe | US, point-in-time S&P 500 members (Sharadar), monthly, Feb 2013 – Aug 2026 |
| Data | Sharadar SF1 as-reported quarterly filings (ARQ), used from the filing date; a filing older than 200 days is dropped |
| Signals | 14 fundamental signals in 6 themes (debt issuance, profit growth, value, profitability, investment, accruals) plus one composite per theme |
| Books | top-minus-bottom decile, equal weight; long/short, beta-neutral long/short, long-only vs the equal-weight universe |
| Costs | 10 bp per side, size-tiered borrow fee on the short leg, financing of net long cash (USD risk-free + 0.5%) |
| Checks | correlation with the matching JKP US factor; spanning by the price shortlist (low beta, momentum, residual momentum, 52-week high) |

> **In one paragraph.** FS13 found that the published JKP factors put **debt issuance** and **profit growth** on common ground in every segment. Built stock by stock in our US universe, **profit growth** holds up: the composite earns +9.3% a year beta-neutral (t 3.0), its long-only book beats the equal-weight universe after beta (alpha t 3.4), it is positive in both the 2013–19 design and the 2020–26 holdout window, and it keeps an alpha of +9.7% (t 3.9) after the price shortlist. **Debt issuance** is weaker here: +4.1% a year long/short (t 1.9), mostly carried by the long side (long-only alpha t 2.5). **Value** (-9.8%, t -1.8) and **investment** (-8.7% beta-neutral, t -2.8) lost money in US large caps since 2013, matching JKP's "faded in the US". Our books track the published JKP US themes closely for value, profit growth and investment (correlation 0.69–0.86) and more loosely for debt issuance, profitability and accruals (0.43–0.61), where SF1's aggregated lines differ from JKP's inputs. Profit growth and investment are strongly opposed (correlation -0.65): growing firms improve their profits and also grow their assets.

![Signals](../figures/fs13b_signals.png)

## 1. Data and point-in-time rules

Sharadar SF1, dimension ARQ: each quarterly report as first filed, with its filing date. At every month-end a stock carries the latest filing dated on or before that day; filings older than 200 days are dropped, so a stock that stops reporting drops out. Flows (revenue, net income, gross profit, operating income, operating cash flow) are summed over the last four quarters where a level ratio needs a year; four-quarter changes require the earlier quarter to be 330–400 days back. Market capitalisation is the month-end value from the same source used for the universe. Every signal is winsorised at the 1st and 99th percentile each month. Coverage: about 620–650 of the ~800 stocks that are ever S&P 500 members have a value in a typical month; the sort uses the stocks that are S&P 500 members that month.

## 2. Definitions

| Signal | Theme | Long the | Code | JKP match |
|---|---|---|---|---|
| Debt growth | Debt issuance | low | `dbt_gr` | `debt_gr3` |
| Net operating assets | Debt issuance | low | `noa_at` | `noa_at` |
| Net financial asset growth | Debt issuance | high | `nfna_gr` | `nfna_gr1a` |
| Sales surprise | Profit growth | high | `sale_su` | `saleq_su` |
| Earnings change / equity | Profit growth | high | `ni_be_ch` | `niq_be_chg1` |
| Earnings change / assets | Profit growth | high | `ni_at_ch` | `niq_at_chg1` |
| Book-to-market | Value | high | `bm` | `be_me` |
| Earnings yield | Value | high | `ep` | `ni_me` |
| Cash-flow yield | Value | high | `cfp` | `ocf_me` |
| Gross profitability | Profitability | high | `gp_at` | `gp_at` |
| Operating profitability | Profitability | high | `op_be` | `ope_be` |
| Asset growth | Investment | low | `at_gr` | `at_gr1` |
| Capex growth | Investment | low | `capx_gr` | `capx_gr1` |
| Accruals | Accruals | low | `acc_at` | `oaccruals_at` |


*Composites average the members' percentile ranks, each signed so that high means good. Definitions follow JKP (Jensen, Kelly & Pedersen 2023) where SF1 has the inputs; net operating assets, net financial assets and the debt measures use SF1's aggregate balance-sheet lines, so they are approximations.*

## 3. Results

| Signal | L/S net / yr | Beta-neutral net / yr | Long-only alpha t | Beta-neutral Sharpe 2013–19 / 2020–26 | Cost / yr | Correlation with JKP US |
|---|---|---|---|---|---|---|
| Debt growth | -2.9% (t -1.2) | -3.6% (t -1.6) | +0.4 | -0.73 / -0.13 | +0.7% | 0.43 |
| Net operating assets | +5.3% (t +1.7) | +2.3% (t +0.8) | +0.9 | +0.28 / +0.58 | +0.2% | 0.31 |
| Net financial asset growth | -0.3% (t -0.2) | -1.1% (t -0.6) | +2.2 | -0.09 / -0.01 | +0.8% | -0.10 |
| **Debt issuance (composite)** | +4.1% (t +1.9) | +1.7% (t +0.8) | +2.5 | +0.30 / +0.64 | +0.7% | 0.61 |
| Sales surprise | +0.8% (t +0.1) | +5.1% (t +0.9) | +1.6 | +0.62 / -0.25 | +0.8% | 0.40 |
| Earnings change / equity | +4.4% (t +1.7) | +6.4% (t +2.2) | +2.0 | -0.13 / +0.57 | +1.2% | 0.54 |
| Earnings change / assets | +5.6% (t +2.0) | +7.2% (t +2.4) | +1.9 | -0.18 / +0.71 | +1.3% | 0.58 |
| **Profit growth (composite)** | +6.7% (t +1.5) | +9.3% (t +3.0) | +3.4 | +0.50 / +0.42 | +1.1% | 0.74 |
| Book-to-market | -8.1% (t -1.4) | -13.8% (t -2.8) | -2.6 | -0.90 / +0.02 | +0.4% | 0.82 |
| Earnings yield | -7.2% (t -1.5) | -2.4% (t -0.9) | -2.2 | -0.29 / -0.52 | +0.5% | 0.49 |
| Cash-flow yield | -6.2% (t -1.2) | -6.7% (t -1.7) | -2.0 | -0.77 / +0.04 | +0.5% | 0.71 |
| **Value (composite)** | -9.8% (t -1.8) | -11.1% (t -2.3) | -1.7 | -0.88 / -0.28 | +0.5% | 0.86 |
| Gross profitability | -0.5% (t -0.1) | +5.9% (t +1.3) | +0.7 | +0.08 / -0.11 | +0.2% | 0.75 |
| Operating profitability | -6.1% (t -1.1) | +1.1% (t +0.3) | +1.3 | +0.02 / -0.54 | +0.3% | 0.49 |
| **Profitability (composite)** | -0.7% (t -0.2) | +4.9% (t +1.4) | +0.7 | +0.37 / -0.34 | +0.3% | 0.45 |
| Asset growth | -6.5% (t -1.2) | -9.1% (t -2.2) | -1.6 | -0.81 / -0.14 | +0.6% | 0.60 |
| Capex growth | -0.8% (t -0.4) | -3.5% (t -1.9) | -0.5 | -0.37 / +0.12 | +1.2% | 0.35 |
| **Investment (composite)** | -5.8% (t -1.4) | -8.7% (t -2.8) | -1.8 | -0.81 / -0.14 | +0.9% | 0.69 |
| Accruals | +4.8% (t +1.0) | +1.7% (t +0.5) | +0.4 | +0.00 / +0.45 | +0.5% | 0.49 |
| **Accruals (composite)** | +4.8% (t +1.0) | +1.7% (t +0.5) | +0.4 | +0.00 / +0.45 | +0.5% | 0.43 |


*Monthly, Feb 2013 – Aug 2026, USD. Newey–West t (6 lags). Long-only alpha: CAPM against the equal-weight universe. JKP correlation: our gross long/short against the matching JKP US factor (theme average for composites), Feb 2013 – Dec 2025.*

![Themes](../figures/fs13b_themes.png)

**Reading it.**

1. **Profit growth is the one theme that works on every test.** Earnings changes scaled by assets or equity carry it; the sales surprise adds little on its own.
2. **Debt issuance works mainly on the long side.** Firms that shrink debt and net operating assets beat the universe, but the short leg (firms raising debt) is not reliably bad in large caps, so the beta-neutral book is flat.
3. **Value and investment lost** in the growth-led US market of 2013–2026. Book-to-market has the highest replication with JKP (0.82), so this is the premium, not the code.
4. **Profitability** is positive once beta-neutral but not significant; **accruals** are positive and weak.
5. Themes that are positive in both the design and the holdout window: Debt issuance, Profit growth, Accruals.

## 4. Against the published factors

| Theme | JKP US Sharpe before 2013 | JKP US Sharpe 2013–25 | Our beta-neutral Sharpe 2013–26 | Correlation of our L/S with JKP |
|---|---|---|---|---|
| Debt issuance | +1.07 | +0.43 | +0.19 | 0.61 |
| Profit growth | +0.44 | +0.34 | +0.74 | 0.74 |
| Value | +0.29 | +0.15 | -0.65 | 0.86 |
| Profitability | +0.29 | +0.31 | +0.39 | 0.45 |
| Investment | +0.42 | +0.12 | -0.77 | 0.69 |
| Accruals | +0.76 | +0.03 | +0.13 | 0.43 |


Both sources agree that profit growth kept working after 2013. JKP shows investment and accruals fading in the US; in our large-cap books value and investment went further and lost money. JKP's debt issuance is stronger than ours, partly because its definitions use detailed financing lines that SF1 aggregates.

## 5. Do they add anything to the price signals?

| Composite | Beta-neutral return / yr | Alpha after the price shortlist (t) | R² on the price shortlist | Closest price signals (correlation) |
|---|---|---|---|---|
| Debt issuance (composite) | +1.7% | +2.6% (t +1.4) | 0.33 | beta -0.49, vol252 -0.37, vol -0.29 |
| Profit growth (composite) | +9.3% | +9.7% (t +3.9) | 0.50 | size -0.67, mom +0.65, hi52 +0.57 |
| Value (composite) | -11.1% | -10.0% (t -2.2) | 0.31 | size +0.62, mom -0.54, lo52 -0.51 |
| Profitability (composite) | +4.9% | +6.1% (t +1.7) | 0.37 | size -0.62, hi52 +0.51, min5 +0.48 |
| Investment (composite) | -8.7% | -8.7% (t -2.9) | 0.26 | size +0.64, mom -0.45, hi52 -0.40 |
| Accruals (composite) | +1.7% | -0.0% (t -0.0) | 0.21 | ivol -0.48, hi52 -0.42, vol252 -0.41 |


*Regression of each beta-neutral composite on the beta-neutral low-beta, 12-1 momentum, residual momentum and 52-week-high books (FS13), Newey–West t.*

Profit growth keeps most of its return after the price signals: it is related to momentum (firms with rising earnings tend to have rising prices) but not explained by it. This makes it the strongest candidate to add to the multifactor model.

## 6. How the themes relate

|  | Debt issuance | Profit growth | Value | Profitability | Investment | Accruals |
|---|---|---|---|---|---|---|
| Debt issuance | +1.00 | +0.14 | -0.01 | -0.01 | +0.05 | +0.15 |
| Profit growth | +0.14 | +1.00 | -0.55 | +0.52 | -0.65 | -0.31 |
| Value | -0.01 | -0.55 | +1.00 | -0.52 | +0.69 | +0.19 |
| Profitability | -0.01 | +0.52 | -0.52 | +1.00 | -0.59 | -0.46 |
| Investment | +0.05 | -0.65 | +0.69 | -0.59 | +1.00 | +0.52 |
| Accruals | +0.15 | -0.31 | +0.19 | -0.46 | +0.52 | +1.00 |


*Correlation of the beta-neutral theme composites, monthly.*

## 7. What goes into the multifactor model (FS14)

- **Add:** the profit-growth composite; debt issuance as a long-side tilt.
- **Keep as diversifiers, not as return sources:** profitability (low correlation with momentum), value (negatively correlated with profit growth and momentum, so it may pay in the next reversal but has cost money since 2013).
- **Leave out:** investment and accruals on their own; their information is largely inside profit growth and value.
- All of this is US only. For the other five markets, JKP factor returns remain the only fundamental source until a global fundamentals feed is added (FS00).

## 8. Caveats

- **Financials are included**; ratios such as gross profitability and net operating assets mean little for banks and insurers. A sector filter needs industry codes (FS00 gap).
- **US only**, S&P 500 members, equal weight; JKP is value-weighted over the whole market.
- **Aggregated balance-sheet lines** make the debt-issuance measures approximate (JKP correlation -0.10–0.43).
- **Multiple testing.** 20 signals × three books add 60 trials to the factsheet ledger, now 682 in all. Programme-wide, 1 of the 60 survives the Benjamini–Hochberg correction: Profit growth (composite) (long-only alpha vs EW, US); its deflated Sharpe ratio is 0.56 on the lenient bound, below the 0.95 bar (`planning/FACTSHEET_TRIAL_LEDGER.md`).

## 9. References

- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Novy-Marx, R. (2013). The other side of value: the gross profitability premium. *Journal of Financial Economics* 108(1), 1–28.
- Fama, E. F. & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics* 116(1), 1–22.
- Cooper, M. J., Gulen, H. & Schill, M. J. (2008). Asset growth and the cross-section of stock returns. *Journal of Finance* 63(4), 1609–1651.
- Hirshleifer, D., Hou, K., Teoh, S. H. & Zhang, Y. (2004). Do investors overvalue firms with bloated balance sheets? *Journal of Accounting and Economics* 38, 297–331.
- Richardson, S. A., Sloan, R. G., Soliman, M. T. & Tuna, I. (2005). Accrual reliability, earnings persistence and stock prices. *Journal of Accounting and Economics* 39(3), 437–485.
- Jegadeesh, N. & Livnat, J. (2006). Revenue surprises and stock returns. *Journal of Accounting and Economics* 41(1–2), 147–171.
- Sloan, R. G. (1996). Do stock prices fully reflect information in accruals and cash flows about future earnings? *The Accounting Review* 71(3), 289–315.
- Fama, E. F. & French, K. R. (1992). The cross-section of expected stock returns. *Journal of Finance* 47(2), 427–465.
- Basu, S. (1977). Investment performance of common stocks in relation to their price-earnings ratios. *Journal of Finance* 32(3), 663–682.

## 10. Reproduce

`code/fundamentals.py` (point-in-time signals from `us_fundamentals.csv`, licensed, not published) → `code/fund_battery.py` (engine, replication, spanning → `results/fund_battery.json`) → `code/build_fs13b.py`.
