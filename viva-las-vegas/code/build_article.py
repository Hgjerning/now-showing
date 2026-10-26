# -*- coding: utf-8 -*-
"""Render A04 'Viva Las Vegas' (teaser + deep article + PDFs)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from common import click_layout, make_pdfs, write_article, write_readme, write_teaser  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES = os.path.join(ROOT, "results")
S = json.load(open(os.path.join(RES, "summary.json"))); R = S["reported"]; a1, a2 = S["A04-1"], S["A04-2"]
# Universe-corrected re-run (2026-10-01): actual S&P 500 members at each date instead of the top 500 among every name
# ever in the index. Not a new trial; the verdict stays as pre-registered. See TRIAL_LEDGER.md.
import numpy as _np
import pandas as _pd
RP = os.path.join(ROOT, "results_pit"); PS = json.load(open(os.path.join(RP, "summary.json"))); PR = PS["reported"]; p2 = PS["A04-2"]


def beta_adjusted(d):
    """Reported, not gated: alpha of D1 - D10 against the equal-weighted average of the ten deciles (OLS)."""
    P = _pd.read_csv(os.path.join(d, "max_deciles_top500.csv"), index_col=0)
    m = P[[f"D{i}" for i in range(1, 11)]].mean(axis=1).values; y = (P["D1"] - P["D10"]).values
    X = _np.c_[_np.ones(len(m)), m]; b = _np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
    sa = _np.sqrt(e @ e / (len(y) - 2) * (1 / len(y) + m.mean() ** 2 / ((m - m.mean()) ** 2).sum()))
    return b[0] * 12, b[0] / sa


ba0, bt0 = beta_adjusted(RES); ba1, bt1 = beta_adjusted(RP)
# Reported, not gated (added 14 Oct 2026 after review): code/reported_factor.py
XS = json.load(open(os.path.join(RP, "reported_stress.json"))); XP, XC = XS["published"], XS["corrected"]
RF = json.load(open(os.path.join(RP, "reported_factor.json"))); RFp, RFc = RF["published"], RF["corrected"]
def al(u, s_, m): v = u["alpha"][s_][m]; return f"{v['alpha_ann'] * 100 + 0.0:+.1f} ({v['t']:.2f})".replace("(-0.00)", "(0.00)")
def ci(d): return f"{d['ci95'][0] * 100:+.1f} to {d['ci95'][1] * 100:+.1f}"
LD = RFc["alpha"]["D1-D10"]["FF5+Mom"]["loadings"]; BMc, BMp = RFc["by_market"], RFp["by_market"]
T5 = "| Alpha, % a year (NW t) | Market only (CAPM) | Fama–French 5 factors | 5 factors + momentum |\n|---|---:|---:|---:|\n"
for s_, lab in [("D1", "Decile 1, steadiest"), ("D10", "Decile 10, lottery"), ("D1-D10", "**Low-MAX minus high-MAX**")]:
    T5 += f"| {lab} | {al(RFc, s_, 'CAPM')} | {al(RFc, s_, 'FF5')} | {al(RFc, s_, 'FF5+Mom')} |\n"
T5 += f"| *Low minus high, published universe* | *{al(RFp, 'D1-D10', 'CAPM')}* | *{al(RFp, 'D1-D10', 'FF5')}* | *{al(RFp, 'D1-D10', 'FF5+Mom')}* |\n"
T7 = f"""| Actual S&P 500 members | Up-market months ({BMc['up']['months']}) | Down-market months ({BMc['down']['months']}) | 2022 (calendar year) |
|---|---:|---:|---:|
| Market, % (excess return in up/down months; total return in 2022) | {BMc['up']['mkt_ann'] * 100:+.0f} a year | {BMc['down']['mkt_ann'] * 100:+.0f} a year | {RFc['year_2022']['mkt'] * 100:+.1f} |
| Steadiest decile, % | {BMc['up']['D1_ann'] * 100:+.0f} a year | {BMc['down']['D1_ann'] * 100:+.0f} a year | {RFc['year_2022']['D1'] * 100:+.1f} |
| Lottery decile, % | {BMc['up']['D10_ann'] * 100:+.0f} a year | {BMc['down']['D10_ann'] * 100:+.0f} a year | {RFc['year_2022']['D10'] * 100:+.1f} |
| **Low-MAX minus high-MAX**, % | **{BMc['up']['spread_ann'] * 100:+.0f}** a year | **{BMc['down']['spread_ann'] * 100:+.0f}** a year | {(RFc['year_2022']['D1'] - RFc['year_2022']['D10']) * 100:+.1f} |
"""
A1, SPc, SPp = RF["A04-1"], RFc["spread"], RFp["spread"]
T6 = f"""| 500 largest, 2013–2026 (A04-2) | Published universe (top 500 among every name ever in the S&P 500) | Corrected universe (actual S&P 500 members on each date) |
|---|---:|---:|
| Low-MAX minus high-MAX, % a year (NW t) | {a2['ann'] * 100:+.1f} ({a2['t']:.2f}) | **{p2['ann'] * 100:+.1f}** ({p2['t']:.2f}) |
| Return, steadiest decile / lottery decile, % a year | {R['decile_ann']['D1'] * 100:.1f} / {R['decile_ann']['D10'] * 100:.1f} | {PR['decile_ann']['D1'] * 100:.1f} / {PR['decile_ann']['D10'] * 100:.1f} |
| Sharpe ratio (excess of T-bills), steadiest / lottery | {XP['sharpe_excess_D1']:.2f} / {XP['sharpe_excess_D10']:.2f} | **{XC['sharpe_excess_D1']:.2f} / {XC['sharpe_excess_D10']:.2f}** |
| 95% interval for the difference in Sharpe ratios (block bootstrap) | {XP['diff_ci95'][0]:+.2f} to {XP['diff_ci95'][1]:+.2f} | {XC['diff_ci95'][0]:+.2f} to {XC['diff_ci95'][1]:+.2f} |
| Beta, steadiest / lottery | {R['beta_D1']:.2f} / {R['beta_D10']:.2f} | {PR['beta_D1']:.2f} / {PR['beta_D10']:.2f} |
| 95% confidence interval, low minus high, % a year | {ci(RF['published']['spread'])} | {ci(RF['corrected']['spread'])} |
| Low minus high after allowing for market risk (CAPM alpha), % a year (t) | {al(RF['published'], 'D1-D10', 'CAPM')} | {al(RF['corrected'], 'D1-D10', 'CAPM')} |
| Verdict (gate p < 0.025) | fail, opposite sign | fail, opposite sign |
"""
# Reported, not gated (added 22 Oct 2026): Deutsche Bank's three questions (DB Quant Handbook, 10 Dec 2010) -> code/reported_db2010.py
DB = json.load(open(os.path.join(RP, "reported_db2010.json"))); DBr, DBv, DBl = DB["reversal"], DB["volatility"], DB["legs"]
def st(d): return f"{d['ann'] * 100:+.1f} ({d['t']:.2f})"
def sa(d): return f"{d['alpha_ann'] * 100:+.1f}% (t {d['t']:.2f})"
T8 = f"""| Actual S&P 500 members, {DB['window'][0][:7]} → {DB['window'][1][:7]} | Low minus high, % a year (NW t) |
|---|---:|
| MAX, deciles (baseline, today's data files) | {st(DB['baseline_spread'])} |
| MAX, quintiles | {st(DB['baseline_quintile_spread'])} |
| MAX quintiles within last month's return quintiles (reversal held fixed) | {st(DBr['max_reversal_neutral'])} |
| MAX quintiles within 60-day volatility quintiles (volatility held fixed) | {st(DBv['max_vol_neutral'])} |
| MAX with volatility removed (residual MAX, deciles) | {st(DBv['max_resid_vol'])} |
| Short-term reversal itself (last month's losers minus winners, deciles) | {st(DBr['rev_spread'])} |
| Long leg: steadiest decile minus all members | {st(DBl['long_D1_minus_EW'])} |
| Short leg: all members minus lottery decile | {st(DBl['short_EW_minus_D10'])} |
"""
REPO = "hgjerning.github.io/now-showing/viva-las-vegas"; STEM = "viva_las_vegas"
ins = R["jkp_insample_1963_2005"]

T1 = f"""| Trial | Hypothesis | Window | Mean, % a year | 95% CI | NW t | p (one-sided) | Gate | Verdict |
|---|---|---|---:|---:|---:|---:|---:|---|
| A04-1 | Low-MAX beats high-MAX, whole US market (JKP) | 2012–2025 | **{a1['ann'] * 100:+.1f}** | {ci(RF['A04-1'])} | {a1['t']:.2f} | {a1['p_gt']:.3f} | 0.025 | fail |
| A04-2 | Low-MAX beats high-MAX, 500 largest (first, hindsight list; verdict of record) | {a2['first'][:7]} → {a2['last'][:7]} | **{a2['ann'] * 100:+.1f}** | {ci(RF['published']['spread'])} | {a2['t']:.2f} | {a2['p_gt']:.3f} | 0.025 | fail (opposite sign) |
"""
T2 = "| Decile (1 = steadiest, 10 = lottery) | " + " | ".join(str(k) for k in range(1, 11)) + " |\n|---|" + "---:|" * 10 + "\n"
T2 += "| Return, % a year | " + " | ".join(f"{R['decile_ann'][f'D{k}'] * 100:.1f}" for k in range(1, 11)) + " |\n"
T3 = f"""| | Decile 1 (steadiest) | Decile 10 (lottery) |
|---|---:|---:|
| Average MAX (biggest daily gain in the month) | {R['avg_max_D1']:.1%} | {R['avg_max_D10']:.1%} |
| Volatility (60-day, annualised) | {R['vol_D1']:.0%} | {R['vol_D10']:.0%} |
| Beta | {R['beta_D1']:.2f} | {R['beta_D10']:.2f} |
| Sharpe ratio (excess of T-bills) | {XP['sharpe_excess_D1']:.2f} | {XP['sharpe_excess_D10']:.2f} |
"""

md = f"""# Viva Las Vegas: do lottery stocks still lose?

### The MAX effect after publication, and in the stocks most people own

![Now Playing](../figures/hero_viva_las_vegas.png)

*Henrik Gjerning · Rude Investment Consulting · September 2026, updated October 2026 · Project 10, article A04*

> **In one paragraph.** Bali, Cakici & Whitelaw (2011) found that stocks with the biggest one-day jumps in the past month ("lottery stocks") go on to underperform. Investors overpay for the chance of another jackpot. I pre-registered two tests. **Across the whole US market (JKP data), after the paper:** low-MAX minus high-MAX earned {a1['ann']:+.1%} a year (t {a1['t']:.2f}). That is positive, but not distinguishable from zero. **In the 500 largest US stocks, 2013–2026:** the lottery decile *beat* the steadiest decile by {-a2['ann']:.0%} a year. The catch: per unit of risk they were level (Sharpe ratios {XP['sharpe_excess_D1']:.2f} and {XP['sharpe_excess_D10']:.2f}), and the lottery decile had twice the beta ({R['beta_D10']:.1f} vs {R['beta_D1']:.1f}) during one of the strongest bull markets on record. In large caps, a lottery ticket was a leveraged bet on the market. Both trials failed. **Then I fixed a flaw flagged in advance** (in the pre-registration of the stock list A04 borrowed): the list knew which companies would later join the S&P 500. On the actual members of each date, the lottery decile's lead shrinks to {-p2['ann']:.0%} a year, and the steady names come out ahead per unit of risk ({XC['sharpe_excess_D1']:.2f} against {XC['sharpe_excess_D10']:.2f}), though not by a margin the data can confirm. **A factor model absorbs the rest:** lottery stocks are high-beta and low-profitability, and once market, size, value, profitability, investment and momentum are priced, low-MAX minus high-MAX is {RFc['alpha']['D1-D10']['FF5+Mom']['alpha_ann'] * 100:+.1f}% a year (t {RFc['alpha']['D1-D10']['FF5+Mom']['t']:.2f}, 95% interval roughly {RFc['alpha']['D1-D10']['FF5+Mom']['alpha_ann'] * 100 - 1.96 * abs(RFc['alpha']['D1-D10']['FF5+Mom']['alpha_ann'] * 100 / RFc['alpha']['D1-D10']['FF5+Mom']['t']):.0f}% to {RFc['alpha']['D1-D10']['FF5+Mom']['alpha_ann'] * 100 + 1.96 * abs(RFc['alpha']['D1-D10']['FF5+Mom']['alpha_ann'] * 100 / RFc['alpha']['D1-D10']['FF5+Mom']['t']):+.0f}%). Nothing detectable is left for MAX to explain, but a moderate discount cannot be ruled out. One caution: the tests could only have detected effects of about {A1['mde_ann']:.0%} a year or more, so “not detected” is not the same as “gone”.

**Statistics box.** A04-1: JKP US `rmax1_21d` factor (capped value-weighted terciles), Jan 2012 → Dec 2025, NW t (6 lags). A04-2: the top 500 by market cap among every name ever in the S&P 500 (a hindsight list, corrected in section 3); MAX = largest daily return in the formation month; equal-weighted deciles held one month; D1 − D10, NW t (3 lags). Two trials, one-sided gate 0.025. **Both failed**, also on the corrected universe in section 3. Reported, not gated (section 4): CAPM, Fama–French five-factor and five-factor-plus-momentum alphas (Ken French data, NW t, 3 lags), 95% confidence intervals, excess-return Sharpe ratios with block-bootstrap intervals, up- vs down-market months; (section 5) three checks from a 2010 bank research note: short-term reversal, volatility-neutral MAX, long vs short leg.

---

## 1. Why this matters now

Zero-commission apps, options on single stocks and the 2020–21 meme-stock wave made lottery-style trading more popular than ever. The behavioural theory is well established: investors with a taste for positive skewness overpay for it (Barberis & Huang 2008), and retail gamblers concentrate in lottery-like stocks (Kumar 2009). The question is whether the resulting underperformance survives outside the small-cap corner where it was found.

## 2. Results

**Table 1. The pre-registered trials**

{T1}

![Figure 1](../figures/fig1_deciles.png)

**Table 2. Returns by MAX decile, 500 largest, 2013–2026 (first, hindsight list)**

{T2}

**Table 3. What the lottery decile really was (first, hindsight list)**

{T3}

![Figure 2](../figures/fig2_jkp_max.png)

In the original sample period (1963–2005) the JKP MAX factor earned {ins['ann']:+.1%} a year (t {ins['t']:.2f}). This value-weighted, tercile-based version is milder than Bali et al.'s decile sort. After publication it earned about half of that. During the meme window (April 2020 → December 2021), low-minus-high MAX in the 500 largest stocks lost {-R['top500_meme_2020_04_2021_12']['ann']:.0%} a year ({-XC['meme']['spread_ann']:.0%} on the corrected universe): the lottery tickets won. But the window starts at the Covid low, and the market then rose {XP['meme']['mkt_excess_cum']:.0%} above T-bills in 21 months; after allowing for market risk the loss is about {-XC['meme']['capm_alpha_ann']:.0%} a year on either list. The meme window was mostly a high-beta rebound.

## 3. What changed when the universe was fixed

The pre-registration of A06, whose stock list A04 adopted, named one bias before anything was run (A04's own pre-registration did not repeat the warning, and called the list "point-in-time", which it was not): the ticker list holds every company that was in the S&P 500 at any time from 2012 to 2026, and the "500 largest" were picked from that list. A company whose stock jumped in 2015 and joined the index in 2019 can sit in the 2015 sample, as a lottery stock that is known to have won. The mechanism is simple: companies join the S&P 500 because their market value has grown, so a list built with hindsight is full of firms whose prices later went up. The steady names in decile 1 are mostly long-standing members, so hindsight changes little there. The jumpy, fast-growing names in decile 10 are where the future joiners sit, and that is where the bias lands. Table 4 shows it: decile 1's return barely moves ({R['decile_ann']['D1'] * 100:.1f}% → {PR['decile_ann']['D1'] * 100:.1f}%), while decile 10 loses almost 4 points ({R['decile_ann']['D10'] * 100:.1f}% → {PR['decile_ann']['D10'] * 100:.1f}%). I re-ran A04-2 with one change (1 October 2026, after the results; a robustness check, not a new trial, and Table 1 keeps the verdict of record): on each date, the universe is the companies actually in the S&P 500 that day, from the index provider's own add/remove history. Same code, same deciles. On the 1 October data files a re-run with the original list reproduced the published numbers, so the differences below come from the universe. Later data updates move both versions by 0.2–0.4 points and leave the gap near 3 points. The corrected universe is also not quite "the 500 largest": S&P adds companies only after they have been profitable, so part of the change is a different list, not only the removal of hindsight. A04-1 uses JKP factor data and does not change.

**Table 4. Published universe vs corrected universe**

{T6}

The verdict does not move: the lottery decile still out-earned the steadiest one in raw return. But two things change. The gap shrinks from {-a2['ann']:.0%} to {-p2['ann']:.0%} a year, and per unit of risk the order flips: on the first list the lottery decile was marginally ahead ({XP['sharpe_excess_D10']:.2f} against {XP['sharpe_excess_D1']:.2f}), on the corrected one the steady decile is ({XC['sharpe_excess_D1']:.2f} against {XC['sharpe_excess_D10']:.2f}). Neither difference is one the data can confirm (Table 4). Allowing for market risk (a CAPM regression), low-MAX minus high-MAX moves to {RFc['alpha']['D1-D10']['CAPM']['alpha_ann'] * 100:+.1f}% a year: the direction Bali, Cakici & Whitelaw found, though well within noise (t {RFc['alpha']['D1-D10']['CAPM']['t']:.2f}). The adjusted figures are reported, not tested.

## 4. Beta, profitability and the bull market (reported, not gated)

These analyses were added after review. They help explain the verdict; they cannot change it. All use the corrected universe unless marked.

**Table 5. Factor-adjusted returns, actual S&P 500 members, {RFc['first'][:7]} → {RFc['last'][:7]}**

{T5}

Against the market alone, the lottery tickets' extra return disappears and the gap turns slightly positive. Add the Fama–French factors and it shrinks towards zero. Add momentum and it changes sign. In the full model, low-MAX minus high-MAX loads {LD['Mkt-RF']:+.2f} on the market and **{LD['RMW']:+.2f} on profitability** (RMW): the lottery decile behaves like a basket of low-profitability companies, the steady decile like a basket of profitable ones. Buying low MAX in large caps is mostly a short-beta, long-profitability bet. None of the alphas comes near significance.

**Table 6. Up and down markets**

{T7}

Up and down months show the average month × 12; 2022 is the actual calendar-year return. The pattern is roughly what a higher beta predicts: the lottery decile rose faster in up months and fell faster in down months (2022 is the exception: it fell less than its beta implies). In the {BMc['down']['months']} months the market fell, low-MAX minus high-MAX earned {BMc['down']['spread_ann'] * 100:+.0f}% a year. In 2022, the one bear year in the sample, the steady decile lost {-RFc['year_2022']['D1'] * 100:.1f}% and the lottery decile {-RFc['year_2022']['D10'] * 100:.1f}%. With {BMc['up']['months']} up months against {BMc['down']['months']} down months, the raw result is mostly a statement about the market.

![Figure 3](../figures/fig3_cumulative.png)

Figure 3 shows how much rests on the last stretch. On the actual S&P 500 members, after {RFc['split_2025']['to2024_months']} of the {RFc['split_2025']['to2024_months'] + RFc['split_2025']['from2025_months']} months (to the end of 2024), $1 in the steady decile had grown to ${RFc['split_2025']['to2024_D1_growth']:.2f}, against ${RFc['split_2025']['to2024_D10_growth']:.2f} in the lottery decile. Then, from January 2025, the lottery decile rose {RFc['split_2025']['from2025_D10']:.0%} in {RFc['split_2025']['from2025_months']} months while the steady decile rose {RFc['split_2025']['from2025_D1']:.0%}. The raw A04-2 result is largely a story about those {RFc['split_2025']['from2025_months']} months.

**How small an effect could these tests see?** Given the noise in the data, A04-1 had an 80% chance of passing only if the true effect was at least {A1['mde_ann']:.0%} a year. That is far more than the {A1['insample_1963_2005_ann']:.1%} the JKP factor earned before publication. For A04-2 the bar is {SPc['mde_ann']:.0%} a year. So A04-1 could not have detected an effect the size of the JKP factor's pre-publication premium; A04-2's bar is about the size of Bali, Cakici & Whitelaw's original decile spread (about 1% a month), so only an effect at least that large would reliably have shown. “Not detected” here means small or absent, not shown to be zero. The 95% intervals in Tables 1 and 4 give the range the data allow.

## 5. Three more questions (reported, not gated)

In December 2010, just before Bali, Cakici & Whitelaw's paper appeared in print, a research note from Deutsche Bank's quantitative strategy team (*DB Quant Handbook*) put the lottery factor through three questions: is it just short-term reversal, is it just volatility, and which side of the trade pays? On US and Canadian stocks up to 2010 their answers were (DB Quant Handbook, pp. 678–683): not reversal (a rank IC of 4.6% for MAX against 2.3% for one-month reversal in the US, and far more persistent, so far less turnover); volatility-neutralising helped in the most recent years; and the payoff came mostly from the short side. I asked the same three questions of the A04-2 universe. They are added after the trials and cannot change the verdict. One note: on today's data files the baseline spread is {DB['baseline_spread']['ann'] * 100:+.1f}% a year rather than the {p2['ann'] * 100:+.1f}% in Table 4 (the data files have been updated since 1 October); every number in this section is measured against that same-run baseline (deciles here are formed by rank, which moves the baseline by 0.06 points against the code of record). Alphas in this section are on today's files, so they differ slightly from Table 5.

**Table 7. The lottery spread with reversal and volatility held fixed, and by leg**

{T8}

![Figure 4](../figures/fig4_db2010.png)

- **Is it reversal? The data cannot say either.** Holding last month's return fixed cuts the quintile spread from {DB['baseline_quintile_spread']['ann'] * 100:+.1f}% to {DBr['max_reversal_neutral']['ann'] * 100:+.1f}% a year, almost as much as holding volatility fixed (below). But reversal itself did not work in large caps after 2012 ({DBr['rev_spread']['ann'] * 100:+.1f}% a year, t {DBr['rev_spread']['t']:.2f}), and the two spreads are unrelated (correlation {DBr['corr_with_max_spread']:+.2f}). Unlike in the 2010 note, reversal's rank IC ({DBr['rank_ic_rev']['mean'] * 100:.2f}%) is larger than MAX's ({DBr['rank_ic_max']['mean'] * 100:.2f}%). Both double sorts also shrink spreads mechanically, because MAX varies less inside each group, and both changes are well inside one standard error of the baseline. As the 2010 note found, MAX is a persistent signal and last month's return is not: the month-to-month rank correlation of the MAX scores is {DBr['signal_persistence_max']:.2f}, of past returns {DBr['signal_persistence_rev']:+.2f}. Adding the reversal spread to the factor model moves the MAX alpha only from {sa(DBr['max_spread_on_ff5_mom'])} to {sa(DBr['max_spread_on_rev_ff5_mom'])}.
- **Is it volatility? Perhaps, but the data cannot say.** With volatility held fixed, the lottery stocks' lead shrinks from {DB['baseline_quintile_spread']['ann'] * 100:+.1f}% to {DBv['max_vol_neutral']['ann'] * 100:+.1f}% a year (quintiles), and after the factor model to {DBv['max_vol_neutral_ff5_mom']['alpha_ann'] * 100:+.1f}% (t {DBv['max_vol_neutral_ff5_mom']['t']:.2f}). The part of MAX that volatility does not explain earns {DBv['max_resid_vol']['ann'] * 100:+.1f}% a year (t {DBv['max_resid_vol']['t']:.2f}). Every one of these numbers is well inside one standard error of the baseline, so neither control changes the spread detectably.
- **Which side pays? As in the 2010 note, the action is in the lottery decile, but here it earned more than the rest rather than less.** Deciles 1 to 9 earned between {min(DBl['deciles_ann'][f'D{k}'] for k in range(1, 10)) * 100:.0f}% and {max(DBl['deciles_ann'][f'D{k}'] for k in range(1, 10)) * 100:.0f}% a year; decile 10 earned {DBl['deciles_ann']['D10'] * 100:.0f}%. About three quarters of the spread is the lottery decile against the rest ({DBl['short_EW_minus_D10']['ann'] * 100:+.1f}% a year, t {DBl['short_EW_minus_D10']['t']:.2f}); the steady decile against the rest adds {DBl['long_D1_minus_EW']['ann'] * 100:+.1f}% (t {DBl['long_D1_minus_EW']['t']:.2f}). In the 2010 note the lottery decile was where the losses were; in large caps after 2012 it is where the gains were, and the factor model cuts the lottery decile's edge over the rest to {-DBl['short_ff5_mom']['alpha_ann'] * 100:.1f}% a year (t {-DBl['short_ff5_mom']['t']:.2f}), within noise.
- **The signal itself.** The 2010 note's US rank IC for MAX was 4.6% a month. In the actual S&P 500 members 2013–2026 it is {DBr['rank_ic_max']['mean'] * 100:.2f}%, and of the right sign: across the whole cross-section MAX points weakly in Bali, Cakici & Whitelaw's direction; the raw gap against it comes from the extreme decile.

None of the three changes the verdict. In modern large caps the MAX spread is too noisy to separate from reversal or volatility; what there is sits in the lottery decile, and factor exposures absorb it.

## 6. What this does and does not show

- **In large caps, MAX is mostly beta and low profitability.** Once you allow for market exposure, the high-MAX stocks earned about what their risk implied, or slightly less on the corrected universe; once profitability and momentum are added, nothing detectable is left (Table 5). This is the same measurement problem as betting against beta (Frazzini & Pedersen 2014; Baker, Bradley & Wurgler 2011): a test that ignores beta rewards leverage in a bull market.
- **2013–2026 is mostly one bull market, and the raw result leans on its last 20 months.** Table 6 shows the raw gap flips sign in falling months; Figure 3 shows the steady decile ahead until 2025. A sample with more bear markets would likely show low MAX ahead in raw return; the factor-adjusted result in Table 5 should depend much less on the cycle.
- **Hindsight-list bias, now measured.** Section 3 corrects it. It tilted the result towards the lottery decile, by about 3 percentage points a year, enough to put the lottery decile marginally ahead per unit of risk.
- **Low power.** The tests could only see large effects (section 4). They rule out a big lottery discount in large caps after 2012, not a small one.
- **Two trials, programme now at 48.** Sections 4 and 5 add no trials.

## 7. Verdict

The pre-registered tests find no reliable evidence that lottery stocks have underperformed since Bali, Cakici & Whitelaw (2011): not across the US market, and not in the 500 largest stocks. In large caps the lottery tickets earned more in raw terms, but they carried twice the market risk through a long bull market. On the actual S&P 500 members the steady names did somewhat better per unit of risk, and a standard factor model absorbs the gap: lottery stocks are high-beta, low-profitability companies. The tests were too small to rule out a modest discount, so the honest summary is that the MAX effect in modern large caps is weak or absent, not robust. If you want lottery-like upside in large caps, you are buying beta and weak profitability. Price it as that.

## Reproduce

```bash
python code/run_max.py          # A04-1..2 + reported, results/summary.json (first list)
P10_UNIVERSE=sp500_pit P10_RESULTS=results_pit python code/run_max.py   # corrected universe, results_pit/
python code/reported_stress.py  # excess-return Sharpe ratios, bootstrap, meme-window alpha (added after the stress test)
python code/reported_factor.py  # section 4 (reported, not gated), results_pit/reported_factor.json
P10_UNIVERSE=sp500_pit python code/reported_db2010.py   # section 5 (reported, not gated), results_pit/reported_db2010.json
python code/make_figures.py && python code/build_article.py
```

The data files are updated over time; results of record are from the 1 October 2026 files (section 3).

## References

- Baker, M., Bradley, B. & Wurgler, J. (2011). Benchmarks as limits to arbitrage: understanding the low-volatility anomaly. *Financial Analysts Journal*, 67(1).
- Bali, T. G., Cakici, N. & Whitelaw, R. F. (2011). Maxing out: stocks as lotteries and the cross-section of expected returns. *Journal of Financial Economics*, 99(2).
- Barberis, N. & Huang, M. (2008). Stocks as lotteries: the implications of probability weighting for security prices. *American Economic Review*, 98(5).
- Deutsche Bank Quantitative Strategy (2010). Lottery factor with new faces. *DB Quant Handbook*, 10 December 2010, 678–683.
- Fama, E. F. & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1).
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics*, 111(1).
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5).
- Kumar, A. (2009). Who gambles in the stock market? *Journal of Finance*, 64(4).

*Not investment advice. Song title used as a cultural reference only; no lyrics are quoted.*
"""
write_article(ROOT, STEM, md, "Viva Las Vegas")

post = f"""VIVA LAS VEGAS: do lottery stocks still lose?

Meme stocks, zero-commission apps, options for everyone. If lottery stocks were ever going to cost their buyers money, it was now.

A famous paper says they should: stocks with the biggest one-day jumps last month go on to underperform (Bali, Cakici & Whitelaw, 2011).

I tested it again on large US stocks, with the tests written down first. At first sight, the lottery tickets beat the steadiest stocks by {-p2['ann']:.0%} a year on the actual S&P 500 members ({-a2['ann']:.0%} on my first, flawed list).

Three questions before you decide the gamblers won:
1. Did they win, or did they just carry more risk?
2. Which flaw in my own stock list was worth 3% a year, and which way did it push the result?
3. How much of 13 years comes down to the last 20 months?

Your answer to question 1 in the comments, then check it here, with tables, code and the pre-registration: {REPO}

#investing #behavioralfinance #quant #statistics
"""
write_teaser(ROOT, post, "hero_viva_las_vegas_teaser.png", "Viva Las Vegas", "October 2026")   # teaser poster asks, article poster answers
click_layout(ROOT, "teaser_slots.png")   # 21 Oct 2026: questions left, drawing right (code/make_teaser_drawing.py)
write_readme(ROOT, "A04 Viva Las Vegas: do lottery stocks still lose?", ["run_max.py", "reported_factor.py", "reported_db2010.py", "make_figures.py", "build_article.py"])
open(os.path.join(ROOT, "README.md"), "a").write("Publication slot: Tuesday 27 October 2026 (Now Showing No. 4).\n")
try:
    make_pdfs(ROOT, STEM)
except Exception as e:  # no browser here: print the PDFs on Windows
    print("PDFs not built here:", type(e).__name__)
print(post); print("words", len(post.split()))
