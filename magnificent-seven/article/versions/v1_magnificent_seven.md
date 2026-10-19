# The Magnificent Seven: does concentration come back to bite?

### Ten stocks, two-fifths of the market, and the lore that the giants always fall

![Now Showing](../figures/hero_magnificent_seven.png)

*Henrik Gjerning · Rude Investment Consulting · September 2026 · Project 10, article A03*

<!-- interval:guess -->
> **The Interval · guess before you read on.** Since 2012, did the 10 largest US stocks beat the other 490 over the following year? A) They lagged, as the lore says · B) About even · C) They beat them. *The answer is in the next paragraph.*
<!-- /interval -->

> **In one paragraph.** In February 2012 the ten largest US companies made up **21%** of the 500 largest. By August 2026 they made up **39%**, and the single largest, NVIDIA, weighed 7.6% on its own. Market lore says this ends badly: the biggest stocks lag, and when concentration peaks the average stock catches up. I pre-registered both claims and tested them on every month since 2012. **Both failed.** The then-top-10 beat the other 490 by **+5.7%** per 12 months on average (t +2.07, the wrong sign for the lore). Rising concentration did not predict an equal-weight catch-up (t 0.72). Of the $70 trillion of net wealth these stocks created, **39% came from just ten names.**

**Statistics box.** Monthly market cap = latest Sharadar filing, scaled by the price move since filing; top 500 each month-end, Feb 2012 → Aug 2026. Twelve-month buy-and-hold, cap-weighted portfolios; overlapping monthly observations; Newey-West (12 lags) and a stationary bootstrap (mean block 12, 10,000 draws). Two trials, one-sided gate p < 0.025. **Both failed.** Price returns (no dividends).

---

## 1. Why this matters now

Index investors today hold a portfolio in which ten names carry nearly two-fifths of the weight. That is a large bet on a few business models (chips, cloud, advertising, devices), and it has prompted a stream of warnings. The historical case rests on two ideas: large firms find it harder to grow (the size effect of Banz 1981), and extreme leadership in the past, such as the Nifty Fifty in the 1970s and the telecoms and tech leaders of 2000, ended in underperformance. The first lesson of Bessembinder (2018) is the opposite: most of the stock market's wealth is created by a handful of stocks, and they are not easy to replace.

## 2. How concentrated is it?

![Figure 1](../figures/fig1_concentration.png)

The top-10 share was flat at around a fifth until 2016 (17% at its low). It then roughly doubled, peaking at **41.0% in October 2025**. The line-up changed almost completely:

- **2012:** AAPL, XOM, MSFT, IBM, CVX, GE, GOOGL, BRK.B, PG, T
- **2026:** NVDA, AAPL, GOOGL, MSFT, AMZN, AVGO, META, TSLA, LLY, MU

Yet month to month the top 10 is sticky: on average only 1.4 names change per year.

## 3. The pre-registered trials

**Table 1. Results**

| Trial | Hypothesis | Estimate | NW t (12 lags) | p (one-sided) | Bootstrap p | Gate | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| A03-1 | The ten largest underperform the other 490 over the next 12 months | **+5.7%** per 12m | +2.07 | 0.981 | 0.987 | 0.025 | fail (opposite sign) |
| A03-2 | Rising concentration predicts an equal-weight catch-up | slope **+0.32**, R² 0.03 | 0.72 | 0.237 | 0.251 | 0.025 | fail |

> **Corrected universe (re-run 1 October 2026).** On the actual S&P 500 members at each date, instead of every company that was ever in the index in 2012–2026, the result barely moves: A03-1 +6.2% a year, t 2.11 (published +5.7%, t 2.07); A03-2 slope 0.43, t 0.70 (published 0.32, t 0.72). The concentration measures are unchanged to the first decimal. Verdicts as registered: 0 of 2. Details: `rerun_comparison.csv`.

![Figure 2](../figures/fig2_top_dog_spread.png)

The giants beat the rest over the following year in **66%** of start months. The average lead was +5.7% per 12 months (median +4.6%). The "top dog" lore did not just fail to show up: it ran the other way.

The catch-up test fared no better. Equal-weight minus cap-weight averaged -0.9% per 12 months, and the prior change in concentration explained 3% of its variation. With about 14 independent years of data, this test was always going to be weak. I said so in the pre-registration.

**Table 2. Year by year (descriptive)**

