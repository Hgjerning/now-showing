# -*- coding: utf-8 -*-
"""REPORTING ONLY since 27 Sep 2026 (the charge itself is applied inside xs.run). Financing charge for the beta-neutral books: net cash borrowed = 1/beta_good - 1/beta_bad (per unit of each leg),
charged at the USD risk-free rate (French RF) plus a 50 bp spread. Writes results/financing.json."""
import json
import os

import numpy as np
import pandas as pd

import perf
import xs
from battery import DIRECTION, SIGS

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; SPREAD = 0.005


def rf_monthly():
    f = pd.read_csv(os.path.join(HERE, "..", "factors", "french_developed_5f_daily.csv"), index_col=0, parse_dates=True)["RF"]
    return (1 + f).groupby(f.index.to_period("M")).prod() - 1


def charge(I, sig, lh, rf):
    S, B = I["S"][sig], I["S"]["beta"]; months = [t for t in S.index if xs.START <= t <= xs.END]
    q = xs.nq(np.median([S.loc[t].notna().sum() for t in months])); out = {}
    for t in months:
        s = S.loc[t].dropna()
        if len(s) < 15:
            continue
        pct = s.rank(pct=True, method="first"); pct = pct if lh else 1 - pct + 1 / len(pct)
        g = s.index[pct > 1 - 1 / q]; b = s.index[pct <= 1 / q]
        bg = float(B.loc[t, g].clip(0.2, 3).mean()); bb = float(B.loc[t, b].clip(0.2, 3).mean())
        if not (np.isfinite(bg) and np.isfinite(bb)):
            continue
        net = 1 / bg - 1 / bb; r = rf.get(t + 1, np.nan)
        out[(t + 1).to_timestamp("M")] = (net, net * (r + SPREAD / 12) if net > 0 else net * r)
    return pd.DataFrame(out, index=["net_cash", "charge"]).T


if __name__ == "__main__":
    rf = rf_monthly(); Bt = pd.read_pickle(os.path.join(RES, "battery_price.pkl")); J = {}; CH = {R: {} for R in U}; IN = {R: xs.inputs(R) for R in U}
    for s in SIGS:
        J[s] = {}
        for R in U:
            I = IN[R]; c = charge(I, s, DIRECTION[s][0], rf); CH[R][s] = c["charge"]
            bn = Bt[R][s].bn_net; adj = bn.dropna()
            J[s][R] = dict(net_cash=float(c.net_cash.mean()), charge=float(c.charge.mean() * 12), bn_fin_ann=float(adj.mean() * 12), bn_fin_sharpe=perf.sharpe(adj))
        df = pd.DataFrame({R: Bt[R][s].bn_net for R in U}).dropna()
        x = df.mean(axis=1); J[s]["pooled"] = dict(ann=float(x.mean() * 12), sharpe=perf.sharpe(x), t=perf.nw_t(x)["t"], pos=int((df.mean() > 0).sum()))
        print(s, {R: round(J[s][R]["net_cash"], 2) for R in U}, J[s]["pooled"], flush=True)
    json.dump(J, open(os.path.join(RES, "financing.json"), "w"), indent=1); pd.to_pickle(CH, os.path.join(RES, "financing_charges.pkl"))
