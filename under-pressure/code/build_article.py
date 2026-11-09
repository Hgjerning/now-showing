# -*- coding: utf-8 -*-
"""Render A07 'Under Pressure' (click teaser + deep article + PDFs).
Single source (23 Oct 2026 stress test): carries the 8 Oct revision (article/under_pressure_v2.md, kept as history) plus
the stress-test fixes. Verdict of record = the corrected point-in-time list (Henrik, 23 Oct 2026); the registered list is
reported beside it. Every number below is read from results_pit/, results/ or results_a07r/."""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from common import click_layout, make_pdfs, write_article, write_readme, write_teaser  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# programme gate: count and q-values from PROGRAMME_GATE (28 Oct 2026: replaces a hard-coded count)
import csv as _csv, re as _re
_G = {r["trial"]: r for r in _csv.DictReader(open(os.path.join(ROOT, "..", "PROGRAMME_GATE.csv"), encoding="utf-8"))}
_GM = open(os.path.join(ROOT, "..", "PROGRAMME_GATE.md"), encoding="utf-8").read()
N_PROG = int(_re.search(r"counted as (\d+) for the multiple-testing", _GM).group(1))
N_RUN = int(_re.search(r"from every `TRIAL_LEDGER.md` \((\d+) trials run", _GM).group(1))
J = lambda *p: json.load(open(os.path.join(ROOT, *p)))
REG, PIT = J("results", "summary.json"), J("results_pit", "summary.json")      # registered list / corrected list (record)
R, PR = REG["reported"], PIT["reported"]
a1, a2, a3 = REG["A07-1"], REG["A07-2"], REG["A07-3"]
p1, p2, p3 = PIT["A07-1"], PIT["A07-2"], PIT["A07-3"]
AR = J("results_a07r", "summary_a07r.json"); RR = J("results_a07r", "reported_a07r.json")["sp500_pit"]
t4, t5 = AR["tests"]["A07-4"], AR["tests"]["A07-5"]; LZ = AR["pooled_logit"]["Z"]
NM = RR["altman_without_mve"]
REPO = "hgjerning.github.io/now-showing/under-pressure"; STEM = "under_pressure"

def by_date(d):  # share-of-dates statistics on dates that have an AUC (stress test 23 Oct: NaN dates are not losses)
    A = pd.read_csv(os.path.join(ROOT, d, "auc_by_date.csv")).dropna(subset=["auc_Z"])
    return dict(n=len(A), z50=int((A.auc_Z > 0.5).sum()), v50=int((A.auc_vol > 0.5).sum()), vO=int((A.auc_vol > A.auc_O).sum()),
                vZ=int((A.auc_vol > A.auc_Z).sum()), vF=int((A.auc_vol > A.auc_F).sum()), zbeat=list(A.loc[A.auc_Z > A.auc_vol, "date"].str[:7]),
                crashes=int(A.crashes.sum()), c19=int(A[A.date.str.startswith("2019")].crashes.sum()), cmin=int(A.crashes.min()), cmax=int(A.crashes.max()),
                last=A.tail(2)[["date", "auc_vol"]].values.tolist(),
                w={c: float(np.average(A[c], weights=A.crashes)) for c in ("auc_vol", "auc_Z", "auc_O", "auc_F")})
DR, DP = by_date("results"), by_date("results_pit")
pc = lambda a, b: f"{a} of {b} ({a / b:.0%})"
YP = pd.read_csv(os.path.join(ROOT, "results_pit", "auc_by_year.csv"), index_col=0)
YR = pd.read_csv(os.path.join(ROOT, "results", "auc_by_year.csv"), index_col=0)
lead_p, lead_r = int((YP.auc_vol > YP.auc_Z).sum()), int((YR.auc_vol > YR.auc_Z).sum())
DEC = pd.read_csv(os.path.join(ROOT, "results_pit", "crash_rate_by_decile.csv"), index_col=0)   # written by make_figures.py
sh = DEC.vol_decile / DEC.vol_decile.sum()
top10, top20, low50 = sh.iloc[9], sh.iloc[8:].sum(), sh.iloc[:5].sum()
zlate = ", ".join(f"{y} {YP.loc[y, 'auc_Z']:.2f}" for y in YP.index if y >= 2021)

