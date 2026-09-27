# -*- coding: utf-8 -*-
"""LinkedIn cards and posts for FS03-FS12 (and FS05) from the results files."""
import base64
import json
import os
import sys

import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import specs

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); RES = os.path.join(ROOT, "results"); OUT = os.path.join(ROOT, "teasers"); os.makedirs(OUT, exist_ok=True)
SURF, INK, INK2, GRID, BLUE, ORANGE, GREY = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0", "#2a78d6", "#eb6834", "#8a8984"
U = ["US", "EU", "UK", "DK", "SC", "WD"]; LAB = {"US": "US", "EU": "EU", "UK": "UK", "DK": "Denmark", "SC": "Scandinavia", "WD": "World"}
PAGES = "https://hgjerning.github.io/now-showing/factsheets"


def card(fname, code, title, sub, rows, legend, verdict, xlabel="Sharpe ratio, 2013–2026, after costs", xlim=(-1.6, 1.6)):
    fig = plt.figure(figsize=(8, 8)); fig.patch.set_facecolor(SURF)
    fig.text(0.06, 0.93, f"STRATEGY FACTSHEET {code}", fontsize=12, color=BLUE, fontweight="bold")
    fig.text(0.06, 0.865, title, fontsize=30 if len(title) < 22 else 24, color=INK, fontweight="bold")
    fig.text(0.06, 0.825, sub, fontsize=12.5, color=INK2)
    ax = fig.add_axes([0.06, 0.26, 0.88, 0.53]); ax.set_facecolor(SURF)
    for yi, (lab, vals) in zip(range(len(rows))[::-1], rows):
        for v, col, mk in vals:
            ax.scatter(v, yi, s=170, color=col, marker=mk, zorder=3, edgecolor=SURF, linewidth=2)
        ax.text(xlim[0] + 0.05, yi, lab, va="center", ha="left", fontsize=13, color=INK)
    ax.axvline(0, color=INK2, lw=1); ax.set_xlim(*xlim); ax.set_ylim(-0.7, len(rows) - 0.3); ax.set_yticks([])
    for sp_ in ax.spines.values(): sp_.set_visible(False)
    ax.grid(axis="x", color=GRID); ax.set_axisbelow(True); ax.set_xlabel(xlabel, color=INK2, fontsize=11); ax.tick_params(colors=INK2)
    for i, (l, col, mk) in enumerate(legend):
        fig.text(0.08 + i * 0.3, 0.135, {"o": "●", "s": "■", "D": "◆"}[mk], color=col, fontsize=15); fig.text(0.11 + i * 0.3, 0.137, l, color=INK, fontsize=11)
    fig.text(0.06, 0.075, verdict, fontsize=13 if len(verdict) < 70 else 11.5, color=INK, fontweight="bold")
    fig.text(0.06, 0.03, "Henrik Gjerning · Project 10 · point-in-time universes, local currency (World in USD)", fontsize=9.5, color=INK2)
    fig.savefig(os.path.join(OUT, fname), dpi=150, facecolor=SURF); plt.close(fig)


def page(stem, hero, post, title):
    css = "body{max-width:620px;margin:0 auto;padding:24px 16px;font:15px/1.55 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#0b0b0b;background:#fcfcfb}img{width:100%;border-radius:6px}p{margin:0 0 12px}.by{color:#52514e;font-size:13px;margin:10px 0 14px}@page{size:A4;margin:14mm}"
    b64 = base64.b64encode(open(os.path.join(OUT, hero), "rb").read()).decode()
    paras = "".join(f"<p>{x.replace(chr(10), '<br>')}</p>" for x in post.strip().split("\n\n"))
    open(os.path.join(OUT, f"{stem}_teaser.html"), "w").write(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}</title><style>{css}</style></head><body><img src='data:image/png;base64,{b64}' alt='{title}'><div class='by'>Henrik Gjerning · LinkedIn</div>{paras}</body></html>")
    open(os.path.join(OUT, f"{stem}_post.txt"), "w").write(post)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); pg.goto("file://" + os.path.abspath(os.path.join(OUT, f"{stem}_teaser.html"))); pg.pdf(path=os.path.join(OUT, f"{stem}_teaser.pdf"), format="A4", print_background=True); b.close()


def n6(k):
    return "all six" if k == 6 else ("none of the six" if k == 0 else f"{k} of six")


