# -*- coding: utf-8 -*-
"""Five-universe daily total-return panels for the Project 10 strategy factsheets.

US : Sharadar closeadj (total return), point-in-time top-500 by market cap (A06 method, lib10/panel.py).
EU, UK, DK, WD : Project1 yfinance cache, TODAY's constituents (survivor lists, as in Project2).
     EU/DK/WD use Yahoo Adj Close (total return). UK is rebuilt from Close + dividends in pence,
     because Yahoo under-adjusts LSE names (Project2 qualitymom2/dividends.py).
All returns in local currency, except WD, which is converted to USD (unhedged) since 27 Sep 2026.
"""
import os
import numpy as np
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
CACHE = os.path.join(D, "cache"); os.makedirs(CACHE, exist_ok=True)
START, END = "2012-01-01", "2026-09-25"
KNOWN_BAD = ["DIA.MC", "ATO.PA", "ZEG.L", "SPM.MI", "VPLAY-B.ST",   # Project2 data.py KNOWN_BAD_SERIES
             "TELIA1.HE", "AF.AS"]   # thin secondary listings in the PIT lists (+92%/-90% single-day prints)
VERIFIED = ["ABVX.PA", "MRNA", "ECHO", "GME"]
REGIONS = ["US", "EU", "UK", "DK", "SC", "WD"]   # SC = SCANDI (STOXX 600 DK+NO+SE+FI)


def _uk_tr():
    C = pd.read_parquet(os.path.join(D, "UK_close.parquet")).sort_index()
    dv = pd.read_parquet(os.path.join(D, "UK_dividends.parquet")).sort_index()
    dv.index = pd.to_datetime(dv.index).tz_localize(None).normalize()
    dv = dv.reindex(columns=C.columns).reindex(C.index).fillna(0.0)   # ex-date aligned to trading day
    Cf = C.ffill()
    r = (Cf + dv) / Cf.shift(1) - 1
    r = r.where(C.notna())
    return r


def _clean(r, tag, low=True):
    """Daily-return guard: known-bad series dropped; r > +100% or r <= -95% set to NaN unless verified."""
    r = r.drop(columns=[c for c in KNOWN_BAD if c in r.columns])
    bad = (r > 1.0) | ((r <= -0.95) if low else False)   # -95% rule only for Yahoo data (GBp/GBP flips); Sharadar keeps real collapses
    for v in VERIFIED:
        if v in bad.columns:
            bad[v] = False
    n = int(bad.values.sum())
    if n:
        print(f"[{tag}] {n} daily returns |r|>100% set to NaN in {int(bad.any().sum())} names")
    return r.mask(bad)


def us_membership(px):
    """Monthly PIT top-500 by market cap (implied shares x price), as lib10/panel.py."""
    f = os.path.join(CACHE, "us_uni.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    fd = pd.read_csv(os.path.join(D, "us_fundamentals.csv"), usecols=["ticker", "calendardate", "date", "marketcap"],
                     parse_dates=["calendardate", "date"]).dropna(subset=["marketcap"])
    fd = fd.sort_values(["ticker", "date"]).drop_duplicates(["ticker", "date"], keep="last")
    pf = px.ffill()
    idx = pf.index.searchsorted(fd.date.values, side="right") - 1
    ok = idx >= 0
    fd = fd[ok].copy(); idx = idx[ok]
    col = {c: i for i, c in enumerate(pf.columns)}
    fd = fd[fd.ticker.isin(col)]
    idx = pf.index.searchsorted(fd.date.values, side="right") - 1
    fd["p_at"] = pf.values[idx, [col[t] for t in fd.ticker]]
    fd["shr"] = fd.marketcap / fd.p_at
    months = px.resample("ME").last().index
    w = fd.pivot_table(index="date", columns="ticker", values="shr", aggfunc="last").reindex(columns=px.columns)
    fdate = pd.DataFrame(np.where(w.notna(), w.index.values[:, None], np.datetime64("NaT")), index=w.index, columns=w.columns)
    u = w.index.union(months)
    shr = w.reindex(u).ffill().reindex(months)
    age = fdate.reindex(u).ffill().reindex(months)
    age = pd.DataFrame(np.repeat(months.values[:, None], px.shape[1], 1), index=months, columns=px.columns) - age.apply(pd.to_datetime)
    shr = shr.where(age <= pd.Timedelta(days=400))
    pm = px.resample("ME").last().where(px.notna().resample("ME").sum() > 0)
    mc = shr * pm
    rk = mc.rank(axis=1, ascending=False, method="first")
    uni = (rk <= 500) & mc.notna()
    out = (uni, mc)
    pd.to_pickle(out, f)
    return out


