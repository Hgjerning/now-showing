# -*- coding: utf-8 -*-
"""A03 version 3 (19 Oct 2026): DESCRIPTIVE additions asked for by the reviews. Not trials: nothing here is gated.
1. Monthly top-10 minus rest (cap-weighted, formed at each month-end, held one month) and its risk: annualised mean,
   volatility, information ratio, worst drawdown, worst 12 months.
2. Factor attribution of that monthly spread: Fama-French 5 factors + momentum (US, Kenneth French), Newey-West 6 lags.
3. Interaction: monthly Fama-MacBeth across the top 500 of next-month return on size (log market cap), 12-1 momentum and
   size x momentum (all cross-sectionally standardised); NW 6 lags on the monthly slopes.
4. Year-by-year table (start months per calendar year) from results/concentration_monthly.csv.
Writes results/v3_extras.json, results/v3_monthly_spread.csv."""
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "lib10"))
from panel import load_all  # noqa: E402
from stats import nw_ols, nw_t  # noqa: E402
CC = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))
FF = os.path.join(CC, "Project2 Investment Strategy", "reporting", "style_cache")

def ff_monthly():
    f = pd.read_csv(os.path.join(FF, "french_us_5f_daily.csv"), index_col=0, parse_dates=True)
    m = pd.read_csv(os.path.join(FF, "french_us_mom_daily.csv"), index_col=0, parse_dates=True)
    d = f.join(m, how="inner"); d.columns = [c.strip() for c in d.columns]
    mom = [c for c in d.columns if c.lower().startswith("mom") or c.lower() == "umd"][0]
    out = (1 + d).resample("ME").prod() - 1
    return out.rename(columns={mom: "MOM"})

def main():
    px, fd, pm, mc, uni, ret = load_all()
    months = mc.index; M = months[(months >= "2012-01-31") & (months <= "2026-07-31")]
    rows, fm = [], []
    lr = np.log(pm)
    for t in M:
        tp = months.get_loc(t)
        if tp + 1 >= len(months): break
        m = mc.loc[t].where(uni.loc[t]).dropna().sort_values(ascending=False)
        top, rest = m.index[:10], m.index[10:]
        r1 = ret.iloc[tp + 1]
        def cw(names):
            w = m[names]; x = r1[names]; ok = x.notna(); return float((w[ok] * x[ok]).sum() / w[ok].sum())
        rows.append(dict(month=months[tp + 1], top=cw(top), rest=cw(rest)))
        if tp >= 12:  # Fama-MacBeth cross-section
            mom = (lr.iloc[tp - 1] - lr.iloc[tp - 12]).reindex(m.index)
            X = pd.DataFrame({"size": np.log(m), "mom": mom, "y": r1.reindex(m.index)}).dropna()
            if len(X) > 100:
                z = (X[["size", "mom"]] - X[["size", "mom"]].mean()) / X[["size", "mom"]].std()
                z["sxm"] = z["size"] * z["mom"]; z["sxm"] = (z.sxm - z.sxm.mean()) / z.sxm.std()
                A = np.column_stack([np.ones(len(z)), z[["size", "mom", "sxm"]].to_numpy()])
                b = np.linalg.lstsq(A, X.y.to_numpy(), rcond=None)[0]
                fm.append(dict(month=months[tp + 1], a=b[0], size=b[1], mom=b[2], sxm=b[3]))
    S = pd.DataFrame(rows).set_index("month"); S["spread"] = S.top - S.rest
    S.to_csv(os.path.join(ROOT, "results", "v3_monthly_spread.csv"))
    s = S.spread
    cum = (1 + s).cumprod(); dd = cum / cum.cummax() - 1
    r12 = (1 + s).rolling(12).apply(np.prod, raw=True) - 1
    out = {"risk": {"months": int(len(s)), "first": str(s.index[0].date()), "last": str(s.index[-1].date()),
                    "ann_mean": float(s.mean() * 12), "ann_vol": float(s.std() * np.sqrt(12)),
                    "info_ratio": float(s.mean() / s.std() * np.sqrt(12)), "nw_t": nw_t(s, 6)["t"],
                    "max_drawdown": float(dd.min()), "max_dd_trough": str(dd.idxmin().date()),
                    "worst_12m": float(r12.min()), "worst_12m_end": str(r12.idxmin().date()), "best_12m": float(r12.max()),
                    "share_months_positive": float((s > 0).mean())}}
    F = ff_monthly(); D = S.join(F, how="inner")
    fac = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "MOM"]
    o = nw_ols(D.spread, D[fac], 6)
    out["attribution"] = {"months": int(o["n"]), "alpha_monthly": float(o["coef"][0]), "alpha_ann": float(o["coef"][0] * 12), "alpha_t": float(o["t"][0]),
                          "r2": float(o["r2"]), "loadings": {f: {"beta": float(o["coef"][i + 1]), "t": float(o["t"][i + 1])} for i, f in enumerate(fac)},
                          "raw_ann": float(D.spread.mean() * 12)}
    o2 = nw_ols(D.spread, D[["Mkt-RF", "SMB"]], 6)
    out["attribution"]["market_size_only"] = {"alpha_ann": float(o2["coef"][0] * 12), "alpha_t": float(o2["t"][0]), "r2": float(o2["r2"])}
    FM = pd.DataFrame(fm).set_index("month")
    out["fama_macbeth"] = {"months": int(len(FM)), **{k: {"mean_bp": float(FM[k].mean() * 1e4), "t": nw_t(FM[k], 6)["t"]} for k in ["size", "mom", "sxm"]},
                           "note": "slopes per 1 s.d., next-month return; sxm = size x momentum interaction"}
    C = pd.read_csv(os.path.join(ROOT, "results", "concentration_monthly.csv"), index_col=0, parse_dates=True)
    yr = C.groupby(C.index.year).agg(C_end=("C", "last"), spread=("spread", "mean"), won=("spread", lambda x: float((x.dropna() > 0).mean()) if x.notna().any() else np.nan),
                                       ew_cw=("ew_cw", "mean"), n=("spread", "count"))
    out["annual"] = [{"year": int(y), "C_end": float(r.C_end), "spread": None if pd.isna(r.spread) else float(r.spread),
                      "won": None if pd.isna(r.won) else float(r.won), "ew_cw": None if pd.isna(r.ew_cw) else float(r.ew_cw), "n": int(r.n)} for y, r in yr.iterrows()]
    json.dump(out, open(os.path.join(ROOT, "results", "v3_extras.json"), "w"), indent=2, default=float)
    print(json.dumps(out, indent=1, default=float))

if __name__ == "__main__":
    main()
