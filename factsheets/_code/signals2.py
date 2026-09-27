# -*- coding: utf-8 -*-
"""Extra monthly signals for FS03-FS12 (added to the signal library).
  vol252  252-day volatility (low-volatility anomaly; Blitz & van Vliet 2007)
  seas    same-calendar-month average return over all available prior years (Heston & Sadka 2008).
          GAP: price history starts 2011-12, so 1 prior year in 2013 growing to 13 by 2026 (HS use up to 20)
  size    US: log market cap (Sharadar); elsewhere log 63-day average traded value (Close x Volume), a liquidity
          proxy for size. GAP: no shares outstanding outside the US. World ranks within each region first.
  resmom  residual momentum: market-model residuals over a 24-month window, sum of t-12..t-2 divided by their std
          (Blitz, Huij & Martens 2011 use 36 months and Fama-French 3 factors). GAP: market-only model, 24 months.
  capw    size weight for benchmarks: US market cap; elsewhere traded value (proxy)
"""
import os

import numpy as np
import pandas as pd

import data
import signals as SG

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
CACHE = os.path.join(D, "cache")


def _tv(R):
    return pd.read_parquet(os.path.join(D, "pit", f"{R}_pit_tradedvalue.parquet")).sort_index()


def _size_raw(R, idx_m):
    if R == "US":
        mc = data.load("US", pit=False)["mcap"]; mc.index = mc.index.to_period("M")
        return mc
    tv = _tv(R); tv = tv.where(tv > 0)
    avg = tv.rolling(63, min_periods=40).mean()
    m = avg.groupby(avg.index.to_period("M")).last()
    return m


def build(R):
    f = os.path.join(CACHE, f"signals2_{R}.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    base = SG.build(R); E = base["E"]; fwd = base["fwd"]
    o = data.load(R); r = o["ret"].loc["2011":]
    per = r.index.to_period("M"); g = r.groupby(per); cnt = g.count()
    S = {}
    S["vol252"] = r.rolling(252, min_periods=200).std().groupby(per).last()
    mret = g.apply(lambda d: (1 + d.fillna(0)).prod() - 1).where(cnt >= 15)
    # seasonality: mean of returns in the same calendar month, all prior years available
    seas = pd.DataFrame(np.nan, index=mret.index, columns=mret.columns)
    for i, t in enumerate(mret.index):
        lags = [t - 12 * k for k in range(1, 21) if (t - 12 * k) in mret.index]
        if lags:
            # the signal at month-end t predicts month t+1: use same month as t+1 in prior years
            tgt = [(t + 1) - 12 * k for k in range(1, 21) if ((t + 1) - 12 * k) in mret.index and ((t + 1) - 12 * k) <= t]
            if tgt:
                seas.loc[t] = mret.loc[tgt].mean()
    S["seas"] = seas
    # size
    if R == "WD":
        parts = []
        for sub in ["US", "UK", "EU"]:
            x = np.log(_size_raw(sub, None)); parts.append(x.rank(axis=1, pct=True))
        S["size"] = pd.concat(parts, axis=1).T.groupby(level=0).first().T
        caps = []
        for sub in ["US", "UK", "EU"]:
            c = _size_raw(sub, None); caps.append(c.div(c.sum(axis=1), axis=0))   # region-normalised weights
        capw = pd.concat(caps, axis=1).T.groupby(level=0).first().T
    else:
        raw = _size_raw(R, None); S["size"] = np.log(raw.where(raw > 0)); capw = raw
    # residual momentum (market model, 24-month window)
    mk = mret.where(E.reindex(mret.index).fillna(False)).mean(axis=1)
    res = pd.DataFrame(np.nan, index=mret.index, columns=mret.columns)
    X = mk.values
    for i in range(24, len(mret.index)):
        y = mret.iloc[i - 24:i + 1]; x = X[i - 24:i + 1]
        xm = x - np.nanmean(x); b = (y.sub(y.mean())).mul(xm, axis=0).sum() / (xm ** 2).sum()
        a = y.mean() - b * np.nanmean(x)
        e = y - (a.values + np.outer(x, b.values))
        win = e.iloc[-12:-1]           # t-11 .. t-1 relative to row i (skip the latest month)
        res.iloc[i] = (win.sum() / win.std()).where(y.notna().sum() >= 20)
    S["resmom"] = res
    idx = E.index
    S = {k: v.reindex(index=idx, columns=E.columns).where(E) for k, v in S.items()}
    capw = capw.reindex(index=idx, columns=E.columns).where(E)
    out = dict(S=S, capw=capw)
    pd.to_pickle(out, f)
    return out


if __name__ == "__main__":
    import sys
    for R in (sys.argv[1:] or data.REGIONS):
        o = build(R); print(R, {k: int(v.notna().sum(axis=1).loc["2013":].median()) for k, v in o["S"].items()}, "capw", int(o["capw"].notna().sum(axis=1).loc["2013":].median()))
