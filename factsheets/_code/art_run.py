# -*- coding: utf-8 -*-
"""FS15: the FS13 battery, FS13c Fama-MacBeth and FS14 procedure on the ART history (1998-2013),
unchanged, as pre-registered in planning/PREREG_FS15.md. Writes results/art_*.json/.pkl."""
import json
import os
import sys

import numpy as np
import pandas as pd

import battery as BT
import fmb as FM
import fs14 as F14
import perf
import xs

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results")
UA = ["US_A", "EU_A", "UK_A", "DK_A", "WD_A"]; M4 = ["US_A", "EU_A", "UK_A", "DK_A"]
xs.START, xs.END = pd.Period("1999-01"), pd.Period("2013-02")
FM.START, FM.END = pd.Period("1999-01"), pd.Period("2013-01")


def pooled(dfs):
    df = pd.DataFrame(dfs).dropna(); x = df.mean(axis=1); C = df.corr().values
    return dict(ann=float(x.mean() * 12), sharpe=perf.sharpe(x), t=perf.nw_t(x)["t"], pos=int((df.mean() > 0).sum()), n=int(df.shape[1]), neff=float(df.shape[1] ** 2 / C.sum()),
                s1=perf.sharpe(x.loc[:"2005-12-31"]), s2=perf.sharpe(x.loc["2006-01-01":]))


def battery():
    f = os.path.join(RES, "battery_art.pkl")
    B = pd.read_pickle(f) if os.path.exists(f) else {}
    for R in UA:
        if R not in B:
            B[R] = BT.one(R); pd.to_pickle(B, f)
    J = {R: {s: BT.stats(B[R][s]) for s in BT.SIGS} for R in UA}
    P = {s: dict(raw=pooled({R: B[R][s].ls_net for R in M4}), bn=pooled({R: B[R][s].bn_net for R in M4}),
                 lo=int(sum(J[R][s]["lo_minus_ew_sharpe"] > 0 for R in M4))) for s in BT.SIGS}
    return B, J, P


def fama_macbeth():
    res, ser = {}, {}
    for R in UA:
        I = xs.inputs(R); E = I["E"]
        for k in list(I["S"]):
            m = E.reindex(index=I["S"][k].index, columns=I["S"][k].columns).fillna(False).astype(bool); I["S"][k] = I["S"][k].where(m)
        sigs = list(FM.PRICE)
        uni = {s: FM.summarise(FM.fm(I, [s], min_n=15), [s])[s] for s in sigs}
        G = FM.fm(I, sigs)
        if len(G) < 60:
            res[R] = dict(uni=uni, multi=None); continue
        res[R] = dict(uni=uni, multi=FM.summarise(G, sigs)); ser[R] = G
    po = {}
    for s in FM.PRICE:
        df = pd.DataFrame({R: ser[R][s].astype(float) for R in ser if R != "WD_A"}).dropna(); x = df.mean(axis=1)
        po[s] = dict(ann=float(x.mean() * 12), t=perf.nw_t(x)["t"], pos=int((df.mean() > 0).sum()), n=int(df.shape[1]))
    res["pooled"] = po
    return res


