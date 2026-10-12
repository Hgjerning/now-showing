# -*- coding: utf-8 -*-
"""C31-4 (PREREGISTRATION_C31_R_2026-10-08.md): does the midterm gap survive macro controls?
ret[+1,+90] = a + b*midterm + c*recession_at_vote + d*ret[-249,0] + e*log CAPE(Oct) + f*CPI inflation (Sep y/y).
Freedman-Lane permutation (10,000, seed 42) of the controls-only residuals; statistic = b. HC3 t alongside."""
import json, os
import numpy as np, pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # paths made repo-relative 9 Oct 2026 (stress test)
import run_c31_5 as C5  # noqa: E402  NBER list and in_rec()

XLS = os.path.join(ROOT, "data", "ie_data.xls")
SEED, DRAWS, GATE = 42, 10000, 0.025


def shiller():
    x = pd.read_excel(XLS, sheet_name="Data", header=7)
    x = x[pd.to_numeric(x["Date"], errors="coerce").notna()].copy()
    d = x["Date"].astype(float); y = d.astype(int); m = ((d - y) * 100).round().astype(int).clip(1, 12)
    x.index = pd.PeriodIndex(pd.to_datetime(dict(year=y, month=m, day=1)), freq="M")
    return pd.to_numeric(x["CPI"], errors="coerce"), pd.to_numeric(x["CAPE"], errors="coerce")


def prior250(px, day0):
    i = px.index.searchsorted(day0)                       # day 0 = first trading day on/after the election date
    return px.iloc[i] / px.iloc[i - 250] - 1 if i >= 250 else np.nan


def fit(y, X):
    return sm.OLS(y, sm.add_constant(X)).fit()


def main():
    W = pd.read_csv(os.path.join(ROOT, "results", "windows_by_year.csv"), parse_dates=["date"]).set_index("year")
    px = pd.read_csv(os.path.join(ROOT, "data", "GSPC_daily_close.csv"), index_col=0, parse_dates=True)["close"].sort_index()
    px = px[~px.index.duplicated()]
    cpi, cape = shiller()
    df = pd.DataFrame({"y": W["ret[1,90]"], "mid": (W.kind == "midterm").astype(float)})
    df["rec"] = [float(C5.in_rec(y)) for y in df.index]
    df["prior"] = [prior250(px, d) for d in W.date]
    df["lcape"] = [np.log(cape.get(pd.Period(f"{y}-10", "M"), np.nan)) for y in df.index]
    df["infl"] = [cpi.get(pd.Period(f"{y}-09", "M"), np.nan) / cpi.get(pd.Period(f"{y - 1}-09", "M"), np.nan) - 1 for y in df.index]
    dropped = [int(y) for y in df.index[df.isna().any(axis=1)]]
    df = df.dropna()
    Z = ["rec", "prior", "lcape", "infl"]
    full = fit(df.y, df[["mid"] + Z]); b = float(full.params["mid"])
    hc3 = full.get_robustcov_results(cov_type="HC3")
    red = fit(df.y, df[Z]); fitted, res = red.fittedvalues.values, red.resid.values
    Xf = sm.add_constant(df[["mid"] + Z]).values
    beta_row = np.linalg.pinv(Xf)[1]                       # b = beta_row @ y
    rng = np.random.default_rng(SEED)
    bs = np.array([beta_row @ (fitted + rng.permutation(res)) for _ in range(DRAWS)])
    p = float((1 + np.sum(bs >= b)) / (DRAWS + 1))
    S = {"C31-4": {"b_midterm": b, "perm_p": p, "hc3_t": float(hc3.tvalues[1]), "hc3_p_one_sided": float(hc3.pvalues[1] / 2 if b > 0 else 1 - hc3.pvalues[1] / 2),
                   "n": int(len(df)), "n_mid": int(df.mid.sum()), "dropped_years": dropped, "gate": GATE, "passed": bool(p < GATE),
                   "coefs": {k: float(v) for k, v in full.params.items()}, "r2": float(full.rsquared)}}
    # reported variants
    rep = {}
    for k in Z:
        m = fit(df.y, df[["mid", k]]); rep[f"midterm_plus_{k}_only"] = {"b": float(m.params["mid"]), "t": float(m.tvalues["mid"])}
    def rec_win(y):
        months = pd.period_range(f"{y}-11", f"{y + 1}-03", freq="M")
        return float(any(pd.Period(a, "M") < mm <= pd.Period(b, "M") for mm in months for a, b in C5.NBER))
    df["rec_win"] = [rec_win(y) for y in df.index]
    m = fit(df.y, df[["mid", "rec_win", "prior", "lcape", "infl"]]); rep["recession_in_window_instead"] = {"b": float(m.params["mid"]), "t": float(m.tvalues["mid"])}
    dec = {}
    for name, sel in [("full", df.index >= 0), ("without_recession_at_vote_years", df.rec == 0),
                      ("post_1945", df.index >= 1946), ("post_2003", df.index >= 2003)]:
        d = df[sel]; diff, pp = C5.perm_one_sided(d.y[d.mid == 1].values, d.y[d.mid == 0].values)
        dec[name] = {"diff": diff, "perm_p": pp, "n_mid": int(d.mid.sum()), "n_ctrl": int((d.mid == 0).sum())}
    rep["decomposition"] = dec
    m = fit(df.y, df[["mid", "prior", "lcape", "infl"]]); rep["without_recession_control"] = {"b": float(m.params["mid"]), "t": float(m.tvalues["mid"])}
    df["mid_x_rec"] = df.mid * df.rec
    m = fit(df.y, df[["mid", "mid_x_rec"] + Z]); rep["interaction"] = {k: float(m.params[k]) for k in ("mid", "mid_x_rec")}
    rep["interaction_t"] = {k: float(m.tvalues[k]) for k in ("mid", "mid_x_rec")}
    S["reported"] = rep
    json.dump(S, open(os.path.join(ROOT, "results_r", "summary_c31_4.json"), "w"), indent=2)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