ART_N = {"US_A": 500, "UK_A": 350, "EU_A": 240, "DK_A": 25}
ART_REGIONS = ["US_A", "EU_A", "UK_A", "DK_A", "WD_A"]
LEGACY_EUR = {"FRF": 6.55957, "ATS": 13.7603, "ESP": 166.386, "BEF": 40.3399, "DEM": 1.95583, "ITL": 1936.27, "NLG": 2.20371, "FIM": 5.94573, "PTE": 200.482, "IEP": 0.787564}


def _art_fx_to_usd(idx):
    """USD per unit, daily, for the ART currencies; EUR before 1999 back-filled with its first value."""
    F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "factors")
    x = pd.read_csv(os.path.join(F, "fx_daily_datasets.csv"), parse_dates=["Date"])
    name = {"EUR": "Euro", "GBP": "United Kingdom", "DKK": "Denmark", "SEK": "Sweden"}
    out = {c: 1 / x[x.Country == n].set_index("Date")["Exchange rate"].astype(float).where(lambda s: s > 0) for c, n in name.items()}
    L = pd.DataFrame(out).sort_index()
    L = L.reindex(L.index.union(idx)).ffill().bfill().reindex(idx)
    L["USD"] = 1.0
    for k, v in LEGACY_EUR.items():
        L[k] = L["EUR"] / v
    return L