def multifactor(B):
    def bat(R):
        b = B[R]
        return (pd.DataFrame({s: b[s].bn_net for s in b}).sort_index(), pd.DataFrame({s: b[s].ls_gross for s in b}).sort_index(), pd.DataFrame({s: b[s].cost for s in b}).sort_index())
    F14.battery = bat
    ser, res = {}, {}
    for R in UA:
        ret, gross, cost = bat(R); idx = ret.index
        out = {v: {} for v in F14.VARIANTS}; prev = {v: pd.Series(dtype=float) for v in F14.VARIANTS}; sel = []
        for i in range(F14.WF - 1, len(idx) - 1):
            cols, passed, kept = F14.step(ret, gross, cost, i); nxt = idx[i + 1]; r1 = ret.loc[nxt]
            sel.append(dict(month=nxt, n_pass=len(passed), n_kept=len(kept), kept=kept))
            for v in F14.VARIANTS:
                w = F14.weights(ret, i, kept, v)
                to = float(w.subtract(prev[v], fill_value=0).abs().sum()) / 2
                out[v][nxt] = (float((w * r1.reindex(w.index).fillna(0)).sum()) if len(w) else 0.0) - F14.TCOST * to; prev[v] = w
        P = pd.DataFrame(out); oos = P.index
        P["ALL-EQ"] = ret.reindex(oos).mean(axis=1)
        P["SHORT"] = ret[["beta", "mom"]].reindex(oos).mean(axis=1)
        P["MARKET"] = B[R]["mom"].ew.reindex(oos)
        S = pd.DataFrame(sel).set_index("month")
        res[R] = {c: F14.st(P[c]) for c in P.columns}
        res[R]["_sel"] = dict(kept_med=float(S.n_kept.median()), cash_months=int((S.n_kept == 0).sum()), months=int(len(S)),
                              kept_freq=(pd.Series([s for k in S.kept for s in k]).value_counts() / len(S)).round(3).to_dict())
        ser[R] = P
    def paired(a, b):
        d = pd.DataFrame({R: ser[R][a] - ser[R][b] for R in M4}).dropna(); x = d.mean(axis=1); mid = x.index[len(x) // 2]
        return dict(ann=float(x.mean() * 12), t=perf.nw_t(x)["t"], s1=float(x.loc[:mid].mean() * 12), s2=float(x.loc[mid:].iloc[1:].mean() * 12), pos=int((d.mean() > 0).sum()), split=str(mid.date()))
    res["primary"] = paired("RP", "ALL-EQ")
    res["vs_alleq"] = {v: paired(v, "ALL-EQ") for v in F14.VARIANTS}
    res["vs_short"] = {v: paired(v, "SHORT") for v in F14.VARIANTS}
    res["pooled"] = {c: F14.st(pd.DataFrame({R: ser[R][c] for R in M4}).dropna().mean(axis=1)) for c in F14.VARIANTS + ["ALL-EQ", "SHORT", "MARKET"]}
    res["variants"] = F14.VARIANTS
    res["short_vs_alleq"] = paired("SHORT", "ALL-EQ")
    x = pd.DataFrame({R: ser[R]["SHORT"] for R in M4}).dropna().mean(axis=1); m = pd.DataFrame({R: ser[R]["MARKET"] for R in M4}).dropna().mean(axis=1)
    res["short_corr_market"] = float(x.corr(m))
    return res, ser


if __name__ == "__main__" and "--fs14-only" in sys.argv:
    B, J, P = battery(); MF, ser = multifactor(B)
    json.dump(MF, open(os.path.join(RES, "art_fs14.json"), "w"), indent=1, default=str); pd.to_pickle(ser, os.path.join(RES, "art_fs14.pkl"))
    print(MF["short_vs_alleq"], MF["short_corr_market"]); sys.exit()
if __name__ == "__main__":
    B, J, P = battery()
    json.dump(dict(stats=J, pooled=P), open(os.path.join(RES, "art_battery.json"), "w"), indent=1, default=float)
    print({s: (round(P[s]["bn"]["t"], 2), P[s]["bn"]["pos"]) for s in P}, flush=True)
    FMR = fama_macbeth(); json.dump(FMR, open(os.path.join(RES, "art_fmb.json"), "w"), indent=1, default=float)
    print("FMB pooled", {s: round(v["t"], 2) for s, v in FMR["pooled"].items()}, flush=True)
    MF, ser = multifactor(B); json.dump(MF, open(os.path.join(RES, "art_fs14.json"), "w"), indent=1, default=str); pd.to_pickle(ser, os.path.join(RES, "art_fs14.pkl"))
    print("primary", MF["primary"]); print("pooled", {c: round(v["sharpe"], 2) for c, v in MF["pooled"].items()})
