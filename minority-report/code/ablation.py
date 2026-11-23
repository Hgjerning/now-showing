# -*- coding: utf-8 -*-
"""A06, added 7 Oct 2026 after external review. REPORTED, NOT GATED (no trial spent). Point-in-time S&P 500 universe.
1. Feature ablation: the same eight models, walk-forward unchanged, with (a) all 12 features [reproduces results_pit],
   (b) 12-1 momentum removed, (c) the whole price-trend family removed (12-1 momentum, 3-month return, 52-week-high distance).
2. Simple single-characteristic benchmarks: top-minus-bottom decile on value (B/M), earnings yield, gross profitability,
   low volatility, small size and 12-1 momentum, same portfolio rules."""
import json, os, sys, time
os.environ.setdefault("P10_UNIVERSE", "sp500_pit")  # the corrected universe (number of record); set before lib10 loads
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import run_ml as R  # noqa: E402  (adds lib10 to the path)
from stats import nw_t, sharpe  # noqa: E402
from features import panel_long  # noqa: E402
OUT = os.path.join(os.path.dirname(HERE), "results_pit")
L = panel_long(); names = list(R.MODELS)
variants = {"all": R.FEATS, "no_mom": [f for f in R.FEATS if f != "mom"],
            "no_trend": [f for f in R.FEATS if f not in ("mom", "r3", "hi52")]}
res = {}
for v, feats in variants.items():
    t0 = time.time(); R.FEATS = feats
    Lw, P = R.walk_forward(L, names)
    P["Ensemble"] = P.groupby(level=0).rank(pct=True).mean(axis=1)
    LS = pd.DataFrame({n: R.long_short(Lw, P[n]).ls for n in P.columns})
    LS.to_csv(f"{OUT}/ablation_ls_{v}.csv")
    res[v] = {n: dict(ann=float(LS[n].mean() * 12), sharpe=sharpe(LS[n]), t=nw_t(LS[n].dropna(), 3)["t"],
                      sh1=sharpe(LS[n].iloc[:len(LS) // 2]), sh2=sharpe(LS[n].iloc[len(LS) // 2:])) for n in LS}
    print(v, round(time.time() - t0), {n: round(x["sharpe"], 2) for n, x in res[v].items()}, flush=True)
# benchmarks
Lw = L[(L.index.get_level_values(0) >= R.FIRST_OOS) & (L.index.get_level_values(0) <= R.LAST_FORM)]
bm = {"Value (book/market)": ("bm", 1), "Earnings yield": ("ep", 1), "Gross profitability": ("gpa", 1), "Low volatility": ("vol60", -1),
      "Small size": ("size", -1), "Momentum (12-1)": ("mom", 1)}
B = {}
for lab, (f, sgn) in bm.items():
    ls = R.long_short(Lw, sgn * Lw[f]).ls
    B[lab] = dict(ann=float(ls.mean() * 12), sharpe=sharpe(ls), t=nw_t(ls.dropna(), 3)["t"], sh1=sharpe(ls.iloc[:len(ls) // 2]), sh2=sharpe(ls.iloc[len(ls) // 2:]))
print(json.dumps(B, indent=1))
json.dump(dict(note="Added 7 Oct 2026 after external review. Reported, not gated. PIT S&P 500 universe.", ablation=res, benchmarks=B),
          open(f"{OUT}/ablation.json", "w"), indent=1)
print("DONE")  # about 15 minutes on 2 cores; written to results_pit/ablation.json and ablation_ls_*.csv
