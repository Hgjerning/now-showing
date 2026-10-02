# -*- coding: utf-8 -*-
"""Factsheet layout v2 (Factsheet Content Review, 2 Oct 2026): verdict box and scorecard, Sharpe anatomy, how the strategy
fits next to the others, a three-panel chart, and an appendix for the per-universe detail. No new trials: every number
comes from results/ (xs_<code>.json, trial_ledger.csv, results_us1999/) and cockpit/cockpit_data.json."""
import json, os, re
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); RES = os.path.join(ROOT, "results"); FIG = os.path.join(ROOT, "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
GATE, PROG = 2.87, None
CK = json.load(open(os.path.join(ROOT, "cockpit", "cockpit_data.json"), encoding="utf-8"))
COLORS = {"US": "#2a78d6", "EU": "#eb6834", "UK": "#2c7a4b", "DK": "#b0373a", "SC": "#8a6bbf", "WD": "#52514e"}
p = lambda x, d=1: "n/a" if x is None or x != x else f"{x * 100:+.{d}f}%"
pu = lambda x, d=1: "n/a" if x is None or x != x else f"{x * 100:.{d}f}%"
f2 = lambda x: "n/a" if x is None or x != x else f"{x:+.2f}"
LAYOUT_NOTE = "*Layout revised 2 October 2026 (verdict and scorecard, Sharpe anatomy, fit with the other strategies; detail moved to the appendix). No number changed.*"


def table(h, rows):
    return "| " + " | ".join(h) + " |\n|" + "|".join(["---"] * len(h)) + "|\n" + "".join("| " + " | ".join(str(x) for x in r) + " |\n" for r in rows)


def ser(code, R, leg):
    d = CK["strat"].get(code, {}).get(R, {}).get(leg)
    return pd.Series(d, dtype=float).sort_index() if d else None


def mkt(R):
    return pd.Series(CK["mkt"][R], dtype=float).sort_index()


def mark(t):
    return f"{t:+.2f} ✔" if t > GATE else (f"{t:+.2f} ✖ (neg.)" if t < -GATE else f"{t:+.2f}")


def prog_bar():
    j = json.load(open(os.path.join(RES, "trial_ledger.json"))); return j["n"], j["z_bonf"]


# ---------------- 1. verdict and scorecard
def verdict_scorecard(code, per):
    LS, LO, EW = "L/S (net)", "Long-only (net)", "EW universe"
    st = lambda R, b: per[R]["stats"][b]
    n, zb = prog_bar()
    led = pd.read_csv(os.path.join(RES, "trial_ledger.csv")); led = led[(led.fs == code) & (led.kind == "primary")]
    prog = led[led.t.abs() > zb]
    ls_p = [UN[R] for R in U if st(R, LS)["t_mean"] > GATE]; ls_n = [UN[R] for R in U if st(R, LS)["t_mean"] < -GATE]
    lo_p = [UN[R] for R in U if st(R, LO)["t_alpha"] > GATE]; lo_n = [UN[R] for R in U if st(R, LO)["t_alpha"] < -GATE]
    u99 = None
    for f in ("t1_xs", "t1_turtle", "t1_lottery"):
        fp = os.path.join(ROOT, "results_us1999", f + ".json")
        if os.path.exists(fp):
            u99 = json.load(open(fp)).get(code, u99) or u99
    parts = [f"Of the 12 registered cells (two books × six universes), **{len(ls_p) + len(lo_p)} pass** the |t| > {GATE} gate"
             + (f" ({', '.join(['L/S ' + x for x in ls_p] + ['long-only ' + x for x in lo_p])})" if ls_p or lo_p else "")
             + (f" and **{len(ls_n) + len(lo_n)} are significantly negative** ({', '.join(['L/S ' + x for x in ls_n] + ['long-only ' + x for x in lo_n])})" if ls_n or lo_n else "") + "."]
    parts.append(f"Programme-wide ({n} trials, |t| > {zb:.2f}): " + ("; ".join(f"{r.test} t {r.t:+.2f}" for r in prog.itertuples()) if len(prog) else "nothing survives") + ".")
    if u99:
        parts.append(f"US 1999–2012, a period the factsheet was not built on: L/S t {u99['ls_t']:+.2f}, long-only alpha t {u99['lo_alpha_t']:+.2f}.")
    rows = [[UN[R], mark(st(R, LS)["t_mean"]), f"{st(R, LS)['sharpe']:.2f}", mark(st(R, LO)["t_alpha"]), f"{st(R, LO)['sharpe']:.2f} vs {st(R, EW)['sharpe']:.2f}",
             pu(st(R, LO)["maxdd"], 0)] for R in U]
    if u99:
        rows.append(["US 1999–2012", mark(u99["ls_t"]), f"{u99['ls_sharpe']:.2f}", mark(u99["lo_alpha_t"]), f"{u99['lo_sharpe']:.2f} vs {u99['ew_sharpe']:.2f}", "–"])
    return ("## 1. Verdict and scorecard\n\n> **Verdict.** " + " ".join(parts) + "\n\n"
            + table(["Universe", "L/S t", "L/S Sharpe", "Long-only alpha t", "Long-only Sharpe vs equal-weight", "Long-only max DD"], rows)
            + f"*✔ passes the {GATE} gate (Bonferroni over 12 cells); ✖ significantly negative. 2013–2026 unless stated.*\n\n")


# ---------------- 3. Sharpe anatomy (+ chart panel)
def anatomy(code):
    rows = []
    for R in U:
        m = mkt(R)
        for leg, lab in (("LS", "L/S"), ("LO", "Long-only")):
            r = ser(code, R, leg)
            if r is None: continue
            x = pd.concat([r, m], axis=1).dropna(); r_, m_ = x.iloc[:, 0], x.iloc[:, 1]
            mu, vol = r_.mean() * 12, r_.std() * np.sqrt(12); beta = r_.cov(m_) / m_.var()
            mk_part = beta * m_.mean() * 12; alpha = mu - mk_part
            sys_v = abs(beta) * m_.std() * np.sqrt(12); spec_v = np.sqrt(max(vol ** 2 - sys_v ** 2, 1e-12))
            c = ser(code, R, "COST") if leg == "LS" else None
            cost = c.reindex(r_.index).mean() * 12 if c is not None else np.nan
            rows.append([UN[R], lab, p(mu), p(mk_part), p(alpha), p(-cost) if cost == cost else "–", pu(vol), pu(sys_v), f"{mu / vol:.2f}", f"{alpha / spec_v:.2f}"])
    return ("## 3. Where the Sharpe comes from\n\nSharpe = annual return ÷ annual volatility. The return splits into the part the market explains (beta × market return) "
            "and the rest (alpha, net of costs); the volatility into the market's share and the strategy's own. The last column is the Sharpe the book would have "
            "with its market exposure hedged out (before hedging costs).\n\n"
            + table(["Universe", "Book", "Return / yr", "= market part", "+ alpha", "Costs / yr (inside the return)", "Volatility", "of which market", "Sharpe", "Sharpe, market hedged"], rows)
            + f"*Monthly, 2013–2026, market = equal-weight universe. Interactive version: the Strategy Cockpit.*\n\n![Growth, drawdown and rolling Sharpe](../figures/xs_{code}_panel.png)\n\n")


def panel(code):
    fig, ax = plt.subplots(3, 1, figsize=(9, 8.2), sharex=True, gridspec_kw=dict(height_ratios=[2, 1.2, 1.2]))
    for R in U:
        r = ser(code, R, "LS")
        if r is None: continue
        r.index = pd.to_datetime(r.index); g = (1 + r).cumprod(); dd = g / g.cummax() - 1
        rs = r.rolling(36).mean() / r.rolling(36).std() * np.sqrt(12)
        ax[0].plot(g.index, g, color=COLORS[R], lw=1.3, label=UN[R]); ax[1].plot(dd.index, dd * 100, color=COLORS[R], lw=1); ax[2].plot(rs.index, rs, color=COLORS[R], lw=1)
    ax[0].set_yscale("log"); from matplotlib.ticker import FuncFormatter, NullFormatter; ax[0].yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}")); ax[0].yaxis.set_minor_formatter(NullFormatter()); ax[0].set_title("Long/short (net): growth of 1, drawdown and rolling 36-month Sharpe", loc="left", fontsize=11)
    ax[0].legend(ncol=6, fontsize=8, frameon=False, loc="upper left"); ax[1].set_ylabel("Drawdown %"); ax[2].set_ylabel("Sharpe, 36m"); ax[2].axhline(0, color="#8a8984", lw=0.8)
    for a in ax:
        a.grid(color="#e6e5e0", lw=0.6); a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, f"xs_{code}_panel.png"), dpi=130); plt.close(fig)


