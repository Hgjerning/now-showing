# -*- coding: utf-8 -*-
import json, os
import build_teasers_xs as BT
RES = os.environ.get("FS_RESULTS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
r = json.load(open(os.path.join(RES, "impact.json"))); rb = json.load(open(os.path.join(RES, "impact_buffer.json")))
U = ["US", "EU", "UK", "DK", "SC", "WD"]
rows = [(BT.LAB[R], [(r[R]["shortlist"]["Y07"]["sharpe"][0], BT.BLUE, "o"), (r[R]["shortlist"]["Y07"]["sharpe"][2], BT.ORANGE, "s"), (r[R]["shortlist"]["Y07"]["sharpe"][3], BT.GREY, "D")]) for R in U]
def m(x):
    return "none" if not x else (f"${x/1e9:.1f}bn" if x >= 1e9 else f"${x/1e6:.0f}m")
BT.card("fs16_card.png", "FS16", "Costs that grow with size", "Low beta + momentum after spread and market impact, 2013–2026", rows,
        [("$1m", BT.BLUE, "o"), ("$100m", BT.ORANGE, "s"), ("$1bn", BT.GREY, "D")], "In Europe alone the edge is gone before $100m.",
        xlabel="Sharpe ratio, net, by capital in the book", xlim=(-3.5, 1.2))
cz = {R: m(r[R]["shortlist"]["Y07"]["capacity"]["zero"]) for R in U}
post = f"""Most backtests charge a flat cost per trade. Real costs grow with the size of the trade.

I re-costed the strategies from my factsheet series with a spread that depends on how liquid each stock is, plus the square-root market-impact law, at $1m, $10m, $100m, $1bn and $10bn.

For the pair that held up best (low beta plus momentum, market-neutral), the net return reaches zero at about:
→ US: {cz['US']}
→ World: {cz['WD']}
→ EU: {cz['EU']}
→ UK: {cz['UK']}
→ Denmark: {cz['DK']}
→ Scandinavia: no positive result even at $1m

The best-looking markets at small size, the UK and EU, fill up first: their low-beta legs sit in thinly traded stocks. Fast signals like short-term reversal are negative already at $10m.

The cheapest fix is patience. Holding a stock until it falls well out of the top group halves turnover and lifts capacity several times, with little loss at small size.

Lesson: many factor results are small-fund results. Ask what size the backtest was run at.

Full factsheet: {BT.PAGES}/fs16-costs-and-capacity

#investing #quant #factorinvesting #tradingcosts #backtesting"""
BT.page("fs16", "fs16_card.png", post, "FS16 Costs that grow with size")
print("teaser FS16")
