# -*- coding: utf-8 -*-
"""Minority Report, Part 1: Where to Look (Now Showing No. 8, 24 Nov 2026). Written 13 Nov 2026.

Text source: article/minority_report_part1_where_to_look_DRAFT_2026-11-13.md  (edit the words THERE).
This script 1) checks every number in that text against the result files and stops if one does not match,
2) writes article/minority_report_part1.md / .html, 3) writes the one-pager (linkedin/post.txt, teaser.html),
4) prints the PDFs where Playwright is installed (Windows). Figures and posters: code/make_figures_part1.py (run first).
The withdrawn October article (article/minority_report.*, code/build_article.py) is not touched; its one-pager is kept in
Articles/_backups_2026-11-13_part1/linkedin_old_A06/.
Run:  python build_part1.py            (add --check to only check the numbers)"""
import csv
import json
import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10"))
from common import click_layout, make_pdfs, write_article, write_teaser  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A31 = os.path.join(ROOT, "..", "A09_Minority_Report_2_Small_Print")
SRC = os.path.join(ROOT, "article", "minority_report_part1_where_to_look_DRAFT_2026-11-13.md")
STEM = "minority_report_part1"; REPO = "hgjerning.github.io/now-showing/minority-report"
J = lambda *p: json.load(open(os.path.join(*p), encoding="utf-8"))
text = open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------- result files
S = J(ROOT, "results_pit", "summary.json"); SREG = J(ROOT, "results", "summary.json")
B = pd.read_csv(os.path.join(ROOT, "results_pit", "scoreboard.csv"), index_col=0)
L = J(ROOT, "results_pit", "costs_like_for_like.json")
U1S = J(A31, "results", "U1", "summary.json"); U2S = J(A31, "results", "U2", "summary.json")
U1 = pd.read_csv(os.path.join(A31, "results", "U1", "scoreboard.csv"), index_col=0)
U2 = pd.read_csv(os.path.join(A31, "results", "U2", "scoreboard.csv"), index_col=0)
R = J(A31, "results", "U1", "reported.json")
SO = pd.read_csv(os.path.join(A31, "results", "U1", "simple_sorts.csv"), index_col=0)
PL = pd.read_csv(os.path.join(A31, "results", "U1", "placebo.csv"))
G = pd.read_csv(os.path.join(A31, "results", "U1", "gross_monthly.csv"), index_col=0, parse_dates=True)["Ensemble"]
PRE = open(os.path.join(A31, "PREREGISTRATION_A31S_Slow_Print_2026-11-06.md"), encoding="utf-8").read()


def nw_t(x, lags=3):
    x = np.asarray(x, float); n = len(x); e = x - x.mean(); v = e @ e / n
    for k in range(1, lags + 1): v += 2 * (1 - k / (lags + 1)) * (e[k:] @ e[:-k]) / n
    return x.mean() / np.sqrt(v / n)


pc = lambda v: f"{v * 100:+.1f}%"; up = lambda v: f"{abs(v) * 100:.1f}%"; t2 = lambda v: f"{v:.2f}"; to = lambda v: f"{v * 100:.0f}%"
ml = [n for n in B.index if n not in ("Ensemble", "Momentum")]
sp, mo = L["sp500_Ensemble_cost0.10pct"], L["sp500_Momentum_cost0.10pct"]
s50, s40 = L["smallcap_Ensemble_cost0.50pct"], L["smallcap_Ensemble_cost0.40pct"]
en = U1.loc["Ensemble"]; rf = U1.loc["RandomForest"]; gp = SO.loc["Profitability (GP/A)"]
nomom = [x for x in R["ablation_no_mom"] if x["name"] == "Ensemble"][0]; pb = R["placebo"]
a1, a2, a3 = S["A06-1"], S["A06-2"], S["A06-3"]; u1, u2, u3 = U1S["A31-U1.1"], U1S["A31-U1.2"], U1S["A31-U1.3"]; e1, e2 = U2S["A31-U2.1"], U2S["A31-U2.2"]
NAMES = {"OLS": "OLS", "Ridge": "Ridge", "Lasso": "Lasso", "ElasticNet": "Elastic Net", "RandomForest": "Random forest", "GradBoost": "Gradient boosting",
         "MLP": "Neural net", "kNN": "k-nearest neighbours"}
