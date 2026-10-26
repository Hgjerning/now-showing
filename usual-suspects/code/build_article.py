# -*- coding: utf-8 -*-
"""Render A05 'The Usual Suspects' (teaser + deep article) from ../results and ../data.
Single source since the stress test of 23 Oct 2026: it carries the v2 changes of 8 Oct 2026 (article/CHANGES_v2.md) and the
stress-test fixes (STRESS_TEST_2026-10-23.md). usual_suspects_v2.* are kept as history only."""
import base64
import json
import os
import re
import sys

import markdown
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES, FIG, D = (os.path.join(ROOT, x) for x in ("results", "figures", "data"))
S = json.load(open(os.path.join(RES, "summary.json"))); Q = json.load(open(os.path.join(RES, "seventh_suspect.json")))
XS = json.load(open(os.path.join(RES, "a05_stress.json")))
us = pd.read_csv(os.path.join(RES, "suspects_us.csv"), index_col=0); q7 = pd.read_csv(os.path.join(RES, "suspects_us_with_qmj.csv"), index_col=0)
dev = pd.read_csv(os.path.join(RES, "suspects_developed.csv"), index_col=0)
ga = pd.read_csv(os.path.join(D, "guru_factor_attribution.csv")); ag = pd.read_csv(os.path.join(D, "art_recipes_gate.csv")).set_index("recipe")
REPO = "hgjerning.github.io/now-showing/usual-suspects"
FG = json.load(open(os.path.join(RES, "fake_gurus.json"))); OI = FG["own_ingredients"]
PA, PB = XS["placebo_published_direction"], XS["placebo_real_signs"]
WL = pd.read_csv(os.path.join(RES, "where_legends_died.csv"))
wl = lambda n, st: WL[(WL.recipe == n) & (WL.step == st)].alpha.iloc[0]
pc = lambda v, d=1: f"{v * 100:+.{d}f}%"
us["pass"] = us["pass"].astype(str) == "True"
order = us.sort_values("alpha_t", ascending=False)
LBL = {"Mkt-RF": "Mkt", "SMB": "Size", "HML": "Value", "RMW": "Prof", "CMA": "Inv", "Mom": "Mom"}
NAME = {"Fisher (price/sales)": "Ken Fisher (price/sales)"}
nm = lambda n: NAME.get(n, n)

T1 = "| Recipe (JKP legs) | Since | Raw premium /yr (t) | 6-factor alpha /yr (t) | R² | α 1963–94 | α 1995–2025 | α since 2012 (t) | Verdict |\n|---|---|---:|---:|---:|---:|---:|---:|---|\n"
for n, r in order.iterrows():
    T1 += (f"| {nm(n)} | {r['first']} | {pc(r.raw_ann)} ({r.raw_t:.2f}) | **{pc(r.alpha_ann)}** ({r.alpha_t:.2f}) | {r.r2:.2f} | {pc(r.alpha_h1)} | {pc(r.alpha_h2)} | "
           f"{pc(r.alpha_2012)} ({r.t_2012:.2f}) | {'**passes**' if r['pass'] else 'no robust alpha'} |\n")
T1 += "\n*The since-2012 column is reported, not tested.*"
T2 = "| Recipe | " + " | ".join(LBL.values()) + " |\n|---|" + "---:|" * 6 + "\n"
for n, r in order.iterrows():
    T2 += f"| {nm(n)} | " + " | ".join(f"{r[f'b_{k}']:+.2f}" + ("*" if abs(r[f't_{k}']) > 2 else "") for k in LBL) + " |\n"
