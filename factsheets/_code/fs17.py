# -*- coding: utf-8 -*-
"""FS17: fundamentals outside the US at factor level (JKP 2013-2025, ART 1999-2013), as pre-registered
in planning/PREREG_FS17.md. Writes results/fs17.json."""
import json
import os

import numpy as np
import pandas as pd

import perf

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results"); FAC = os.path.join(HERE, "..", "factors")
THEMES = ["Profit growth", "Issuance", "Value", "Profitability"]
JKP_CL = {"Profit growth": "Profit Growth", "Issuance": "Debt Issuance", "Value": "Value", "Profitability": "Profitability"}
ART_F = {"Profit growth": "Revision (composite)", "Issuance": "Buyback (composite)", "Value": "Value (composite)", "Profitability": "Profitability (composite)"}
B_MKT = {"UK": "gbr", "DK": "dnk", "EU": "world_ex_us", "WD": "world", "US": "usa"}
A_MKT = {"EU_A": "Europe", "UK_A": "UK", "US_A": "America"}
NONUS_B, NONUS_A = ["UK", "DK", "EU"], ["EU_A", "UK_A"]
MN = {"UK": "UK", "DK": "Denmark", "EU": "EU (World ex US)", "WD": "World", "US": "US", "EU_A": "Europe", "UK_A": "UK", "US_A": "America"}


def m(ix):
    return pd.DatetimeIndex(ix).to_period("M").to_timestamp("M")


def scale(x):
    vol = x.rolling(12, min_periods=6).std().shift(1) * np.sqrt(12)
    return (x * (0.10 / vol).clip(upper=3.0)).dropna()


def nw_reg(y, X):
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    yy = df["y"].values; A = np.column_stack([np.ones(len(df)), df.drop(columns="y").values])
    b, *_ = np.linalg.lstsq(A, yy, rcond=None); e = yy - A @ b
    u = A * e[:, None]; S = u.T @ u
    for L in range(1, 7):
        w = 1 - L / 7; G = u[L:].T @ u[:-L]; S += w * (G + G.T)
    XtXi = np.linalg.inv(A.T @ A); V = XtXi @ S @ XtXi
    return dict(alpha=float(b[0] * 12), t=float(b[0] / np.sqrt(V[0, 0])), r2=float(1 - e.var() / yy.var()), n=int(len(df)))


def themes_B():
    cl = pd.read_csv(os.path.join(FAC, "jkp_cluster_labels.csv")).set_index("characteristic")["cluster"]; out = {}
    for R, c in B_MKT.items():
        f = pd.read_csv(os.path.join(FAC, f"jkp_{c}_factors_monthly.csv"), index_col=0, parse_dates=True); f.index = m(f.index)
        out[R] = pd.DataFrame({t: f[[k for k in f.columns if cl.get(k) == JKP_CL[t]]].mean(axis=1) for t in THEMES}).loc["2012-01":"2025-12"]
    return out


def themes_A():
    s = pd.read_csv(os.path.join(FAC, "art_factor_spreads_monthly.csv"), index_col=0, parse_dates=True); s.index = m(s.index)
    return {R: pd.DataFrame({t: s[f"{seg}|{ART_F[t]}"] for t in THEMES}).loc["1998-01":"2013-03"] for R, seg in A_MKT.items()}


def legs(pkl, R, idx=None):
    B = pd.read_pickle(os.path.join(RES, pkl))[R]
    L = pd.DataFrame({"low beta": B["beta"].bn_net, "momentum": B["mom"].bn_net}); L.index = m(L.index)
    return L


