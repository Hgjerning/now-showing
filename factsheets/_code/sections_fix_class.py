# -*- coding: utf-8 -*-
"""Sections 10 (what goes wrong and how to fix it) and 11 (classification) for FS01 and FS02.
Every number is read from results/fix_summary.json, turtle_diagnostics.json, turtle_summary.json, lottery_summary.json."""
import json
import os

import numpy as np

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
U = ["US", "EU", "UK", "DK", "SC", "WD"]
UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
JKPU = ["US", "UK", "DK", "WD"]
GATE_P = 0.05 / 7
p = lambda x, d=1: f"{x * 100:+.{d}f}%"
f2 = lambda x: f"{x:.2f}"


def table(head, rows):
    s = "| " + " | ".join(str(x).replace("|", "&#124;") for x in head) + " |\n|" + "|".join(["---"] * len(head)) + "|\n"
    for r in rows:
        s += "| " + " | ".join(str(x).replace("|", "&#124;") for x in r) + " |\n"
    return s


def rng(vals, fmt=p):
    return f"{fmt(min(vals))} to {fmt(max(vals))}"


def mom(c):
    return c["corr"].get("momentum", c["corr"].get("WML"))


def step_table(K, bench=None):
    rows = []
    steps = K["steps"]
    for j, s in enumerate(steps):
        d = [K["per"][R][s]["design"]["sharpe"] for R in U]; h = [K["per"][R][s]["holdout"]["sharpe"] for R in U]
        if j == 0:
            imp, pd_, ph = "–", "–", "–"
        else:
            prev = steps[j - 1]
            imp = f"{sum(K['per'][R][s]['holdout']['sharpe'] > K['per'][R][prev]['holdout']['sharpe'] for R in U)} of 6"
            pp = K["pooled"][s]
            pd_ = f"{pp['vs_previous_design']['diff']:+.2f} (p {pp['vs_previous_design']['p']:.3f})"
            ph = f"{pp['vs_previous_holdout']['diff']:+.2f} (p {pp['vs_previous_holdout']['p']:.3f})" + (" ✔" if pp['vs_previous_holdout']['p'] < GATE_P else "")
        a = K["avg_holdout"][s]
        extra = [f"{p(a['alpha'])} ({a['t_alpha']:.1f})", f2(a["beta"])] if "alpha" in a else [f"{a['t']:.2f}"]
        rows.append([s, f"{np.mean(d):.2f}", pd_, f"{a['sharpe']:.2f}", ph, imp, p(a["ann"]), p(a["maxdd"], 0)] + extra)
    head = ["Step", "Design Sharpe (avg of 6)", "Δ vs previous, design (p)", "Holdout Sharpe (6-universe book)", "Δ vs previous, holdout (p)", "Holdout: universes improved", "Holdout return / yr", "Holdout max DD"]
    head += ["Alpha vs EW / yr (t)", "Beta"] if "alpha" in K["avg_holdout"][steps[0]] else ["t(mean)"]
    if bench:
        a = K["avg_holdout"][bench]
        rows.append([f"*{bench} (reference)*", "", "", f"{a['sharpe']:.2f}", "", "", p(a["ann"]), p(a["maxdd"], 0), "–", "1.00"])
    return table(head, rows)


def per_universe(K):
    rows = []
    for R in U:
        rows.append([UN[R]] + [f"{K['per'][R][s]['design']['sharpe']:.2f} / {K['per'][R][s]['holdout']['sharpe']:.2f}" for s in K["steps"]])
    return table(["Universe"] + [s.split(" ")[0] for s in K["steps"]], rows)


