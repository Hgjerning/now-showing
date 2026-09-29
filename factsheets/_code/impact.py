# -*- coding: utf-8 -*-
"""FS16: spread + square-root market impact, as pre-registered in planning/PREREG_FS16.md.
Writes results/impact.json and results/impact.pkl."""
import json
import os

import numpy as np
import pandas as pd

import data
import perf
import xs

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); D = os.path.join(HERE, "..", "data")
U = ["US", "EU", "UK", "DK", "SC", "WD"]
AUMS = [1e6, 1e7, 1e8, 1e9, 1e10]
Y0, Y1 = 0.7, 1.0
BOOKS = {"low beta (beta-neutral)": ("beta", False, True), "12-1 momentum (beta-neutral)": ("mom", True, True),
         "12-1 momentum (L/S)": ("mom", True, False), "low volatility (L/S)": ("vol252", False, False),
         "short-term reversal (L/S)": ("r1", False, False), "low MAX (L/S)": ("max1", False, False)}
SHORT = ["low beta (beta-neutral)", "12-1 momentum (beta-neutral)"]


def adv_usd(R):
    """Monthly (Period) 63-day ADV in USD, stocks in columns."""
    if R == "WD":
        return pd.concat([adv_usd(k) for k in ("US", "UK", "EU")], axis=1).T.groupby(level=0).first().T
    if R == "US":
        tv = pd.read_parquet(os.path.join(D, "pit", "US_tradedvalue.parquet")).sort_index()
        a = tv.where(tv > 0).rolling(63, min_periods=40).mean(); a = a.groupby(a.index.to_period("M")).last()
        mc = data.load("US")["mcap"].copy(); mc.index = mc.index.to_period("M")
        a = a.reindex(index=mc.index, columns=mc.columns)
        ratio = a / mc
        q = mc.rank(axis=1, pct=True).apply(lambda r: np.ceil(r * 5).clip(1, 5))
        fill = pd.DataFrame(np.nan, index=mc.index, columns=mc.columns)
        for t in mc.index:
            med = ratio.loc[t].groupby(q.loc[t]).median()
            fill.loc[t] = mc.loc[t] * q.loc[t].map(med)
        return a.fillna(fill)
    tv = pd.read_parquet(os.path.join(D, "pit", f"{R}_pit_tradedvalue.parquet")).sort_index()
    tv.index = pd.to_datetime(tv.index).tz_localize(None) if getattr(tv.index, "tz", None) else pd.to_datetime(tv.index)
    usd = data.to_usd.__globals__["fx_usd_returns"]  # returns only; build levels below
    F = os.path.join(HERE, "..", "factors"); x = pd.read_csv(os.path.join(F, "fx_daily_datasets.csv"), parse_dates=["Date"])
    name = {"EUR": "Euro", "GBP": "United Kingdom", "DKK": "Denmark", "SEK": "Sweden"}
    lv = pd.DataFrame({c: 1 / x[x.Country == n].set_index("Date")["Exchange rate"].astype(float).where(lambda s: s > 0) for c, n in name.items()})
    pl = pd.read_parquet(os.path.join(F, "px_PLNUSD_X.parquet"))["Close"]; pl.index = pd.to_datetime(pl.index).tz_localize(None) if getattr(pl.index, "tz", None) else pd.to_datetime(pl.index)
    lv["PLN"] = pl; lv = lv.sort_index().reindex(lv.index.union(tv.index)).ffill().bfill().reindex(tv.index)
    ccy = {c: data.CCY.get(c.split(".")[-1], "EUR") if "." in c else "USD" for c in tv.columns}
    fxm = pd.DataFrame({c: (lv[ccy[c]] if ccy[c] in lv else 1.0) for c in tv.columns}, index=tv.index)
    if R == "UK":
        fxm = fxm / 100.0   # LSE prices in pence
    tvu = (tv * fxm).where(tv > 0)
    a = tvu.rolling(63, min_periods=40).mean()
    return a.groupby(a.index.to_period("M")).last()


def half_spread(adv):
    return (0.0005 * (adv / 5e7) ** -0.3).clip(0.0002, 0.005)


def book_costs(I, sig, lh, bn, ADV, buffer=False):
    rec = []; P = xs.run(I, sig, lh, beta_neutral=bn, record=rec, buffer=buffer)
    vol = I["S"]["vol"]
    prev_g, prev_b = pd.Series(dtype=float), pd.Series(dtype=float)
    rows = {}
    for (t, wg, wb) in rec:
        dg = wg.subtract(prev_g, fill_value=0).abs(); db = wb.subtract(prev_b, fill_value=0).abs(); prev_g, prev_b = wg, wb
        dw = dg.add(db, fill_value=0); dw = dw[dw > 0]
        a = ADV.loc[t].reindex(dw.index) if t in ADV.index else pd.Series(np.nan, index=dw.index)
        a = a.fillna(a.median() if a.notna().any() else 5e7)
        sg = vol.loc[t].reindex(dw.index).fillna(vol.loc[t].median()) if t in vol.index else pd.Series(0.02, index=dw.index)
        sp = half_spread(a)
        out = {"spread": float((dw * sp).sum())}
        for K in AUMS:
            part = K * dw / a
            out[f"imp07_{K:.0e}"] = float((dw * Y0 * sg * np.sqrt(part)).sum()); out[f"imp10_{K:.0e}"] = float((dw * Y1 * sg * np.sqrt(part)).sum())
            out[f"part_{K:.0e}"] = float(part.median())
        rows[(t + 1).to_timestamp("M")] = out
    C = pd.DataFrame(rows).T.reindex(P.index)
    base = P.ls_gross - P.borrow - P.fin
    return P, C, base


