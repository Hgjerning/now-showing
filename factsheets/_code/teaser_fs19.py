# -*- coding: utf-8 -*-
import json, os
import build_teasers_xs as BT
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
r = json.load(open(os.path.join(RES, "fs19.json"))); C = r["C"]["markets"]; B = r["B"]["episodes"]
U = ["US", "EU", "UK", "DK", "SC", "WD"]
rows = [(BT.LAB[R], [(C[R]["shortlist | raw"]["ann"] * 100, BT.GREY, "D"), (C[R]["shortlist | sector-neutral"]["ann"] * 100, BT.BLUE, "o")]) for R in U]
BT.card("fs19_card.png", "FS19", "Bug, luck or sector bet?", "Low beta + momentum, net return a year, 2013–2026", rows,
        [("unrestricted", BT.GREY, "D"), ("ranked within sectors", BT.BLUE, "o")], "Two thirds survive inside sectors. The engine is clean.",
        xlabel="net return, % a year", xlim=(-9, 22))
ps, pr = r["C"]["pooled | sector-neutral"], r["C"]["pooled | raw"]
post = f"""Before you trust a backtest, try to break it. I tried three ways.

1. Is it a bug? I rebuilt every signal from data cut off in 2015, 2019 and 2023: identical values, so no peeking at the future. On random noise the strategies earn nothing, as they should. A deliberate cheat (next month's return as the signal) is caught instantly.

2. Is it a sector bet? Ranked only within sectors, the low beta + momentum pair keeps {ps['ann']*100:.1f}% a year (t {ps['t']:.1f}) of its {pr['ann']*100:.1f}%. About two thirds is stock picking, not sector timing.

3. Is it a few lucky episodes? Here is the surprise. The "market-neutral" low-beta book lost {abs(B['US']['COVID crash']['low beta'])*100:.0f}% in the US in the COVID crash and {abs(B['US']['2022 rate shock']['low beta'])*100:.0f}% in 2022. Low betas drift up and high betas drift down, so a book that is neutral on paper still carries market risk. Momentum did the hedging, and the combined overlay stayed within ±8% in every episode.

Lesson: "beta-neutral" in a backtest usually means neutral on estimated betas. Check the realised beta.

Full factsheet: {BT.PAGES}/fs19-robustness

#investing #quant #factorinvesting #backtesting #riskmanagement"""
BT.page("fs19", "fs19_card.png", post, "FS19 Robustness")
print("teaser FS19")