# ---------------- 4. how it fits
def fits(code):
    """Adds to a market portfolio when Sharpe(self) > corr(self, market) x Sharpe(market). Correlations with the other
    strategies use each pair's common months; Sharpe ratios use each series' full sample (as in the scorecard)."""
    names = CK["meta"]["names"]; others = [c for c in CK["strat"] if c not in (code, "FS18")]
    rows = []
    for R in U:
        r = ser(code, R, "LS"); m = mkt(R)
        if r is None: continue
        x = pd.concat([r.rename("self"), m.rename("mkt")], axis=1).dropna()
        sr_s = x.self.mean() / x.self.std() * np.sqrt(12); sr_m = x.mkt.mean() / x.mkt.std() * np.sqrt(12)
        rm = x.self.corr(x.mkt); hurdle = rm * sr_m
        rho = pd.Series({c: r.corr(ser(c, R, "LS")) for c in others if ser(c, R, "LS") is not None})
        top = rho.abs().idxmax(); worst = x.mkt <= x.mkt.quantile(0.10)
        rows.append([UN[R], f2(rm), f2(rho.mean()), f"{names[top]['name']} ({rho[top]:+.2f})", f"{sr_m:.2f}", f"{hurdle:+.2f}", f"{sr_s:.2f}",
                     "adds" if sr_s > hurdle else "dilutes", p(x.self[worst].mean()), p(x.mkt[worst].mean())])
    return ("## 4. How it fits next to the market and the other strategies\n\nA long/short book improves a market portfolio when its own Sharpe beats "
            "the hurdle: its correlation with the market × the market's Sharpe. A negative correlation makes the hurdle negative, so even a book with "
            "a small positive Sharpe diversifies; the size of the gain still depends on that Sharpe.\n\n"
            + table(["Universe", "Corr. with market", "Avg corr. with the other strategies", "Most similar strategy", "Market Sharpe", "Hurdle Sharpe",
                     "This L/S Sharpe", "Verdict", "L/S in the worst 10% of market months", "Market in those months"], rows)
            + "*Long/short (net), monthly, 2013–2026; market = equal-weight universe; other strategies = the long/short books of FS01–FS12. "
              "The Strategy Cockpit lets you build books of several strategies.*\n\n")


