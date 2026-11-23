# -*- coding: utf-8 -*-
"""Render A06 'Minority Report' (teaser + deep article + PDFs).
23 Oct 2026 (stress test): single source again. Carries the 8 Oct revision (v2, kept as article/minority_report_v2.* for the
record) plus the stress-test fixes (STRESS_TEST_2026-10-23.md). Numbers of record: the corrected universe (results_pit/).
Click teaser as A04/A05 (00_Planning/TEASER_STYLE_2026-10-21.md)."""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from common import click_layout, make_pdfs, write_article, write_readme, write_teaser  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES = os.path.join(ROOT, "results"); PIT = os.path.join(ROOT, "results_pit")
S = json.load(open(os.path.join(RES, "summary.json"))); a1, a2, a3 = S["A06-1"], S["A06-2"], S["A06-3"]          # registered universe
SP = json.load(open(os.path.join(PIT, "summary.json"))); p1, p2, p3 = SP["A06-1"], SP["A06-2"], SP["A06-3"]       # corrected: numbers of record
P = json.load(open(os.path.join(RES, "placebo_summary.json")))
PS = pd.read_csv(os.path.join(RES, "placebo_shuffled.csv"))
B = pd.read_csv(os.path.join(RES, "scoreboard.csv"), index_col=0); BP = pd.read_csv(os.path.join(PIT, "scoreboard.csv"), index_col=0)
AB = json.load(open(os.path.join(PIT, "ablation.json"))); ABL, BMK = AB["ablation"], AB["benchmarks"]
REPO = "hgjerning.github.io/now-showing/minority-report"
STEM = "minority_report"
ml = [n for n in B.index if n not in ("Ensemble", "Momentum")]
neg2_pit = int((BP.loc[ml, "sharpe_h2"] < 0).sum()); pos1_pit = int((BP.loc[ml, "sharpe_h1"] > 0).sum())
h1lo, h1hi = BP.loc[ml, "sharpe_h1"].min(), BP.loc[ml, "sharpe_h1"].max(); h2lo, h2hi = BP.loc[ml, "sharpe_h2"].min(), BP.loc[ml, "sharpe_h2"].max()
r1lo, r1hi = B.loc[ml, "sharpe_h1"].min(), B.loc[ml, "sharpe_h1"].max(); neg2_reg = int((B.loc[ml, "sharpe_h2"] < 0).sum())
beaten = {m: (PS[PS.model == m].sharpe < v["real_sharpe"]).mean() for m, v in P.items()}
q = {m: PS[PS.model == m].sharpe.quantile([0.025, 0.975]).tolist() for m in P}
sr0_ann = a3["sr0"] * 12 ** 0.5

T1 = f"""| Trial | Hypothesis | Stock list | Estimate | Test statistic | p / threshold | Verdict |
|---|---|---|---:|---:|---:|---|
| A06-1 | Ensemble long-short earns a positive return | **actual members** | **{p1['mean'] * 12:+.1%} a year, Sharpe {p1['sharpe']:.2f}** | NW t {p1['t']:.2f} | p {p1['p_gt']:.3f} (gate 0.0167) | fail |
| | | registered (flattering) | {a1['mean'] * 12:+.1%} a year, Sharpe {a1['sharpe']:.2f} | NW t {a1['t']:.2f} | p {a1['p_gt']:.3f} | fail |
| A06-2 | Ensemble beats 12-1 momentum | **actual members** | **{p2['mean'] * 12:+.1%} a year** | NW t {p2['t']:.2f} | p {p2['p_gt']:.3f} | fail (wrong sign) |
| | | registered (flattering) | {a2['mean'] * 12:+.1%} a year | NW t {a2['t']:.2f} | p {a2['p_gt']:.3f} | fail (wrong sign) |
| A06-3 | Best of nine survives the selection | **actual members** | **{p3['best']}, Sharpe {p3['sr_ann']:.2f}** | deflated Sharpe {p3['dsr']:.2f} | needs > 0.983 | fail |
| | | registered (flattering) | {a3['best']}, Sharpe {a3['sr_ann']:.2f} | deflated Sharpe {a3['dsr']:.2f} | needs > 0.983 | fail |
"""
T2 = "| Model | Real Sharpe | Placebo mean | Placebo SD | 95% of placebo runs | Share of placebo runs beaten |\n|---|---:|---:|---:|---:|---:|\n" + "\n".join(
    f"| {n} | {v['real_sharpe']:.2f} | {v['placebo_mean']:+.2f} | {v['placebo_sd']:.2f} | {q[n][0]:+.2f} to {q[n][1]:+.2f} | {beaten[n]:.0%} |" for n, v in P.items())
