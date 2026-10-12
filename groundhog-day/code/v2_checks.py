# -*- coding: utf-8 -*-
"""Groundhog Day, version 2: checks added after external review (October 2026).

REPORTED, NOT GATED. None of these checks was pre-registered; none changes C31-1's verdict.
They answer the reviewer's questions: is the result an artefact of eras, recessions, a weak
control, decay, missing dividends, or something every market shows?

    python code/v2_checks.py            -> results/v2_checks.json
Optional inputs (downloaded on Windows by code/v2_download.py):
    data/FTSE_daily_close.csv, data/GDAXI_daily_close.csv, data/shiller_dividends.csv
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from eventstudies import core  # noqa: E402
from run_midterm import perm_one_sided, welch, SEED, DRAWS  # noqa: E402

OUT = os.path.join(ROOT, "results")
COL = "ret[1,90]"

# NBER business-cycle peaks and troughs (month of peak, month of trough), 1926 onwards
NBER = [("1926-10", "1927-11"), ("1929-08", "1933-03"), ("1937-05", "1938-06"), ("1945-02", "1945-10"),
        ("1948-11", "1949-10"), ("1953-07", "1954-05"), ("1957-08", "1958-04"), ("1960-04", "1961-02"),
        ("1969-12", "1970-11"), ("1973-11", "1975-03"), ("1980-01", "1980-07"), ("1981-07", "1982-11"),
        ("1990-07", "1991-03"), ("2001-03", "2001-11"), ("2007-12", "2009-06"), ("2020-02", "2020-04")]


def in_recession(d):
    d = pd.Timestamp(d)
    for p, t in NBER:
        # recession months are peak+1 .. trough (NBER convention)
        if pd.Period(p, "M") < d.to_period("M") <= pd.Period(t, "M"):
            return True
    return False


def stratified_perm(vals, is_mid, strata, n=DRAWS, seed=SEED):
    """One-sided p for mean(mid)-mean(ctrl), labels shuffled only within strata."""
    vals, is_mid, strata = np.asarray(vals, float), np.asarray(is_mid, bool), np.asarray(strata)
    obs = vals[is_mid].mean() - vals[~is_mid].mean()
    rng = np.random.default_rng(seed)
    groups = [np.where(strata == s)[0] for s in np.unique(strata)]
    k = 0
    lab = is_mid.copy()
    for _ in range(n):
        for g in groups:
            lab[g] = rng.permutation(is_mid[g])
        if vals[lab].mean() - vals[~lab].mean() >= obs:
            k += 1
    return float(obs), float((k + 1) / (n + 1))


def strat_diff(vals, is_mid, strata):
    """Within-stratum differences, averaged with midterm-count weights."""
    df = pd.DataFrame({"v": vals, "m": is_mid, "s": strata})
    rows, w = [], []
    for s, g in df.groupby("s"):
        if g.m.sum() and (~g.m).sum():
            rows.append(g[g.m].v.mean() - g[~g.m].v.mean()); w.append(g.m.sum())
    return float(np.average(rows, weights=w))


def era(y):
    return "1928-59" if y <= 1959 else ("1960-89" if y <= 1989 else "1990-2025")


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def main():
    tab = pd.read_csv(os.path.join(OUT, "windows_by_year.csv"), index_col="year", parse_dates=["date"])
    tab = tab[tab[COL].notna()].copy()
    tab["mid"] = tab.kind == "midterm"
    tab["era"] = [era(y) for y in tab.index]
    tab["recession_at_election"] = [in_recession(d) for d in tab.date]
    end90 = tab.date + pd.Timedelta(days=130)
    tab["recession_in_window"] = [any(in_recession(d) for d in pd.date_range(a, b, freq="MS")) or in_recession(a)
                                  for a, b in zip(tab.date, end90)]
    v, m = tab[COL].to_numpy(), tab.mid.to_numpy()
    base = float(v[m].mean() - v[~m].mean())
    out = {"note": "Added in version 2 after external review. Reported, not gated.", "base_diff": r4(base),
           "n_mid": int(m.sum()), "n_ctrl": int((~m).sum())}

    # 1. block permutation within eras
    d, p = stratified_perm(v, m, tab.era)
    by = {e: dict(n_mid=int(g.mid.sum()), n_ctrl=int((~g.mid).sum()), mid=r4(g[g.mid][COL].mean()),
                  ctrl=r4(g[~g.mid][COL].mean()), diff=r4(g[g.mid][COL].mean() - g[~g.mid][COL].mean()))
          for e, g in tab.groupby("era")}
    out["era_permutation"] = dict(diff=r4(d), p_one_sided=r4(p), within_era_weighted_diff=r4(strat_diff(v, m, tab.era)), by_era=by)

    # 2. recessions: who had one, matched comparison, exclusion
    rec = {}
    for flag in ["recession_at_election", "recession_in_window"]:
        f = tab[flag].to_numpy()
        dm, pm = stratified_perm(v, m, f)
        keep = ~f
        de, pe, _ = perm_one_sided(v[m & keep], v[~m & keep], "greater")
        rec[flag] = dict(mid_years_with=sorted(int(y) for y in tab.index[m & f]),
                         share_mid=r4(f[m].mean()), share_ctrl=r4(f[~m].mean()),
                         matched_diff=r4(strat_diff(v, m, f)), matched_p=r4(pm),
                         excl_n_mid=int((m & keep).sum()), excl_n_ctrl=int((~m & keep).sum()),
                         excl_diff=r4(de), excl_p=r4(pe),
                         mid_rec=r4(v[m & f].mean()), ctrl_rec=r4(v[~m & f].mean()), n_ctrl_rec=int((~m & f).sum()),
                         mid_norec=r4(v[m & keep].mean()), ctrl_norec=r4(v[~m & keep].mean()),
                         ctrl_years_with=sorted(int(y) for y in tab.index[~m & f]))
    # how many midterm recessions ended (NBER trough) within six months of the vote
    tr = [pd.Period(t, "M") for _, t in NBER]
    ends = {int(y): any(0 <= (t - pd.Timestamp(d).to_period("M")).n <= 6 for t in tr)
            for y, d in zip(tab.index[m], tab.date[m]) if in_recession(d)}
    rec["mid_recession_ended_within_6m"] = ends
    out["recessions"] = rec

    # 3. why is the control weak?
    C = tab[~tab.mid][COL].sort_values()
    M = tab[tab.mid][COL]
    worst = [{"year": int(y), "ret": r4(r)} for y, r in C.head(8).items()]
    drop = {}
    for k in [3, 5, 8]:
        c2 = C.iloc[k:]
        drop[str(k)] = dict(ctrl=r4(c2.mean()), diff=r4(M.mean() - c2.mean()))
    # symmetric: drop k worst from BOTH groups (worst midterms too)
    sym = {}
    for k in [2, 3]:
        sym[str(k)] = r4(M.sort_values().iloc[k:].mean() - C.iloc[round(k * len(C) / len(M)):].mean())
    trim = lambda s, q=0.1: s[(s >= s.quantile(q)) & (s <= s.quantile(1 - q))].mean()
    dec = {}
    for dcd, g in tab.groupby((tab.index // 10) * 10):
        dec[f"{dcd}s"] = dict(mid=r4(g[g.mid][COL].mean()), ctrl=r4(g[~g.mid][COL].mean()), n_ctrl=int((~g.mid).sum()))
    out["control_weakness"] = dict(
        ctrl_mean=r4(C.mean()), ctrl_median=r4(C.median()), mid_mean=r4(M.mean()), mid_median=r4(M.median()),
        median_diff=r4(M.median() - C.median()), trimmed10_diff=r4(trim(M) - trim(C)),
        ctrl_share_negative=r4((C < 0).mean()), mid_share_negative=r4((M < 0).mean()),
        ctrl_worst8=worst, mid_worst3=[{"year": int(y), "ret": r4(r)} for y, r in M.sort_values().head(3).items()],
        drop_worst_ctrl=drop, drop_worst_both=sym,
        by_kind={k: r4(g[COL].mean()) for k, g in tab.groupby("kind")}, by_decade=dec)

    # 4. decay: splits and rolling 26-year windows (about six midterms each)
    splits = {}
    for cut in [1980, 2003]:
        a, b = tab[tab.index < cut], tab[tab.index >= cut]
        splits[str(cut)] = dict(before=r4(a[a.mid][COL].mean() - a[~a.mid][COL].mean()), n_mid_before=int(a.mid.sum()),
                                after=r4(b[b.mid][COL].mean() - b[~b.mid][COL].mean()), n_mid_after=int(b.mid.sum()),
                                p_after=r4(perm_one_sided(b[b.mid][COL], b[~b.mid][COL], "greater")[1]))
    roll = []
    for s in range(1928, 2026 - 25):
        g = tab[(tab.index >= s) & (tab.index <= s + 25)]
        roll.append(dict(start=s, end=s + 25, n_mid=int(g.mid.sum()), diff=r4(g[g.mid][COL].mean() - g[~g.mid][COL].mean())))
    rd = pd.DataFrame(roll)
    rd.to_csv(os.path.join(OUT, "v2_rolling26.csv"), index=False)
    # trend in midterm minus control: regress each midterm's excess over its era-free control on year
    yrs = tab.index[tab.mid].to_numpy(); ex = M.to_numpy() - C.mean()
    slope = np.polyfit(yrs, ex, 1)[0]
    out["decay"] = dict(splits=splits, rolling_min=r4(rd["diff"].min()), rolling_max=r4(rd["diff"].max()),
                        rolling_share_positive=r4((rd["diff"] > 0).mean()), rolling_last=roll[-1],
                        slope_per_decade=r4(slope * 10))

    # 5. dividends (needs data/shiller_dividends.csv: date, price, dividend [annual rate])
    fp = os.path.join(ROOT, "data", "shiller_dividends.csv")
    if os.path.exists(fp):
        sh = pd.read_csv(fp, parse_dates=["date"]).set_index("date").sort_index()
        dy = (sh["dividend"] / sh["price"]).dropna()
        yld = np.array([dy[:d].iloc[-1] if len(dy[:d]) else np.nan for d in tab.date])
        tr = v + yld * 90 / 252
        ok = ~np.isnan(tr)
        dtr, ptr, _ = perm_one_sided(tr[m & ok], tr[~m & ok], "greater")
        out["total_return"] = dict(diff=r4(dtr), p=r4(ptr), yld_mid=r4(np.nanmean(yld[m])), yld_ctrl=r4(np.nanmean(yld[~m])),
                                   n=int(ok.sum()), method="price return + dividend yield at election x 90/252 (Shiller)")
    else:
        out["total_return"] = "data/shiller_dividends.csv missing: run code/v2_download.py on Windows"

    # 6. international placebo: the same US election dates, other markets, local currency
    intl = {}
    n225 = [os.path.join(ROOT, "data", "N225_daily_close.csv")] + [os.path.join(ROOT, "..", d, "data", "N225_daily_close.csv") for d in ("A03_Titanic_AI_Bubble", "titanic")]
    srcs = {"Nikkei 225": next((f for f in n225 if os.path.exists(f)), n225[0]),
            "FTSE 100": os.path.join(ROOT, "data", "FTSE_daily_close.csv"),
            "DAX": os.path.join(ROOT, "data", "GDAXI_daily_close.csv")}
    spx = pd.read_csv(os.path.join(ROOT, "data", "GSPC_daily_close.csv"), index_col=0, parse_dates=True)["close"].sort_index()
    for name, f in srcs.items():
        if not os.path.exists(f):
            intl[name] = "missing: run code/download_data.py"; continue
        px = pd.read_csv(f, index_col=0, parse_dates=True)["close"].dropna().sort_index()
        px = px[px > 0]
        t = tab[tab.date >= px.index[0] + pd.Timedelta(days=200)]
        r = core.window_returns(px, t.date.values, (1, 90)).to_numpy()
        ok = ~np.isnan(r); mm = t.mid.to_numpy()
        dd, pp, _ = perm_one_sided(r[mm & ok], r[~mm & ok], "greater")
        s_same = t[COL].to_numpy()
        ds, _, _ = perm_one_sided(s_same[mm & ok], s_same[~mm & ok], "greater")
        intl[name] = dict(first_year=int(t.index[0]), n_mid=int((mm & ok).sum()), n_ctrl=int((~mm & ok).sum()),
                          mid=r4(np.nanmean(r[mm])), ctrl=r4(np.nanmean(r[~mm])), diff=r4(dd), p_one_sided=r4(pp),
                          sp500_diff_same_years=r4(ds), corr_with_sp500=r4(np.corrcoef(r[ok], s_same[ok])[0, 1]))
    out["international"] = intl

    json.dump(out, open(os.path.join(OUT, "v2_checks.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
