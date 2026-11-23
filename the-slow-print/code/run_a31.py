# -*- coding: utf-8 -*-
"""A31 Minority Report 2: the A06 walk-forward on U1 (US small caps) and U2 (European blue chips), net of costs.
Pre-registration: PREREGISTRATION_A31_2026-10-06.md (signed). Models, hyperparameters and features are A06's.
    python run_a31.py U1 <panel.pkl> <outdir>"""
import json, os, sys, time, warnings
import numpy as np, pandas as pd
from scipy import stats as st
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from stats import deflated_sharpe, nw_t, sharpe
warnings.filterwarnings("ignore")
FEATS = ["r1", "r3", "mom", "vol60", "maxret", "hi52", "beta", "size", "bm", "ep", "gpa", "ag"]
SPEC = {"U1": dict(start="1999-12-31", first_oos=2004, cost=0.0050), "U2": dict(start="2013-01-31", first_oos=2017, cost=0.0015),
        "U3": dict(start="2013-01-31", first_oos=2017, cost=0.0050)}
LAST_FORM = pd.Timestamp("2026-07-31"); GATE = 0.05 / 9; DSR_BAR = 1 - GATE


class MLPavg:
    def __init__(self):
        self.m = [MLPRegressor(hidden_layer_sizes=(32, 16), alpha=1e-3, early_stopping=True, max_iter=200, random_state=s) for s in (1, 2, 3)]
    def fit(self, X, y):
        for m in self.m: m.fit(X, y)
        return self
    def predict(self, X):
        return np.mean([m.predict(X) for m in self.m], axis=0)


MODELS = {  # identical to A06 run_ml.py
    "OLS": lambda: LinearRegression(), "Ridge": lambda: Ridge(alpha=10), "Lasso": lambda: Lasso(alpha=1e-4),
    "ElasticNet": lambda: ElasticNet(alpha=1e-4, l1_ratio=0.5),
    "RandomForest": lambda: RandomForestRegressor(300, max_depth=6, min_samples_leaf=200, max_features=0.5, n_jobs=int(os.environ.get("A31_NJOBS", "2")), random_state=42),
    "GradBoost": lambda: HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_depth=3, min_samples_leaf=200, random_state=42),
    "MLP": lambda: MLPavg(), "kNN": lambda: KNeighborsRegressor(n_neighbors=500),
}


def walk_forward(L, names, start, first_oos, feats=FEATS, shuffle_seed=None, ckpt=None):
    """ckpt: optional path; predictions are saved after each year and finished years are skipped on restart (results unchanged)."""
    months = L.index.get_level_values(0)
    L = L[(months >= start) & (months <= LAST_FORM)]; months = L.index.get_level_values(0)
    y = L["y"].to_numpy().copy()
    if shuffle_seed is not None:
        rng = np.random.default_rng(shuffle_seed)
        for m in np.unique(months):
            i = np.where(months == m)[0]; y[i] = y[rng.permutation(i)]
    X = L[feats].to_numpy(); preds = {n: pd.Series(np.nan, index=L.index) for n in names}
    done = set()
    if ckpt and os.path.exists(ckpt):
        c = pd.read_pickle(ckpt); done = set(c["years"]); preds = {n: c["preds"][n] for n in names}
    for yr in range(first_oos, LAST_FORM.year + 1):
        if yr in done:
            continue
        tr = (months <= pd.Timestamp(f"{yr - 1}-11-30")) & ~np.isnan(y); te = months.year == yr
        for n in names:
            t0 = time.time(); m = MODELS[n]().fit(X[tr], y[tr]); preds[n].iloc[np.where(te)[0]] = m.predict(X[te])
        print(yr, "trained on", int(tr.sum()), flush=True)
        if ckpt:
            done.add(yr); pd.to_pickle({"years": sorted(done), "preds": preds}, ckpt + ".tmp"); os.replace(ckpt + ".tmp", ckpt)
    return L, pd.DataFrame(preds).dropna()