def cap(sh, grid):
    """Size where Sharpe halves vs the smallest size, and where it reaches zero (log-linear)."""
    s0 = sh[0]; res = {}
    for key, target in (("half", s0 / 2), ("zero", 0.0)):
        val = None
        if s0 > target:
            for i in range(1, len(sh)):
                if sh[i] <= target:
                    x0, x1 = np.log10(grid[i - 1]), np.log10(grid[i]); y0, y1 = sh[i - 1], sh[i]
                    val = float(10 ** (x0 + (target - y0) * (x1 - x0) / (y1 - y0))); break
            if val is None:
                val = float("inf")
        res[key] = val
    return res


def run():
    out, ser = {}, {}
    for R in U:
        I = xs.inputs(R); ADV = adv_usd(R); out[R] = {}; ser[R] = {}
        nets = {}
        for name, (sig, lh, bn) in BOOKS.items():
            P, C, base = book_costs(I, sig, lh, bn, ADV)
            flat = P.ls_net
            res = dict(flat=dict(ann=float(flat.mean() * 12), sharpe=perf.sharpe(flat.dropna())), spread_cost=float(C.spread.mean() * 12))
            for Y in ("07", "10"):
                sh, ann, cst = [], [], []
                for K in AUMS:
                    n = (base - C.spread - C[f"imp{Y}_{K:.0e}"]).dropna(); sh.append(perf.sharpe(n)); ann.append(float(n.mean() * 12))
                    cst.append(float((C.spread + C[f"imp{Y}_{K:.0e}"]).mean() * 12))
                    if Y == "07":
                        nets[(name, K)] = n
                res[f"Y{Y}"] = dict(sharpe=sh, ann=ann, cost=cst, capacity=cap(sh, AUMS))
            res["participation"] = [float(C[f"part_{K:.0e}"].median()) for K in AUMS]
            res["turnover"] = float((P.to_good + P.to_bad).mean())
            out[R][name] = res
            print(R, name, "flat", round(res["flat"]["sharpe"], 2), "impact", [round(x, 2) for x in res["Y07"]["sharpe"]], flush=True)
        # the shortlist: equal weights of its two legs
        res = {"Y07": {"sharpe": [], "ann": []}}
        for K in AUMS:
            n = pd.concat([nets[(SHORT[0], K)], nets[(SHORT[1], K)]], axis=1).mean(axis=1).dropna()
            res["Y07"]["sharpe"].append(perf.sharpe(n)); res["Y07"]["ann"].append(float(n.mean() * 12)); ser[R][K] = n
        res["Y07"]["capacity"] = cap(res["Y07"]["sharpe"], AUMS)
        out[R]["shortlist"] = res
    out["aums"] = AUMS; out["books"] = list(BOOKS)
    json.dump(out, open(os.path.join(RES, "impact.json"), "w"), indent=1, default=float)
    pd.to_pickle(ser, os.path.join(RES, "impact.pkl"))
    return out


if __name__ == "__main__":
    run()


def run_liquid(min_adv=5e6):
    """Exploratory (not pre-registered): drop stocks with ADV below min_adv before sorting, shortlist books only."""
    out = {}
    for R in U:
        I = xs.inputs(R); ADV = adv_usd(R)
        ok = (ADV.reindex(index=I["E"].index, columns=I["E"].columns) >= min_adv)
        for k in list(I["S"]):
            I["S"][k] = I["S"][k].where(ok.reindex(index=I["S"][k].index, columns=I["S"][k].columns).fillna(False).astype(bool))
        nets = {}
        for name in SHORT:
            sig, lh, bn = BOOKS[name]; P, C, base = book_costs(I, sig, lh, bn, ADV)
            for K in AUMS:
                nets[(name, K)] = (base - C.spread - C[f"imp07_{K:.0e}"]).dropna()
        sh, ann = [], []
        for K in AUMS:
            n = pd.concat([nets[(SHORT[0], K)], nets[(SHORT[1], K)]], axis=1).mean(axis=1).dropna(); sh.append(perf.sharpe(n)); ann.append(float(n.mean() * 12))
        out[R] = dict(sharpe=sh, ann=ann, capacity=cap(sh, AUMS), n_med=int(ok.sum(axis=1).loc["2013":].median()))
        print("liquid", R, [round(x, 2) for x in sh], out[R]["capacity"], out[R]["n_med"], flush=True)
    json.dump(out, open(os.path.join(RES, "impact_liquid.json"), "w"), indent=1, default=float)
    return out


if __name__ == "__main__" and False:
    pass


def run_buffer():
    """Exploratory (not pre-registered): the shortlist with the FS03-FS12 turnover buffer (hold a stock until it leaves the top 3/q)."""
    out = {}
    for R in U:
        I = xs.inputs(R); ADV = adv_usd(R); nets = {}; to = []
        for name in SHORT:
            sig, lh, bn = BOOKS[name]; P, C, base = book_costs(I, sig, lh, bn, ADV, buffer=True); to.append(float((P.to_good + P.to_bad).mean()))
            for K in AUMS:
                nets[(name, K)] = (base - C.spread - C[f"imp07_{K:.0e}"]).dropna()
        sh, ann = [], []
        for K in AUMS:
            n = pd.concat([nets[(SHORT[0], K)], nets[(SHORT[1], K)]], axis=1).mean(axis=1).dropna(); sh.append(perf.sharpe(n)); ann.append(float(n.mean() * 12))
        out[R] = dict(sharpe=sh, ann=ann, capacity=cap(sh, AUMS), turnover=float(np.mean(to)))
        print("buffer", R, [round(x, 2) for x in sh], out[R]["capacity"], round(out[R]["turnover"], 2), flush=True)
    json.dump(out, open(os.path.join(RES, "impact_buffer.json"), "w"), indent=1, default=float)
    return out
