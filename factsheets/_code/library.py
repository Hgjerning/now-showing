# -*- coding: utf-8 -*-
"""Signal library (19 price signals) computed once per universe: top-minus-bottom L/S returns (gross, EW),
their CAPM stats, average characteristic (rank) correlations, and the EW / size-weighted benchmarks.
Used by the 360° section of every factsheet and later by the multifactor battery."""
import json
import os

import numpy as np
import pandas as pd

import data
import perf
import xs

RES = os.environ.get("FS_RESULTS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
CACHE = data.CACHE   # 2026-10-01: follows data.py
LIB = ["max1", "max5", "min1", "min5", "range", "asym", "skew", "ivol", "vol", "vol252", "beta", "r1", "mom", "resmom", "seas", "hi52", "lo52", "brk55", "size"]
START, END = xs.START, xs.END


def ls_series(S, fwd, sig, lag=1):
    x = S[sig]; out = {}
    months = [t for t in x.index if START <= t <= END]
    q = xs.nq(np.median([x.loc[t].notna().sum() for t in months]))
    for t in months:
        s = x.loc[t].dropna()
        if len(s) < 15 or (t + lag) not in fwd.index:
            continue
        pct = s.rank(pct=True, method="first"); r = fwd.loc[t + lag, s.index].fillna(0)
        out[(t + 1).to_timestamp("M")] = float(r[pct > 1 - 1 / q].mean() - r[pct <= 1 / q].mean())
    return pd.Series(out)


def char_corr(S, sigs):
    months = [t for t in S[sigs[0]].index if START <= t <= END]; acc = []
    for t in months[::3]:
        df = pd.DataFrame({k: S[k].loc[t] for k in sigs}).dropna()
        if len(df) >= 15:
            acc.append(df.rank().corr().values)
    return pd.DataFrame(np.nanmean(acc, axis=0), index=sigs, columns=sigs)


def build(R):
    f = os.path.join(CACHE, f"library_{R}.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    I = xs.inputs(R); S, fwd = I["S"], I["fwd"]
    ew = pd.Series({t.to_timestamp("M"): v for t, v in I["ew"].items()})
    L = pd.DataFrame({k: ls_series(S, fwd, k) for k in LIB})
    mk = ew.reindex(L.index)
    mv = ew.rolling(3).std().shift(1).reindex(L.index); hi = mv > mv.median()
    st = {}
    for k in LIB:
        s = L[k].dropna(); reg = perf.nw_ols(s.values, mk.reindex(s.index).values, 6)
        st[k] = dict(ann=float(s.mean() * 12), t=perf.nw_t(s)["t"], sharpe=perf.sharpe(s), beta=reg["beta"], alpha=reg["alpha"] * 12, t_alpha=reg["t_alpha"],
                     up=float(s[mk.reindex(s.index) > 0].mean() * 12), down=float(s[mk.reindex(s.index) <= 0].mean() * 12),
                     hivol=float(s[hi.reindex(s.index).fillna(False)].mean() * 12), lovol=float(s[~hi.reindex(s.index).fillna(True)].mean() * 12))
    out = dict(L=L, stats=st, cc=char_corr(S, LIB), ew=ew, sw=xs.size_weighted(I))
    pd.to_pickle(out, f)
    return out


if __name__ == "__main__":
    import sys
    for R in (sys.argv[1:] or data.REGIONS):
        o = build(R); print(R, {k: round(v["ann"] * 100, 1) for k, v in o["stats"].items()})
