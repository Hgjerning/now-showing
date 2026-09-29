# -*- coding: utf-8 -*-
"""FS19 parts B (stress episodes, momentum crashes) and C (sector neutrality), planning/PREREG_FS19.md.
Writes results/fs19.json and results/fs19.pkl."""
import json
import os
import sys

import numpy as np
import pandas as pd

import fs18
import perf
import sectors
import xs

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; POOL = ["US", "EU", "UK", "DK", "SC"]
EPIS = {"2015–16 sell-off": ("2015-06", "2016-02"), "Q4 2018": ("2018-10", "2018-12"), "COVID crash": ("2020-02", "2020-03"),
        "COVID rebound": ("2020-04", "2020-12"), "2022 rate shock": ("2022-01", "2022-09")}
F = os.path.join(RES, "fs19.json")


def cum(s, a, b):
    x = s.loc[a:b].dropna(); return float((1 + x).prod() - 1) if len(x) else None


def dm(mom, mkt):
    """Daniel-Moskowitz: mom = a + b1 bear + b2 mkt + b3 bear*mkt; bear = past-24m market cum return < 0 (lagged)."""
    past = (1 + mkt).rolling(24).apply(np.prod, raw=True).shift(1) - 1
    d = pd.concat([mom, mkt, (past < 0).astype(float).where(past.notna())], axis=1, keys=["y", "m", "bear"]).dropna()
    X = np.column_stack([np.ones(len(d)), d.bear, d.m, d.bear * d.m]); y = d.y.values
    b, *_ = np.linalg.lstsq(X, y, rcond=None); u = y - X @ b; n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X); Xu = X * u[:, None]; S = Xu.T @ Xu / n
    for L in range(1, 7):
        G = Xu[L:].T @ Xu[:-L] / n; S += (1 - L / 7) * (G + G.T)
    se = np.sqrt(np.diag(n * XtXi @ S @ XtXi))
    return dict(n=int(n), bear_months=int(d.bear.sum()), b_bear_mkt=float(b[3]), t_bear_mkt=float(b[3] / se[3]), b_mkt=float(b[2]), t_mkt=float(b[2] / se[2]))


def partB():
    ser = pd.read_pickle(os.path.join(RES, "fs18.pkl")); out = {"episodes": {}, "dm": {}}; keep = {}
    for R in U:
        I, nets, turn = fs18.books(R); N = nets[5e7]; d = ser[(R, 5e7)]
        mk = d.market_ex + d.rf; port = d.portfolio_ex + d.rf
        books = {"market": mk, "low beta": N["low beta"], "12-1 momentum": N["12-1 momentum"], "overlay": d.overlay, "market + overlay": port}
        out["episodes"][R] = {e: {k: cum(v, a, b) for k, v in books.items()} for e, (a, b) in EPIS.items()}
        ew = pd.Series({t.to_timestamp("M"): v for t, v in I["ew"].items()})
        out["dm"][R] = dm(N["12-1 momentum"].dropna(), ew)
        keep[R] = books
        print("B", R, out["dm"][R], flush=True)
    A = pd.read_pickle(os.path.join(RES, "battery_art.pkl")); ys, xs_ = [], []
    for R in ["US_A", "EU_A", "UK_A", "DK_A"]:
        I = xs.inputs(R); ew = pd.Series({t.to_timestamp("M"): v for t, v in I["ew"].items()})
        m = A[R]["mom"]["bn_net"].dropna(); out["dm"][R] = dm(m, ew)
        past = (1 + ew).rolling(24).apply(np.prod, raw=True).shift(1) - 1
        print("B", R, out["dm"][R], flush=True)
        ys.append((m, ew))
    # pooled ART: stack the four regions (same regression, one sample)
    y = pd.concat([a.reset_index(drop=True) for a, b in ys]); rows = []
    for m, ew in ys:
        past = (1 + ew).rolling(24).apply(np.prod, raw=True).shift(1) - 1
        d = pd.concat([m, ew, (past < 0).astype(float).where(past.notna())], axis=1, keys=["y", "m", "bear"]).dropna(); rows.append(d)
    D = pd.concat(rows); X = np.column_stack([np.ones(len(D)), D.bear, D.m, D.bear * D.m]); b, *_ = np.linalg.lstsq(X, D.y.values, rcond=None)
    u = D.y.values - X @ b; XtXi = np.linalg.inv(X.T @ X); V = XtXi @ ((X * u[:, None]).T @ (X * u[:, None])) @ XtXi
    out["dm"]["ART pooled"] = dict(n=int(len(D)), bear_months=int(D.bear.sum()), b_bear_mkt=float(b[3]), t_bear_mkt=float(b[3] / np.sqrt(V[3, 3])), b_mkt=float(b[2]), t_mkt=float(b[2] / np.sqrt(V[2, 2])), se="White (stacked panel)")
    print("B ART pooled", out["dm"]["ART pooled"], flush=True)
    return out, keep


