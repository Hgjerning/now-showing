# -*- coding: utf-8 -*-
"""A31 reported extension, U1 US small caps: wide features added to long_U1.pkl -> long_U1_wide.pkl.
Price splice, membership, market cap and as-of rule (filing date, max age 400 days) identical to build_u1.py."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, ".")
from wide_features import price_wide, fund_wide
from build_u2_common import finish
D = "/mnt/user-data/uploads/ClaudeCode/Project10_Articles/Factsheets/_data_private"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

a = pd.read_parquet(f"{D}/pit/USS98_pit_adjclose.parquet").sort_index(); b = pd.read_parquet(f"{D}/pit/USS_pit_adjclose.parquet").sort_index()
a.index = pd.to_datetime(a.index); b.index = pd.to_datetime(b.index); a = a.where(a > 0); b = b.where(b > 0)
cut = pd.Timestamp("2011-06-01"); cols = sorted(set(a.columns) | set(b.columns))
A = a.reindex(columns=cols); B = b.reindex(columns=cols); del a, b
common = A.index.intersection(B.index); both = (A.loc[common].notna() & B.loc[common].notna())
fac = pd.Series(1.0, index=cols)
for t in cols:
    w = both[t]
    if w.any():
        d = w[w].index[-1]; fac[t] = B.at[d, t] / A.at[d, t]
px = pd.concat([A.loc[A.index < cut] * fac, B.loc[B.index >= cut]]).sort_index(); px = px[~px.index.duplicated()]; del A, B
m = pd.concat([pd.read_csv(f"{D}/pit/members_USS98.csv", parse_dates=["date"]), pd.read_csv(f"{D}/pit/members_USS.csv", parse_dates=["date"])])
m["month"] = m.date.dt.to_period("M").dt.to_timestamp("M"); m = m.sort_values("date").drop_duplicates(["month", "ticker"])
m = m[m.date == m.groupby("month").date.transform("max")]
pm = px.resample("ME").last().where(px.notna().resample("ME").sum() > 0); months = pm.index
uni = pd.DataFrame(False, index=months, columns=px.columns)
for mo, g in m.groupby("month"):
    if mo in uni.index:
        uni.loc[mo, [t for t in g.ticker if t in uni.columns]] = True
uni = uni & pm.notna()
L = pd.read_pickle(f"{OUT}/long_U1.pkl")
print("prices", px.shape, flush=True)

FLOW = {"rev": "revenue", "ni": "netinc", "gp": "gp", "ebit": "ebit", "cfo": "ncfo", "capex": "capex", "div": "ncfdiv",
        "rnd": "rnd", "sgna": "sgna", "dep": "depamor"}
STOCK = {"assets": "assets", "equity": "equity", "debt": "debt", "cash": "cashneq", "ca": "assetsc", "cl": "liabilitiesc",
         "ppe": "ppnenet", "inv": "inventory", "rec": "receivables", "liab": "liabilities", "intang": "intangibles"}
use = ["ticker", "calendardate", "date", "marketcap"] + list(FLOW.values()) + list(STOCK.values())
fd = pd.concat([pd.read_csv(f"{D}/us_small/us_small_fundamentals_ARQ98.csv.gz", usecols=use, parse_dates=["calendardate", "date"]),
                pd.read_csv(f"{D}/us_small/us_small_fundamentals_ARQ.csv.gz", usecols=use, parse_dates=["calendardate", "date"])])
fd = fd.sort_values(["ticker", "calendardate", "date"]).drop_duplicates(["ticker", "calendardate"], keep="last")
fd = fd[fd.ticker.isin(px.columns)].reset_index(drop=True)
g = fd.groupby("ticker", group_keys=False)
fd["qn"] = fd.calendardate.dt.year * 4 + (fd.calendardate.dt.month - 1) // 3
consec = g["qn"].diff(3) == 3; ly_ok = g["qn"].diff(4) == 4
for k, c in FLOW.items():
    fd[k] = g[c].rolling(4, min_periods=4).sum().reset_index(level=0, drop=True).where(consec)
for k, c in STOCK.items():
    fd[k] = fd[c]
pf = px.ffill().reindex(px.index.union(pd.DatetimeIndex(fd.date.unique()))).ffill()
fd["p_at"] = [pf.at[d, t] if t in pf.columns else np.nan for d, t in zip(fd.date, fd.ticker)]; del pf
fd["shares"] = fd.marketcap / fd.p_at          # split-adjusted share count (adjusted-price units), as build_u1
g = fd.groupby("ticker", group_keys=False)
for k in ["rev", "ni", "gp", "assets", "shares", "liab", "inv"]:
    fd[k + "_ly"] = g[k].shift(4).where(ly_ok)


def asof_monthly(col):
    w = fd.dropna(subset=[col]).pivot_table(index="date", columns="ticker", values=col, aggfunc="last").reindex(columns=px.columns)
    idx = w.index.union(months)
    v = w.reindex(idx).ffill().reindex(months)
    fdate = pd.DataFrame(np.where(w.notna(), w.index.values[:, None], np.datetime64("NaT", "ns")), index=w.index, columns=w.columns)
    fdate = fdate.reindex(idx).ffill().reindex(months)
    age = pd.DataFrame(np.repeat(months.values[:, None], len(px.columns), 1), index=months, columns=px.columns) - fdate.apply(pd.to_datetime)
    return v.where(age <= pd.Timedelta(days=400)).astype("float32")


G = {k: asof_monthly(k) for k in list(FLOW) + list(STOCK) + ["shares", "rev_ly", "ni_ly", "gp_ly", "assets_ly", "shares_ly", "liab_ly", "inv_ly"]}
mc = (G["shares"] * pm).astype("float64")
print("fundamentals as-of done", flush=True)
F = fund_wide(G, mc); del G
F = {k: v.astype("float32") for k, v in F.items()}
F.update({k: v.astype("float32") for k, v in price_wide(px.astype("float32"), pm.astype("float32"), months).items()})
finish(L, F, uni, OUT, "U1")
