# -*- coding: utf-8 -*-
"""Render A03 'The Magnificent Seven' (teaser + deep article + PDFs)."""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from common import make_pdfs, write_article, write_readme, write_teaser  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES = os.path.join(ROOT, "results")
S = json.load(open(os.path.join(RES, "summary.json"))); R = S["reported"]; a1, a2 = S["A03-1"], S["A03-2"]
D = pd.read_csv(os.path.join(RES, "concentration_monthly.csv"), index_col=0, parse_dates=True)
REPO = "hgjerning.github.io/now-showing/magnificent-seven"
STEM = "magnificent_seven"

T1 = f"""| Trial | Hypothesis | Estimate | NW t (12 lags) | p (one-sided) | Bootstrap p | Gate | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| A03-1 | The ten largest underperform the other 490 over the next 12 months | **{a1['mean']:+.1%}** per 12m | {a1['t']:+.2f} | {a1['p_lt']:.3f} | {a1['boot_p_lt']:.3f} | 0.025 | fail (opposite sign) |
| A03-2 | Rising concentration predicts an equal-weight catch-up | slope **{a2['slope']:+.2f}**, R² {a2['r2']:.2f} | {a2['t']:.2f} | {a2['p_gt']:.3f} | {a2['boot_p_gt']:.3f} | 0.025 | fail |
"""
yr = D.groupby(D.index.year).agg(C=("C", "last"), spread=("spread", "mean"), ew_cw=("ew_cw", "mean"))
T2 = "| Year-end | Top-10 share | Mean next-12m spread, top 10 − rest (start months in year) | Mean next-12m EW − CW |\n|---|---:|---:|---:|\n" + "\n".join(
    f"| {y} | {r.C:.1%} | {r.spread:+.1%} | {r.ew_cw:+.1%} |" if pd.notna(r.spread) else f"| {y} | {r.C:.1%} | n/a | n/a |" for y, r in yr.iterrows())
T3 = "| Rank | Ticker | Net wealth created, $ tn |\n|---:|---|---:|\n" + "\n".join(f"| {i + 1} | {t} | {v:.2f} |" for i, (t, v) in enumerate(zip(R["top10_creators"], R["top10_creators_usd_tn"])))