def turtle_bullets(T, Tp, t3, fin, t4d, UP):
    t1, t2, t3s, t4 = (Tp[k] for k in ["T1 long-only", "T2 + System 2 only", "T3 + 4N stop", "T4 + market trend filter"])
    pas = lambda x: "passes" if x["p"] < GATE_P else "does not pass"
    out = [f"- **Dropping the shorts is the big step:** design {t1['vs_previous_design']['diff']:+.2f} (p {t1['vs_previous_design']['p']:.3f}, {pas(t1['vs_previous_design'])}), holdout {t1['vs_previous_holdout']['diff']:+.2f} (p {t1['vs_previous_holdout']['p']:.3f}, {pas(t1['vs_previous_holdout'])} the gate).",
           f"- **System 2 only:** {t2['vs_previous_design']['diff']:+.2f} design, {t2['vs_previous_holdout']['diff']:+.2f} holdout. Fewer trades, no reliable gain.",
           f"- **The 4N stop:** {t3s['vs_previous_design']['diff']:+.2f} design, {t3s['vs_previous_holdout']['diff']:+.2f} holdout (p {t3s['vs_previous_holdout']['p']:.2f}). Positive in both windows, too small to pass.",
           f"- **The market trend filter is not trustworthy:** {t4['vs_previous_holdout']['diff']:+.2f} in the holdout but {t4d['diff']:+.2f} in the design window. The market was in an up-trend {min(UP) * 100:.0f}–{max(UP) * 100:.0f}% of the time, so the filter rarely binds, and its result rests on one or two episodes.",
           f"- **Where it ends:** T3 (long-only, System 2, 4N stop) has a holdout Sharpe of {T['avg_holdout']['T3 + 4N stop']['sharpe']:.2f} against {T['avg_holdout']['EW universe']['sharpe']:.2f} for the equal-weight universe (difference {t3['diff']:+.2f}, p {t3['p']:.2f}) with a beta of about {T['avg_holdout']['T3 + 4N stop']['beta']:.2f}. T4 reaches {T['avg_holdout']['T4 + market trend filter']['sharpe']:.2f} ({fin['diff']:+.2f} vs the universe, p {fin['p']:.2f})."]
    return "\n".join(out)


def lottery_bullets(L, Lp, l1, l2, l3, l2better_d, l2worse):
    U6 = ["US", "EU", "UK", "DK", "SC", "WD"]
    bd = sum(L["per"][R]["L1 beta-neutral"]["design"]["sharpe"] > L["per"][R]["L0 baseline"]["design"]["sharpe"] for R in U6)
    bh = sum(L["per"][R]["L1 beta-neutral"]["holdout"]["sharpe"] > L["per"][R]["L0 baseline"]["holdout"]["sharpe"] for R in U6)
    c2 = np.mean([L["per"][R]["L2 + vol-scaled MAX"]["cost"] for R in U6]); c3 = np.mean([L["per"][R]["L3 + turnover buffer"]["cost"] for R in U6])
    pas = lambda x: "passes" if x["p"] < GATE_P else "does not pass"
    out = [f"- **Beta-neutral legs are the real fix.** Sharpe {l1['vs_previous_design']['diff']:+.2f} in the design window (p {l1['vs_previous_design']['p']:.4f}, {pas(l1['vs_previous_design'])}) and {l1['vs_previous_holdout']['diff']:+.2f} in the holdout (p {l1['vs_previous_holdout']['p']:.3f}, {pas(l1['vs_previous_holdout'])} the gate); better in {bd} of 6 universes in the design window and {bh} of 6 in the holdout. The fixed L/S earns {p(Lp['L1_vs_zero_holdout']['ann'])} a year in the holdout (t {Lp['L1_vs_zero_holdout']['t']:.1f}): the beta drag is gone, and what is left is statistically zero.",
           f"- **Vol-scaled MAX failed out of sample.** It helped in {l2better_d} of 6 universes in the design window and hurt in {l2worse} of 6 in the holdout ({l2['vs_previous_holdout']['diff']:+.2f}). {'A textbook overfit signature, and a useful one: ' if l2better_d >= 4 else ''}once plain volatility is removed, large-cap lottery-ness carries no premium.",
           f"- **The turnover buffer** cuts costs from {c2 * 100:.1f}% to {c3 * 100:.1f}% a year ({l3['vs_previous_design']['diff']:+.2f} design, {l3['vs_previous_holdout']['diff']:+.2f} holdout, p {l3['vs_previous_holdout']['p']:.2f}), not significant."]
    return "\n".join(out)