SORTN = {"Value (B/M)": "Value (book/market)", "Low volatility": "Low volatility", "Earnings yield": "Earnings yield", "Momentum 12-1": "Momentum (12-1)", "Small size": "Small size"}

# ---------------------------------------------------------------- every number in the text, rebuilt from the result files
C = []   # (what, exact string that must be in the text)
C.append(("T1 ensemble", f"| Machine-learning ensemble | {pc(a1['mean'] * 12)} | {t2(a1['t'])} | {to(sp['turnover_m'])} | **{pc(sp['net_ann'])}** | {t2(sp['net_t'])} |"))
C.append(("T1 momentum", f"| 12-1 momentum | {pc(B.loc['Momentum', 'ann_ret'])} | {t2(B.loc['Momentum', 'nw_t'])} | {to(mo['turnover_m'])} | {pc(mo['net_ann'])} | {t2(mo['net_t'])} |"))
for k, nm in NAMES.items():
    r = U1.loc[k]; C.append((f"T2 {k}", f"| {nm} | {pc(r.gross_ann)} | {t2(r.gross_t)} | {to(r.turnover_m)} | {pc(r.net_ann)} | {t2(r.net_t)} |"))
C.append(("T2 ensemble", f"| **Ensemble** | **{pc(en.gross_ann)}** | **{t2(en.gross_t)}** | **{to(en.turnover_m)}** | **{pc(en.net_ann)}** | **{t2(en.net_t)}** |"))
r = U1.loc["Momentum"]; C.append(("T2 momentum", f"| 12-1 momentum | {pc(r.gross_ann)} | {t2(r.gross_t)} | {to(r.turnover_m)} | {pc(r.net_ann)} | {t2(r.net_t)} |"))
C.append(("T3 S&P", f"| S&P 500, ensemble (0.10%) | {pc(sp['gross_ann'])} | {to(sp['turnover_m'])} | {pc(sp['net_ann'])} | {t2(sp['net_t'])} |"))
C.append(("T3 small 0.50", f"| US small caps, ensemble (0.50%) | {pc(s50['gross_ann'])} | {to(s50['turnover_m'])} | {pc(s50['net_ann'])} | {t2(s50['net_t'])} |"))
C.append(("T3 small 0.40", f"| US small caps, ensemble (0.40%)* | {pc(s40['gross_ann'])} | {to(s40['turnover_m'])} | {pc(s40['net_ann'])} | {t2(s40['net_t'])} |"))
C.append(("T4 profitability", f"| **Gross profitability** | {pc(gp.gross_ann)} | {to(gp.turnover_m)} | **{pc(gp.net_ann)}** | **{t2(gp.net_t)}** |"))
for k, nm in SORTN.items():
    r = SO.loc[k]; C.append((f"T4 {k}", f"| {nm} | {pc(r.gross_ann)} | {to(r.turnover_m)} | {pc(r.net_ann)} | {t2(r.net_t)} |"))