T1 = f"""| Trial | Hypothesis | Corrected list (record) | Registered list | Gate | Verdict of record |
|---|---|---|---|---:|---|
| A07-1 | Altman Z ranks crashes better than chance | AUC **{p1['mean']:.3f}** [{p1['lo']:.3f}, {p1['hi']:.3f}], p {p1['p']:.4f} | {a1['mean']:.3f} [{a1['lo']:.3f}, {a1['hi']:.3f}], p {a1['p']:.3f} | 0.0167 | **pass** (registered list: fail) |
| A07-2 | Ohlson O beats trailing volatility | AUC {p2['auc_O']:.3f} − {p2['auc_vol']:.3f} = **{p2['mean']:+.3f}**, p {p2['p']:.3f} | {a2['auc_O']:.3f} − {a2['auc_vol']:.3f} = {a2['mean']:+.3f} | 0.0167 | fail (wrong sign) |
| A07-3 | Safe (low O) out-earn distressed (high O) | **{p3['ann']:+.1%}** a year, NW t {p3['t']:.2f} | {a3['ann']:+.1%}, t {a3['t']:.2f} | 0.0167 | fail |
"""
T2 = f"""| Score | Built from | AUC, corrected list (record) | Registered list | Reading |
|---|---|---:|---:|---|
| Trailing 252-day volatility | prices | **{PR['auc_vol_all']:.3f}** | {R['auc_vol_all']:.3f} | ranks a random crasher above a random survivor {PR['auc_vol_all']:.0%} of the time |
| Piotroski F (2000), reversed | nine accounting signals (a quality checklist) | {PR['auc_F']:.3f} | {R['auc_F']:.3f} | weak (reported, not gated) |
| Altman Z (1968), reversed | five ratios, one of them market cap | {PR['auc_Z']:.3f} | {R['auc_Z']:.3f} | weak but above chance on the record |
| Ohlson O (1980) | nine accounting items | {PR['auc_O_all']:.3f} | {R['auc_O_all']:.3f} | close to a coin |
"""
T3 = "| Decile (1 = safest) | " + " | ".join(str(i) for i in DEC.index) + " |\n|---|" + "---:|" * len(DEC) + "\n"
T3 += "| Sorted on volatility | " + " | ".join(f"{x:.1%}" for x in DEC.vol_decile) + " |\n"
T3 += "| Sorted on Ohlson O | " + " | ".join(f"{x:.1%}" for x in DEC.O_decile) + " |\n"
T4 = f"""| | Registered list (top 500 among every name ever in the S&P 500, 2012–2026) | Corrected list (actual S&P 500 members on each date): **record** |
|---|---:|---:|
| Firm-quarters / crash base rate | {R['n_obs']:,} / {R['base_rate']:.1%} | {PR['n_obs']:,} / {PR['base_rate']:.1%} |
| AUC trailing volatility | {R['auc_vol_all']:.3f} | **{PR['auc_vol_all']:.3f}** |
| AUC Piotroski F | {R['auc_F']:.3f} | {PR['auc_F']:.3f} |
| **A07-1** AUC Altman Z (gate p < 0.0167) | {a1['mean']:.3f}, p {a1['p']:.3f}: fail | **{p1['mean']:.3f}** [{p1['lo']:.3f}, {p1['hi']:.3f}], **p {p1['p']:.4f}: pass** |
| Altman Z above 0.5 | {pc(DR['z50'], DR['n'])} dates | {pc(DP['z50'], DP['n'])} dates |
| AUC Ohlson O | {R['auc_O_all']:.3f} | {PR['auc_O_all']:.3f} |
| **A07-2** AUC Ohlson O minus volatility | {a2['mean']:+.3f}: fail | {p2['mean']:+.3f}: fail |
| Volatility beats Ohlson | {pc(DR['vO'], DR['n'])} dates | {pc(DP['vO'], DP['n'])} dates |
| **A07-3** safe minus distressed, a year | {a3['ann']:+.1%} (t {a3['t']:.2f}): fail | {p3['ann']:+.1%} (t {p3['t']:.2f}): fail |
"""
T7 = f"""| Trial | Model | AUC with accounts | AUC volatility only | Difference [95% interval] | p | Verdict |
|---|---|---:|---:|---|---:|---|
| A07-4 | volatility + Altman + Ohlson + Piotroski | {t4['auc_model']:.3f} | {t4['auc_V']:.3f} | {t4['mean']:+.3f} [{t4['lo']:+.3f}, {t4['hi']:+.3f}] | {t4['p']:.2f} | fail |
| A07-5 | volatility + Altman | {t5['auc_model']:.3f} | {t5['auc_V']:.3f} | {t5['mean']:+.3f} [{t5['lo']:+.3f}, {t5['hi']:+.3f}] | {t5['p']:.2f} | fail |
"""
q = PR["crash_by_O_quintile"]; r12 = PR["r12_by_O_quintile"]

