# -*- coding: utf-8 -*-
"""A04 Viva Las Vegas: the MAX (lottery-stock) effect after publication and in large caps."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from features import price_features  # noqa: E402
from panel import load_all  # noqa: E402
from stats import nw_t, sharpe  # noqa: E402

D, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, os.environ.get("P10_RESULTS", "results")); os.makedirs(OUT, exist_ok=True)
GATE = 0.025


def main():
    J = pd.read_csv(os.path.join(D, "jkp_usa_factors_monthly.csv"), index_col=0, parse_dates=True)["rmax1_21d"].dropna()
    post = J.loc["2012-01-31":"2025-12-31"]; a1 = nw_t(post, 6)
    S = {"A04-1": {**a1, "ann": a1["mean"] * 12, "sharpe": sharpe(post), "passed": bool(a1["p_gt"] < GATE)}}
    px, fd, pm, mc, uni, ret = load_all(); F = price_features(px, pm)
    mx, vol, beta = F["maxret"], F["vol60"], F["beta"]
    rows = []
    months = pm.index[(pm.index >= "2013-01-31") & (pm.index <= "2026-07-31")]
    for i, t in enumerate(months):
        nxt = pm.index[pm.index.get_loc(t) + 1]
        s = mx.loc[t].where(uni.loc[t]).dropna(); d = pd.qcut(s.rank(method="first"), 10, labels=False) + 1
        r = ret.loc[nxt, s.index]
        row = {"month": nxt, **{f"D{k}": float(r[d == k].mean()) for k in range(1, 11)},
               "max_D1": float(s[d == 1].mean()), "max_D10": float(s[d == 10].mean()),
               "vol_D1": float(vol.loc[t, s.index][d == 1].mean()), "vol_D10": float(vol.loc[t, s.index][d == 10].mean()),
               "beta_D1": float(beta.loc[t, s.index][d == 1].mean()), "beta_D10": float(beta.loc[t, s.index][d == 10].mean())}
        rows.append(row)
    P = pd.DataFrame(rows).set_index("month"); P["low_minus_high"] = P.D1 - P.D10
    P.to_csv(os.path.join(OUT, "max_deciles_top500.csv"))
    a2 = nw_t(P.low_minus_high, 3)
    S["A04-2"] = {**a2, "ann": a2["mean"] * 12, "sharpe": sharpe(P.low_minus_high), "first": str(P.index[0].date()), "last": str(P.index[-1].date()),
                  "passed": bool(a2["p_gt"] < GATE)}
    pre = J.loc["1963-07-31":"2005-12-31"]; mid = J.loc["2006-01-31":"2011-12-31"]; meme = P.loc["2020-04-30":"2021-12-31", "low_minus_high"]
    S["reported"] = {"jkp_insample_1963_2005": {**nw_t(pre, 6), "ann": pre.mean() * 12},
                     "jkp_2006_2011": {"ann": float(mid.mean() * 12)},
                     "top500_meme_2020_04_2021_12": {"ann": float(meme.mean() * 12), "months": int(len(meme))},
                     "decile_ann": {f"D{k}": float(P[f"D{k}"].mean() * 12) for k in range(1, 11)},
                     "avg_max_D1": float(P.max_D1.mean()), "avg_max_D10": float(P.max_D10.mean()),
                     "vol_D1": float(P.vol_D1.mean()), "vol_D10": float(P.vol_D10.mean()), "beta_D1": float(P.beta_D1.mean()), "beta_D10": float(P.beta_D10.mean()),
                     "sharpe_D1": sharpe(P.D1), "sharpe_D10": sharpe(P.D10)}
    J.to_csv(os.path.join(OUT, "jkp_max_factor.csv"), header=["ret"])
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=2, default=float)
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
