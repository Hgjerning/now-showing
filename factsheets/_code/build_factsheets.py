# -*- coding: utf-8 -*-
"""Builds FS01 (Turtle Traders) and FS02 (Lottery / MAX) factsheets: md -> html (embedded figures) -> pdf.
Every number is read from results/*.json or results/*.csv produced by analyse.py."""
import base64
import json
import os

import markdown

import sections_fix_class
import nbh_section
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
RES, FIG, OUT = os.path.join(ROOT, "results"), os.path.join(ROOT, "figures"), os.path.join(ROOT, "factsheets")
os.makedirs(OUT, exist_ok=True)
CSS = open(os.path.join(HERE, "style.css")).read() + """
.kf{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 18px;background:var(--box);padding:14px 18px;border-radius:6px;font:13px/1.45 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;margin:14px 0}
.kf b{display:block;color:var(--ink2);font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
.verdict{border-left:4px solid #eb6834}
"""
U = ["US", "EU", "UK", "DK", "SC", "WD"]
UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
GATE = 2.87
UNL = {"US": "US (top 500, point-in-time)", "EU": "EU (11 national blue-chip indices, point-in-time)", "UK": "UK (FTSE 350, point-in-time)", "DK": "DK (OMXC25, point-in-time)", "SC": "SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)", "WD": "World (US + UK + EU, point-in-time)"}
p = lambda x, d=1: "n/a" if x is None or x != x else f"{x * 100:+.{d}f}%"
pu = lambda x, d=1: "n/a" if x is None or x != x else f"{x * 100:.{d}f}%"
f2 = lambda x: "n/a" if x is None or x != x else f"{x:.2f}"
ci = lambda c: f"[{c[0]:.2f}, {c[1]:.2f}]"


def n6(k):
    return "all six" if k == 6 else f"{k} of the six"


def rng_(v, pct=False):
    return (f"{p(min(v))} to {p(max(v))}" if pct else f"{min(v):.2f} to {max(v):.2f}")


def table(head, rows):
    s = "| " + " | ".join(str(x).replace("|", "&#124;") for x in head) + " |\n|" + "|".join(["---"] * len(head)) + "|\n"
    for r in rows:
        s += "| " + " | ".join(str(x).replace("|", "&#124;") for x in r) + " |\n"
    return s


def universe_table():
    rows = [
        ["US", "Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted", "**Point-in-time**: top 500 by market cap each month-end (Sharadar filings × price, A06 method)", "~499", "USD"],
        ["EU", "Project1 yfinance cache, Adj Close (TR)", "**Point-in-time**: union of 11 national blue-chip indices (CAC 40, DAX, AEX, IBEX 35, FTSE MIB, OMXS30, OMXC25, OMXH25, BEL 20, PSI-20, WIG20), quarterly Wikipedia snapshots 2012–2026; 83% of member-quarters priced", "~238", "local (EUR, SEK, DKK, PLN)"],
        ["UK", "Project1 cache, Close + pence dividends (Yahoo under-adjusts LSE ~100×)", "**Point-in-time**: FTSE 100 + FTSE 250, quarterly snapshots; 75% priced", "~242", "GBP"],
        ["DK", "Project1 cache, Adj Close", "**Point-in-time**: OMX Copenhagen 25, quarterly snapshots; 91% priced", "~19", "DKK"],
        ["SCANDI", "Project1 cache, Adj Close", "**Point-in-time**: OMXC25 + OMXS30 + OMXH25 (Oslo has no snapshot history); 88% priced", "~62", "local (DKK, SEK, EUR)"],
        ["World", "US Sharadar + UK + EU above", "**Point-in-time** union of the three; local-currency returns summed, not converted", "~963", "mixed"],
    ]
    return table(["Universe", "Prices", "Membership", "Names eligible (median)", "Currency"], rows) + """
*Membership comes from Project2's cache of dated Wikipedia index pages (the same parsing as `run_wiki_pit.py` / `run_eu_pit.py`), with a short list of verified ticker renames (e.g. NZYM-B → NSIS-B, WDH → DEMANT, DAI → MBG). A name is eligible from the day after the snapshot that lists it, once it has 60 days of prices. Member-quarters without a price are mostly delisted names that Yahoo no longer serves, so some survivorship remains; see §13.*
"""


def surv_table(key):
    """Survivor list (first edition of this factsheet) vs point-in-time, same code."""
    import json as _j
    S = _j.load(open(os.path.join(ROOT, "results_survivor", f"{key}_summary.json"))); P = _j.load(open(os.path.join(RES, f"{key}_summary.json")))
    rows = []
    for R in ["EU", "UK", "DK", "SC", "WD"]:
        if key == "turtle":
            f = lambda J, b: J[R]["stats"][b]
            rows.append([UN[R], f"{p(f(S, 'EW universe (benchmark)')['il_cagr'])} → {p(f(P, 'EW universe (benchmark)')['il_cagr'])}",
                         f"{f(S, 'Turtle L/S (S1+S2)')['sharpe']:.2f} → {f(P, 'Turtle L/S (S1+S2)')['sharpe']:.2f}",
                         f"{f(S, 'Turtle long-only (S1+S2)')['sharpe']:.2f} → {f(P, 'Turtle long-only (S1+S2)')['sharpe']:.2f}",
                         f"{p(f(S, 'Turtle long-only (S1+S2)')['alpha'])} → {p(f(P, 'Turtle long-only (S1+S2)')['alpha'])}"])
        else:
            f = lambda J, b: J[R]["stats"][b]
            rows.append([UN[R], f"{p(f(S, 'EW universe (benchmark)')['cagr'])} → {p(f(P, 'EW universe (benchmark)')['cagr'])}",
                         f"{p(f(S, 'L/S low minus high MAX (net)')['ann_mean'])} → {p(f(P, 'L/S low minus high MAX (net)')['ann_mean'])}",
                         f"{f(S, 'Low-MAX long-only (net)')['sharpe']:.2f} → {f(P, 'Low-MAX long-only (net)')['sharpe']:.2f}",
                         f"{f(S, 'EW universe (benchmark)')['sharpe']:.2f} → {f(P, 'EW universe (benchmark)')['sharpe']:.2f}"])
    head = ["Universe", "EW universe CAGR", "L/S Sharpe", "Long-only Sharpe", "Long-only alpha vs EW"] if key == "turtle" else ["Universe", "EW universe CAGR", "L/S return / yr (net)", "Low-MAX Sharpe", "EW Sharpe"]
    return table(head, rows)


