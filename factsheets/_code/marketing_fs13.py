# -*- coding: utf-8 -*-
"""Marketing kit for FS13 and the factsheet series: LinkedIn card + post, LinkedIn carousel (PDF),
X thread, newsletter blurb, series-launch post. All numbers read from the results files."""
import base64
import json
import os

import build_teasers_xs as BT
from common_ground import U, UN, LAB

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); RES = os.path.join(ROOT, "results"); FIG = os.path.join(ROOT, "figures")
OUT = os.path.join(ROOT, "teasers"); MK = os.path.join(OUT, "marketing"); os.makedirs(MK, exist_ok=True)
PAGES = BT.PAGES; BLUE, ORANGE, GREY = BT.BLUE, BT.ORANGE, BT.GREY
p = lambda x, d=1: f"{x * 100:+.{d}f}%"


def load():
    O = json.load(open(os.path.join(RES, "common_ground.json"))); FIN = json.load(open(os.path.join(RES, "financing.json")))
    th = {r["theme"]: r for r in O["themes"]}; PS = O["price"]
    return O, FIN, th, PS


def card(O, th):
    names = ["Momentum", "Low risk", "Debt issuance", "Profit growth", "Value", "Short-term reversal", "Seasonality", "Tail direction (skewness)"]
    short = {"Tail direction (skewness)": "Skewness", "Short-term reversal": "Reversal"}
    rows = []
    for n in names:
        r = th[n]; v = []
        if r.get("price"): v.append((r["price"]["t"], BLUE, "o"))
        if r.get("jkp"): v.append((r["jkp"]["t"], ORANGE, "s"))
        rows.append((short.get(n, n), v))
    common = [r["theme"] for r in O["themes"] if r["verdict"].startswith("Common ground")]
    BT.card("fs13_card.png", "FS13", "Every signal, every corner", "19 price signals × 6 markets + 153 published factors, 2013–2026", rows,
            [("our engine, 6 markets", BLUE, "o"), ("JKP, 4 segments", ORANGE, "s")],
            "Positive in every corner: " + ", ".join(c.lower() for c in common) + ".", xlabel="t-statistic of the cross-market average (|t| > 2 = significant)", xlim=(-6.5, 7))