def load_art(region):
    """ART extract (Project2 reporting/art_cache), Jan 1998 - Mar 2013, including later-delisted stocks.
    Universe: each month-end the top-N stocks by 63-day average traded value in USD (>= 60 days of history,
    priced in the last 5 days); eligible in month m if in the universe at the end of m-1 (PREREG_FS15.md)."""
    f = os.path.join(CACHE, f"{region}.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    A = os.path.join(D, "art")
    if region == "WD_A":
        parts = [load_art(k) for k in ("US_A", "UK_A", "EU_A")]
        idx = parts[0]["ret"].index.union(parts[1]["ret"].index).union(parts[2]["ret"].index)
        ret = pd.concat([p["ret_usd"].reindex(idx) for p in parts], axis=1)
        elig = pd.concat([p["elig"].reindex(idx).fillna(False) for p in parts], axis=1).astype(bool)
        tv = pd.concat([p["tv_usd"].reindex(idx) for p in parts], axis=1)
        ret = ret.loc[ret.notna().sum(axis=1) >= 0.2 * ret.notna().sum(axis=1).median()]
        elig = elig.reindex(ret.index).fillna(False).astype(bool)
        out = dict(ret=ret, ret_usd=ret, idx=(1 + ret.fillna(0)).cumprod().where(ret.notna().cumsum() > 0), elig=elig & ret.notna(), mcap=None, tv_usd=tv.reindex(ret.index))
        pd.to_pickle(out, f); return out
    k = region[:2]
    P = pd.read_parquet(os.path.join(A, f"art_{k}_totret_daily.parquet")).sort_index(); P = P.where(P > 0)
    T = pd.read_parquet(os.path.join(A, f"art_{k}_turnover_daily.parquet")).sort_index().reindex(index=P.index, columns=P.columns)
    ccy = pd.read_csv(os.path.join(A, f"art_{k}_currency.csv")).set_index("StockId")["Currency"]
    P.columns = [str(c) for c in P.columns]; T.columns = P.columns; ccy.index = [str(c) for c in ccy.index]
    r = P.pct_change(fill_method=None).where(P.notna())
    # bad-tick guard: +50% followed by a -33% reversal the next day (or the mirror) -> both days NaN
    spike = ((r > 0.5) & (r.shift(-1) < -0.33)) | ((r < -0.33) & (r.shift(-1) > 0.5))
    r = r.mask(spike | spike.shift(1, fill_value=False))
    r = _clean(r, region, low=True)
    r = r.loc[r.notna().sum(axis=1) >= max(5, 0.2 * r.notna().sum(axis=1).median())]
    fx = _art_fx_to_usd(r.index)
    cc = ccy.reindex(r.columns).fillna("USD" if k == "US" else {"UK": "GBP", "DK": "DKK", "EU": "EUR"}[k])
    fxm = pd.DataFrame({c: fx[cc[c]] if cc[c] in fx else fx["EUR"] for c in r.columns}, index=r.index)
    tv_usd = (T.reindex(r.index) * fxm).where(lambda x: x > 0)
    ret_usd = ((1 + r) * (1 + fxm.pct_change(fill_method=None).fillna(0)) - 1).where(r.notna())
    hist = r.notna().cumsum() >= 60
    recent = r.notna().rolling(5, min_periods=1).sum() > 0
    avg = tv_usd.rolling(63, min_periods=40).mean().where(hist & recent)
    months = r.resample("ME").last().index
    am = avg.resample("ME").last()
    rk = am.rank(axis=1, ascending=False, method="first")
    uni = (rk <= ART_N[region]) & am.notna()
    elig = uni.shift(1).reindex(r.index, method="ffill").fillna(False).astype(bool)
    out = dict(ret=r, ret_usd=ret_usd, idx=(1 + r.fillna(0)).cumprod().where(r.notna().cumsum() > 0), elig=elig & r.notna(), mcap=None, tv_usd=tv_usd)
    pd.to_pickle(out, f)
    return out


def load(region, pit=True):
    """PIT (default): EU/UK/DK/SC from Wikipedia point-in-time index membership (Project2 cache, see
    _data_private/build_pit.py); WD = US Sharadar PIT + UK PIT + EU PIT. pit=False: the original survivor lists.
    Returns dict: ret (daily TR returns, local ccy), idx (TR index), elig (daily eligibility bool), mcap (US only)."""
    if region.endswith("_A"):
        return load_art(region)
    if pit and region != "US":
        return load_pit(region)
    f = os.path.join(CACHE, f"{region}.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    mc = None
    if region == "US":
        px = pd.read_csv(os.path.join(D, "us_master_universe_prices.csv"), index_col=0, parse_dates=True).sort_index()
        px = px.where(px > 0)
        r = px.pct_change(fill_method=None).where(px.notna())
        uni_m, mc = us_membership(px)
        # member in month m if in top-500 at end of month m-1
        elig = uni_m.shift(1).reindex(px.index, method="ffill").fillna(False).astype(bool)
    else:
        if region == "UK":
            r = _uk_tr()
        else:
            A = pd.read_parquet(os.path.join(D, f"{region}_adjclose.parquet")).sort_index()
            A = A.where(A > 0)
            r = A.pct_change(fill_method=None).where(A.notna())
            if region == "WD":   # replace .L names with the dividend-rebuilt series
                uk = _uk_tr()
                common = [c for c in uk.columns if c in r.columns]
                r[common] = uk[common].reindex(r.index)
        elig = None
    r = _clean(r, region, low=(region != "US")).loc[START:END]
    r = r.loc[r.notna().sum(axis=1) >= max(5, 0.2 * r.shape[1])]    # drop exchange holidays with thin data
    if elig is None:
        # survivor list: eligible once the name has 252 days of history
        elig = r.notna().cumsum() >= 252
    else:
        elig = elig.reindex(r.index).fillna(False).astype(bool)
    idx = (1 + r.fillna(0)).cumprod().where(r.notna().cumsum() > 0)
    out = dict(ret=r, idx=idx, elig=elig & r.notna(), mcap=mc)
    pd.to_pickle(out, f)
    return out


def _uk_tr_from(C):
    dv = pd.read_parquet(os.path.join(D, "UK_dividends.parquet")).sort_index()
    dv.index = pd.to_datetime(dv.index).tz_localize(None).normalize()
    dv = dv.reindex(columns=C.columns).reindex(C.index).fillna(0.0)
    Cf = C.ffill()
    return ((Cf + dv) / Cf.shift(1) - 1).where(C.notna())


CCY = {"DE": "EUR", "MI": "EUR", "PA": "EUR", "MC": "EUR", "AS": "EUR", "HE": "EUR", "BR": "EUR", "LS": "EUR", "ST": "SEK", "CO": "DKK", "WA": "PLN", "L": "GBP"}


def fx_usd_returns(idx):
    """Daily returns of USD per unit of each currency (Fed H.10 via datasets/exchange-rates; PLN from Yahoo, 2015+)."""
    F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "factors")
    x = pd.read_csv(os.path.join(F, "fx_daily_datasets.csv"), parse_dates=["Date"])
    name = {"EUR": "Euro", "GBP": "United Kingdom", "DKK": "Denmark", "SEK": "Sweden"}
    out = {}
    for c, n in name.items():
        s = x[x.Country == n].set_index("Date")["Exchange rate"].astype(float)
        out[c] = 1 / s.where(s > 0)                       # H.10 quotes units per USD for all four
    pl = pd.read_parquet(os.path.join(F, "px_PLNUSD_X.parquet"))["Close"]; pl.index = pd.to_datetime(pl.index).tz_localize(None)
    out["PLN"] = pl
    L = pd.DataFrame(out).sort_index().reindex(idx.union(pd.DatetimeIndex(sorted(set().union(*[v.index for v in out.values()]))))).ffill().reindex(idx)
    return L.pct_change(fill_method=None)


def to_usd(ret):
    """Convert local-currency daily returns to USD, unhedged: (1+r)(1+fx)-1. Names without an FX series (PLN before 2015) stay local."""
    fx = fx_usd_returns(ret.index)
    out = ret.copy()
    for c in ret.columns:
        k = CCY.get(c.split(".")[-1]) if "." in c else None
        if k:
            f = fx[k].reindex(ret.index)
            out[c] = ((1 + ret[c]) * (1 + f.fillna(0)) - 1).where(ret[c].notna())
    return out


def load_pit(region):
    f = os.path.join(CACHE, f"{region}_pit.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    if region == "WD":
        parts = [load("US"), load_pit("UK"), load_pit("EU")]
        idx = parts[0]["ret"].index.union(parts[1]["ret"].index).union(parts[2]["ret"].index)
        ret = pd.concat([p["ret"].reindex(idx) for p in parts], axis=1)
        elig = pd.concat([p["elig"].reindex(idx).fillna(False) for p in parts], axis=1).astype(bool)
        ret = ret.loc[:, ~ret.columns.duplicated()]; elig = elig.loc[:, ~elig.columns.duplicated()]
        ret = to_usd(ret)   # World in one currency (USD, unhedged) since 27 Sep 2026
        ret = ret.loc[ret.notna().sum(axis=1) >= 0.2 * ret.notna().sum(axis=1).median()]
        elig = elig.reindex(ret.index).fillna(False).astype(bool)
        idxp = (1 + ret.fillna(0)).cumprod().where(ret.notna().cumsum() > 0)
        out = dict(ret=ret, idx=idxp, elig=elig & ret.notna(), mcap=None)
        pd.to_pickle(out, f); return out
    A = pd.read_parquet(os.path.join(D, "pit", f"{region}_pit_adjclose.parquet")).sort_index()
    A = A.where(A > 0)
    r = A.pct_change(fill_method=None).where(A.notna())
    if region == "UK":
        C = pd.read_parquet(os.path.join(D, "pit", "UK_pit_close.parquet")).sort_index()
        r = _uk_tr_from(C.where(C > 0))
    r = _clean(r, region + "-PIT").loc[START:END]
    r = r.loc[r.notna().sum(axis=1) >= max(5, 0.2 * r.notna().sum(axis=1).median())]
    m = pd.read_csv(os.path.join(D, "pit", f"members_{region}.csv"), parse_dates=["date"])
    snaps = sorted(m.date.unique())
    mem = pd.DataFrame(False, index=pd.DatetimeIndex(snaps), columns=r.columns)
    for d, g in m.groupby("date"):
        cols = [t for t in g.ticker if t in mem.columns]
        mem.loc[d, cols] = True
    # snapshot at d is effective from the next trading day; before the first snapshot use the first (stated)
    mem = mem.reindex(mem.index.union(r.index)).ffill().bfill().shift(1).bfill().reindex(r.index).fillna(False).astype(bool)
    hist = r.notna().cumsum() >= 60
    out = dict(ret=r, idx=(1 + r.fillna(0)).cumprod().where(r.notna().cumsum() > 0), elig=mem & hist & r.notna(), mcap=None)
    pd.to_pickle(out, f)
    return out


def month_elig(elig):
    """Month-end eligibility that does not depend on the stock trading on the exact last day of the month
    (national holidays such as 24/31 December or Easter would otherwise drop whole markets): eligible if
    eligible on any of the last 5 trading days of the month."""
    e = elig.astype(float).rolling(5, min_periods=1).max().astype(bool)
    return e.groupby(e.index.to_period("M")).last()


if __name__ == "__main__":
    for R in REGIONS:
        o = load(R)
        e = o["elig"].sum(axis=1)
        print(R, o["ret"].shape, o["ret"].index[0].date(), o["ret"].index[-1].date(),
              "eligible names: median", int(e.median()), "min", int(e.iloc[260:].min()), "max", int(e.max()))