T3 = ("| Model | Ann. L/S return | Sharpe | NW t | Mean IC | Hit rate | Sharpe, formed Jan 2017–Sep 2021 | Sharpe, formed Oct 2021–Jul 2026 | Sharpe, registered list |\n"
      "|---|---:|---:|---:|---:|---:|---:|---:|---:|\n" + "\n".join(
    f"| {'**' + n + '**' if n in ('Ensemble', 'Momentum') else n} | {r.ann_ret:+.1%} | {r.sharpe:.2f} | {r.nw_t:.2f} | {r.ic:.3f} | {r.hit:.0%} | {r.sharpe_h1:.2f} | {r.sharpe_h2:.2f} | {B.loc[n, 'sharpe']:.2f} |" for n, r in BP.iterrows()))
T3R = ("| Model | Sharpe | Sharpe, formed Jan 2017–Sep 2021 | Sharpe, formed Oct 2021–Jul 2026 |\n|---|---:|---:|---:|\n" + "\n".join(
    f"| {n} | {r.sharpe:.2f} | {r.sharpe_h1:.2f} | {r.sharpe_h2:.2f} |" for n, r in B.iterrows()))
T4 = "| Simple sort (top minus bottom decile) | Ann. L/S return | Sharpe | NW t |\n|---|---:|---:|---:|\n" + "\n".join(
    f"| {k} | {v['ann']:+.1%} | {v['sharpe']:.2f} | {v['t']:.2f} |" for k, v in BMK.items())
T5 = "| Model | All 12 features | Without 12-1 momentum | Without the trend family |\n|---|---:|---:|---:|\n" + "\n".join(
    f"| {'**' + n + '**' if n == 'Ensemble' else n} | {ABL['all'][n]['sharpe']:.2f} | {ABL['no_mom'][n]['sharpe']:.2f} | {ABL['no_trend'][n]['sharpe']:.2f} |" for n in ABL['all'])
mom = BMK['Momentum (12-1)']

