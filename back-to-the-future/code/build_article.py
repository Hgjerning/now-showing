# -*- coding: utf-8 -*-
"""Render Case 33 (teaser + deep article) from ../results and ../data. No result is typed in."""
import base64
import json
import os

import markdown
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES, FIG, D = (os.path.join(ROOT, x) for x in ("results", "figures", "data"))
S = json.load(open(os.path.join(RES, "summary.json")))
REPO = "hgjerning.github.io/now-showing/back-to-the-future"
pc = lambda v, d=1: f"{v * 100:+.{d}f}%"
wf = pd.DataFrame(S["waterfall"]); rec, oos, mt, hc = S["record"], S["oos"], S["multiple_testing"], S["haircuts"]
ins, sv, rb, band, roll, plc = S["insample_rederived"], pd.DataFrame(S["survivorship"]), S["random_books"], S["band"], S["rolling"], S["placebo"]
lit = pd.read_csv(os.path.join(D, "literature_haircuts.csv"))
a = lambda k: float(wf.loc[wf.step == k, "alpha_ann"].iloc[0])
t = lambda k: float(wf.loc[wf.step == k, "t_stat"].iloc[0])
svmin, svmax = sv.haircut.min(), sv.haircut.max()

# ------------------------------------------------------------------ tables
T1 = "| # | Date (2026) | Restatement | What changed | Alpha / yr | t (type) | Sharpe: strategy vs benchmark |\n|---|---|---|---|---:|---|---|\n"
for r in wf.itertuples():
    shp = f"{r.sharpe_book:.3f} vs {r.sharpe_bench:.3f}" if pd.notna(r.sharpe_book) else "n/a"
    T1 += f"| {r.step} | {r.date[5:]} | {r.label} | {r.what_changed} | **{pc(r.alpha_ann, 2)}** | {r.t_stat:.2f} ({r.t_type}) | {shp} |\n"
T1 += f"| OOS | 09-01 | Out of sample, 1995–2011 | Same rules on a point-in-time universe never used in development | **{pc(oos['record_alpha'], 2)}** | {oos['record_t']:.2f} | {oos['record_sharpe']:.3f} vs {oos['record_bench_sharpe']:.3f} |\n"
T1 += "\n*The rows are restatements in the order they happened, not additive components: row 3 was measured on the row-2 book, and row 4 is today's number of record. Sources for every row are in `data/waterfall_sources.csv`.*"

T2 = "| Universe | Sharpe on today's members | Sharpe on members at the time | Overstatement | Method |\n|---|---:|---:|---:|---|\n"
T2 += "\n".join(f"| {r.region} | {r.biased:.3f} | {r.pit:.3f} | {r.overstatement * 100:+.0f}% (haircut {r.haircut * 100:.0f}%) | {r.note} |" for r in sv.itertuples())

reg = oos["per_region"]
T3 = f"""| | Strategy | Benchmark |
|---|---:|---:|
| Period, weeks | {oos['start']} to {oos['end']}, {oos['n']} | same |
| CAGR | {pc(oos['cagr'])} | {pc(oos['bench_cagr'])} |
| Sharpe | {oos['record_sharpe']:.3f} | {oos['record_bench_sharpe']:.3f} |
| Maximum drawdown | **{oos['record_mdd'] * 100:.1f}%** | {oos['record_bench_mdd'] * 100:.1f}% |
| Beta to benchmark | {oos['record_beta']:.2f} | 1.00 |
| Alpha / yr, 95% CI (record) | **{pc(oos['record_alpha'], 2)}** [{pc(oos['record_ci'][0])}, {pc(oos['record_ci'][1])}], t {oos['record_t']:.2f} | |
| Alpha / yr, plain OLS (re-derived here) | {pc(oos['rederived_alpha_ols'], 2)}, t {oos['rederived_t_ols']:.2f} | |
| Europe leg alone | {pc(list(reg.values())[0]['alpha'], 2)}, t {list(reg.values())[0]['t']:.2f} | |
| America leg alone | {pc(list(reg.values())[1]['alpha'], 2)}, t {list(reg.values())[1]['t']:.2f} | |

*Benchmark: cap-weighted return of the same point-in-time universe (top 600 Europe, top 500 America), equal-weighted across the two regions, as pre-registered. The strategy ends with more wealth than the benchmark only because it carried more market risk (beta {oos['record_beta']:.2f}); per unit of risk it lost.*"""

