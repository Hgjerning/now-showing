# -*- coding: utf-8 -*-
"""A04, reported (not gated), added 14 Oct 2026 after review:
factor-adjusted alphas (CAPM, FF5, FF5+momentum) for D1, D10 and D1-D10; 95% confidence intervals and the
smallest effect each trial could have detected; up- vs down-market months; cumulative D1 vs D10.
Inputs: results/ and results_pit/ (decile returns written by run_max.py), data/french_us_*_daily.csv (Ken French).
Writes results_pit/reported_factor.json and figures/fig3_cumulative.png. Adds no trials."""
import json, os, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D, FIG = os.path.join(ROOT, "data"), os.path.join(ROOT, "figures")
LAGS = 3  # as A04-2
Z, ZP = 1.959964, 0.841621  # two-sided 95%; 80% power

def nw(y, X=None, lags=LAGS):
    y = np.asarray(y, float); n = len(y)
    X = np.ones((n, 1)) if X is None else np.column_stack([np.ones(n), X])
    b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
    XtXi = np.linalg.inv(X.T @ X); S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None]); S += (1 - L / (lags + 1)) * (G + G.T)
    se = np.sqrt(np.diag(XtXi @ S @ XtXi)); return b, se, 1 - e.var() / y.var()

def french():
    a = pd.read_csv(os.path.join(D, "french_us_5f_daily.csv"), index_col=0, parse_dates=True)
    m = pd.read_csv(os.path.join(D, "french_us_mom_daily.csv"), index_col=0, parse_dates=True)
    x = a.join(m.rename(columns={m.columns[0]: "Mom"}), how="inner")
    return (1 + x).resample("ME").prod(min_count=1) - 1

F = french()
MODELS = {"CAPM": ["Mkt-RF"], "FF5": ["Mkt-RF", "SMB", "HML", "RMW", "CMA"], "FF5+Mom": ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "Mom"]}
out = {}
for uni, folder in [("published", "results"), ("corrected", "results_pit")]:
    dec = pd.read_csv(os.path.join(ROOT, folder, "max_deciles_top500.csv"), index_col=0, parse_dates=True)
    x = dec.join(F, how="inner"); n = len(x)
    ser = {"D1": x["D1"] - x["RF"], "D10": x["D10"] - x["RF"], "D1-D10": x["D1"] - x["D10"]}
    u = {"months": n, "first": str(x.index[0].date()), "last": str(x.index[-1].date()), "alpha": {}}
    for name, y in ser.items():
        u["alpha"][name] = {}
        for mdl, cols in MODELS.items():
            b, se, r2 = nw(y.values, x[cols].values)
            u["alpha"][name][mdl] = {"alpha_ann": b[0] * 12, "t": b[0] / se[0], "mkt_beta": b[1], "r2": r2,
                                     "loadings": dict(zip(cols, map(float, b[1:])))}
    # raw spread: CI and minimum detectable effect (one-sided 2.5%, 80% power)
    b, se, _ = nw(dec["D1"].values - dec["D10"].values)  # full A04-2 window (factor data end one month earlier)
    u["spread"] = {"ann": b[0] * 12, "ci95": [(b[0] - Z * se[0]) * 12, (b[0] + Z * se[0]) * 12], "mde_ann": (Z + ZP) * se[0] * 12}
    # up vs down market months
    up = x["Mkt-RF"] > 0
    u["by_market"] = {k: {"months": int(m.sum()), "spread_ann": float(ser["D1-D10"][m].mean() * 12),
                          "D1_ann": float(x["D1"][m].mean() * 12), "D10_ann": float(x["D10"][m].mean() * 12),
                          "mkt_ann": float(x["Mkt-RF"][m].mean() * 12)} for k, m in [("up", up), ("down", ~up)]}
    y22 = x.loc["2022"]; u["year_2022"] = {"D1": float((1 + y22["D1"]).prod() - 1), "D10": float((1 + y22["D10"]).prod() - 1),
                                           "mkt": float((1 + y22["Mkt-RF"] + y22["RF"]).prod() - 1)}
    a_, b_ = dec.loc[:"2024-12-31"], dec.loc["2025-01-01":]
    u["split_2025"] = {"to2024_months": len(a_), "to2024_D1_growth": float((1 + a_["D1"]).prod()), "to2024_D10_growth": float((1 + a_["D10"]).prod()),
                       "from2025_months": len(b_), "from2025_D1": float((1 + b_["D1"]).prod() - 1), "from2025_D10": float((1 + b_["D10"]).prod() - 1)}
    out[uni] = u
    if uni == "corrected":
        c1, c10 = (1 + x["D1"]).cumprod(), (1 + x["D10"]).cumprod()