def book(L, score, cost, q=0.1):
    """Monthly decile long-short with drift-aware turnover. Returns DataFrame gross, net, turnover, ic."""
    df = pd.DataFrame({"s": score, "r": L.loc[score.index, "fwd"]})
    out = []; prev = None
    for m, g in df.groupby(level=0):
        g = g.droplevel(0); k = g.s.rank(pct=True)
        lo, sh = g.index[k > 1 - q], g.index[k <= q]
        w = pd.concat([pd.Series(1 / len(lo), index=lo), pd.Series(-1 / len(sh), index=sh)])
        w = w.groupby(level=0).sum()
        traded = (w.sub(prev, fill_value=0).abs().sum()) if prev is not None else w.abs().sum()
        r = g.r.reindex(w.index)
        rl, rs = r[w > 0].mean(), r[w < 0].mean()
        gross = rl - rs
        # drift to next month (missing next-month return: position closed at zero return)
        rr = r.fillna(0.0)
        wl = w[w > 0] * (1 + rr[w > 0]); ws = w[w < 0] * (1 + rr[w < 0])
        prev = pd.concat([wl / wl.sum(), -ws / ws.sum()]) if len(wl) and len(ws) else None
        ic = st.spearmanr(g.s, g.r, nan_policy="omit")[0]
        out.append(dict(month=m, gross=gross, turnover=traded, net=gross - cost * traded, ic=ic, long=rl, short=rs))
    return pd.DataFrame(out).set_index("month")


def halves_pos(x):
    x = x.dropna(); h = len(x) // 2
    return bool(x.iloc[:h].mean() > 0 and x.iloc[h:].mean() > 0)


def main():
    u, f, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True); sp = SPEC[u]
    t0 = time.time(); L = pd.read_pickle(f); names = list(MODELS)
    Lw, P = walk_forward(L, names, sp["start"], sp["first_oos"])
    P["Ensemble"] = P.groupby(level=0).rank(pct=True).mean(axis=1); P["Momentum"] = Lw.loc[P.index, "raw_mom"]
    P.to_pickle(f"{OUT}/oos_predictions.pkl")
    B = {n: book(Lw, P[n].dropna(), sp["cost"]) for n in P.columns}
    NET = pd.DataFrame({n: b.net for n, b in B.items()}); GROSS = pd.DataFrame({n: b.gross for n, b in B.items()})
    NET.to_csv(f"{OUT}/net_monthly.csv"); GROSS.to_csv(f"{OUT}/gross_monthly.csv")
    pd.DataFrame({n: b.turnover for n, b in B.items()}).to_csv(f"{OUT}/turnover_monthly.csv")
    rows = []
    for n in NET:
        x, g = NET[n].dropna(), GROSS[n].dropna(); h = len(x) // 2; to = B[n].turnover.iloc[1:].mean()
        rows.append(dict(model=n, net_ann=x.mean() * 12, net_sharpe=sharpe(x), net_t=nw_t(x, 3)["t"], gross_ann=g.mean() * 12,
                         gross_sharpe=sharpe(g), gross_t=nw_t(g, 3)["t"], turnover_m=to, breakeven_cost=g.mean() / to if to > 0 else np.nan,
                         ic=float(B[n].ic.mean()), hit=float((x > 0).mean()), net_sharpe_h1=sharpe(x.iloc[:h]), net_sharpe_h2=sharpe(x.iloc[h:]), months=len(x)))
    S_board = pd.DataFrame(rows).set_index("model"); S_board.to_csv(f"{OUT}/scoreboard.csv")
    S = {"universe": u, "cost_one_way": sp["cost"], "gate": GATE}
    e = NET["Ensemble"].dropna(); a1 = nw_t(e, 3)
    S[f"A31-{u}.1"] = {**a1, "sharpe": sharpe(e), "halves_positive": halves_pos(e), "passed": bool(a1["p_gt"] < GATE and halves_pos(e))}
    d = (NET["Ensemble"] - NET["Momentum"]).dropna(); a2 = nw_t(d, 3)
    S[f"A31-{u}.2"] = {**a2, "halves_positive": halves_pos(d), "passed": bool(a2["p_gt"] < GATE and halves_pos(d))}
    nine = names + ["Momentum"]; srm = {n: NET[n].mean() / NET[n].std() for n in nine}; best = max(srm, key=srm.get); xb = NET[best].dropna()
    ds = deflated_sharpe(srm[best], list(srm.values()), len(xb), float(st.skew(xb)), float(st.kurtosis(xb, fisher=False)))
    S[f"A31-{u}.3"] = {"best": best, "sr_ann": float(srm[best] * np.sqrt(12)), **ds, "halves_positive": halves_pos(xb),
                       "passed": bool(ds["dsr"] > DSR_BAR and halves_pos(xb))}
    S["months"] = [str(NET.index[0].date()), str(NET.index[-1].date())]; S["minutes"] = round((time.time() - t0) / 60, 1)
    json.dump(S, open(f"{OUT}/summary.json", "w"), indent=2, default=float)
    print(S_board.round(3).to_string()); print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