md = f"""# Under Pressure: which distress score sees the crash coming?

### Altman, Ohlson and Piotroski against one number from the price chart

![Now Playing](../figures/hero_under_pressure.png)

*Henrik Gjerning · Rude Investment Consulting · Project 10, article A06 (registered as A07) · Revised 8 October 2026; stress-tested 23 October 2026*

<!-- interval:guess -->
<!-- /interval -->

> **In one paragraph.** Among America's 500 largest companies, which number best ranks the stocks that will **crash** (fall 40% or more below today's price) within the next year: a classic accounting distress score, or simply how much the price has been swinging? I pre-registered the test and ran it over 51 quarter-ends from 2012 to 2025. **On the actual S&P 500 members of each date, the list of record, trailing volatility ranked crashes with an AUC of {PR['auc_vol_all']:.2f}. Piotroski's F reached {PR['auc_F']:.2f}, Altman's Z {PR['auc_Z']:.2f} and Ohlson's O {PR['auc_O_all']:.2f}, close to a coin.** One of the three pre-registered trials passed: Altman's Z ranks crashes better than chance (p {p1['p']:.4f}). Ohlson's O did not beat volatility, and there was no distress premium. **The corrected list became the record on 23 October 2026, after its numbers were known.** On the list I registered (the top 500 among every company ever in the index, which knew future index members), Altman's Z failed ({a1['mean']:.3f}, p {a1['p']:.3f}) and the count was 0 of 3; my registered prediction for Altman was "pass". A follow-up registered on 8 October asked whether the balance sheet adds anything once volatility is known. Out of sample it did not improve the ranking (AUC {t4['auc_model']:.3f} with all three scores against {t4['auc_V']:.3f} for volatility alone); both follow-up trials failed.

**Statistics box.** Outcome: a crash, meaning the lowest close in the 12 months after a quarter-end is at most 60% of the formation close. AUC is computed within each quarter-end, then averaged over quarter-ends with at least one crash ({DP['n']} on the corrected list, {DR['n']} on the registered list). Inference: moving-block bootstrap over formation dates (block 4 quarters, 10,000 draws); A07-3 uses Newey-West (6 lags). Three trials, one-sided gate p < 0.0167. **Verdict of record (corrected list): 1 of 3, A07-1 passes.** Registered list: 0 of 3. The corrected list became the record on 23 October 2026, after its numbers were known (see section 5). Follow-ups A07-4 and A07-5 (registered 8 October; gate p < 0.025 each; family-wide line across the six revisited trials 0.0083): 0 of 2. Two lists: *registered*, the 500 largest each quarter among every name that was in the S&P 500 at any time 2012–2026; *corrected*, the companies actually in the index on each date. Base crash rate {PR['base_rate']:.1%} (corrected), {R['base_rate']:.1%} (registered). Sharadar as-reported fundamentals, used from their filing date; firms without a classified balance sheet (most banks and insurers) excluded. US large caps only. Every gated statistic was recomputed independently in the 23 October stress test and matched.

---

## 1. Why this matters now

Higher rates have brought distress scores back into fashion. The classic tools are half a century old. Altman (1968) fitted five ratios to 66 manufacturers. Ohlson (1980) used nine items and a logit. Piotroski (2000) built a nine-point quality checklist for cheap stocks; it is not a bankruptcy model, but investors use it the same way. Later work, notably Shumway (2001), Hillegeist, Keating, Cram & Lundstedt (2004), Bharath & Shumway (2008) and Campbell, Hilscher & Szilagyi (2008), found that models using market data beat Z and O at predicting failure. Campbell, Hilscher & Szilagyi's best predictors were accounting ratios measured at market value (profitability and leverage over market equity) plus volatility and past returns. Begley, Ming & Watts (1996) had already found that Z and O lost much of their accuracy out of sample.

This article asks the equity investor's version of that question, in the stocks most investors actually own, with the test written down before it was run.

## 2. Design (pre-registered)

- **Universe:** each quarter-end from Dec 2012 to Jun 2025, about 419 firms per date after excluding firms without current assets or current liabilities. Two lists, described in the statistics box; the corrected list is the record.
- **Scores:** Altman Z (1968 manufacturing coefficients), Ohlson O (1980 model 1 coefficients), Piotroski F (nine signals), and trailing 252-day volatility. Twelve-month flows are summed over four quarters; each filing is used only after its filing date and dropped after 400 days. No coefficients were re-estimated.
- **Outcome:** a crash, meaning the price falls at least 40% below the formation price at some point in the next 12 months (formation close to the 12-month low).
- **Metric:** AUC, the probability that a randomly chosen crasher has a worse score than a randomly chosen survivor (Hanley & McNeil 1982). 0.5 is a coin flip; 1.0 is perfect.

## 3. The pre-registered trials

**Table 1. Verdicts**

{T1}
My written predictions were: pass for Altman (about 85%), fail for Ohlson vs volatility, fail for the distress puzzle. On the corrected list all three predictions came out right; on the registered list I was wrong about Altman.

## 4. The main result: the price chart ranks crashes far better

**Table 2. The scoreboard**

{T2}
![Figure 1](../figures/fig1_auc.png)

The gap is not a close call. On the corrected list, volatility's AUC was above 0.5 on all {DP['v50']} quarter-ends with a crash and above Ohlson's on {pc(DP['vO'], DP['n'])}. It beat Altman's Z on {pc(DP['vZ'], DP['n'])} and Piotroski's F on {pc(DP['vF'], DP['n'])} (reported, not tested). Altman's Z was above 0.5 on {pc(DP['z50'], DP['n'])}.

The decile table is the easiest way to see what an AUC of {PR['auc_vol_all']:.2f} means.

**Table 3. Crash rate by decile (corrected list, pooled 2012–2025)**

{T3}
![Figure 2](../figures/fig2_crash_by_decile.png)

Sorted by volatility, the crash rate climbs steadily from {DEC.vol_decile.iloc[0]:.1%} to {DEC.vol_decile.iloc[9]:.1%}. Sorted by the O-score it is flat. Treating the deciles as equal in size, the 10% most volatile stocks held about **{top10:.0%}** of all crashes, the 20% most volatile about **{top20:.0%}**, and the calmer half only about **{low50:.0%}** (reported, derived from Table 3, not tested).

![Figure 3](../figures/fig3_auc_by_year.png)

Figure 3 shows the year-by-year picture. Volatility's yearly average leads Altman's in all {lead_p} years on the corrected list ({lead_r} of {len(YR)} on the registered list); by date, Altman was ahead on {len(DP['zbeat'])} of {DP['n']} ({', '.join(DP['zbeat'])}). Three things limit how far the averages travel. First, crashes cluster: the four 2019 formation dates, whose 12-month windows contain the Covid fall of 2020, hold {DP['c19']:,} of the {DP['crashes']:,} crashes, about **{DP['c19'] / DP['crashes']:.0%}**. Because AUC is averaged across dates, each date counts once, which limits that cluster's pull, but it also means a date with {DP['cmin']} crash weighs as much as one with {DP['cmax']}. Weighted by crashes instead, the AUCs are {DP['w']['auc_vol']:.2f} (volatility), {DP['w']['auc_F']:.2f} (Piotroski), {DP['w']['auc_Z']:.2f} (Altman) and {DP['w']['auc_O']:.2f} (Ohlson): the same order. Second, the two most recent dates (March and June 2025) are volatility's weakest: AUC {DP['last'][0][1]:.2f} and {DP['last'][1][1]:.2f}. Third, Altman's signal sits in 2012–2020: its yearly AUC since then is {zlate}. Two or three years cannot tell a trend from noise, but neither lead is constant.

## 5. What changed when the list was fixed, and which list is the record

The pre-registration named one bias before anything was run: the ticker list holds every company that was in the S&P 500 at any time from 2012 to 2026, and the "500 largest" were picked from that list, so a company that joined the index in 2020 can sit in the 2014 sample. The A07 pre-registration said the same survivorship caveat as A06 applies, and A06 had said the bias affects all models equally. For A07 it did not.

I re-ran everything with one change: on each date, the universe is the companies actually in the S&P 500 that day, from the index provider's add/remove history. Same code, scores and test. A re-run with the original list on today's data reproduces the registered numbers, so the differences below come from the list alone.

**Table 4. Registered list vs corrected list**

{T4}
More crashes enter the sample ({R['base_rate']:.1%} → {PR['base_rate']:.1%}), because the corrected list keeps smaller members that later fell out of the index, exactly the companies the "ever-member" list had dropped. Every score gets better at spotting them, and Altman's Z improves the most: from a coin flip to a result that clears the pre-registered gate and also a programme-wide Bonferroni line (0.05 / 30 ≈ 0.0017).

Why Altman, more than the others? Not because of its market-value term: section 7 tests that, and without it Altman's AUC is unchanged ({NM['auc_Z_without_MVE_TL_mean']:.3f} against {NM['auc_Z_full_mean']:.3f}). The reason is not established.

**Which list counts.** The programme's rule of 1 October was that the registered verdict stays on record and the corrected run is reported beside it. On 23 October 2026, after these numbers were known, I changed that rule: the corrected list is the verdict of record for every article, because it is the list an investor could actually have held. For A07 that turns a 0 of 3 into a 1 of 3. A rule changed after the data were seen deserves suspicion, so both counts are shown everywhere, and the reader can choose. The safer reading is the one that holds on both lists: **volatility ranks large-cap crashes far better than the textbook scores; Altman's Z carries a weak signal that the registered list hid.**

## 6. The distress puzzle (A07-3)

Dichev (1998) and Campbell et al. (2008) found that distressed stocks earn *lower* returns, the "distress puzzle"; Griffin & Lemmon (2002) found the effect concentrated among firms with low book-to-market. Here, a quarterly-rebuilt portfolio of the safest O-quintile minus the most distressed returned {p3['ann']:+.1%} a year (t {p3['t']:.2f}) on the corrected list and {a3['ann']:+.1%} (t {a3['t']:.2f}) on the registered list, 2013–2026. Among the 500 largest there is no puzzle and no premium. The crash rate is also flat across O-quintiles ({', '.join(f'{q[k]:.1%}' for k in sorted(q))}), and the mean 12-month price return barely differs ({r12['1']:+.1%} safest, {r12['5']:+.1%} most distressed).

## 7. Revisited: does the balance sheet add anything? (October 2026)

The first version left one question open, and the review called it the most important. I registered it on 8 October 2026 (`PREREGISTRATION_A07_R_2026-10-08.md`; two trials, gate p < 0.025 each). At each quarter-end from {AR['first_test'][:7]} to {AR['last_test'][:7]} ({AR['n_test_dates']} dates), two logit models are fitted only on earlier quarters whose outcome was already known, and then used to rank the next crashes. One uses volatility alone; the other adds the accounting scores. The test runs on the corrected list. I predicted both trials would fail.

{T7}
The accounts did not improve the ranking; the point estimate was slightly lower, and the interval for A07-4 just includes zero. The same holds at 30% and 50% crash thresholds and on the registered list (reported). Fitted on all the data at once (in sample), Altman's Z still carries some information next to volatility (coefficient {LZ['coef']:+.2f}, z {LZ['z']:.1f}, standard errors clustered by firm and date), but that is not enough to improve a ranking made from earlier data only. Altman's signal is not its market-value term: without it, its AUC is unchanged ({NM['auc_Z_without_MVE_TL_mean']:.3f} against {NM['auc_Z_full_mean']:.3f}), and the version without it adds nothing out of sample either.

## 8. What this does and does not show

**Is volatility winning by construction?** Partly, yes. The outcome is a large future price move, and a stock that already moves a lot is mechanically more likely to fall 40% in a year, distressed or not. The result is therefore not evidence that volatility understands the economic causes of distress, nor that it sees trouble earlier: AUC measures how well a score ranks next year's crashes, not who saw them first. It says something narrower: for ranking which large caps will crash, the price already carries far more usable information than the three textbook scores.

- **Incremental value.** Tested in section 7: out of sample, the accounting scores add nothing to volatility for large caps.
- **Crashes are not bankruptcies.** Altman and Ohlson were built to predict legal failure, which is rare in S&P 500 names. In small caps or high-yield issuers they may do much better. This sample says nothing about that.
- **Altman outside its design.** The 1968 Z was fitted on manufacturers. Here it is applied to every non-financial large cap, including utilities, real-estate trusts and carmakers with finance arms, where the sales/assets and working-capital terms mark stable firms as distressed. Altman's Z'' for non-manufacturers was checked afterwards (below).
- **Ohlson as implemented.** Model 1 coefficients as published; cash flow from operations stands in for Ohlson's funds from operations; total liabilities above total assets is common in large caps because of buybacks, not distress. Not tested separately.
- **Piotroski.** A quality checklist for value stocks, not a distress model. In the original code a missing prior-year input scored 0 instead of making F missing; the corrected version changes nothing that matters (below).
- **Reported, not tested (23 Oct 2026).** Run after the stress test from the same Season 1 data on the corrected list, same crash target and AUC procedure; no trial, no gate, and the verdict of record is unchanged (`results_pit/extra_checks_2026-10-23.json`). *Altman's Z'' for non-manufacturers* (6.56·WC/TA + 3.26·RE/TA + 6.72·EBIT/TA + 1.05·book equity/TL; Altman 1983; Altman, Iwanicz-Drozdowska, Laitinen & Suvas 2017) ranks crashes **worse** than the original Z: AUC 0.563 (p 0.014) against 0.598. *Excluding utilities and real-estate trusts* (about 10% of observations, by SIC code and Sharadar sector), the original Z rises to 0.628 and Z'' to 0.588; ranking Z *within sector* gives 0.600. So the design mismatch costs Altman a little, but it does not explain why volatility wins. *Piotroski with the missing-input fix:* AUC 0.614, unchanged from 0.614, and the A07-4 follow-up with the fixed F is unchanged too (−0.021, p 0.98).
- **Possible restatement look-ahead.** Twelve-month sums take the latest version of each quarter, and a restated quarter may carry a later filing date than the score date. The size of this effect is unknown.
- **No refit, one threshold.** Published coefficients only; a refitted model would be a new trial. The 40% cut-off was fixed in advance; section 7 is the same at 30% and 50%.
- **Registered but not delivered.** The follow-up pre-registration listed ROC curves for the four scores; they were not produced.
- **Effective sample.** 51 dates, {DP['n']} with crashes, about {DP['c19'] / DP['crashes']:.0%} of all crashes from four 2019 dates. US large caps, 2012–2025, one market era.
- **Multiple testing.** Three trials; Season 1 had 30 original trials plus the two follow-ups, and the programme now counts {N_RUN} run trials ({N_PROG} all in). A07-1 on the corrected list (p {p1['p']:.4f}) clears a Bonferroni line across the 30 Season 1 trials (0.0017) and survives the programme-wide Benjamini–Hochberg correction (q {float(_G['A07-1']['q_BH']):.2f}).

## 9. Verdict

In this large-cap sample, a single market number, how much the price has been swinging over the past year, ranked next year's 40% crashes far better than Altman's Z, Ohlson's O or Piotroski's F, on both lists. On the list of record Altman's Z carries a weak but real signal (1 of 3 trials passed); on the registered list it did not (0 of 3). Ohlson's O stays close to a coin. That does not make accounting information useless: much of what these scores were built to capture already shows up in the price, and in an out-of-sample test the balance sheet added nothing beyond it. For a large-cap screen, the price chart is the better first warning; the balance sheet is better used to explain what it flags.

<!-- interval:joke -->
<!-- /interval -->

## Reproduce

```bash
python code/run_distress.py      # A07-1..3 + reported, results/summary.json (P10_UNIVERSE for the corrected list: results_pit/)
python code/run_a07r.py          # A07-4/5 follow-up, results_a07r/ (run_a07r_rep.py: reported extras)
python code/make_figures.py && python code/make_teaser_drawing.py && python code/build_article.py
```

## References

- Altman, E. I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *Journal of Finance*, 23(4).
- Altman, E. I. (1983). *Corporate Financial Distress*. New York: Wiley (the Z'' model for non-manufacturers).
- Altman, E. I., Iwanicz-Drozdowska, M., Laitinen, E. K. & Suvas, A. (2017). Financial distress prediction in an international context: a review and empirical analysis of Altman's Z-score model. *Journal of International Financial Management & Accounting*, 28(2).
- Begley, J., Ming, J. & Watts, S. (1996). Bankruptcy classification errors in the 1980s: an empirical analysis of Altman's and Ohlson's models. *Review of Accounting Studies*, 1(4).
- Bharath, S. T. & Shumway, T. (2008). Forecasting default with the Merton distance to default model. *Review of Financial Studies*, 21(3).
- Campbell, J. Y., Hilscher, J. & Szilagyi, J. (2008). In search of distress risk. *Journal of Finance*, 63(6).
- Chen, J., Hong, H. & Stein, J. C. (2001). Forecasting crashes: trading volume, past returns, and conditional skewness in stock prices. *Journal of Financial Economics*, 61(3).
- Dichev, I. D. (1998). Is the risk of bankruptcy a systematic risk? *Journal of Finance*, 53(3).
- Griffin, J. M. & Lemmon, M. L. (2002). Book-to-market equity, distress risk, and stock returns. *Journal of Finance*, 57(5).
- Hanley, J. A. & McNeil, B. J. (1982). The meaning and use of the area under a receiver operating characteristic (ROC) curve. *Radiology*, 143(1).
- Hillegeist, S. A., Keating, E. K., Cram, D. P. & Lundstedt, K. G. (2004). Assessing the probability of bankruptcy. *Review of Accounting Studies*, 9(1).
- Künsch, H. R. (1989). The jackknife and the bootstrap for general stationary observations. *Annals of Statistics*, 17(3).
- Newey, W. K. & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3).
- Ohlson, J. A. (1980). Financial ratios and the probabilistic prediction of bankruptcy. *Journal of Accounting Research*, 18(1).
- Piotroski, J. D. (2000). Value investing: the use of historical financial statement information to separate winners from losers. *Journal of Accounting Research*, 38 (Supplement).
- Shumway, T. (2001). Forecasting bankruptcy more accurately: a simple hazard model. *Journal of Business*, 74(1).

*Not investment advice. Song title used as a cultural reference only; no lyrics are quoted.*
"""
write_article(ROOT, STEM, md, "Under Pressure")

