# -*- coding: utf-8 -*-
"""A31 reported extension (REPORTED_EXTENSION_WIDE_FEATURES_2026-10-06.md): the A31 walk-forward on the wide feature set.
Variants W1 raw, W2 clustered composites, W3 PCA (90% variance); transforms fitted on each training window only.
    python run_wide.py U2 long_U2_wide.pkl out_U2/core_net_monthly_dir out_U2_wide [W1,W2,W3]
Reported, not gated, not trials."""
import json, os, sys, time, warnings
import numpy as np, pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.decomposition import PCA
from run_a31 import FEATS, LAST_FORM, MODELS, SPEC, book
from stats import nw_t, sharpe
warnings.filterwarnings("ignore")
RHO_CUT = 0.6; PCA_VAR = 0.90


def cluster_map(Xtr, names, seed=0):
    rng = np.random.default_rng(seed); n = len(Xtr)
    S = Xtr[rng.choice(n, min(n, 200_000), replace=False)]
    C = np.corrcoef(S, rowvar=False); C = np.nan_to_num(C)
    Dm = 1 - np.abs(C); np.fill_diagonal(Dm, 0); Dm = (Dm + Dm.T) / 2
    lab = fcluster(linkage(squareform(Dm, checks=False), "average"), t=1 - RHO_CUT, criterion="distance")
    groups = []
    for c in np.unique(lab):
        idx = np.where(lab == c)[0]; first = idx[0]
        sign = np.sign(C[first, idx]); sign[sign == 0] = 1
        groups.append((idx, sign))
    return groups, [[names[i] for i in g[0]] for g in groups], C


def apply_clusters(X, groups, months):
    Z = np.column_stack([(X[:, idx] * s).mean(axis=1) for idx, s in groups])
    Zr = pd.DataFrame(Z).groupby(months).rank(pct=True).to_numpy() - 0.5
    return Zr


def walk(L, feats, variant, sp, log, ckpt=None):
    months = L.index.get_level_values(0)
    L = L[(months >= sp["start"]) & (months <= LAST_FORM)]; months = L.index.get_level_values(0)
    y = L["y"].to_numpy(); X = L[feats].to_numpy(dtype="float64")
    preds = {n: pd.Series(np.nan, index=L.index) for n in MODELS}; done = set()
    if ckpt and os.path.exists(ckpt):
        c = pd.read_pickle(ckpt); done = set(c["years"]); preds = c["preds"]; log.update(c["log"])
    for yr in range(sp["first_oos"], LAST_FORM.year + 1):
        if yr in done:
            continue
        tr = np.asarray((months <= pd.Timestamp(f"{yr - 1}-11-30")) & ~np.isnan(y)); te = np.asarray(months.year == yr)
        Xtr, Xte = X[tr], X[te]
        if variant == "W2":
            groups, gnames, _ = cluster_map(Xtr, feats)
            Xtr = apply_clusters(Xtr, groups, months[tr]); Xte = apply_clusters(Xte, groups, months[te])
            log.setdefault("clusters", {})[yr] = gnames
        elif variant == "W3":
            p = PCA(n_components=PCA_VAR, svd_solver="full").fit(Xtr); Xtr, Xte = p.transform(Xtr), p.transform(Xte)
            log.setdefault("n_pcs", {})[yr] = int(p.n_components_)
        for n in MODELS:
            m = MODELS[n]().fit(Xtr, y[tr]); preds[n].iloc[np.where(te)[0]] = m.predict(Xte)
        print(variant, yr, "trained on", int(tr.sum()), "inputs", Xtr.shape[1], flush=True)
        if ckpt:
            done.add(yr); pd.to_pickle({"years": sorted(done), "preds": preds, "log": log}, ckpt + ".tmp"); os.replace(ckpt + ".tmp", ckpt)
    return L, pd.DataFrame(preds).dropna()


def row(n, b):
    x, g = b.net.dropna(), b.gross.dropna(); to = b.turnover.iloc[1:].mean(); h = len(x) // 2
    return dict(model=n, net_ann=x.mean() * 12, net_sharpe=sharpe(x), net_t=nw_t(x, 3)["t"], gross_ann=g.mean() * 12,
                gross_sharpe=sharpe(g), gross_t=nw_t(g, 3)["t"], turnover_m=to, breakeven_cost=g.mean() / to if to > 0 else np.nan,
                ic=float(b.ic.mean()), net_sharpe_h1=sharpe(x.iloc[:h]), net_sharpe_h2=sharpe(x.iloc[h:]), months=len(x))