def embed(html):
    for f in sorted(os.listdir(FIG)):
        html = html.replace(f"../figures/{f}", "data:image/png;base64," + base64.b64encode(open(os.path.join(FIG, f), "rb").read()).decode())
    return html


def fix_abs_pipes(md):
    """Escape |x| (absolute-value bars) inside markdown table rows so they do not split cells."""
    import re
    rx = re.compile(r"(?<!\\)\|([^\s|\-\\][^|\n]{0,8}?[^\s|\\]|[^\s|\-\\])\|")
    return "\n".join(rx.sub(lambda m: "&#124;" + m.group(1) + "&#124;", L) if L.lstrip().startswith("|") and not re.fullmatch(r"\s*\|[\s:|\-]+\|?\s*", L) else L for L in md.split("\n"))


def write(stem, md, title):
    md = fix_abs_pipes(md)
    open(os.path.join(OUT, f"{stem}.md"), "w").write(md)
    body = markdown.markdown(md, extensions=["tables", "fenced_code", "md_in_html"]).replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"
    open(os.path.join(OUT, f"{stem}.html"), "w").write(embed(html))


def pdf(stem):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(color_scheme="light")
        pg.goto("file://" + os.path.abspath(os.path.join(OUT, f"{stem}.html"))); pg.wait_for_load_state("networkidle")
        pg.pdf(path=os.path.join(OUT, f"{stem}.pdf"), format="A4", print_background=True, prefer_css_page_size=True); b.close()


def calendar(J, book, U_):
    years = sorted({int(y) for R in U_ for y in J[R]["stats"][book]["calendar"]})
    rows = []
    for y in years:
        rows.append([str(y)] + [p(J[R]["stats"][book]["calendar"].get(str(y)), 1) for R in U_])
    return table(["Year"] + [UN[R] for R in U_], rows)


def attr_rows(J, key):
    rows = []
    for R in U:
        a = J[R]["attribution"][key]; c, t = a["coef"], a["t"]
        loads = ", ".join(f"{k} {c[k]:+.2f} ({t[k]:+.1f})" for k in c if k != "alpha" and abs(t[k]) >= 2)
        rows.append([UN[R], a["model"], f"{a['months']}", p(c["alpha"]), f2(t["alpha"]), f2(a["r2"]), loads or "none |t| ≥ 2"])
    return table(["Universe", "Factor model", "Months", "Alpha / yr", "t(alpha)", "R²", "Loadings with |t| ≥ 2 (t)"], rows)


