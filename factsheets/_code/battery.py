# -*- coding: utf-8 -*-
"""Price battery: every library signal, pre-declared direction, same engine (xs.run), six universes.
Writes results/battery_price.pkl (monthly series) and results/battery_price.json (stats).
Directions are fixed from the literature BEFORE looking at results (see DIRECTION and REF)."""
import json
import os
import sys

import numpy as np
import pandas as pd

import data
import perf
import xs

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
U = data.REGIONS
# signal: (long_high, family, label, source of the direction)
DIRECTION = {
    "max1":   (False, "Lottery & tails", "Low MAX (1 day)", "Bali, Cakici & Whitelaw 2011"),
    "max5":   (False, "Lottery & tails", "Low MAX (5 days)", "Bali, Cakici & Whitelaw 2011"),
    "min1":   (True,  "Lottery & tails", "Mild worst day (MIN)", "low-risk convention: small crashes"),
    "min5":   (True,  "Lottery & tails", "Mild worst 5 days", "low-risk convention"),
    "range":  (False, "Lottery & tails", "Narrow daily range", "low-risk convention"),
    "asym":   (False, "Lottery & tails", "Low net tail", "Boyer, Mitton & Vorkink 2010 (low skew)"),
    "skew":   (False, "Lottery & tails", "Low skewness", "Boyer, Mitton & Vorkink 2010"),
    "ivol":   (False, "Low risk", "Low idiosyncratic vol", "Ang, Hodrick, Xing & Zhang 2006"),
    "vol":    (False, "Low risk", "Low volatility (63d)", "Blitz & van Vliet 2007"),
    "vol252": (False, "Low risk", "Low volatility (252d)", "Blitz & van Vliet 2007"),
    "beta":   (False, "Low risk", "Low beta", "Frazzini & Pedersen 2014"),
    "r1":     (False, "Reversal", "Short-term reversal", "Jegadeesh 1990"),
    "mom":    (True,  "Momentum", "Momentum 12-1", "Jegadeesh & Titman 1993"),
    "resmom": (True,  "Momentum", "Residual momentum", "Blitz, Huij & Martens 2011"),
    "seas":   (True,  "Seasonality", "Same-month seasonality", "Heston & Sadka 2008"),
    "hi52":   (True,  "Momentum", "Near 52-week high", "George & Hwang 2004"),
    "lo52":   (True,  "Momentum", "Far above 52-week low", "momentum-consistent (falling knife loses)"),
    "brk55":  (True,  "Momentum", "Near 55-day high", "Turtle breakout, cross-sectional"),
    "size":   (False, "Size", "Small size", "Banz 1981"),
}
SIGS = list(DIRECTION)


def one(R):
    I = xs.inputs(R); out = {}
    for s in SIGS:
        lh = DIRECTION[s][0]
        P0 = xs.run(I, s, lh); P1 = xs.run(I, s, lh, beta_neutral=True)
        out[s] = pd.DataFrame(dict(ls_net=P0.ls_net, ls_gross=P0.ls_gross, lo_net=P0.good_net, ew=P0.ew, cost=P0.cost,
                                   to=P0.to_good + P0.to_bad, bn_net=P1.ls_net.reindex(P0.index)))
        print(R, s, flush=True)
    return out


def stats(df):
    s = df.ls_net.dropna(); ew = df.ew.reindex(s.index); b = df.bn_net.dropna(); lo = df.lo_net.dropna()
    reg = perf.nw_ols(s.values, ew.values, 6); regl = perf.nw_ols(lo.values, df.ew.reindex(lo.index).values, 6)
    return dict(ann=float(s.mean() * 12), sharpe=perf.sharpe(s), t=perf.nw_t(s)["t"], alpha=reg["alpha"] * 12, t_alpha=reg["t_alpha"], beta=reg["beta"],
                bn_ann=float(b.mean() * 12), bn_sharpe=perf.sharpe(b), bn_t=perf.nw_t(b)["t"],
                lo_minus_ew_sharpe=perf.sharpe(lo) - perf.sharpe(df.ew.reindex(lo.index)), lo_alpha=regl["alpha"] * 12, lo_t_alpha=regl["t_alpha"],
                cost=float(df.cost.mean() * 12), gross=float(df.ls_gross.mean() * 12), to=float(df.to.mean()),
                design=perf.sharpe(s.loc[:"2019-12-31"]), holdout=perf.sharpe(s.loc["2020-01-01":]))


if __name__ == "__main__":
    # one pickle per region (safe to run regions in parallel), merged into battery_price.pkl
    for R in (sys.argv[1:] or U):
        fr = os.path.join(RES, f"battery_price_{R}.pkl")
        if not os.path.exists(fr):
            pd.to_pickle(one(R), fr)
    B = {R: pd.read_pickle(os.path.join(RES, f"battery_price_{R}.pkl")) for R in U if os.path.exists(os.path.join(RES, f"battery_price_{R}.pkl"))}
    pd.to_pickle(B, os.path.join(RES, "battery_price.pkl"))
    J = {R: {s: stats(B[R][s]) for s in SIGS} for R in U if R in B}
    json.dump(dict(direction=DIRECTION, stats=J), open(os.path.join(RES, "battery_price.json"), "w"), indent=1)
    print("done", sorted(B))