T2 += "\n*\\* |t| > 2 (Newey–West, 6 lags).*"
ps = us[us["pass"]].index
cut = {p: (us.loc[p, "alpha_ann"] - q7.loc[p, "alpha_ann"]) / us.loc[p, "alpha_ann"] for p in ps}
oth = [p for p in ps if p != "Greenblatt"]
T3 = "| Recipe | α, 6 factors (t) | α, + quality (t) | QMJ loading (t) | Share of alpha taken by quality |\n|---|---:|---:|---:|---:|\n"
T3 += "\n".join(f"| {p} | {pc(us.loc[p, 'alpha_ann'])} ({us.loc[p, 'alpha_t']:.2f}) | {pc(q7.loc[p, 'alpha_ann'])} ({q7.loc[p, 'alpha_t']:.2f}) | {q7.loc[p, 'b_QMJ']:+.2f} ({q7.loc[p, 't_QMJ']:.1f}) | {cut[p] * 100:.0f}% |" for p in ps)
T4 = f"| Recipe | US α (t) | Developed-markets α (t), {XS['developed_window']['first']} to {XS['developed_window']['last']} |\n|---|---:|---:|\n"
T4 += "\n".join(f"| {nm(n)} | {pc(us.loc[n, 'alpha_ann'])} ({us.loc[n, 'alpha_t']:.2f}) | {pc(dev.loc[n, 'alpha_ann'])} ({dev.loc[n, 'alpha_t']:.2f}) |" for n in order.index)
labs = {"wesley_gray_quant_momentum": "Gray, quant momentum", "van_vliet_low_vol_multifactor": "van Vliet, low-vol multifactor",
        "wayne_thorp_earnings_revision": "Thorp, earnings revisions (IBES)", "wayne_thorp_surprise_proxy": "Thorp, earnings-surprise proxy",
        "meb_faber_shareholder_yield_core": "Faber, shareholder yield (core)"}
def lab(a):
    for k, v in labs.items():
        if a.startswith(k):
            return v
    return a
T5 = "| Screen (our reconstruction) | Universe | Weeks | Excess vs equal-weight universe /yr (t) | Alpha after own ingredients + 13 JKP themes /yr (t) |\n|---|---|---:|---:|---:|\n"
T5 += "\n".join(f"| {lab(r.arm)} | {r.universe} | {r.n_weeks} | {pc(r.excess_ann)} ({r.t_excess:.2f}) | {pc(r.alpha_legs_themes_ann)} ({r.t_alpha_legs_themes:.2f}) |" for r in ga.itertuples())
n_neg, n_sig = int((ga.excess_ann < 0).sum()), int((ga.t_excess < -2).sum())
gg, gm = ag.loc["greenblatt_type_value_profitability"], ag.loc["millennial_buyback_value_mom_profitability"]
SRC = [("Graham", "Benjamin Graham", "*The Intelligent Investor* (1949), defensive-investor criteria"),
       ("Greenblatt", "Joel Greenblatt", "*The Little Book That Beats the Market* (2006), the magic formula"),
       ("Buffett (quality)", "Warren Buffett", "no rule book: the recipe is quality-minus-junk, following Frazzini, Kabiller & Pedersen (2018)"),
       ("Lynch", "Peter Lynch", "*One Up on Wall Street* (1989), PEG approximation"),
       ("O'Neil CAN SLIM", "William O'Neil", "*How to Make Money in Stocks* (1988), CAN SLIM"),
       ("Dreman", "David Dreman", "*Contrarian Investment Strategies* (1998)"),
       ("Neff", "John Neff", "*John Neff on Investing* (1999)"),
       ("Zweig", "Martin Zweig", "*Winning on Wall Street* (1986)"),
       ("Fisher (price/sales)", "Kenneth Fisher", "*Super Stocks* (1984), price/sales"),
       ("Carlisle", "Tobias Carlisle", "*The Acquirer's Multiple* (2017)"),
       ("O'Shaughnessy growth", "James O'Shaughnessy", "*What Works on Wall Street* (1996 and later editions)"),
       ("O'Shaughnessy value", "James O'Shaughnessy", "*What Works on Wall Street*"),
       ("P. O'Shaughnessy millennial", "Patrick O'Shaughnessy", "*Millennial Money* (2014)"),
       ("Piotroski-type small growth", "Joseph Piotroski (academic)", "Piotroski (2000), F-score"),
       ("Mohanram P/B growth", "Partha Mohanram (academic)", "Mohanram (2005), G-score"),
       ("Motley Fool small-cap growth", "The Motley Fool", "small-cap growth criteria as summarised in Project1 (no single book)")]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_suspects import RECIPES  # noqa: E402
T7 = "| Recipe | Rules published by | Source of the rules | JKP legs (− = short) |\n|---|---|---|---|\n"
T7 += "\n".join(f"| {nm(r)} | {who} | {src} | `{' '.join(RECIPES[r])}` |" for r, who, src in SRC)
sc = XS["scorecard"]; lag = XS["nw_lag_sensitivity"]; m11 = XS["medians_11_nonpassers"]; s12 = sc["alpha_since_2012_smaller"]
dv = XS["developed_window"]["by_t"]

