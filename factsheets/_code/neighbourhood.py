# -*- coding: utf-8 -*-
"""360° neighbourhood of a factor: likeness, mirror, cousins, decomposition, conditioning.

For a target signal (e.g. MAX) on each of the six point-in-time universes:
  A. characteristic likeness: average monthly cross-sectional Spearman correlation between signals
  B. return likeness: correlation of the monthly top-minus-bottom (L/S) returns
  C. performance of every neighbour's L/S (ann. mean, NW t, beta and CAPM alpha vs the EW universe)
  D. mirror test: independent 3x3 double sort target x mirror (universes with >= 60 names)
  E. spanning: target L/S regressed on the neighbours' L/S + market (and the mirror on the target)
  F. conditioning: L/S in up vs down market months and in high vs low market-volatility months
  G. horizon: L/S in months t+1, t+2..3, t+4..6
All L/S are equal-weighted top quantile minus bottom quantile (deciles >= 100 names, quintiles 50-99, terciles < 50),
gross of costs, Feb 2013 - Aug 2026. Signs are raw: e.g. the MAX L/S is 'most lottery-like minus calmest'.
"""
import json
import os

import numpy as np
import pandas as pd

import data
import perf
import signals as SG

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
U = data.REGIONS
START, END = pd.Period("2013-01"), pd.Period("2026-07")     # formation months -> holding Feb 2013 .. Aug 2026


def nq(n):
    return 10 if n >= 100 else (5 if n >= 50 else 3)


def ls_series(S, fwd, sig, lag=1):
    x = S[sig]; out = {}
    months = [t for t in x.index if START <= t <= END]
    q = nq(np.median([x.loc[t].notna().sum() for t in months]))
    for t in months:
        s = x.loc[t].dropna()
        if len(s) < 15 or (t + lag) not in fwd.index:
            continue
        pct = s.rank(pct=True, method="first")
        r = fwd.loc[t + lag, s.index].fillna(0)
        out[(t + 1).to_timestamp("M")] = float(r[pct > 1 - 1 / q].mean() - r[pct <= 1 / q].mean())
    return pd.Series(out)


def char_corr(S, sigs):
    months = [t for t in S[sigs[0]].index if START <= t <= END]
    acc = []
    for t in months[::3]:                              # quarterly sample keeps it fast; plenty of observations
        df = pd.DataFrame({k: S[k].loc[t] for k in sigs}).dropna()
        if len(df) >= 15:
            acc.append(df.rank().corr().values)
    return pd.DataFrame(np.nanmean(acc, axis=0), index=sigs, columns=sigs)


def double_sort(S, fwd, a, b, k=3):
    months = [t for t in S[a].index if START <= t <= END]
    cells = np.full((k, k, len(months)), np.nan)
    for i, t in enumerate(months):
        df = pd.DataFrame({"a": S[a].loc[t], "b": S[b].loc[t]}).dropna()
        if len(df) < 9 * k or (t + 1) not in fwd.index:
            continue
        ia = pd.qcut(df.a.rank(method="first"), k, labels=False); ib = pd.qcut(df.b.rank(method="first"), k, labels=False)
        r = fwd.loc[t + 1, df.index].fillna(0)
        for x in range(k):
            for y in range(k):
                m = (ia == x) & (ib == y)
                if m.sum() >= 2:
                    cells[x, y, i] = r[m].mean()
    return np.nanmean(cells, axis=2) * 12, cells


def spanning(y, X):
    d = pd.concat([y.rename("y"), X], axis=1).dropna()
    b = perf.nw_ols(d.y.values, d.drop(columns="y").values, 6) if X.shape[1] == 1 else None
    Xc = np.column_stack([np.ones(len(d)), d.drop(columns="y").values]); yy = d.y.values
    beta = np.linalg.lstsq(Xc, yy, rcond=None)[0]; u = yy - Xc @ beta; n = len(yy)
    XtXi = np.linalg.inv(Xc.T @ Xc); Xu = Xc * u[:, None]; Sm = Xu.T @ Xu / n
    for L in range(1, 7):
        G = Xu[L:].T @ Xu[:-L] / n; Sm += (1 - L / 7) * (G + G.T)
    se = np.sqrt(np.diag(n * XtXi @ Sm @ XtXi))
    cols = ["alpha"] + list(d.columns[1:])
    return dict(coef={c: float(v * (12 if c == "alpha" else 1)) for c, v in zip(cols, beta)}, t={c: float(v) for c, v in zip(cols, beta / se)},
                r2=float(1 - u @ u / ((yy - yy.mean()) @ (yy - yy.mean()))), n=n)


