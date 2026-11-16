import re
# -*- coding: utf-8 -*-
"""Render A08 'Video Killed the Radio Star' (teaser + deep article + PDFs)."""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from common import click_layout, make_pdfs, write_article, write_readme, write_teaser  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES = os.path.join(ROOT, "results")
S = json.load(open(os.path.join(RES, "summary.json"))); R = S["reported"]; a1, a2 = S["A08-1"], S["A08-2"]
V = json.load(open(os.path.join(RES, "pubyear_sensitivity.json")))
RB = json.load(open(os.path.join(RES, "robustness_2026-10-23.json")))   # 23 Oct 2026 stress test: reported, not tested
RP, SH, FE = RB["registered_placebo"], RB["shuffle_placebo"], RB["month_fixed_effects"]
import csv as _csv   # 23 Oct 2026: programme count and q-values read from the rebuilt gate (one source for every article)
_G = {r["trial"]: r for r in _csv.DictReader(open(os.path.join(ROOT, "..", "PROGRAMME_GATE.csv"), encoding="utf-8"))}
_GM = open(os.path.join(ROOT, "..", "PROGRAMME_GATE.md"), encoding="utf-8").read()
N_PROG = int(re.search(r"counted as (\d+) for the multiple-testing", _GM).group(1))
Q_BH = {k: float(_G[k]["q_BH"]) for k in ("A08-1", "A08-2")}
HOLM = {k: _G[k]["holm5"] == "1" for k in Q_BH}
_fdr = lambda q: "passes at a 5% false discovery rate" if q < 0.05 else ("passes at 10%, not at 5%" if q < 0.10 else "fails at both 5% and 10%")
T = pd.read_csv(os.path.join(RES, "decay_by_factor.csv"), index_col=0).sort_values("year")
SIG = T[T.post_t > 2].sort_values("post_t", ascending=False)   # individually significant after publication
REPO = "hgjerning.github.io/now-showing/video-killed-the-radio-star"; STEM = "video_killed_the_radio_star"

T1 = f"""| Trial | Hypothesis | Estimate | t | p (one-sided) | Gate | Programme q (BH) | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| A08-1 | Factor returns fall after publication | **{a1['coef_ann']:+.1%}** a year ({a1['decay_share']:.0%} of the pre-publication average of {a1['pre_mean_ann']:.1%}) | {a1['t']:.2f} | {a1['p_lt']:.4f} | 0.025 | {Q_BH['A08-1']:.3f} | **PASS** |
| A08-2 | Factors still earn a positive return after publication | **{a2['ann']:+.1%}** a year (before costs) | {a2['t']:.2f} | {a2['p_gt']:.4f} | 0.025 | {Q_BH['A08-2']:.3f} | **PASS** |
"""
fmt = lambda v: "n/a" if pd.isna(v) else f"{v:+.0%}"
T2 = "| Factor | Paper | Data from | Before, % a year | After, % a year | t after | Decay |\n|---|---|---|---:|---:|---:|---:|\n" + "\n".join(
    f"| {r.label} | {r.paper} ({r.year}) | {r['first'][:4]} | {r.pre_ann * 100:+.1f} | {r.post_ann * 100:+.1f} | {r.post_t:.1f} | {fmt(r.decay) if r.pre_ann >= 0.01 else 'n/a'} |" for _, r in T.iterrows())
lo, hi = min(SH['net_decline_share'], RP['net_decline_share'], FE['share_of_pre_mean']), max(SH['net_decline_share'], RP['net_decline_share'], FE['share_of_pre_mean'])
sig_names = ", ".join(f"{r.label.lower()} (t {r.post_t:.1f})" for _, r in SIG.iterrows())