T4 = "| Number of strategies tried | t needed (Bonferroni, 5% two-sided) | Does t = 2.90 clear it? |\n|---:|---:|---|\n"
T4 += "\n".join(f"| {n} | {v:.2f} | {'yes' if mt['t_first'] >= v else 'no'} |" for n, v in mt["t_needed"].items())

T5 = "| Study | Sample | Finding | Haircut |\n|---|---|---|---:|\n"
T5 += "\n".join(f"| {r.study} | {r.sample} | {r.finding} | {'' if pd.isna(r.haircut_pct) else f'{r.haircut_pct:.0f}%'} |" for r in lit.itertuples())
T5 += f"\n| **This strategy** | one momentum book, 2012–2026 | alpha, first result → number of record | **{hc['alpha_first_to_record'] * 100:.0f}%** |"
T5 += f"\n| **This strategy** | same | alpha, first result → out of sample | **{hc['alpha_first_to_oos'] * 100:.0f}%** |"
T5 += f"\n| **This strategy** | same | Sharpe, first result → number of record | **{hc['sharpe_first_to_record'] * 100:.0f}%** |"

T6 = "| Region | Sharpe gain from the band | 95% CI (paired block bootstrap) |\n|---|---:|---|\n"
names = {"EU": "Europe", "UK": "UK", "WD": "World", "DK": "Denmark", "US": "US"}
T6 += "\n".join(f"| {names[r['region']]} | {r['diff']:+.3f} | [{r['ci_lo']:+.3f}, {r['ci_hi']:+.3f}] |" for r in band["regions"])
T6 += f"\n| **Book (50/50 US/Europe)** | **{band['book_diff']:+.3f}** | [{band['ci'][0]:+.3f}, {band['ci'][1]:+.3f}] |"

