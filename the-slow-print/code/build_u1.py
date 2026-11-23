# -*- coding: utf-8 -*-
"""A31 U1: US small caps (ranks 1,001-3,000, point in time), 1998-2026. Builds the long panel with the A06 features.
Same definitions as lib10/panel.py + features.py (A06), applied to the Sharadar USS98 + USS panels."""
import os, sys, numpy as np, pandas as pd
D = "/mnt/user-data/uploads/ClaudeCode/Project10_Articles/Factsheets/_data_private"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FEATS = ["r1", "r3", "mom", "vol60", "maxret", "hi52", "beta", "size", "bm", "ep", "gpa", "ag"]

# ---- prices: splice USS98 (to 2011-06-30) and USS (from 2011-06-01) per ticker, scaled at the last common day
a = pd.read_parquet(f"{D}/pit/USS98_pit_adjclose.parquet").sort_index(); b = pd.read_parquet(f"{D}/pit/USS_pit_adjclose.parquet").sort_index()
a.index = pd.to_datetime(a.index); b.index = pd.to_datetime(b.index); a = a.where(a > 0); b = b.where(b > 0)
cut = pd.Timestamp("2011-06-01")
cols = sorted(set(a.columns) | set(b.columns))
A = a.reindex(columns=cols); B = b.reindex(columns=cols)
common = A.index.intersection(B.index)
# scale factor: ratio on the last common day where both exist
both = (A.loc[common].notna() & B.loc[common].notna())
fac = pd.Series(1.0, index=cols)
for t in cols:
    w = both[t]
    if w.any():
        d = w[w].index[-1]; fac[t] = B.at[d, t] / A.at[d, t]
px = pd.concat([A.loc[A.index < cut] * fac, B.loc[B.index >= cut]]).sort_index()
px = px[~px.index.duplicated()]
print("prices", px.shape, px.index[0].date(), px.index[-1].date(), flush=True)

# ---- membership (monthly)
m = pd.concat([pd.read_csv(f"{D}/pit/members_USS98.csv", parse_dates=["date"]), pd.read_csv(f"{D}/pit/members_USS.csv", parse_dates=["date"])])
m["month"] = m.date.dt.to_period("M").dt.to_timestamp("M")
m = m.sort_values("date").drop_duplicates(["month", "ticker"])
# for the join month (2011-06) both panels may list members: keep the later (USS) list
last = m.groupby("month").date.transform("max"); m = m[m.date == last]
pm = px.resample("ME").last().where(px.notna().resample("ME").sum() > 0)
months = pm.index
uni = pd.DataFrame(False, index=months, columns=px.columns)
for mo, g in m.groupby("month"):
    if mo in uni.index:
        uni.loc[mo, [t for t in g.ticker if t in uni.columns]] = True
uni = uni & pm.notna()
print("members per month", uni.sum(1).loc["1999":].describe().round(0).to_dict(), flush=True)

# ---- fundamentals (Sharadar ARQ), TTM with consecutive-quarter check
cols_f = ["ticker", "calendardate", "date", "assets", "equity", "netinc", "gp", "marketcap"]
fd = pd.concat([pd.read_csv(f"{D}/us_small/us_small_fundamentals_ARQ98.csv.gz", usecols=cols_f, parse_dates=["calendardate", "date"]),
                pd.read_csv(f"{D}/us_small/us_small_fundamentals_ARQ.csv.gz", usecols=cols_f, parse_dates=["calendardate", "date"])])
fd = fd.sort_values(["ticker", "calendardate", "date"]).drop_duplicates(["ticker", "calendardate"], keep="last")
g = fd.groupby("ticker", group_keys=False)
fd["qn"] = fd.calendardate.dt.year * 4 + (fd.calendardate.dt.month - 1) // 3
consec = g["qn"].diff(3) == 3
for c in ["netinc", "gp"]:
    fd[c + "_ttm"] = g[c].rolling(4, min_periods=4).sum().reset_index(level=0, drop=True).where(consec)
fd["assets_ly"] = g["assets"].shift(4).where(g["qn"].diff(4) == 4)
fd = fd[fd.ticker.isin(px.columns)]

def asof_monthly(fd, col, months, tickers):
    w = fd.pivot_table(index="date", columns="ticker", values=col, aggfunc="last").reindex(columns=tickers)
    idx = w.index.union(months)
    v = w.reindex(idx).ffill().reindex(months)
    fdate = pd.DataFrame(np.where(w.notna(), w.index.values[:, None], np.datetime64("NaT")), index=w.index, columns=w.columns)
    fdate = fdate.reindex(idx).ffill().reindex(months)
    age = pd.DataFrame(np.repeat(months.values[:, None], len(tickers), 1), index=months, columns=tickers) - fdate.apply(pd.to_datetime)
    return v.where(age <= pd.Timedelta(days=400))

