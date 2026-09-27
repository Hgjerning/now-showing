# -*- coding: utf-8 -*-
"""Lottery factor: MAX (Bali, Cakici & Whitelaw 2011), built monthly per universe.

Formation at month-end t: MAX1 = largest daily total return in month t (>= 15 valid days);
MAX5 = mean of the five largest (robustness). Eligible = in the universe at month-end t
(US: point-in-time top 500; others: survivor list with >= 252 days of history).
Sort into deciles (quintiles for 50-99 names = SCANDI, terciles below 50 = DK). Equal-weighted (US also value-weighted),
held for month t+1 (compounded daily TR). L/S = lowest-MAX minus highest-MAX.
Costs: 10 bp per side on one-way turnover of each leg.
"""
import numpy as np
import borrow as BR
import pandas as pd

import data

COST = 0.0010


def build(o, signal="max1", start="2012-12-31", vw=False, R=None):
    ret, elig = o["ret"], o["elig"]
    g = ret.groupby(ret.index.to_period("M"))
    cnt = g.count()
    if signal == "max1":
        S = g.max()
    else:
        S = g.apply(lambda d: d.apply(lambda c: c.nlargest(5).mean() if c.notna().sum() >= 5 else np.nan))
    S = S.where(cnt >= 15)
    fwd = (g.apply(lambda d: (1 + d.fillna(0)).prod() - 1)).where(cnt > 0)   # month return (0 for no data days)
    E = data.month_elig(elig)
    months = S.index
    if vw:
        mc = o["mcap"].copy(); mc.index = mc.index.to_period("M")
    rows, hold, logs = [], {}, []
    prev = {}
    ns = [int(S.loc[t].where(E.loc[t]).notna().sum()) for t in months if t.to_timestamp("M") >= pd.Timestamp(start) and t in E.index]
    nmed = float(np.median(ns)); qfix = 10 if nmed >= 100 else (5 if nmed >= 50 else 3)   # fixed per universe
    for i in range(len(months) - 1):
        t, nx = months[i], months[i + 1]
        if t.to_timestamp("M") < pd.Timestamp(start):
            continue
        s = S.loc[t].where(E.loc[t]).dropna()
        if len(s) < 15:
            continue
        q = qfix
        b = pd.qcut(s.rank(method="first"), q, labels=False) + 1
        r = fwd.loc[nx, s.index].fillna(0.0) if nx in fwd.index else None
        row = {"month": nx.to_timestamp("M"), "n": len(s), "q": q}
        w_all = {}
        for k in range(1, q + 1):
            names = b.index[b == k]
            if vw:
                w = mc.loc[t, names].fillna(0); w = w / w.sum()
            else:
                w = pd.Series(1 / len(names), index=names)
            w_all[k] = w
            row[f"Q{k}"] = float((w * r[names]).sum())
        row["EW"] = float(r.mean())
        # turnover & costs (weights drift ignored: rebalanced back to target each month)
        for leg, k in (("low", 1), ("high", q)):
            w = w_all[k]; pw = prev.get(leg, pd.Series(dtype=float))
            to = float(w.subtract(pw, fill_value=0).abs().sum()) / 2
            row[f"to_{leg}"] = to
            prev[leg] = w
        row["low_net"] = row["Q1"] - COST * 2 * row["to_low"]
        row["ls_gross"] = row["Q1"] - row[f"Q{q}"]
        row["borrow"] = BR.monthly_fee(R, t, w_all[q])
        row["ls_net"] = row["ls_gross"] - COST * 2 * (row["to_low"] + row["to_high"]) - row["borrow"]
        row["max_low"] = float(s[b == 1].mean()); row["max_high"] = float(s[b == q].mean())
        rows.append(row)
        hold[t.to_timestamp("M")] = dict(low=list(w_all[1].index), high=list(w_all[q].index),
                                         low_max=s[b == 1].to_dict(), high_max=s[b == q].to_dict())
    P = pd.DataFrame(rows).set_index("month")
    return P, hold


def current_portfolio(o, asof="2026-08-31"):
    """Holdings formed at the last complete month-end (for the 'current book' box)."""
    ret, elig = o["ret"], o["elig"]
    m = ret.loc[pd.Timestamp(asof).replace(day=1):asof]
    s = m.max().where(m.count() >= 15).where(elig.loc[:asof].iloc[-1]).dropna()
    q = 10 if len(s) >= 100 else (5 if len(s) >= 50 else 3)
    b = pd.qcut(s.rank(method="first"), q, labels=False) + 1
    return s[b == 1].sort_values(), s[b == q].sort_values(ascending=False)