md = f"""# The Usual Suspects: fifteen legends, one Fool, one regression

### Are the published rules of Graham, Buffett, Lynch, Greenblatt and friends anything more than value, momentum and quality in disguise?

![Now Showing](../figures/hero_usual_suspects.png)

*Henrik Gjerning · Rude Investment Consulting · September 2026, revised 8 October and 23 October 2026 · Project 10, article A05*

*Revised after an external review (8 Oct) and a stress test with three referees (23 Oct). The pre-registered result is unchanged.*

> **In one paragraph.** I rebuilt sixteen famous stock-picking rule sets as factor recipes: twelve practitioners (one of them with two recipes), two academics' published screens and the Motley Fool. Each recipe is a small portfolio of academic factor legs that approximates the *published* rules. It is not anyone's portfolio. I ran each recipe through one regression on six standard factors: market, size, value, profitability, investment and momentum. **The median raw premium of {S['median_abs_raw'] * 100:.1f}% a year falls to a median alpha of {S['median_abs_alpha'] * 100:.1f}%.** The pre-registered trial asked whether at least one recipe keeps a robust alpha. **It passed: five recipes did** (the Buffett-quality, Graham, Mohanram, Greenblatt and Patrick O'Shaughnessy recipes), more than the one to three I predicted. **But five is not many.** Fake gurus built from published academic factors and put through exactly the same test pass about half the time, about {PA['mean']:.0f} of 16 on average; with the real recipes' overlaps kept, five or fewer happens in {PA['p_le_5'] * 100:.0f}–{PB['p_le_5'] * 100:.0f}% of fake panels. So surviving six factors is ordinary for a factor recipe. Quality accounts for much of what the survivors keep, though not all of it. All of this is about the rules that were written down, not the people.

**Statistics box.** Headline: median raw premium {S['median_abs_raw'] * 100:.1f}%/yr → median six-factor alpha {S['median_abs_alpha'] * 100:.1f}%/yr (medians of absolute values, across recipes). 16 recipes, US, monthly 1963–2025 (650–750 months each). Factors: Fama–French 5 + momentum (Kenneth French data, built independently of the JKP recipe legs; daily returns compounded to months). Newey–West t, 6 lags. Trial A05-1 (pre-registered): a recipe passes if |t(α)| > {S['gate_t']:.3f} (Bonferroni over 16, two-sided 5%) **and** α has the same sign in 1963–94 and 1995–2025. **Result: {S['n_pass']} of 16 pass; trial PASSED.** My pre-registered prediction (1–3 pass) was wrong. Median R² {S['median_r2']:.2f}. Programme trial count: 21. Reported, not gated: fake-guru placebos (independent fakes: pass rate {FG['pass_rate'] * 100:.0f}%, mean {FG['panel_mean']:.1f} of 16 per panel; keeping the real recipes' shared legs: mean {PB['mean']:.1f}–{PA['mean']:.1f}, P(5 or fewer) = {PA['p_le_5']:.2f}–{PB['p_le_5']:.2f}); a seventh factor (quality); developed markets {XS['developed_window']['first']} to {XS['developed_window']['last']} ({S['world_n_sig']} of 16 with |t| > {S['gate_t']:.3f}).

---

## 1. The line-up

Every famous investor has a book, and most books contain rules: low P/E, high earnings yield, strong balance sheet, rising earnings, relative strength. Services such as Validea turn those rules into screens and sell the portfolios. The academic question is older: are those rules *new* information, or combinations of factors we already know?

Project1 translated each rule set into **factor legs** from Jensen, Kelly & Pedersen's (2023) global factor database. The Graham recipe, for instance, is book-to-market, earnings yield, dividend yield, Altman Z and low debt. Each recipe is the equal-weight average of its long-short legs. The appendix lists every recipe, its legs and where the rules come from. The sixteen recipes come from twelve practitioners (James O'Shaughnessy has two), two academics (Piotroski and Mohanram) and the Motley Fool; "fifteen legends" in the title is a film-title pun for the fifteen recipes with a named author. One recipe needs a special note: Buffett never published screening rules, so the "Buffett" recipe is quality-minus-junk, following Frazzini, Kabiller & Pedersen's (2018) reading of his record.

> **What exactly is being tested?** Not Warren Buffett, Benjamin Graham, Peter Lynch or Joel Greenblatt. The test is of factor proxies built to approximate the rules published under their names. When this article says "the Graham recipe passes", it means the factor recipe inspired by Graham's published rules, not Graham. A poor proxy can overstate or understate what the rules contain, and the investors' actual portfolios, judgement and stock selection are not in the data.

A sceptic can put the design in one line: *you built factor portfolios and found that factor models explain them.* That is fair, and it sets the scope. The recipes are made of academic factor legs, so overlap with a factor model is expected. The test can show how much of the written-down rules decomposes into known factors. It cannot show whether the investors had skill.

## 2. The regression

For each recipe, monthly return = α + six factor loadings + noise. The six factors come from Kenneth French's library (Fama & French, 2015; Carhart, 1997), built independently of the JKP legs. The pre-registration (`PREREGISTRATION_A05_2026-09-25.md`) fixed the gate before the run and recorded my prediction: one to three recipes survive.

![Figure 1](../figures/fig1_suspects_dumbbell.png)

**Table 1. Sixteen recipes, one regression (sorted by alpha t-statistic)**

{T1}

**The pre-registered trial passed: five recipes clear the bar, not the one to three I predicted.** They are the recipes with **quality, safety or cash-flow content**. The Greenblatt recipe is return on capital plus earnings yield. The Graham recipe includes the Altman Z-score and low debt. The Buffett recipe is literally quality-minus-junk. The Mohanram recipe is cash flow and R&D. The Patrick O'Shaughnessy recipe combines payout, value, momentum and QMJ.

The other eleven leave no robust alpha (median R² {m11['r2']:.2f}, median |alpha| {m11['abs_alpha'] * 100:.1f}% a year). For four of them there was little to explain: the Zweig, Neff, O'Shaughnessy value and Motley Fool recipes had no significant raw premium to begin with. One is a borderline miss: the **Carlisle recipe keeps {pc(us.loc['Carlisle', 'alpha_ann'])} a year (t {us.loc['Carlisle', 'alpha_t']:.2f})**, with the same sign in both halves, larger than the Graham or Greenblatt recipes' alpha; it misses the Bonferroni bar, and with 24 Newey–West lags instead of 6 its t reaches {lag['24']['t_Carlisle']:.2f} and it would have passed (reported; the six-lag choice was pre-registered). The pure momentum and the other pure value recipes (O'Neil, Neff, Dreman, Ken Fisher, Lynch, O'Shaughnessy value and growth) are well explained, with R² between 0.72 and 0.86.

**Since 2012** every passer's alpha is smaller than its full-sample alpha, but the P. O'Shaughnessy recipe's barely ({pc(us.loc["P. O'Shaughnessy millennial", 'alpha_ann'])} to {pc(us.loc["P. O'Shaughnessy millennial", 'alpha_2012'])}, t {us.loc["P. O'Shaughnessy millennial", 't_2012']:.2f}), and the Buffett and Graham recipes, the two strongest over the full sample, have since-2012 t-statistics of {us.loc['Buffett (quality)', 't_2012']:.2f} and {us.loc['Graham', 't_2012']:.2f}. For the eleven others the since-2012 alpha *rose* for nine; none of them reaches the bar. My pre-registered expectation that the since-2012 alpha would be smaller "for almost every recipe" was wrong: {s12['n_smaller']} of 16.

## 3. Fake gurus: is five a lot?

Five passes out of sixteen needs a benchmark. If random combinations of published academic factors pass the same regression as often, the five say little about the legends' rules.

So I built fake gurus. Each draws one to five legs (the same mix of sizes as the real recipes) at random from the 153 US factors in the JKP database, takes each leg in the direction the literature says it pays, and averages them. Every fake goes through exactly the A05-1 procedure: six factors, Newey–West t, the {S['gate_t']:.3f} bar and the same-sign test in both halves. A harder version uses only the legends' own 29 signed legs ({XS['n_base_legs']} distinct factors), recombined. These checks were added after the first review; they are reported, not gated, and do not count as trials.

The stress test added one more version. The real recipes share legs (earnings yield appears in four, dividend yield in four, quality in two), and recipes that share legs pass or fail together. Independent fakes miss that, so they understate how much a panel's pass count can vary. The **structure-preserving placebo** keeps the real overlaps: in each of {PA['panels']:,} panels, every one of the {XS['n_base_legs']} distinct legs is swapped for a different random factor, and all sixteen recipes are rebuilt with the same sharing. It keeps exactly shared legs, not the correlation among related legs (the three QMJ legs, the various value ratios), so it may still understate the spread.

![Figure 4](../figures/fig4_fake_gurus.png)

**Table 2. The legends' recipes against fake gurus**

| | Pass rate | Passes out of 16 | Chance of 5 or fewer out of 16 |
|---|---:|---:|---:|
| The 16 legends' recipes | {FG['real_n_pass'] / 16 * 100:.0f}% | {FG['real_n_pass']} (actual) | |
| Independent fakes, any of 153 factors ({FG['n_fakes']:,}) | {FG['pass_rate'] * 100:.0f}% | {FG['panel_mean']:.1f} on average; 95th percentile {FG['panel_q95']:.0f} | {FG['p_le_real']:.2f} (±{XS['independent_placebo_mc_se_p']:.2f}) |
| Independent fakes, the legends' own factors ({OI['n']:,}) | {OI['pass_rate'] * 100:.0f}% | {OI['expected_of_16']:.1f} on average | {OI['p_le_real']:.2f} |
| Real overlaps kept, legs in their published direction ({PA['panels']:,} panels) | {PA['mean'] / 16 * 100:.0f}% | {PA['mean']:.1f} on average (SD {PA['sd']:.1f}) | {PA['p_le_5']:.2f} (±{PA['mc_se_p']:.2f}) |
| Real overlaps kept, the real recipes' signs ({PB['panels']:,} panels) | {PB['mean'] / 16 * 100:.0f}% | {PB['mean']:.1f} on average (SD {PB['sd']:.1f}) | {PB['p_le_5']:.2f} (±{PB['mc_se_p']:.2f}) |

*± is the Monte Carlo standard error. Independent fakes: seed 42, panels of 16 ({FG['panels']}); overlap-preserving: seeds 5051 and 5052.*

**The legends' recipes do no better than random recipes built from published academic factors.** A random recipe passes about half the time, and a panel of sixteen typically produces six to eight passes. With the real overlaps kept, five or fewer happens in {PA['p_le_5'] * 100:.0f}–{PB['p_le_5'] * 100:.0f}% of panels: five is ordinary. The reading is narrow: passing six factors is not a mark of distinction for a factor recipe, and five passes is about what sixteen random recipes from the published-anomaly zoo give. The right panel of Figure 4 adds one detail: for a similar raw premium, the legends' recipes leave less alpha than the fakes. They are more "usual", not less.

The benchmark is demanding in one way. The fakes take each factor in the direction its academic paper found, and most of those papers were published after 1963, so they are well-informed gurus; Jensen, Kelly & Pedersen (2023) find that most published factors replicate, which is why random draws from that pool pass so often. Some real recipes hold legs against the published direction (low debt, large size, low book-to-market), which the "real signs" row reproduces.

## 4. Fingerprints: who did it

**Table 3. Factor loadings**

{T2}

![Figure 2](../figures/fig2_fingerprints.png)

The fingerprints read like the books. The O'Neil (CAN SLIM) recipe is mostly momentum. The Dreman and Neff recipes are value with a profitability tilt. The Motley Fool recipe earns little to explain ({pc(us.loc['Motley Fool small-cap growth', 'raw_ann'])} a year), tilts to small caps, and is the least explained of the group (R² {us.loc['Motley Fool small-cap growth', 'r2']:.2f}).

![Figure 5](../figures/fig5_where_legends_died.png)

**Where the legends died.** Figure 5 lets the suspects in one at a time. The Lynch recipe starts at {pc(wl('Lynch', 'Raw premium'))} a year; the market factor lifts it to {pc(wl('Lynch', '+ Market'))} (its market loading is negative), value cuts it to {pc(wl('Lynch', '+ Value'))} and profitability to {pc(wl('Lynch', '+ Profitability'))}. The Greenblatt recipe dies mostly at profitability ({pc(wl('Greenblatt', '+ Value'))} to {pc(wl('Greenblatt', '+ Profitability'))}) and then at quality. The Buffett and Graham recipes lose little to the six factors; the Buffett recipe even gains at first, because its negative market and value loadings mean the raw premium understates it. Quality then takes about half of the Buffett recipe's alpha and a third of the Graham recipe's. The two survivors not discussed so far follow the same pattern. The Mohanram recipe gains when value enters ({pc(wl('Mohanram P/B growth', '+ Size'))} to {pc(wl('Mohanram P/B growth', '+ Value'))}, a negative value loading: it holds growth stocks), then loses most at momentum and quality, ending at {pc(wl('Mohanram P/B growth', '+ Quality (QMJ)'))}. The P. O'Shaughnessy recipe is lifted by the market factor to {pc(wl("P. O'Shaughnessy millennial", '+ Market'))}, then worn down step by step by value, profitability and momentum to {pc(wl("P. O'Shaughnessy millennial", '+ Momentum'))}, and quality takes it to {pc(wl("P. O'Shaughnessy millennial", '+ Quality (QMJ)'))}. The Lynch panel is the contrast: a recipe that did not survive, where value and profitability take everything. The order of entry is a choice: a different order moves the steps, not the end points.

## 5. The seventh suspect: quality (explanatory, not confirmatory)

The quality regression was not part of the pre-registered decision rule. It was added after the primary result to ask one question: do the passers share a common omitted exposure? It is also partly circular, because the Buffett and P. O'Shaughnessy recipes contain JKP's own QMJ legs. Read it as interpretation, not as a test. Asness, Frazzini & Pedersen (2019) show that quality-minus-junk carries alpha against the three-factor and Carhart models (against the five-factor model much of it is absorbed by profitability); here it still loads strongly after the five factors and momentum (Table 4), so I added their US QMJ factor as a seventh regressor.

**Table 4. The five passing recipes, before and after quality**

{T3}

![Figure 3](../figures/fig3_seventh_suspect.png)

With quality added, the Greenblatt recipe's alpha falls to {pc(q7.loc['Greenblatt', 'alpha_ann'])} (t {q7.loc['Greenblatt', 'alpha_t']:.2f}): on this evidence the magic-formula recipe is quality plus value. For the other four, quality takes {min(cut[p] for p in oth) * 100:.0f}–{max(cut[p] for p in oth) * 100:.0f}% of the alpha, and they keep {min(q7.loc[p, 'alpha_ann'] for p in oth) * 100:.1f}% to {max(q7.loc[p, 'alpha_ann'] for p in oth) * 100:.1f}% a year, still with |t| above 3. All four combine safety (low leverage, Altman Z) or cash flow with value, a known academic cluster; but six factors plus quality do not explain all of what they keep.

## 6. Other published screens as real portfolios (Project1, reported)

Factor recipes are long-short, rebalanced monthly, cost-free and spread across thousands of stocks. A real screen is a long-only list of names. Project1 built **four other published rule sets, not among the sixteen** (Gray, van Vliet, Thorp and Faber), as real stock portfolios on two kinds of universe: point-in-time historical data (ART, 2003–2013, in-sample on ART's own universe) and today's index members (live, 2015–2026; survivor-biased, price returns only). These are our reconstructions of the published screens, not the managers' funds. The live Thorp rows use an earnings-surprise proxy, not earnings revisions. The numbers are copied from Project1 (aggregates only), not re-estimated.

**Table 5. Four other screens against their own universe (Project1, reported)**

{T5}

{n_neg} of the 12 rows trail their universe; {n_sig} do so significantly (t below −2). On the point-in-time data only Faber's shareholder yield beat its universe, and after its ingredients its t falls below 2. On the live universes, Gray's momentum and van Vliet's low-vol screens trailed by 5–6% a year in the US. Among Project1's pre-registered stock-level recipes on the point-in-time data, a **Greenblatt-type** value-plus-profitability recipe passed (Sharpe {gg.sharpe:.2f} vs {gg.bench_sharpe:.2f}, P = {gg.p_sharpe_le0:.4f}), in-sample on ART's own universe; the **Millennial (P. O'Shaughnessy-type)** recipe did not (Sharpe difference {gm.sharpe_diff:+.2f}, P = {gm.p_sharpe_le0:.2f}).

## 7. Beyond the US (reported, not gated)

**Table 6. The same recipes in developed markets**

{T4}

Outside the US four of the five US passers (Graham, Buffett, Mohanram and P. O'Shaughnessy) are the only ones with |t| above {S['gate_t']:.3f}; the Greenblatt ({dv['Greenblatt']:.2f}) and Motley Fool ({dv['Motley Fool small-cap growth']:.2f}) recipes just miss. By size of alpha, the Greenblatt and Carlisle recipes are larger than the P. O'Shaughnessy recipe. No half-split is applied here, and the sample starts in {XS['developed_window']['first']} (French's developed momentum starts then; the pre-registration said 1990-07). These tests were not part of the decision rule.

## 8. Limits, and what would change my mind

- **Factor portfolios explained by factor models.** Overlap is expected by construction. The result establishes how much of the written rules decomposes into known factors, not absence of skill.
- **Rules, not people.** A better proxy could do better or worse. Frazzini, Kabiller & Pedersen (2018) decompose Buffett's *actual* record and find it largely explained by leveraged low-risk and quality exposure, but that is their study of his record, not this one.
- **Post hoc pieces.** The quality regression, the placebos and the decomposition were all added after the primary result. They interpret A05-1; they do not re-test it.
- **Gross of costs.** Long-short factor returns ignore trading costs and shorting constraints (Novy-Marx & Velikov, 2016). A residual of 1.5% a year gross is fragile.
- **Publication.** Most legs were published during the sample; McLean & Pontiff (2016) predict decay. The passers' alphas are smaller since 2012 (one only slightly), but the other recipes' alphas rose, so this is not general decay.
- **Multiple testing.** The Bonferroni gate controls error within the sixteen recipes, but the programme has now run 21 trials. Effect sizes and the placebo deserve more weight than any single t-statistic. The verdict does not depend on the lag choice: 0, 3, 6 or 12 lags give five passes, 24 lags six (Carlisle).
- **US-centred.** The gate is US only; other markets are reported.

**My pre-registered expectations, scored.** (1) "R² above 0.6 for the value-type recipes and O'Neil": right except the Graham recipe ({sc['R2_above_0.6_value_type_and_ONeil']['Graham']:.2f}). (2) "One to three pass, the rest with |α| below 2% a year": wrong, five passed, and the Carlisle recipe kept {pc(us.loc['Carlisle', 'alpha_ann'])}. (3) "Alpha since 2012 smaller for almost every recipe": wrong, {s12['n_smaller']} of 16.

**What would falsify the factor reading?** Three findings would. (1) Real recipes passing clearly more often than fake gurus, say in the top 5% of fake panels (more than {PA['q95']:.0f} of 16). (2) Passers whose alpha holds up after 2012 and after quality, rather than shrinking. (3) Stock-level screens of the same rules beating their universes after costs on point-in-time data. (2) shows up only for the P. O'Shaughnessy recipe, which itself contains QMJ as a leg; (3) only for the Greenblatt-type recipe, in-sample on ART's universe and before costs.

## 9. Verdict

The published rules of famous investors decompose largely into value, momentum, profitability, investment and quality. **The median premium falls from {S['median_abs_raw'] * 100:.1f}% to {S['median_abs_alpha'] * 100:.1f}% a year after six standard factors.** The pre-registered trial passed: five recipes keep a robust alpha, more than I expected. But five is about what random recipes from published academic factors produce. Quality accounts for much of what remains (most of the Greenblatt recipe's alpha and {min(cut[p] for p in oth) * 100:.0f}–{max(cut[p] for p in oth) * 100:.0f}% of the other four), but four recipes keep {min(q7.loc[p, 'alpha_ann'] for p in oth) * 100:.1f}–{max(q7.loc[p, 'alpha_ann'] for p in oth) * 100:.1f}% a year that six factors plus quality do not explain. None of this says the legends lacked skill. It says the part of their method they wrote down contains less information beyond known factors than is often assumed, and is now measurable with standard factor models and available in cheap funds. Whether the small residuals of the Graham, Buffett-quality, Mohanram and P. O'Shaughnessy recipes reflect omitted risk, imperfect factor measurement or real insight remains open.

## Appendix. The sixteen recipes, their legs and sources

{T7}

*Sources are the books or papers the rule summaries come from, as mapped by Project1; the legs are proxies chosen by Project1, not the authors' own definitions.*

## Reproduce

```bash
python code/run_suspects.py      # A05-1: 16 recipes x FF5+Mom, US; developed markets reported
python code/seventh_suspect.py   # reported: + AQR QMJ
python code/fake_gurus.py        # added after review, reported: fake-guru placebo, where the legends died
python code/a05_stress_checks.py # added after the stress test, reported: overlap-preserving placebo, lag sensitivity, scorecard
python code/make_figures_review.py
python code/make_figures.py && python code/build_article.py && python code/make_pdfs.py
```

Factor data: JKP (jkpfactors.com), Kenneth French data library, AQR data sets. Download the files from the providers; `data/` is excluded from the public repository (provider terms; the two Project1 summary files are licensed ART aggregates), and the results files hold only the outputs.

## References

- Asness, C. S., Frazzini, A. & Pedersen, L. H. (2019). Quality minus junk. *Review of Accounting Studies*, 24(1), 34–112.
- Carhart, M. M. (1997). On persistence in mutual fund performance. *Journal of Finance*, 52(1), 57–82.
- Fama, E. F. & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1–22.
- Frazzini, A., Kabiller, D. & Pedersen, L. H. (2018). Buffett's alpha. *Financial Analysts Journal*, 74(4), 35–55.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5), 2465–2518.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance*, 71(1), 5–32.
- Mohanram, P. S. (2005). Separating winners from losers among low book-to-market stocks using financial statement analysis. *Review of Accounting Studies*, 10(2–3), 133–170.
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies*, 29(1), 104–147.
- Piotroski, J. D. (2000). Value investing: the use of historical financial statement information to separate winners from losers. *Journal of Accounting Research*, 38 (Supplement), 1–41.
- Practitioner books the recipes draw on: Graham (1949) *The Intelligent Investor*; Greenblatt (2006) *The Little Book That Beats the Market*; Lynch (1989) *One Up on Wall Street*; O'Neil (1988) *How to Make Money in Stocks*; Dreman (1998) *Contrarian Investment Strategies*; Neff (1999) *John Neff on Investing*; Zweig (1986) *Winning on Wall Street*; K. Fisher (1984) *Super Stocks*; Carlisle (2017) *The Acquirer's Multiple*; J. O'Shaughnessy (1996) *What Works on Wall Street*; P. O'Shaughnessy (2014) *Millennial Money*.

*Not investment advice.*
"""
open(os.path.join(ROOT, "article", "usual_suspects.md"), "w").write(md)