md = f"""# Video Killed the Radio Star: does publication kill a factor?

### 29 famous factors, before and after the paper that made them famous

![Now Playing](../figures/hero_video_killed.png)

*Henrik Gjerning · Rude Investment Consulting · Revised 23 October 2026 (stress test); publishes 17 November 2026 · Project 10, article A07 (registered as A08)*

> **In one paragraph.** Every factor has a birthday: the year a paper made it famous. McLean & Pontiff (2016) found that returns on 97 anomalies were 26% lower after the original sample ended and 58% lower after publication. I repeated the test on 29 of the best-known US factors (value, momentum, profitability, accruals, low volatility, MAX and more), using Jensen, Kelly & Pedersen's (2023) public factor data to 2025. **After publication, returns fell by {a1['coef_ann'] * -1:.1%} a year, {a1['decay_share']:.0%} of the pre-publication average** (t {a1['t']:.2f}), and they **stayed positive: {a2['ann']:+.1%} a year** on average (t {a2['t']:.2f}), before costs. Both pre-registered trials passed, as predicted. How much of the fall the papers *caused* is less clear. Random publication years produce a much smaller fall ({RP['mean_ann'] * -1:.1%}), but the real years cluster around 2000, just before a slump that hit every factor. Shuffling the real years between factors already produces a fall of {SH['mean_ann'] * -1:.1%}, and allowing for swings common to all factors leaves {FE['coef_ann'] * -1:.1%} (t {FE['t']:.1f}). Net of that slump, between about {lo:.0%} and {hi:.0%} of the old premium went with publication (reported, not tested).

**Statistics box.** JKP US factors: capped value-weighted tercile long-short, signed as the original paper predicts. Pre-publication = first month → December of the publication year; post = the following January → Dec 2025. A08-1: pooled regression of monthly returns on a post-publication dummy with factor fixed effects, standard errors clustered by month. A08-2: equal-weighted average of the factors in their post-publication months, NW t (6 lags). Registered placebo: 1,000 sets of random publication years (at least 10 years into each factor's data, no later than 2015). Two trials, gate 0.025. **Both passed.** Programme-wide ({N_PROG} trials, Benjamini–Hochberg): A08-1 q {Q_BH['A08-1']:.3f} ({_fdr(Q_BH['A08-1'])}), A08-2 q {Q_BH['A08-2']:.3f} ({_fdr(Q_BH['A08-2'])}); neither survives Holm at 5%. Robustness checks added in the 23 October stress test (shuffled real years, month fixed effects) are reported, not tested.

---

## 1. Why this matters now

Factor funds and ETFs sell published factors, and almost every product is marketed on a backtest that includes the years before the factor was published. Harvey, Liu & Zhu (2016) argued that many published factors are false discoveries; Hou, Xue & Zhang (2020) found that most fail to replicate once microcaps are handled carefully; Jensen, Kelly & Pedersen (2023) replied that most do replicate. McLean & Pontiff (2016) separated two effects: returns were 26% lower in the years after the original sample ended but before publication (a sign of data mining) and 58% lower after publication (data mining plus investors trading on the paper). Falck, Rej & Thesmar (2022) put out-of-sample performance at about half of in-sample. For anyone buying a factor fund, the number that matters is the post-publication return, not the backtest.

This design does not have each paper's sample-end date, so its "before" period pools the original sample, earlier data (JKP go back to 1926) and the post-sample years. It cannot separate data mining from arbitrage; its 51% is the counterpart of McLean & Pontiff's 58%, not of their 26%.

## 2. Results

**Table 1. The pre-registered trials**

{T1}

![Figure 1](../figures/fig1_before_after.png)

**Is it the paper, or just the calendar?** The registered placebo draws random publication years from each factor's own history. They produce an average fall of only {RP['mean_ann'] * -1:.1%} a year, and none of 1,000 sets is as low as the real {a1['coef_ann'] * -1:.1%} (the lowest is {RP['min_ann']:.1%}). That rules out a fall of this size by chance placement. It does not rule out the calendar. The real publication years average 2000, so most "after" months fall in the 2010s and early 2020s, when factor returns were weak across the board. Two checks added in the stress test (reported, not tested) take that into account:

- **Shuffled real years.** Giving each factor another factor's publication year ({SH['draws']:,} shuffles) produces an average fall of {SH['mean_ann'] * -1:.1%} a year; {SH['share_le_actual']:.1%} of shuffles are as low as the real fall.
- **Month effects.** Adding a separate effect for every month, which absorbs swings common to all factors, leaves a fall of {FE['coef_ann'] * -1:.1%} a year (t {FE['t']:.2f}), which would not pass the gate.

So most of the fall lines up with publication, but part of it is the post-2010 slump that hit every factor. Net of the slump, between about {lo:.0%} (shuffled years) and {hi:.0%} (registered placebo, month effects) of the old premium went with publication.

![Figure 2](../figures/fig2_placebo.png)

**After publication.** A08-2 averages, month by month, the factors that are past their publication year: {a2['ann']:+.1%} a year. Its early years rest on few factors: one in 1978, six by 1990, ten by 1997. The simpler average of the 29 factors' own post-publication returns is {T.post_ann.mean():.1%} a year, which is the number on the poster. Both are before costs.

## 3. Factor by factor

**Table 2. All 29 factors (reported)**

{T2}

*Decay = 1 − after/before. "n/a" where the pre-publication average is below 1% a year, where the ratio means little. Decays above 100% mean the factor turned negative after publication.*

The price-based signals faded most: short-term reversal, residual and intermediate momentum, seasonality. The profitability factors barely moved, and the other accounting-based factors (accruals, net operating assets, asset growth) lost about half, close to the average. Quality minus junk (an accounting-based factor) fell to almost nothing, but it has only {int(T.loc['qmj', 'post_n'])} months after its paper (t {T.loc['qmj', 'post_t']:.2f}). It is tempting to read this as "cheap-to-copy signals are arbitraged faster", but that was not tested, and the faders include the factors that are most expensive to trade because of their turnover (short-term reversal, momentum); McLean & Pontiff's "low arbitrage cost" refers to liquid, low-risk stocks, not to cheap data. Size and illiquidity turned negative after publication. Low beta (betting against beta) was negative both before and after in this unlevered, value-weighted form.

**Positive is not the same as reliable.** {int((T.post_ann > 0).sum())} of 29 factors stayed positive after publication, but only {len(SIG)} are significant on their own: {sig_names}. Many have short post-publication histories.

## 4. What this does and does not show

- **Verdict of record.** A08 uses JKP's published factor returns, not a stock list, so the 23 October rule (the corrected point-in-time list is the record) does not apply: the registered run is the record.
- **Correlation, not cause.** The tests show that returns fell after publication; they do not show that the papers caused it. The arbitrage explanation is McLean & Pontiff's, and the robustness checks above show that part of the fall is a common slump.
- **Publication years are the journal years** of the papers listed. Working-paper versions often circulated earlier, which would move the break forward.
- **Years checked against JKP's own factor-details table** (Jensen, Kelly & Pedersen, `Factor Details.xlsx`, bkelly-lab/ReplicationCrisis). 26 of 29 match. Three differ for a stated reason: for earnings/price JKP cite Basu's 1983 paper, I use his 1977 paper; for quality-minus-junk JKP give 2018 (online), the journal year is 2019; for cash-based profitability JKP give no citation (Ball et al., 2016). Re-run with JKP's years: fall {V['A08-1']['coef_ann']:.1%} a year (t {V['A08-1']['t']:.2f}) and post-publication return {V['A08-2']['ann']:.1%} (t {V['A08-2']['t']:.2f}); the factor-by-factor shares are unchanged. Both verdicts unchanged; reported, not a trial.
- **Before costs.** All returns are gross; no trading costs are modelled.
- **Unlevered, value-weighted terciles.** Factors built on small caps or with leverage (like the original BAB) behave differently.
- **29 factors, not 97 or 153.** I chose factors whose founding paper I could name with confidence. The full open-source library of Chen & Zimmermann (2022) would allow a broader test.
- **US only.** Jacobs & Müller (2020) find little post-publication decline outside the US. Linnainmaa & Roberts (2018) show that many accounting anomalies are also weak in the years *before* their original samples, another sign of data mining.
- **Programme count.** Two trials here; {N_PROG} in the programme-wide gate (23 October 2026).

## 5. Verdict

Both registered tests passed. After publication the average factor's return fell by about half, from {a1['pre_mean_ann']:.1%} to roughly 2% a year, and it stayed positive, before costs. What this study cannot say is how much of the fall the papers caused: the real publication years sit just before a slump that hit every factor, and net of that slump between about {lo:.0%} and {hi:.0%} of the old premium went with publication. For an investor the practical lesson survives either way: when you read a factor backtest, expect roughly half of the pre-publication return, and then ask whether the fee eats the rest.

## Reproduce

```bash
# data: download the JKP US factor returns (jkpfactors.com) and Factor Details.xlsx (github.com/bkelly-lab/ReplicationCrisis)
# into data/ (see data/README.md); they are not redistributed here.
python code/run_decay.py                  # A08-1..2 + placebo, results/summary.json
python code/check_pubyears.py             # publication years vs JKP's table
python code/robustness_2026-10-23.py      # shuffled years, month effects (reported, not tested)
python code/make_teaser_drawing.py && python code/make_figures.py && python code/build_article.py
```

## References

- Chen, A. Y. & Zimmermann, T. (2022). Open source cross-sectional asset pricing. *Critical Finance Review*, 11(2).
- Falck, A., Rej, A. & Thesmar, D. (2022). When systematic strategies decay. *Quantitative Finance*, 22(11).
- Harvey, C. R., Liu, Y. & Zhu, H. (2016). … and the cross-section of expected returns. *Review of Financial Studies*, 29(1).
- Hou, K., Xue, C. & Zhang, L. (2020). Replicating anomalies. *Review of Financial Studies*, 33(5).
- Jacobs, H. & Müller, S. (2020). Anomalies across the globe: once public, no longer existent? *Journal of Financial Economics*, 135(1).
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5).
- Linnainmaa, J. T. & Roberts, M. R. (2018). The history of the cross-section of stock returns. *Review of Financial Studies*, 31(7).
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance*, 71(1).
- The 29 founding papers are listed in Table 2 and in `PREREGISTRATION_A08_2026-09-25.md`.

*Not investment advice. Song title used as a cultural reference only; no lyrics are quoted.*
"""
write_article(ROOT, STEM, md, "Video Killed the Radio Star")

