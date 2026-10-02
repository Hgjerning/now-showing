# -*- coding: utf-8 -*-
"""FS01 fixes, stacked in a pre-declared order (each step = one trial), judged on the 2020-2026 holdout.
T0 baseline L/S (S1+S2) | T1 long-only | T2 + System 2 only (fewer, longer trades) | T3 + 4N stop instead of 2N
| T4 + market trend filter (universe index 25-day EMA above its 350-day EMA; Faith 2007 style)."""
import os, sys, pandas as pd
import data, turtle
RES = os.environ.get("FS_RESULTS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
R = sys.argv[1]; o = data.load(R); r, e = o["ret"], o["elig"]
base = pd.read_pickle(os.path.join(RES, f"turtle_{R}.pkl"))
idx = (1 + r.where(e).mean(axis=1).fillna(0)).cumprod()
up = idx.ewm(span=25, adjust=False).mean() > idx.ewm(span=350, adjust=False).mean()
S = {"T0 baseline L/S": 0.5 * base["S1"]["ret"] + 0.5 * base["S2"]["ret"],
     "T1 long-only": 0.5 * base["S1_long"]["ret"] + 0.5 * base["S2_long"]["ret"],
     "T2 + System 2 only": base["S2_long"]["ret"]}
x3 = turtle.run(r, e, system=2, allow_short=False, stop_mult=4.0); S["T3 + 4N stop"] = x3["ret"]
x4 = turtle.run(r, e, system=2, allow_short=False, stop_mult=4.0, regime=up); S["T4 + market trend filter"] = x4["ret"]
S["EW universe"] = r.where(e).mean(axis=1).loc["2013-01-01":]
tr = {"T3": x3["trades"], "T4": x4["trades"]}
pd.to_pickle(dict(series=pd.DataFrame(S), trades=tr, expo4=x4["expo"], up=up), os.path.join(RES, f"turtle_fix_{R}.pkl"))
print(R, {k: round(v.mean() * 252, 3) for k, v in S.items()}, "T4 trades", len(x4["trades"]), "up share %.2f" % up.loc["2013":].mean())
