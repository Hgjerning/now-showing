# -*- coding: utf-8 -*-
"""Evaluates the stacked fixes (design 2013-2019 vs holdout 2020-2026) and builds the classification evidence."""
import json
import os

import numpy as np
import pandas as pd

import data
import perf

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results"); FAC = os.path.join(HERE, "..", "factors")
U = data.REGIONS
DES, HOL = ("2013-01-01", "2019-12-31"), ("2020-01-01", "2026-08-31")
N_TRIALS = 7            # 4 Turtle steps + 3 lottery steps, judged pooled across universes
GATE_P = 0.05 / N_TRIALS


def stats(m, b=None):
    m = m.dropna()
    out = dict(ann=float(m.mean() * 12), sharpe=perf.sharpe(m), maxdd=float(perf.drawdown(m).min()), t=perf.nw_t(m)["t"])
    if b is not None:
        reg = perf.nw_ols(m.values, b.reindex(m.index).values)
        out.update(alpha=reg["alpha"] * 12, t_alpha=reg["t_alpha"], beta=reg["beta"])
    return out


def pooled_test(a, b, lo, hi):
    """Paired stationary-bootstrap Sharpe difference of the six-universe equal-weight average, a vs b."""
    x = a.loc[lo:hi].mean(axis=1); y = b.loc[lo:hi].mean(axis=1)
    return perf_paired(x.values, y.values)


def perf_paired(a, b, draws=5000, seed=42):
    rng = np.random.default_rng(seed); n = len(a); obs = perf.sharpe(a) - perf.sharpe(b); d = np.empty(draws)
    for k in range(draws):
        i = perf.stationary_idx(n, 6, rng); d[k] = perf.sharpe(a[i]) - perf.sharpe(b[i])
    p = (1 + np.sum(d - d.mean() >= obs)) / (draws + 1)
    return dict(diff=float(obs), p=float(p), lo=float(np.percentile(d, 2.5)), hi=float(np.percentile(d, 97.5)))


def turtle():
    steps = ["T0 baseline L/S", "T1 long-only", "T2 + System 2 only", "T3 + 4N stop", "T4 + market trend filter"]
    per, M = {}, {s: {} for s in steps + ["EW universe"]}
    cc = json.load(open(os.path.join(RES, "turtle_cost_check.json")))
    for R in U:
        F = pd.read_pickle(os.path.join(RES, f"turtle_fix_{R}.pkl"))
        m = perf.to_monthly(F["series"]).loc[:"2026-08-31"]
        for s in steps + ["EW universe"]:
            M[s][R] = m[s]
        per[R] = {s: {"design": stats(m[s].loc[DES[0]:DES[1]], m["EW universe"]), "holdout": stats(m[s].loc[HOL[0]:HOL[1]], m["EW universe"])} for s in steps + ["EW universe"]}
        t4 = F["trades"]["T4"]; per[R]["T4_trades"] = dict(n=int(len(t4)), per_year=float(len(t4) / 13.7), win=float((t4.pnl_pct > 0).mean()))
    M = {s: pd.DataFrame(v) for s, v in M.items()}
    pooled = {}
    for i in range(1, len(steps)):
        pooled[steps[i]] = {"vs_previous_holdout": pooled_test(M[steps[i]], M[steps[i - 1]], *HOL),
                            "vs_previous_design": pooled_test(M[steps[i]], M[steps[i - 1]], *DES)}
    pooled["final_vs_EW_holdout"] = pooled_test(M[steps[-1]], M["EW universe"], *HOL)
    pooled["T3_vs_EW_holdout"] = pooled_test(M["T3 + 4N stop"], M["EW universe"], *HOL)
    avg = {s: stats(M[s].mean(axis=1).loc[HOL[0]:HOL[1]], M["EW universe"].mean(axis=1)) for s in M}
    return dict(per=per, pooled=pooled, avg_holdout=avg, cost_check=cc, steps=steps), M


def lottery():
    S = pd.read_pickle(os.path.join(RES, "lottery_fix_series.pkl"))
    steps = list(next(iter(S.values())).keys())
    per, M = {}, {s: {} for s in steps}
    for R in U:
        ew = S[R][steps[0]].ew
        per[R] = {}
        for s in steps:
            x = S[R][s].loc["2013-02-28":]
            M[s][R] = x.ls_net
            per[R][s] = {"design": stats(x.ls_net.loc[DES[0]:DES[1]], ew), "holdout": stats(x.ls_net.loc[HOL[0]:HOL[1]], ew),
                         "cost": float(x.cost.mean() * 12), "b_low": float(x.b_low.mean()), "b_high": float(x.b_high.mean()), "to": float(x.to.mean())}
    M = {s: pd.DataFrame(v) for s, v in M.items()}
    zero = M[steps[0]] * 0
    pooled = {}
    for i in range(1, len(steps)):
        pooled[steps[i]] = {"vs_previous_holdout": pooled_test(M[steps[i]], M[steps[i - 1]], *HOL),
                            "vs_previous_design": pooled_test(M[steps[i]], M[steps[i - 1]], *DES)}
    pooled["L1_vs_zero_holdout"] = {"t": perf.nw_t(M[steps[1]].mean(axis=1).loc[HOL[0]:HOL[1]])["t"], "ann": float(M[steps[1]].mean(axis=1).loc[HOL[0]:HOL[1]].mean() * 12)}
    avg = {s: stats(M[s].mean(axis=1).loc[HOL[0]:HOL[1]]) for s in M}
    return dict(per=per, pooled=pooled, avg_holdout=avg, steps=steps, diag=json.load(open(os.path.join(RES, "lottery_diagnostics.json")))), M