def texts(O, FIN, th, PS):
    lb, mo, rm, se = PS["beta"]["bn"], PS["mom"]["bn"], PS["resmom"]["bn"], PS["seas"]["bn"]
    mt, di, pg = th["Momentum"], th["Debt issuance"], th["Profit growth"]
    nbh = sum(PS[s]["bn"]["bh"] + PS[s]["raw"]["bh"] for s in PS); strong = [k for k in O["replication"] if O["replication"][k]["US"] >= 0.8]
    ag = O["agree_price_mean"]; nc_us = FIN["beta"]["US"]["net_cash"]; JS = O["jkp_summary"]
    faded = [r["theme"].lower() for r in O["themes"] if "faded" in r["verdict"]]
    link = f"{PAGES}/fs13-signal-battery"
    li = f"""I put every signal in every corner.

19 price signals × 6 markets (US, Europe, UK, Denmark, Scandinavia, World), 2013–2026, point-in-time index members, after costs. Plus the 153 published factors of Jensen, Kelly & Pedersen, by country.

The question: what works everywhere, and not just in one market?

→ After correcting for 38 tests, no price signal earns a positive return that survives on its own. Thirteen years of large caps is too short to prove a single signal.
→ The direction is more consistent than the significance. Momentum is positive in {mt['price']['pos']} of 6 of my markets and all {mt['jkp']['pos']} published segments (t {mt['jkp']['t']:.1f} there, {mt['price']['t']:.1f} in my large caps after borrow fees).
→ Low beta is positive in {lb['pos']} of 6, once you remove the market bet and pay for the leverage it needs ({nc_us:.1f}× borrowed in the US).
→ 19 signals are really two bets: a low-risk block of nine and a momentum block of four.
→ In the fundamentals, debt issuance (t {di['jkp']['t']:.1f}) and profit growth (t {pg['jkp']['t']:.1f}) worked in every segment. {', '.join(faded[:-1]).capitalize()} and {faded[-1]} faded in the US.
→ Seasonality and skewness lose reliably in large caps{' (seasonality is the one signal that survives the correction, as a loser)' if PS['seas']['bn']['bh'] else ''}.
→ Scandinavia marches to its own drum: its ranking of what works has a {ag['SC']:.2f} correlation with the other markets.

Engine check: my US signals correlate 0.8 or more with the published factors for {len(strong)} of {len(O['replication'])}.

Full factsheet with every number, the test design and what goes into the multifactor model next: {link}

#investing #quant #factorinvesting #momentum #research"""
    x = [f"1/ I put every signal in every corner: 19 price signals × 6 markets, 2013–26, point-in-time, after costs, plus 153 published JKP factors. What works everywhere? 🧵".replace(" 🧵", ""),
         "2/ After correcting for 38 tests, no price signal earns a positive return that survives on its own. 13 years of large caps can't prove one signal alone.",
         f"3/ The direction is more consistent. Momentum: positive in {mt['price']['pos']}/6 markets and {mt['jkp']['pos']}/4 published segments (t {mt['jkp']['t']:.1f}). Low beta: {lb['pos']}/6 after removing beta, borrow fees and leverage costs.",
         "4/ 19 signals ≈ 2 bets. MAX, MIN, range, idio vol, vol and beta are one low-risk block; momentum, 52w high, 52w low distance and the breakout are another.",
         f"5/ Fundamentals that worked everywhere since 2013: debt issuance (t {di['jkp']['t']:.1f}) and profit growth (t {pg['jkp']['t']:.1f}). Faded in the US: {', '.join(faded)}.",
         f"6/ Scandinavia's ranking of what works has ~{ag['SC']:.2f} correlation with other markets. Small markets are single-stock stories. Full factsheet: {link}"]
    nl = f"""**Every signal, every corner (FS13).** I ran all 19 price signals in six markets and set them against the 153 published JKP factors to find what works everywhere. After correcting for 38 tests no price signal earns a positive return that survives on its own; thirteen years of large caps can't prove any one signal. The direction is more consistent: momentum is positive in {mt['price']['pos']} of 6 markets and every published segment, low beta in {lb['pos']} of 6 once the market bet is removed, borrow is paid and leverage financed, and debt issuance and profit growth lead the fundamentals. The 19 signals are really two bets, low risk and momentum. Seasonality and skewness lose in large caps, and Scandinavia disagrees with everyone. [Read the factsheet]({link})"""
    series = f"""Fourteen factsheets, one set of rules.

Over the past weeks I ran the famous strategies (Turtle Traders, the lottery factor, momentum, low volatility, betting against beta, the 52-week high and low, size, seasonality, reversal, residual momentum, even 10,000 dart-throwing monkeys) through the same code on six point-in-time markets, 2013–2026, after costs.

Each factsheet has the P&L, trade records, drawdowns, factor attribution, what goes wrong and how to fix it, where the strategy fits, and a 360° view of its neighbours.

Three things stood out:
→ Most folklore fails where it fights momentum.
→ Raw long/short numbers in a bull market are mostly a hidden market bet.
→ Six markets are not six tests: they co-move so much that they count as fewer than two.

FS00 sums it all up in one table, with a gap analysis of what is still missing. FS13 asks which signals work in every corner.

{PAGES}

#investing #quant #factorinvesting #backtesting"""
    return li, x, nl, series