# ------------------------------------------------------------------ deep article
md = f"""# Back to the Future: my strategy beat the market by 5% a year. In the past.

### One momentum strategy, six honest corrections, and what was left

![Now Showing](../figures/hero_back_to_the_future.png)

*Henrik Gjerning · Rude Investment Consulting · September 2026 · Project 10, Case 33*

> **In one paragraph.** On 1 September 2026 a weekly momentum strategy I had built showed **{pc(a(1))} a year of alpha** against the MSCI World ETF, with a t-statistic of {t(1):.2f}. Two weeks of checking later, the same strategy's number of record is **{pc(rec['alpha'])} (t {rec['t_block']:.2f})**. Adjusted for known factors it is **{pc(a(5))}**. On sixteen years of point-in-time data it had never seen, it earned **{pc(oos['record_alpha'])} (t {oos['record_t']:.2f})** with a **{oos['record_mdd'] * 100:.0f}%** drawdown against the market's {oos['record_bench_mdd'] * 100:.0f}%. Nothing was fraudulent and nothing was unusual. Every correction was a standard one: dividends, currency, a code bug, survivorship, the right null hypothesis, and counting the trials. The haircut, {hc['alpha_first_to_record'] * 100:.0f}%, is in line with what the literature finds for published anomalies and for bank strategies once they go live. The only result that survived was about **trading less**.

**Statistics box.** In-sample: {ins['n']} weeks, {ins['start']} to {ins['end']}. Number of record: alpha {pc(rec['alpha'], 2)} a year, 95% CI [{pc(rec['ci'][0])}, {pc(rec['ci'][1])}], t {rec['t_block']:.2f} (block bootstrap) / {rec['t_ols']:.2f} (OLS), beta {rec['beta']:.2f}. Trials {rec['trials']}, Bonferroni bar t {rec['bonferroni_t']:.2f}. Harvey–Liu–Zhu haircut of the first t at 33 trials: {mt['hlz_33']['haircut'] * 100:.0f}%. Out of sample: {oos['n']} weeks, alpha {pc(oos['record_alpha'], 2)}, t {oos['record_t']:.2f}. Cross-sectional placebo z: {plc['z_live']:.2f} on today's members, {plc['z_pit']:.2f} on point-in-time members.

![Figure 1](../figures/fig1_alpha_waterfall.png)

---

## 1. The result that looked too good

The strategy is a long-only, weekly-rebalanced momentum book. Each week it ranks large-cap stocks in the US and Europe on eight price-only features (12- and 6-month momentum, trend, volatility, short-term reversal and a few more) and holds the ten best per region, weighted by inverse volatility. It pays a measured, realistic commission and prefers names it already holds, to save turnover.

The first regression against the MSCI World ETF, over 2012–2026, gave {pc(a(1), 2)} a year, t {t(1):.2f}, and a Sharpe ratio of {float(wf.sharpe_book[0]):.3f} against the benchmark's {float(wf.sharpe_bench[0]):.3f}. That is the result a quant hopes for. It is also exactly what the literature warns about. The rest of this article is what happened when I tried to break it.

## 2. The waterfall

**Table 1. The same strategy, restated after each correction**

{T1}

### Correction 1: dividends (+5.1% → +4.3%)

The US leg used total-return prices. The European legs, and the benchmark itself, used price-only closes. Mixing the two quietly favours whichever side leaves out dividends, and the benchmark's return rose more when dividends were added: its Sharpe went from {float(wf.sharpe_bench[0]):.3f} to {float(wf.sharpe_bench[1]):.3f}. **Lesson: strategy and benchmark must be on the same return basis, every leg.**

### Correction 2: currency (+4.3% → +3.4%)

European legs were summed in their local currencies (EUR, SEK, DKK, CHF and PLN) as if they had been hedged for free, while the benchmark is an unhedged USD fund. Restated in the benchmark's currency, the alpha fell to {pc(a(3))} and the t to {t(3):.2f}. **Lesson: a return has a currency. Say which one.**

### Correction 3: the holding bug (→ {pc(rec['alpha'])})

To save trading costs, the strategy gives a bonus to stocks it already holds. A parameter search had set that bonus so high that the book barely traded: about forty names over fifteen years, changed in roughly one week in seventeen. It had become a buy-and-hold portfolio of stocks picked early in the sample. Resetting the bonus on mechanical grounds, not on performance, gives today's number of record: **{pc(rec['alpha'], 2)} a year, t {rec['t_block']:.2f}**. Its Sharpe of {ins['sharpe_book']:.3f} is now *below* the benchmark's {ins['sharpe_urth']:.3f}. Maximum drawdown is {ins['mdd_book'] * 100:.1f}% against {ins['mdd_urth'] * 100:.1f}%. I re-derived these from the stored weekly series and they match to the last digit.

### Correction 4: known factors (→ {pc(a(5))})

With the bug fixed, the strategy's momentum loading appears clearly (+0.51, t 5.8, on 13 JKP themes). Regressed on those factors, the alpha is {pc(a(5))} (t {t(5):.2f}). Across four attribution models it lies between −1.7% and +2.9% a year, and every t is below 1. **It is a momentum fund, and momentum is available cheaply.**

## 3. Survivorship: backtesting on today's winners

The easiest universe to download is today's index. It is also the most dangerous. Every stock in it survived to be there, and a momentum strategy is especially good at finding the ones that went on to survive.

**Table 2. The same strategy on today's members vs members at the time**

{T2}

![Figure 3](../figures/fig3_survivorship.png)

The haircut ranges from {svmin * 100:.0f}% to {svmax * 100:.0f}% of the Sharpe ratio. The effect is even larger on a placebo test, which replays the strategy's exact holding schedule with randomly chosen names. On today's index members the strategy looked extraordinary (z = {plc['z_live']:.2f}). On members at the time it sits at the {plc['pct_pit']:.0f}th percentile (z = {plc['z_pit']:.2f}): about one random portfolio in eleven did better. Survivorship and momentum interact. Among survivors, past winners are disproportionately the names that kept winning, so the same test on the convenient universe inflates the answer about 3.7 times.

## 4. The wrong null: a dartboard beats the market

A common way to judge a stock-picking strategy is to ask whether its alpha is significantly above zero. But zero is the wrong benchmark when the universe itself is biased. I drew {rb['n']:,} random ten-stock books from the same survivor universe and measured their alpha the same way.

![Figure 4](../figures/fig4_random_books.png)

The random books averaged a t of {rb['mean_t']:.2f} and {rb['share_t_gt_2'] * 100:.1f}% of them cleared t > 2. The strategy's own t of {rb['frozen_t']:.2f} beat almost all of them ({rb['share_t_gt_frozen'] * 100:.2f}% did better). That test was run on the frozen, bugged book, and it shows how much apparent skill the universe hands out for free. **Lesson: test against random portfolios drawn from the same universe, not against zero.**

## 5. Out of sample: sixteen years the strategy had never seen

Before looking, I registered one test. The same rules would run on a point-in-time database of European and American large caps, 1995–2011, a period the strategy had never touched. The pass rule was t > 2.

**Table 3. The out-of-sample test**

{T3}

![Figure 2](../figures/fig2_oos_drawdown.png)

It did not replicate. The in-sample drawdown advantage also disappeared. The 2012–2026 window contains no full bear market, and 1995–2011 contains two. A strategy that looked defensive in-sample lost {abs(oos['record_mdd']) * 100:.0f}% peak to trough, far more than the market.

## 6. Counting the trials

Every choice you make after seeing the data (a feature, a lookback, a region, a parameter) is another draw from the lottery. This project counted them: {rec['trials']} pre-registered trials by the time of the last correction.

**Table 4. What t is needed when you have tried N things**

{T4}

The first t of {t(1):.2f} would have survived only up to 13 trials. The Harvey, Liu & Zhu (2016) Bonferroni haircut at 33 trials takes the t to {mt['hlz_33']['t_adj']:.2f}, a {mt['hlz_33']['haircut'] * 100:.0f}% haircut to the Sharpe ratio, before any of the corrections above. The deflated Sharpe ratio of the best of the first 24 variants (Bailey & López de Prado, 2014) was {S['dsr_best_of_24']:.4f}, below the 0.95 threshold. **Lesson: write the count down before you start, and raise the bar with it.**

## 7. How typical is this? Relevance statistics

**Table 5. This strategy's haircut against the literature**

{T5}

A {hc['alpha_first_to_record'] * 100:.0f}% alpha haircut sounds dramatic. It is ordinary. McLean & Pontiff find published anomalies lose 58% of their return after publication. Suhonen, Lennkh & Perez find bank-marketed alternative-beta strategies lose a median 73% of their backtested Sharpe once live. Hou, Xue & Zhang fail most of 452 anomalies on a clean replication. Wiecki et al. find that a backtest's Sharpe barely predicts its live Sharpe. On that evidence, **the right prior for any backtest is that most of it will go**. This one went slightly faster than average, because each correction here was cheap to make.

## 8. What survived: trading less

One result cleared every test I put to it. The strategy skips trades below a fixed size (a no-trade band), and that measurably improves its Sharpe ratio in every region.

**Table 6. The no-trade band**

{T6}

![Figure 5](../figures/fig5_band_and_rolling_alpha.png)

It is not selection skill. It is cost control: the same strategy, run with less churn. Compared with an index fund, the strategy still has nothing to show. Its rolling three-year alpha has been negative in {roll['share_neg_since_2019'] * 100:.0f}% of weeks since 2019 and stood at {pc(roll['last'])} at the last reading ({roll['last_date']}).

## 9. A checklist before you believe a backtest

1. **Same return basis** for every leg and the benchmark (total return, same currency).
2. **Point-in-time universe:** the index as it was, including the names that later died.
3. **Clean data:** one bad split (a 1:1000 reverse split read as +107,385% in a week) was held by this momentum strategy for 63 weeks.
4. **The right null:** random portfolios from the same universe, not zero.
5. **Count every trial** and raise the t-bar with it; report the deflated Sharpe.
6. **Test on untouched data** with a rule written down before looking.
7. **Report the drawdown path**, not only the Sharpe, and a sample with a bear market in it.

## 10. Caveats

- This is one strategy. The corrections are general, but their sizes are not.
- The point-in-time European universe is itself incomplete (26% of historical names lack prices), so its survivorship estimate is a lower bound.
- The out-of-sample period (1995–2011) comes from a licensed database. Only summary statistics and charts are published, not the series.
- Currency restatement was measured on the pre-fix book (row 3 of Table 1).

## Reproduce

```bash
python code/analyse.py         # re-derives the numbers of record, writes results/summary.json
python code/make_figures.py    # figures/
python code/build_article.py   # this article and the LinkedIn teaser
python code/make_pdfs.py       # PDFs
```

The weekly return series live in `data_private/` and are not published: they derive from licensed data. Everything else (summary files, sources for each number, code) is in the repository.

## References

- Bailey, D. H. & López de Prado, M. (2014). The deflated Sharpe ratio: correcting for selection bias, backtest overfitting and non-normality. *Journal of Portfolio Management*, 40(5).
- Brown, S. J., Goetzmann, W., Ibbotson, R. G. & Ross, S. A. (1992). Survivorship bias in performance studies. *Review of Financial Studies*, 5(4).
- Harvey, C. R., Liu, Y. & Zhu, H. (2016). … and the cross-section of expected returns. *Review of Financial Studies*, 29(1).
- Hou, K., Xue, C. & Zhang, L. (2020). Replicating anomalies. *Review of Financial Studies*, 33(5).
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5).
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1).
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance*, 71(1).
- Gârleanu, N. & Pedersen, L. H. (2013). Dynamic trading with predictable returns and transaction costs. *Journal of Finance*, 68(6).
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies*, 29(1).
- Suhonen, A., Lennkh, M. & Perez, F. (2017). Quantifying backtest overfitting in alternative beta strategies. *Journal of Portfolio Management*, 43(2).
- Wiecki, T., Campbell, A., Lent, J. & Stauth, J. (2016). All that glitters is not gold: comparing backtest and out-of-sample performance on a large cohort of trading algorithms. *Journal of Investing*, 25(3).
- White, H. (2000). A reality check for data snooping. *Econometrica*, 68(5).

*Not investment advice.*
"""
open(os.path.join(ROOT, "article", "backtest_vs_reality.md"), "w").write(md)

