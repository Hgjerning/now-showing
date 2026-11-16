# -*- coding: utf-8 -*-
"""A08 robustness checks from the 23 Oct 2026 stress test. Reported, not tested (no trial).
(1) Shuffled-real-years placebo: the 29 real publication years permuted across factors (2,000 draws, seed 42).
(2) Pooled regression with factor AND month fixed effects (two-way within transformation), SE clustered by month as in A08-1.
(3) Placebo-net decline share for the registered placebo and the shuffle placebo.
(4) Recomputes the 'reported' block of results/pubyear_sensitivity.json for the alternative years (Basu 1983, QMJ 2018).
Writes results/robustness_2026-10-23.json (aggregate numbers only)."""
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import run_decay as R  # noqa: E402

def two_way(J, years, iters=200, tol=1e-12):
    rows = []
    for f, y in years.items():
        s = J[f].dropna(); rows.append(pd.DataFrame({"f": f, "r": s.values, "post": (s.index.year > y).astype(float), "m": s.index}))
    Z = pd.concat(rows, ignore_index=True)
    r, p = Z.r.values.copy(), Z.post.values.copy()
    fi, mi = pd.factorize(Z.f)[0], pd.factorize(Z.m)[0]
    def dm(x):
        for _ in range(iters):
            x0 = x.copy()
            x = x - np.bincount(fi, x)[fi] / np.bincount(fi)[fi]
            x = x - np.bincount(mi, x)[mi] / np.bincount(mi)[mi]
            if np.max(np.abs(x - x0)) < tol: break
        return x
    rd, pd_ = dm(r), dm(p)
    b = (pd_ * rd).sum() / (pd_ ** 2).sum(); u = rd - b * pd_
    g = np.bincount(mi, pd_ * u); se = np.sqrt((g ** 2).sum()) / (pd_ ** 2).sum()
    return float(b), float(b / se)

def main():
    J = pd.read_csv(os.path.join(ROOT, "data", "jkp_usa_factors_monthly.csv"), index_col=0, parse_dates=True)[list(R.PUB)].loc[:"2025-12-31"]
    years = {f: v[2] for f, v in R.PUB.items()}
    S = json.load(open(os.path.join(ROOT, "results", "summary.json")))
    b, pre = S["A08-1"]["coef_monthly"], S["A08-1"]["pre_mean_ann"] / 12
    reg = np.load(os.path.join(ROOT, "results", "placebo_coef.npy"))
    rng = np.random.default_rng(42); fs = list(years); ys = np.array([years[f] for f in fs]); sh = []
    for _ in range(2000):
        sh.append(R.pooled(J, dict(zip(fs, rng.permutation(ys))))[0])
    sh = np.array(sh)
    bfe, tfe = two_way(J, years)
    O = {"note": "Reported, not tested (23 Oct 2026 stress test). No trial.",
         "actual_coef_ann": b * 12, "pre_mean_ann": pre * 12,
         "registered_placebo": {"draws": int(len(reg)), "mean_ann": float(reg.mean() * 12), "min_ann": float(reg.min() * 12),
                                "share_le_actual": float((reg <= b).mean()), "net_decline_ann": float((b - reg.mean()) * 12),
                                "net_decline_share": float(-(b - reg.mean()) / pre)},
         "shuffle_placebo": {"draws": 2000, "seed": 42, "mean_ann": float(sh.mean() * 12), "min_ann": float(sh.min() * 12),
                             "share_le_actual": float((sh <= b).mean()), "net_decline_ann": float((b - sh.mean()) * 12),
                             "net_decline_share": float(-(b - sh.mean()) / pre)},
         "month_fixed_effects": {"coef_ann": bfe * 12, "t": tfe, "share_of_pre_mean": float(-bfe / pre),
                                 "se": "clustered by month, as A08-1"}}
    # pubyear sensitivity: recompute the per-factor reported block with the alternative years
    alt = dict(years); alt["ni_me"] = 1983; alt["qmj"] = 2018
    T = []
    for f, y in alt.items():
        s = J[f].dropna(); a, c = s[s.index.year <= y].mean(), s[s.index.year > y].mean()
        T.append((a, c, 1 - c / a if a > 0 else np.nan))
    T = pd.DataFrame(T, columns=["pre", "post", "decay"])
    O["pubyear_sensitivity_reported"] = {"share_positive_post": float((T.post > 0).mean()), "median_decay": float(T.decay.median()),
                                         "share_decayed": float((T.post < T.pre).mean()), "n_factors": len(T)}
    json.dump(O, open(os.path.join(ROOT, "results", "robustness_2026-10-23.json"), "w"), indent=2)
    print(json.dumps(O, indent=1))

if __name__ == "__main__":
    main()