md = f"""# The Magnificent Seven: does concentration come back to bite?

### Ten stocks, two-fifths of the market, and the lore that the giants always fall

![Now Showing](../figures/hero_magnificent_seven.png)

*Henrik Gjerning · Rude Investment Consulting · September 2026 · Project 10, article A03*

> **In one paragraph.** In February 2012 the ten largest US companies made up **{R['C_first']:.0%}** of the 500 largest. By August 2026 they made up **{R['C_last']:.0%}**, and the single largest, NVIDIA, weighed {R['C1_last']:.1%} on its own. Market lore says this ends badly: the biggest stocks lag, and when concentration peaks the average stock catches up. I pre-registered both claims and tested them on every month since 2012. **Both failed.** The then-top-10 beat the other 490 by **{a1['mean']:+.1%}** per 12 months on average (t {a1['t']:+.2f}, the wrong sign for the lore). Rising concentration did not predict an equal-weight catch-up (t {a2['t']:.2f}). Of the ${R['wealth_net_usd_tn']:.0f} trillion of net wealth these stocks created, **{R['wealth_top10_share']:.0%} came from just ten names.**

**Statistics box.** Monthly market cap = latest Sharadar filing, scaled by the price move since filing; top 500 each month-end, Feb 2012 → Aug 2026. Twelve-month buy-and-hold, cap-weighted portfolios; overlapping monthly observations; Newey-West (12 lags) and a stationary bootstrap (mean block 12, 10,000 draws). Two trials, one-sided gate p < 0.025. **Both failed.** Price returns (no dividends).

---

## 1. Why this matters now

Index investors today hold a portfolio in which ten names carry nearly two-fifths of the weight. That is a large bet on a few business models (chips, cloud, advertising, devices), and it has prompted a stream of warnings. The historical case rests on two ideas: large firms find it harder to grow (the size effect of Banz 1981), and extreme leadership in the past, such as the Nifty Fifty in the 1970s and the telecoms and tech leaders of 2000, ended in underperformance. The first lesson of Bessembinder (2018) is the opposite: most of the stock market's wealth is created by a handful of stocks, and they are not easy to replace.

## 2. How concentrated is it?

![Figure 1](../figures/fig1_concentration.png)

The top-10 share was flat at around a fifth until 2016 ({R['C_min']:.0%} at its low). It then roughly doubled, peaking at **{R['C_max']:.1%} in {pd.Timestamp(R['C_max_month']):%B %Y}**. The line-up changed almost completely:

- **2012:** {R['top10_first'].replace(',', ', ')}
- **2026:** {R['top10_last'].replace(',', ', ')}

Yet month to month the top 10 is sticky: on average only {R['top10_changes_per_year']:.1f} names change per year.

## 3. The pre-registered trials

**Table 1. Results**

{T1}

> **Corrected universe (re-run 1 October 2026).** On the actual S&P 500 members at each date, instead of every company that was ever in the index in 2012–2026, the result barely moves: A03-1 +6.2% a year, t 2.11 (published +5.7%, t 2.07); A03-2 slope 0.43, t 0.70 (published 0.32, t 0.72). The concentration measures are unchanged to the first decimal. Verdicts as registered: 0 of 2. Details: `rerun_comparison.csv`.

![Figure 2](../figures/fig2_top_dog_spread.png)

The giants beat the rest over the following year in **{a1['share_months_top_won']:.0%}** of start months. The average lead was {a1['mean']:+.1%} per 12 months (median {R['median_spread_12m']:+.1%}). The "top dog" lore did not just fail to show up: it ran the other way.

The catch-up test fared no better. Equal-weight minus cap-weight averaged {R['ew_cw_mean_12m']:+.1%} per 12 months, and the prior change in concentration explained {a2['r2']:.0%} of its variation. With about 14 independent years of data, this test was always going to be weak. I said so in the pre-registration.

**Table 2. Year by year (descriptive)**

{T2}

## 4. Where the wealth came from

![Figure 3](../figures/fig3_wealth_creation.png)

Following Bessembinder (2018), I summed each stock's monthly dollar gains (last month's market cap × this month's return) from 2012 to 2026, across {R['n_stocks']} names that were in the S&P 500 at some point.

- Net wealth created: **${R['wealth_net_usd_tn']:.0f} trillion** (price only).
- The top 10 creators: **{R['wealth_top10_share']:.0%}**. The top 2% ({R['n_top2pct']} names): **{R['wealth_top2pct_share']:.0%}**.
- {R['share_negative']:.0%} of the names destroyed wealth over the period; the largest losses were in {', '.join(R['bottom5'])}.

**Table 3. The ten biggest wealth creators, 2012–2026**

{T3}

## 5. What this does and does not show

- **One regime, one sample.** 2012–2026 is the era of the platform giants. The lore is built on the 1970s and 2000. Fourteen years of data cannot overturn it; they only show that it did not work *here*.
- **Survivor-list bias favours winners.** The ticker list holds every name that was ever in the S&P 500 during 2012–2026. Firms added after big gains are in the sample earlier than an index investor would have held them. This inflates the "rest" as well as the top, so the spread is less affected than the levels. Re-running on the actual members at each date (box under Table 1) moves the spread by half a percentage point.
- **Price returns only.** The 2012 top 10 paid higher dividends than the 2026 top 10. Including dividends would narrow the spread in the early years.
- **Two trials, both failed.** Programme total now 32.

## 6. Verdict

The lore that "the biggest stocks always lag" was not a law in this sample; it was a coin that came up the other way two-thirds of the time. Concentration at two-fifths is a risk to be sized, not a timing signal. The strongest evidence here is Bessembinder's: a small number of companies create most of the wealth, and an index fund is the cheapest way not to miss them. The price is holding a portfolio that looks more like a sector bet every year.

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
"""
write_article(ROOT, STEM, md, "The Magnificent Seven")

post = f"""THE MAGNIFICENT SEVEN: does concentration come back to bite?

In 2012 the ten largest US stocks were {R['C_first']:.0%} of the 500 largest. Today they are {R['C_last']:.0%}.

Market lore says this ends badly:
→ the biggest stocks lag the rest
→ when concentration peaks, the average stock catches up

I wrote both claims down as tests before looking, then ran them on every month since 2012.

Both failed.

The then-top-10 beat the other 490 by {a1['mean']:+.1%} over the following year on average, and did so in {a1['share_months_top_won']:.0%} of start months. Rising concentration predicted nothing about the catch-up (t = {a2['t']:.1f}).

And the wealth? Of ${R['wealth_net_usd_tn']:.0f} trillion created since 2012, {R['wealth_top10_share']:.0%} came from just ten stocks. {R['share_negative']:.0%} of names destroyed wealth.

The fair caveat: 14 years is one regime, and the lore was built on the 1970s and 2000. This doesn't prove the giants can't fall. It shows the "top dog" rule wasn't a timing signal here.

Concentration is a risk to size, not a date to guess.

Tables, code and the pre-registration: {REPO}

#investing #indexfunds #magnificent7 #statistics
"""
write_teaser(ROOT, post, "hero_magnificent_seven.png", "The Magnificent Seven", "October 2026")
write_readme(ROOT, "A03 The Magnificent Seven: does concentration come back to bite?", ["run_concentration.py", "make_figures.py", "build_article.py"],
             "\n`results/wealth_creation_by_stock.csv` is derived from Sharadar market caps and is listed in `.gitignore`.\n")
open(os.path.join(ROOT, ".gitignore"), "w").write("results/wealth_creation_by_stock.csv\n")
make_pdfs(ROOT, STEM)
open(os.path.join(ROOT, "README.md"), "a").write("Publication slot: 19 January 2027.\n")
print(post); print("words", len(post.split()))
