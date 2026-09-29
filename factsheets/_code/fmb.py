# -*- coding: utf-8 -*-
"""Fama-MacBeth: all signals together. Each month t, next-month returns of the eligible stocks are regressed
cross-sectionally on the signals, each transformed to a signed percentile rank in [-0.5, 0.5] (high = the
pre-declared good end), so a slope is roughly the top-minus-bottom return that signal adds holding the others
fixed. Missing signal values are set to 0 (the median) after ranking. Slopes are averaged over time with
Newey-West t (6 lags). Two specifications per market: univariate (each signal alone) and multivariate (one
representative per FS13 cluster, plus the US fundamental composites in the US).
Writes results/fmb.json and results/fmb.pkl."""
import json
import os

import numpy as np
import pandas as pd

import fundamentals as FU
import perf
import xs
from battery import DIRECTION

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results")
U = ["US", "EU", "UK", "DK", "SC", "WD"]
# one representative per FS13 cluster (and the within-block candidates the multifactor model may use)
PRICE = ["beta", "vol252", "max1", "mom", "resmom", "hi52", "r1", "seas", "skew", "size"]
FUNDC = [FU.COMP[t] for t in FU.THEMES]
LAB = {**{s: DIRECTION[s][2] for s in DIRECTION}, **{FU.COMP[t]: t + " (fund.)" for t in FU.THEMES}}
LH = {**{s: DIRECTION[s][0] for s in DIRECTION}, **{FU.COMP[t]: True for t in FU.THEMES}}
START, END = pd.Period("2013-01"), pd.Period("2026-07")


def signed_rank(x, long_high):
    r = x.rank(pct=True) - 0.5
    return r if long_high else -r


def fm(I, sigs, min_n=30):
    S, fwd, E = I["S"], I["fwd"], I["E"]
    months = [t for t in S[sigs[0]].index if START <= t <= END and (t + 1) in fwd.index]
    rows = {}
    for t in months:
        el = E.loc[t] if t in E.index else None
        names = el.index[el.values] if el is not None else S[sigs[0]].columns
        y = fwd.loc[t + 1].reindex(names)
        X = pd.DataFrame({s: signed_rank(S[s].loc[t].reindex(names), LH[s]) if t in S[s].index else np.nan for s in sigs})
        ok = y.notna() & (X.notna().sum(axis=1) >= max(1, int(0.6 * len(sigs))))
        if ok.sum() < max(min_n, 3 * len(sigs) if len(sigs) > 1 else 15):
            continue
        Xo = X[ok].fillna(0.0).values; yo = y[ok].values
        A = np.column_stack([np.ones(len(yo)), Xo])
        b, *_ = np.linalg.lstsq(A, yo, rcond=None)
        rows[(t + 1).to_timestamp("M")] = dict(zip(["const"] + sigs, b)) | {"n": int(ok.sum())}
    return pd.DataFrame(rows).T


def summarise(G, sigs):
    out = {}
    for s in sigs:
        x = G[s].astype(float).dropna()
        out[s] = dict(ann=float(x.mean() * 12), t=perf.nw_t(x)["t"], months=int(len(x)),
                      design=float(x.loc[:"2019-12-31"].mean() * 12), holdout=float(x.loc["2020-01-01":].mean() * 12))
    return out


def run():
    res, ser = {}, {}
    for R in U:
        I = xs.inputs(R)
        E = I["E"]
        for k in list(I["S"]):
            m = E.reindex(index=I["S"][k].index, columns=I["S"][k].columns).fillna(False).astype(bool); I["S"][k] = I["S"][k].where(m)
        sigs = list(PRICE)
        if R == "US":
            F = FU.build(); I["S"].update({k: F[k] for k in FUNDC}); sigs += FUNDC
        uni = {s: summarise(fm(I, [s], min_n=15), [s])[s] for s in sigs}
        G = fm(I, sigs)
        if len(G) < 60:      # too few stocks for 10+ regressors (Denmark, ~19 names): univariate only
            res[R] = dict(uni=uni, multi=None, n_med=None, months=0); print(R, "univariate only", flush=True); continue
        multi = summarise(G, sigs)
        res[R] = dict(uni=uni, multi=multi, n_med=int(G["n"].median()), months=int(len(G)))
        ser[R] = G
        print(R, {s: round(multi[s]["t"], 1) for s in sigs}, flush=True)
    # pooled across markets: average multivariate slope series (price signals present in all six)
    pooled = {}
    for s in PRICE:
        df = pd.DataFrame({R: ser[R][s].astype(float) for R in ser}).dropna()
        x = df.mean(axis=1); C = df.corr().values
        pooled[s] = dict(ann=float(x.mean() * 12), t=perf.nw_t(x)["t"], pos=int((df.mean() > 0).sum()), n=int(df.shape[1]), neff=float(df.shape[1] ** 2 / C.sum()))
    res["pooled"] = pooled
    # US: each fundamental composite alone on top of the price signals (separates it from the other fundamentals)
    I = xs.inputs("US"); E = I["E"]
    for k in list(I["S"]):
        m = E.reindex(index=I["S"][k].index, columns=I["S"][k].columns).fillna(False).astype(bool); I["S"][k] = I["S"][k].where(m)
    F = FU.build(); I["S"].update({k: F[k] for k in FUNDC})
    res["us_one_at_a_time"] = {}
    for f in FUNDC:
        G = fm(I, PRICE + [f]); sm = summarise(G, PRICE + [f])
        res["us_one_at_a_time"][f] = dict(fund=sm[f], mom=sm["mom"])
        print("US +", f, round(sm[f]["t"], 2), "mom", round(sm["mom"]["t"], 2), flush=True)
    res["labels"] = LAB; res["price"] = PRICE; res["fund"] = FUNDC
    json.dump(res, open(os.path.join(RES, "fmb.json"), "w"), indent=1, default=float)
    pd.to_pickle(ser, os.path.join(RES, "fmb.pkl"))
    return res


if __name__ == "__main__":
    r = run()
    print("pooled", {s: (round(v["ann"] * 100, 2), round(v["t"], 2), v["pos"]) for s, v in r["pooled"].items()})
    for s in FUNDC:
        print(s, round(r["US"]["uni"][s]["t"], 2), round(r["US"]["multi"][s]["t"], 2))
