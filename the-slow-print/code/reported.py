# -*- coding: utf-8 -*-
"""A31 reported analyses (prereg section 4: reported, not gated, not trials).
    python reported.py U2 long_U2.pkl out_U2 [--placebo N] [--skip-ablation]
Writes <out>/reported.json, simple_sorts.csv, placebo.csv, ablation_net_monthly.csv."""
import json, sys
import numpy as np, pandas as pd
from run_a31 import FEATS, MODELS, SPEC, book, walk_forward
from stats import nw_t, sharpe

SORTS = {"Value (B/M)": ("bm", 1), "Earnings yield": ("ep", 1), "Profitability (GP/A)": ("gpa", 1),
         "Low volatility": ("vol60", -1), "Small size": ("size", -1), "Momentum 12-1": ("mom", 1)}


def row(name, b):
    x, g = b.net.dropna(), b.gross.dropna(); to = b.turnover.iloc[1:].mean()
    return dict(name=name, net_ann=x.mean() * 12, net_sharpe=sharpe(x), net_t=nw_t(x, 3)["t"], gross_ann=g.mean() * 12,
                gross_sharpe=sharpe(g), gross_t=nw_t(g, 3)["t"], turnover_m=to, breakeven_cost=g.mean() / to if to > 0 else np.nan)


def main():
    u, f, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; sp = SPEC[u]; a = sys.argv[4:]
    npl = int(a[a.index("--placebo") + 1]) if "--placebo" in a else 20
    L = pd.read_pickle(f); P = pd.read_pickle(f"{OUT}/oos_predictions.pkl")
    NET = pd.read_csv(f"{OUT}/net_monthly.csv", index_col=0, parse_dates=True)
    GROSS = pd.read_csv(f"{OUT}/gross_monthly.csv", index_col=0, parse_dates=True)
    R = {"universe": u}
    # simple one-characteristic sorts over the same OOS months
    Lo = L.loc[P.index]; rows = []
    for nm, (c, s) in SORTS.items():
        rows.append(row(nm, book(L, (s * Lo[c]).dropna(), sp["cost"])))
    pd.DataFrame(rows).set_index("name").to_csv(f"{OUT}/simple_sorts.csv"); R["simple_sorts"] = rows
    # 2017-2026 window (like-for-like with A06)
    w = {}
    for n in ["Ensemble", "Momentum", "Ridge", "GradBoost"]:
        x, g = NET[n]["2017":].dropna(), GROSS[n]["2017":].dropna()
        w[n] = dict(net_ann=x.mean() * 12, net_sharpe=sharpe(x), gross_ann=g.mean() * 12, gross_sharpe=sharpe(g), months=len(x))
    R["window_2017_2026"] = w
    # shuffled-target placebo: Ridge and GradBoost
    real = {n: dict(net=sharpe(NET[n].dropna()), gross=sharpe(GROSS[n].dropna())) for n in ["Ridge", "GradBoost"]}
    import os
    pl = pd.read_csv(f"{OUT}/placebo.csv").to_dict("records") if os.path.exists(f"{OUT}/placebo.csv") else []
    have = {r["seed"] for r in pl}
    for seed in range(1, npl + 1):
        if seed in have:
            continue
        Lw, Q = walk_forward(L, ["Ridge", "GradBoost"], sp["start"], sp["first_oos"], shuffle_seed=seed, ckpt=f"{OUT}/_ckpt_placebo_{seed}.pkl")
        for n in Q:
            b = book(Lw, Q[n], sp["cost"]); pl.append(dict(seed=seed, model=n, net=sharpe(b.net.dropna()), gross=sharpe(b.gross.dropna())))
        pd.DataFrame(pl).to_csv(f"{OUT}/placebo.csv", index=False); print("placebo seed", seed, flush=True)
    D = pd.DataFrame(pl); R["placebo"] = {}
    for n in real:
        d = D[D.model == n]
        R["placebo"][n] = dict(real_net=real[n]["net"], real_gross=real[n]["gross"], placebo_gross_mean=d.gross.mean(),
                               placebo_gross_max=d.gross.max(), share_placebo_gross_ge_real=float((d.gross >= real[n]["gross"]).mean()),
                               placebo_net_mean=d.net.mean(), runs=len(d))
    json.dump(R, open(f"{OUT}/reported.json", "w"), indent=2, default=float)
    # ablation without 12-1 momentum (full ensemble, all eight models)
    if "--skip-ablation" not in a:
        fx = [c for c in FEATS if c != "mom"]
        Lw, Q = walk_forward(L, list(MODELS), sp["start"], sp["first_oos"], feats=fx, ckpt=f"{OUT}/_ckpt_ablation.pkl")
        Q["Ensemble"] = Q.groupby(level=0).rank(pct=True).mean(axis=1)
        B = {n: book(Lw, Q[n], sp["cost"]) for n in Q}
        pd.DataFrame({n: b.net for n, b in B.items()}).to_csv(f"{OUT}/ablation_net_monthly.csv")
        R["ablation_no_mom"] = [row(n, b) for n, b in B.items()]
        json.dump(R, open(f"{OUT}/reported.json", "w"), indent=2, default=float)
    print(json.dumps(R, indent=1, default=float))


if __name__ == "__main__":
    main()