# ================================================================================================
def fs01_sections():
    F = json.load(open(os.path.join(RES, "fix_summary.json"))); D = json.load(open(os.path.join(RES, "turtle_diagnostics.json")))
    J = json.load(open(os.path.join(RES, "turtle_summary.json")))
    T, C = F["turtle"], F["classification"]; cc = T["cost_check"]
    ev = {R: D[R]["ev55"] for R in U}
    side = {R: D[R]["pnl"]["by_side"] for R in U}
    shortp = [sum(v["pnl"] for k, v in side[R].items() if k.endswith("short")) / 7 for R in U]
    longp = [sum(v["pnl"] for k, v in side[R].items() if k.endswith("long")) / 7 for R in U]
    stopn = [D[R]["pnl"]["by_reason"]["2N stop"]["n"] / sum(v["n"] for v in D[R]["pnl"]["by_reason"].values()) for R in U]
    stopp = [D[R]["pnl"]["by_reason"]["2N stop"]["pnl"] / 7 for R in U]; chp = [D[R]["pnl"]["by_reason"]["channel exit"]["pnl"] / 7 for R in U]
    vr = lambda q, k: np.median([D[R]["vr"][str(q)][k] for R in U])
    cost_rows = [[UN[R], p(cc[R]["gross"]), p(cc[R]["net"]), p(cc[R]["net"] - cc[R]["gross"])] for R in U if R in cc]
    ev_rows = [[UN[R]] + [f"{ev[R]['long'][w]['mean'] * 100:+.2f}% ({ev[R]['long'][w]['t']:.1f})" for w in ev[R]["long"]] + [f"{ev[R]['short'][w]['mean'] * 100:+.2f}% ({ev[R]['short'][w]['t']:.1f})" for w in ["t+2..5", "t+6..20"]] for R in U]
    Tp = T["pooled"]; fin = Tp["final_vs_EW_holdout"]; t3 = Tp["T3_vs_EW_holdout"]
    import pandas as _pd
    UP = [float(_pd.read_pickle(os.path.join(RES, f"turtle_fix_{R}.pkl"))["up"].loc["2013":].mean()) for R in U]
    t4d = T["pooled"]["T4 + market trend filter"]["vs_previous_design"]
    md = f"""## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the *design* window (2013–2019) only, write down the fixes in a fixed order, then judge each fix on the untouched *holdout* (Jan 2020 – Aug 2026). Every fix stays inside the Turtle rulebook: it changes a knob Faith (2003, 2007) describes (direction, system, stop width, a trend filter), not the idea. Each step is one trial, tested on the equal-weighted average of the six universes with a paired stationary-bootstrap test of the Sharpe difference against the previous step; with 7 fix trials across both factsheets the gate is p < {GATE_P:.4f}. Honest caveat: I had seen the full-sample results in §1–9 before choosing the fixes, so the holdout is clean for the *numbers* but not for the *ideas*.

### 10.1 Diagnosis: five things go wrong

**1. Costs eat the book.** Close-to-close N is small for large caps (median about 1% of the price), so a 0.1%-risk unit is about 10% of equity; with ~500 trades a year and pyramiding, the book trades well over 100× its equity a year. At 10 bp per side that is a double-digit drag:

{table(["Universe", "L/S before costs", "L/S after costs", "Cost drag / yr"], cost_rows)}
*Design window 2013–2019, S1+S2 long/short, re-run with costs and borrow set to zero.* Costs explain {min(1 - cc[R]['gross'] / cc[R]['net'] for R in cc if cc[R]['net'] < 0) * 100:.0f}–{max(min(1 - cc[R]['gross'] / cc[R]['net'], 1) for R in cc if cc[R]['net'] < 0) * 100:.0f}% of the loss; the rest is below. (Novy-Marx & Velikov 2016 show the same for high-turnover anomalies in general.)

**2. The short side does all the damage.** Summed trade P&L a year, 2013–2019: short trades {rng(shortp, lambda x: f"{x * 100:+.0f}%")} of equity, long trades {rng(longp, lambda x: f"{x * 100:+.0f}%")}. Shorting single stocks in markets rising 10–15% a year, with no stock-specific edge (point 4), loses roughly the market return on the short book.

**3. The 2N stop is too tight for single stocks.** {min(stopn) * 100:.0f}–{max(stopn) * 100:.0f}% of trades end on the 2N stop, and their summed P&L is {rng(stopp, lambda x: f"{x * 100:.0f}%")} of equity a year (summed across trades, not compounded); trades that reach the channel exit sum to {rng(chp, lambda x: f"{x * 100:+.0f}%")}. With a close-to-close N, 2N is only about 2% below the entry, a move the median large cap makes every few days, so the stop harvests noise and multiplies trading.

**4. There is no trend to follow in single stocks at these horizons.** After a fresh 55-day breakout, the stock's return *in excess of its universe* is small and mostly insignificant at every horizon, and where it is significant it is as often negative as positive (t-statistics in brackets):

{table(["Universe", "Long: t+1", "t+2..5", "t+6..20", "t+21..60", "Short: t+2..5", "t+6..20"], ev_rows)}
Variance ratios (Lo & MacKinlay 1988) say the same thing: the median single stock has VR(20) = {vr(20, 'stock'):.2f} and VR(60) = {vr(60, 'stock'):.2f}, net of the market {vr(20, 'idio'):.2f} and {vr(60, 'idio'):.2f}. Values below 1 mean mild mean reversion, not trend. Breakout rules need VR > 1 (Figure 4, panel C). This is the root cause, and no parameter inside the rulebook can create a trend that is not in the data.

**5. Not the culprit: the one-day fill lag.** The fill-day column (t+1) is a few basis points either way (largest {max(abs(ev[R]['long']['t+1 (fill day)']['mean']) for R in U) * 100:.2f}%), so waiting for the next close costs next to nothing. A "confirmation delay" fix I had coded was dropped before testing, because the diagnosis gave it nothing to fix.

![Diagnosis](../figures/fs01_fig4_diagnosis.png)

### 10.2 The fixes, one step at a time

T0 → T1 drop the shorts (point 2) → T2 keep System 2 only, fewer and longer trades (point 1) → T3 widen the stop from 2N to 4N (point 3) → T4 add a market trend filter: only take new longs when the universe index's 25-day EMA is above its 350-day EMA, a filter of the kind Faith (2007) tests.

{step_table(T, "EW universe")}
*✔ = passes the gate (p < {GATE_P:.4f}). Design Sharpe = average across the six universes; the Δ tests and the holdout columns use the six-universe equal-weighted book. Alpha and beta vs the six-universe equal-weight benchmark, Newey-West t.*

**Per universe, Sharpe design / holdout**

{per_universe(T)}
![Fix ladder](../figures/fs01_fig5_fixes.png)

### 10.3 What the fixes achieve

{turtle_bullets(T, Tp, t3, fin, t4d, UP)}

**Bottom line.** The fixes remove self-inflicted damage (shorting a bull market, a stop tighter than daily noise, a cost bill from oversized units). What remains is a stop-protected, half-beta equity book, not an edge. The Turtle rules need assets that trend, which is why they were built for, and still work in, diversified futures (Moskowitz, Ooi & Pedersen 2012; Hurst, Ooi & Pedersen 2017). Recommended specification if you insist on stocks: **T3** (long-only, System 2, 4N stop; no market filter, because that filter failed in the design window), and judge it against a half-beta equal-weight portfolio, not against cash.

"""
    # ---------------- classification
    cl = C["Turtle L/S"]; lo = C["Turtle long-only"]; fx = C["Turtle fixed (T3)"]
    tg = [cl[R]["tm_gamma"] for R in U]; tt = [cl[R]["tm_t"] for R in U]
    rows = [
        ["Series family (Content_ver2 'Odd ideas')", "**Breakout & trend**"],
        ["Academic style", "Trend following / time-series momentum (Moskowitz, Ooi & Pedersen 2012); Donchian (1960) breakout"],
        ["Signal", "Price only (technical); each stock against its own past, not ranked against other stocks"],
        ["Cross-section vs time series", f"**Time series.** Position depends on the stock's own channel; the book's net exposure floats (L/S average net {rng([J[R]['exposure']['net'] for R in U], lambda x: f'{x * 100:+.0f}%')})"],
        ["Horizon and turnover", f"Medium term: winners held ~{np.mean([J[R]['trades']['days_win'] for R in U]):.0f} days, losers ~{np.mean([J[R]['trades']['days_loss'] for R in U]):.0f}; {np.mean([J[R]['trades']['per_year'] for R in U]):.0f} trades a year; very high turnover"],
        ["Trade-level payoff", f"Positively skewed: {np.mean([J[R]['trades']['win_rate'] for R in U]) * 100:.0f}% winners, payoff ratio {np.mean([J[R]['trades']['payoff'] for R in U]):.1f}, roughly the best quarter of trades carries the book"],
        ["Book-level payoff", f"No convexity on stocks: Treynor–Mazuy γ ranges {min(tg):+.2f} to {max(tg):+.2f} (t {min(tt):.1f} to {max(tt):.1f}); futures trend books show a clear 'smile'. In the worst 10% of market months the L/S earns {rng([cl[R]['worst_mkt'] for R in U])} a month: a weak hedge, not crisis alpha"],
        ["Nearest JKP theme (L/S)", f"**Momentum** (correlation {rng([mom(cl[R]) for R in U], f2)}); low risk {rng([cl[R]['corr']['low_risk'] for R in JKPU], f2)}"],
        ["Nearest theme (long-only, T3)", f"**Market beta**: correlation with the market {rng([fx[R]['corr'].get('mkt', fx[R]['corr'].get('Mkt-RF')) for R in U], f2)}, *negative* with low risk ({rng([fx[R]['corr']['low_risk'] for R in JKPU], f2)}): breakouts select volatile stocks"],
        ["Economic rationale", "Behavioural: under-reaction then herding (Barberis, Shleifer & Vishny 1998; Hong & Stein 1999). No risk-based story. In futures, also hedging pressure and slow-moving capital"],
        ["Capacity and crowding", "High capacity in large caps, but the turnover makes it cost-bound. Crowded in futures (the CTA industry), not in single stocks"],
        ["Publication", "Donchian 1960; Turtle rules private 1983, published 2003 (Faith); TSMOM formalised 2012"],
        ["Where it fits", "**A futures strategy mis-applied to stocks.** On single stocks it becomes a momentum-flavoured, high-beta, high-cost book. The correct home is the index/futures level; on stocks, the related evidence-based sibling is cross-sectional 12-1 momentum (Jegadeesh & Titman 1993), not channel breakouts"],
    ]
    md += f"""## 11. Classification: where does it fit?

Evidence: correlations of monthly returns with the 13 JKP factor themes (US, UK, DK, World) or the French Europe factors (EU, SCANDI), a Treynor–Mazuy regression r = a + b·m + γ·m² on the equal-weight universe (γ > 0 = convex, the trend-follower's signature), and returns in the worst and best 10% of market months.

{table(["Dimension", "Turtle Traders on stocks"], rows)}
![Classification map](../figures/fs_class_map.png)

The map places every book from both factsheets in the same space. The Turtle long/short sits on the momentum axis; its long-only and fixed versions drop into the high-beta corner (negative correlation with low risk), the exact opposite of where the lottery factor lives. The two factsheets are, in factor terms, mirror images: breakouts buy what MAX sells.

"""
    return md


