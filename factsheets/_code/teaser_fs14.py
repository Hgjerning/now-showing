# -*- coding: utf-8 -*-
"""LinkedIn card + post for FS14 (numbers from results/fs14.json)."""
import json, os
import build_teasers_xs as BT
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; LAB = BT.LAB
r = json.load(open(os.path.join(RES, "fs14.json"))); pr = r["primary"]; po = r["pooled"]
L = json.load(open(os.path.join(RES, "trial_ledger.json")))
best = max(r["variants"], key=lambda v: po[v]["sharpe"])
rows = [(LAB[R], [(r[R]["RP"]["sharpe"], BT.BLUE, "o"), (r[R]["ALL-EQ"]["sharpe"], BT.GREY, "D"), (r[R]["SHORT"]["sharpe"], BT.ORANGE, "s")]) for R in U]
ok = pr["t"] > 2 and pr["s1"] > 0 and pr["s2"] > 0
BT.card("fs14_card.png", "FS14", "The multifactor model", "Pre-registered selection and weighting, out of sample 2016–2026", rows,
        [("Dynamic selection (RP)", BT.BLUE, "o"), ("All books, equal", BT.GREY, "D"), ("Fixed shortlist*", BT.ORANGE, "s")],
        f"Beats owning everything by {pr['ann']*100:+.1f}% a year (t {pr['t']:.1f}): {'passes' if ok else 'not enough to pass'} its own bar.",
        xlabel="Sharpe ratio, out of sample, net (*chosen with hindsight)", xlim=(-0.8, 1.0))
post = f"""I wrote the rules down before I ran the model. Here is what happened.

FS14 is the last step of the factsheet series: take 25 market-neutral factor books (19 price signals in six markets, plus six US fundamental themes), and every month, using only the past:
→ keep the books with a credible 3-year record (probabilistic Sharpe ≥ 0.8, costs under half the gross spread),
→ drop near-duplicates (correlation above 0.7),
→ weight what is left (11 pre-registered rules, from equal weights to 60-month exponential mean/variance).

The bar, set in advance: beat owning all 25 books equally with t > 2, and in both 2016–19 and 2020–26.

Result: {pr['ann']*100:+.1f}% a year better (t {pr['t']:.1f}), positive in both periods, in {pr['pos']} of 5 markets. Not enough. The claim fails its own test.

Two more honest findings:
→ A fixed shortlist of low beta and momentum (plus profit growth and debt issuance in the US) did better, but I picked it after seeing the data.
→ None of these market-neutral books came close to simply owning the market over the same years.

After {L['n']} tests across 14 factsheets, that is the lesson: discipline protects you from fooling yourself more than it finds alpha.

Full factsheet, pre-registration and trial ledger: {BT.PAGES}/fs14-multifactor-model

#investing #quant #factorinvesting #research #backtesting"""
BT.page("fs14", "fs14_card.png", post, "FS14 The multifactor model")
print("teaser FS14")
