# -*- coding: utf-8 -*-
"""A07 Under Pressure: distress scores vs future crashes (pre-registered, see PREREGISTRATION_A07)."""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10"))
from features import price_features  # noqa: E402
from panel import asof_monthly, load_all  # noqa: E402
from stats import auc, block_boot_mean, nw_t  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, os.environ.get("P10_RESULTS", "results"))
os.makedirs(OUT, exist_ok=True)
GATE = 0.05 / 3


def main():
    px, fd, pm, mc, uni, ret = load_all()
    months, tick = pm.index, px.columns
    cols = ["assets", "assetsc", "liabilities", "liabilitiesc", "workingcapital", "retearn", "ebit_ttm", "revenue_ttm", "netinc_ttm",
            "ncfo_ttm", "netinc_ttm_ly", "assets_ly", "ncfo_ttm_ly", "gp_ttm", "gp_ttm_ly", "revenue_ttm_ly", "currentratio",
            "currentratio_ly", "sharesbas", "sharesbas_ly", "debtnc", "debtnc_ly"]
    A = {c: asof_monthly(fd, c, months, tick) for c in cols}
    vol = price_features(px, pm)["vol252"]
    qe = [m for m in months if m.month in (3, 6, 9, 12) and pd.Timestamp("2012-12-31") <= m <= pd.Timestamp("2026-06-30")]
    rows = []
    P = px.to_numpy(); didx = px.index
    for d in qe:
        u = uni.loc[d]; t = u[u].index
        g = {c: A[c].loc[d, t] for c in cols}
        ok = g["assetsc"].notna() & g["liabilitiesc"].notna() & (g["assets"] > 0) & (g["liabilities"] > 0)
        t = t[ok.values]; g = {c: v[t] for c, v in g.items()}
        TA, TL = g["assets"], g["liabilities"]
        Z = 1.2 * g["workingcapital"] / TA + 1.4 * g["retearn"] / TA + 3.3 * g["ebit_ttm"] / TA + 0.6 * mc.loc[d, t] / TL + 1.0 * g["revenue_ttm"] / TA
        Znm = Z - 0.6 * mc.loc[d, t] / TL
        ni, nil = g["netinc_ttm"], g["netinc_ttm_ly"]
        O = (-1.32 - 0.407 * np.log(TA / 1e6) + 6.03 * TL / TA - 1.43 * g["workingcapital"] / TA + 0.0757 * g["liabilitiesc"] / g["assetsc"]
             - 1.72 * (TL > TA) - 2.37 * ni / TA - 1.83 * g["ncfo_ttm"] / TL + 0.285 * ((ni < 0) & (nil < 0)) - 0.521 * (ni - nil) / (ni.abs() + nil.abs()))
        roa, roal = ni / TA, nil / g["assets_ly"]
        F = ((roa > 0).astype(int) + (g["ncfo_ttm"] > 0) + (roa > roal) + (g["ncfo_ttm"] > ni) + (g["debtnc"] / TA < g["debtnc_ly"] / g["assets_ly"])
             + (g["currentratio"] > g["currentratio_ly"]) + (g["sharesbas"] <= g["sharesbas_ly"])
             + (g["gp_ttm"] / g["revenue_ttm"] > g["gp_ttm_ly"] / g["revenue_ttm_ly"]) + (g["revenue_ttm"] / TA > g["revenue_ttm_ly"] / g["assets_ly"]))
        F = F.where(nil.notna() & g["assets_ly"].notna())
        # outcome: 12-month drawdown from formation close
        i0 = didx.searchsorted(d, side="right") - 1
        crash, r12, minr = {}, {}, {}
        for tk in t:
            j = px.columns.get_loc(tk); p0 = P[i0, j]
            if not np.isfinite(p0):
                continue
            path = P[i0 + 1:i0 + 253, j]; path = path[np.isfinite(path)]
            if len(path) == 0:
                continue
            crash[tk] = path.min() / p0 <= 0.6; minr[tk] = path.min() / p0; r12[tk] = path[-1] / p0 - 1
        df = pd.DataFrame({"Z": Z, "O": O, "F": F, "vol": vol.loc[d, t], "crash": pd.Series(crash), "r12": pd.Series(r12), "Z_nm": Znm, "minr": pd.Series(minr)})
        df["date"] = d; rows.append(df)
    D = pd.concat(rows); D.index.name = "ticker"; D = D.reset_index()
    D.to_csv(os.path.join(OUT, "scores_panel_ext.csv"), index=False); return
    E = D[D.date <= "2025-06-30"].dropna(subset=["crash"])
    E["crash"] = E.crash.astype(bool)
    per = []
    for d, g in E.groupby("date"):
        c = g.dropna(subset=["O", "vol"])
        per.append(dict(date=d, n=len(g), crashes=int(g.crash.sum()), auc_Z=auc(-g.Z, g.crash), auc_O=auc(g.O, g.crash), auc_F=auc(-g.F, g.crash),
                        auc_vol=auc(g.vol, g.crash), auc_O_c=auc(c.O, c.crash), auc_vol_c=auc(c.vol, c.crash)))
    PD = pd.DataFrame(per).set_index("date"); PD.to_csv(os.path.join(OUT, "auc_by_date.csv"))
    S = {}
    a1 = block_boot_mean(PD.auc_Z.dropna(), 4, 10000, 42, null=0.5); S["A07-1"] = {**a1, "passed": bool(a1["p"] < GATE)}
    dd = (PD.auc_O_c - PD.auc_vol_c).dropna(); a2 = block_boot_mean(dd, 4, 10000, 42, 0.0)
    S["A07-2"] = {**a2, "auc_O": float(PD.auc_O_c.mean()), "auc_vol": float(PD.auc_vol_c.mean()), "passed": bool(a2["p"] < GATE)}
    # A07-3: quintile portfolios on O, formed quarterly, held 3 months
    Dq = D.dropna(subset=["O"]).copy(); Dq["q"] = Dq.groupby("date").O.transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) + 1)
    pr = []
    for m in months[(months >= "2013-01-31") & (months <= "2026-08-31")]:
        f = max(x for x in qe if x < m); g = Dq[Dq.date == f]
        r = ret.loc[m, g.ticker].to_numpy()
        pr.append({"month": m, **{f"Q{k}": np.nanmean(r[(g.q == k).to_numpy()]) for k in range(1, 6)}})
    Q = pd.DataFrame(pr).set_index("month"); Q["safe_minus_distressed"] = Q.Q1 - Q.Q5; Q.to_csv(os.path.join(OUT, "O_quintile_returns.csv"))
    a3 = nw_t(Q.safe_minus_distressed, 6); S["A07-3"] = {**a3, "ann": a3["mean"] * 12, "passed": bool(a3["p_gt"] < GATE)}
    # reported
    E2 = E.dropna(subset=["O"]).copy(); E2["q"] = E2.groupby("date").O.transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) + 1)
    S["reported"] = {"auc_F": float(PD.auc_F.mean()), "auc_O_all": float(PD.auc_O.mean()), "auc_vol_all": float(PD.auc_vol.mean()),
                     "auc_Z": float(PD.auc_Z.mean()), "base_rate": float(E.crash.mean()), "n_obs": int(len(E)), "n_dates": int(len(PD)),
                     "crash_by_O_quintile": E2.groupby("q").crash.mean().to_dict(), "r12_by_O_quintile": E2.groupby("q").r12.mean().to_dict(),
                     "auc_Z_hit_share": float((PD.auc_Z > 0.5).mean()), "auc_vol_beats_O_share": float((PD.auc_vol_c > PD.auc_O_c).mean())}
    PD["year"] = PD.index.year; PD.groupby("year")[["auc_Z", "auc_O", "auc_F", "auc_vol", "crashes", "n"]].agg(
        {"auc_Z": "mean", "auc_O": "mean", "auc_F": "mean", "auc_vol": "mean", "crashes": "sum", "n": "sum"}).to_csv(os.path.join(OUT, "auc_by_year.csv"))
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=2, default=float)
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
