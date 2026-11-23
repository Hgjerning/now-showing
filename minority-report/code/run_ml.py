# -*- coding: utf-8 -*-
"""A06 Minority Report: walk-forward ML scoreboard (pre-registered, see PREREGISTRATION_A06)."""
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd
from scipy import stats as st
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from features import FEATS, panel_long  # noqa: E402
from stats import deflated_sharpe, nw_t, sharpe  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, os.environ.get("P10_RESULTS", "results"))
os.makedirs(OUT, exist_ok=True)
FIRST_OOS, LAST_FORM = pd.Timestamp("2017-01-31"), pd.Timestamp("2026-07-31")
GATE = 0.05 / 3


class MLPavg:
    def __init__(self):
        self.m = [MLPRegressor(hidden_layer_sizes=(32, 16), alpha=1e-3, early_stopping=True, max_iter=200, random_state=s) for s in (1, 2, 3)]

    def fit(self, X, y):
        for m in self.m:
            m.fit(X, y)
        return self

    def predict(self, X):
        return np.mean([m.predict(X) for m in self.m], axis=0)


MODELS = {
    "OLS": lambda: LinearRegression(),
    "Ridge": lambda: Ridge(alpha=10),
    "Lasso": lambda: Lasso(alpha=1e-4),
    "ElasticNet": lambda: ElasticNet(alpha=1e-4, l1_ratio=0.5),
    "RandomForest": lambda: RandomForestRegressor(300, max_depth=6, min_samples_leaf=200, max_features=0.5, n_jobs=2, random_state=42),
    "GradBoost": lambda: HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_depth=3, min_samples_leaf=200, random_state=42),
    "MLP": lambda: MLPavg(),
    "kNN": lambda: KNeighborsRegressor(n_neighbors=500),
}


def walk_forward(L, names, shuffle_seed=None):
    months = L.index.get_level_values(0)
    L = L[(months >= "2013-01-31") & (months <= LAST_FORM)]
    months = L.index.get_level_values(0)
    y = L["y"].to_numpy().copy()
    if shuffle_seed is not None:  # placebo: shuffle targets within each month
        rng = np.random.default_rng(shuffle_seed)
        for m in np.unique(months):
            i = np.where(months == m)[0]; y[i] = y[rng.permutation(i)]
    X = L[FEATS].to_numpy()
    preds = {n: pd.Series(np.nan, index=L.index) for n in names}
    for yr in range(FIRST_OOS.year, LAST_FORM.year + 1):
        # training months: targets known before Jan of yr -> formation month <= Nov of yr-1
        tr = (months <= pd.Timestamp(f"{yr - 1}-11-30")) & ~np.isnan(y)
        te = (months.year == yr)
        for n in names:
            m = MODELS[n]().fit(X[tr], y[tr]); preds[n].iloc[np.where(te)[0]] = m.predict(X[te])
    return L, pd.DataFrame(preds).dropna()


def long_short(L, score, q=0.1):
    df = pd.DataFrame({"s": score, "r": L.loc[score.index, "fwd"]}).dropna()
    def one(g):
        k = g.s.rank(pct=True)
        return pd.Series({"ls": g.r[k > 1 - q].mean() - g.r[k <= q].mean(), "long": g.r[k > 1 - q].mean(),
                          "short": g.r[k <= q].mean(), "ic": st.spearmanr(g.s, g.r)[0]})
    return df.groupby(level=0).apply(one)


def main():
    t0 = time.time(); L = panel_long(); names = list(MODELS)
    Lw, P = walk_forward(L, names); print("fit", round(time.time() - t0))
    P["Ensemble"] = P.groupby(level=0).rank(pct=True).mean(axis=1)
    P["Momentum"] = Lw.loc[P.index, "raw_mom"]
    P.to_pickle(os.path.join(OUT, "oos_predictions.pkl"))
    res = {n: long_short(Lw, P[n]) for n in P.columns}
    LS = pd.DataFrame({n: r.ls for n, r in res.items()}); LS.to_csv(os.path.join(OUT, "longshort_monthly.csv"))
    IC = pd.DataFrame({n: r.ic for n, r in res.items()}); IC.to_csv(os.path.join(OUT, "ic_monthly.csv"))
    pd.DataFrame({n: r.long for n, r in res.items()}).to_csv(os.path.join(OUT, "long_monthly.csv"))
    board = []
    for n in LS:
        x = LS[n].dropna(); t = nw_t(x, 3)
        h = len(x) // 2
        board.append(dict(model=n, mean_m=t["mean"], ann_ret=t["mean"] * 12, sharpe=sharpe(x), nw_t=t["t"], p=t["p_gt"],
                          ic=float(IC[n].mean()), ic_t=nw_t(IC[n].dropna(), 3)["t"], hit=float((x > 0).mean()),
                          sharpe_h1=sharpe(x.iloc[:h]), sharpe_h2=sharpe(x.iloc[h:]), months=len(x)))
    B = pd.DataFrame(board).set_index("model"); B.to_csv(os.path.join(OUT, "scoreboard.csv"))
    S = {}
    a1 = nw_t(LS["Ensemble"].dropna(), 3); S["A06-1"] = {**a1, "sharpe": sharpe(LS["Ensemble"]), "passed": bool(a1["p_gt"] < GATE)}
    d = (LS["Ensemble"] - LS["Momentum"]).dropna(); a2 = nw_t(d, 3); S["A06-2"] = {**a2, "passed": bool(a2["p_gt"] < GATE)}
    nine = names + ["Momentum"]
    srm = {n: LS[n].mean() / LS[n].std() for n in nine}; best = max(srm, key=srm.get); xb = LS[best].dropna()
    ds = deflated_sharpe(srm[best], list(srm.values()), len(xb), float(st.skew(xb)), float(st.kurtosis(xb, fisher=False)))
    S["A06-3"] = {"best": best, "sr_monthly": float(srm[best]), "sr_ann": float(srm[best] * np.sqrt(12)), **ds, "passed": bool(ds["dsr"] > 1 - GATE)}
    S["months"] = [str(LS.index[0].date()), str(LS.index[-1].date())]
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=2)
    print(B.round(3)); print(json.dumps(S, indent=1)); print("total", round(time.time() - t0))


if __name__ == "__main__":
    main()