def vif(Xdf):
    C = np.corrcoef(Xdf.to_numpy(dtype="float64"), rowvar=False)
    return pd.Series(np.diag(np.linalg.pinv(C)), index=Xdf.columns)


def load_panel(f):
    """.pkl, or a folder of yearly parquet chunks (U1_wide_*.parquet) exported for running on another machine."""
    if os.path.isdir(f):
        import glob
        L = pd.concat([pd.read_parquet(p) for p in sorted(glob.glob(os.path.join(f, "*.parquet")))])
        return L.set_index(["month", "ticker"]).sort_index()
    return pd.read_pickle(f)


def main():
    u, f, core, OUT = sys.argv[1:5]; variants = (sys.argv[5] if len(sys.argv) > 5 else "W1,W2,W3").split(",")
    os.makedirs(OUT, exist_ok=True); sp = SPEC[u]; L = load_panel(f)
    feats = FEATS + [c for c in L.columns if c.startswith("x_")]
    core_net = pd.read_csv(f"{core}/net_monthly.csv", index_col=0, parse_dates=True)["Ensemble"]
    # diagnostics (whole sample, not used for any choice)
    oos = L[L.index.get_level_values(0) >= pd.Timestamp(f"{sp['first_oos']}-01-01")]
    smp = oos.sample(min(len(oos), 300_000), random_state=0)
    vif(smp[feats]).sort_values(ascending=False).to_csv(f"{OUT}/vif_wide.csv")
    smp[feats].corr().round(3).to_csv(f"{OUT}/corr_wide.csv")
    groups, gnames, _ = cluster_map(smp[feats].to_numpy(dtype="float64"), feats)
    Zs = pd.DataFrame(apply_clusters(smp[feats].to_numpy(dtype="float64"), groups, smp.index.get_level_values(0)),
                      columns=["c%d:" % i + "+".join(g[:3]) for i, g in enumerate(gnames)])
    vif(Zs).sort_values(ascending=False).to_csv(f"{OUT}/vif_clusters.csv")
    vif(smp[FEATS]).sort_values(ascending=False).to_csv(f"{OUT}/vif_core12.csv")
    R_prev = json.load(open(f"{OUT}/wide_summary.json")) if os.path.exists(f"{OUT}/wide_summary.json") else {}
    R = {"universe": u, "features": feats, "n_features": len(feats), "whole_sample_clusters": gnames}
    for v in variants:
        t0 = time.time(); log = {}
        if os.path.exists(f"{OUT}/scoreboard_{v}.csv") and v in R_prev:
            R[v] = R_prev[v]; continue
        Lw, P = walk(L, feats, v, sp, log, ckpt=f"{OUT}/_ckpt_{v}.pkl")
        P["Ensemble"] = P.groupby(level=0).rank(pct=True).mean(axis=1)
        P.to_pickle(f"{OUT}/oos_predictions_{v}.pkl")
        B = {n: book(Lw, P[n], sp["cost"]) for n in P.columns}
        NET = pd.DataFrame({n: b.net for n, b in B.items()}); NET.to_csv(f"{OUT}/net_monthly_{v}.csv")
        pd.DataFrame({n: b.gross for n, b in B.items()}).to_csv(f"{OUT}/gross_monthly_{v}.csv")
        sb = pd.DataFrame([row(n, b) for n, b in B.items()]).set_index("model"); sb.to_csv(f"{OUT}/scoreboard_{v}.csv")
        d = (NET["Ensemble"] - core_net).dropna(); dt = nw_t(d, 3)
        R[v] = dict(ensemble=sb.loc["Ensemble"].to_dict(), minus_core_ensemble_net_ann=d.mean() * 12, minus_core_t=dt["t"],
                    minutes=round((time.time() - t0) / 60, 1), **log)
        json.dump(R, open(f"{OUT}/wide_summary.json", "w"), indent=1, default=float)
        print(sb.round(3).to_string(), flush=True)
    print(json.dumps({k: R.get(k) for k in variants}, indent=1, default=float)[:4000])


if __name__ == "__main__":
    main()