md = f"""# Minority Report: can machine-learning precogs see next month's winners?

### Eight models, one 1993 rule, the same 500 large stocks, and a pre-registered test

![Now Showing](../figures/hero_minority_report.png)

*Henrik Gjerning · Rude Investment Consulting · September 2026 · Revised 8 October 2026; stress-tested 23 October 2026 · Project 10, article A06*

> **In one paragraph.** I gave eight standard machine-learning models (four regressions, a random forest, gradient boosting, a neural net and k-nearest neighbours) the same twelve features and the same 500 large US stocks, fixed every hyperparameter in advance, and let them predict each month out of sample from 2017 to 2026. **None of the three pre-registered tests passed.** On the actual S&P 500 members at each date, the numbers of record, the ensemble lost {abs(p1['mean']) * 12:.1%} a year (Sharpe {p1['sharpe']:.2f}, t {p1['t']:.2f}), trailed plain 12-1 momentum by {abs(p2['mean']) * 12:.1%} a year (t {p2['t']:.2f}), and the best of the nine candidates was momentum itself (Sharpe {p3['sr_ann']:.2f}, deflated Sharpe {p3['dsr']:.2f} against the 0.983 required). What makes the result worth reading is how much better the models first looked. Three things flattered them. *The stock list:* the list I registered contained future S&P 500 members before they joined; on it the ensemble earned {a1['mean'] * 12:+.1%} a year and the random forest a Sharpe of {a3['sr_ann']:.2f}. *The period:* on the actual members all eight models made money on portfolios formed up to September 2021 and all eight lost money afterwards. *Selection:* the best of nine on the registered list does not survive a correction for having tried nine. This is one fixed implementation in large caps with twelve inputs, before costs, not a verdict on machine learning in general.

**Statistics box.** Walk-forward, expanding window, retrained every January; out-of-sample formation months Jan 2017 → Jul 2026 ({p1['n']} months). Equal-weighted top-minus-bottom deciles, held one month, before costs, price returns. Newey–West t (3 lags). Deflated Sharpe ratio (Bailey & López de Prado, 2014) with N = 9 candidates. Three trials, gate p < 0.0167. **All three failed**, on both stock lists. **Numbers of record: the corrected list** (actual S&P 500 members at each date, Sharadar): ensemble {p1['mean'] * 12:+.1%} a year (Sharpe {p1['sharpe']:.2f}, t {p1['t']:.2f}); ensemble minus momentum {p2['mean'] * 12:+.1%} a year (t {p2['t']:.2f}); best of nine = momentum (deflated Sharpe {p3['dsr']:.2f}). Registered (flattering) list, the top 500 of every company ever in the index: ensemble {a1['mean'] * 12:+.1%} (Sharpe {a1['sharpe']:.2f}, t {a1['t']:.2f}). Placebo, ablation and simple sorts: reported, not gated. Programme trial count: 27. Every gated statistic was recomputed independently in the 23 October stress test and matched.

---

## 1. Why this matters now

Almost every asset manager now claims an AI edge. The academic evidence is real but specific. Gu, Kelly & Xiu (2020) find that tree models and neural nets predict US stock returns better than linear models, in some cases roughly doubling their performance, and that they work well among large stocks too. Later work (Freyberger, Neuhierl & Weber, 2020; Kelly, Malamud & Zhou, 2024; Leippold, Wang & Zhou, 2022, for China) also finds gains from flexible models. Two findings cut the other way for a large-cap investor. Avramov, Cheng & Metzker (2023) show that the *portfolio* gains shrink sharply once microcaps, distressed firms and other hard-to-trade stocks are excluded. Blitz, Hanauer, Hoogteijling & Howard (2023) find that machine-learning alpha is short-lived and comes with high turnover. The question for anyone buying an "AI fund" of large caps is whether the machines add anything there, monthly and in a fixed, untuned form. I predicted they would not: all three trials were expected to fail.

## 2. Design (pre-registered)

- **Universe:** each month-end, the 500 largest US stocks by point-in-time market cap (Sharadar), 2013–2026.
- **Features (12):** 1-month and 3-month return, 12-1 momentum, 60-day volatility, maximum daily return, distance from the 52-week high, beta, size, book/market, earnings/price, gross profitability, asset growth. All rank-scaled within the month; a missing value is set to the middle rank.
- **Target:** next month's return rank.
- **Models:** OLS; Ridge; Lasso; Elastic Net; random forest (300 trees, depth 6); histogram gradient boosting (registered as 200 rounds, depth 3; see section 8); MLP (32-16, three seeds); kNN (k = 500). Every hyperparameter was fixed in the pre-registration: no tuning, no hidden trials.
- **Training:** the first models are trained on formation months 2013-01 to 2016-11 (the December target is not yet known at the January retrain; the pre-registration said 2016-12), then retrained each January on an expanding window.
- **Benchmark:** sorting on 12-1 momentum alone (Jegadeesh & Titman, 1993).
- **Portfolio:** top decile minus bottom decile (about 50 stocks a side), equal weight, held one month.

> **A correction before the results.** The universe I registered and first ran was not the S&P 500 as it stood at each date. It was the 500 largest of every company that was *ever* in the index between 2012 and 2026, which lets later winners into earlier years. The pre-registration flagged this bias and expected it to matter little for comparisons between models. A re-run on the actual members at each date (1 October 2026; same code, seeds and specification) made every model worse. The registered verdicts did not change, but the corrected run is the one to read, and it leads every table and figure below. The placebo was run on the registered list only; the ablation and simple sorts on the corrected list only.

## 3. The pre-registered trials

**Table 1. The pre-registered trials, corrected and registered stock list**

{T1}

All three predictions held. On the actual index members the machine-learning edges disappear: on the registered list they were largely the survivor list. A Sharpe of {a3['sr_ann']:.2f} for the best registered model sounds respectable on its own. The deflated Sharpe ratio asks a different question: is it unusually high once nine competing models have been tried? Given how widely the nine results spread, the luckiest of nine would be expected to show about {sr0_ann:.2f} by chance, and {a3['sr_ann']:.2f} is not clearly above that. That bar is, if anything, lenient: the nine candidates are highly correlated (the four linear models are nearly identical), so their results spread less than independent tries would, and the expected luckiest result is lower. The verdict fails either way.

![Figure 1](../figures/fig1_scoreboard.png)

## 4. The placebo: what does noise look like?

I retrained Ridge and gradient boosting 50 times each on targets shuffled within every month. Every link between features and future returns is destroyed; models, features and portfolio construction stay identical. This was run on the registered list only.

**Table 2. Real vs shuffled targets (registered list, reported)**

{T2}

A model trained on pure noise produces out-of-sample Sharpe ratios anywhere from about {min(q[m][0] for m in q):.1f} to {max(q[m][1] for m in q):+.1f} over this period (the middle 95% of runs). Both real models lie inside that range, even on the flattering list; so does the best registered model, the random forest at {B.loc['RandomForest', 'sharpe']:.2f}. This is the quiet danger of machine learning in finance: with enough models, one will always look good.

## 5. The period: brilliant until 2021

**Table 3. The full scoreboard, out of sample, actual index members**

{T3}

*Halves: portfolios formed January 2017 to September 2021 (57 months) and October 2021 to July 2026 (58 months). Sub-period Sharpe was pre-registered as reported, not gated. The last column is the registered list.*

![Figure 2](../figures/fig2_cumulative.png)

![Figure 3](../figures/fig3_halves.png)

The split by halves is the most informative result in the article. On the actual index members, all {pos1_pit} machine-learning models earned positive Sharpe ratios ({h1lo:.2f} to {h1hi:.2f}) on portfolios formed up to September 2021. Anyone who backtested them in 2021 would have been encouraged. On portfolios formed from October 2021 onward, {neg2_pit} of 8 lost money ({h2lo:.2f} to {h2hi:.2f}). Momentum, which every model could see as a feature, went the other way, from {BP.loc['Momentum', 'sharpe_h1']:.2f} to {BP.loc['Momentum', 'sharpe_h2']:+.2f}. On the registered list the same pattern is roughly twice as large (first-half Sharpe {r1lo:.2f} to {r1hi:.2f}; {neg2_reg} of 8 negative afterwards, Table 3b). The second half coincided with rising rates and a market led by mega-cap growth, but this design cannot say which, if any, of those changes broke the models. Each half is under five years, so a single half-sample Sharpe is noisy: a rough rule of thumb puts its standard error near 0.45.

**Table 3b. Registered list, for comparison (reported)**

{T3R}

## 6. Is momentum an unfairly hard benchmark?

Momentum is the strongest single signal the models could see. Table 4 shows the other simple sorts on the corrected list, same portfolio rules (reported, not tested).

**Table 4. Simple one-characteristic sorts, corrected list (reported)**

{T4}

Every simple sort except momentum lost money in large caps over these years. These are price returns, which understates the sorts that favour high-dividend stocks (value, earnings yield, low volatility). Momentum, at Sharpe {mom['sharpe']:.2f} (t {mom['t']:.2f}), was the best of a weak field, not a high bar. The models did not clear it either.

## 7. Feature ablation: were the models just momentum?

If the models only did well by rediscovering momentum, they told us little. So I re-ran the whole walk-forward on the corrected list, unchanged except for the inputs: once without 12-1 momentum, and once without the price-trend family (12-1 momentum, 3-month return and distance from the 52-week high). Reported, not gated.

**Table 5. Out-of-sample Sharpe ratio by input set, corrected list**

{T5}

Removing momentum does not hurt. The ensemble moves from {ABL['all']['Ensemble']['sharpe']:.2f} to {ABL['no_mom']['Ensemble']['sharpe']:.2f}, and to {ABL['no_trend']['Ensemble']['sharpe']:.2f} without the trend family. The neural net and kNN do somewhat better without it, but with nine models and three input sets, some cells will look good by chance. Every number lies within the range of the shuffled-target runs in Table 2 (measured on the registered list). So the models were not simply repackaging momentum, but they found nothing else that lasted either.

## 8. Limits, and what would have counted as success

- **This implementation, not machine learning in general.** One fixed implementation, 12 inputs, large caps, a 4-year first training window (Gu, Kelly & Xiu use 18), before costs. Their inputs are far richer, and the published portfolio gains are largest in small, illiquid stocks.
- **No tuning, by design.** Tuned models might do better in-sample. Each tuning choice is another trial, and the deflated Sharpe would charge for it.
- **Gradient boosting deviated from the registration.** It was registered as 200 boosting rounds, but scikit-learn's default early stopping was left on: with more than 10,000 training rows it holds out 10% and stops after 10 rounds without improvement. The effect cannot be measured without re-running on the licensed data.
- **Two settings not in the pre-registration.** Beta is measured against the equal-weighted average of the whole master list, not the month's 500; and a fundamental value older than 400 days is treated as missing.
- **Turnover was pre-registered as reported but was not computed.** A monthly long-short decile book turns over heavily, so net of costs every number here is lower (see A11 *Money for Nothing*).
- **Price returns only**, which understates high-dividend sorts (section 6).
- **115 months, one change of regime.** Short for a monthly long-short book; the halves are shorter still.
- **Survivor-list bias.** Measured for the trials, the halves and the scoreboard; not for the placebo.
- **Multiple testing.** Three trials here, 27 in the programme.

**What would have counted as evidence for machine learning here?** A positive ensemble long-short with t above about 2.1 (p < 0.0167) on the corrected list; an ensemble that beats momentum in both halves, not just one; a best model whose deflated Sharpe clears 0.983; and real Sharpe ratios clearly outside the shuffled-target range. None of these appeared.

## 9. Verdict

The strongest finding is not that machine learning failed. It is how fragile its apparent success was. A survivor-contaminated stock list, a friendly period and picking the best of nine models each made it look better than it was. Once those are accounted for, nothing survives, and in the 500 largest US stocks a one-line rule from 1993 did at least as well. That does not mean machine learning cannot add value elsewhere. It means claims of machine-learning alpha should be judged on a corrected universe, a true out-of-sample record that spans more than one regime, and a correction for the number of models tried.

## Reproduce

```bash
python code/run_ml.py        # A06-1..3, results/summary.json (about 5 minutes on 2 cores)
python code/run_placebo.py   # shuffled-target placebo (about 20 minutes)
P10_UNIVERSE=sp500_pit P10_RESULTS=results_pit python code/run_ml.py   # corrected universe
python code/ablation.py      # added after review: feature ablation and simple sorts (about 15 minutes)
python code/make_figures.py && python code/make_teaser_drawing.py && python code/build_article.py
```

## References

- Avramov, D., Cheng, S. & Metzker, L. (2023). Machine learning vs. economic restrictions: evidence from stock return predictability. *Management Science*, 69(5).
- Bailey, D. H. & López de Prado, M. (2014). The deflated Sharpe ratio: correcting for selection bias, backtest overfitting, and non-normality. *Journal of Portfolio Management*, 40(5).
- Blitz, D., Hanauer, M. X., Hoogteijling, T. & Howard, C. (2023). The term structure of machine learning alpha. *Journal of Financial Data Science*.
- Freyberger, J., Neuhierl, A. & Weber, M. (2020). Dissecting characteristics nonparametrically. *Review of Financial Studies*, 33(5).
- Gu, S., Kelly, B. & Xiu, D. (2020). Empirical asset pricing via machine learning. *Review of Financial Studies*, 33(5).
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1).
- Kelly, B., Malamud, S. & Zhou, K. (2024). The virtue of complexity in return prediction. *Journal of Finance*, 79(1).
- Leippold, M., Wang, Q. & Zhou, W. (2022). Machine learning in the Chinese stock market. *Journal of Financial Economics*, 145(2), 64–82.
- Newey, W. K. & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3).

*Not investment advice. Film title used as a cultural reference only.*
"""
write_article(ROOT, STEM, md, "Minority Report")

