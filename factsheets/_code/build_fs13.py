# -*- coding: utf-8 -*-
"""FS13: the signal battery. Every price signal in every market, plus 153 published JKP factors: where is the common ground?"""
import json
import os

import numpy as np

import build_factsheets as BF
from battery import DIRECTION, SIGS
from common_ground import U, UN, LAB, REPL, JMAP, THEMES
from jkp_battery import SEG

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results")
table = BF.table
p = lambda x, d=1: f"{x * 100:+.{d}f}%"; f2 = lambda x: f"{x:+.2f}"


def build():
    O = json.load(open(os.path.join(RES, "common_ground.json"))); PS = O["price"]; TH = O["themes"]; RP = O["replication"]; JS = O["jkp_summary"]
    bh_bn = [s for s in SIGS if PS[s]["bn"]["bh"]]; bh_raw = [s for s in SIGS if PS[s]["raw"]["bh"]]
    pos_bn = [s for s in SIGS if PS[s]["bn"]["pos"] == 6 and PS[s]["bn"]["t"] > 0]
    raw_pos6 = [s for s in SIGS if PS[s]["raw"]["pos"] == 6]
    lr = ["max1", "max5", "min1", "min5", "range", "ivol", "vol", "vol252", "beta"]
    raw_lr_neg = sum(PS[s]["raw"]["t"] < 0 for s in lr); bn_lr_pos = sum(PS[s]["bn"]["t"] > 0 for s in lr)
    common = [r for r in TH if r["verdict"].startswith("Common ground")]
    pooled_only = [r for r in TH if r["verdict"].startswith("Works pooled")]
    neg = [r for r in TH if r["verdict"].startswith("Reliably negative")]
    faded = [r for r in TH if "faded" in r["verdict"]]
    ari = O["clusters"]["ari"]; groups = O["clusters"]["groups"]
    ag_p = O["agree_price_mean"]; ag_j = O["agree_jkp_mean"]
    us_repl = {k: RP[k]["US"] for k in RP}; strong = [k for k in RP if RP[k]["US"] >= 0.8]
    # tables
    dir_rows = [[LAB[s], DIRECTION[s][1], "high" if DIRECTION[s][0] else "low", DIRECTION[s][3]] for s in SIGS]
    ps_rows = []
    for s in sorted(SIGS, key=lambda s: -PS[s]["bn"]["t"]):
        v = PS[s]
        ps_rows.append([LAB[s], v["family"], f"{p(v['raw']['ann'])} (t {v['raw']['t']:+.1f})", f"{v['raw']['pos']} / 6",
                        f"{p(v['bn']['ann'])} (t {v['bn']['t']:+.1f}){' ✓' if v['bn']['bh'] else ''}", f"{v['bn']['pos']} / 6",
                        f"{v['lo_beats']} / 6", f"{v['bn']['neff']:.1f}", p(v["cost"]), f"{v['bn']['design']:+.2f} / {v['bn']['holdout']:+.2f}"])
    fam = {"4": "low risk and tail size", "5": "momentum", "1": "tail direction", "2": "reversal", "6": "residual momentum", "7": "seasonality", "3": "size"}
    grp_rows = [[", ".join(LAB[s] for s in g), str(len(g))] for g in sorted(groups.values(), key=len, reverse=True)]
    ag_rows = [[UN[R], f"{ag_p[R]:.2f}"] for R in U]
    agj_rows = [[SEG[s], f"{ag_j[s]:.2f}"] for s in SEG]
    rp_rows = [[LAB[k], REPL[k]] + [f"{RP[k][R]:.2f}" for R in U] for k in RP]
    top_rows = [[r["factor"], r["cluster"], p(r["ann"]), f"{r['sharpe']:.2f}", f"{r['t']:+.1f}", f"{int(r['pos'])} / 4", p(r["pre_ann"]), "✓" if r["bh"] else ""] for r in JS["top"]]
    th_rows = []
    for r in TH:
        pr = r.get("price"); jk = r.get("jkp")
        th_rows.append([r["theme"], f"{pr['t']:+.1f} ({pr['pos']}/6)" if pr else "—", f"{jk['t']:+.1f} ({jk['pos']}/4)" if jk else "—",
                        f"{r['jkp_pre']['usa']:+.2f} → {r['jkp_sh']['usa']:+.2f}" if jk else "—", f"{r['jkp_bh']} / {r['jkp_n']}" if jk else "—", r["verdict"]])
    FIN = json.load(open(os.path.join(RES, "financing.json"))); nc = {R: FIN["beta"][R]["net_cash"] for R in U}
    ag_sorted = sorted(U, key=lambda R: ag_p[R])
    disc = [(s_, k) for s_ in SIGS for k in ("raw", "bn") if PS[s_][k]["bh"]]
    disc_pos = [d for d in disc if PS[d[0]][d[1]]["t"] > 0]; disc_neg = [d for d in disc if PS[d[0]][d[1]]["t"] < 0]
    dname = lambda d: LAB[d[0]] + (" (beta-neutral)" if d[1] == "bn" else " (raw)")
    lb = PS["beta"]["bn"]; mo = PS["mom"]["bn"]; rm = PS["resmom"]["bn"]; se = PS["seas"]["bn"]
    mom_th = next(r for r in TH if r["theme"] == "Momentum"); lr_th = next(r for r in TH if r["theme"] == "Low risk")
    di = next(r for r in TH if r["theme"] == "Debt issuance"); pg = next(r for r in TH if r["theme"] == "Profit growth")
    md = f"""# FACTSHEET FS13 · The signal battery

### Every signal in every market: where is the common ground?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · price data to 31 August 2026, JKP to December 2025*

| Key facts | |
|---|---|
| Price battery | 19 price signals × 6 point-in-time universes (US, EU, UK, DK, SCANDI, World), monthly, 2013–2026, our engine, net of 10 bp per side and a size-tiered borrow fee on the short leg |
| Published battery | 153 JKP factors (Jensen, Kelly & Pedersen 2023) × 5 segments (US, UK, Denmark, World ex US, World), 2013–2025, grouped into 13 themes |
| Direction | fixed from the literature before the run (table in §1); no signal was flipped after seeing results |
| Books | long/short (top minus bottom quantile), beta-neutral long/short (charged for the cash it borrows at the USD risk-free rate + 50 bp), long-only vs the equal-weight universe |
| Pooled test | equal-weight average of the markets; its t-statistic includes the co-movement between markets |
| Multiple testing | Benjamini–Hochberg at 5% over 38 price tests (19 signals × raw/beta-neutral) and over 153 JKP factors; Harvey–Liu–Zhu t > 3 as a second bar |

> **In one paragraph.** {"**No price signal earns a positive return that survives the multiple-testing correction**" if not disc_pos else "**Only " + ", ".join(dname(d) for d in disc_pos) + " survive" + ("s" if len(disc_pos) == 1 else "") + " the multiple-testing correction on the positive side**"} once short legs pay borrow fees and the beta-neutral books pay for the leverage they use; thirteen years of large caps are too short for more.{" What does survive is a loser: " + ", ".join(dname(d) for d in disc_neg) + " reliably loses money." if disc_neg else ""} The common ground is in the *direction*. **Low beta** is positive in {lb['pos']} of 6 of our markets after all costs (t {lb['t']:.1f}) but flat in JKP's value-weighted factors. **Momentum** is positive in {mom_th['price']['pos']} of 6 of our markets (12-1 momentum {mo['pos']} of 6, residual momentum {rm['pos']} of 6) and in all {mom_th['jkp']['pos']} JKP segments (t {mom_th['jkp']['t']:.1f}); in our large caps it is not significant on its own (t {mom_th['price']['t']:.1f}). Among the fundamental themes we cannot yet build ourselves, **debt issuance** (t {di['jkp']['t']:.1f}) and **profit growth** (t {pg['jkp']['t']:.1f}) worked in every JKP segment since 2013. **Same-month seasonality** and **tail direction** are reliably negative in our large caps. The 19 price signals hold only a handful of independent bets: one low-risk block of nine and one momentum block of four, the same structure in the US, EU and World (adjusted Rand index {min(ari['US'], ari['EU'], ari['WD']):.2f}–{max(ari['US'], ari['EU'], ari['WD']):.2f}). {UN[ag_sorted[0]]} and {UN[ag_sorted[1]]} agree least with the other markets on which signals work. The engine reproduces the published US factors (correlation ≥ 0.8 for {len(strong)} of {len(RP)} matched signals).

![Common ground map](../figures/fs13_common_map.png)

## 1. What was tested

Two batteries, one question: which signals work across segments, and which only in one corner?

**Price battery (our data, our engine).** Every signal in the library (`code/signals.py`, `signals2.py`) runs through the same sort engine as FS03–FS12 (`code/xs.py`) in all six universes: monthly quantile sort (deciles ≥ 100 names, quintiles 50–99, terciles below), equal weight, 10 bp per side on turnover. Three books per signal: long/short, **beta-neutral** long/short (each leg scaled to beta 1 before netting, so the market bet that dominated FS02 and FS04 is removed), and long-only against owning all stocks equally. The direction of every signal was set from the literature before running:

{table(["Signal", "Family", "Long the", "Direction from"], dir_rows)}

*Two directions are conventions rather than paper results: MIN and the daily range follow the low-risk reading (small tails are good), and "far above the 52-week low" is the momentum reading, which FS12 had already shown. Treat those three as less than fully out-of-sample.*

**Published battery (JKP).** The 153 factors of Jensen, Kelly & Pedersen (2023, *Is There a Replication Crisis in Finance?*), capped value-weighted long/short, in USD, signed so the original paper's prediction is positive, grouped into their 13 themes. JKP covers fundamentals (value, quality, investment, profitability, accruals, debt issuance) that we do not yet have outside the US. Segments: US, UK, Denmark, World ex US (disjoint from the US) and World. **There is no JKP file for EU or Scandinavia in our cache and the JKP site is not reachable from the build environment; World ex US stands in for both where a comparison is needed.**

## 2. The price battery: every signal, every market

![Price heatmap](../figures/fs13_price_heatmap.png)

{table(["Signal", "Family", "L/S net, 6-market average", "L/S > 0", "Beta-neutral, net of costs and financing (✓ = BH)", "Beta-neutral > 0", "Long-only beats EW Sharpe", "Effective markets", "Cost / yr", "Beta-neutral Sharpe 2013–19 / 2020–26"], ps_rows)}

*Averages are the equal-weight mean of the six market series; t is Newey–West on that mean. Effective markets = 36 / sum of the 6×6 correlation matrix. ✓ = discovery under Benjamini–Hochberg at 5% over 38 tests.*

**Reading it.**

1. **The raw long/short numbers are mostly a beta story.** {raw_lr_neg} of the 9 low-risk and tail-size signals have a negative raw average and {bn_lr_pos} of 9 turn positive once the legs are beta-neutral and financed. Their raw books are short the market in a market that rose.
2. **Beta-neutral low-risk books need a lot of leverage.** To bring the low-beta leg up to a beta of one, the low-beta book borrows on average {min(nc.values()):.1f}–{max(nc.values()):.1f} units of cash per unit of capital ({', '.join(f"{UN[R]} {nc[R]:.1f}" for R in U)}). Charged at the USD risk-free rate plus 50 bp, low beta still earns {p(lb['ann'])} a year (Sharpe {lb['sharpe']:.2f}, t {lb['t']:.1f}, positive in {lb['pos']} of 6), the strongest positive price signal, but it no longer clears the correction. The charge is conservative for EU and Denmark, where short rates were negative for 2015–21.
3. **After the correction: {len(disc)} discover{'y' if len(disc) == 1 else 'ies'} out of 38**{(": " + ", ".join(f"{dname(d)} (t {PS[d[0]][d[1]]['t']:+.1f})" for d in disc)) if disc else ""}. The strongest positive candidates are low beta (t {lb['t']:+.1f}) and 12-1 momentum (t {mo['t']:+.1f}); neither clears the bar.
4. **Momentum holds in most markets in both books**: 12-1 momentum is positive raw in {PS['mom']['raw']['pos']} and beta-neutral in {mo['pos']} of six markets, residual momentum in {PS['resmom']['raw']['pos']} and {rm['pos']}. Positive raw in all six: {', '.join(LAB[s] for s in raw_pos6) or 'none'}.
5. **Tail direction is not priced the way the lottery literature expects** in our large caps: low skewness and low net tail lose in most markets, raw and beta-neutral.
6. **Costs sort the families**: the within-month signals (MAX, MIN, skewness, reversal, seasonality) cost 3–4% a year; volatility, beta, momentum and size cost 0–2%.

## 3. Common ground among signals: two blocks

![Correlation](../figures/fs13_corr.png)

Clustering the beta-neutral long/short returns (average correlation over the six markets, average linkage, cut at correlation 0.5) gives:

{table(["Signals in the group", "Size"], grp_rows)}

**The nineteen signals hold far fewer independent bets.** Everything that measures the *size* of price moves — MAX, MIN, the daily range, idiosyncratic volatility, volatility and beta — is one block. Momentum, 52-week high, 52-week low distance and the breakout are a second block. Residual momentum, reversal, seasonality, tail direction and size stand alone.

**Is the structure the same in every market?** Adjusted Rand index between each market's own clustering and the pooled one: {', '.join(f"{UN[R]} {ari[R]:.2f}" for R in U)} (1 = identical, 0 = random). The two-block structure is almost identical in the US, EU and World and looser in the UK and Scandinavia, where small groups and fewer names make correlations noisier.

## 4. Common ground among segments: do markets agree on what works?

Spearman rank correlation between markets of the 19 beta-neutral Sharpe ratios (average against the other five markets):

{table(["Market", "Average agreement with the other markets"], ag_rows)}

The same test on the 153 JKP factors (2013–2025 Sharpe ratios):

{table(["Segment", "Average agreement with the other segments"], agj_rows)}

**{'The Nordic markets are the odd ones out' if set(ag_sorted[:2]) <= {'DK', 'SC'} else UN[ag_sorted[0]] + ' is the odd one out'}.** In the price battery {UN[ag_sorted[0]]} ({ag_p[ag_sorted[0]]:.2f}) and {UN[ag_sorted[1]]} ({ag_p[ag_sorted[1]]:.2f}) agree least; in JKP it is Denmark ({ag_j['dnk']:.2f}). With ~19 stocks in OMXC25, ~62 in SCANDI and a JKP Danish universe dominated by a few large names, factor returns there are driven by single companies. The US, EU/World ex US and World agree most, partly because they overlap. The median correlation of the same JKP factor across segments: US–World ex US {JS['co']['usa-world_ex_us']:.2f}, US–UK {JS['co']['gbr-usa']:.2f}, US–Denmark {JS['co']['dnk-usa']:.2f}; factor returns are mostly local, so a signal that works in several segments is genuine breadth, not one bet counted twice.

## 5. The published factors: 153 JKP factors since 2013

![JKP themes](../figures/fs13_jkp_themes.png)

Pooled over the four disjoint segments (US, UK, Denmark, World ex US), **{JS['bh']} of {JS['n']} factors** are discoveries under Benjamini–Hochberg at 5% and {JS['hlz']} clear the Harvey–Liu–Zhu bar of t > 3. The strongest twelve:

{table(["Factor", "Theme", "Average return / yr", "Sharpe", "t", "Positive in", "Before 2013 (4-segment average)", "BH"], top_rows)}

**Reading it.** The winners since 2013 come from three themes: **momentum** (12-1, 9-1, 6-1, residual momentum, 52-week high, seasonality at lag 1), **debt issuance** (firms that shrink net financing, debt or net operating assets beat those that raise them) and **profit growth** (sales and earnings surprises and changes). Value, investment and accruals, stars of the pre-2013 literature, weakened sharply in the US; short-term reversal fell from a Sharpe of {next(r for r in TH if r['theme'] == 'Short-term reversal')['jkp_pre']['usa']:.2f} to {next(r for r in TH if r['theme'] == 'Short-term reversal')['jkp_sh']['usa']:.2f} there.

## 6. Replication check: does our engine match the published factors?

![Replication](../figures/fs13_replication.png)

{table(["Our signal", "JKP factor"] + [UN[R] + (" (proxy)" if R in ("EU", "SC") else "") for R in U], rp_rows)}

In the US, where the universes are closest (our top 500 vs JKP's capped value-weighted full market), **{len(strong)} of {len(RP)} matched signals correlate 0.8 or more** with the published factor ({', '.join(LAB[k] for k in strong)}). This closes the replication gap raised in FS00: the engine produces the known factors. The weaker matches have known reasons: our seasonality averages up to 13 years of same-month returns while JKP's `seas_1_1an` uses only last year's; our size sort is within the 500 largest (JKP spans micro caps). EU and Scandinavia are compared with World ex US, so their lower numbers measure the proxy, not the engine.

## 7. Where is the common ground?

{table(["Theme", "Our price data: t (markets > 0)", "JKP: t (segments > 0)", "JKP US Sharpe before 2013 → since", "JKP factors that are BH discoveries", "Verdict"], th_rows)}

*Price t: beta-neutral composite of the theme's signals, average of 6 markets. JKP t: equal-weight theme portfolio, average of 4 disjoint segments, 2013–2025. "Common ground" = positive in every segment of every source that covers the theme, and pooled t > 2 in at least one source. "Faded in the US" = JKP US Sharpe above 0.3 before 2013 and below 0.15 since.*

**Common ground:** {', '.join(r['theme'] for r in common) or 'none'}. **Positive almost everywhere, not significant:** {', '.join(r['theme'] for r in TH if r['verdict'].startswith('Positive almost')) or 'none'}. **Works pooled, not everywhere:** {', '.join(r['theme'] for r in pooled_only) or 'none'}. **Reliably negative:** {', '.join(r['theme'] for r in neg) or 'none'}. **Faded in the US:** {', '.join(r['theme'] for r in faded) or 'none'}.

**Momentum is the strongest theme across both sources**: positive in {mom_th['price']['pos']} of six of our markets and all {mom_th['jkp']['pos']} JKP segments; significant in JKP (t {mom_th['jkp']['t']:+.1f}) but not in our large caps once short legs pay borrow fees (t {mom_th['price']['t']:+.1f}){'; it misses the common-ground label because ' + ', '.join(UN[R] for R in U if mom_th['price_sh'][R] <= 0) + ' is negative' if mom_th['price']['pos'] < 6 else ''}. **Low risk** is positive in {lr_th['price']['pos']} of six of our markets after financing (t {lr_th['price']['t']:.1f}) but only {lr_th['jkp']['pos']} of 4 JKP segments (t {lr_th['jkp']['t']:.1f}); JKP's low-risk factors are value-weighted and not beta-neutral, so they carry the short-market drag that our beta-neutral books remove. **Debt issuance** (t {di['jkp']['t']:.1f}) and **profit growth** (t {pg['jkp']['t']:.1f}) are the only themes positive in every segment with a significant pooled return, and both are fundamental themes to add first. Value, quality, profitability and investment were positive in most JKP segments but not significant since 2013.

## 8. What this means for the multifactor model

The battery gives a pre-selection that is transparent and grounded in more than one segment:

1. **Carry forward:** low beta (beta-neutral, financed) as the low-risk representative, and 12-1 momentum, residual momentum and the 52-week high from the momentum block; the other signals in each block are near-duplicates.
2. **Add from fundamentals next** (US stock level from Sharadar; JKP factor level elsewhere): debt issuance and profit growth first, then quality and value as diversifiers even though they were weak since 2013.
3. **Drop:** same-month seasonality, short-term reversal and tail direction (skewness, net tail) in large caps; the lottery/tail-size signals add nothing beyond low beta and volatility.
4. **Treat Denmark as a robustness market, not a selection market**: its signal ranking agrees least with the others.
5. The next factsheet applies the planned filters (net return, Sharpe, turnover per segment), rolling 3-year correlations and the dynamic weighting to this shortlist, walk-forward.

## 9. Caveats

- **Different construction.** Our books are equal-weighted, net, local currency (World in USD), large caps; JKP's are capped value-weighted, gross, USD, broad market. Agreement across the two is therefore stronger evidence than either alone, but numbers are not comparable one-to-one.
- **Proxies.** EU and Scandinavia have no JKP data here; World ex US stands in. World overlaps US, UK and EU in both batteries; the pooled tests use disjoint segments for JKP and report the effective number of markets for the price battery.
- **Periods.** Price battery Feb 2013 – Aug 2026; JKP Jan 2013 – Dec 2025. JKP's "before 2013" history starts in the 1920s for the US and in 1987 for the UK, Denmark and World ex US.
- **Multiple testing.** 38 price tests and 153 JKP factors are corrected with Benjamini–Hochberg; the earlier factsheets' fix ladders are not in this count (see the FS00 gap on a programme-level ledger).
- **Three directions are conventions** (MIN, range, 52-week low distance); see §1.
- **Costs.** 10 bp per side, a size-tiered borrow fee on every short leg and financing of net long cash (USD risk-free + 50 bp) are charged; market impact is not (FS00).

## 10. References

- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Hou, K., Xue, C. & Zhang, L. (2020). Replicating anomalies. *Review of Financial Studies* 33(5), 2019–2133.
- Harvey, C. R., Liu, Y. & Zhu, H. (2016). … and the cross-section of expected returns. *Review of Financial Studies* 29(1), 5–68.
- Benjamini, Y. & Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society B* 57(1), 289–300.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance* 71(1), 5–32.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics* 111(1), 1–25.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance* 48(1), 65–91.
- Blitz, D., Huij, J. & Martens, M. (2011). Residual momentum. *Journal of Empirical Finance* 18(3), 506–521.
- George, T. J. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance* 59(5), 2145–2176.
- Bali, T. G., Cakici, N. & Whitelaw, R. F. (2011). Maxing out. *Journal of Financial Economics* 99(2), 427–446.
- Ang, A., Hodrick, R. J., Xing, Y. & Zhang, X. (2006). The cross-section of volatility and expected returns. *Journal of Finance* 61(1), 259–299.
- Boyer, B., Mitton, T. & Vorkink, K. (2010). Expected idiosyncratic skewness. *Review of Financial Studies* 23(1), 169–202.
- Heston, S. L. & Sadka, R. (2008). Seasonality in the cross-section of stock returns. *Journal of Financial Economics* 87(2), 418–445.
- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns. *Journal of Finance* 45(3), 881–898.
- Banz, R. W. (1981). The relationship between return and market value of common stocks. *Journal of Financial Economics* 9(1), 3–18.
- Blitz, D. & van Vliet, P. (2007). The volatility effect. *Journal of Portfolio Management* 34(1), 102–113.

## 11. Reproduce

`code/battery.py` (price battery → `results/battery_price.json/.pkl`), `code/jkp_battery.py` (JKP battery → `results/battery_jkp_*.csv`), `code/financing.py` (financing charge for the beta-neutral books), `code/common_ground.py` (pooled tests, clusters, agreement, replication, themes, figures → `results/common_ground.json`), `code/build_fs13.py` (this factsheet). JKP monthly factor files come from Project2's `reporting/style_cache`.
"""
    BF.write("FS13_Signal_Battery", md, "FS13 The signal battery")
    BF.pdf("FS13_Signal_Battery")


if __name__ == "__main__":
    build(); print("built FS13")
