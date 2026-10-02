# -*- coding: utf-8 -*-
"""US fundamental battery: 14 Sharadar signals + 6 theme composites through the same engine as FS03-FS13
(xs.run: deciles of the PIT top-500, equal weight, 10 bp per side, size-tiered borrow fee, financing of net long cash).
Adds: replication vs the matching JKP US factor, overlap with the price battery, and spanning by the price shortlist.
Writes results/fund_battery.json and results/fund_battery.pkl."""
import json
import os

import numpy as np
import pandas as pd

import fundamentals as FU
import perf
import xs
from battery import stats

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results"); FAC = os.path.join(HERE, "..", "factors")
SIGS = list(FU.FUND) + [FU.COMP[t] for t in FU.THEMES]
LH = {**{k: v[1] for k, v in FU.FUND.items()}, **{FU.COMP[t]: True for t in FU.THEMES}}
LAB = {**{k: v[2] for k, v in FU.FUND.items()}, **{FU.COMP[t]: t + " (composite)" for t in FU.THEMES}}
THEME = {**{k: v[0] for k, v in FU.FUND.items()}, **{FU.COMP[t]: t for t in FU.THEMES}}
PRICE_SHORT = ["beta", "mom", "resmom", "hi52"]


def run():
    I = xs.inputs("US"); S = FU.build(); I["S"].update(S)
    out = {}
    for s in SIGS:
        P0 = xs.run(I, s, LH[s]); P1 = xs.run(I, s, LH[s], beta_neutral=True)
        out[s] = pd.DataFrame(dict(ls_net=P0.ls_net, ls_gross=P0.ls_gross, lo_net=P0.good_net, ew=P0.ew, cost=P0.cost, to=P0.to_good + P0.to_bad,
                                   borrow=P0.borrow, bn_net=P1.ls_net.reindex(P0.index)))
        print(s, round(out[s].ls_net.mean() * 12, 4), flush=True)
    pd.to_pickle(out, os.path.join(RES, "fund_battery.pkl"))
    return out


def analyse(out):
    J = {s: stats(out[s]) for s in SIGS}
    # replication: our gross L/S vs JKP US factor
    jk = pd.read_csv(os.path.join(FAC, "jkp_usa_factors_monthly.csv"), index_col=0, parse_dates=True); jk.index = jk.index.to_period("M")
    cl = pd.read_csv(os.path.join(FAC, "jkp_cluster_labels.csv")).set_index("characteristic")["cluster"]
    for s in SIGS:
        o = out[s].ls_gross.copy(); o.index = o.index.to_period("M")
        if s in FU.FUND:
            k = FU.FUND[s][3]
            J[s]["jkp"] = k; J[s]["repl"] = float(pd.concat([o, jk[k]], axis=1).dropna().loc["2013-02":"2025-12"].corr().iloc[0, 1]) if k in jk else None
        else:
            facs = [c for c in jk.columns if cl.get(c) == FU.JKP_CLUSTER[THEME[s]]]
            J[s]["jkp"] = f"JKP {FU.JKP_CLUSTER[THEME[s]]} theme ({len(facs)} factors)"
            J[s]["repl"] = float(pd.concat([o, jk[facs].mean(axis=1)], axis=1).dropna().loc["2013-02":"2025-12"].corr().iloc[0, 1])
    # overlap with the price battery and spanning by the price shortlist (beta-neutral books)
    B = pd.read_pickle(os.path.join(RES, "battery_price.pkl"))["US"]
    PR = pd.DataFrame({p: B[p].bn_net for p in B})
    for s in SIGS:
        y = out[s].bn_net.dropna()
        c = PR.reindex(y.index).corrwith(y).sort_values(key=abs, ascending=False)
        J[s]["nearest_price"] = [(k, float(v)) for k, v in c.head(3).items()]
        X = PR[PRICE_SHORT].reindex(y.index).dropna(); yy = y.reindex(X.index)
        Xc = np.column_stack([np.ones(len(X)), X.values]); b, *_ = np.linalg.lstsq(Xc, yy.values, rcond=None)
        e = yy.values - Xc @ b; n, k = Xc.shape
        # Newey-West (6 lags) standard error of the intercept
        u = Xc * e[:, None]; S0 = u.T @ u
        for L in range(1, 7):
            w = 1 - L / 7; G = u[L:].T @ u[:-L]; S0 += w * (G + G.T)
        XtXi = np.linalg.inv(Xc.T @ Xc); V = XtXi @ S0 @ XtXi
        J[s]["span_alpha"] = float(b[0] * 12); J[s]["span_t"] = float(b[0] / np.sqrt(V[0, 0])); J[s]["span_r2"] = float(1 - e.var() / yy.var())
    # correlation among theme composites
    C = pd.DataFrame({t: out[FU.COMP[t]].bn_net for t in FU.THEMES}).corr()
    res = dict(stats=J, labels=LAB, theme=THEME, long_high=LH, comp_corr=C.round(3).to_dict(), price_short=PRICE_SHORT)
    json.dump(res, open(os.path.join(RES, "fund_battery.json"), "w"), indent=1, default=float)
    return res


if __name__ == "__main__":
    f = os.path.join(RES, "fund_battery.pkl")
    out = pd.read_pickle(f) if os.path.exists(f) else run()
    R = analyse(out)
    for s in SIGS:
        v = R["stats"][s]
        print(f"{LAB[s]:34s} LS {v['ann']*100:+5.1f}% t {v['t']:+.2f} | bn {v['bn_ann']*100:+5.1f}% t {v['bn_t']:+.2f} | LO-EW SR {v['lo_minus_ew_sharpe']:+.2f} a_t {v['lo_t_alpha']:+.2f} | repl {v['repl']:.2f} | span a {v['span_alpha']*100:+.1f}% t {v['span_t']:+.2f} R2 {v['span_r2']:.2f} | D/H {v['design']:+.2f}/{v['holdout']:+.2f}")
    print(pd.DataFrame(R["comp_corr"]).round(2))
