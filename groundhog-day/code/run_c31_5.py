# -*- coding: utf-8 -*-
"""C31-5 (PREREGISTRATION_C31_R_2026-10-08.md + Clarification 1): midterm gap in the unseen pre-1928 sample.
Shiller monthly price P; window P(Mar, y+1) / P(Nov, y) - 1. Reported: calibration 1928-2025 and NBER extension."""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # paths made repo-relative 9 Oct 2026 (stress test)
SEED, DRAWS, GATE = 42, 10000, 0.025


def perm_one_sided(x, y, alternative="greater", n=DRAWS, seed=SEED):
    x, y = np.asarray(x, float), np.asarray(y, float)
    v = np.concatenate([x, y]); nx = len(x); obs = x.mean() - y.mean()
    rng = np.random.default_rng(seed); d = np.empty(n)
    for i in range(n):
        p = rng.permutation(v); d[i] = p[:nx].mean() - p[nx:].mean()
    k = np.sum(d >= obs) if alternative == "greater" else np.sum(d <= obs)
    return float(obs), float((k + 1) / (n + 1))


NBER = [("1869-06", "1870-12"), ("1873-10", "1879-03"), ("1882-03", "1885-05"), ("1887-03", "1888-04"), ("1890-07", "1891-05"),
        ("1893-01", "1894-06"), ("1895-12", "1897-06"), ("1899-06", "1900-12"), ("1902-09", "1904-08"), ("1907-05", "1908-06"),
        ("1910-01", "1912-01"), ("1913-01", "1914-12"), ("1918-08", "1919-03"), ("1920-01", "1921-07"), ("1923-05", "1924-07"),
        ("1926-10", "1927-11"), ("1929-08", "1933-03"), ("1937-05", "1938-06"), ("1945-02", "1945-10"), ("1948-11", "1949-10"),
        ("1953-07", "1954-05"), ("1957-08", "1958-04"), ("1960-04", "1961-02"), ("1969-12", "1970-11"), ("1973-11", "1975-03"),
        ("1980-01", "1980-07"), ("1981-07", "1982-11"), ("1990-07", "1991-03"), ("2001-03", "2001-11"), ("2007-12", "2009-06"),
        ("2020-02", "2020-04")]


def in_rec(y):
    m = pd.Period(f"{y}-11", "M")  # vote month
    return any(pd.Period(p, "M") < m <= pd.Period(t, "M") for p, t in NBER)


def windows(sh, years):
    P = sh["price"]
    out = {}
    for y in years:
        a, b = pd.Timestamp(f"{y}-11-01"), pd.Timestamp(f"{y + 1}-03-01")
        if a in P.index and b in P.index and np.isfinite(P[a]) and np.isfinite(P[b]):
            out[y] = P[b] / P[a] - 1
    return pd.Series(out)


def test(w, mids):
    m = w[w.index.isin(mids)]; c = w[~w.index.isin(mids)]
    d, p = perm_one_sided(m.values, c.values)
    t = stats.ttest_ind(m, c, equal_var=False, alternative="greater")
    return {"n_mid": len(m), "n_ctrl": len(c), "mid": float(m.mean()), "ctrl": float(c.mean()), "diff": d, "perm_p": p,
            "welch_t": float(t.statistic), "welch_p": float(t.pvalue), "sd_all": float(w.std())}


def main():
    sh = pd.read_csv(os.path.join(ROOT, "data", "shiller_dividends.csv"), parse_dates=["date"]).set_index("date").sort_index()
    pre = list(range(1871, 1928)); mids_pre = [y for y in pre if y % 4 == 2 and y >= 1874]
    w = windows(sh, pre)
    S = {"C31-5": {**test(w, mids_pre), "gate": GATE}}
    S["C31-5"]["passed"] = bool(S["C31-5"]["perm_p"] < GATE)
    S["C31-5"]["midterm_years"] = mids_pre
    S["C31-5"]["by_year"] = {int(k): float(v) for k, v in w.items()}
    # reported: calibration on the C31 years (1928-2025; midterms 1930-2022)
    cal = list(range(1928, 2026)); mids_cal = [y for y in cal if y % 4 == 2]
    wc = windows(sh, cal)
    S["calibration_1928_2025"] = test(wc, mids_cal)
    # correlation with the daily ret[+1,+90] used in C31-1
    wy = pd.read_csv(os.path.join(ROOT, "results", "windows_by_year.csv"), index_col="year")["ret[1,90]"]
    j = pd.concat([wc.rename("monthly"), wy.rename("daily")], axis=1).dropna()
    S["calibration_1928_2025"]["corr_with_daily_ret90"] = float(j.corr().iloc[0, 1])
    # reported: pre-1928 with NBER recession-at-vote control (exclusion and OLS)
    rec = pd.Series({y: in_rec(y) for y in w.index})
    S["pre1928_recession"] = {"mid_years_with_recession": [y for y in mids_pre if rec[y]],
                              "ctrl_share_recession": float(rec[~rec.index.isin(mids_pre)].mean())}
    keep = rec[~rec].index
    S["pre1928_recession"]["excl"] = test(w.loc[keep], mids_pre)
    X = np.column_stack([np.ones(len(w)), w.index.isin(mids_pre).astype(float), rec.reindex(w.index).astype(float)])
    beta, *_ = np.linalg.lstsq(X, w.values, rcond=None)
    S["pre1928_recession"]["ols_midterm_coef"] = float(beta[1])
    # pooled all years 1871-2025 (reported)
    allw = pd.concat([w, wc]); allm = [y for y in allw.index if y % 4 == 2 and y >= 1874]
    S["pooled_1871_2025_monthly"] = test(allw, allm)
    json.dump(S, open(os.path.join(ROOT, "results_r", "summary_c31_5.json"), "w"), indent=2)
    print(json.dumps({k: (v if k != "C31-5" else {kk: vv for kk, vv in v.items() if kk != "by_year"}) for k, v in S.items()}, indent=1))


if __name__ == "__main__":
    main()
