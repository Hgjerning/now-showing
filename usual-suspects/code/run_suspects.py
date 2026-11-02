# -*- coding: utf-8 -*-
"""A05: regress the 16 guru recipes on French FF5 + momentum. Writes ../results/."""
import json
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, "results")
os.makedirs(OUT, exist_ok=True)
GATE_T = 2.955
LAGS = 6
# verbatim from Project1 factor_recipes.py RECIPES (guru items only)
RECIPES = {
    "Greenblatt": ["ebit_bev", "op_at"],
    "Carlisle": ["ebitda_mev"],
    "O'Shaughnessy growth": ["sale_me", "ret_12_1", "ni_inc8q"],
    "O'Shaughnessy value": ["div12m_me", "sale_me", "-market_equity"],
    "P. O'Shaughnessy millennial": ["eqnpo_me", "be_me", "ret_12_1", "qmj"],
    "Zweig": ["ni_inc8q", "saleq_gr1", "sale_gr3", "-debt_me"],
    "Neff": ["ni_me", "div12m_me", "sale_gr3"],
    "Dreman": ["ni_me", "ocf_me", "div12m_me"],
    "Lynch": ["ni_me", "ni_inc8q", "sale_gr3"],
    "Buffett (quality)": ["qmj", "qmj_prof", "qmj_safety"],
    "Graham": ["be_me", "ni_me", "div12m_me", "z_score", "-debt_me"],
    "O'Neil CAN SLIM": ["niq_su", "ni_inc8q", "ret_12_1", "prc_highprc_252d"],
    "Fisher (price/sales)": ["sale_me", "sale_gr3"],
    "Piotroski-type small growth": ["f_score", "market_equity", "sale_gr1"],
    "Motley Fool small-cap growth": ["market_equity", "sale_gr1", "ebit_sale", "-debt_me"],
    "Mohanram P/B growth": ["-be_me", "ocf_at", "ni_be", "rd_sale"],
}
FAC = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "Mom"]


def recipe(f, legs):
    cols = [(-1.0 if l.startswith("-") else 1.0) * f[l.lstrip("-")] for l in legs]
    return pd.concat(cols, axis=1).dropna().mean(axis=1)


def french_monthly(five, mom):
    a = pd.read_csv(os.path.join(D, five), index_col=0, parse_dates=True)
    m = pd.read_csv(os.path.join(D, mom), index_col=0, parse_dates=True)
    m = m.rename(columns={m.columns[0]: "Mom"})
    x = a.join(m, how="inner")
    x = (1 + x).resample("ME").prod(min_count=1) - 1
    return x


def nw_ols(y, X, lags=LAGS):
    X = np.column_stack([np.ones(len(X)), X]); n, k = X.shape
    b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None])
        S += w * (G + G.T)
    V = XtXi @ S @ XtXi
    r2 = 1 - e.var() / y.var()
    return b, b / np.sqrt(np.diag(V)), r2


def nw_mean_t(y, lags=LAGS):
    b, t, _ = nw_ols(y, np.zeros((len(y), 0)), lags)
    return b[0], t[0]


def run(fac, f, start=None, end=None):
    rows = {}
    for name, legs in RECIPES.items():
        r = recipe(f, legs)
        r.index = r.index.to_period("M").to_timestamp("M")
        df = pd.concat([r.rename("r"), fac[FAC]], axis=1, join="inner").dropna()
        if start: df = df.loc[start:]
        if end: df = df.loc[:end]
        if len(df) < 60:
            continue
        b, t, r2 = nw_ols(df.r.values, df[FAC].values)
        m, mt = nw_mean_t(df.r.values)
        rows[name] = dict(first=str(df.index[0].date())[:7], last=str(df.index[-1].date())[:7], n=len(df),
                          raw_ann=m * 12, raw_t=mt, alpha_ann=b[0] * 12, alpha_t=t[0], r2=r2,
                          **{f"b_{k}": v for k, v in zip(FAC, b[1:])}, **{f"t_{k}": v for k, v in zip(FAC, t[1:])})
    return pd.DataFrame(rows).T


def main():
    fus = pd.read_csv(os.path.join(D, "jkp_usa_factors_monthly.csv"), index_col=0, parse_dates=True)
    fus.index = pd.to_datetime(fus.index).to_period("M").to_timestamp("M")
    fac = french_monthly("french_us_5f_daily.csv", "french_us_mom_daily.csv")
    full = run(fac, fus, end="2025-12-31")
    h1 = run(fac, fus, end="1994-12-31"); h2 = run(fac, fus, start="1995-01-01", end="2025-12-31")
    w12 = run(fac, fus, start="2012-01-01", end="2025-12-31")
    full["alpha_h1"] = h1["alpha_ann"]; full["alpha_h2"] = h2["alpha_ann"]; full["alpha_2012"] = w12["alpha_ann"]; full["t_2012"] = w12["alpha_t"]
    full["pass"] = (full.alpha_t.astype(float).abs() > GATE_T) & (np.sign(full.alpha_h1.astype(float)) == np.sign(full.alpha_h2.astype(float)))
    full.index.name = "recipe"
    full.to_csv(os.path.join(OUT, "suspects_us.csv"))
    # developed markets (reported)
    fw = pd.read_csv(os.path.join(D, "jkp_world_factors_monthly.csv"), index_col=0, parse_dates=True)
    fw.index = pd.to_datetime(fw.index).to_period("M").to_timestamp("M")
    facw = french_monthly("french_developed_5f_daily.csv", "french_developed_mom_daily.csv")
    world = run(facw, fw, start="1990-07-01", end="2025-12-31"); world.index.name = "recipe"
    world.to_csv(os.path.join(OUT, "suspects_developed.csv"))
    S = dict(n_recipes=len(full), n_pass=int(full["pass"].sum()), passed=bool(full["pass"].any()), gate_t=GATE_T,
             passers=list(full.index[full["pass"]]), median_r2=float(full.r2.astype(float).median()),
             n_raw_sig=int((full.raw_t.astype(float).abs() > GATE_T).sum()),
             median_abs_raw=float(full.raw_ann.astype(float).abs().median()), median_abs_alpha=float(full.alpha_ann.astype(float).abs().median()),
             world_n_sig=int((world.alpha_t.astype(float).abs() > GATE_T).sum()), world_median_r2=float(world.r2.astype(float).median()))
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=2)
    pd.set_option("display.width", 250)
    print(full[["first", "n", "raw_ann", "raw_t", "alpha_ann", "alpha_t", "r2", "alpha_h1", "alpha_h2", "alpha_2012", "pass"]].astype({"raw_ann": float, "alpha_ann": float}).round(3).to_string())
    print(world[["raw_ann", "raw_t", "alpha_ann", "alpha_t", "r2"]].astype(float).round(3).to_string())
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
