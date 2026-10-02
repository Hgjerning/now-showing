# -*- coding: utf-8 -*-
"""FS02 diagnostics and within-strategy fixes for the MAX (lottery) factor.

Diagnostics (design window Feb 2013 - Dec 2019):
  D1 beta drag: L/S = alpha + beta x EW; how much of the loss is the market
  D2 cost drag from turnover
  D3 what MAX measures in large caps: cross-sectional rank correlation of MAX with 60-day volatility and with beta
  D4 signal horizon: L/S spread in months t+1, t+2..3, t+4..6 after formation
Fixes, stacked in a pre-declared order, each one trial, judged on the HOLDOUT Jan 2020 - Aug 2026:
  L1 beta-neutral legs: each leg scaled by 1 / its ex-ante beta (Frazzini & Pedersen 2014 construction)
  L2 + signal = MAX5 / 21-day volatility (JKP rmax5_rvol_21d): lottery-ness net of plain volatility
  L3 + turnover buffer: enter the extreme 1/q, keep until outside the extreme min(3/q, 1/2)
"""
import json
import os

import numpy as np
import borrow as BR
import pandas as pd

import data

RES = os.environ.get("FS_RESULTS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
COST = 0.0010
CACHE = data.CACHE   # 2026-10-01: follows data.py


def monthly_inputs(R):
    f = os.path.join(CACHE, f"lotfix_{R}.pkl")
    if os.path.exists(f):
        out = pd.read_pickle(f); out["R"] = R; return out
    o = data.load(R); r, e = o["ret"], o["elig"]
    mkt = r.where(e).mean(axis=1)
    per = r.index.to_period("M")
    g = r.groupby(per); cnt = g.count()
    max1 = g.max().where(cnt >= 15)
    max5 = g.apply(lambda d: d.apply(lambda c: c.nlargest(5).mean() if c.notna().sum() >= 5 else np.nan)).where(cnt >= 15)
    vol21 = g.std().where(cnt >= 15)
    vol60 = r.rolling(60, min_periods=40).std().groupby(per).last()
    # 252-day beta vs EW universe
    m = mkt.to_numpy()[:, None]; x = r
    ex = x.rolling(252, min_periods=200).mean(); em = mkt.rolling(252, min_periods=200).mean()
    exy = (x.fillna(0) * m).where(x.notna()).rolling(252, min_periods=200).mean(); vm = mkt.rolling(252, min_periods=200).var(ddof=0)
    beta = exy.sub(ex.mul(em, axis=0)).div(vm, axis=0).groupby(per).last()
    fwd = g.apply(lambda d: (1 + d.fillna(0)).prod() - 1).where(cnt > 0)
    E = data.month_elig(e)
    ew = mkt.groupby(per).apply(lambda s: (1 + s).prod() - 1)
    out = dict(max1=max1, max5vol=max5 / vol21, vol60=vol60, beta=beta, fwd=fwd, E=E, ew=ew)
    pd.to_pickle(out, f); out["R"] = R
    return out


def build(I, signal="max1", beta_neutral=False, buffer=False, start="2012-12", end="2026-07"):
    S, fwd, E, B = I[signal], I["fwd"], I["E"], I["beta"]
    months = [t for t in S.index if pd.Period(start) <= t <= pd.Period(end)]
    ns = [int(S.loc[t].where(E.loc[t]).notna().sum()) for t in months]
    nmed = np.median(ns); q = 10 if nmed >= 100 else (5 if nmed >= 50 else 3)
    keep = min(3 / q, 0.5)
    held = {"low": set(), "high": set()}; prevw = {"low": pd.Series(dtype=float), "high": pd.Series(dtype=float)}
    rows = []
    for t in months:
        nx = t + 1
        if nx not in fwd.index:
            break
        s = S.loc[t].where(E.loc[t]).dropna()
        if len(s) < 15:
            continue
        pct = s.rank(pct=True, method="first")
        r = fwd.loc[nx, s.index].fillna(0.0)
        legs = {}
        for leg, inn, out_ in (("low", pct <= 1 / q, pct <= keep), ("high", pct > 1 - 1 / q, pct > 1 - keep)):
            names = set(s.index[inn])
            if buffer:
                names |= {n for n in held[leg] if n in s.index and out_[n]}
            names = sorted(names); held[leg] = set(names)
            w = pd.Series(1 / len(names), index=names)
            b = float(B.loc[t, names].clip(0.2, 3).mean()) if beta_neutral else 1.0
            if beta_neutral and not np.isfinite(b):
                b = 1.0
            w = w / b
            to = float(w.subtract(prevw[leg], fill_value=0).abs().sum()) / 2; prevw[leg] = w
            legs[leg] = dict(ret=float((w * r[names]).sum()), to=to, n=len(names), beta=b, w=w)
        ls = legs["low"]["ret"] - legs["high"]["ret"]
        cost = COST * 2 * (legs["low"]["to"] + legs["high"]["to"]); bf = BR.monthly_fee(I.get("R"), t, legs["high"]["w"])
        fin = BR.financing(t, float(legs["low"]["w"].sum() - legs["high"]["w"].sum()))
        rows.append(dict(month=nx.to_timestamp("M"), ls_gross=ls, ls_net=ls - cost - bf - fin, cost=cost, borrow=bf, fin=fin, to=legs["low"]["to"] + legs["high"]["to"],
                         n_low=legs["low"]["n"], n_high=legs["high"]["n"], b_low=legs["low"]["beta"], b_high=legs["high"]["beta"], ew=float(I["ew"].loc[nx])))
    return pd.DataFrame(rows).set_index("month")


def diagnostics(R, I):
    S, E, fwd = I["max1"], I["E"], I["fwd"]
    months = [t for t in S.index if pd.Period("2012-12") <= t <= pd.Period("2019-11")]
    rc_vol, rc_beta, hz = [], [], {"t+1": [], "t+2..3": [], "t+4..6": []}
    for t in months:
        s = S.loc[t].where(E.loc[t]).dropna()
        if len(s) < 15:
            continue
        rc_vol.append(s.rank().corr(I["vol60"].loc[t, s.index].rank()))
        rc_beta.append(s.rank().corr(I["beta"].loc[t, s.index].rank()))
        q = 10 if len(s) >= 100 else (5 if len(s) >= 50 else 3)
        pct = s.rank(pct=True, method="first"); lo, hi = s.index[pct <= 1 / q], s.index[pct > 1 - 1 / q]
        for k, (a, b) in {"t+1": (1, 1), "t+2..3": (2, 3), "t+4..6": (4, 6)}.items():
            vals = []
            for h in range(a, b + 1):
                if t + h in fwd.index:
                    rr = fwd.loc[t + h]; vals.append(rr[lo].mean() - rr[hi].mean())
            if vals:
                hz[k].append(np.mean(vals))
    return dict(rankcorr_max_vol=float(np.nanmean(rc_vol)), rankcorr_max_beta=float(np.nanmean(rc_beta)),
                horizon={k: float(np.mean(v) * 12) for k, v in hz.items()})


if __name__ == "__main__":
    import sys
    out = {}; series = {}
    for R in data.REGIONS:
        I = monthly_inputs(R)
        steps = {"L0 baseline": build(I), "L1 beta-neutral": build(I, beta_neutral=True),
                 "L2 + vol-scaled MAX": build(I, signal="max5vol", beta_neutral=True),
                 "L3 + turnover buffer": build(I, signal="max5vol", beta_neutral=True, buffer=True)}
        series[R] = steps
        out[R] = dict(diag=diagnostics(R, I))
        print(R, out[R]["diag"], {k: round(v.ls_net.mean() * 12, 3) for k, v in steps.items()})
    pd.to_pickle(series, os.path.join(RES, "lottery_fix_series.pkl"))
    json.dump(out, open(os.path.join(RES, "lottery_diagnostics.json"), "w"), indent=1)
