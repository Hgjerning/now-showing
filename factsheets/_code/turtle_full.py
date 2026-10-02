# -*- coding: utf-8 -*-
"""FS01 long-only books scaled to 100% invested (Henrik, 2026-10-01: "scale to 1"). Not a new trial: the same four
pre-declared long-only steps (T1-T4 in turtle_fix.py), re-stated at 100% invested via turtle.fully_invested().
Usage: python turtle_full.py <REGION> [...]   ->  results/turtle_full_<REGION>.json, then python turtle_full.py --table
"""
import json
import os
import sys

import numpy as np
import pandas as pd

import data
import turtle

RES = os.environ.get("FS_RESULTS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
REGIONS = ["US", "EU", "UK", "DK", "SC", "WD"]


def stats(x):
    x = x.dropna()
    if len(x) < 50 or x.std() == 0:
        return None
    w = (1 + x).cumprod()
    return dict(ann=float(x.mean() * 252), vol=float(x.std() * np.sqrt(252)), sharpe=float(x.mean() / x.std() * np.sqrt(252)),
                cagr=float(w.iloc[-1] ** (252 / len(x)) - 1), maxdd=float((w / w.cummax() - 1).min()))


def one(R):
    o = data.load(R); r, e = o["ret"], o["elig"]
    idx = (1 + r.where(e).mean(axis=1).fillna(0)).cumprod()
    up = idx.ewm(span=25, adjust=False).mean() > idx.ewm(span=350, adjust=False).mean()
    runs = {"S1_long": turtle.run(r, e, system=1, allow_short=False), "S2_long": turtle.run(r, e, system=2, allow_short=False),
            "T3": turtle.run(r, e, system=2, allow_short=False, stop_mult=4.0),
            "T4": turtle.run(r, e, system=2, allow_short=False, stop_mult=4.0, regime=up)}
    full = {k: turtle.fully_invested(v) for k, v in runs.items()}
    books = {"T1 long-only": (0.5 * runs["S1_long"]["ret"] + 0.5 * runs["S2_long"]["ret"], 0.5 * full["S1_long"]["ret"] + 0.5 * full["S2_long"]["ret"],
                              0.5 * runs["S1_long"]["expo"]["long"] + 0.5 * runs["S2_long"]["expo"]["long"]),
             "T2 + System 2 only": (runs["S2_long"]["ret"], full["S2_long"]["ret"], runs["S2_long"]["expo"]["long"]),
             "T3 + 4N stop": (runs["T3"]["ret"], full["T3"]["ret"], runs["T3"]["expo"]["long"]),
             "T4 + market trend filter": (runs["T4"]["ret"], full["T4"]["ret"], runs["T4"]["expo"]["long"])}
    ew = r.where(e).mean(axis=1).loc["2013-01-01":]
    out = {"region": R, "books": {}, "ew": {"full": stats(ew), "holdout": stats(ew.loc["2020-01-01":])}}
    for name, (raw, f, L) in books.items():
        out["books"][name] = {"avg_invested_raw": float(L.loc["2013":].mean()),
                              "cash_days": float((L.loc["2013":] <= 1e-9).mean()),
                              "raw": {"full": stats(raw.loc["2013":]), "holdout": stats(raw.loc["2020":])},
                              "invested_100": {"full": stats(f.loc["2013":]), "holdout": stats(f.loc["2020":])}}
    json.dump(out, open(os.path.join(RES, f"turtle_full_{R}.json"), "w"), indent=1)
    for name, b in out["books"].items():
        a, c = b["raw"]["full"], b["invested_100"]["full"]
        print(f"{R} {name:26s} invested {b['avg_invested_raw']:.0%} -> 100% | Sharpe {a['sharpe']:.2f} -> {c['sharpe']:.2f} | "
              f"CAGR {a['cagr']:+.1%} -> {c['cagr']:+.1%} | maxDD {a['maxdd']:.0%} -> {c['maxdd']:.0%}", flush=True)


if __name__ == "__main__":
    for R in [a for a in sys.argv[1:] if not a.startswith("--")] or REGIONS:
        one(R)
