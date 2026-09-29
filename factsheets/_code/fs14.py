# -*- coding: utf-8 -*-
"""FS14 multifactor model, exactly as pre-registered in planning/PREREG_FS14.md (27 Sep 2026).
Walk-forward: at month-end t, using returns up to t, filter -> prune -> weight; hold for t+1.
Writes results/fs14.json and results/fs14.pkl."""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats as sst

import perf

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results")
U = ["US", "EU", "UK", "DK", "SC", "WD"]
WF, PSR_MIN, COST_SHARE, RHO = 36, 0.80, 0.50, 0.70
VARIANTS = ["EQ", "RP"] + [f"W{w}-{k}" for w in (12, 36, 60) for k in ("E", "L", "X")]
TCOST = 0.001
SHORT = {"all": ["beta", "mom"], "US": ["beta", "mom", "c_debt_issuance", "c_profit_growth"]}


def battery(R):
    B = pd.read_pickle(os.path.join(RES, "battery_price.pkl"))[R]
    ret = pd.DataFrame({s: B[s].bn_net for s in B}); gross = pd.DataFrame({s: B[s].ls_gross for s in B}); cost = pd.DataFrame({s: B[s].cost for s in B})
    if R == "US":
        F = pd.read_pickle(os.path.join(RES, "fund_battery.pkl"))
        for s in [k for k in F if k.startswith("c_")]:
            ret[s] = F[s].bn_net; gross[s] = F[s].ls_gross; cost[s] = F[s].cost
    return ret.sort_index(), gross.sort_index(), cost.sort_index()


def psr(x):
    x = x.dropna(); n = len(x)
    if n < 12 or x.std() == 0:
        return 0.0
    sr = x.mean() / x.std(); g3 = sst.skew(x); g4 = sst.kurtosis(x, fisher=False)
    return float(sst.norm.cdf(sr * np.sqrt(n - 1) / np.sqrt(max(1 - g3 * sr + (g4 - 1) / 4 * sr ** 2, 1e-9))))


def obs_weights(n, kind, window):
    if kind == "E":
        w = np.ones(n)
    elif kind == "L":
        w = np.arange(1, n + 1, dtype=float)
    else:
        hl = window / 3; w = 0.5 ** ((n - 1 - np.arange(n)) / hl)
    return w / w.sum()


def wstats(X, kind, window):
    w = obs_weights(len(X), kind, window)
    mu = (X.values * w[:, None]).sum(0); var = ((X.values - mu) ** 2 * w[:, None]).sum(0) * len(X) / max(len(X) - 1, 1)
    return pd.Series(mu, X.columns), pd.Series(var, X.columns)


def step(ret, gross, cost, i):
    """Selection at month index i (uses rows i-WF+1..i)."""
    win = ret.iloc[i - WF + 1:i + 1]; g = gross.iloc[i - WF + 1:i + 1]; c = cost.iloc[i - WF + 1:i + 1]
    cols = [s for s in ret.columns if win[s].notna().sum() >= WF - 2]
    passed = []
    for s in cols:
        x = win[s].dropna(); gm = g[s].mean(); cm = c[s].mean()
        if x.mean() > 0 and psr(x) >= PSR_MIN and gm > 0 and cm < COST_SHARE * gm:
            passed.append(s)
    order = sorted(passed, key=lambda s: -(win[s].mean() / win[s].std()))
    C = win[order].corr() if order else None; kept = []
    for s in order:
        if all(abs(C.loc[s, k]) <= RHO for k in kept):
            kept.append(s)
    return cols, passed, kept


def weights(ret, i, kept, var):
    if not kept:
        return pd.Series(dtype=float)
    if var == "EQ":
        return pd.Series(1 / len(kept), kept)
    if var == "RP":
        v = ret[kept].iloc[i - WF + 1:i + 1].std(); w = 1 / v
        return w / w.sum()
    W, k = int(var[1:3]), var[-1]
    X = ret[kept].iloc[max(0, i - W + 1):i + 1].dropna(how="all").fillna(0.0)
    mu, v = wstats(X, k, W); w = mu.clip(lower=0) / v.where(v > 0)
    w = w.fillna(0)
    return (w / w.sum()) if w.sum() > 0 else pd.Series(1 / len(kept), kept)


