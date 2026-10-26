# -*- coding: utf-8 -*-
"""A04, reported (not gated), added 22 Oct 2026: the three questions of Deutsche Bank's 'Lottery factor with new faces'
(DB Quant Handbook, 10 Dec 2010, pp. 678-683), asked of the A04-2 universe (actual S&P 500 members, P10_UNIVERSE=sp500_pit).
  1. Is MAX just short-term reversal?  Own reversal spread in the same universe (last month's losers minus winners), rank ICs,
     signal persistence (DB: rank IC and factor serial correlation), the MAX spread regressed on reversal + FF5 + momentum,
     and a reversal-neutral MAX spread (MAX quintiles within past-month-return quintiles).
  2. Is MAX just volatility?  Volatility-neutral MAX (MAX quintiles within 60-day volatility quintiles) and residual MAX
     (MAX minus its cross-sectional fit on volatility, deciles).
  3. Which side pays?  Long leg (decile 1 minus the equal-weighted universe) and short leg (universe minus decile 10).
Same panel as run_max.py, on today's data files; deciles by rank (ceil), where run_max.py uses qcut (baseline -6.38% vs -6.32%); the baseline spread is recomputed here so every comparison is
like for like. Writes results_pit/reported_db2010.json and figures/fig4_db2010.png. Adds no trials."""
import json, os, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from features import price_features  # noqa: E402
from panel import load_all  # noqa: E402

D, FIG, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, "figures"), os.path.join(ROOT, "results_pit")
LAGS = 3


def nw(y, X=None, lags=LAGS):
    y = np.asarray(y, float); n = len(y)
    X = np.ones((n, 1)) if X is None else np.column_stack([np.ones(n), X])
    b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
    XtXi = np.linalg.inv(X.T @ X); S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None]); S += (1 - L / (lags + 1)) * (G + G.T)
    se = np.sqrt(np.diag(XtXi @ S @ XtXi)); return b, se


def stat(s):
    s = pd.Series(s).dropna(); b, se = nw(s.values); return {"ann": float(b[0] * 12), "t": float(b[0] / se[0]), "months": int(len(s))}


def bins(s, k):
    return (np.ceil(k * s.rank(method="first") / len(s))).astype(int)