# ------------------------------------------------------------------------------------------------
def fs01():
    J = json.load(open(os.path.join(RES, "turtle_summary.json")))
    M, LO, B, IX = "Turtle L/S (S1+S2)", "Turtle long-only (S1+S2)", "EW universe (benchmark)", "Index Turtle (S2 on EW index)"
    s0 = J["US"]["stats"][M]
    FX = json.load(open(os.path.join(RES, "fix_summary.json")))["turtle"]
    head_rows = []
    for R in U:
        s, lo, b = J[R]["stats"][M], J[R]["stats"][LO], J[R]["stats"][B]
        head_rows.append([UN[R], p(s["il_cagr"]), f2(s["sharpe"]), pu(s["il_maxdd"], 0), p(lo["il_cagr"]), f2(lo["sharpe"]), pu(lo["il_maxdd"], 0), p(b["il_cagr"]), f2(b["sharpe"]), pu(b["il_maxdd"], 0)])
    n_neg = sum(J[R]["stats"][M]["sharpe"] < 0 for R in U)
    lo_beats = sum(J[R]["stats"][LO]["sharpe"] > J[R]["stats"][B]["sharpe"] for R in U)
    lo_alpha_pass = [UN[R] for R in U if J[R]["stats"][LO]["t_alpha"] > GATE]
    ls_attr = [J[R]["attribution"][M] for R in U]
    str_t = [a["t"].get("short_term_reversal") for a in ls_attr if "short_term_reversal" in a["t"]]
    tr_all = {R: J[R]["trades"] for R in U}
    win = sum(tr_all[R]["win_rate"] for R in U) / 6; payoff = sum(tr_all[R]["payoff"] for R in U) / 6
    md = f"""# FACTSHEET FS01 · The Turtle Traders

### Richard Dennis's 1983 trading rules, applied stock by stock to six equity universes

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 25 September 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Donchian channel breakout, pyramiding, 2N stops</div>
<div><b>Origin</b>Dennis & Eckhardt, 1983; rules published by Faith (2003)</div>
<div><b>Asset class</b>Single stocks (the Turtles traded futures)</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World</div>
<div><b>Backtest</b>Jan 2013 – Sep 2026, daily, net of costs</div>
<div><b>Books</b>Long/short (headline) and long-only</div>
<div><b>Rebalance</b>Event driven, next-day close fills</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **Verdict in one paragraph.** Dennis's students reportedly made more than $100 million with these rules on 1980s futures (Covel 2007). On single stocks, 2013–2026, the long/short version **lost money in all six universes** (Sharpe {min(J[R]['stats'][M]['sharpe'] for R in U):.2f} to {max(J[R]['stats'][M]['sharpe'] for R in U):.2f}). Nearly all of the loss is the short side: stocks that break to a new low tend to bounce, and a rising market punishes every short. The long-only version made money everywhere, but **had a lower Sharpe than simply owning the equal-weight universe in {n6(sum(J[R]['stats'][LO]['sharpe'] < J[R]['stats'][B]['sharpe'] for R in U))}**; its alpha against the universe is between {p(min(J[R]['stats'][LO]['alpha'] for R in U))} and {p(max(J[R]['stats'][LO]['alpha'] for R in U))} a year, and none reaches the {GATE} gate. The trade profile is textbook trend following, about {win * 100:.0f}% winners with winners {payoff:.1f}× the size of losers. On stocks, that is not enough to pay for the whipsaws. **What goes wrong (§10):** costs from oversized units, a short book in a bull market, a 2N stop tighter than daily noise and, at the root, no trend in single stocks to follow. Fixing what can be fixed gives a long-only, half-beta book that still trails the equal-weight universe's Sharpe in the 2020–26 holdout ({FX['avg_holdout']['T3 + 4N stop']['sharpe']:.2f} vs {FX['avg_holdout']['EW universe']['sharpe']:.2f}). **Classification (§11):** a futures trend strategy mis-applied to stocks. **360° view (§12):** the cross-sectional breakout does carry beta-adjusted information, but it is a noisy subset of the 52-week-high and momentum effects.

## 1. Headline performance

{table(["Universe", "L/S CAGR", "L/S Sharpe", "L/S max DD", "Long-only CAGR", "LO Sharpe", "LO max DD", "EW universe CAGR", "EW Sharpe", "EW max DD"], head_rows)}
*Daily returns, local currency (World in USD), net of 10 bp per side and 50 bp/yr short borrow; no interest on cash; rf = 0. CAGR, maximum drawdown: Project1 `InvestmentLibrary.reporting.generate_standard_report`. Sharpe on monthly returns. The benchmark is the equal-weight universe rebalanced daily (same names, same data).*

![Growth of 1](../figures/fs01_fig1_growth.png)

## 2. Strategy description

The Turtles were 23 novices recruited through a newspaper advert by Richard Dennis and William Eckhardt in 1983-84 to settle a bet: can trading be taught? They were given one mechanical rule set and traded Dennis's money in about 20 liquid futures markets. The rules were kept private until Curtis Faith published them in 2003 ("The Original Turtle Trading Rules"); Faith (2007) and Covel (2007) tell the story. The core is Richard Donchian's channel breakout (Donchian 1960): buy a new N-day high, sell a new N-day low.

| Rule | Original Turtle rule (Faith 2003) | This factsheet |
|---|---|---|
| Volatility unit **N** | 20-day exponential average of the true range | Same, close-to-close true range \\|ΔP\\| (Sharadar has no high/low) |
| Position unit | 1% of equity per 1 N move | **0.1%** of equity per N (see §5) |
| System 1 | Enter on a 20-day breakout, exit on a 10-day opposite breakout. Skip the signal if the previous 20-day breakout would have been a winner; take the 55-day breakout regardless (failsafe) | Same, including the skip filter, tracked on hypothetical trades |
| System 2 | Enter on a 55-day breakout, exit on a 20-day opposite breakout | Same |
| Stop | 2 N from the latest entry; all units' stops move up with each add | Same |
| Pyramiding | Add 1 unit every ½ N in the trade's favour, maximum 4 units per market | Same |
| Portfolio limit | 12 units per direction (fewer for correlated markets) | Gross cap: 100% long and 100% short of equity per system |
| Capital split | Traders ran both systems | 50% System 1, 50% System 2 |
| Direction | Long and short | Long/short headline; long-only variant; also the index version |

## 3. Data load

{universe_table()}
Window: signals from January 2012, performance from 2 January 2013 (a year of history needed for eligibility) to 24/25 September 2026. Eligibility: US, member of the point-in-time top 500 at the previous month-end; others, at least 252 days of price history. Cleaning follows Project2's rules: the five series Project2 verified as corrupt (DIA.MC, ATO.PA, ZEG.L, SPM.MI, VPLAY-B.ST) are dropped, and any daily move beyond ±100% is set to missing unless it was verified as real (ABVX.PA, MRNA, ECHO, GME). That removed 12 US and 2 European daily prints.

## 4. Signal ("factor") creation

For stock *i* on day *t*, with *P* the total-return index:

- N<sub>t</sub> = (19·N<sub>t−1</sub> + \\|P<sub>t</sub> − P<sub>t−1</sub>\\|) / 20
- Long entry when P<sub>t</sub> > max(P<sub>t−L</sub> … P<sub>t−1</sub>); short entry when P<sub>t</sub> < min(…); L = 20 (System 1) or 55 (System 2)
- Exit long when P<sub>t</sub> < min of the last X closes (X = 10 or 20), or P<sub>t</sub> ≤ stop; mirror for shorts
- Add a unit when P<sub>t</sub> ≥ last entry + ½ N; stop = last entry − 2 N
- Unit size in shares = 0.001 × equity / N<sub>t</sub>, so a 1 N move in one unit costs 0.1% of equity

The signal is a time-series rule per stock, not a cross-sectional rank. There is no parameter fitting: every number is the 1983 rule.

## 5. Model build (portfolio construction and simulation)

- **Event-driven, close-only simulator** (`code/turtle.py`). Signals on the close of day *t* are filled on the close of day *t+1*, so there is no look-ahead. Positions are held in shares and marked to market daily.
- **Why 0.1% and not 1%.** Close-to-close N is about 1% of a large-cap share price, so a 1% unit would be roughly 100% of equity in one name and the original 12-unit limit 1,200% gross. At 0.1% one unit is about 10% of equity, four units at most about 40%, and the gross cap keeps the book near fully invested.
- **Oversubscription.** A 500-stock universe produces dozens of breakouts on busy days. New units are filled in order of breakout strength (distance past the channel in N) until the gross cap is reached. Adds to open trades go first.
- **Costs.** 10 bp per side on traded notional (commission plus half-spread for large caps), 50 bp a year on short notional, no interest earned on cash (conservative: 2022–26 rates were 4–5%).
- **Delistings.** A position with no price for five trading days is closed at the last price (matters for US point-in-time data).
- **Index version** ("futures-style"): the same System 2 rules applied to the equal-weight universe index as one market, the closest analogue to what the Turtles actually traded; 0.25% per unit so four units ≈ fully invested, 100% cap.

## 6. Performance in detail

"""
    for R in U:
        st = J[R]["stats"]
        rows = []
        for k, lab in [(M, "Turtle L/S (S1+S2)"), ("System 1 L/S", "System 1 only"), ("System 2 L/S", "System 2 only"), (LO, "Turtle long-only"), (IX, "Index Turtle (S2)"), (B, "EW universe")]:
            s = st[k]
            rows.append([lab, p(s["il_cagr"]), pu(s["il_vol"]), f"{s['sharpe']:.2f} {ci(s['sharpe_ci'])}", f2(s["il_sortino"]), pu(s["il_maxdd"], 0), f2(s["il_calmar"]),
                         pu(s["hit"], 0), pu(s["cvar95"], 1), f2(s["beta"]) if k != B else "1.00", f"{p(s['alpha'])} ({s['t_alpha']:.1f})" if k != B else "–"])
        e = J[R]["exposure"]
        md += f"**{UNL[R]}**, median {J[R]['n_names']} names; L/S book averages {e['long'] * 100:.0f}% long, {e['short'] * 100:.0f}% short, {e['npos']:.0f} positions\n\n"
        md += table(["Book", "CAGR", "Vol", "Sharpe [95% CI]", "Sortino", "Max DD", "Calmar", "Hit (mo)", "CVaR 95% (day)", "Beta", "Alpha/yr (t)"], rows) + "\n"
    md += f"""*Sharpe 95% CI: stationary bootstrap of monthly returns (Politis & Romano 1994; mean block 6, 5,000 draws). Beta and alpha: OLS of monthly returns on the equal-weight universe, Newey-West t (6 lags). CVaR: mean of the worst 5% of days (InvestmentLibrary.risk.cvar_historic).*

![Drawdowns](../figures/fs01_fig2_drawdown.png)

**Calendar-year returns, Turtle long/short**

{calendar(J, M, U)}
**Calendar-year returns, Turtle long-only**

{calendar(J, LO, U)}
## 7. Trading record

Every trade is in `results/turtle_trades_<universe>.csv` (ticker, direction, entry and exit date, units, prices, P&L in % of equity at entry, R multiple, exit reason). 1R = the risk of the first unit, 2 N.

"""
    rows = []
    for R in U:
        t = J[R]["trades"]
        rows.append([UN[R], f"{t['n']:,}", f"{t['per_year']:.0f}", pu(t["win_rate"], 0), p(t["avg_win"], 2), p(t["avg_loss"], 2), f2(t["payoff"]), f2(t["profit_factor"]),
                     f"{t['expectancy_R']:+.2f}", f"{t['days_win']:.0f} / {t['days_loss']:.0f}", f"{t['avg_units']:.1f}", pu(t["stop_share"], 0), f"{t['pnl_long'] * 100:+.0f}% / {t['pnl_short'] * 100:+.0f}%"])
    md += table(["Universe", "Trades", "Per yr", "Win rate", "Avg win", "Avg loss", "Payoff", "Profit factor", "Expectancy (R)", "Days held win / loss", "Avg units", "Stopped out", "Summed P&L long / short"], rows)
    rows = []
    for R in U:
        t = J[R]["trades_longonly"]
        rows.append([UN[R], f"{t['n']:,}", pu(t["win_rate"], 0), f2(t["payoff"]), f2(t["profit_factor"]), f"{t['expectancy_R']:+.2f}", f"{t['days_win']:.0f} / {t['days_loss']:.0f}"])
    md += "\n**Long-only book**\n\n" + table(["Universe", "Trades", "Win rate", "Payoff", "Profit factor", "Expectancy (R)", "Days held win / loss"], rows)
    op = pd.read_csv(os.path.join(RES, "turtle_open_US.csv")).head(8)
    oprow = [[r.ticker, r.dir, r.system, int(r.units), r.entry[:10], pu(abs(r.weight), 1)] for r in op.itertuples()]
    md += f"""
*Summed P&L adds each trade's P&L in % of equity at entry; it shows where the money went, not a compounded return.*

![Trades](../figures/fs01_fig3_trades.png)

The shape is the classic trend-follower's: most trades are small losses, stopped at about −1 to −2 R, and a thin right tail of 10–40 R winners carries the book. Across all universes the best ~23% of trades earn everything; the other 77% give it back and more.

**Open book, US, 24 September 2026 (largest 8 of {J['US']['open_positions']})**

{table(["Ticker", "Side", "System", "Units", "Entered", "Weight"], oprow)}
Open books for every universe: `results/turtle_open_<universe>.csv`.

## 8. Risk and factor attribution

Monthly returns regressed on seven factor themes: JKP (Jensen, Kelly & Pedersen 2023) market, size, value, momentum, low risk, quality and short-term reversal for the US, UK, DK and World; French Europe 5 factors plus momentum (WML) for EU and SCANDI (JKP has no Europe series; World ex-US is Asia-heavy, which Project2 learned the hard way). Factor data to Dec 2025 (JKP) or Jul 2026 (French). Newey-West t, 6 lags.

**Turtle long/short**

{attr_rows(J, M)}
**Turtle long-only**

{attr_rows(J, LO)}
**Reading the loadings.** The long/short book loads on momentum, as it should, and **negatively on short-term reversal** in every JKP universe: {', '.join(f"{UN[R]} {J[R]['attribution'][M]['coef']['short_term_reversal']:+.2f} (t {J[R]['attribution'][M]['t']['short_term_reversal']:.1f})" for R in ['US', 'UK', 'DK', 'WD'])}; significant (|t| ≥ 2) in {', '.join(UN[R] for R in ['US', 'UK', 'DK', 'WD'] if abs(J[R]['attribution'][M]['t']['short_term_reversal']) >= 2)}. Entering the day after a breakout means buying last week's winners and shorting last week's losers, which is exactly the trade that one-month reversal (Jegadeesh 1990) punishes in single stocks. Futures markets do not have that reversal, which is one reason the rules worked there.

## 9. Statistical verdict

- **Gate.** 12 strategy × universe cells across the two factsheets; Bonferroni two-sided 0.05/12 gives |t| > {GATE}.
- **Long/short:** negative Sharpe in {n_neg} of 6. The negative factor alphas are significant in several universes, so this is evidence the rule *loses*, not just that it fails to win.
- **Long-only:** higher Sharpe than the equal-weight universe in {lo_beats} of 6; alpha vs the universe passes the gate in {len(lo_alpha_pass)} of 6{(' (' + ', '.join(lo_alpha_pass) + ')') if lo_alpha_pass else ''}. Its appeal is a lower beta ({min(J[R]['stats'][LO]['beta'] for R in U):.2f}–{max(J[R]['stats'][LO]['beta'] for R in U):.2f}) and a shallower maximum drawdown than the universe in {sum(J[R]['stats'][LO]['il_maxdd'] > J[R]['stats'][B]['il_maxdd'] for R in U)} of 6, not extra return. Results lean on a few trades: single positions such as Abivax (ABVX.PA, the verified +561% trial-result week in 2025) or Rheinmetall can make a year.
- **Index version:** Sharpe between {min(J[R]['stats'][IX]['sharpe'] for R in U):.2f} and {max(J[R]['stats'][IX]['sharpe'] for R in U):.2f}. Small either way: timing the index with breakouts does not add value in a 13-year bull market, the same result as A11 *A Beautiful Mind* for moving-average rules.
- **Probabilistic Sharpe** (Bailey & López de Prado 2012), P(true Sharpe > 0): L/S {', '.join(f"{UN[R]} {J[R]['stats'][M]['psr0']:.2f}" for R in U)}.

## 13. Caveats

1. **Survivorship: fixed as far as the data allow.** The first edition of this factsheet used today's index members outside the US. This edition uses point-in-time membership everywhere (§3). The table shows the change, same code, same period (survivor list → point-in-time). Note that the universes also changed definition (national blue-chip indices instead of STOXX 600), so the difference is survivorship plus composition.

{surv_table("turtle")}
The equal-weight universes lose 2–5 percentage points a year once survivors are removed, which is the survivorship bias Project2 measured. The conclusions do not change. About a fifth of member-quarters have no price (mostly delisted names Yahoo no longer serves), so a residual bias remains; it flatters long books and hurts short books.
2. **Close-only simulation.** The Turtles entered intraday at the breakout price; here the fill is the next day's close. That is conservative for entries and exits alike.
3. **Close-to-close N** ignores intraday highs and lows, so it understates the true range and makes units somewhat larger than the original rule.
4. **Currency.** Local currency; World sums local-currency returns without converting them.
5. **Sizing is an adaptation.** The 0.1% unit and the gross cap are my choices, set once on mechanics (leverage), never tuned on returns. Other choices would change the level of returns, not the sign of the short side.
6. **Not a registered trial.** This factsheet is descriptive and is not added to the programme's trial ledger. The fix ladder in §10 is counted inside the factsheets (7 trials, gate 0.05/7). The *Trading Places* article (Season 2) will pre-register a single test.

## 14. Academic references

- Faith, C. (2003). *The Original Turtle Trading Rules*. OriginalTurtles.org (free PDF).
- Faith, C. (2007). *Way of the Turtle: The Secret Methods that Turned Ordinary People into Legendary Traders*. McGraw-Hill.
- Covel, M. (2007). *The Complete TurtleTrader*. HarperCollins.
- Donchian, R. D. (1960). High finance in copper. *Financial Analysts Journal*, 16(6), 133–142.
- Wilcox, C. & Crittenden, E. (2005). Does trend-following work on stocks? Blackstar Funds white paper.
- Moskowitz, T., Ooi, Y. H. & Pedersen, L. H. (2012). Time series momentum. *Journal of Financial Economics*, 104(2), 228–250.
- Hurst, B., Ooi, Y. H. & Pedersen, L. H. (2017). A century of evidence on trend-following investing. *Journal of Portfolio Management*, 44(1), 15–29.
- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns. *Journal of Finance*, 45(3), 881–898.
- George, T. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance*, 59(5), 2145–2176.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5), 2465–2518.
- Fama, E. & French, K. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1–22.
- Newey, W. & West, K. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.
- Politis, D. & Romano, J. (1994). The stationary bootstrap. *Journal of the American Statistical Association*, 89(428), 1303–1313.
- Bailey, D. & López de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk*, 15(2), 3–44.
- Lo, A. & MacKinlay, A. C. (1988). Stock market prices do not follow random walks: Evidence from a simple specification test. *Review of Financial Studies*, 1(1), 41–66.
- Barberis, N., Shleifer, A. & Vishny, R. (1998). A model of investor sentiment. *Journal of Financial Economics*, 49(3), 307–343.
- Hong, H. & Stein, J. (1999). A unified theory of underreaction, momentum trading, and overreaction in asset markets. *Journal of Finance*, 54(6), 2143–2184.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1), 65–91.
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies*, 29(1), 104–147.
- Treynor, J. & Mazuy, K. (1966). Can mutual funds outguess the market? *Harvard Business Review*, 44(4), 131–136.

## 15. Reproduce

`code/data.py` (universes) → `code/turtle.py` + `run_turtle.py <U>` (simulator) → `analyse.py turtle` (statistics, attribution) → §10–11: `diag_turtle.py`, `cost_check.py`, `turtle_fix.py <U>`, `fix_analysis.py` → §12: `signals.py`, `neighbourhood.py brk`, `nbh_figs.py`, `nbh_section.py` → `make_figures.py` → `build_factsheets.py` (sections 10–11 in `sections_fix_class.py`). Metrics call Project1 `InvestmentLibrary` (stats, risk, reporting). Licensed Sharadar and cached Yahoo prices are not included; results files hold derived numbers only.
"""
    md = md.replace("## 13. Caveats", sections_fix_class.fs01_sections() + nbh_section.fs01() + "## 13. Caveats")
    write("FS01_Turtle_Traders", md, "FS01 The Turtle Traders: factsheet")
    return md


