"""A06 after costs, like for like with A31 (6 Nov 2026). REPORTED, NOT GATED: no new trial.

A06 was pre-registered to report turnover but never computed it, so its results are before costs only. For the combined
Minority Report (Part 1, 24 Nov 2026) the S&P 500 and US small-cap results must be compared on the same terms:
  - same window: formation months 2017-01 .. 2026-07 (A06's out-of-sample window; A31 U1 is cut to it),
  - same book and cost method: A31's book() (decile long-short, equal weight, drift-aware turnover of both legs,
    cost = one-way rate x traded weight), copied verbatim below,
  - cost per universe from _shared/lib10/costs.py tiers: S&P 500 members 0.10% one-way (us_large); A31 used 0.50% for
    small caps (its signed rate; costs.py's us_small tier is 0.40%), so small caps are also shown at 0.40%.
Inputs: results_pit/oos_predictions.pkl (A06's saved predictions, corrected S&P 500 list) and the cached long panel
(P10_UNIVERSE=sp500_pit). Check: the gross series must match results_pit/longshort_monthly.csv.
Run from the ClaudeCode folder:  python Project10_Articles\\Articles\\A08_Minority_Report_ML\\code\\costs_like_for_like.py
Writes results_pit/costs_like_for_like.json and results_pit/costs_like_for_like_monthly.csv.
"""
import json, os, sys, time
os.environ.setdefault("P10_UNIVERSE", "sp500_pit")
_HERE0 = os.path.dirname(os.path.abspath(__file__))
_win = os.path.join(_HERE0, "..", "..", "..", "Factsheets", "_data_private", "p10_cache_win")
if os.path.exists(os.path.join(_win, "long_sp500_pit.pkl")):
    os.environ.setdefault("P10_CACHE", os.path.abspath(_win))   # the Windows copy of the long panel cache
import numpy as np, pandas as pd
from scipy import stats as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); ART = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ART, "_shared", "lib10"))
from features import panel_long  # noqa: E402
t0 = time.time(); say = lambda m: print(f"[{time.strftime('%H:%M:%S')}] {m}  ({(time.time() - t0) / 60:.1f} min)", flush=True)


def book(L, score, cost, q=0.1):   # verbatim from A09_Minority_Report_2_Small_Print/code/run_a31.py (signed 6 Oct 2026)
    df = pd.DataFrame({"s": score, "r": L.loc[score.index, "fwd"]})
    out = []; prev = None
    for m, g in df.groupby(level=0):
        g = g.droplevel(0); k = g.s.rank(pct=True)
        lo, sh = g.index[k > 1 - q], g.index[k <= q]
        w = pd.concat([pd.Series(1 / len(lo), index=lo), pd.Series(-1 / len(sh), index=sh)])
        w = w.groupby(level=0).sum()
        traded = (w.sub(prev, fill_value=0).abs().sum()) if prev is not None else w.abs().sum()
        r = g.r.reindex(w.index)
        rl, rs = r[w > 0].mean(), r[w < 0].mean()
        gross = rl - rs
        rr = r.fillna(0.0)
        wl = w[w > 0] * (1 + rr[w > 0]); ws = w[w < 0] * (1 + rr[w < 0])
        prev = pd.concat([wl / wl.sum(), -ws / ws.sum()]) if len(wl) and len(ws) else None
        ic = st.spearmanr(g.s, g.r, nan_policy="omit")[0]
        out.append(dict(month=m, gross=gross, turnover=traded, net=gross - cost * traded, ic=ic, long=rl, short=rs))
    return pd.DataFrame(out).set_index("month")


def nwt(x, L=3):
    x = x.dropna(); e = x - x.mean(); T = len(x); v = (e ** 2).sum() / T
    for l in range(1, L + 1):
        v += 2 * (1 - l / (L + 1)) * (e.values[l:] * e.values[:-l]).sum() / T
    return float(x.mean() / np.sqrt(v / T))


def stats(g, n, to):
    return dict(gross_ann=float(g.mean() * 12), gross_t=nwt(g), net_ann=float(n.mean() * 12), net_t=nwt(n),
                net_sharpe=float(n.mean() / n.std() * np.sqrt(12)), turnover_m=float(to.iloc[1:].mean()),
                breakeven_oneway=float(g.mean() / to.iloc[1:].mean()), months=int(n.notna().sum()))


say("loading A06 predictions and the S&P 500 long panel (cached)")
P = pd.read_pickle(os.path.join(ROOT, "results_pit", "oos_predictions.pkl")); L = panel_long()
ref = pd.read_csv(os.path.join(ROOT, "results_pit", "longshort_monthly.csv"), index_col=0, parse_dates=True)
out, monthly = {"note": "reported, not gated; 6 Nov 2026; window 2017-01..2026-07 formation months"}, {}
for i, name in enumerate(["Ensemble", "Momentum"], 1):
    say(f"{i}/2 S&P 500 book: {name}")
    for cost in (0.0010, 0.0005, 0.0025):
        b = book(L, P[name].dropna(), cost)
        if cost == 0.0010:
            chk = (b.gross - ref[name].reindex(b.index)).abs().max()
            out[f"check_{name}_gross_vs_A06"] = float(chk)
            monthly[f"sp500_{name}_gross"] = b.gross; monthly[f"sp500_{name}_net"] = b.net; monthly[f"sp500_{name}_turnover"] = b.turnover
        out[f"sp500_{name}_cost{cost * 100:.2f}pct"] = stats(b.gross, b.net, b.turnover)
say("US small caps (A31 U1 saved monthly series), same window")
U = os.path.join(ART, "A09_Minority_Report_2_Small_Print", "results", "U1")
G = pd.read_csv(os.path.join(U, "gross_monthly.csv"), index_col=0, parse_dates=True).loc["2017-01":"2026-07"]
T = pd.read_csv(os.path.join(U, "turnover_monthly.csv"), index_col=0, parse_dates=True).loc["2017-01":"2026-07"]
for name in ["Ensemble", "Momentum"]:
    for cost in (0.0050, 0.0040):
        n = G[name] - cost * T[name]
        out[f"smallcap_{name}_cost{cost * 100:.2f}pct"] = stats(G[name], n, T[name])
json.dump(out, open(os.path.join(ROOT, "results_pit", "costs_like_for_like.json"), "w"), indent=2)
pd.DataFrame(monthly).to_csv(os.path.join(ROOT, "results_pit", "costs_like_for_like_monthly.csv"))
for k, v in out.items():
    if isinstance(v, dict):
        print(f"  {k:38s} gross {v['gross_ann']:+.1%} (t {v['gross_t']:.2f})  net {v['net_ann']:+.1%} (t {v['net_t']:.2f})  turnover {v['turnover_m']:.0%}/m")
    else:
        print(f"  {k}: {v}")
say("done. Paste the lines above to Claude.")