# ---------------- classification evidence ----------------
def jkp13(c):
    f = pd.read_csv(os.path.join(FAC, f"jkp_{c}_themes_daily.csv"), index_col=0, parse_dates=True).loc["2012":]
    return perf.to_monthly(f)


def french(c):
    f = pd.read_csv(os.path.join(FAC, f"french_{c}_5f_daily.csv"), index_col=0, parse_dates=True)
    m = pd.read_csv(os.path.join(FAC, f"french_{c}_mom_daily.csv"), index_col=0, parse_dates=True)
    return perf.to_monthly(f.join(m).drop(columns=["RF"]).loc["2012":])


FSET = {"US": lambda: jkp13("usa"), "UK": lambda: jkp13("gbr"), "DK": lambda: jkp13("dnk"), "WD": lambda: jkp13("world"),
        "EU": lambda: french("europe"), "SC": lambda: french("europe")}


def classify(books):
    """books: {name: {R: monthly series}}; correlation with every factor theme, convexity, tails."""
    out = {}
    for name, d in books.items():
        out[name] = {}
        for R in U:
            m = d[R].dropna(); F = FSET[R](); j = pd.concat([m.rename("y"), F], axis=1, join="inner").dropna()
            corr = j.corr()["y"].drop("y").sort_values(key=abs, ascending=False)
            ew = books["_EW"][R].reindex(m.index)
            X = np.column_stack([ew.values, ew.values ** 2]); y = m.values
            Xc = np.column_stack([np.ones(len(y)), X]); b = np.linalg.lstsq(Xc, y, rcond=None)[0]
            u = y - Xc @ b; n = len(y); XtXi = np.linalg.inv(Xc.T @ Xc); Xu = Xc * u[:, None]; Sm = Xu.T @ Xu / n
            for L in range(1, 7):
                G = Xu[L:].T @ Xu[:-L] / n; Sm += (1 - L / 7) * (G + G.T)
            se = np.sqrt(np.diag(n * XtXi @ Sm @ XtXi))
            bad = ew <= ew.quantile(0.1); good = ew >= ew.quantile(0.9)
            out[name][R] = dict(top=[(k, float(v)) for k, v in corr.head(3).items()], corr=corr.to_dict(),
                                tm_gamma=float(b[2]), tm_t=float(b[2] / se[2]), skew=float(m.skew()),
                                worst_mkt=float(m[bad].mean()), best_mkt=float(m[good].mean()))
    return out


if __name__ == "__main__":
    T, MT = turtle(); L, ML = lottery()
    Tser = pd.read_pickle(os.path.join(RES, "turtle_series.pkl")); Lser = pd.read_pickle(os.path.join(RES, "lottery_series.pkl"))
    books = {"Turtle L/S": {R: MT["T0 baseline L/S"][R] for R in U}, "Turtle long-only": {R: MT["T1 long-only"][R] for R in U},
             "Turtle fixed (T3)": {R: MT["T3 + 4N stop"][R] for R in U},
             "MAX L/S": {R: ML["L0 baseline"][R] for R in U}, "MAX beta-neutral (L1)": {R: ML["L1 beta-neutral"][R] for R in U},
             "_EW": {R: MT["EW universe"][R] for R in U}}
    C = classify({k: v for k, v in books.items()})
    C.pop("_EW")
    json.dump(dict(turtle=T, lottery=L, classification=C), open(os.path.join(RES, "fix_summary.json"), "w"), indent=1, default=float)
    for s, v in T["pooled"].items(): print("T", s, {k: (round(x["diff"], 2), round(x["p"], 3)) for k, x in v.items()} if "vs_previous_holdout" in v else (round(v["diff"], 2), round(v["p"], 3)))
    for s, v in L["pooled"].items(): print("L", s, v)
    for s, v in T["avg_holdout"].items(): print("Tavg", s, {k: round(x, 3) for k, x in v.items()})
    for s, v in L["avg_holdout"].items(): print("Lavg", s, {k: round(x, 3) for k, x in v.items()})
    for n, v in C.items(): print(n, {R: (v[R]["top"][0][0], round(v[R]["top"][0][1], 2), round(v[R]["tm_gamma"], 2), round(v[R]["tm_t"], 1)) for R in U})
