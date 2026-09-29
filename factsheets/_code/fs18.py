# -*- coding: utf-8 -*-
"""FS18: the portfolio I would actually run, as pre-registered in planning/PREREG_FS18.md.
Market (size-weighted, long-only) + a vol-targeted overlay of beta-neutral, buffered books net of the FS16 cost model.
Writes results/fs18.json and results/fs18.pkl."""
import json
import os
import sys

import numpy as np
import pandas as pd

import borrow as BR
import impact as IM
import perf
import xs

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results")
U = ["US", "EU", "UK", "DK", "SC", "WD"]
POOL = ["US", "EU", "UK", "DK", "SC"]
KS = [5e7, 2.5e8]
BOOKS = {"low beta": ("beta", False), "12-1 momentum": ("mom", True)}
US_EXTRA = {"profit growth": ("c_profit_growth", True), "debt issuance": ("c_debt_issuance", True)}
TARGET, CAP = 0.05, 3.0


def books(R):
    I = xs.inputs(R)
    bk = dict(BOOKS)
    if R == "US":
        import fundamentals as FU
        I["S"].update(FU.build()); bk.update(US_EXTRA)
    ADV = IM.adv_usd(R); IM.AUMS = KS
    nets = {K: {} for K in KS}; turn = {}
    for name, (sig, lh) in bk.items():
        P, C, base = IM.book_costs(I, sig, lh, True, ADV, buffer=True)
        turn[name] = float((P.to_good + P.to_bad).mean())
        for K in KS:
            nets[K][name] = (base - C.spread - C[f"imp07_{K:.0e}"])
        print(R, name, "net@50m ann", round(float(nets[KS[0]][name].mean() * 12), 4), flush=True)
    return I, nets, turn


def overlay(B):
    """B: DataFrame of book returns. Inverse 36m vol weights (equal until 36 months), then scaled to 5% vol on trailing 12m."""
    B = B.dropna(how="all")
    iv = 1 / B.rolling(36, min_periods=36).std().shift(1)
    w = iv.div(iv.sum(axis=1), axis=0)
    eq = B.notna().astype(float); eq = eq.div(eq.sum(axis=1), axis=0)
    ok = iv.notna().all(axis=1)
    w = w.where(pd.DataFrame(np.repeat(ok.values[:, None], w.shape[1], axis=1), index=w.index, columns=w.columns), eq)
    raw = (w * B.fillna(0)).sum(axis=1)
    vol = raw.rolling(12, min_periods=12).std().shift(1) * np.sqrt(12)
    scale = (TARGET / vol).clip(upper=CAP)
    return (scale * raw).dropna(), raw, scale.dropna(), w


def mdd(r):
    c = (1 + r).cumprod(); return float((c / c.cummax() - 1).min())


def main():
    rf = BR.rf_monthly()
    out, ser = {"markets": {}}, {}
    for R in U:
        I, nets, turn = books(R)
        mk = xs.size_weighted(I)
        r_f = pd.Series(rf.reindex(mk.index.to_period("M")).values, index=mk.index).fillna(0)
        res = {"books": list(nets[KS[0]]), "turnover": turn}
        for K in KS:
            B = pd.DataFrame(nets[K]); ov, raw, scale, w = overlay(B)
            idx = ov.index.intersection(mk.index)
            m_ex = (mk - r_f).reindex(idx); o = ov.reindex(idx); port_ex = m_ex + o
            bk = {n: dict(ann=float(B[n].dropna().mean() * 12), sharpe=perf.sharpe(B[n].dropna())) for n in B}
            d = dict(start=str(idx[0].date()), end=str(idx[-1].date()), n=len(idx),
                     overlay=dict(ann=float(o.mean() * 12), vol=float(o.std() * np.sqrt(12)), sharpe=perf.sharpe(o), t=perf.nw_t(o)["t"], mdd=mdd(o),
                                  corr_market=float(o.corr(m_ex)), scale_mean=float(scale.reindex(idx).mean())),
                     market=dict(ann=float(m_ex.mean() * 12), sharpe=perf.sharpe(m_ex), mdd=mdd(mk.reindex(idx))),
                     portfolio=dict(ann=float(port_ex.mean() * 12), sharpe=perf.sharpe(port_ex), mdd=mdd((port_ex + r_f.reindex(idx)))),
                     books=bk, weights_last=w.iloc[-1].round(3).to_dict())
            d["sharpe_diff"] = d["portfolio"]["sharpe"] - d["market"]["sharpe"]
            res[f"{K:.0e}"] = d; ser[(R, K)] = pd.DataFrame(dict(market_ex=m_ex, overlay=o, portfolio_ex=port_ex, rf=r_f.reindex(idx)))
            print(R, f"{K:.0e}", "overlay SR", round(d["overlay"]["sharpe"], 2), "mkt SR", round(d["market"]["sharpe"], 2), "port SR", round(d["portfolio"]["sharpe"], 2), flush=True)
        out["markets"][R] = res
    # primary: pooled mean monthly overlay across the five markets (equal weight per month over those available)
    for K in KS:
        O = pd.DataFrame({R: ser[(R, K)]["overlay"] for R in POOL}); pooled = O.mean(axis=1).dropna()
        nw = perf.nw_t(pooled)
        sub = {p: dict(ann=float(pooled.loc[a:b].mean() * 12), t=perf.nw_t(pooled.loc[a:b])["t"]) for p, (a, b) in {"2013-19": ("2013", "2019"), "2020-26": ("2020", "2026")}.items()}
        c = O.corr().values; neff = float(len(POOL) ** 2 / np.nansum(c))
        out[f"pooled_{K:.0e}"] = dict(ann=float(pooled.mean() * 12), t=nw["t"], sharpe=perf.sharpe(pooled), sub=sub, n_eff=neff, start=str(pooled.index[0].date()))
        ser[("pooled", K)] = pooled
    p = out["pooled_5e+07"]
    out["passed"] = bool(p["t"] > 2 and all(v["ann"] > 0 for v in p["sub"].values()))
    out["ks"] = KS
    json.dump(out, open(os.path.join(RES, "fs18.json"), "w"), indent=1, default=float)
    pd.to_pickle(ser, os.path.join(RES, "fs18.pkl"))
    print("PRIMARY", p, "passed", out["passed"])


if __name__ == "__main__":
    main()