def xs_teaser(code):
    sp = specs.S[code]; J = json.load(open(os.path.join(RES, f"xs_{code}.json"))); per = J["per"]
    st = lambda R, b: per[R]["stats"][b]
    rows = [(LAB[R], [(st(R, "L/S (net)")["sharpe"], BLUE, "o"), (st(R, "Long-only (net)")["sharpe"], ORANGE, "s"), (st(R, "EW universe")["sharpe"], GREY, "D")]) for R in U]
    pos = sum(st(R, "L/S (net)")["ann_mean"] > 0 for R in U); lob = sum(st(R, "Long-only (net)")["sharpe"] > st(R, "EW universe")["sharpe"] for R in U)
    verdict = f"Long/short positive in {n6(pos)} markets; long-only beat owning all stocks in {n6(lob)}."
    good = sp["good"].split(" (")[0]
    card(f"{code.lower()}_card.png", code, sp["title"], sp["sub"], rows, [("Long/short", BLUE, "o"), (f"Long-only", ORANGE, "s"), ("Own all stocks equally", GREY, "D")], verdict)
    a = [st(R, "L/S (net)")["ann_mean"] for R in U]; al = [st(R, "L/S (net)")["alpha"] for R in U]
    steps = J["steps"]; h0, h1 = J["avg_holdout"][steps[0]], J["avg_holdout"][steps[-1]]
    near = [k for R in U for k in per[R]["nbh"]["near"][:1]]
    red = max(abs(per[R]["nbh"]["span"]["t"]["alpha"]) for R in U) < 2
    post = f"""{sp['claim']}

I tested it on six markets, 2013–2026: US, Europe, UK, Denmark, Scandinavia and the world. Point-in-time index members, after costs.

Long/short ({good} minus {sp['bad'].split(' (')[0]}): {min(a) * 100:+.1f}% to {max(a) * 100:+.1f}% a year, positive in {n6(pos)} markets. Adjusted for market beta: {min(al) * 100:+.1f}% to {max(al) * 100:+.1f}%.
Long-only ({good}): a better Sharpe than owning all the stocks equally in {n6(lob)} markets.

The pre-declared fixes (beta-neutral legs, a turnover buffer, volatility targeting) took the 2020–26 holdout Sharpe from {h0['sharpe']:.2f} to {h1['sharpe']:.2f}.

360° view: {'once its nearest neighbours are in the model, nothing is left: the signal is redundant.' if red else 'it keeps some information beyond its nearest neighbours.'}

Full factsheet with P&L, trade records, drawdowns, factor attribution, fixes, classification and the 360° view: {PAGES}/{sp['slug']}

#investing #quant #factorinvesting #backtesting"""
    page(code.lower(), f"{code.lower()}_card.png", post, f"{code} {sp['title']}")


def monkey_teaser():
    M = json.load(open(os.path.join(RES, "monkey_summary.json")))
    rows = [(LAB[R], [(M[R]["share_beat_cagr"] * 100, BLUE, "o"), (M[R]["share_beat_sharpe"] * 100, ORANGE, "s")]) for R in U]
    card("fs05_card.png", "FS05", "Monkey portfolios", "Can a blindfolded monkey beat the index?", rows,
         [("beat the index on return", BLUE, "o"), ("beat it on Sharpe", ORANGE, "s")], "Monkeys win where small beats big. That's all they know.",
         xlabel="share of 10,000 random portfolios, %", xlim=(-20, 100))
    b = [M[R]["share_beat_cagr"] for R in U]
    post = f"""Burton Malkiel (1973): a blindfolded monkey throwing darts at the stock pages could do as well as the experts.

I let 10,000 monkeys pick 10–30 stocks every January in six markets, 2013–2026, point-in-time index members, after costs.

Share of monkeys that beat the index: {', '.join(f"{LAB[R]} {M[R]['share_beat_cagr'] * 100:.0f}%" for R in U)}.

The monkeys are not lucky or clever. A random portfolio is an equal-weight portfolio, and equal weight is a bet on small companies. They win in the years small beats big and lose when the mega-caps lead, as they did in the US.

The lesson for any stock picker: compare yourself with the equal-weight universe as well as the index, or a size tilt will look like skill.

Full factsheet: {PAGES}/fs05-monkey-portfolios

#investing #quant #indexing #behavioralfinance"""
    page("fs05", "fs05_card.png", post, "FS05 Monkey portfolios")


if __name__ == "__main__":
    for c in (sys.argv[1:] or specs.ORDER):
        xs_teaser(c); print("teaser", c)
    monkey_teaser(); print("teaser FS05")