def carousel(O, FIN, th, PS):
    lb, mo = PS["beta"]["bn"], PS["mom"]["bn"]; mt, di, pg = th["Momentum"], th["Debt issuance"], th["Profit growth"]
    nbh = sum(PS[s]["bn"]["bh"] + PS[s]["raw"]["bh"] for s in PS); ag = O["agree_price_mean"]
    img = lambda f: "data:image/png;base64," + base64.b64encode(open(os.path.join(FIG, f), "rb").read()).decode()
    best = sorted(PS, key=lambda s: -abs(PS[s]["bn"]["t"]))[:4]
    slides = [
        ("STRATEGY FACTSHEET FS13", "Every signal,<br>every corner", "19 price signals × 6 markets<br>+ 153 published factors<br>2013–2026, after costs", None),
        ("THE TEST", "What works everywhere,<br>not just in one market?", "US · Europe · UK · Denmark · Scandinavia · World<br>point-in-time index members, 10 bp per side<br>beta-neutral books pay for their leverage<br>JKP factors: US, UK, Denmark, World ex US", None),
        ("FINDING 1", "After 38 tests,<br>no winner survives alone", "Largest |t|: " + " · ".join(f"{LAB[s]} t {PS[s]['bn']['t']:+.1f}" for s in best) + "<br>Thirteen years of large caps can't prove a single signal.", None),
        ("FINDING 2", "Momentum and low beta<br>point the right way", f"Momentum: {mt['price']['pos']} of 6 markets in my data · {mt['jkp']['pos']} of 4 published segments (t {mt['jkp']['t']:.1f})<br>Low beta: {lb['pos']} of 6 after beta, borrow and leverage costs", "fs13_common_map.png"),
        ("FINDING 3", "19 signals,<br>really two bets", "One low-risk block of nine (MAX, MIN, range, volatility, beta)<br>one momentum block of four. Same structure in US, EU, World.", "fs13_corr.png"),
        ("FINDING 4", "Fundamentals: debt issuance<br>and profit growth", f"Positive in every JKP segment since 2013 (t {di['jkp']['t']:.1f} and {pg['jkp']['t']:.1f})<br>Value, investment and accruals faded in the US", "fs13_jkp_themes.png"),
        ("FINDING 5", "Scandinavia marches<br>to its own drum", f"Agreement with the other markets on what works:<br>Scandinavia {ag['SC']:.2f} · Denmark {ag['DK']:.2f} · World {ag['WD']:.2f} · US {ag['US']:.2f}", None),
        ("NEXT", "Into the<br>multifactor model", "Carry: low beta, momentum, residual momentum, 52-week high<br>Add: debt issuance, profit growth<br>Drop: seasonality, reversal, skewness<br><br>Full factsheet: hgjerning.github.io/now-showing/factsheets", None),
    ]
    css = """@page{size:1080px 1350px;margin:0}body{margin:0;font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif}
    .s{width:1080px;height:1350px;box-sizing:border-box;padding:90px 80px;background:#fcfcfb;color:#0b0b0b;page-break-after:always;position:relative;overflow:hidden}
    .k{color:#2a78d6;font-weight:700;font-size:30px;letter-spacing:1px}.h{font-size:78px;font-weight:800;line-height:1.08;margin:36px 0 34px}
    .b{font-size:38px;line-height:1.5;color:#52514e}.i{margin-top:40px;width:100%;max-height:760px;object-fit:contain;border-radius:10px}.f{position:absolute;bottom:50px;left:80px;right:80px;font-size:24px;color:#8a8984;display:flex;justify-content:space-between}
    .s:first-child{background:#0b0b0b;color:#fcfcfb}.s:first-child .b{color:#c9c8c3}.s:first-child .h{font-size:110px}"""
    html = "".join(f"<div class='s'><div class='k'>{k}</div><div class='h'>{h}</div><div class='b'>{b}</div>{f'<img class=i src={img(f)}>' if f else ''}<div class='f'><span>Henrik Gjerning · Project 10</span><span>{i + 1} / {len(slides)}</span></div></div>" for i, (k, h, b, f) in enumerate(slides))
    fn = os.path.join(MK, "fs13_carousel.html"); open(fn, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{html}</body></html>")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg_ = b.new_page(); pg_.goto("file://" + fn); pg_.pdf(path=os.path.join(MK, "fs13_carousel_linkedin.pdf"), width="1080px", height="1350px", print_background=True); b.close()


if __name__ == "__main__":
    O, FIN, th, PS = load(); card(O, th)
    li, x, nl, series = texts(O, FIN, th, PS)
    BT.page("fs13", "fs13_card.png", li, "FS13 Every signal, every corner")
    open(os.path.join(MK, "fs13_x_thread.txt"), "w").write("\n\n".join(x))
    open(os.path.join(MK, "fs13_newsletter.md"), "w").write(nl)
    open(os.path.join(MK, "series_launch_post.txt"), "w").write(series)
    for i, t in enumerate(x):
        assert len(t) <= 280, (i, len(t))
    carousel(O, FIN, th, PS)
    kit = f"""# Marketing kit · FS13 and the factsheet series

## LinkedIn post (FS13) · with `fs13_card.png` or the carousel `fs13_carousel_linkedin.pdf` (upload as a document)

{li}

## LinkedIn carousel
`fs13_carousel_linkedin.pdf`: 8 slides, 1080×1350 (portrait, LinkedIn's document format).

## Series launch post (FS00–FS13) · use `../fs05_card.png` or the FS00 heatmap

{series}

## X / Twitter thread

""" + "\n\n".join(x) + f"""

## Newsletter / website blurb

{nl}

## Posting notes
- Post the carousel as a LinkedIn *document*; put the link in the first comment if reach matters more than clicks.
- The links point to GitHub Pages under `now-showing/factsheets/`, which is still marked unreleased in `.gitignore`: publish the folder before posting.
- Every number above is generated from `results/common_ground.json` and `results/financing.json` by `code/marketing_fs13.py`; re-run after any rebuild.
"""
    open(os.path.join(MK, "MARKETING_KIT.md"), "w").write(kit)
    print("marketing done")
