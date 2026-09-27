# -*- coding: utf-8 -*-
"""Runs one sort strategy (FS03-FS12) on the six universes and writes results/xs_<code>.json + series pickle."""
import json
import os
import sys

import numpy as np
import pandas as pd

import analyse
import data
import fix_analysis as FA
import library
import neighbourhood as NB
import perf
import specs
import xs

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
U = data.REGIONS
DES, HOL = ("2013-01-01", "2019-12-31"), ("2020-01-01", "2026-08-31")
END_M = "2026-08-31"


def run(code):
    sp = specs.S[code]; sig, lh, con, mir = sp["sig"], sp["long_high"], sp["construction"], sp["mirror"]
    out = dict(code=code, per={}); ser = {}
    for R in U:
        I = xs.inputs(R); lib = library.build(R)
        lad = xs.ladder(I, sig, lh, con)
        P = lad["X0 baseline"]; q = P.attrs["q"]
        ew = P.ew; sw = lib["sw"].reindex(P.index)
        books = {"L/S (net)": P.ls_net, "Long-only (net)": P.good_net, "Good leg (gross)": P.good, "Bad leg (gross)": P.bad, "EW universe": ew, "Size-weighted universe": sw}
        st = {k: analyse.metrics(None, monthly=v.dropna(), bench_m=ew) for k, v in books.items()}
        for k, v in books.items():
            st[k]["calendar"] = {int(y): float(x) for y, x in perf.calendar_table(v.dropna()).items()}
        att = {"L/S (net)": analyse.attribution(P.ls_net, R), "Long-only (net)": analyse.attribution(P.good_net, R)}
        # diagnostics (design window)
        d = P.loc[DES[0]:DES[1]]
        reg = perf.nw_ols(d.ls_gross.values, d.ew.values, 6)
        diag = dict(beta=reg["beta"], beta_drag=float(reg["beta"] * d.ew.mean() * 12), alpha_gross=float(reg["alpha"] * 12), cost=float(d.cost.mean() * 12),
                    gross=float(d.ls_gross.mean() * 12), good_vs_ew=float((d.good - d.ew).mean() * 12), ew_vs_bad=float((d.ew - d.bad).mean() * 12),
                    to=float((d.to_good + d.to_bad).mean()), worst=[(str(i.date())[:7], float(v)) for i, v in d.ls_net.nsmallest(3).items()],
                    first_half=float(P.ls_gross.loc[:"2019-12-31"].mean() * 12), second_half=float(P.ls_gross.loc["2020-01-01":].mean() * 12))
        # ladder
        L = {k: {"design": FA.stats(v.ls_net.loc[DES[0]:DES[1]], v.ew), "holdout": FA.stats(v.ls_net.loc[HOL[0]:HOL[1]], v.ew), "cost": float(v.cost.mean() * 12), "to": float((v.to_good + v.to_bad).mean())} for k, v in lad.items()}
        # 360 view
        S = I["S"]; fwd = I["fwd"]
        cc = library.char_corr(S, library.LIB) if False else lib["cc"]
        LL = lib["L"]
        rc = LL.corr()
        near = rc[sig].drop(sig).abs().sort_values(ascending=False).index[:5].tolist()
        mk = lib["ew"].reindex(LL.index)
        span = NB.spanning(LL[sig], pd.concat([LL[near], mk.rename("mkt")], axis=1))
        ds = None
        if int(P.n_good.median() * q) >= 60:
            m_, _ = NB.double_sort(S, fwd, sig, mir); ds = m_.tolist()
        hz = {f"t+{k}": float(library.ls_series(S, fwd, sig, k).mean() * 12) for k in (1, 2, 3, 6)}
        # classification: correlations with JKP/French themes, TM gamma, tails
        cls = FA.classify({"x": {R: P.ls_net}, "_EW": {R: ew}})["x"][R] if False else None
        F = FA.FSET[R](); j = pd.concat([P.ls_net.rename("y"), F], axis=1, join="inner").dropna()
        corr = j.corr()["y"].drop("y")
        X = np.column_stack([np.ones(len(P)), ew.values, ew.values ** 2]); b = np.linalg.lstsq(X, P.ls_net.values, rcond=None)[0]
        u = P.ls_net.values - X @ b; n = len(u); XtXi = np.linalg.inv(X.T @ X); Xu = X * u[:, None]; Sm = Xu.T @ Xu / n
        for Lg in range(1, 7):
            G = Xu[Lg:].T @ Xu[:-Lg] / n; Sm += (1 - Lg / 7) * (G + G.T)
        se = np.sqrt(np.diag(n * XtXi @ Sm @ XtXi))
        bad_m = ew <= ew.quantile(0.1); good_m = ew >= ew.quantile(0.9)
        cls = dict(corr=corr.to_dict(), top=[(k, float(v)) for k, v in corr.sort_values(key=abs, ascending=False).head(3).items()], tm_gamma=float(b[2]), tm_t=float(b[2] / se[2]),
                   worst_mkt=float(P.ls_net[bad_m].mean()), best_mkt=float(P.ls_net[good_m].mean()), skew=float(P.ls_net.skew()))
        rec = P[["n_good", "n_bad", "to_good", "to_bad", "good", "bad", "ls_gross", "ls_net"]]
        rec.to_csv(os.path.join(RES, f"xs_{code}_record_{R}.csv"))
        cur = S[sig].loc[xs.END + 1].dropna() if (xs.END + 1) in S[sig].index else S[sig].iloc[-1].dropna()
        cur = cur.sort_values(ascending=not lh)
        out["per"][R] = dict(q=q, n=int(S[sig].loc[xs.START:xs.END].notna().sum(axis=1).median()), stats=st, attribution=att, diag=diag, ladder=L,
                             nbh=dict(near=near, ret_corr={k: float(rc.loc[k, sig]) for k in library.LIB}, char_corr={k: float(cc.loc[k, sig]) for k in library.LIB},
                                      char_corr_mirror={k: float(cc.loc[k, mir]) for k in library.LIB}, span=span, double_sort=ds, horizon=hz,
                                      up=float(lib["stats"][sig]["up"]), down=float(lib["stats"][sig]["down"])),
                             cls=cls, current_good=cur.head(10).index.tolist(), current_bad=cur.tail(10).index.tolist()[::-1])
        ser[R] = dict(books=pd.DataFrame(books), ladder={k: v.ls_net for k, v in lad.items()}, ew=ew)
        print(code, R, "L/S net %.1f%% t %.2f | LO %.1f%% | EW %.1f%%" % (st["L/S (net)"]["ann_mean"] * 100, st["L/S (net)"]["t_mean"], st["Long-only (net)"]["cagr"] * 100, st["EW universe"]["cagr"] * 100))
    # pooled ladder tests
    steps = list(ser[U[0]]["ladder"].keys()); M = {s: pd.DataFrame({R: ser[R]["ladder"][s] for R in U}) for s in steps}
    EWd = pd.DataFrame({R: ser[R]["ew"] for R in U})
    out["steps"] = steps
    out["pooled"] = {steps[i]: {"design": FA.pooled_test(M[steps[i]].fillna(0), M[steps[i - 1]].fillna(0), *DES), "holdout": FA.pooled_test(M[steps[i]].fillna(0), M[steps[i - 1]].fillna(0), *HOL)} for i in range(1, len(steps))}
    out["avg_holdout"] = {s: FA.stats(M[s].mean(axis=1).loc[HOL[0]:HOL[1]], EWd.mean(axis=1)) for s in steps}
    out["avg_design"] = {s: FA.stats(M[s].mean(axis=1).loc[DES[0]:DES[1]], EWd.mean(axis=1)) for s in steps}
    dsl = [np.array(out["per"][R]["nbh"]["double_sort"]) for R in U if out["per"][R]["nbh"]["double_sort"] is not None]
    out["double_sort_avg"] = np.mean(dsl, axis=0).tolist() if dsl else None
    out["double_sort_universes"] = [R for R in U if out["per"][R]["nbh"]["double_sort"] is not None]
    pd.to_pickle(ser, os.path.join(RES, f"xs_{code}.pkl"))
    json.dump(out, open(os.path.join(RES, f"xs_{code}.json"), "w"), indent=1, default=float)
    return out


if __name__ == "__main__":
    for c in sys.argv[1:]:
        run(c)