# 23 Oct 2026: click teaser (00_Planning/TEASER_STYLE_2026-10-21.md, as A04-A07). The post asks; the article answers
# (THE_INTERVAL.json A08 "click"). The verdict stays on the article's poster and in the article.
post = f"""VIDEO KILLED THE RADIO STAR: does publication kill a factor?

Factor funds sell value, momentum and profitability on backtests. Every one of those factors was made famous by a paper: value in 1985, momentum in 1993, gross profitability in 2013.

The claim: once a factor is published, its returns shrink. McLean & Pontiff (2016) found a 58% drop across 97 anomalies.

I tested it on 29 of the best-known US factors, 1926–2025, with the tests written down first. At first sight: before their papers, the 29 factors earned {a1['pre_mean_ann']:.1%} a year on average.

Three questions before you buy the backtest:
1. Is it the paper, or just the calendar?
2. Which stars faded, and which kept singing?
3. Is what's left worth paying for?

Your answer to question 1 in the comments, then check it here, with tables, code and the pre-registration: {REPO} · Not investment advice.

#factorinvesting #quant #investing #research
"""
write_teaser(ROOT, post, "hero_video_killed_teaser.png", "Video Killed the Radio Star", "17 November 2026")   # teaser poster asks, article poster answers
click_layout(ROOT, "teaser_radio.png", alt="Drawing: an old radio whose three dials hold the teaser's three questions")   # code/make_teaser_drawing.py
write_readme(ROOT, "A07 Video Killed the Radio Star: does publication kill a factor?", ["run_decay.py", "check_pubyears.py", "robustness_2026-10-23.py", "make_figures.py", "build_article.py"])
rd = os.path.join(ROOT, "README.md"); txt = open(rd, encoding="utf-8").read()
txt = txt.replace("TRIAL_LEDGER.md).\n\n", "TRIAL_LEDGER.md).\n\nFeature No. 7 (17 Nov 2026). Renumbered from A08 to A07 on 8 Nov 2026, when the original A06 was withdrawn; the pre-registration, trial IDs (A08-1, A08-2) and file names keep their registered A08 labels.\n\n", 1)   # 8 Nov 2026
txt = txt.replace("Raw Sharadar prices and fundamentals are licensed and are **not** included. Results files hold only derived statistics.",
                  "Data: Jensen, Kelly & Pedersen's public US factor returns (jkpfactors.com) and their Factor Details.xlsx; download into data/ (see data/README.md). They are not redistributed here. Results files hold only derived statistics.")
txt = txt.replace("Pipeline run: 25 September 2026.", "Pipeline run: 25 September 2026; robustness checks 23 October 2026.")
open(rd, "w", encoding="utf-8").write(txt.rstrip("\n") + "\nPublication slot: Tuesday 17 November 2026 (Now Showing No. 7).\n")
try:
    make_pdfs(ROOT, STEM)
except Exception as e:  # no browser here: print the PDFs elsewhere
    print("PDFs not built here:", type(e).__name__)
print(post); print("words", len(post.split()))
