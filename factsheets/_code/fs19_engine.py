# -*- coding: utf-8 -*-
"""FS19 part A: engine tests (planning/PREREG_FS19.md). Writes results/fs19_engine.json."""
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd

import data
import perf
import signals as SG
import signals2 as SG2
import xs

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results")
SIGS = ["max1", "min1", "max5", "min5", "range", "asym", "skew", "ivol", "vol", "beta", "r1", "mom", "hi52", "lo52", "brk55", "vol252", "seas", "size", "resmom"]
_load = data.load


def rebuild(R, transform):
    """Rebuild S (both signal modules) with data.load returning transformed returns; caches redirected to a temp dir."""
    tmp = tempfile.mkdtemp(); c1, c2 = SG.CACHE, SG2.CACHE
    SG.CACHE = SG2.CACHE = tmp

    def patched(r, *a, **k):
        o = dict(_load(r, *a, **k))
        if r == R and not k.get("pit", True) is False:
            o["ret"], o["elig"] = transform(o["ret"], o["elig"])
        return o
    data.load = patched
    try:
        b = SG.build(R); x = SG2.build(R)
    finally:
        data.load = _load; SG.CACHE, SG2.CACHE = c1, c2
    S = dict(b["S"]); S.update(x["S"])
    return dict(S=S, fwd=b["fwd"], E=b["E"], ew=b["ew"], capw=x["capw"], R=R)


def truncation():
    out = {}
    for R in ["US", "EU", "UK"]:
        full = xs.inputs(R); out[R] = {}
        for T in ["2015-12", "2019-12", "2023-12"]:
            end = pd.Period(T).to_timestamp("M")
            I = rebuild(R, lambda r, e: (r.loc[:end], e.loc[:end]))
            d = {}
            for k in SIGS:
                a = full["S"][k].loc[pd.Period(T)]; b = I["S"][k].loc[pd.Period(T)] if pd.Period(T) in I["S"][k].index else pd.Series(dtype=float)
                j = a.dropna().index.intersection(b.dropna().index)
                d[k] = dict(max_abs_diff=float((a[j] - b[j]).abs().max()) if len(j) else None, n_common=int(len(j)), n_full=int(a.notna().sum()), n_trunc=int(b.notna().sum()))
            out[R][T] = d
            bad = [k for k, v in d.items() if v["max_abs_diff"] is None or v["max_abs_diff"] > 1e-9 or v["n_full"] != v["n_trunc"]]
            print("truncation", R, T, "mismatch:", bad, flush=True)
    return out


LH = {"max1": False, "min1": True, "max5": False, "min5": True, "range": False, "asym": False, "skew": False, "ivol": False, "vol": False, "beta": False,
      "r1": False, "mom": True, "hi52": True, "lo52": False, "brk55": True, "vol252": False, "seas": True, "size": False, "resmom": True}


def noise():
    out = {"t": {}, "cheat": {}}
    for R in ["US", "EU"]:
        for seed in range(5):
            rng = np.random.default_rng(seed)
            I = rebuild(R, lambda r, e: (pd.DataFrame(rng.normal(0, 0.02, r.shape), index=r.index, columns=r.columns).where(r.notna()), e))
            for k in SIGS:
                P = xs.run(I, k, LH[k], borrow=False, finance=False)
                out["t"][f"{R}|{seed}|{k}"] = perf.nw_t(P.ls_gross.dropna())["t"]
            f = I["fwd"]
            I["S"]["cheat_next"] = f.shift(-1).where(I["E"]); I["S"]["cheat_now"] = f.where(I["E"])
            for k in ["cheat_next", "cheat_now"]:
                P = xs.run(I, k, True, borrow=False, finance=False); out["cheat"][f"{R}|{seed}|{k}"] = perf.nw_t(P.ls_gross.dropna())["t"]
            print("noise", R, seed, "max|t|", round(max(abs(v) for kk, v in out["t"].items() if kk.startswith(f"{R}|{seed}|")), 2),
                  "cheat", {k: round(v, 1) for k, v in out["cheat"].items() if k.startswith(f"{R}|{seed}|")}, flush=True)
    ts = np.array(list(out["t"].values()))
    out["share_abs_t_gt_1_96"] = float((np.abs(ts) > 1.96).mean()); out["max_abs_t"] = float(np.abs(ts).max()); out["n"] = int(len(ts))
    return out


def costs():
    out = {}
    I = xs.inputs("US")
    for name, sig, lh in [("low beta (bn)", "beta", False), ("12-1 momentum (bn)", "mom", True)]:
        P = xs.run(I, sig, lh, beta_neutral=True)
        e1 = float(((P.ls_gross - P.ls_net) - (P.cost + P.borrow + P.fin)).abs().max())
        e2 = float((P.cost - xs.COST * 2 * (P.to_good + P.to_bad)).abs().max())
        Q = xs.run(I, sig, lh, beta_neutral=True, borrow=False, finance=False)
        e3 = float(((Q.ls_gross - Q.cost) - Q.ls_net).abs().max())
        out[name] = dict(identity=e1, cost_formula=e2, no_borrow_fin=e3)
        print("costs", name, e1, e2, e3, flush=True)
    return out


def betas():
    out = {}
    for R in ["US", "EU", "UK", "DK", "SC", "WD"]:
        I = xs.inputs(R); ew = pd.Series({t.to_timestamp("M"): v for t, v in I["ew"].items()})
        out[R] = {}
        for name, sig, lh in [("low beta (bn)", "beta", False), ("12-1 momentum (bn)", "mom", True)]:
            P = xs.run(I, sig, lh, beta_neutral=True); y = P.ls_gross.dropna(); x = ew.reindex(y.index)
            reg = perf.nw_ols(y.values, x.values, 6); out[R][name] = dict(beta=float(reg["beta"]), t=float(reg.get("t_beta", np.nan)) if isinstance(reg, dict) else None)
        print("beta", R, {k: round(v["beta"], 2) for k, v in out[R].items()}, flush=True)
    return out


def main(parts):
    f = os.path.join(RES, "fs19_engine.json"); out = json.load(open(f)) if os.path.exists(f) else {}
    for p in parts:
        out[p] = globals()[p]()
        json.dump(out, open(f, "w"), indent=1, default=float)


if __name__ == "__main__":
    main(sys.argv[1:] or ["costs", "betas", "truncation", "noise"])