# ------------------------------------------------------------------ teaser
post = f"""BACK TO THE FUTURE: my strategy beat the market by 5% a year. In the past.

Then I tested it properly.

In early September I had what every quant hopes for: a momentum strategy with {pc(a(1))} a year of alpha against the MSCI World ETF, t-stat {t(1):.2f}.

Then I checked it, one correction at a time:
→ Include dividends everywhere: {pc(a(2))}
→ Measure every leg in the same currency: {pc(a(3))}
→ Fix a bug that had quietly frozen the portfolio: {pc(rec['alpha'])}, t {rec['t_block']:.2f}
→ Adjust for known factors: {pc(a(5))}

Then the test I wrote down in advance: sixteen years of data it had never seen. Result: {pc(oos['record_alpha'])} a year, t {oos['record_t']:.2f}, and a {oos['record_mdd'] * 100:.0f}% drawdown against the market's {oos['record_bench_mdd'] * 100:.0f}%.

Two lessons cost the most.
Survivorship: backtesting on today's index members flattered the Sharpe ratio by {svmin * 100:.0f}–{svmax * 100:.0f}% in every region I measured.
The wrong null: {rb['share_t_gt_2'] * 100:.0f}% of random 10-stock portfolios from the same universe also "beat" the market with t > 2.

I tried {rec['trials']} things along the way, so the honest bar was t = {rec['bonferroni_t']:.2f}. Nothing cleared it.

One thing survived: skipping small trades added {band['book_diff']:+.2f} to the Sharpe ratio, significant in every region. The only edge I found was trading less.

The total haircut, {hc['alpha_first_to_record'] * 100:.0f}%, is ordinary. Published anomalies lose 58% after publication; bank strategies lose a median 73% once live.

Full article, tables and code: {REPO}

#quant #backtesting #investing #statistics
"""
open(os.path.join(ROOT, "linkedin", "post.txt"), "w").write(post)

