# -*- coding: utf-8 -*-
"""A03 The Magnificent Seven: concentration trials (pre-registered, see PREREGISTRATION_A03)."""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from panel import load_all  # noqa: E402
from stats import nw_ols, nw_t, stationary_idx  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, os.environ.get("P10_RESULTS", "results"))
os.makedirs(OUT, exist_ok=True)
GATE = 0.05 / 2
H = 12


def bh_return(ret, t_pos, tickers, w):
    """Buy-and-hold H-month return of a weighted basket; a stock that stops trading sits in cash."""
    R = ret.iloc[t_pos + 1:t_pos + 1 + H][tickers].fillna(0.0).to_numpy()
    g = np.prod(1 + R, axis=0) - 1
    return float(np.sum(w * g) / np.sum(w))


def main():
    px, fd, pm, mc, uni, ret = load_all()
    months = mc.index
    M = months[(months >= "2012-02-29") & (months <= "2026-08-31")]
    rows = []
    for t in M:
        tp = months.get_loc(t)
        m = mc.loc[t].where(uni.loc[t]).dropna().sort_values(ascending=False)
        top, rest = m.index[:10], m.index[10:]
        r = dict(month=t, C=m.iloc[:10].sum() / m.sum(), C1=m.iloc[0] / m.sum(), top10=",".join(top))
        if tp + H < len(months) and months[tp + H] <= pd.Timestamp("2026-08-31"):
            r["top_ret"] = bh_return(ret, tp, top, m[top].to_numpy())
            r["rest_ret"] = bh_return(ret, tp, rest, m[rest].to_numpy())
            r["cw_ret"] = bh_return(ret, tp, m.index, m.to_numpy())
            r["ew_ret"] = bh_return(ret, tp, m.index, np.ones(len(m)))
        rows.append(r)
    D = pd.DataFrame(rows).set_index("month")
    D["spread"] = D.top_ret - D.rest_ret; D["ew_cw"] = D.ew_ret - D.cw_ret; D["dC"] = D.C - D.C.shift(12)
    D.to_csv(os.path.join(OUT, "concentration_monthly.csv"))
    S = {}
    s = D.spread.dropna(); a1 = nw_t(s, 12)
    rng = np.random.default_rng(42); bm = np.array([s.to_numpy()[stationary_idx(len(s), 12, rng)].mean() for _ in range(10000)])
    S["A03-1"] = {**a1, "boot_p_lt": float((1 + np.sum(bm - bm.mean() <= a1["mean"])) / 10001), "passed": bool(a1["p_lt"] < GATE),
                  "share_months_top_won": float((s > 0).mean()), "first": str(s.index[0].date()), "last": str(s.index[-1].date())}
    E = D.dropna(subset=["ew_cw", "dC"]); o = nw_ols(E.ew_cw, E[["dC"]], 12)
    rng = np.random.default_rng(42); bs = []
    y, x = E.ew_cw.to_numpy(), E.dC.to_numpy()
    for _ in range(10000):
        i = stationary_idx(len(y), 12, rng); xx = x[i] - x[i].mean(); bs.append(xx @ (y[i] - y[i].mean()) / (xx @ xx))
    bs = np.array(bs); b = float(o["coef"][1])
    S["A03-2"] = {"slope": b, "t": float(o["t"][1]), "p_gt": float(1 - __import__("scipy").stats.norm.cdf(o["t"][1])), "r2": o["r2"], "n": o["n"],
                  "boot_p_gt": float((1 + np.sum(bs - bs.mean() >= b)) / 10001), "passed": bool(o["t"][1] > 1.96)}
    # reported: wealth creation (price-only, vs zero), membership turnover
    wc = (mc.shift(1) * ret).loc["2012-02-29":"2026-08-31"].sum(min_count=1).dropna().sort_values(ascending=False)
    wc.to_csv(os.path.join(OUT, "wealth_creation_by_stock.csv"), header=["usd"])
    net = wc.sum(); n2 = int(np.ceil(0.02 * len(wc)))
    sets = D.top10.str.split(",").apply(set)
    ann = [len(sets.iloc[i] - sets.iloc[i - 12]) for i in range(12, len(sets))]
    S["reported"] = {"C_first": float(D.C.iloc[0]), "C_last": float(D.C.iloc[-1]), "C_max": float(D.C.max()), "C_max_month": str(D.C.idxmax().date()),
                     "C_min": float(D.C.min()), "C1_last": float(D.C1.iloc[-1]), "top10_first": D.top10.iloc[0], "top10_last": D.top10.iloc[-1],
                     "wealth_net_usd_tn": float(net / 1e12), "wealth_top10_share": float(wc.iloc[:10].sum() / net), "wealth_top2pct_share": float(wc.iloc[:n2].sum() / net),
                     "n_stocks": int(len(wc)), "n_top2pct": n2, "share_negative": float((wc < 0).mean()), "top10_creators": list(wc.index[:10]),
                     "top10_creators_usd_tn": [float(v / 1e12) for v in wc.iloc[:10]], "bottom5": list(wc.index[-5:]),
                     "top10_changes_per_year": float(np.mean(ann)), "mean_spread_12m": float(s.mean()), "median_spread_12m": float(s.median()),
                     "ew_cw_mean_12m": float(D.ew_cw.mean())}
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=2)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