PLOT_ONLY = os.environ.get("DB_PLOT_ONLY") == "1"   # re-draw figures/fig4_db2010.png from results_pit/reported_db2010.json
if not PLOT_ONLY:
    px, fd, pm, mc, uni, ret = load_all(); F = price_features(px, pm)
    mx, vol = F["maxret"], F["vol60"]
    months = pm.index[(pm.index >= "2013-01-31") & (pm.index <= "2026-07-31")]
    rows, ic_max, ic_rev, pers_max, pers_rev = [], [], [], [], []
    prev = None
    for t in months:
        nxt = pm.index[pm.index.get_loc(t) + 1]
        m = mx.loc[t].where(uni.loc[t]).dropna()
        df = pd.DataFrame({"max": m, "vol": vol.loc[t, m.index], "rev": ret.loc[t, m.index], "r": ret.loc[nxt, m.index]})
        r = df["r"]
        d = bins(df["max"], 10)
        row = {"month": nxt, "D1": r[d == 1].mean(), "D10": r[d == 10].mean(), "EW": r.mean(),
               **{f"D{k}": r[d == k].mean() for k in range(2, 10)}}
        q5 = bins(df["max"], 5); row["max_quintile"] = r[q5 == 1].mean() - r[q5 == 5].mean()   # like-for-like baseline for the quintile versions
        dd = df.dropna(subset=["rev"]); dr = bins(dd["rev"], 10)
        row["rev_spread"] = dd["r"][dr == 1].mean() - dd["r"][dr == 10].mean()          # last month's losers minus winners
        # reversal-neutral MAX: MAX quintiles within past-month-return quintiles, low minus high averaged over the five groups
        g = bins(dd["rev"], 5); sp = []
        for k in range(1, 6):
            x = dd[g == k]; q = bins(x["max"], 5); sp.append(x["r"][q == 1].mean() - x["r"][q == 5].mean())
        row["max_rev_neutral"] = np.nanmean(sp)
        # volatility-neutral MAX: MAX quintiles within 60-day volatility quintiles
        dv = df.dropna(subset=["vol"]); gv = bins(dv["vol"], 5); sp = []
        for k in range(1, 6):
            x = dv[gv == k]; q = bins(x["max"], 5); sp.append(x["r"][q == 1].mean() - x["r"][q == 5].mean())
        row["max_vol_neutral"] = np.nanmean(sp)
        # residual MAX: MAX minus its cross-sectional fit on volatility, deciles
        bb = np.polyfit(dv["vol"].values, dv["max"].values, 1); res = dv["max"] - np.polyval(bb, dv["vol"].values)
        dq = bins(res, 10); row["max_resid_vol"] = dv["r"][dq == 1].mean() - dv["r"][dq == 10].mean()
        rows.append(row)
        ic_max.append(df[["max", "r"]].dropna().corr(method="spearman").iloc[0, 1] * -1)    # low MAX -> high return = positive IC
        ic_rev.append(dd[["rev", "r"]].corr(method="spearman").iloc[0, 1] * -1)
        if prev is not None:
            c = pd.concat([df[["max", "rev"]], prev], axis=1, keys=["now", "then"]).dropna()
            pers_max.append(c[("now", "max")].rank().corr(c[("then", "max")].rank()))
            pers_rev.append(c[("now", "rev")].rank().corr(c[("then", "rev")].rank()))
        prev = df[["max", "rev"]]
    P = pd.DataFrame(rows).set_index("month"); P["spread"] = P.D1 - P.D10
    P.to_csv(os.path.join(OUT, "db2010_monthly.csv"))

    fr = pd.read_csv(os.path.join(D, "french_us_5f_daily.csv"), index_col=0, parse_dates=True).join(
        pd.read_csv(os.path.join(D, "french_us_mom_daily.csv"), index_col=0, parse_dates=True).rename(columns=lambda c: "Mom"), how="inner")
    FM = (1 + fr).resample("ME").prod(min_count=1) - 1
    x = P.join(FM, how="inner")
    cols = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "Mom"]


    def alpha(y, cs):
        b, se = nw(y.values, x[cs].values); return {"alpha_ann": float(b[0] * 12), "t": float(b[0] / se[0]), "loadings": dict(zip(cs, map(float, b[1:])))}


    out = {"source": "Deutsche Bank, DB Quant Handbook, 'Lottery factor with new faces', 10 Dec 2010, pp. 678-683",
           "window": [str(P.index[0].date()), str(P.index[-1].date())],
           "baseline_spread": stat(P.spread), "baseline_quintile_spread": stat(P.max_quintile), "note": "baseline recomputed on today's data files; the published A04-2 corrected figure is -5.9% a year (t -1.30)",
           "reversal": {"rev_spread": stat(P.rev_spread), "corr_with_max_spread": float(P.spread.corr(P.rev_spread)),
                        "rank_ic_max": {"mean": float(np.mean(ic_max)), "ic_ratio": float(np.mean(ic_max) / np.std(ic_max))},
                        "rank_ic_rev": {"mean": float(np.mean(ic_rev)), "ic_ratio": float(np.mean(ic_rev) / np.std(ic_rev))},
                        "signal_persistence_max": float(np.mean(pers_max)), "signal_persistence_rev": float(np.mean(pers_rev)),
                        "max_spread_on_rev_ff5_mom": alpha(x.spread, cols + ["rev_spread"]),
                        "max_spread_on_ff5_mom": alpha(x.spread, cols),
                        "max_reversal_neutral": stat(P.max_rev_neutral)},
           "volatility": {"max_vol_neutral": stat(P.max_vol_neutral), "max_resid_vol": stat(P.max_resid_vol),
                          "max_vol_neutral_ff5_mom": alpha(x.max_vol_neutral, cols)},
           "legs": {"long_D1_minus_EW": stat(P.D1 - P.EW), "short_EW_minus_D10": stat(P.EW - P.D10),
                    "long_ff5_mom": alpha(x.D1 - x.EW, cols), "short_ff5_mom": alpha(x.EW - x.D10, cols),
                    "deciles_ann": {f"D{k}": float(P[f"D{k}"].mean() * 12) for k in range(1, 11)}, "EW_ann": float(P.EW.mean() * 12)}}
    json.dump(out, open(os.path.join(OUT, "reported_db2010.json"), "w"), indent=2)
else:
    out = json.load(open(os.path.join(OUT, "reported_db2010.json")))

import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
try:
    from common import BLUE, GREY, INK, INK2, ORANGE, mpl_style; mpl_style(plt)
except Exception:
    BLUE, GREY, INK, INK2, ORANGE = "#1f5fa8", "#999", "#222", "#666", "#e07b24"
bars = [("MAX, deciles (baseline)", out["baseline_spread"], BLUE),
        ("MAX, quintiles (compare the two \"within\" rows)", out["baseline_quintile_spread"], BLUE),
        ("MAX within past-month-return groups", out["reversal"]["max_reversal_neutral"], GREY),
        ("MAX within volatility groups", out["volatility"]["max_vol_neutral"], GREY),
        ("MAX with volatility removed (residual)", out["volatility"]["max_resid_vol"], GREY),
        ("Short-term reversal (losers minus winners)", out["reversal"]["rev_spread"], ORANGE)]
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
y = np.arange(len(bars))[::-1]
ax.barh(y, [b[1]["ann"] * 100 for b in bars], color=[b[2] for b in bars], height=0.6)
for yy, b in zip(y, bars):
    v = b[1]["ann"] * 100; ax.text(v + (0.3 if v >= 0 else -0.3), yy, f"{v:+.1f}% (t {b[1]['t']:.2f})", va="center", ha="left" if v >= 0 else "right", fontsize=9.5)
ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(y); ax.set_yticklabels([b[0] for b in bars], fontsize=10)
lo = min(b[1]["ann"] * 100 for b in bars); hi = max(b[1]["ann"] * 100 for b in bars); ax.set_xlim(min(lo * 1.6, -1), max(hi * 1.6, 1))
ax.set_xlabel("Low minus high, % a year (next month, equal weight)")
ax.set_title("Three checks from a 2010 research note, S&P 500 members 2013-2026", loc="left", fontsize=12, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig4_db2010.png")); plt.close(fig)
print(json.dumps(out, indent=1))
