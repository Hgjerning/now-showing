# -*- coding: utf-8 -*-
"""A31 U2: European blue chips (11 national indices, quarterly point-in-time membership), prices converted to EUR.
Season 2 EU panel (total-return fix) cleaned with universes.clean_yahoo (rule v2). EODHD fundamentals (eu_fund_long).
Gross profit is taken from the raw EODHD statements (eu_grossprofit.parquet, extracted 2026-10-06), matched on ticker, frequency and period end."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, ".")
from universes import clean_yahoo, snapshot_membership
D = "/mnt/user-data/uploads/ClaudeCode/Project10_Articles/Factsheets/_data_private"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FEATS = ["r1", "r3", "mom", "vol60", "maxret", "hi52", "beta", "size", "bm", "ep", "gpa", "ag"]
CCY = {"DE": "EUR", "PA": "EUR", "AS": "EUR", "MC": "EUR", "MI": "EUR", "HE": "EUR", "BR": "EUR", "LS": "EUR",
       "ST": "SEK", "CO": "DKK", "WA": "PLN"}

def fx_usd():
    S = {}
    for c in ["EUR", "SEK", "DKK", "CHF", "GBP"]:
        try:
            f = pd.read_csv(f"{D}/annox_universe/fx_long/{c}USD.csv", parse_dates=["date"]).set_index("date").close
            S[c] = f[f > 0]
        except FileNotFoundError:
            pass
    p = pd.read_parquet("/mnt/user-data/uploads/ClaudeCode/Project20 Investments/Project1/Data/cache/prices/px_PLNUSD_X.parquet")
    p.columns = [c[0] if isinstance(c, tuple) else c for c in p.columns]
    S["PLN"] = p["Close"].dropna(); S["PLN"].index = pd.to_datetime(S["PLN"].index).tz_localize(None)
    S["USD"] = None
    return S

FX = fx_usd()
def to_eur(c, idx):
    """multiplier local -> EUR on dates idx"""
    eur = FX["EUR"].reindex(FX["EUR"].index.union(idx)).ffill().reindex(idx)
    if c == "EUR": return pd.Series(1.0, index=idx)
    if c == "USD": return 1 / eur
    s = FX.get(c)
    if s is None: return pd.Series(np.nan, index=idx)
    s = s.reindex(s.index.union(idx)).ffill().reindex(idx)
    s[idx < FX[c].index[0]] = np.nan
    return s / eur

raw = pd.read_parquet(f"{D}/pit/EU_pit_adjclose_tr.parquet").sort_index(); raw.index = pd.to_datetime(raw.index).astype("datetime64[ns]")
px, info = clean_yahoo(raw)
print("prices", px.shape, "dropped", len(info["dropped"]), flush=True)
mem = pd.read_csv(f"{D}/pit/members_EU.csv")
M, cov_names = snapshot_membership(px.index, list(px.columns), mem)
M = pd.DataFrame(M, index=px.index, columns=px.columns)
sfx = pd.Series({t: t.split(".")[-1] for t in px.columns})
mult = pd.DataFrame({t: to_eur(CCY.get(sfx[t], "EUR"), px.index) for t in px.columns})
pxe = px * mult
pm = pxe.resample("ME").last().where(pxe.notna().resample("ME").sum() > 0)
months = pm.index
uni = M.resample("ME").last().reindex(months).fillna(False).astype(bool) & pm.notna()
print("members per month", uni.sum(1).loc["2013":].describe().round(0).to_dict(), flush=True)

# fundamentals
fd = pd.read_parquet(f"{D}/eodhd_fundamentals/eu_fund_long.parquet")
fd = fd[fd.region == "EU"].copy(); fd = fd[fd.ticker.isin(px.columns)]
gpx = pd.read_parquet(f"{D}/_staging/eu_grossprofit.parquet").drop_duplicates(["ticker", "freq", "period_end"])
fd = fd.merge(gpx, on=["ticker", "freq", "period_end"], how="left")
fd = fd.sort_values(["ticker", "period_end", "avail_date"])
q = fd[fd.freq == "Q"].drop_duplicates(["ticker", "period_end"], keep="last").copy()
gq = q.groupby("ticker", group_keys=False)
span = (q.period_end - gq.period_end.shift(3)).dt.days
q["ni_ttm"] = gq.netIncome.rolling(4, min_periods=4).sum().reset_index(level=0, drop=True).where(span.between(250, 300))
q["gp_ttm"] = gq.grossProfit.rolling(4, min_periods=4).sum().reset_index(level=0, drop=True).where(span.between(250, 300))
y = fd[fd.freq == "Y"].drop_duplicates(["ticker", "period_end"], keep="last").copy(); y["ni_ttm"] = y.netIncome; y["gp_ttm"] = y.grossProfit
R = pd.concat([q, y]).sort_values(["ticker", "avail_date", "period_end"])
# assets one year earlier (any frequency, period end 320-410 days before)
def assets_ly(g):
    g = g.sort_values("period_end"); out = []
    pe = g.period_end.values; a = g.totalAssets.values
    for i in range(len(g)):
        d = (pe[i] - pe) / np.timedelta64(1, "D"); k = np.where((d >= 320) & (d <= 410))[0]
        out.append(a[k[-1]] if len(k) else np.nan)
    return pd.Series(out, index=g.index)
R["assets_ly"] = R.groupby("ticker", group_keys=False).apply(assets_ly)
R["ag"] = R.totalAssets / R.assets_ly - 1
R["gpa"] = R.gp_ttm / R.totalAssets
R = R.rename(columns={"avail_date": "date"})

def asof_monthly(fd, col, months, tickers, maxage=550):
    w = fd.dropna(subset=[col]).pivot_table(index="date", columns="ticker", values=col, aggfunc="last").reindex(columns=tickers)
    idx = w.index.union(months)
    v = w.reindex(idx).ffill().reindex(months)
    fdate = pd.DataFrame(np.where(w.notna(), w.index.values[:, None], np.datetime64("NaT", "ns")), index=w.index, columns=w.columns)
    fdate = fdate.reindex(idx).ffill().reindex(months)
    age = pd.DataFrame(np.repeat(months.values[:, None], len(tickers), 1), index=months, columns=tickers) - fdate.apply(pd.to_datetime)
    return v.where(age <= pd.Timedelta(days=maxage))

tick = px.columns
ccyf = asof_monthly(R.assign(c=R.currency), "c", months, tick)
def eur_of(colvals):
    out = colvals.copy() * np.nan
    for c in ["EUR", "SEK", "DKK", "PLN", "USD", "CHF", "GBP"]:
        mlt = to_eur(c, months)
        out = out.where(ccyf != c, colvals.mul(mlt, axis=0))
    return out
sh = asof_monthly(R, "commonStockSharesOutstanding", months, tick)
mc = sh * pm
eq = eur_of(asof_monthly(R, "totalStockholderEquity", months, tick))
ni = eur_of(asof_monthly(R, "ni_ttm", months, tick))
F = {}
dr = pxe.pct_change(fill_method=None); dr = dr.where(dr.abs() < 1.0); mkt = dr.mean(axis=1)
F["r1"] = pm / pm.shift(1) - 1; F["r3"] = pm / pm.shift(3) - 1; F["mom"] = pm.shift(1) / pm.shift(12) - 1
F["vol60"] = (dr.rolling(60, min_periods=40).std() * np.sqrt(252)).resample("ME").last()
F["maxret"] = dr.resample("ME").max()
F["hi52"] = (pxe / pxe.rolling(252, min_periods=200).max()).resample("ME").last()
mm = mkt.to_numpy()[:, None]; xy = (dr.fillna(0) * mm).where(dr.notna())
ex = dr.rolling(252, min_periods=200).mean(); em = mkt.rolling(252, min_periods=200).mean()
exy = xy.rolling(252, min_periods=200).mean(); vm = mkt.rolling(252, min_periods=200).var(ddof=0)
F["beta"] = (exy.sub(ex.mul(em, axis=0))).div(vm, axis=0).resample("ME").last()
F = {k: v.reindex(months).where(pm.notna()) for k, v in F.items()}
F["size"] = np.log(mc); F["bm"] = eq / mc; F["ep"] = ni / mc
F["gpa"] = asof_monthly(R, "gpa", months, tick)
F["ag"] = asof_monthly(R, "ag", months, tick)
# reported only: operating profitability EBIT/assets (candidate substitute, NOT used unless the pre-registration is amended)
R["ebit_ttm_proxy"] = R.ebit / R.totalAssets
F_op = asof_monthly(R, "ebit_ttm_proxy", months, tick)
ret = pm.pct_change(fill_method=None); fwd = ret.shift(-1)
rows = []
for k in FEATS + ["fwd", "raw_mom", "mc", "opa"]:
    src = {"fwd": fwd, "raw_mom": F["mom"], "mc": mc, "opa": F_op}.get(k, F.get(k))
    rows.append(src.where(uni).stack(future_stack=True).rename(k))
L = pd.concat(rows, axis=1)
L = L[uni.stack(future_stack=True).reindex(L.index).fillna(False).astype(bool)]
L.index.names = ["month", "ticker"]
cov = L[FEATS + ["opa"]].notna().groupby(level=0).mean(); cov["n"] = L.groupby(level=0).size()
cov["fx_missing"] = L.assign(c=[CCY.get(t.split('.')[-1]) for t in L.index.get_level_values(1)]).pipe(lambda x: x.r1.isna()).groupby(level=0).mean()
cov.to_csv(f"{OUT}/coverage_U2.csv")
L.to_pickle(f"{OUT}/long_U2_raw.pkl")
gq2 = L.groupby(level=0)
for k in FEATS:
    L[k] = (gq2[k].rank(pct=True) - 0.5).fillna(0.0)
L["y"] = gq2["fwd"].rank(pct=True) - 0.5
L.drop(columns=["opa"]).to_pickle(f"{OUT}/long_U2.pkl")
print(cov.loc["2013":].describe().T[["mean", "min"]].round(3)); print("DONE")
