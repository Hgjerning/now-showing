# -*- coding: utf-8 -*-
"""Diagnostics for FS01: why do Turtle rules fail on single stocks?

D1 Breakout event study: excess return (stock minus EW universe) after fresh 20- and 55-day breakouts, split into
   the fill day (t+1, missed by a next-close fill), t+2..5, t+6..20, t+21..60. Long and short breakouts separately.
D2 Trendiness: variance ratios VR(q) = Var(q-day)/(q Var(1-day)) for single stocks (total and idiosyncratic) and
   for the EW universe index. VR > 1 = trending, VR < 1 = mean-reverting.
D3 P&L decomposition of the headline book by side, system, exit reason and cost.
Diagnostics are computed on the DESIGN window 2013-2019; the fixes are judged on the HOLDOUT 2020-2026.
"""
import json
import os

import numpy as np
import pandas as pd

import data

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
DESIGN = ("2013-01-01", "2019-12-31")
WIN = {"t+1 (fill day)": (1, 1), "t+2..5": (2, 5), "t+6..20": (6, 20), "t+21..60": (21, 60)}


def event_study(ret, elig, L, lo, hi):
    P = (1 + ret.fillna(0)).cumprod().where(ret.notna().cumsum() > 0).ffill()
    mkt = ret.where(elig).mean(axis=1)
    ex = ret.sub(mkt, axis=0).fillna(0)
    C = np.vstack([np.zeros(ex.shape[1]), np.log1p(ex.clip(lower=-0.99)).cumsum().to_numpy()])   # C[k] = sum up to row k-1
    hiL = P.shift(1).rolling(L, min_periods=L).max(); loL = P.shift(1).rolling(L, min_periods=L).min()
    BL = (P > hiL) & elig; BS = (P < loL) & elig
    fresh_l = BL & ~BL.shift(1, fill_value=False).rolling(5, min_periods=1).max().astype(bool)
    fresh_s = BS & ~BS.shift(1, fill_value=False).rolling(5, min_periods=1).max().astype(bool)
    sel = (ret.index >= lo) & (ret.index <= hi)
    out = {}
    T = len(ret)
    for name, F in (("long", fresh_l), ("short", fresh_s)):
        ii, jj = np.where(F.to_numpy() & sel[:, None])
        res = {}
        for w, (a, b) in WIN.items():
            ok = ii + b < T
            v = C[ii[ok] + b + 1, jj[ok]] - C[ii[ok] + a, jj[ok]]
            m = float(np.expm1(v).mean()); se = float(np.expm1(v).std() / np.sqrt(len(v)))
            res[w] = dict(mean=m, t=m / se, n=int(ok.sum()))
        out[name] = res
    return out


def index_event(ret, elig, L, lo, hi):
    m = ret.where(elig).mean(axis=1).loc["2012":]
    P = (1 + m).cumprod(); hiL = P.shift(1).rolling(L).max(); loL = P.shift(1).rolling(L).min()
    base = m.loc[lo:hi].mean()
    out = {}
    for name, F in (("long", P > hiL), ("short", P < loL)):
        idx = np.where(F.loc[lo:hi].to_numpy())[0] + m.index.get_loc(m.loc[lo:].index[0])
        res = {}
        for w, (a, b) in WIN.items():
            v = [m.iloc[i + a:i + b + 1].sum() - base * (b - a + 1) for i in idx if i + b < len(m)]
            res[w] = dict(mean=float(np.mean(v)), n=len(v))
        out[name] = res
    return out


def vr(x, q):
    x = x.dropna()
    if len(x) < 5 * q:
        return np.nan
    s1 = x.var(); sq = x.rolling(q).sum().iloc[q - 1::q].var()   # non-overlapping
    return float(sq / (q * s1))


def variance_ratios(ret, elig, lo, hi):
    r = ret.where(elig).loc[lo:hi]; m = r.mean(axis=1)
    idio = r.sub(m, axis=0)
    out = {}
    for q in (5, 20, 60):
        out[q] = dict(stock=float(np.nanmedian([vr(r[c], q) for c in r.columns])),
                      idio=float(np.nanmedian([vr(idio[c], q) for c in idio.columns])),
                      index=vr(m, q))
    return out


def pnl_decomp(R):
    tl = pd.read_csv(os.path.join(RES, f"turtle_trades_{R}.csv"), parse_dates=["entry", "exit"])
    d = tl[(tl.exit >= DESIGN[0]) & (tl.exit <= DESIGN[1])]
    g = d.groupby(["system", "dir"]).pnl_pct.agg(["count", "sum"])
    rs = d.groupby("reason").pnl_pct.agg(["count", "sum", "mean"])
    return dict(by_side={f"{a}_{b}": dict(n=int(v["count"]), pnl=float(v["sum"])) for (a, b), v in g.iterrows()},
                by_reason={k: dict(n=int(v["count"]), pnl=float(v["sum"]), mean=float(v["mean"])) for k, v in rs.iterrows()})


if __name__ == "__main__":
    out = {}
    for R in data.REGIONS:
        o = data.load(R)
        out[R] = dict(ev55=event_study(o["ret"], o["elig"], 55, *DESIGN), ev20=event_study(o["ret"], o["elig"], 20, *DESIGN),
                      idx55=index_event(o["ret"], o["elig"], 55, *DESIGN), vr=variance_ratios(o["ret"], o["elig"], *DESIGN), pnl=pnl_decomp(R))
        e = out[R]["ev55"]
        print(R, {s: {w: f"{v['mean']*100:+.2f}% t{v['t']:.1f}" for w, v in e[s].items()} for s in e}, "VR", {q: {k: round(x, 2) for k, x in v.items()} for q, v in out[R]["vr"].items()})
    json.dump(out, open(os.path.join(RES, "turtle_diagnostics.json"), "w"), indent=1)