def run(name, target, mirror, sigs, span_on, mirror_span_on):
    out = {"target": target, "mirror": mirror, "signals": sigs, "per": {}}
    CC, RC, LSall = [], [], {}
    for R in U:
        o = SG.build(R); S, fwd, ew = o["S"], o["fwd"], o["ew"]
        ewm = pd.Series({t.to_timestamp("M"): v for t, v in ew.items()})
        L = pd.DataFrame({k: ls_series(S, fwd, k) for k in sigs}); LSall[R] = L
        mk = ewm.reindex(L.index)
        perf_ = {}
        for k in sigs:
            s = L[k].dropna(); reg = perf.nw_ols(s.values, mk.reindex(s.index).values, 6)
            perf_[k] = dict(ann=float(s.mean() * 12), t=perf.nw_t(s)["t"], sharpe=perf.sharpe(s), beta=reg["beta"], alpha=reg["alpha"] * 12, t_alpha=reg["t_alpha"],
                            up=float(s[mk.reindex(s.index) > 0].mean() * 12), down=float(s[mk.reindex(s.index) <= 0].mean() * 12))
        mv = ewm.rolling(3).std().shift(1).reindex(L.index); hi = mv > mv.median()
        for k in sigs:
            s = L[k]; perf_[k].update(hivol=float(s[hi].mean() * 12), lovol=float(s[~hi & mv.notna()].mean() * 12))
        cc = char_corr(S, sigs); CC.append(cc.values); rc = L.corr(); RC.append(rc.values)
        n_names = int(np.median([S[target].loc[t].notna().sum() for t in S[target].index if START <= t <= END]))
        ds = None
        if n_names >= 60:
            m, _ = double_sort(S, fwd, target, mirror)
            ds = m.tolist()
        hz = {}
        for lag, lab in ((1, "t+1"), (2, "t+2"), (3, "t+3"), (4, "t+4"), (6, "t+6")):
            hz[lab] = float(ls_series(S, fwd, target, lag).mean() * 12)
        sp = spanning(L[target], pd.concat([L[span_on], mk.rename("mkt")], axis=1))
        spm = spanning(L[mirror], pd.concat([L[mirror_span_on], mk.rename("mkt")], axis=1))
        out["per"][R] = dict(n=n_names, perf=perf_, char_corr=cc.round(3).to_dict(), ret_corr=rc.round(3).to_dict(), double_sort=ds, horizon=hz,
                             span_target=sp, span_mirror=spm)
        print(name, R, "n", n_names, {k: round(perf_[k]["ann"] * 100, 1) for k in sigs})
    out["char_corr_avg"] = pd.DataFrame(np.nanmean(CC, axis=0), index=sigs, columns=sigs).round(3).to_dict()
    out["ret_corr_avg"] = pd.DataFrame(np.nanmean(RC, axis=0), index=sigs, columns=sigs).round(3).to_dict()
    ds = [np.array(out["per"][R]["double_sort"]) for R in U if out["per"][R]["double_sort"] is not None]
    out["double_sort_avg"] = np.mean(ds, axis=0).tolist(); out["double_sort_universes"] = [R for R in U if out["per"][R]["double_sort"] is not None]
    pd.to_pickle(LSall, os.path.join(RES, f"nbh_{name}_ls.pkl"))
    json.dump(out, open(os.path.join(RES, f"nbh_{name}.json"), "w"), indent=1, default=float)
    return out


if __name__ == "__main__":
    import sys
    if "max" in sys.argv:
        run("max", "max1", "min1", SG.SIGNALS, ["min1", "ivol", "vol", "beta", "skew", "r1"], ["max1", "ivol", "vol", "beta", "r1"])
    if "brk" in sys.argv:
        run("brk", "brk55", "lo52", SG.SIGNALS, ["mom", "hi52", "r1", "vol", "max1"], ["brk55", "mom", "r1", "vol", "min1"])
