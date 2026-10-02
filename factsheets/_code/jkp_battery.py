# -*- coding: utf-8 -*-
"""JKP factor battery: 153 published factors (Jensen, Kelly & Pedersen 2023), signed as in the original papers,
capped value-weighted long/short, USD. Segments: USA, GBR, DNK, World ex US (disjoint from USA), World.
Window 2013-01..2025-12 (JKP ends Dec 2025). Compares with each factor's pre-2013 history in the same segment."""
import json
import os

import numpy as np
import pandas as pd

import perf

HERE = os.path.dirname(os.path.abspath(__file__)); FAC = os.path.join(HERE, "..", "factors"); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results")
SEG = {"usa": "US", "gbr": "UK", "dnk": "Denmark", "world_ex_us": "World ex US", "world": "World"}
W0, W1 = "2013-01-01", "2025-12-31"


def load():
    F = {s: pd.read_csv(os.path.join(FAC, f"jkp_{s}_factors_monthly.csv"), index_col=0, parse_dates=True) for s in SEG}
    cl = pd.read_csv(os.path.join(FAC, "jkp_cluster_labels.csv")).set_index("characteristic")["cluster"]
    return F, cl


def fstats(x):
    x = x.dropna()
    if len(x) < 36:
        return None
    return dict(ann=float(x.mean() * 12), sharpe=perf.sharpe(x), t=perf.nw_t(x)["t"], n=int(len(x)))


def bh(p, q=0.05):
    """Benjamini-Hochberg: boolean array of discoveries."""
    p = np.asarray(p); o = np.argsort(p); m = len(p); thr = q * np.arange(1, m + 1) / m
    ok = p[o] <= thr; k = np.max(np.where(ok)[0]) + 1 if ok.any() else 0
    d = np.zeros(m, bool); d[o[:k]] = True; return d


def build():
    from scipy import stats as sst
    F, cl = load(); facs = [c for c in F["usa"].columns if c in cl.index]
    rows = []
    for s in SEG:
        f = F[s]
        for k in facs:
            a = fstats(f[k].loc[W0:W1]); b = fstats(f[k].loc[:"2012-12-31"])
            if a:
                rows.append(dict(seg=s, factor=k, cluster=cl[k], **a, pre_ann=b["ann"] if b else np.nan, pre_sharpe=b["sharpe"] if b else np.nan, pre_t=b["t"] if b else np.nan))
    T = pd.DataFrame(rows)
    T["p"] = 2 * (1 - sst.norm.cdf(T.t.abs()))
    T["bh"] = False
    for s in SEG:
        m = T.seg == s; T.loc[m, "bh"] = bh(T.loc[m, "p"].values)
    # pooled across the four disjoint segments (USA, GBR, DNK, World ex US): equal-weight average series; its t includes the co-movement
    DIS = ["usa", "gbr", "dnk", "world_ex_us"]; pooled = {}
    for k in facs:
        df = pd.DataFrame({s: F[s][k] for s in DIS}).loc[W0:W1].dropna()
        if len(df) < 36:
            continue
        C = df.corr().values; neff = len(DIS) ** 2 / C.sum()
        a = fstats(df.mean(axis=1)); pre = pd.DataFrame({s: F[s][k] for s in DIS}).loc[:"2012-12-31"].mean(axis=1)
        pooled[k] = dict(cluster=cl[k], **a, neff=float(neff), pos=int((df.mean() > 0).sum()), pre_ann=float(pre.dropna().mean() * 12), mean_corr=float(C[np.triu_indices(len(DIS), 1)].mean()))
    P = pd.DataFrame(pooled).T
    P["p"] = 2 * (1 - sst.norm.cdf(P.t.astype(float).abs())); P["bh"] = bh(P.p.values); P["hlz"] = P.t.astype(float) > 3.0
    # clusters: equal-weight theme portfolios per segment
    CL = {}
    for s in SEG:
        f = F[s].loc[W0:W1]
        for c in sorted(cl.unique()):
            ks = [k for k in facs if cl[k] == c and f[k].notna().sum() > 36]
            x = f[ks].mean(axis=1); st = fstats(x); pre = fstats(F[s][ks].loc[:"2012-12-31"].mean(axis=1))
            CL[(s, c)] = dict(**st, pre_sharpe=pre["sharpe"] if pre else np.nan)
    CLdf = pd.DataFrame(CL).T
    # agreement across segments: Spearman correlation of factor Sharpe ratios
    SH = T.pivot(index="factor", columns="seg", values="sharpe")[list(SEG)]
    agree = SH.corr(method="spearman")
    # co-movement of the same factor across segments
    co = {}
    for a_ in SEG:
        for b_ in SEG:
            if a_ < b_:
                co[f"{a_}-{b_}"] = float(np.nanmedian([F[a_][k].loc[W0:W1].corr(F[b_][k].loc[W0:W1]) for k in facs]))
    out = dict(T=T, P=P, CL=CLdf, agree=agree, co=co, facs=facs, cl=cl, SH=SH)
    pd.to_pickle(out, os.path.join(RES, "battery_jkp.pkl"))
    T.to_csv(os.path.join(RES, "battery_jkp_factors.csv"), index=False); P.to_csv(os.path.join(RES, "battery_jkp_pooled.csv"))
    return out


if __name__ == "__main__":
    o = build()
    P = o["P"]
    print(P.sort_values("t", ascending=False).head(15)[["cluster", "ann", "sharpe", "t", "pos", "neff", "bh", "pre_ann"]])
    print("BH discoveries", int(P.bh.sum()), "HLZ t>3", int(P.hlz.sum()), "of", len(P))
    print(o["agree"].round(2)); print(o["co"])
    print(o["CL"]["sharpe"].unstack().round(2))
