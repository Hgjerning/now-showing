# -*- coding: utf-8 -*-
"""Reported-only robustness for C31-1 (no verdicts). Reads ../results/windows_by_year.csv."""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results")
SEED, GATE = 42, 0.025
tab = pd.read_csv(os.path.join(OUT, "windows_by_year.csv"), index_col=0)
col = "ret[1,90]"
M, C = tab[tab.kind == "midterm"][col].dropna(), tab[tab.kind != "midterm"][col].dropna()


def perm_p(x, y, n=10000, seed=SEED):
    x, y = np.asarray(x, float), np.asarray(y, float)
    v = np.concatenate([x, y]); nx = len(x); obs = x.mean() - y.mean()
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(n):
        p = rng.permutation(v)
        if p[:nx].mean() - p[nx:].mean() >= obs:
            cnt += 1
    return (cnt + 1) / (n + 1)


rows = []
def add(name, x, y, note=""):
    w = stats.ttest_ind(x, y, equal_var=False, alternative="greater")
    rows.append(dict(check=name, n_mid=len(x), n_ctrl=len(y), mid_mean=x.mean(), ctrl_mean=y.mean(), diff=x.mean() - y.mean(),
                     welch_t=float(w.statistic), p_welch_1s=float(w.pvalue), p_perm_1s=perm_p(x, y), note=note))

add("Primary (C31-1)", M, C)
add("Since 1950", M[M.index >= 1950], C[C.index >= 1950])
add("Since 1974 (Goldman window)", M[M.index >= 1974], C[C.index >= 1974])
add("Excl. 1930s (1930-1939)", M[(M.index < 1930) | (M.index > 1939)], C[(C.index < 1930) | (C.index > 1939)])
add("Control = odd years only", M, tab[tab.kind == "odd"][col].dropna())
add("Control = presidential years only", M, tab[tab.kind == "presidential"][col].dropna())
add("Excl. best midterm (1970)", M.drop(M.idxmax()), C)
add("Excl. 2 worst control years", M, C.drop(C.nsmallest(2).index))
lo = M.quantile(0.1); hi = M.quantile(0.9); lc = C.quantile(0.1); hc = C.quantile(0.9)
add("10% winsorised both groups", M.clip(lo, hi), C.clip(lc, hc))
rb = pd.DataFrame(rows)
mw = stats.mannwhitneyu(M, C, alternative="greater")
loo = []
for y in M.index:
    loo.append(stats.ttest_ind(M.drop(y), C, equal_var=False, alternative="greater").pvalue)
extra = dict(mann_whitney_U=float(mw.statistic), mann_whitney_p_1s=float(mw.pvalue), median_mid=float(M.median()), median_ctrl=float(C.median()),
             leave_one_out_max_p_welch=float(max(loo)), leave_one_out_argmax=int(M.index[int(np.argmax(loo))]),
             family_bonferroni_17_one_sided=0.05 / 17, worst_ctrl=C.nsmallest(5).round(4).to_dict(), best_ctrl=C.nlargest(3).round(4).to_dict())


# forward: exact permutation break-even for 2026 (10,000 shuffles per point)
def pooled(r):
    return perm_p(np.append(M.to_numpy(), r), C.to_numpy())
grid = np.round(np.arange(-0.26, -0.14, 0.01), 3)
be = {float(g): pooled(g) for g in grid}
extra["breakeven_perm"] = be
wgrid = np.round(np.arange(-0.30, 0.40, 0.001), 3)
wp = np.array([stats.ttest_ind(np.append(M, g), C, equal_var=False, alternative="greater").pvalue for g in wgrid])
p_now = stats.ttest_ind(M, C, equal_var=False, alternative="greater").pvalue
better = wgrid[wp <= p_now]
extra["welch_p_now"] = float(p_now)
extra["r26_range_that_strengthens"] = [float(better.min()), float(better.max())]
extra["r26_welch_breakeven"] = float(wgrid[np.argmax(wp < GATE)])
rb.to_csv(os.path.join(OUT, "robustness.csv"), index=False)
with open(os.path.join(OUT, "robustness_extra.json"), "w") as f:
    json.dump(extra, f, indent=2)
print(rb.round(4).to_string()); print(json.dumps(extra, indent=1))