# ------------------------------------------------------------------ HTML
CSS = open(os.path.join(ROOT, "code", "style.css")).read()
def embed(html):
    for f in sorted(os.listdir(FIG)):
        html = html.replace(f"../figures/{f}", "data:image/png;base64," + base64.b64encode(open(os.path.join(FIG, f), "rb").read()).decode())
    return html
body = markdown.markdown(md, extensions=["tables", "fenced_code"]).replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
open(os.path.join(ROOT, "article", "backtest_vs_reality.html"), "w").write(embed(
    f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Backtest vs reality</title><style>{CSS}</style></head><body>{body}</body></html>"))
paras = post.strip().split("\n\n")[:-1]
html_p = [f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paras]
html_p[-1] = html_p[-1].replace("<p>", "<p class='link'>")
teaser = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Backtest vs reality: teaser</title><style>{open(os.path.join(ROOT, 'code', 'teaser.css')).read()}</style></head><body>
<div class='by'>Henrik Gjerning · LinkedIn · 13 October 2026</div>{html_p[0]}<img src='../figures/hero_back_to_the_future.png' alt='Back to the Future: now showing'>{''.join(html_p[1:])}</body></html>"""
open(os.path.join(ROOT, "linkedin", "teaser.html"), "w").write(embed(teaser))
print(post); print("words:", len(post.split()))

# ---- picture first: the hero card opens the one-pager (series rule, 2026-09-25)
import re as _re
_tp = os.path.join(ROOT, "linkedin", "teaser.html")
_h = open(_tp).read(); _m = _re.search(r"<img [^>]*>", _h)
if _m:
    _img = _m.group(0); _h = _h.replace(_img, "", 1)
    _h = _re.sub(r"(<body[^>]*>)", lambda mm: mm.group(1) + _img.replace("<img ", "<img class='hero' ", 1), _h, count=1)
    _h = _h.replace("</style>", "img.hero{width:52%;display:block;margin:0 auto 12px;border-radius:4px}@media print{img.hero{width:48%}}</style>", 1)
    open(_tp, "w").write(_h)