| Year-end | Top-10 share | Mean next-12m spread, top 10 − rest (start months in year) | Mean next-12m EW − CW |
|---|---:|---:|---:|
| 2012 | 19.0% | -16.1% | +3.9% |
| 2013 | 17.9% | -0.8% | +1.6% |
| 2014 | 17.7% | -1.8% | +0.7% |
| 2015 | 19.0% | +4.5% | -0.8% |
| 2016 | 19.2% | +5.5% | -0.4% |
| 2017 | 21.1% | +12.5% | -1.8% |
| 2018 | 22.4% | +2.5% | -0.7% |
| 2019 | 24.3% | +27.9% | -6.6% |
| 2020 | 28.7% | +3.9% | +4.4% |
| 2021 | 30.3% | -5.5% | +2.5% |
| 2022 | 25.2% | +3.1% | -3.3% |
| 2023 | 32.0% | +21.8% | -6.7% |
| 2024 | 38.0% | +13.1% | -4.8% |
| 2025 | 40.5% | +8.6% | +0.1% |
| 2026 | 39.3% | n/a | n/a |

## 4. Where the wealth came from

![Figure 3](../figures/fig3_wealth_creation.png)

Following Bessembinder (2018), I summed each stock's monthly dollar gains (last month's market cap × this month's return) from 2012 to 2026, across 792 names that were in the S&P 500 at some point.

- Net wealth created: **$70 trillion** (price only).
- The top 10 creators: **39%**. The top 2% (16 names): **47%**.
- 12% of the names destroyed wealth over the period; the largest losses were in NBL, NOV, CHKAQ, APA, KHC.

**Table 3. The ten biggest wealth creators, 2012–2026**

| Rank | Ticker | Net wealth created, $ tn |
|---:|---|---:|
| 1 | NVDA | 5.42 |
| 2 | AAPL | 5.20 |
| 3 | GOOGL | 4.12 |
| 4 | MSFT | 3.85 |
| 5 | AMZN | 2.53 |
| 6 | AVGO | 1.71 |
| 7 | META | 1.46 |
| 8 | LLY | 1.12 |
| 9 | JPM | 1.10 |
| 10 | MU | 1.07 |

## 5. What this does and does not show

- **One regime, one sample.** 2012–2026 is the era of the platform giants. The lore is built on the 1970s and 2000. Fourteen years of data cannot overturn it; they only show that it did not work *here*.
- **Survivor-list bias favours winners.** The ticker list holds every name that was ever in the S&P 500 during 2012–2026. Firms added after big gains are in the sample earlier than an index investor would have held them. This inflates the "rest" as well as the top, so the spread is less affected than the levels. Re-running on the actual members at each date (box under Table 1) moves the spread by half a percentage point.
- **Price returns only.** The 2012 top 10 paid higher dividends than the 2026 top 10. Including dividends would narrow the spread in the early years.
- **Two trials, both failed.** Programme total now 32.

<!-- interval:joke -->
> **Interval.** Market lore says the giants always fall. Fourteen years on, the lore is still waiting at the saloon.
<!-- /interval -->

## 6. Verdict

The lore that "the biggest stocks always lag" was not a law in this sample; it was a coin that came up the other way two-thirds of the time. Concentration at two-fifths is a risk to be sized, not a timing signal. The strongest evidence here is Bessembinder's: a small number of companies create most of the wealth, and an index fund is the cheapest way not to miss them. The price is holding a portfolio that looks more like a sector bet every year.

<!-- research -->
## What I would research next

**Not researched here**

- The 1970s Nifty Fifty and the 2000 tech peak, where the lore comes from.
- Other countries with high concentration (e.g. Denmark, Switzerland, Taiwan).

**With more or better data**

- Total returns with dividends for the whole period.
- A long history of index weights before 2012.

**With better analysis**

- Test concentration as a risk measure (drawdown, tracking error) instead of a return-timing signal.
- Re-run on the actual index members throughout as the main test, not a robustness box.
<!-- /research -->

## Reproduce

```bash
python code/run_concentration.py   # A03-1..2 + reported, results/summary.json
python code/make_figures.py && python code/build_article.py
```

## References

- Banz, R. W. (1981). The relationship between return and market value of common stocks. *Journal of Financial Economics*, 9(1).
- Bessembinder, H. (2018). Do stocks outperform Treasury bills? *Journal of Financial Economics*, 129(3).
- Bessembinder, H., Chen, T.-F., Choi, G. & Wei, K. C. J. (2023). Long-term shareholder returns: evidence from 64,000 global stocks. *Financial Analysts Journal*, 79(3).
- Fama, E. F. & French, K. R. (1992). The cross-section of expected stock returns. *Journal of Finance*, 47(2).
- Newey, W. K. & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3).
- Politis, D. N. & Romano, J. P. (1994). The stationary bootstrap. *Journal of the American Statistical Association*, 89(428).

*Not investment advice. Film title used as a cultural reference only.*
