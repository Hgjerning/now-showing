# The Magnificent Seven: does concentration come back to bite?

### Ten stocks, two-fifths of the market, and the lore that the giants always fall

![Now Showing](../figures/hero_magnificent_seven.png)

*Henrik Gjerning · Rude Investment Consulting · September 2026 · Project 10, article A03*

*Revised 8 October 2026 after external review (v2).*

> **In one paragraph.** In February 2012 the ten largest US companies made up **21%** of the 500 largest. By August 2026 they made up **39%**, and NVIDIA alone weighed 7.6%. Market lore says this ends badly: the biggest stocks lag, and when concentration peaks the average stock catches up. I pre-registered both claims and tested them on every month since 2012. **Neither showed up.** The then-top-10 *beat* the other 490 by **+5.7%** per 12 months on average (t +2.07), the opposite of the lore, although most of that lead came after 2019. Rising concentration did not predict an equal-weight catch-up (t 0.72), but that test had little power. Meanwhile wealth creation was extremely lopsided: of the $70 trillion these stocks added, **39% came from just ten names**, 1.3% of the 792. The evidence argues against using concentration as a timing signal. It does not show that concentration is harmless.

**Statistics box.** Monthly market cap = latest Sharadar filing, scaled by the price move since filing; top 500 each month-end, Feb 2012 → Aug 2026. Twelve-month buy-and-hold, cap-weighted portfolios; 163 overlapping monthly start dates (about 14 independent years); Newey-West (12 lags) and a stationary bootstrap (mean block 12, 10,000 draws). Two trials, one-sided gate p < 0.025. **Both failed.** Price returns only (no dividends). US large caps, one market era.

---

## 1. Why this matters now

Index investors now hold a portfolio in which ten names carry nearly two-fifths of the weight: a large bet on a few business models (chips, cloud, advertising, devices). The warnings rest on two ideas. Large firms find it harder to grow (the size effect of Banz 1981; Fama & French 1992), and past episodes of extreme leadership, such as the Nifty Fifty in the 1970s and the tech and telecom leaders of 2000, ended in underperformance. Against that stands Bessembinder (2018): most of the stock market's wealth is created by a handful of stocks, and they are hard to replace.

## 2. How concentrated is it?

![Figure 1](../figures/fig1_concentration.png)

The top-10 share hovered around a fifth until 2016 (17% at its low), then roughly doubled, peaking at **41.0% in October 2025**. The line-up changed almost completely:

- **2012:** AAPL, XOM, MSFT, IBM, CVX, GE, GOOGL, BRK.B, PG, T
- **2026:** NVDA, AAPL, GOOGL, MSFT, AMZN, AVGO, META, TSLA, LLY, MU

Month to month, though, the top 10 is sticky: on average 1.4 names change per year.

## 3. The pre-registered trials

**Table 1. Results**

| Trial | Hypothesis | Estimate | NW t (12 lags) | p (one-sided) | Bootstrap p | Gate | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| A03-1 | The ten largest underperform the other 490 over the next 12 months | **+5.7%** per 12m | +2.07 | 0.981 | 0.987 | 0.025 | fail (opposite sign) |
| A03-2 | Rising concentration predicts an equal-weight catch-up | slope **+0.32**, R² 0.03 | 0.72 | 0.237 | 0.251 | 0.025 | fail |

> **Corrected universe (re-run 1 October 2026).** On the actual S&P 500 members at each date, instead of every company that was ever in the index in 2012–2026, the results barely move: A03-1 +6.2% per 12 months, t 2.11; A03-2 slope 0.43, t 0.70. The concentration measures are unchanged to the first decimal. Verdicts as registered: 0 of 2.

![Figure 2](../figures/fig2_top_dog_spread.png)

**A03-1: the giants did not lag.** The top 10 beat the rest over the following year in **66%** of start months; the average lead was +5.7% per 12 months (median +4.6%). I predicted this test would fail with the opposite sign, and it did. Note what this is and is not. It is clear evidence against the lore *in this sample*. It is not a registered test that the largest stocks outperform, and with about 14 independent years a t of 2.07 should not be read as a law in the other direction.

**The lead was not steady** (Figure 2). Splitting the start months in two (reported, not tested): from 2012–2018 the top 10 led by only +1.1% on average and won in 59% of months; from 2019–2025 they led by +10.5% and won in 74%. Leaving out the two strongest start years, 2019 and 2023, the average lead falls to +2.4%. The result is mostly a story about the platform and AI years.

**A03-2: no detectable catch-up, which is not the same as no catch-up.** Equal-weight minus cap-weight averaged -0.9% per 12 months, and the prior change in concentration explained 3% of its variation. With about 14 independent years this test was always weak, and I said so in the pre-registration. The fair reading is "no measurable evidence of a catch-up in this sample", not "concentration does not matter".

## 4. Where the wealth came from

![Figure 3](../figures/fig3_wealth_creation.png)

Following Bessembinder (2018), I summed each stock's monthly dollar gains (last month's market cap × this month's return) from 2012 to 2026 across the 792 names that were in the S&P 500 at some point. Net wealth created: **$70 trillion** (price only). 12% of the names destroyed wealth; the largest losses were in NBL, NOV, CHKAQ, APA and KHC.

**Table 2. How lopsided? Share of net wealth created, 2012–2026 (reported, not tested)**

| Biggest creators | Share of the 792 names | Share of net wealth |
|---|---:|---:|
| Top 1 (NVDA) | 0.1% | 8% |
| Top 5 | 0.6% | 30% |
| Top 10 | 1.3% | **39%** |
| Top 21 | 2.7% | 50% |
| Top 50 | 6.3% | 64% |

**Is 39% a lot?** For scale: Bessembinder (2018) found that about 4% of all US listed stocks accounted for the entire net wealth created by the US market from 1926 to 2016. The numbers are not directly comparable, because his universe holds every listed stock, including thousands of small losers, while this one holds only companies that made it into the S&P 500. Within that already-successful group, half of all the wealth came from 21 names.

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

- **One regime, one sample.** 2012–2026 is the era of the platform giants, and the top-10 lead is concentrated in its second half. The lore is built on the 1970s and 2000. Fourteen years cannot overturn it; they show only that it did not work *here*.
- **Ten is a choice.** The cut-off was fixed in advance, but whether the result holds for the top 5, 20 or 50 has not been checked.
- **Size or something else?** The top 10 may simply have been the most profitable or had the strongest momentum. No factor attribution was run, so "large" should not be read as the cause.
- **Low power for A03-2.** A null result from about 14 independent years says little about whether a catch-up exists.
- **Survivor-list bias, measured.** Re-running on the actual index members at each date moved the spread by half a percentage point (box under Table 1).
- **Price returns only.** The 2012 top 10 paid higher dividends than the 2026 top 10. Including dividends would narrow the spread in the early years.
- **Not a risk measure.** Nothing here measures how a concentrated index behaves in a sell-off led by its largest names. Concentration as a source of risk is untested.
- **Two trials, both failed.** Programme total now 32.

## 6. Verdict

In 2012–2026 the lore that "the biggest stocks always lag" did not hold: the largest companies outperformed the rest, mostly from 2019 onward. Rising concentration did not predict a comeback for the average stock, though that test was weak. Wealth creation was concentrated in a handful of names, which is the practical case for owning the index rather than trying to pick around its leaders. None of this makes a two-fifths weight in ten stocks harmless. It argues against using concentration as a timing signal; it says nothing about how large the risk is. Size that exposure deliberately.

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