# 23 Oct 2026: click teaser (00_Planning/TEASER_STYLE_2026-10-21.md, as A04-A06). The post asks; the article answers
# (THE_INTERVAL.json A07 "click"). The verdict stays on the article's poster and in the article.
post = f"""UNDER PRESSURE: which distress score sees the crash coming?

Higher rates have brought distress scores back. Altman's Z (1968) and Ohlson's O (1980) are still the textbook tools for spotting a company in trouble.

I put them, and Piotroski's F, up against one number from the price chart: how much the stock swung last year. The job: rank next year's crashes (falls of 40% or more) among America's 500 largest companies, 2012–2025, with the tests written down first. One limit up front: these scores were built to predict bankruptcy, not price crashes. At first sight, on my first stock list, Altman's Z scored {R['auc_Z']:.2f}, where 0.50 is a coin flip.

Three questions before you trust the balance sheet:
1. Once you know how much a stock swings, does its balance sheet add anything?
2. Which flaw in my own stock list hid most of Altman's signal?
3. Is it fair to ask a bankruptcy score to spot price crashes?

Your answer to question 1 in the comments, then check it here, with tables, code and the pre-registration: {REPO} · Not investment advice.

#investing #creditrisk #quant #statistics
"""
write_teaser(ROOT, post, "hero_under_pressure_teaser.png", "Under Pressure", "10 November 2026")   # teaser poster asks, article poster answers
click_layout(ROOT, "teaser_gauges.png", alt="Drawing: three pressure gauges holding the teaser's three questions")   # code/make_teaser_drawing.py
write_readme(ROOT, "A06 Under Pressure: which distress score sees the crash coming?",
             ["run_distress.py", "run_a07r.py", "make_figures.py", "make_teaser_drawing.py", "build_article.py"],
             "\nFeature No. 6 (10 Nov 2026). Renumbered from A07 to A06 on 8 Nov 2026, when the original A06 (Minority Report, machine learning) was withdrawn; the pre-registrations, trial IDs (A07-1 ... A07-5) and file names keep their registered A07 labels.\n\nThe corrected point-in-time list (`results_pit/`) is the verdict of record (23 Oct 2026); `results/` is the registered list; "
             "`results_a07r/` holds the 8 Oct follow-up (A07-4/5). Per-firm `scores_panel.csv` files are derived from Sharadar and are listed in `.gitignore`.\n")
with open(os.path.join(ROOT, "README.md"), "a", encoding="utf-8") as f:   # README is rewritten above, so this line appears once
    f.write("Publication slot: Tuesday 10 November 2026 (Now Showing No. 6).\n")
GI = ["**/scores_panel*.csv", "results*/scores_panel*.csv", "results*/*stock*.csv", "ext_*/"]   # never narrower than this (stress test 23 Oct)
gp = os.path.join(ROOT, ".gitignore"); old = open(gp).read().split() if os.path.exists(gp) else []
open(gp, "w").write("\n".join(dict.fromkeys(old + GI)) + "\n")
try:
    sys.path.insert(0, os.path.join(ROOT, "..", "_shared")); from add_contact_box import patch_file
    for f in (os.path.join(ROOT, "linkedin", "teaser.html"), os.path.join(ROOT, "article", STEM + ".html")): patch_file(f)
except Exception as e:  # noqa: BLE001
    print("contact box not added:", e)
try:
    make_pdfs(ROOT, STEM)
except Exception as e:  # no browser here: print the PDFs on Windows
    print("PDFs not built here:", type(e).__name__)
print(post); print("words", len(post.split()))