def analyse(TH, pkl, markets, nonus, window):
    res = {}; pair_s, short_s, comb_s = {}, {}, {}
    for R in markets:
        L = legs(pkl, R); T = TH[R]
        Ls = L.apply(scale); Ts = T.apply(scale)
        pair = Ts[["Profit growth", "Issuance"]].mean(axis=1)
        rows = {t: nw_reg(Ts[t], Ls) | dict(sharpe=perf.sharpe(T[t].loc[window[0]:window[1]].dropna())) for t in THEMES}
        rows["pair"] = nw_reg(pair, Ls) | dict(sharpe=perf.sharpe(pair.loc[window[0]:window[1]].dropna()))
        sh = Ls.mean(axis=1); cb = pd.concat([Ls, Ts[["Profit growth", "Issuance"]]], axis=1).dropna().mean(axis=1)
        idx = sh.index.intersection(cb.index).intersection(pair.index)
        idx = idx[(idx >= pd.Timestamp(window[0])) & (idx <= pd.Timestamp(window[1]))]
        d = (cb - sh).reindex(idx)
        res[R] = dict(themes=rows, short_sharpe=perf.sharpe(sh.reindex(idx)), comb_sharpe=perf.sharpe(cb.reindex(idx)), diff_t=perf.nw_t(d.dropna())["t"],
                      corr_pair_short=float(pair.reindex(idx).corr(sh.reindex(idx))), months=int(len(idx)))
        pair_s[R] = pair.reindex(idx); short_s[R] = Ls.reindex(idx); comb_s[R] = (sh.reindex(idx), cb.reindex(idx))
    # pooled over non-US markets
    y = pd.concat([pair_s[R] for R in nonus], axis=1).mean(axis=1)
    X = pd.concat({R: short_s[R] for R in nonus}, axis=1).T.groupby(level=1).mean().T
    pooled = nw_reg(y, X)
    shp = pd.concat([comb_s[R][0] for R in nonus], axis=1).mean(axis=1); cbp = pd.concat([comb_s[R][1] for R in nonus], axis=1).mean(axis=1)
    pooled.update(short_sharpe=perf.sharpe(shp.dropna()), comb_sharpe=perf.sharpe(cbp.dropna()), diff_t=perf.nw_t((cbp - shp).dropna())["t"])
    per_theme = {}
    for t in THEMES:
        yt = pd.concat([TH[R][t].pipe(scale).reindex(pair_s[R].index) for R in nonus], axis=1).mean(axis=1)
        per_theme[t] = nw_reg(yt, X)
    return res, pooled, per_theme


def main():
    B, A = themes_B(), themes_A()
    rb, pb, tb = analyse(B, "battery_price.pkl", list(B_MKT), NONUS_B, ("2013-02-28", "2025-12-31"))
    ra, pa, ta = analyse(A, "battery_art.pkl", list(A_MKT), NONUS_A, ("1999-02-28", "2013-03-31"))
    passed = pb["t"] > 2 and pa["t"] > 2
    out = dict(B=dict(markets=rb, pooled=pb, pooled_themes=tb), A=dict(markets=ra, pooled=pa, pooled_themes=ta), passed=bool(passed), names=MN, themes=THEMES)
    json.dump(out, open(os.path.join(RES, "fs17.json"), "w"), indent=1, default=float)
    print("2013-25 pooled pair alpha", round(pb["alpha"] * 100, 2), "t", round(pb["t"], 2), "| Sharpe short", round(pb["short_sharpe"], 2), "comb", round(pb["comb_sharpe"], 2), "diff t", round(pb["diff_t"], 2))
    print("1999-13 pooled pair alpha", round(pa["alpha"] * 100, 2), "t", round(pa["t"], 2), "| Sharpe short", round(pa["short_sharpe"], 2), "comb", round(pa["comb_sharpe"], 2), "diff t", round(pa["diff_t"], 2))
    print("themes B", {t: (round(v["alpha"] * 100, 1), round(v["t"], 2)) for t, v in tb.items()})
    print("themes A", {t: (round(v["alpha"] * 100, 1), round(v["t"], 2)) for t, v in ta.items()})
    for per, rr in (("B", rb), ("A", ra)):
        for R, v in rr.items():
            print(per, R, "pair a", round(v["themes"]["pair"]["alpha"] * 100, 1), "t", round(v["themes"]["pair"]["t"], 2), "SR short", round(v["short_sharpe"], 2), "comb", round(v["comb_sharpe"], 2), "corr", round(v["corr_pair_short"], 2))
    print("PASSED" if passed else "NOT PASSED")


if __name__ == "__main__":
    main()