# 23 Oct 2026: click teaser (as A04/A05). The post asks; the article answers (THE_INTERVAL.json A06 "click").
post = f"""MINORITY REPORT: can machine-learning precogs see next month's winners?

Almost every fund now sells an AI edge. The best-known evidence: Gu, Kelly & Xiu (2020) found that tree models and neural nets predict US stock returns better than linear models, large stocks included.

I lined up eight machine-learning models against one rule from 1993 (buy last year's winners), on 500 large US stocks, with the tests written down first. One fixed implementation, 12 inputs, before costs: a test of this setup, not of ML in general. At first sight the random forest's Sharpe of {B.loc['RandomForest', 'sharpe']:.2f} beat momentum's {B.loc['Momentum', 'sharpe']:.2f}.

Three questions before you buy the AI fund:
1. Did the machines beat a 1993 rule, or did their stock list know the future?
2. When did the precogs stop seeing the future?
3. How good does a model trained on pure noise look?

Your answer to question 1 in the comments, then check it here, with tables, code and the pre-registration: {REPO} · Not investment advice.

#machinelearning #AI #investing #quant
"""
write_teaser(ROOT, post, "hero_minority_report_teaser.png", "Minority Report", "10 November 2026")   # teaser poster asks, article poster answers
click_layout(ROOT, "teaser_precogs.png", alt="Drawing: the three questions inside three precogs' crystal balls")   # code/make_teaser_drawing.py
write_readme(ROOT, "A06 Minority Report: can machine-learning precogs see next month's winners?",
             ["run_ml.py", "run_placebo.py", "ablation.py", "make_figures.py", "make_teaser_drawing.py", "build_article.py"],
             "\nThe numbers of record are the corrected universe in `results_pit/`. `results/oos_predictions.pkl` and `results_pit/oos_predictions.pkl` hold per-stock predictions and are listed in `.gitignore`.\n")
open(os.path.join(ROOT, ".gitignore"), "w").write("results/oos_predictions.pkl\nresults_pit/oos_predictions.pkl\nresults_rerun_top500/\n")
open(os.path.join(ROOT, "README.md"), "a").write("Publication slot: Tuesday 10 November 2026 (Now Showing No. 6).\n")
try:
    make_pdfs(ROOT, STEM)
except Exception as e:  # no browser here: print the PDFs on Windows
    print("PDFs not built here:", type(e).__name__)
print(post); print("words", len(post.split()))