C += [
    ("abstract S&P", f"lost {up(a1['mean'] * 12)} a year before costs and {up(sp['net_ann'])} after them"),
    ("abstract small gross", f"**{pc(en.gross_ann)} a year before costs (t {t2(en.gross_t)}, 2004-2026; reported, not gated)**"),
    ("abstract turnover", f"trades {to(en.turnover_m)} of its capital a month (buys plus sells, both legs"),
    ("abstract small net", f"at most **{pc(en.net_ann)} a year (t {t2(en.net_t)})**"),
    ("months", f"({a1['n']} months)"), ("months small", f"({u1['n']} months)"),
    ("A06-1 p", f"(p {t2(a1['p_gt'])})"), ("A06-2", f"trailed momentum by {up(a2['mean'] * 12)} a year (t {t2(a2['t'])})"),
    ("A06-3", f"(Sharpe {t2(a3['sr_ann'])}, deflated Sharpe {t2(a3['dsr'])} against the 0.983 required)"),
    ("turnover pair", f"({to(sp['turnover_m'])} against {to(mo['turnover_m'])} a month)"),
    ("halves 1", f"(Sharpe {t2(B.loc[ml, 'sharpe_h1'].min())} to {t2(B.loc[ml, 'sharpe_h1'].max())})"),
    ("halves 2", f"({t2(B.loc[ml, 'sharpe_h2'].max())} to {t2(B.loc[ml, 'sharpe_h2'].min())})"),
    ("flattering list", f"(the ensemble showed {pc(SREG['A06-1']['mean'] * 12)} a year instead of {pc(a1['mean'] * 12)})"),
    ("Europe", f"earned {pc(U2.loc['Ensemble', 'gross_ann'])} a year before costs (t {t2(U2.loc['Ensemble', 'gross_t'])}) and {pc(e1['mean'] * 12)} after 0.15% costs (t {t2(e1['t'])})"),
    ("Europe vs momentum", f"trailed momentum by {up(e2['mean'] * 12)} a year"),
    ("placebo real", f"were {t2(pb['Ridge']['real_gross'])} and {t2(pb['GradBoost']['real_gross'])}"),
    ("placebo mean", f"averaged {t2(pb['Ridge']['placebo_gross_mean'])} and {t2(pb['GradBoost']['placebo_gross_mean'])}"),
    ("placebo best", f"the best shuffled gradient-boosting run reached {t2(PL[PL.model == 'GradBoost'].gross.max())}"),
    ("no momentum", f"still earns {pc(nomom['gross_ann'])} a year before costs (t {t2(nomom['gross_t'])})"),
    ("cost a year", f"costs {up(12 * en.turnover_m * 0.005)} a year and turns {pc(en.gross_ann)} into {pc(en.net_ann)} (t {t2(en.net_t)})"),
    ("break-even", f"The break-even cost is {en.breakeven_cost * 100:.2f}% per trade"),
    ("U1.1 p", f"(p {t2(u1['p_gt'])})"),
    ("U1.2", f"({pc(u2['mean'] * 12)} a year, t {t2(u2['t'])}, p {u2['p_gt']:.3f})"),
    ("U1.3", f"(the random forest, Sharpe {t2(u3['sr_ann'])}) has a deflated Sharpe of {t2(u3['dsr'])} against 0.9944"),
    ("0.1 point", f"moves the small-cap result by {(s40['net_ann'] - s50['net_ann']) * 100:.1f} points a year"),
    ("same window", f"earned {pc(s50['gross_ann'])} a year before costs with a t of only {t2(s50['gross_t'])}"),
    ("sub 2017-21", f"{pc(G['2017-01':'2021-09'].mean() * 12)} a year before costs on portfolios formed Jan 2017 - Sep 2021"),
    ("sub 2021-26", f"{pc(G['2021-10':'2026-07'].mean() * 12)} on those formed Oct 2021 - Jul 2026"),
    ("sub 2004-16", f"(2004-2016: {pc(G['2004-01':'2016-12'].mean() * 12)})"),
    ("profitability vs machines", f"({pc(gp.gross_ann)} against {pc(en.gross_ann)}) and more after them ({pc(gp.net_ann)} against {pc(en.net_ann)})"),
    ("turnover pair small", f"turns over {to(gp.turnover_m)} a month where the ensemble turns over {to(en.turnover_m)}"),
    ("crossing", f"cross near {(en.gross_ann - gp.gross_ann) / (12 * (en.turnover_m - gp.turnover_m)) * 100:.2f}% per trade"),
    ("answer 1", f"{pc(a1['mean'] * 12)} a year before costs in the S&P 500 (t {t2(a1['t'])}), {pc(en.gross_ann)} in US small caps (t {t2(en.gross_t)}; reported, not gated)"),
    ("answer 1 window", f"in the window the two studies share, 2017-2026, it is {pc(s50['gross_ann'])} (t {t2(s50['gross_t'])})"),
    ("answer 3", f"{pc(gp.net_ann)} a year after costs (t {t2(gp.net_t)}) against {pc(en.net_ann)} for the ensemble"),
    ("verdict signal", f"{pc(en.gross_ann)} a year, t {t2(en.gross_t)} (reported, not gated), not matched by any of 40 shuffled runs"),
    ("verdict bill", f"Trading at {to(en.turnover_m)} a month and 0.50% per trade leaves {pc(en.net_ann)} a year (t {t2(en.net_t)})"),
]
bad = [(w, s) for w, s in C if s not in text]
flags = {"A06 best of nine is momentum": a3["best"] == "Momentum", "U1 best of nine is the random forest": u3["best"] == "RandomForest",
         "U2 best of nine is momentum": U2S["A31-U2.3"]["best"] == "Momentum", "no shuffled run reached the real model": all(v["share_placebo_gross_ge_real"] == 0 for v in pb.values()),
         "0 of 9 passed": not any(d[k]["passed"] for d in (S, U1S, U2S) for k in d if isinstance(d[k], dict) and "passed" in d[k]),
         "all eight small-cap t above 2.2": bool((U1.loc[list(NAMES), "gross_t"] > 2.2).all()),
         "same-window small-cap t matches": abs(nw_t(G["2017-01":"2026-07"]) - s50["gross_t"]) < 0.01,
         "no trade count in the text (anonymity, 15 Nov 2026)": "65,920" not in text}
