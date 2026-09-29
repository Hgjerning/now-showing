# -*- coding: utf-8 -*-
import json, os
import build_teasers_xs as BT
from battery import DIRECTION
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
A = json.load(open(os.path.join(RES, "art_battery.json")))["pooled"]; CG = json.load(open(os.path.join(RES, "common_ground.json")))["price"]
MF = json.load(open(os.path.join(RES, "art_fs14.json"))); F = json.load(open(os.path.join(RES, "art_fmb.json")))["pooled"]
L = json.load(open(os.path.join(RES, "trial_ledger.json")))
sig = ["beta", "vol252", "mom", "resmom", "seas", "max1", "r1", "skew"]
rows = [(DIRECTION[s][2], [(CG[s]["bn"]["t"], BT.BLUE, "o"), (A[s]["bn"]["t"], BT.ORANGE, "s")]) for s in sig]
sh = MF["short_vs_alleq"]; po = MF["pooled"]; pr = MF["primary"]
BT.card("fs15_card.png", "FS15", "The earlier history", "Same rules, 1998–2013: two bear markets the model never saw", rows,
        [("2013–2026", BT.BLUE, "o"), ("1999–2013", BT.ORANGE, "s")], f"Low beta + momentum: Sharpe {po['SHORT']['sharpe']:.2f} out of sample.",
        xlabel="t-statistic, beta-neutral book, cross-market average", xlim=(-10, 4))
post = f"""I tested my conclusions on data they had never seen: 1998–2013, including the dot-com bust and 2008.

Same 19 signals, same directions, same costs, same pre-registered multifactor rules. The history comes from an old research database of mine, with delisted stocks included, for the US, Europe, the UK and Denmark.

→ Low beta is confirmed: positive in all four markets in both periods (t {A['beta']['bn']['t']:.1f} before 2013).
→ Momentum keeps its sign, and in a regression with all signals it again adds return (t {F['mom']['t']:.1f}).
→ Low skewness loses in both periods (t {A['skew']['bn']['t']:.1f}). In large caps, lottery-like stocks kept earning more, not less.
→ Seasonality flips: strong before 2013, failed after. Published and then faded.
→ The dynamic multifactor selection fails its pre-registered test again ({pr['ann']*100:+.1f}% a year, t {pr['t']:.1f}).

And the result I did not expect: the simple pair I picked from the later data, low beta plus momentum, beat owning every signal by {sh['ann']*100:+.1f}% a year (t {sh['t']:.1f}) in all four markets, with near-zero correlation to the market. Out of sample, by construction.

It still does not clear the correction for all {L['n']} tests I have run. But it is the closest thing to common ground this series has found.

Full factsheet and pre-registration: {BT.PAGES}/fs15-earlier-history

#investing #quant #factorinvesting #research #backtesting"""
BT.page("fs15", "fs15_card.png", post, "FS15 The earlier history")
print("teaser FS15")
