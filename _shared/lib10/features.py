# -*- coding: utf-8 -*-
"""Monthly stock features (A06 list), all measured with information available at month-end t."""
import os

import numpy as np
import pandas as pd

from panel import CACHE, asof_monthly, load_all


def price_features(px, pm):
    f = os.path.join(CACHE, "pfeat.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    months = pm.index
    dr = px.pct_change(fill_method=None)
    dr = dr.where(dr.abs() < 1.0)  # guard against bad ticks
    mkt = dr.mean(axis=1)
    F = {}
    F["r1"] = pm / pm.shift(1) - 1
    F["r3"] = pm / pm.shift(3) - 1
    F["mom"] = pm.shift(1) / pm.shift(12) - 1
    vol60 = dr.rolling(60, min_periods=40).std() * np.sqrt(252)
    F["vol60"] = vol60.resample("ME").last()
    F["maxret"] = dr.resample("ME").max()
    hi = px.rolling(252, min_periods=200).max()
    F["hi52"] = (px / hi).resample("ME").last()
    vol252 = dr.rolling(252, min_periods=200).std() * np.sqrt(252)
    F["vol252"] = vol252.resample("ME").last()
    # beta: rolling cov / var against equal-weight market
    m = mkt.to_numpy()[:, None]
    xy = (dr.fillna(0) * m).where(dr.notna())
    ex = dr.rolling(252, min_periods=200).mean(); em = mkt.rolling(252, min_periods=200).mean()
    exy = xy.rolling(252, min_periods=200).mean(); vm = mkt.rolling(252, min_periods=200).var(ddof=0)
    F["beta"] = ((exy.sub(ex.mul(em, axis=0))).div(vm, axis=0)).resample("ME").last()
    F = {k: v.reindex(months) for k, v in F.items()}
    F = {k: v.where(pm.notna()) for k, v in F.items()}
    pd.to_pickle(F, f)
    return F


def fund_features(fd, mc, months, tickers):
    f = os.path.join(CACHE, "ffeat.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    F = {}
    F["size"] = np.log(mc)
    F["bm"] = asof_monthly(fd, "equity", months, tickers) / mc
    F["ep"] = asof_monthly(fd, "netinc_ttm", months, tickers) / mc
    fd = fd.assign(gpa=fd.gp_ttm / fd.assets, ag=fd.assets / fd.assets_ly - 1)
    F["gpa"] = asof_monthly(fd, "gpa", months, tickers)
    F["ag"] = asof_monthly(fd, "ag", months, tickers)
    pd.to_pickle(F, f)
    return F


FEATS = ["r1", "r3", "mom", "vol60", "maxret", "hi52", "beta", "size", "bm", "ep", "gpa", "ag"]


def panel_long():
    """Long panel: rows = (month, ticker) in the top-500 universe; rank-scaled features, next-month return."""
    f = os.path.join(CACHE, "long.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    px, fd, pm, mc, uni, ret = load_all()
    F = price_features(px, pm); F.update(fund_features(fd, mc, pm.index, px.columns))
    fwd = ret.shift(-1)
    rows = []
    for k in FEATS + ["fwd", "raw_mom", "mc", "vol252"]:
        src = {"fwd": fwd, "raw_mom": F["mom"], "mc": mc, "vol252": F["vol252"]}.get(k, F.get(k))
        s = src.where(uni).stack(future_stack=True).rename(k)
        rows.append(s)
    L = pd.concat(rows, axis=1)
    L = L[uni.stack(future_stack=True).reindex(L.index).fillna(False).astype(bool)]
    L.index.names = ["month", "ticker"]
    g = L.groupby(level=0)
    for k in FEATS:
        L[k] = (g[k].rank(pct=True) - 0.5).fillna(0.0)
    L["y"] = g["fwd"].rank(pct=True) - 0.5
    L.to_pickle(f)
    return L


if __name__ == "__main__":
    L = panel_long()
    print(L.shape); print(L.groupby(level=0).size().describe()); print(L.describe().T[["mean", "std"]])
