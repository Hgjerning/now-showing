# -*- coding: utf-8 -*-
"""Generic cross-sectional strategy engine for FS03-FS12.

Books (monthly, formed at month-end t, held through t+1, equal-weighted unless stated):
  L/S        long the 'good' extreme quantile minus the other extreme (direction set per strategy), net of costs
  long-only  the 'good' leg, net of costs
  EW         equal-weight universe (benchmark 1); SW = size-weighted universe (benchmark 2: US market cap,
             elsewhere traded value as a proxy)
Construction variants: 'sort' (quantile sort), 'bab' (Frazzini & Pedersen 2014 rank-weighted, beta-scaled legs).
Uniform pre-declared fix ladder (design 2013-2019, holdout 2020-2026):
  X0 baseline -> X1 beta-neutral legs (1/ex-ante beta) -> X2 + turnover buffer (enter extreme 1/q, keep within 3/q)
  -> X3 + volatility targeting (scale the L/S to 10% a year using its trailing 6-month volatility, lagged)
Costs: 10 bp per side on one-way turnover of each leg (leverage included).
"""
import numpy as np
import borrow as BR
import pandas as pd

import signals as SG
import signals2 as SG2

COST = 0.0010
START, END = pd.Period("2013-01"), pd.Period("2026-07")


def nq(n):
    return 10 if n >= 100 else (5 if n >= 50 else 3)


def inputs(R):
    b = SG.build(R); x = SG2.build(R)
    S = dict(b["S"]); S.update(x["S"])
    return dict(S=S, fwd=b["fwd"], E=b["E"], ew=b["ew"], capw=x["capw"], R=R)


def size_weighted(I):
    fwd, cw = I["fwd"], I["capw"]; out = {}
    for t in cw.index:
        if not (START <= t <= END) or (t + 1) not in fwd.index:
            continue
        w = cw.loc[t].dropna(); w = w[w > 0]
        if len(w) < 5:
            continue
        w = w / w.sum(); out[(t + 1).to_timestamp("M")] = float((w * fwd.loc[t + 1, w.index].fillna(0)).sum())
    return pd.Series(out)


def run(I, sig, long_high, construction="sort", beta_neutral=False, buffer=False, voltarget=False, borrow=True, finance=True, record=None):
    S, fwd, B = I["S"][sig], I["fwd"], I["S"]["beta"]
    months = [t for t in S.index if START <= t <= END]
    q = nq(np.median([S.loc[t].notna().sum() for t in months])); keep = min(3 / q, 0.5)
    held = {"good": set(), "bad": set()}; prev = {"good": pd.Series(dtype=float), "bad": pd.Series(dtype=float)}
    rows = []
    for t in months:
        if (t + 1) not in fwd.index:
            break
        s = S.loc[t].dropna()
        if len(s) < 15:
            continue
        pct = s.rank(pct=True, method="first"); pct = pct if long_high else 1 - pct + 1 / len(pct)
        r = fwd.loc[t + 1, s.index].fillna(0)
        legs = {}
        if construction == "bab":
            b = B.loc[t, s.index].dropna(); b = b[(b > 0.05)]
            z = b.rank(); zc = z - z.mean()
            wL = (-zc).clip(lower=0); wH = zc.clip(lower=0); wL, wH = wL / wL.sum(), wH / wH.sum()
            bL, bH = float((wL * b).sum()), float((wH * b).sum())
            for leg, w, bb in (("good", wL / bL, bL), ("bad", wH / bH, bH)):
                to = float(w.subtract(prev[leg], fill_value=0).abs().sum()) / 2; prev[leg] = w
                legs[leg] = dict(ret=float((w * r[w.index]).sum()), to=to, beta=bb, n=int((w > 0).sum()), unlev=float((w * bb * r[w.index]).sum()), w=w[w > 0])
        else:
            for leg, inn, out_ in (("good", pct > 1 - 1 / q, pct > 1 - keep), ("bad", pct <= 1 / q, pct <= keep)):
                names = set(s.index[inn])
                if buffer:
                    names |= {n for n in held[leg] if n in s.index and out_[n]}
                names = sorted(names); held[leg] = set(names)
                w = pd.Series(1 / len(names), index=names)
                bb = float(B.loc[t, names].clip(0.2, 3).mean()) if beta_neutral else 1.0
                if not np.isfinite(bb):
                    bb = 1.0
                w = w / bb
                to = float(w.subtract(prev[leg], fill_value=0).abs().sum()) / 2; prev[leg] = w
                legs[leg] = dict(ret=float((w * r[names]).sum()), to=to, beta=bb, n=len(names), unlev=float((w * bb * r[names]).sum()), w=w)
        g, bd = legs["good"], legs["bad"]
        ls = g["ret"] - bd["ret"]; cost = COST * 2 * (g["to"] + bd["to"])
        bf = BR.monthly_fee(I.get("R"), t, bd["w"]) if borrow else 0.0
        if record is not None:
            record.append((t, g["w"], bd["w"]))
        netcash = float(g["w"].sum() - bd["w"].sum()); fin = BR.financing(t, netcash) if finance else 0.0
        rows.append(dict(month=(t + 1).to_timestamp("M"), ls_gross=ls, ls_net=ls - cost - bf - fin, cost=cost, borrow=bf, fin=fin, netcash=netcash, good_net=g["unlev"] - COST * 2 * g["to"] * g["beta"],
                         good=g["unlev"], bad=bd["unlev"], to_good=g["to"], to_bad=bd["to"], n_good=g["n"], n_bad=bd["n"], ew=float(fwd.loc[t + 1, s.index].fillna(0).mean())))
    P = pd.DataFrame(rows).set_index("month")
    if voltarget:
        vol = P.ls_net.rolling(6, min_periods=4).std().shift(1) * np.sqrt(12)
        lev = (0.10 / vol).clip(upper=3.0)
        P["ls_net"] = P.ls_net * lev; P["ls_gross"] = P.ls_gross * lev; P["lev"] = lev   # financing scales with the leverage
        P = P.dropna(subset=["ls_net"])
    P.attrs["q"] = q
    return P


def ladder(I, sig, long_high, construction="sort"):
    if construction == "bab":
        steps = {"X0 baseline": run(I, sig, long_high, "bab"),
                 "X2 + turnover buffer": None,   # buffer does not apply to rank weights; BAB skips X1 and X2
                 "X3 + volatility targeting": run(I, sig, long_high, "bab", voltarget=True)}
        return {k: v for k, v in steps.items() if v is not None}
    return {"X0 baseline": run(I, sig, long_high),
            "X1 beta-neutral legs": run(I, sig, long_high, beta_neutral=True),
            "X2 + turnover buffer": run(I, sig, long_high, beta_neutral=True, buffer=True),
            "X3 + volatility targeting": run(I, sig, long_high, beta_neutral=True, buffer=True, voltarget=True)}