def neutral(S, sec, how):
    s = S.copy(); g = pd.Series({c: sec.get(c, "UNCL") for c in s.columns})
    T = s.T
    if how == "rank":
        return T.groupby(g).rank(pct=True).T.where(S.notna())
    return T.groupby(g).transform("mean").T.where(S.notna())


def partC():
    sec = sectors.sector_map(); out = {"markets": {}}; keep = {}
    for R in U:
        I = xs.inputs(R); res = {}
        cols = I["S"]["beta"].loc["2013":].dropna(how="all", axis=1).columns
        res["coverage"] = float(np.mean([c in sec for c in cols]))
        nets = {}
        for name, sig, lh in [("low beta", "beta", False), ("12-1 momentum", "mom", True)]:
            I["S"][sig + "_sn"] = neutral(I["S"][sig], sec, "rank"); I["S"][sig + "_sc"] = neutral(I["S"][sig], sec, "mean")
            for var, k in (("raw", sig), ("sector-neutral", sig + "_sn"), ("sector component", sig + "_sc")):
                P = xs.run(I, k, lh, beta_neutral=True); nets[(name, var)] = P.ls_net
                res[f"{name} | {var}"] = dict(ann=float(P.ls_net.mean() * 12), t=perf.nw_t(P.ls_net.dropna())["t"], sharpe=perf.sharpe(P.ls_net.dropna()))
        for var in ("raw", "sector-neutral", "sector component"):
            sl = pd.concat([nets[("low beta", var)], nets[("12-1 momentum", var)]], axis=1).mean(axis=1).dropna(); nets[("shortlist", var)] = sl
            res[f"shortlist | {var}"] = dict(ann=float(sl.mean() * 12), t=perf.nw_t(sl)["t"], sharpe=perf.sharpe(sl))
        for name in ("low beta", "12-1 momentum", "shortlist"):
            dlt = (nets[(name, "sector-neutral")] - nets[(name, "raw")]).dropna()
            res[f"{name} | difference"] = dict(ann=float(dlt.mean() * 12), t=perf.nw_t(dlt)["t"], corr=float(nets[(name, "sector-neutral")].corr(nets[(name, "raw")])))
        out["markets"][R] = res; keep[R] = nets
        print("C", R, round(res["coverage"], 2), {k: round(v["ann"], 4) for k, v in res.items() if isinstance(v, dict) and k.startswith("shortlist")}, flush=True)
    for var in ("raw", "sector-neutral"):
        p = pd.DataFrame({R: keep[R][("shortlist", var)] for R in POOL}).mean(axis=1).dropna()
        out[f"pooled | {var}"] = dict(ann=float(p.mean() * 12), t=perf.nw_t(p)["t"], sharpe=perf.sharpe(p), start=str(p.index[0].date()))
    pr, ps = out["pooled | raw"], out["pooled | sector-neutral"]
    out["passed"] = bool(ps["t"] > 2 and ps["ann"] >= 0.5 * pr["ann"])
    print("PRIMARY", ps, "raw", pr, "passed", out["passed"])
    return out, keep


def main(parts):
    out = json.load(open(F)) if os.path.exists(F) else {}
    pk = os.path.join(RES, "fs19.pkl"); ser = pd.read_pickle(pk) if os.path.exists(pk) else {}
    for p in parts:
        o, k = {"B": partB, "C": partC}[p](); out[p] = o; ser[p] = k
        json.dump(out, open(F, "w"), indent=1, default=float); pd.to_pickle(ser, pk)


if __name__ == "__main__":
    main(sys.argv[1:] or ["C", "B"])