tick = px.columns
pf = px.ffill().reindex(px.index.union(pd.DatetimeIndex(fd.date.unique()))).ffill()
fd["p_at"] = [pf.at[d, t] if t in pf.columns else np.nan for d, t in zip(fd.date, fd.ticker)]
fd["shr"] = fd.marketcap / fd.p_at
mc = asof_monthly(fd, "shr", months, tick) * pm
print("market caps done", flush=True)

# ---- price features (A06 definitions), computed in column chunks to fit in memory (float32)
px = px.astype("float32"); pm = pm.astype("float32")
dr_all_sum = None; cnt = None
for i in range(0, px.shape[1], 1500):
    d = px.iloc[:, i:i + 1500].pct_change(fill_method=None); d = d.where(d.abs() < 1.0)
    s1 = d.sum(axis=1, min_count=1); c1 = d.notna().sum(axis=1)
    dr_all_sum = s1.fillna(0) if dr_all_sum is None else dr_all_sum + s1.fillna(0); cnt = c1 if cnt is None else cnt + c1
mkt = (dr_all_sum / cnt.replace(0, np.nan)).astype("float64")
em = mkt.rolling(252, min_periods=200).mean(); vm = mkt.rolling(252, min_periods=200).var(ddof=0)
F = {k: [] for k in ["r1", "r3", "mom", "vol60", "maxret", "hi52", "beta"]}
for i in range(0, px.shape[1], 1500):
    p = px.iloc[:, i:i + 1500]; pmi = pm.iloc[:, i:i + 1500]
    dr = p.pct_change(fill_method=None); dr = dr.where(dr.abs() < 1.0)
    F["r1"].append(pmi / pmi.shift(1) - 1); F["r3"].append(pmi / pmi.shift(3) - 1); F["mom"].append(pmi.shift(1) / pmi.shift(12) - 1)
    F["vol60"].append((dr.rolling(60, min_periods=40).std() * np.sqrt(252)).resample("ME").last())
    F["maxret"].append(dr.resample("ME").max())
    F["hi52"].append((p / p.rolling(252, min_periods=200).max()).resample("ME").last())
    mm = mkt.to_numpy()[:, None]; xy = (dr.fillna(0) * mm).where(dr.notna())
    ex = dr.rolling(252, min_periods=200).mean(); exy = xy.rolling(252, min_periods=200).mean()
    F["beta"].append((exy.sub(ex.mul(em, axis=0))).div(vm, axis=0).resample("ME").last())
    del dr, xy, ex, exy
    print("chunk", i, flush=True)
F = {k: pd.concat(v, axis=1).reindex(months).where(pm.notna()) for k, v in F.items()}
print("price features done", flush=True)
F["size"] = np.log(mc)
F["bm"] = asof_monthly(fd, "equity", months, tick) / mc
F["ep"] = asof_monthly(fd, "netinc_ttm", months, tick) / mc
fd["gpa"] = fd.gp_ttm / fd.assets; fd["ag"] = fd.assets / fd.assets_ly - 1
F["gpa"] = asof_monthly(fd, "gpa", months, tick); F["ag"] = asof_monthly(fd, "ag", months, tick)
ret = pm.pct_change(fill_method=None); fwd = ret.shift(-1)
rows = []
for k in FEATS + ["fwd", "raw_mom", "mc"]:
    src = {"fwd": fwd, "raw_mom": F["mom"], "mc": mc}.get(k, F.get(k))
    rows.append(src.where(uni).stack(future_stack=True).rename(k))
L = pd.concat(rows, axis=1)
L = L[uni.stack(future_stack=True).reindex(L.index).fillna(False).astype(bool)]
L.index.names = ["month", "ticker"]
# coverage before rank-scaling (share non-missing per feature per month)
cov = L[FEATS].notna().groupby(level=0).mean()
cov["n"] = L.groupby(level=0).size()
cov.to_csv(f"{OUT}/coverage_U1.csv")
gq = L.groupby(level=0)
for k in FEATS:
    L[k] = (gq[k].rank(pct=True) - 0.5).fillna(0.0)
L["y"] = gq["fwd"].rank(pct=True) - 0.5
L.to_pickle(f"{OUT}/long_U1.pkl")
print(cov.loc["1999-12":].describe().T[["mean", "min"]].round(3)); print("DONE")
