# -*- coding: utf-8 -*-
"""Point-in-time monthly panel for the S&P master universe (A06-A10).

Market cap at month-end t = latest Sharadar `marketcap` filed on or before t, scaled by the
split-adjusted price change since that filing date (i.e. implied shares x price).
"""
import os

import numpy as np
import pandas as pd

SD = os.environ.get("P10_DATA", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_private_data"))  # licensed Sharadar files, not in the repo
CACHE = os.path.join(SD, "cache")
os.makedirs(CACHE, exist_ok=True)


def daily_prices():
    f = os.path.join(CACHE, "px.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    px = pd.read_csv(os.path.join(SD, "us_master_universe_prices.csv"), index_col=0, parse_dates=True).sort_index()
    px = px.where(px > 0)
    px.to_pickle(f)
    return px


def fundamentals():
    f = os.path.join(CACHE, "fund.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    cols = ["ticker", "calendardate", "date", "assets", "assetsc", "liabilities", "liabilitiesc", "workingcapital", "retearn",
            "ebit", "revenue", "netinc", "ncfo", "equity", "gp", "marketcap", "sharesbas", "debtnc", "grossmargin",
            "currentratio", "assetturnover"]
    fd = pd.read_csv(os.path.join(SD, "us_fundamentals.csv"), usecols=cols, parse_dates=["calendardate", "date"])
    fd = fd.sort_values(["ticker", "calendardate", "date"]).drop_duplicates(["ticker", "calendardate"], keep="last")
    g = fd.groupby("ticker", group_keys=False)
    # consecutive-quarter check for TTM sums
    qn = fd.calendardate.dt.year * 4 + (fd.calendardate.dt.month - 1) // 3
    fd["qn"] = qn
    consec = (g["qn"].diff(3) == 3)
    for c in ["revenue", "netinc", "ncfo", "gp", "ebit"]:
        s = g[c].rolling(4, min_periods=4).sum().reset_index(level=0, drop=True)
        fd[c + "_ttm"] = s.where(consec)
    for c in ["netinc_ttm", "assets", "ncfo_ttm", "gp_ttm", "revenue_ttm", "currentratio", "assetturnover", "grossmargin", "sharesbas", "debtnc"]:
        fd[c + "_ly"] = g[c].shift(4).where(g["qn"].diff(4) == 4)
    fd.to_pickle(f)
    return fd


def month_end_prices(px):
    """Last close within each calendar month (captures the partial month before a delisting)."""
    pm = px.resample("ME").last()
    traded = px.notna().resample("ME").sum() > 0
    return pm.where(traded)


def asof_monthly(fd, col, months, tickers):
    """Value of `col` from the latest filing on or before each month-end (NaN if > 400 days old)."""
    w = fd.pivot_table(index="date", columns="ticker", values=col, aggfunc="last")
    w = w.reindex(columns=tickers)
    idx = w.index.union(months)
    v = w.reindex(idx).ffill().reindex(months)
    fdate = pd.DataFrame(np.where(w.notna(), w.index.values[:, None], np.datetime64("NaT")), index=w.index, columns=w.columns)
    fdate = fdate.reindex(idx).ffill().reindex(months)
    age = (pd.DataFrame(np.repeat(months.values[:, None], len(tickers), 1), index=months, columns=tickers) - fdate.apply(pd.to_datetime))
    return v.where(age <= pd.Timedelta(days=400))


def market_cap(px, fd, months):
    f = os.path.join(CACHE, "mcap.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    tick = px.columns
    pf = px.ffill().reindex(px.index.union(pd.DatetimeIndex(fd.date.unique()))).ffill()
    fd = fd.copy()
    fd["p_at"] = [pf.at[d, t] if t in pf.columns else np.nan for d, t in zip(fd.date, fd.ticker)]
    fd["shr"] = fd.marketcap / fd.p_at
    shr = asof_monthly(fd, "shr", months, tick)
    pm = month_end_prices(px).reindex(months)
    mc = shr * pm
    mc.to_pickle(f)
    return mc


def top_n(mc, n=500):
    r = mc.rank(axis=1, ascending=False, method="first")
    return (r <= n) & mc.notna()


def load_all():
    px = daily_prices()
    fd = fundamentals()
    pm = month_end_prices(px)
    months = pm.index
    mc = market_cap(px, fd, months)
    uni = top_n(mc)
    ret = pm.pct_change(fill_method=None)
    return px, fd, pm, mc, uni, ret


if __name__ == "__main__":
    px, fd, pm, mc, uni, ret = load_all()
    print(pm.shape, uni.sum(axis=1).describe())
    print(mc.iloc[-2].sort_values(ascending=False).head(12) / 1e9)