# 23 Oct 2026: click teaser (00_Planning/TEASER_STYLE_2026-10-21.md, as A04). The post asks; the article answers
# (THE_INTERVAL.json A05 "click"). The verdict stays on the article's poster and in the article, not in the post.
post = f"""THE USUAL SUSPECTS: are the legends' stock-picking rules anything more than textbook factors?

Value, momentum and quality now come in ETFs for a few basis points. Yet whole businesses still sell the rules of Graham, Lynch, Greenblatt and O'Neil as stock screens, as if the rules held an edge of their own.

I rebuilt 16 of those rule sets as factor recipes (the rules they wrote down, not the investors' portfolios) and put each through one pre-registered regression on six textbook factors. At first sight the recipes earn a median premium of {S['median_abs_raw'] * 100:.1f}% a year.

Three questions before you buy the screen:
1. How much of that premium is left after six textbook factors, and which famous recipes turn out to be plain momentum or value?
2. Five recipes survive. Is that a lot, next to fake gurus built from random academic factors?
3. Who is the seventh suspect behind most of what the survivors keep?

Your answer to question 1 in the comments, then check it here, with tables, code and the pre-registration: {REPO} · Not investment advice.

#investing #factorinvesting #quant #valueinvesting
"""
sys.path.insert(0, os.path.join(ROOT, "..", "_shared", "lib10"))
try:
    import interval
    md2 = interval.add_to_md(ROOT, md); open(os.path.join(ROOT, "article", "usual_suspects.md"), "w").write(md2); md = md2
    post = interval.add_to_post(ROOT, post)
