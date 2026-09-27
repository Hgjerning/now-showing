# -*- coding: utf-8 -*-
"""LinkedIn one-pagers for the factsheet sidebar: a data card (hero) + post text -> teaser.html/pdf."""
import base64, json, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); RES = os.path.join(ROOT, "results"); OUT = os.path.join(ROOT, "teasers"); os.makedirs(OUT, exist_ok=True)
SURF, INK, INK2, GRID, BLUE, ORANGE, GREY = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0", "#2a78d6", "#eb6834", "#8a8984"
U = ["US", "EU", "UK", "DK", "SC", "WD"]; LAB = {"US": "US", "EU": "EU", "UK": "UK", "DK": "Denmark", "SC": "Scandinavia", "WD": "World"}
PAGES = "https://hgjerning.github.io/now-showing/factsheets"


def card(fname, code, title, sub, rows, legend, verdict):
    fig = plt.figure(figsize=(8, 8)); fig.patch.set_facecolor(SURF)
    fig.text(0.06, 0.93, f"STRATEGY FACTSHEET {code}", fontsize=12, color=BLUE, fontweight="bold", family="DejaVu Sans")
    fig.text(0.06, 0.865, title, fontsize=30, color=INK, fontweight="bold")
    fig.text(0.06, 0.825, sub, fontsize=12.5, color=INK2)
    ax = fig.add_axes([0.06, 0.26, 0.88, 0.53]); ax.set_facecolor(SURF)
    y = range(len(rows))[::-1]
    for yi, (lab, vals) in zip(y, rows):
        for k, (v, col, mk) in enumerate(vals):
            ax.scatter(v, yi, s=170, color=col, marker=mk, zorder=3, edgecolor=SURF, linewidth=2)
        ax.text(-1.55, yi, lab, va="center", ha="left", fontsize=13, color=INK)
    ax.axvline(0, color=INK2, lw=1); ax.set_xlim(-1.6, 1.4); ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.set_yticks([]); ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.tick_params(colors=INK2, labelsize=10)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.grid(axis="x", color=GRID); ax.set_axisbelow(True); ax.set_xlabel("Sharpe ratio, 2013–2026, after costs", color=INK2, fontsize=11)
    for i, (l, col, mk) in enumerate(legend):
        fig.text(0.08 + i * 0.3, 0.135, "●" if mk == "o" else "■" if mk == "s" else "◆", color=col, fontsize=15)
        fig.text(0.11 + i * 0.3, 0.137, l, color=INK, fontsize=11)
    fig.text(0.06, 0.075, verdict, fontsize=13.5, color=INK, fontweight="bold")
    fig.text(0.06, 0.03, "Henrik Gjerning · Project 10 · point-in-time universes, local currency (World in USD)", fontsize=9.5, color=INK2)
    fig.savefig(os.path.join(OUT, fname), dpi=150, facecolor=SURF); plt.close(fig)


def page(stem, hero, post, title):
    css = "body{max-width:620px;margin:0 auto;padding:24px 16px;font:15px/1.55 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#0b0b0b;background:#fcfcfb}img{width:100%;border-radius:6px}p{margin:0 0 12px}.by{color:#52514e;font-size:13px;margin:10px 0 14px}@page{size:A4;margin:14mm}"
    b64 = base64.b64encode(open(os.path.join(OUT, hero), "rb").read()).decode()
    paras = "".join(f"<p>{x.replace(chr(10), '<br>')}</p>" for x in post.strip().split("\n\n"))
    html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}</title><style>{css}</style></head><body><img src='data:image/png;base64,{b64}' alt='{title}'><div class='by'>Henrik Gjerning · LinkedIn</div>{paras}</body></html>"
    open(os.path.join(OUT, f"{stem}_teaser.html"), "w").write(html); open(os.path.join(OUT, f"{stem}_post.txt"), "w").write(post)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); pg.goto("file://" + os.path.abspath(os.path.join(OUT, f"{stem}_teaser.html"))); pg.pdf(path=os.path.join(OUT, f"{stem}_teaser.pdf"), format="A4", print_background=True); b.close()


