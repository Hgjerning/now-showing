# -*- coding: utf-8 -*-
"""A07 revisited (PREREGISTRATION_A07_R_2026-10-08.md + Clarification 1).
Input: scores_panel.csv from run_distress.py (P10_UNIVERSE as set). Out-of-sample expanding-window logits."""
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10"))
from stats import auc, block_boot_mean  # noqa: E402

warnings.filterwarnings("ignore")
RES = sys.argv[1] if len(sys.argv) > 1 else "results_rev"
OUT = sys.argv[2] if len(sys.argv) > 2 else "results_a07r"
os.makedirs(OUT, exist_ok=True)
GATE = 0.025
LOG = []


def prep(D, thr_col="crash"):
    E = D[D.date <= "2025-06-30"].dropna(subset=["Z", "O", "F", "vol", thr_col]).copy()
    E["y"] = E[thr_col].astype(bool).astype(int)
    # within-date percentile ranks, higher = more distressed
    g = E.groupby("date")
    E["r_vol"] = g.vol.rank(pct=True)
    E["r_Z"] = g.Z.rank(pct=True, ascending=False)
    E["r_O"] = g.O.rank(pct=True)
    E["r_F"] = g.F.rank(pct=True, ascending=False)
    return E


def fit(X, y):
    try:
        m = sm.Logit(y, sm.add_constant(X)).fit(disp=0, maxiter=200)
        if not m.mle_retvals.get("converged", True):
            raise RuntimeError("no convergence")
        return lambda Z: m.predict(sm.add_constant(Z, has_constant="add"))
    except Exception as e:  # fallback per Clarification 1
        from sklearn.linear_model import LogisticRegression
        LOG.append(f"fallback: {e}")
        m = LogisticRegression(C=1e6, max_iter=1000).fit(X, y)
        return lambda Z: m.predict_proba(Z)[:, 1]


MODELS = {"V": ["r_vol"], "V+A": ["r_vol", "r_Z", "r_O", "r_F"], "V+Z": ["r_vol", "r_Z"], "V+O": ["r_vol", "r_O"], "V+F": ["r_vol", "r_F"]}


def oos(E):
    dates = sorted(E.date.unique()); rows = []
    for i, t in enumerate(dates):
        tr_dates = [s for s in dates if s <= t - pd.DateOffset(months=12) + pd.offsets.MonthEnd(0)]
        if len(tr_dates) < 8:
            continue
        tr, te = E[E.date.isin(tr_dates)], E[E.date == t]
        if te.y.nunique() < 2:
            continue
        row = {"date": t, "n_test": len(te), "crashes": int(te.y.sum()), "n_train_dates": len(tr_dates)}
        for k, cols in MODELS.items():
            f = fit(tr[cols].to_numpy(), tr.y.to_numpy()); row[f"auc_{k}"] = auc(pd.Series(f(te[cols].to_numpy())), pd.Series(te.y.to_numpy().astype(bool)))
        rows.append(row)
    return pd.DataFrame(rows).set_index("date")


def tests(P):
    out = {}
    for name, k in [("A07-4", "V+A"), ("A07-5", "V+Z"), ("rep_V+O", "V+O"), ("rep_V+F", "V+F")]:
        d = (P[f"auc_{k}"] - P["auc_V"]).dropna()
        b = block_boot_mean(d, 4, 10000, 42, 0.0)
        out[name] = {**b, "auc_model": float(P[f"auc_{k}"].mean()), "auc_V": float(P["auc_V"].mean()), "passed": bool(b["p"] < GATE) if name.startswith("A07") else None}
    return out


def pooled(E):
    X = E[["r_vol", "r_Z", "r_O", "r_F"]].apply(lambda s: (s - s.mean()) / s.std())
    X = pd.concat([X, pd.get_dummies(E.date, drop_first=True, dtype=float)], axis=1)
    X = sm.add_constant(X)
    y, Xa = E.y.to_numpy(), X.to_numpy()
    m = sm.Logit(y, Xa).fit(disp=0, maxiter=500)
    # two-way cluster (firm, date): V = V_firm + V_date - V_het (Cameron, Gelbach & Miller 2011)
    def cov(groups):
        kw = dict(cov_type="cluster", cov_kwds={"groups": groups}) if groups is not None else dict(cov_type="HC0")
        return sm.Logit(y, Xa).fit(disp=0, maxiter=500, start_params=m.params, **kw).cov_params()
    fid, did = pd.factorize(E.ticker)[0], pd.factorize(E.date)[0]
    V = cov(fid) + cov(did) - cov(None)
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    names = ["const", "vol", "Z", "O", "F"]
    return {n: {"coef": float(m.params[i]), "se_2way": float(se[i]), "z": float(m.params[i] / se[i])} for i, n in enumerate(names)}


def main():
    D = pd.read_csv(os.path.join(RES, "scores_panel.csv"), parse_dates=["date"])
    # crash flags at 30% and 50% need the path; recompute only for reported thresholds via r12 is not possible,
    # so reported thresholds are computed in run_thresholds() from prices.
    E = prep(D)
    P = oos(E); P.to_csv(os.path.join(OUT, "oos_auc_by_date.csv"))
    S = {"universe": os.environ.get("P10_UNIVERSE", "?"), "n_obs": int(len(E)), "n_dates_all": int(E.date.nunique()),
         "n_test_dates": int(len(P)), "first_test": str(P.index.min().date()), "last_test": str(P.index.max().date()),
         "base_rate": float(E.y.mean()), "tests": tests(P), "pooled_logit": pooled(E)}
    thr = os.path.join(RES, "scores_panel_thresholds.csv")
    if os.path.exists(thr):
        T = pd.read_csv(thr, parse_dates=["date"])
        for c in ["crash30", "crash50"]:
            Et = prep(T, c); Pt = oos(Et); S[f"threshold_{c}"] = tests(Pt)
    S["fallback_log"] = LOG
    json.dump(S, open(os.path.join(OUT, "summary_a07r.json"), "w"), indent=2, default=float)
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
