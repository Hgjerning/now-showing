# -*- coding: utf-8 -*-
"""A31 reported extension: wide feature set (REPORTED_EXTENSION_WIDE_FEATURES_2026-10-06.md).
Price features computed in column chunks (float32). Fundamental ratios from a standardised as-of table."""

import numpy as np, pandas as pd

PRICE_X = ["mom6", "mom36", "chmom", "season", "retvol", "idiovol", "betasq", "skew252", "skew21", "minret",
           "rsi14", "dsma50", "dsma200", "macdh", "z21"]


def _rsi(p, n=14):
    d = p.diff(); up = d.clip(lower=0); dn = -d.clip(upper=0)
    au = up.ewm(alpha=1 / n, adjust=False, min_periods=n).mean(); ad = dn.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + au / ad)


def price_wide(px, pm, months, chunk=1500):
    """px daily prices (float32), pm month-end prices. Returns dict name -> monthly DataFrame."""
    # equal-weight market from all names
    s = None; c = None
    for i in range(0, px.shape[1], chunk):
        d = px.iloc[:, i:i + chunk].pct_change(fill_method=None); d = d.where(d.abs() < 1.0)
        a, b = d.sum(axis=1, min_count=1).fillna(0), d.notna().sum(axis=1)
        s = a if s is None else s + a; c = b if c is None else c + b
    mkt = (s / c.replace(0, np.nan)).astype("float64")
    em = mkt.rolling(252, min_periods=200).mean(); vm = mkt.rolling(252, min_periods=200).var(ddof=0)
    F = {k: [] for k in ["retvol", "idiovol", "beta", "skew252", "skew21", "minret", "rsi14", "dsma50", "dsma200", "macdh", "z21"]}
    for i in range(0, px.shape[1], chunk):
        p = px.iloc[:, i:i + chunk]
        dr = p.pct_change(fill_method=None); dr = dr.where(dr.abs() < 1.0)
        ME = lambda x: x.resample("ME").last()
        F["retvol"].append(ME(dr.rolling(21, min_periods=15).std()))
        mm = mkt.to_numpy()[:, None]; xy = (dr.fillna(0) * mm).where(dr.notna())
        ex = dr.rolling(252, min_periods=200).mean(); exy = xy.rolling(252, min_periods=200).mean()
        beta = (exy.sub(ex.mul(em, axis=0))).div(vm, axis=0)
        alpha = ex.sub(beta.mul(em, axis=0))
        # idiosyncratic variance = var(r) - beta^2 var(m)  (252-day, population)
        vr = dr.rolling(252, min_periods=200).var(ddof=0)
        F["idiovol"].append(ME(np.sqrt((vr - beta ** 2 * vm.to_numpy()[:, None]).clip(lower=0))))
        F["beta"].append(ME(beta))
        F["skew252"].append(ME(dr.rolling(252, min_periods=200).skew()))
        F["skew21"].append(ME(dr.rolling(21, min_periods=15).skew()))
        F["minret"].append(dr.resample("ME").min())
        pf = p.ffill(limit=5)
        F["rsi14"].append(ME(_rsi(pf)))
        F["dsma50"].append(ME(pf / pf.rolling(50, min_periods=40).mean() - 1))
        F["dsma200"].append(ME(pf / pf.rolling(200, min_periods=160).mean() - 1))
        e12, e26 = pf.ewm(span=12, adjust=False, min_periods=26).mean(), pf.ewm(span=26, adjust=False, min_periods=26).mean()
        macd = e12 - e26; F["macdh"].append(ME((macd - macd.ewm(span=9, adjust=False).mean()) / pf))
        F["z21"].append(ME((pf - pf.rolling(21, min_periods=15).mean()) / pf.rolling(21, min_periods=15).std()))
        del dr, xy, ex, exy, beta, alpha, vr, pf
        print("wide price chunk", i, flush=True)
    F = {k: pd.concat(v, axis=1).reindex(months).where(pm.notna()) for k, v in F.items()}
    F["betasq"] = F.pop("beta") ** 2
    F["mom6"] = pm.shift(1) / pm.shift(6) - 1
    F["mom36"] = pm.shift(13) / pm.shift(36) - 1
    F["chmom"] = F["mom6"] - (pm.shift(7) / pm.shift(12) - 1)
    F["season"] = pm.shift(11) / pm.shift(12) - 1
    return {k: F[k] for k in PRICE_X}


def ratio(a, b):
    return a / b.where(b.abs() > 0)


def fund_wide(G, mc):
    """G: dict of monthly as-of DataFrames (same shape as mc); keys among rev, ni, gp, ebit, cfo, capex, div, rnd, sgna,
    dep, assets, equity, debt, cash, ca, cl, ppe, inv, rec, liab, intang, shares and *_ly (one year earlier).
    Numerators divided by mc must be in the price currency. A feature is skipped if any input is missing."""
    pos = lambda x: x.where(x > 0)
    SPEC = {
        "sp": (["rev"], lambda g: ratio(g["rev"], mc)),
        "cfp": (["cfo"], lambda g: ratio(g["cfo"], mc)),
        "dy": (["div"], lambda g: ratio(g["div"].abs(), mc)),
        "lev": (["debt"], lambda g: ratio(g["debt"], mc)),
        "roa": (["ni", "assets"], lambda g: ratio(g["ni"], g["assets"])),
        "roe": (["ni", "equity"], lambda g: ratio(g["ni"], pos(g["equity"]))),
        "opa": (["ebit", "assets"], lambda g: ratio(g["ebit"], g["assets"])),
        "gm": (["gp", "rev"], lambda g: ratio(g["gp"], pos(g["rev"]))),
        "sgr": (["rev", "rev_ly"], lambda g: ratio(g["rev"], pos(g["rev_ly"])) - 1),
        "dni": (["ni", "ni_ly", "assets_ly"], lambda g: ratio(g["ni"] - g["ni_ly"], g["assets_ly"])),
        "acc": (["ni", "cfo", "assets"], lambda g: ratio(g["ni"] - g["cfo"], g["assets"])),
        "capexa": (["capex", "assets"], lambda g: ratio(g["capex"].abs(), g["assets"])),
        "currat": (["ca", "cl"], lambda g: ratio(g["ca"], g["cl"])),
        "casha": (["cash", "assets"], lambda g: ratio(g["cash"], g["assets"])),
        "chcsho": (["shares", "shares_ly"], lambda g: ratio(g["shares"], g["shares_ly"]) - 1),
        "lgr": (["liab", "liab_ly"], lambda g: ratio(g["liab"], g["liab_ly"]) - 1),
        "chinv": (["inv", "inv_ly", "assets"], lambda g: ratio(g["inv"] - g["inv_ly"], g["assets"])),
        "rdm": (["rnd"], lambda g: ratio(g["rnd"], mc)),
        "sgas": (["sgna", "rev"], lambda g: ratio(g["sgna"], pos(g["rev"]))),
        "chgm": (["gp", "rev", "gp_ly", "rev_ly"], lambda g: ratio(g["gp"], pos(g["rev"])) - ratio(g["gp_ly"], pos(g["rev_ly"]))),
        "recs": (["rec", "rev"], lambda g: -ratio(g["rec"], pos(g["rev"]))),
        "tanga": (["intang", "assets"], lambda g: 1 - ratio(g["intang"], g["assets"])),
        "depr": (["dep", "ppe"], lambda g: ratio(g["dep"], g["ppe"])),
    }
    return {k: f(G).astype("float64") for k, (need, f) in SPEC.items() if all(G.get(n) is not None for n in need)}