# ---------------- reorganise the 15-section page into the v2 layout
def reorganise(md, code, per, attr_alpha_rng, capm_rng):
    head, *chunks = re.split(r"(?m)^(?=## )", md)
    sec = {}
    for c in chunks:
        m = re.match(r"## (\d+)\. ", c)
        sec[int(m.group(1)) if m else c[:20]] = c
    head = head.replace("<div><b>Status</b>Descriptive factsheet, not a registered trial</div>",
                        f"<div><b>Status</b>Registered gate |t| &gt; {GATE} over 12 cells; every cell in the programme trial ledger</div>")
    head = head.replace("(§10)", "(§9)").replace("(§11)", "(appendix C)").replace("(§12)", "(appendix D)")
    head = head.rstrip() + "\n\n" + LAYOUT_NOTE + "\n\n"
    ren = lambda c, old, new: re.sub(rf"(?m)^## {old}\. ", f"## {new}. ", c, count=1)
    s1 = ren(sec[1], 1, 2).rstrip() + (f"\n\n**Read with care.** A long/short book with a negative beta shows a large CAPM alpha in a rising market. The factor-model "
                                        f"alpha in section 7, after momentum, value and the other themes, is the better guide: here the L/S CAPM alpha ranges "
                                        f"{capm_rng} and the factor alpha {attr_alpha_rng}.\n\n")
    method = "## 6. Method: data, signal and portfolio\n\n" + "".join(re.sub(r"(?m)^## \d+\. ", "### ", sec[k]) for k in (3, 4, 5))
    nine = re.sub(r"(?m)^### 10\.", "### 9.", ren(sec[10], 10, 9))
    eight = ren(sec[9], 9, 8).replace("## 8. Statistical verdict", "## 8. Statistical detail")
    cav = ren(sec[13], 13, 10)
    cav = re.sub(r"\*\*Not a registered trial\.\*\* Descriptive; ", "**Trials.** Every gated cell is in the factsheet trial ledger; ", cav)
    body = (verdict_scorecard(code, per) + s1 + anatomy(code) + fits(code) + ren(sec[2], 2, 5) + method + ren(sec[8], 8, 7) + eight + nine
            + cav + ren(sec[14], 14, 11) + ren(sec[15], 15, 12))
    app = ("\n## Appendix\n\n" + re.sub(r"(?m)^## 6\. ", "### A. ", sec[6]) + re.sub(r"(?m)^## 7\. Trading record", "### B. Trading record and current book", sec[7])
           + re.sub(r"(?m)^## 11\. ", "### C. ", sec[11]) + re.sub(r"(?m)^## 12\. ", "### D. ", sec[12]))
    return head + body + app