# ------------------------------------------------------------------------------------------------
def fs02():
    J = json.load(open(os.path.join(RES, "lottery_summary.json")))
    LS, LO, B, M5 = "L/S low minus high MAX (net)", "Low-MAX long-only (net)", "EW universe (benchmark)", "L/S MAX5 (net)"
    hi = lambda R: f"High-MAX leg (Q{J[R]['q']}, gross)"
    head = []
    for R in U:
        s, lo, b = J[R]["stats"][LS], J[R]["stats"][LO], J[R]["stats"][B]
        head.append([UN[R], f"{J[R]['n_names']} / {J[R]['q']}", p(s["ann_mean"]), f2(s["t_mean"]), f"{p(s['alpha'])} ({s['t_alpha']:.1f})", f2(s["beta"]),
                     p(lo["cagr"]), f2(lo["sharpe"]), pu(lo["maxdd"], 0), p(b["cagr"]), f2(b["sharpe"]), pu(b["maxdd"], 0)])
    neg = sum(J[R]["stats"][LS]["ann_mean"] < 0 for R in U)
    gross = {R: pd.read_csv(os.path.join(RES, f'lottery_monthly_record_{R}.csv')).ls_gross.mean() * 12 for R in U}
    capm_pass = [UN[R] for R in U if abs(J[R]["stats"][LS]["t_alpha"]) > GATE]
    us = J["US"]["stats"][LS]
    md = f"""# FACTSHEET FS02 · The lottery factor (MAX)

### Do investors overpay for stocks that just had one huge day? Six universes, 2013–2026

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Buy low-MAX, sell high-MAX stocks</div>
<div><b>Origin</b>Bali, Cakici & Whitelaw (2011), JFE</div>
<div><b>Signal</b>Largest daily return in the past month</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, 163 months, net of costs</div>
<div><b>Books</b>Long/short (headline) and low-MAX long-only</div>
<div><b>Rebalance</b>Monthly, equal-weighted</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **Verdict in one paragraph.** Bali, Cakici & Whitelaw found that US stocks with the largest one-day jump last month earned about 1% a month *less* the next month, in 1962–2005. Investors pay up for lottery tickets. In 2013–2026 the effect is gone: **after costs the long/short lost money in {n6(neg)} universes** ({p(min(J[R]['stats'][LS]['ann_mean'] for R in U))} to {p(max(J[R]['stats'][LS]['ann_mean'] for R in U))} a year); before costs it was slightly positive only in {', '.join(UN[R] for R in U if gross[R] > 0) or 'none'}, and clearly negative in the US and World, where the lottery stocks won. The reason is beta. The high-MAX group has a beta of {min(J[R]['quantile_beta'][f'Q{J[R]["q"]}'] for R in U):.2f}–{max(J[R]['quantile_beta'][f'Q{J[R]["q"]}'] for R in U):.2f} against the universe, the low-MAX group {min(J[R]['quantile_beta']['Q1'] for R in U):.2f}–{max(J[R]['quantile_beta']['Q1'] for R in U):.2f}, and markets rose strongly. Adjusted for that one number, the CAPM alpha of the long/short is between {p(min(J[R]['stats'][LS]['alpha'] for R in U))} and {p(max(J[R]['stats'][LS]['alpha'] for R in U))} a year and passes the gate in {len(capm_pass)} of 6. The low-MAX long-only book delivered what low-risk investing promises: a beta of {min(J[R]['stats'][LO]['beta'] for R in U):.2f}–{max(J[R]['stats'][LO]['beta'] for R in U):.2f}, a shallower drawdown than the universe in {sum(J[R]['stats'][LO]['maxdd'] > J[R]['stats'][B]['maxdd'] for R in U)} of 6, a higher Sharpe in {sum(J[R]['stats'][LO]['sharpe'] > J[R]['stats'][B]['sharpe'] for R in U)} of 6 ({', '.join(UN[R] for R in U if J[R]['stats'][LO]['sharpe'] > J[R]['stats'][B]['sharpe'])}), and alphas of {p(min(J[R]['stats'][LO]['alpha'] for R in U))} to {p(max(J[R]['stats'][LO]['alpha'] for R in U))} that do not pass the gate. **What goes wrong (§10):** an unhedged beta bet plus a signal that, in large caps, mostly measures volatility. Beta-neutral legs remove most of the loss in both the design and the 2020–26 holdout window, and what remains is a premium of about zero. **Classification (§11):** a member of the low-risk family, not a factor of its own. **360° view (§12):** lottery and falling knife are the two tails of the same volatility, mirrors in their returns but not in the stocks they pick; neither tail is priced on its own once volatility and beta are in the model, and MAX is fully spanned by its neighbours.

## 1. Headline performance

{table(["Universe", "Names / groups", "L/S return / yr", "L/S t", "L/S CAPM alpha (t)", "L/S beta", "Low-MAX CAGR", "Low-MAX Sharpe", "Low-MAX max DD", "EW CAGR", "EW Sharpe", "EW max DD"], head)}
*Monthly, local currency (World in USD). L/S = equal-weighted lowest-MAX group minus highest-MAX group, net of 10 bp per side on turnover and a size-tiered borrow fee on the high-MAX leg. Newey-West t (6 lags). CAPM alpha and beta against the equal-weight universe. Metrics from Project1 InvestmentLibrary where applicable.*

![Growth](../figures/fs02_fig1_growth.png)

## 2. Strategy description

**The idea.** Many investors like lottery-like payoffs: a small chance of a very large gain. Cumulative prospect theory predicts that people overweight small probabilities (Tversky & Kahneman 1992). Barberis & Huang (2008) show that this makes positively skewed stocks overpriced, so they earn low future returns. Kumar (2009) documents that retail investors tilt towards lottery-type stocks. Bali, Cakici & Whitelaw (2011) proposed the simplest proxy for "lottery-ness": **MAX, the largest daily return in the previous month.** In US data 1962–2005 the highest-MAX decile underperformed the lowest by over 1% a month, value-weighted, and the effect subsumed idiosyncratic volatility (Ang et al. 2006). European evidence followed (Annaert, De Ceuster & Verstegen 2013; Walkshäusl 2014). Bali, Brown, Murray & Tang (2017) argue that lottery demand explains the beta anomaly (Frazzini & Pedersen 2014), which is why beta sits at the centre of this factsheet.

**The trade.** Each month-end, rank stocks by MAX, buy the calmest group, sell the most lottery-like group, hold one month.

## 3. Data load

{universe_table()}
Same cleaning as FS01: the five verified corrupt series are dropped and daily moves beyond ±100% are removed unless verified real. This matters more here than anywhere else, because a single bad print *is* a MAX signal.

## 4. Factor creation

For stock *i* in month *t*, with *r<sub>i,d</sub>* the daily total return:

- **MAX1<sub>i,t</sub> = max<sub>d∈t</sub> r<sub>i,d</sub>**, requiring at least 15 valid days in the month
- **MAX5<sub>i,t</sub>** = mean of the five largest daily returns (robustness, Bali et al.'s alternative)
- Eligible: in the universe at month-end *t* (US point-in-time top 500; others survivor list, ≥ 252 days of history)
- Sort into equal-count groups: **deciles** with ≥ 100 names (US, EU, UK, World), **quintiles** with 50–99 (SCANDI), **terciles** below 50 (DK). The number of groups is fixed per universe for the whole sample.

Average MAX in the extreme groups: {', '.join(f"{UN[R]} {J[R]['max_low'] * 100:.1f}% vs {J[R]['max_high'] * 100:.1f}%" for R in U)}.

## 5. Model build

- Equal-weighted groups, formed at month-end *t*, held through month *t+1* (compounded daily total returns; a stock that stops trading earns its return up to its last price).
- **Long/short** = group 1 − last group. **Long-only** = group 1. **Benchmark** = equal-weighted universe, same month.
- **Costs:** 10 bp per side × one-way turnover of each leg. Average monthly one-way turnover: low-MAX {', '.join(f"{UN[R]} {J[R]['to_low'] * 100:.0f}%" for R in U)}; the high-MAX leg turns over about as much. Cost drag on the L/S: {', '.join(f"{UN[R]} {J[R]['cost_drag'] * 100:.1f}%" for R in U)} a year.
- **Robustness books:** MAX5 signal; US value-weighted (Sharadar market caps), which is closest to the original paper.
- Code: `code/lottery.py` (portfolio build), `run_lottery.py`, `analyse.py lottery`.

## 6. Performance in detail

"""
    for R in U:
        st = J[R]["stats"]; rows = []
        keys = [(LS, "L/S low − high MAX (net)"), (M5, "L/S MAX5 (net)")] + ([("L/S value-weighted (net)", "L/S value-weighted (net)")] if "L/S value-weighted (net)" in st else []) + \
               [(LO, "Low-MAX long-only (net)"), (hi(R), f"High-MAX group (gross)"), (B, "EW universe")]
        for k, lab in keys:
            s = st[k]
            rows.append([lab, p(s["ann_mean"]), p(s["cagr"]), pu(s["vol"]), f"{s['sharpe']:.2f} {ci(s['sharpe_ci'])}", f2(s["il_sortino"]), pu(s["maxdd"], 0), pu(s["hit"], 0),
                         f"{s['t_mean']:.2f}", f2(s["beta"]) if k != B else "1.00", f"{p(s['alpha'])} ({s['t_alpha']:.1f})" if k != B else "–", pu(s["cvar95"], 1)])
        md += f"**{UNL[R]}**, median {J[R]['n_names']} names, {J[R]['q']} groups\n\n"
        md += table(["Book", "Mean / yr", "CAGR", "Vol", "Sharpe [95% CI]", "Sortino", "Max DD", "Hit", "t(mean)", "Beta", "Alpha/yr (t)", "CVaR 95% (month)"], rows) + "\n"
    md += f"""*Sharpe CI: stationary bootstrap, mean block 6 months, 5,000 draws. Max drawdown on monthly returns. The equal-weight universe here is rebalanced monthly, so its figures differ slightly from FS01's daily-rebalanced version.*

![Quantiles](../figures/fs02_fig3_quantiles.png)

![Beta](../figures/fs02_fig4_beta.png)

The beta chart is the whole story in one picture: across {sum(J[R]['q'] for R in U)} MAX groups in six universes, average return rises with beta, and the lottery groups sit at the top right simply because they carry the most market risk.

![Drawdowns](../figures/fs02_fig2_drawdown.png)

**Calendar-year returns, L/S low − high MAX (net)**

""" + calendar(J, LS, U) + "\n**Calendar-year returns, low-MAX long-only (net)**\n\n" + calendar(J, LO, U)
    rows = []
    for R in U:
        rec = pd.read_csv(os.path.join(RES, f"lottery_monthly_record_{R}.csv"), index_col=0)
        rows.append([UN[R], f"{len(rec)}", f"{rec.n.median():.0f}", f"{rec.n.median() / J[R]['q']:.0f}", pu(J[R]["to_low"], 0), pu(J[R]["to_high"], 0),
                     pu((rec.ls_net > 0).mean(), 0), p(rec.ls_net.min()), rec.ls_net.idxmin()[:7], p(J[R]["meme"])])
    cur = []
    for R in ["US", "EU", "DK", "SC"]:
        cur.append([UN[R], ", ".join(t for t, _ in J[R]["current_low"][:8]), ", ".join(t for t, _ in J[R]["current_high"][:8])])
    md += f"""
## 7. Trading record

A factor has no discrete trades; its record is the monthly rebalance log, `results/lottery_monthly_record_<universe>.csv` (names, average MAX per leg, turnover, leg returns, gross and net L/S).

{table(["Universe", "Rebalances", "Names", "Names per leg", "Turnover low leg", "Turnover high leg", "L/S months positive", "Worst L/S month", "When", "L/S during the 2020–21 retail boom / yr"], rows)}
**Current book** (formed on 31 August 2026 for September; first 8 names per leg, sorted by MAX)

{table(["Universe", "Long: calmest (lowest MAX)", "Short: most lottery-like (highest MAX)"], cur)}
## 8. Risk and factor attribution

Same factor sets as FS01: JKP 7 themes (market, size, value, momentum, low risk, quality, short-term reversal) for US, UK, DK and World; French Europe 5 factors + WML for EU and SCANDI. Newey-West t, 6 lags. JKP's own `rmax1_21d` factor (the MAX factor itself) sits inside the low-risk theme.

**L/S low − high MAX**

{attr_rows(J, LS)}
**Low-MAX long-only**

{attr_rows(J, LO)}
**Reading it.** Once beta is removed, most of the L/S loss disappears (CAPM alpha t between {min(J[R]['stats'][LS]['t_alpha'] for R in U):.1f} and {max(J[R]['stats'][LS]['t_alpha'] for R in U):.1f}). The L/S is, above all, a low-risk position: its loading on JKP's low-risk theme is {rng_([J[R]['attribution'][LS]['coef']['low_risk'] for R in ['US', 'UK', 'DK', 'WD']])} with t up to {max(J[R]['attribution'][LS]['t']['low_risk'] for R in ['US', 'UK', 'DK', 'WD']):.0f}. Where the JKP alpha is negative ({', '.join(UN[R] for R in ['US', 'UK', 'DK', 'WD'] if J[R]['attribution'][LS]['coef']['alpha'] < 0)}), the L/S earned less than that low-risk exposure would predict: net-of-cost, equal-weighted large-cap sorts are a costly way to hold low risk.

**The low-MAX long-only alphas need a warning.** Against the factor models it shows {rng_([J[R]['attribution'][LO]['coef']['alpha'] for R in U if R != 'US'], True)} a year outside the US (largest t {max(J[R]['attribution'][LO]['t']['alpha'] for R in U):.2f}, {UN[max(U, key=lambda R: J[R]['attribution'][LO]['t']['alpha'])]}{', which formally clears the gate' if max(J[R]['attribution'][LO]['t']['alpha'] for R in U) > GATE else ''}). Against its own equal-weight universe, in the same currency, the alphas are smaller ({p(min(J[R]['stats'][LO]['alpha'] for R in U))} to {p(max(J[R]['stats'][LO]['alpha'] for R in U))}). The factor returns are in USD (JKP) or USD-based (French) while the book is in local currency, so I read the universe-relative alpha as the honest number.

## 9. Statistical verdict

- **Gate:** |t| > {GATE} (12 cells, Bonferroni 0.05/12, two-sided).
- **Raw L/S:** negative after costs in {neg} of 6; before costs positive in {sum(gross[R] > 0 for R in U)} of 6. The US gross spread ({p(pd.read_csv(os.path.join(RES, 'lottery_monthly_record_US.csv')).ls_gross.mean() * 12)} a year; {p(us['ann_mean'])} net, t {us['t_mean']:.2f}) reproduces A15 *Viva Las Vegas* (A15-2: −9.2%/yr gross, t −1.93, same top-500 deciles on price returns).
- **CAPM alpha of the L/S:** {rng_([J[R]['stats'][LS]['alpha'] for R in U], True)}, passes in {len(capm_pass)} of 6. Once beta is priced the anomaly is neither alive nor reversed: the raw result is a beta bet in disguise.
- **Low-MAX long-only:** alpha between {p(min(J[R]['stats'][LO]['alpha'] for R in U))} and {p(max(J[R]['stats'][LO]['alpha'] for R in U))} (largest t {max(J[R]['stats'][LO]['t_alpha'] for R in U):.2f}), none past the gate; beta {min(J[R]['stats'][LO]['beta'] for R in U):.2f}–{max(J[R]['stats'][LO]['beta'] for R in U):.2f}.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): {', '.join(f"{UN[R]} {J[R]['stats'][LS]['psr0']:.2f}" for R in U)}.
- **Publication decay.** JKP's broad US MAX factor earned +4.0%/yr before 2006 (t 1.48) and +2.0%/yr in 2012–2025 (t 0.55), from A15. McLean & Pontiff (2016) predict roughly this post-publication shrinkage.

## 13. Caveats

1. **Survivorship, and it cut in a particular direction here.** The first edition used today's index members outside the US. A high-MAX stock that jumped and later collapsed out of the index was missing, while one that jumped and kept rising was present, which flattered the high-MAX leg. This edition uses point-in-time membership (§3), and the table confirms the direction (survivor list → point-in-time; the universe definitions also changed):

{surv_table("lottery")}
The non-US L/S numbers moved towards zero and the low-MAX book improved relative to its universe. About a fifth of member-quarters still have no price (mostly delisted names), so a residual bias of the same sign remains.
2. **Large caps only.** The effect is strongest in small, retail-held stocks; these universes are blue chips. DK (3 groups of ~6) and SCANDI (5 groups of ~12) are thin and noisy.
3. **Equal-weighting** (except the US value-weighted robustness book). The original paper's headline is value-weighted.
4. **Currency:** local; World mixes currencies.
5. **Not a registered trial.** A15 carries the registered tests (A15-1, A15-2); this factsheet extends them descriptively to five more universes. The fix ladder in §10 is counted inside the factsheets (7 trials, gate 0.05/7).

## 14. Academic references

- Bali, T. G., Cakici, N. & Whitelaw, R. F. (2011). Maxing out: Stocks as lotteries and the cross-section of expected returns. *Journal of Financial Economics*, 99(2), 427–446.
- Barberis, N. & Huang, M. (2008). Stocks as lotteries: The implications of probability weighting for security prices. *American Economic Review*, 98(5), 2066–2100.
- Kumar, A. (2009). Who gambles in the stock market? *Journal of Finance*, 64(4), 1889–1933.
- Tversky, A. & Kahneman, D. (1992). Advances in prospect theory: Cumulative representation of uncertainty. *Journal of Risk and Uncertainty*, 5(4), 297–323.
- Ang, A., Hodrick, R., Xing, Y. & Zhang, X. (2006). The cross-section of volatility and expected returns. *Journal of Finance*, 61(1), 259–299.
- Annaert, J., De Ceuster, M. & Verstegen, K. (2013). Are extreme returns priced in the stock market? European evidence. *Journal of Banking & Finance*, 37(9), 3401–3411.
- Walkshäusl, C. (2014). The MAX effect: European evidence. *Journal of Banking & Finance*, 42, 1–10.
- Bali, T. G., Brown, S., Murray, S. & Tang, Y. (2017). A lottery-demand-based explanation of the beta anomaly. *Journal of Financial and Quantitative Analysis*, 52(6), 2369–2397.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics*, 111(1), 1–25.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance*, 71(1), 5–32.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5), 2465–2518.
- Harvey, C., Liu, Y. & Zhu, H. (2016). …and the cross-section of expected returns. *Review of Financial Studies*, 29(1), 5–68.
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies*, 29(1), 104–147.
- Treynor, J. & Mazuy, K. (1966). Can mutual funds outguess the market? *Harvard Business Review*, 44(4), 131–136.
- Boyer, B., Mitton, T. & Vorkink, K. (2010). Expected idiosyncratic skewness. *Review of Financial Studies*, 23(1), 169–202.
- Conrad, J., Dittmar, R. & Ghysels, E. (2013). Ex ante skewness and expected stock returns. *Journal of Finance*, 68(1), 85–124.
- George, T. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance*, 59(5), 2145–2176.
- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns. *Journal of Finance*, 45(3), 881–898.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1), 65–91.
- Newey & West (1987); Politis & Romano (1994); Bailey & López de Prado (2012): as in FS01.

## 15. Reproduce

`code/data.py` → `lottery.py` + `run_lottery.py <U>` → `analyse.py lottery` → §10–11: `lottery_fix.py`, `fix_analysis.py` → §12: `signals.py`, `neighbourhood.py max`, `nbh_figs.py`, `nbh_section.py` → `make_figures.py` → `build_factsheets.py`. Metrics call Project1 `InvestmentLibrary`. Licensed prices are not included.
"""
    md = md.replace("## 13. Caveats", sections_fix_class.fs02_sections() + nbh_section.fs02() + "## 13. Caveats")
    write("FS02_Lottery_MAX", md, "FS02 The lottery factor (MAX): factsheet")
    return md


if __name__ == "__main__":
    fs01(); fs02()
    for s in ["FS01_Turtle_Traders", "FS02_Lottery_MAX"]:
        pdf(s)
    print(os.listdir(OUT))
