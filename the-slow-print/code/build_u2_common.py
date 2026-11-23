# -*- coding: utf-8 -*-
"""Helpers for the A31 wide-feature builds. U2 price/FX/as-of logic is identical to build_u2.py."""
import numpy as np, pandas as pd
from universes import clean_yahoo, snapshot_membership
D = "/mnt/user-data/uploads/ClaudeCode/Project10_Articles/Factsheets/_data_private"
CCY = {"DE": "EUR", "PA": "EUR", "AS": "EUR", "MC": "EUR", "MI": "EUR", "HE": "EUR", "BR": "EUR", "LS": "EUR",
       "ST": "SEK", "CO": "DKK", "WA": "PLN"}
FIRST_OOS = {"U1": "2004-01-31", "U2": "2017-01-31", "U3": "2017-01-31"}


def _fx():
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
    return S


FX = None


def to_eur(c, idx):
    global FX
    FX = FX or _fx()
    eur = FX["EUR"].reindex(FX["EUR"].index.union(idx)).ffill().reindex(idx)
    if c == "EUR": return pd.Series(1.0, index=idx)
    if c == "USD": return 1 / eur
    s = FX.get(c)
    if s is None: return pd.Series(np.nan, index=idx)
    s = s.reindex(s.index.union(idx)).ffill().reindex(idx)
    s[idx < FX[c].index[0]] = np.nan
    return s / eur


def prices():
    raw = pd.read_parquet(f"{D}/pit/EU_pit_adjclose_tr.parquet").sort_index(); raw.index = pd.to_datetime(raw.index).astype("datetime64[ns]")
    px, info = clean_yahoo(raw)
    M, _ = snapshot_membership(px.index, list(px.columns), pd.read_csv(f"{D}/pit/members_EU.csv"))
    M = pd.DataFrame(M, index=px.index, columns=px.columns)
    sfx = pd.Series({t: t.split(".")[-1] for t in px.columns})
    mult = pd.DataFrame({t: to_eur(CCY.get(sfx[t], "EUR"), px.index) for t in px.columns})
    pxe = px * mult
    pm = pxe.resample("ME").last().where(pxe.notna().resample("ME").sum() > 0)
    months = pm.index
    uni = M.resample("ME").last().reindex(months).fillna(False).astype(bool) & pm.notna()
    return px, pxe, pm, months, uni, px.columns


def fundamentals_table(tick):
    fd = pd.read_parquet(f"{D}/eodhd_fundamentals/eu_fund_long.parquet")
    fd = fd[fd.region == "EU"].copy(); fd = fd[fd.ticker.isin(tick)]
    gpx = pd.read_parquet(f"{D}/_staging/eu_grossprofit.parquet").drop_duplicates(["ticker", "freq", "period_end"])
    fd = fd.merge(gpx, on=["ticker", "freq", "period_end"], how="left")
    return fd.sort_values(["ticker", "period_end", "avail_date"])


def add_ttm(fd, flows):
    """TTM: four consecutive quarters (span 250-300 days) or the annual figure. Returns the stacked Q+Y table."""
    q = fd[fd.freq == "Q"].drop_duplicates(["ticker", "period_end"], keep="last").copy()
    y = fd[fd.freq == "Y"].drop_duplicates(["ticker", "period_end"], keep="last").copy()
    gq = q.groupby("ticker", group_keys=False); span = (q.period_end - gq.period_end.shift(3)).dt.days
    for k, c in flows.items():
        q[k] = gq[c].rolling(4, min_periods=4).sum().reset_index(level=0, drop=True).where(span.between(250, 300))
        y[k] = y[c]
    R = pd.concat([q, y]).sort_values(["ticker", "avail_date", "period_end"])
    return R.rename(columns={"avail_date": "date"})


def add_ly(R, cols):
    """value from the record whose period end is 320-410 days earlier (any frequency), as build_u2 assets_ly."""
    out = {c + "_ly": np.full(len(R), np.nan) for c in cols}
    R = R.reset_index(drop=True)
    for t, g in R.groupby("ticker"):
        g = g.sort_values("period_end"); pe = g.period_end.values; ix = g.index.values
        for i in range(len(g)):
            d = (pe[i] - pe) / np.timedelta64(1, "D"); k = np.where((d >= 320) & (d <= 410))[0]
            if len(k):
                for c in cols:
                    vals = g[c].values[k]; vals = vals[~np.isnan(vals)]
                    if len(vals): out[c + "_ly"][ix[i]] = vals[-1]
    for c, v in out.items():
        R[c] = v
    return R


def asof_monthly(fd, col, months, tickers, maxage=550):
    w = fd.dropna(subset=[col]).pivot_table(index="date", columns="ticker", values=col, aggfunc="last").reindex(columns=tickers)
    idx = w.index.union(months)
    v = w.reindex(idx).ffill().reindex(months)
    fdate = pd.DataFrame(np.where(w.notna(), w.index.values[:, None], np.datetime64("NaT", "ns")), index=w.index, columns=w.columns)
    fdate = fdate.reindex(idx).ffill().reindex(months)
    age = pd.DataFrame(np.repeat(months.values[:, None], len(tickers), 1), index=months, columns=tickers) - fdate.apply(pd.to_datetime)
    return v.where(age <= pd.Timedelta(days=maxage))


def eur_of(v, ccyf, months):
    out = v * np.nan
    for c in ["EUR", "SEK", "DKK", "PLN", "USD", "CHF", "GBP"]:
        out = out.where(ccyf != c, v.mul(to_eur(c, months), axis=0))
    return out


def finish(L, F, uni, OUT, code):
    """Stack wide features onto the ranked core panel; drop features with <50% mean OOS coverage; rank to [-0.5, 0.5]."""
    idx = L.index; extra = {}
    for k, v in F.items():
        s = v.where(uni).stack(future_stack=True); s.index.names = ["month", "ticker"]
        extra[k] = s.reindex(idx)
    X = pd.DataFrame(extra, index=idx)
    oos = X.index.get_level_values(0) >= pd.Timestamp(FIRST_OOS[code])
    cov = X[oos].notna().groupby(level=0).mean()
    cmean = cov.mean().sort_values()
    keep = list(cmean[cmean >= 0.5].index); drop = list(cmean[cmean < 0.5].index)
    cov.to_csv(f"{OUT}/coverage_{code}_wide.csv")
    g = X[keep].groupby(level=0)
    for k in keep:
        L["x_" + k] = (g[k].rank(pct=True) - 0.5).fillna(0.0).astype("float32")
    L.to_pickle(f"{OUT}/long_{code}_wide.pkl")
    print("coverage (OOS mean):"); print(cmean.round(3).to_string())
    print("kept", len(keep), "dropped", drop, "total features", 12 + len(keep)); print("DONE")