T = json.load(open(os.path.join(RES, "turtle_summary.json"))); L = json.load(open(os.path.join(RES, "lottery_summary.json"))); F = json.load(open(os.path.join(RES, "fix_summary.json")))
M, LO, B = "Turtle L/S (S1+S2)", "Turtle long-only (S1+S2)", "EW universe (benchmark)"
rows = [(LAB[R], [(T[R]["stats"][M]["sharpe"], BLUE, "o"), (T[R]["stats"][LO]["sharpe"], ORANGE, "s"), (T[R]["stats"][B]["sharpe"], GREY, "D")]) for R in U]
card("fs01_card.png", "FS01", "The Turtle Traders", "Richard Dennis's 1983 rules, stock by stock, six markets",
     rows, [("Turtle long/short", BLUE, "o"), ("Turtle long-only", ORANGE, "s"), ("Own all stocks equally", GREY, "D")],
     "Long/short lost in all six. Long-only never beat owning all stocks.")
t = F["turtle"]["avg_holdout"]
post1 = f"""In 1983 Richard Dennis bet that trading could be taught. He hired 23 novices, gave them one rulebook, and they reportedly made over $100 million trading futures.

I ran the same rules on single stocks in six markets, 2013–2026: US, Europe, UK, Denmark, Scandinavia and the world. Point-in-time index members, after costs.

The long/short version lost money in all six markets (Sharpe {min(T[R]['stats'][M]['sharpe'] for R in U):.2f} to {max(T[R]['stats'][M]['sharpe'] for R in U):.2f}).
The long-only version made money, but had a lower Sharpe than simply owning all the stocks equally, in every market.

Why? Four things: costs from oversized positions, shorting a bull market, a stop tighter than a normal day's noise, and at the root: single stocks do not trend at these horizons. A new 55-day high predicts nothing about the next 60 days.

Fixing what can be fixed gives a half-beta equity book, not an edge (holdout Sharpe {t['T3 + 4N stop']['sharpe']:.2f} vs {t["EW universe"]["sharpe"]:.2f} for owning all the stocks). The rules were built for futures. That is where they belong.

This is the first strategy factsheet: rules, data, full P&L, trade records, drawdowns, factor attribution, what goes wrong, and where the strategy fits.

Full factsheet: {PAGES}/fs01-turtle-traders

#investing #quant #trendfollowing #backtesting"""
page("fs01", "fs01_card.png", post1, "FS01 The Turtle Traders")
LS, LLO = "L/S low minus high MAX (net)", "Low-MAX long-only (net)"
rows = [(LAB[R], [(L[R]["stats"][LS]["sharpe"], BLUE, "o"), (L[R]["stats"][LLO]["sharpe"], ORANGE, "s"), (L[R]["stats"][B]["sharpe"], GREY, "D")]) for R in U]
card("fs02_card.png", "FS02", "The lottery factor", "Do investors overpay for stocks that just had one huge day?",
     rows, [("Low minus high MAX", BLUE, "o"), ("Calmest stocks only", ORANGE, "s"), ("Own all stocks equally", GREY, "D")],
     "The anomaly was beta in disguise. Hedge it, and nothing is left.")
lh = F["lottery"]["pooled"]["L1_vs_zero_holdout"]
post2 = f"""Would you buy a lottery ticket? Many investors do, in stock form: they chase the stocks that just had one spectacular day.

Bali, Cakici & Whitelaw (2011) showed that US stocks with the biggest one-day jump last month earned about 1% a month less afterwards. Investors overpay for the thrill.

I tested it in six markets, 2013–2026, point-in-time members, after costs. Buying the calmest stocks and shorting the most lottery-like lost money in all six markets ({min(L[R]['stats'][LS]['ann_mean'] for R in U) * 100:+.0f}% to {max(L[R]['stats'][LS]['ann_mean'] for R in U) * 100:+.0f}% a year).

The catch is beta. Lottery stocks carry a beta of about 1.3, calm stocks about 0.7. In a 13-year bull market that alone decides the race. Hedge the beta and the loss disappears, and so does the premium: {lh['ann'] * 100:+.1f}% a year, t {lh['t']:.1f}.

The calm stocks on their own still did what low-risk investing promises: smaller drawdowns in every market and a better Sharpe than owning all the stocks in three of six.

Where does it fit? Not a factor of its own, but a noisier member of the low-risk family.

Full factsheet: {PAGES}/fs02-lottery-max

#investing #quant #factorinvesting #behavioralfinance"""
page("fs02", "fs02_card.png", post2, "FS02 The lottery factor")
print(os.listdir(OUT))
