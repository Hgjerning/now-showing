# -*- coding: utf-8 -*-
"""Monthly price-only signal library on the six point-in-time universes (the base of the factor battery).

All signals are measured with information up to month-end t and used for month t+1.
  max1   largest daily return in month t (lottery; Bali, Cakici & Whitelaw 2011)
  max5   mean of the 5 largest daily returns in month t
  min1   most negative daily return in month t (crash / falling knife; the MAX mirror)
  min5   mean of the 5 most negative daily returns
  range  max1 - min1 (total extremeness)
  asym   max1 + min1 (net tail: > 0 = up-tail dominates, < 0 = down-tail dominates)
  skew   skewness of daily returns in month t (Boyer, Mitton & Vorkink 2010 use expected idiosyncratic skew)
  ivol   std of daily residuals vs the EW universe in month t (Ang, Hodrick, Xing & Zhang 2006)
  vol    63-day std of daily returns
  beta   252-day beta vs the EW universe
  r1     return in month t (short-term reversal; Jegadeesh 1990)
  mom    return t-12..t-1 (momentum; Jegadeesh & Titman 1993)
  hi52   price / 252-day high (George & Hwang 2004; 1 = at the high, low = deep drawdown)
  lo52   price / 252-day low (1 = at the 52-week low: the falling knife)
  brk55  price / prior 55-day high (Turtle System 2 breakout distance)
Requires >= 15 valid days in month t for the within-month statistics.
"""
import os

import numpy as np
import pandas as pd

import data

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "cache")
SIGNALS = ["max1", "max5", "min1", "min5", "range", "asym", "skew", "ivol", "vol", "beta", "r1", "mom", "hi52", "lo52", "brk55"]


def _topk(r, per, k, largest=True):
    """Mean of the k largest (or smallest) daily returns per month, vectorised."""
    out = {}
    for p_, d in r.groupby(per):
        a = d.to_numpy(float)
        fill = -np.inf if largest else np.inf
        srt = np.sort(np.where(np.isnan(a), fill, a), axis=0)
        sel = srt[-k:] if largest else srt[:k]
        m = sel.mean(axis=0); m[np.isnan(a).sum(axis=0) > a.shape[0] - k] = np.nan
        out[p_] = m
    return pd.DataFrame(out, index=r.columns).T


def build(R):
    f = os.path.join(CACHE, f"signals_{R}.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    s0 = "1998" if R.endswith("_A") else "2012"
    o = data.load(R); r, e = o["ret"].loc[s0:], o["elig"].loc[s0:]
    mkt = r.where(e).mean(axis=1)
    per = r.index.to_period("M"); g = r.groupby(per); cnt = g.count(); ok = cnt >= 15
    S = {}
    S["max1"] = g.max().where(ok); S["min1"] = g.min().where(ok)
    S["max5"] = _topk(r, per, 5, largest=True).where(ok)
    S["min5"] = _topk(r, per, 5, largest=False).where(ok)
    S["range"] = S["max1"] - S["min1"]; S["asym"] = S["max1"] + S["min1"]
    S["skew"] = g.skew().where(ok)
    res = r.sub(mkt, axis=0)       # simple market-adjusted residual (beta-1 residual) for a robust monthly IVOL
    S["ivol"] = res.groupby(per).std().where(ok)
    S["vol"] = r.rolling(63, min_periods=40).std().groupby(per).last()
    m = mkt.to_numpy()[:, None]
    ex = r.rolling(252, min_periods=200).mean(); em = mkt.rolling(252, min_periods=200).mean()
    exy = (r.fillna(0) * m).where(r.notna()).rolling(252, min_periods=200).mean(); vm = mkt.rolling(252, min_periods=200).var(ddof=0)
    S["beta"] = exy.sub(ex.mul(em, axis=0)).div(vm, axis=0).groupby(per).last()
    P = (1 + r.fillna(0)).cumprod().where(r.notna().cumsum() > 0).ffill()
    pm = P.groupby(per).last()
    S["r1"] = g.apply(lambda d: (1 + d.fillna(0)).prod() - 1).where(ok)
    S["mom"] = pm.shift(1) / pm.shift(12) - 1
    S["hi52"] = (P / P.rolling(252, min_periods=200).max()).groupby(per).last()
    S["lo52"] = (P / P.rolling(252, min_periods=200).min()).groupby(per).last()
    S["brk55"] = (P / P.shift(1).rolling(55, min_periods=55).max()).groupby(per).last()
    E = data.month_elig(e)
    fwd = g.apply(lambda d: (1 + d.fillna(0)).prod() - 1).where(cnt > 0)
    ew = mkt.groupby(per).apply(lambda s: (1 + s).prod() - 1)
    S = {k: v.where(E) for k, v in S.items()}
    out = dict(S=S, fwd=fwd, E=E, ew=ew)
    pd.to_pickle(out, f)
    return out


if __name__ == "__main__":
    import sys
    for R in (sys.argv[1:] or data.REGIONS):
        o = build(R); print(R, {k: int(v.notna().sum(axis=1).median()) for k, v in o["S"].items()})