except Exception as e:  # noqa: BLE001
    print("interval not added:", e)
open(os.path.join(ROOT, "linkedin", "post.txt"), "w").write(post)

CSS = open(os.path.join(ROOT, "code", "style.css")).read()
def embed(html):
    for f in sorted(os.listdir(FIG)):
        html = html.replace(f"../figures/{f}", "data:image/png;base64," + base64.b64encode(open(os.path.join(FIG, f), "rb").read()).decode())
    return html
body = markdown.markdown(interval.strip(md) if "interval" in dir() else md, extensions=["tables", "fenced_code"]).replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>The Usual Suspects</title><style>{CSS}</style></head><body>{body}</body></html>"
try:
    html = interval.add_to_html(ROOT, html)
except Exception as e:  # noqa: BLE001
    print("interval html not added:", e)
open(os.path.join(ROOT, "article", "usual_suspects.html"), "w").write(embed(html))
from common import click_layout, write_teaser  # noqa: E402  (23 Oct 2026: click teaser, as A04)
write_teaser(ROOT, post, "hero_usual_suspects_teaser.png", "The Usual Suspects", "3 November 2026")   # teaser poster asks, article poster answers
click_layout(ROOT, "teaser_lineup.png", alt="Drawing: the three questions held up by three suspects in a police line-up")   # code/make_teaser_drawing.py
_tp = os.path.join(ROOT, "linkedin", "teaser.html")
print(post); print("words:", len(post.split()))
try:
    sys.path.insert(0, os.path.join(ROOT, "..", "_shared")); from add_contact_box import patch_file
    for f in (_tp, os.path.join(ROOT, "article", "usual_suspects.html")): patch_file(f)
except Exception as e:  # noqa: BLE001
    print("contact box not added:", e)