# ================================================================================================
def fs02_sections():
    F = json.load(open(os.path.join(RES, "fix_summary.json"))); J = json.load(open(os.path.join(RES, "lottery_summary.json")))
    L, C = F["lottery"], F["classification"]; dg = L["diag"]
    PH = json.load(open(os.path.join(RES, "lottery_posthoc.json")))
    LS = "L/S low minus high MAX (net)"
    beta_drag = [J[R]["stats"][LS]["beta"] * J[R]["stats"]["EW universe (benchmark)"]["ann_mean"] for R in U]
    hz_rows = [[UN[R]] + [p(dg[R]["diag"]["horizon"][k]) for k in ["t+1", "t+2..3", "t+4..6"]] + [f2(dg[R]["diag"]["rankcorr_max_vol"]), f2(dg[R]["diag"]["rankcorr_max_beta"])] for R in U]
    Lp = L["pooled"]; l1 = Lp["L1 beta-neutral"]; l2 = Lp["L2 + vol-scaled MAX"]; l3 = Lp["L3 + turnover buffer"]
    l2worse = sum(L["per"][R]["L2 + vol-scaled MAX"]["holdout"]["sharpe"] < L["per"][R]["L1 beta-neutral"]["holdout"]["sharpe"] for R in U)
    l2better_d = sum(L["per"][R]["L2 + vol-scaled MAX"]["design"]["sharpe"] > L["per"][R]["L1 beta-neutral"]["design"]["sharpe"] for R in U)
    md = f"""## 10. What goes wrong, and how to fix it

**Method.** As in FS01: diagnose on the design window (Feb 2013 – Dec 2019), fix in a pre-declared order, judge on the holdout (Jan 2020 – Aug 2026), one trial per step, pooled six-universe test of the Sharpe difference, gate p < {GATE_P:.4f} (7 fix trials across both factsheets). The fixes stay inside the MAX strategy: they change how the two legs are sized, how MAX is measured, and how often names change, not what the strategy bets on.

### 10.1 Diagnosis: four things go wrong

**1. A hidden short on the market.** The L/S has a beta of about −0.6 because low-MAX stocks are low-beta and high-MAX stocks high-beta. With equal-weight universes rising 10–15% a year, beta alone costs {rng(beta_drag)} a year (beta × the universe's return), comparable to or larger than the raw loss (larger in {', '.join(UN[R] for R in U if abs(J[R]['stats'][LS]['beta'] * J[R]['stats']['EW universe (benchmark)']['ann_mean']) > abs(J[R]['stats'][LS]['ann_mean']))}); §1 shows CAPM alphas within {max(abs(J[R]['stats'][LS]['alpha']) for R in U) * 100:.0f}%. The original paper sorted on MAX without neutralising beta; in a 1962–2005 sample that averaged out, in a 13-year bull market it does not.

**2. MAX in large caps is mostly volatility.** The cross-sectional rank correlation of MAX with 60-day volatility is {rng([dg[R]['diag']['rankcorr_max_vol'] for R in U], f2)}, and with beta {rng([dg[R]['diag']['rankcorr_max_beta'] for R in U], f2)} (table below). Among blue-chip stocks, a big up-day usually means a volatile stock or news (earnings, M&A), not a retail lottery ticket. The lottery premium lives in small, retail-held stocks (Kumar 2009; Bali et al. 2011), which these universes exclude by construction and which no fix inside them can bring back.

**3. Turnover.** The low leg turns over {rng([J[R]['to_low'] for R in U], lambda x: f'{x * 100:.0f}%')} a month and the high leg about as much, so costs take {rng([J[R]['cost_drag'] for R in U], lambda x: f'{x * 100:.1f}%')} a year.

**4. Waiting does not help.** The spread is no better, and mostly worse, two to six months after formation, so a longer holding period will not rescue it:

{table(["Universe", "L/S, month t+1 (ann.)", "t+2..3", "t+4..6", "Rank corr MAX vs volatility", "Rank corr MAX vs beta"], hz_rows)}
*Design window, gross, equal-weighted extreme groups.*

### 10.2 The fixes, one step at a time

L0 baseline → L1 **beta-neutral legs**: each leg scaled by 1/its ex-ante 252-day beta, so the L/S has zero expected beta (the Frazzini & Pedersen 2014 construction; point 1) → L2 **vol-scaled MAX**: rank on MAX5 / 21-day volatility (JKP's `rmax5_rvol_21d`), lottery-ness net of plain volatility (point 2) → L3 **turnover buffer**: enter the extreme 1/q, keep a name until it leaves the extreme 3/q (point 3).

{step_table(L)}
*Pooled test on the equal-weighted six-universe L/S. ✔ = passes p < {GATE_P:.4f}.*

**Per universe, Sharpe design / holdout**

{per_universe(L)}
![Fix ladder](../figures/fs02_fig5_fixes.png)

### 10.3 What the fixes achieve

{lottery_bullets(L, Lp, l1, l2, l3, l2better_d, l2worse)}

**Bottom line.** What went wrong is not the idea but the packaging: an unhedged beta bet and a signal that, in large caps, measures volatility. Fixing the beta turns a {p(L['avg_holdout']['L0 baseline']['ann'])}/yr loser (six-universe book, holdout) into a market-neutral book earning {p(Lp['L1_vs_zero_holdout']['ann'])} (t {Lp['L1_vs_zero_holdout']['t']:.1f}), statistically zero. The lottery premium itself is not present in these universes after 2012. Recommended specification if you want the exposure: **L1 (beta-neutral) with the turnover buffer on the original MAX signal**. That exact combination was not in the pre-declared ladder, so I report it post hoc and count it as nothing: costs fall to {PH['pooled']['cost'] * 100:.1f}% a year and the holdout L/S earns {p(PH['pooled']['holdout_ann'])} (t {PH['pooled']['holdout_t']:.1f}, Sharpe {PH['pooled']['holdout_sharpe']:.2f} vs {PH['pooled']['l1_holdout_sharpe']:.2f} for L1). Treat it as a defensive, low-risk tilt with an expected premium near zero; for a long-only investor, the low-MAX portfolio is a reasonable low-beta equity sleeve, not an alpha source.

"""
    cl = C["MAX L/S"]; bn = C["MAX beta-neutral (L1)"]
    hib = [J[R]['quantile_beta']['Q' + str(J[R]['q'])] for R in U]
    tg = [cl[R]["tm_gamma"] for R in U]; tt = [cl[R]["tm_t"] for R in U]
    rows = [
        ["Series family (Content_ver2 'Odd ideas')", "**Lottery & attention**"],
        ["Academic style", "Low-risk / defensive anomaly (the family of betting-against-beta, low volatility, idiosyncratic volatility); behavioural origin in probability weighting"],
        ["Signal", "Price only: one statistic of last month's daily returns"],
        ["Cross-section vs time series", "**Cross-sectional**: stocks ranked against each other, always long one group and short another"],
        ["Horizon and turnover", f"One month; {rng([J[R]['to_low'] for R in U], lambda x: f'{x * 100:.0f}%')} of the low leg replaced monthly; cost drag {rng([J[R]['cost_drag'] for R in U], lambda x: f'{x * 100:.1f}%')} a year"],
        ["Market exposure", f"Beta {rng([J[R]['stats'][LS]['beta'] for R in U], f2)} as published (low-MAX {rng([J[R]['quantile_beta']['Q1'] for R in U], f2)}, high-MAX {rng(hib, f2)}); zero by construction after fix L1"],
        ["Book-level payoff", f"**Concave**: Treynor–Mazuy γ {min(tg):+.2f} to {max(tg):+.2f} (t {min(tt):.1f} to {max(tt):.1f}); earns {rng([cl[R]['worst_mkt'] for R in U])} a month in the worst 10% of market months and loses {rng([cl[R]['best_mkt'] for R in U])} in the best 10%. A defensive profile: it pays in sell-offs and bleeds in rallies"],
        ["Nearest JKP theme", f"**Low risk** (correlation {rng([cl[R]['corr']['low_risk'] for R in JKPU], f2)}; still {rng([bn[R]['corr']['low_risk'] for R in JKPU], f2)} after beta-neutralising). Momentum {rng([mom(cl[R]) for R in U], f2)}"],
        ["Economic rationale", "Behavioural: cumulative prospect theory and probability weighting (Tversky & Kahneman 1992; Barberis & Huang 2008), retail gambling demand (Kumar 2009). Constraint-based: leverage-constrained investors buy high-beta stocks (Frazzini & Pedersen 2014); Bali, Brown, Murray & Tang (2017) tie the two together"],
        ["Where the premium lives", "Small, illiquid, retail-held stocks; weak in the 500 largest US stocks and in large-cap Europe"],
        ["Capacity and crowding", "Large-cap version: high capacity, low premium. Low-risk ETFs and defensive funds hold the long leg in size"],
        ["Publication", "Bali, Cakici & Whitelaw 2011 (data to 2005); European evidence 2013–14; post-publication decay per McLean & Pontiff (2016)"],
        ["Where it fits", "**A member of the low-risk family, not a separate factor.** In large caps it is a noisier, costlier version of low volatility / betting-against-beta. It belongs in a defensive sleeve next to those, sized by its beta, and should be judged on beta-neutral terms"],
    ]
    md += f"""## 11. Classification: where does it fit?

Evidence as in FS01: correlations with the JKP themes or French Europe factors, a Treynor–Mazuy convexity regression on the equal-weight universe, and behaviour in the worst and best 10% of market months.

{table(["Dimension", "Lottery factor (MAX)"], rows)}
![Classification map](../figures/fs_class_map.png)

On the map the MAX long/short sits high on the low-risk axis; beta-neutralising moves it toward the centre but keeps it in the defensive half. The Turtle books from FS01 sit in the opposite corner. The two strategies are close to mirror images: a breakout rule buys exactly the volatile, recently jumping stocks that the MAX rule sells.

"""
    return md