print(f"number check: {len(C) - len(bad)} of {len(C)} strings match the result files; {sum(flags.values())} of {len(flags)} facts hold")
for w, s in bad: print("  NOT IN TEXT:", w, "->", s)
for k, v in flags.items():
    if not v: print("  FALSE:", k)
if bad or not all(flags.values()):
    sys.exit("build stopped: fix the text or the check first")
if "--check" in sys.argv: sys.exit(0)

# ---------------------------------------------------------------- article
GM = open(os.path.join(ROOT, "..", "PROGRAMME_GATE.md"), encoding="utf-8").read()
n_prog = int(re.search(r"counted as (\d+) for the multiple-testing", GM).group(1)); n_run = int(re.search(r"\((\d+) trials run", GM).group(1))
gate = {r["trial"]: r for r in csv.DictReader(open(os.path.join(ROOT, "..", "PROGRAMME_GATE.csv"), encoding="utf-8"))}
mine = [k for k in gate if k.startswith(("A06-", "A31-U"))]; assert len(mine) == 9, mine
qmin = min(float(gate[k]["q_BH"]) for k in mine)
md = text.replace("Programme trial count: <!-- HENRIK: filled by build_part1.py from PROGRAMME_GATE.md -->.",
                  f"Programme trial count: {n_run} trials run ({n_prog} all in); across the programme the smallest Benjamini-Hochberg q among these nine is {qmin:.2f}.")
assert "HENRIK: filled by build_part1.py" not in md
os.makedirs(os.path.join(ROOT, "linkedin"), exist_ok=True)
write_article(ROOT, STEM, md, "Minority Report, Part 1: Where to Look")

# ---------------------------------------------------------------- one-pager (click teaser, 00_Planning/TEASER_STYLE_2026-10-21.md)
lo, hi = U1.loc[list(NAMES), "gross_ann"].min(), U1.loc[list(NAMES), "gross_ann"].max()
post = f"""MINORITY REPORT, PART 1: where do the machines find anything?

Almost every fund now sells an AI edge. Few of us have watched a stock-picking model meet its trading bill.

The best-known evidence: Gu, Kelly & Xiu (2020) found that tree models and neural nets predict US stock returns better than linear models.

I gave eight standard models the same twelve inputs, fixed every setting in advance, and ran them on the S&P 500, on 2,000 US small caps and on European blue chips. In one of the three, all eight earned {lo * 100:.0f}% to {hi * 100:.0f}% a year before costs. None of nine pre-registered tests passed; the interesting part is why.

Three questions:
1. Same models, same inputs: where do they find something, the 500 largest stocks or the 2,000 small ones?
2. How much of a +15% a year signal is left after trading costs?
3. Which slow one-line rule kept more than the machines after costs in small caps (and only there)?

Your answer to question 1 in the comments, then check it here, with tables, code and the pre-registrations: {REPO} · Not investment advice.

#machinelearning #AI #investing #quant
"""
write_teaser(ROOT, post, "hero_minority_report_part1_teaser.png", "Minority Report, Part 1", "24 November 2026")
click_layout(ROOT, "teaser_precogs_part1.png", alt="Drawing: the three questions inside three precogs' crystal balls")
try:
    make_pdfs(ROOT, STEM)
except Exception as e:  # no browser here: print the PDFs on Windows
    print("PDFs not built here:", type(e).__name__)
print("words in post:", len(post.split()))
