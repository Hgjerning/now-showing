# -*- coding: utf-8 -*-
import json, os
import build_teasers_xs as BT
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
r = json.load(open(os.path.join(RES, "fs18.json"))); M = r["markets"]; P = r["pooled_5e+07"]
U = ["US", "EU", "UK", "DK", "SC", "WD"]
rows = [(BT.LAB[R], [(M[R]["5e+07"]["market"]["sharpe"], BT.GREY, "D"), (M[R]["5e+07"]["portfolio"]["sharpe"], BT.BLUE, "o"), (M[R]["2e+08"]["portfolio"]["sharpe"], BT.ORANGE, "s")]) for R in U]
BT.card("fs18_card.png", "FS18", "The portfolio I would actually run", "Market + a 5%-volatility overlay of what survived, net of costs, 2014–2026", rows,
        [("market alone", BT.GREY, "D"), ("+ overlay, $50m", BT.BLUE, "o"), ("+ overlay, $250m", BT.ORANGE, "s")], "A small edge in big markets. Nothing in the Nordics.",
        xlabel="Sharpe ratio (excess of T-bills)", xlim=(0, 1.2))
g = {R: M[R]["5e+07"]["sharpe_diff"] for R in U}
post = f"""18 factsheets later, here is the portfolio I would actually run.

Hold the market. Next to it, run a small market-neutral overlay made only of what survived the series: low beta and 12-1 momentum everywhere, plus profit growth and debt issuance in the US. Size it to 5% volatility. Charge every cost: spread, market impact, borrow fees, financing.

Result, 2014–2026, at $50m per book, change in Sharpe ratio vs the market alone:
→ US: {g['US']:+.2f}
→ EU: {g['EU']:+.2f}
→ UK: {g['UK']:+.2f}
→ World: {g['WD']:+.2f}
→ Denmark: {g['DK']:+.2f}
→ Scandinavia: {g['SC']:+.2f}

Pooled, the overlay adds {P['ann']*100:.1f}% a year with t = {P['t']:.2f}. My pre-registered bar was t > 2. Not passed, narrowly.

At $250m per book the gain halves or worse outside the US, and turns negative in the UK and the Nordics.

So: a small, cheap overlay in large, liquid markets earns its place. It is not a strategy that scales, and the Nordics are not the place for it.

That is the honest end of the series. Every test, including the ones that failed, is in the public trial ledger.

Full factsheet: {BT.PAGES}/fs18-portfolio-i-would-run

#investing #quant #factorinvesting #portfolioconstruction #backtesting"""
BT.page("fs18", "fs18_card.png", post, "FS18 The portfolio I would actually run")
print("teaser FS18")