def run_market(R):
    ret, gross, cost = battery(R); idx = ret.index
    out = {v: {} for v in VARIANTS}; prev = {v: pd.Series(dtype=float) for v in VARIANTS}
    sel = []; W_hist = {v: {} for v in VARIANTS}
    for i in range(WF - 1, len(idx) - 1):
        cols, passed, kept = step(ret, gross, cost, i)
        nxt = idx[i + 1]
        sel.append(dict(month=nxt, n_cand=len(cols), n_pass=len(passed), n_kept=len(kept), passed=passed, kept=kept))
        r1 = ret.loc[nxt]
        for v in VARIANTS:
            w = weights(ret, i, kept, v)
            to = float(w.subtract(prev[v], fill_value=0).abs().sum()) / 2 if len(prev[v]) or len(w) else 0.0
            gr = float((w * r1.reindex(w.index).fillna(0)).sum()) if len(w) else 0.0
            out[v][nxt] = gr - TCOST * to; prev[v] = w; W_hist[v][nxt] = w.to_dict()
    P = pd.DataFrame(out)
    oos = P.index
    P["ALL-EQ"] = ret.reindex(oos).mean(axis=1)
    sh = [s for s in (SHORT["US"] if R == "US" else SHORT["all"]) if s in ret.columns]
    P["SHORT"] = ret[sh].reindex(oos).mean(axis=1)
    B = pd.read_pickle(os.path.join(RES, "battery_price.pkl"))[R]
    P["MARKET"] = B["mom"].ew.reindex(oos)
    for c in VARIANTS + ["ALL-EQ", "SHORT"]:          # ex-ante vol scaling to 10%, cap 3x
        vol = P[c].rolling(12, min_periods=6).std().shift(1) * np.sqrt(12)
        P[c + " (10% vol)"] = P[c] * (0.10 / vol).clip(upper=3.0)
    return P, pd.DataFrame(sel).set_index("month"), W_hist, list(ret.columns)


def st(x):
    x = x.dropna()
    if len(x) < 12:
        return None
    cum = (1 + x).cumprod(); dd = float((cum / cum.cummax() - 1).min())
    return dict(ann=float(x.mean() * 12), vol=float(x.std() * np.sqrt(12)), sharpe=perf.sharpe(x), t=perf.nw_t(x)["t"], maxdd=dd,
                s1=perf.sharpe(x.loc[:"2019-12-31"]), s2=perf.sharpe(x.loc["2020-01-01":]), months=int(len(x)))


def main():
    res, ser, sels, cands = {}, {}, {}, {}
    for R in U:
        P, S, W, cand = run_market(R); ser[R] = P; sels[R] = S; cands[R] = cand
        res[R] = {c: st(P[c]) for c in P.columns}
        freq = pd.Series([s for k in S.kept for s in k]).value_counts() / len(S)
        pfreq = pd.Series([s for k in S.passed for s in k]).value_counts() / len(S)
        res[R]["_sel"] = dict(n_cand=len(cand), pass_med=float(S.n_pass.median()), kept_med=float(S.n_kept.median()), cash_months=int((S.n_kept == 0).sum()),
                              kept_freq=freq.round(3).to_dict(), pass_freq=pfreq.round(3).to_dict(), last_kept=S.kept.iloc[-1])
        print(R, {c: round(res[R][c]["sharpe"], 2) for c in ["EQ", "RP", "W36-X", "ALL-EQ", "SHORT", "MARKET"]}, "kept med", res[R]["_sel"]["kept_med"], flush=True)
    # primary test: RP - ALL-EQ pooled over the five non-World markets
    M5 = [R for R in U if R != "WD"]
    def paired(a, b):
        d = pd.DataFrame({R: ser[R][a] - ser[R][b] for R in M5}).dropna(); x = d.mean(axis=1)
        return dict(ann=float(x.mean() * 12), t=perf.nw_t(x)["t"], s1=float(x.loc[:"2019-12-31"].mean() * 12), s2=float(x.loc["2020-01-01":].mean() * 12), pos=int((d.mean() > 0).sum()))
    res["primary"] = paired("RP", "ALL-EQ")
    res["vs_short"] = {v: paired(v, "SHORT") for v in VARIANTS}
    res["vs_alleq"] = {v: paired(v, "ALL-EQ") for v in VARIANTS}
    res["pooled"] = {}
    for c in VARIANTS + ["ALL-EQ", "SHORT"]:
        x = pd.DataFrame({R: ser[R][c] for R in M5}).dropna().mean(axis=1); res["pooled"][c] = st(x)
    res["variants"] = VARIANTS
    json.dump(res, open(os.path.join(RES, "fs14.json"), "w"), indent=1, default=str)
    pd.to_pickle(dict(ser=ser, sel=sels, cand=cands), os.path.join(RES, "fs14.pkl"))
    print("primary", res["primary"])
    print("pooled", {c: round(v["sharpe"], 2) for c, v in res["pooled"].items()})


if __name__ == "__main__":
    main()