# A04-1 (JKP) CI and MDE
J = pd.read_csv(os.path.join(ROOT, "results_pit", "jkp_max_factor.csv"), index_col=0, parse_dates=True)["ret"].loc["2012-01-01":"2025-12-31"]
b, se, _ = nw(J.values, lags=6)
out["A04-1"] = {"ann": b[0] * 12, "ci95": [(b[0] - Z * se[0]) * 12, (b[0] + Z * se[0]) * 12], "mde_ann": (Z + ZP) * se[0] * 12,
                "months": len(J), "insample_1963_2005_ann": 0.0402}
json.dump(out, open(os.path.join(ROOT, "results_pit", "reported_factor.json"), "w"), indent=2)

sys.path.insert(0, os.path.join(ROOT, "..", "_shared", "lib10"))
try:
    from common import BLUE, ORANGE, INK, INK2, mpl_style; mpl_style(plt)
except Exception:
    BLUE, ORANGE, INK, INK2 = "#1f5fa8", "#e07b24", "#222", "#666"
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
ax.plot(c1.index, c1.values, color=BLUE, lw=2, label="Decile 1, steadiest")
ax.plot(c10.index, c10.values, color=ORANGE, lw=2, label="Decile 10, lottery")
ax.axvspan(pd.Timestamp("2020-04-01"), pd.Timestamp("2021-12-31"), color="#999", alpha=0.15, lw=0)
ax.text(pd.Timestamp("2020-05-01"), ax.get_ylim()[1] * 0.92, "meme window", fontsize=9.5, color=INK2)
ax.set_yscale("log"); ax.set_ylabel("Growth of $1 (log scale)")
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
ax.yaxis.set_major_locator(FixedLocator([1, 1.5, 2, 3, 4, 6, 8])); ax.yaxis.set_minor_locator(NullLocator())
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:g}")); ax.legend(frameon=False, loc="upper left")
ax.set_title("S&P 500 members: steady decile ahead until 2025, lottery decile +107% since", loc="left", fontsize=12.5, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_cumulative.png")); plt.close(fig)

for uni in ("published", "corrected"):
    u = out[uni]; print(f"\n== {uni} ({u['months']} months {u['first']}..{u['last']})")
    for name in ("D1", "D10", "D1-D10"):
        print(name, "  ".join(f"{m}: {v['alpha_ann']*100:+.1f}% (t {v['t']:.2f}, b {v['mkt_beta']:.2f}, R2 {v['r2']:.2f})" for m, v in u["alpha"][name].items()))
    print("loadings D1-D10 FF5+Mom:", {k: round(v, 2) for k, v in u["alpha"]["D1-D10"]["FF5+Mom"]["loadings"].items()})
    s = u["spread"]; print(f"spread {s['ann']*100:+.1f}% CI [{s['ci95'][0]*100:+.1f}, {s['ci95'][1]*100:+.1f}] MDE {s['mde_ann']*100:.1f}%")
    print("by market", {k: {kk: round(vv*100, 1) if 'ann' in kk else vv for kk, vv in v.items()} for k, v in u["by_market"].items()})
    print("2022", {k: round(v*100, 1) for k, v in u["year_2022"].items()})
a = out["A04-1"]; print(f"\nA04-1 {a['ann']*100:+.1f}% CI [{a['ci95'][0]*100:+.1f}, {a['ci95'][1]*100:+.1f}] MDE {a['mde_ann']*100:.1f}% n {a['months']}")
