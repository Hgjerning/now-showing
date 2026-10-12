# -*- coding: utf-8 -*-
"""Case 31: the midterm rally against a same-season control.

Runs the trials of PREREGISTRATION_C31_2026-09-25.md and writes every number to ../results/.
Nothing here chooses a window: every window, seed and sample is the pre-registration's.

    python code/run_midterm.py
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from eventstudies import core  # noqa: E402

OUT = os.path.join(ROOT, "results")
os.makedirs(OUT, exist_ok=True)
SEED, DRAWS = 42, 10000
GATE = 0.05 / 2
MID_2026 = pd.Timestamp("2026-11-03")


def perm_one_sided(x, y, alternative, n=DRAWS, seed=SEED):
    """One-sided label-permutation p for mean(x) - mean(y). Add-one correction."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    v = np.concatenate([x, y]); nx = len(x)
    obs = x.mean() - y.mean()
    rng = np.random.default_rng(seed)
    d = np.empty(n)
    for i in range(n):
        p = rng.permutation(v)
        d[i] = p[:nx].mean() - p[nx:].mean()
    k = np.sum(d >= obs) if alternative == "greater" else np.sum(d <= obs)
    return float(obs), float((k + 1) / (n + 1)), d


def welch(x, y, alternative):
    diff, t, dof = core.welch_t(x, y)
    p = stats.t.sf(t, dof) if alternative == "greater" else stats.t.cdf(t, dof)
    return diff, t, dof, float(p)


def boot_ci(x, n=DRAWS, seed=SEED):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    m = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return np.quantile(m, [0.025, 0.975])


def boot_diff_ci(x, y, n=DRAWS, seed=SEED):
    rng = np.random.default_rng(seed)
    x, y = np.asarray(x, float), np.asarray(y, float)
    mx = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    my = rng.choice(y, size=(n, len(y)), replace=True).mean(axis=1)
    return np.quantile(mx - my, [0.025, 0.975])


def realised_vol(prices, dates, a, b):
    """Annualised sd of daily log returns over trading days a..b around each date."""
    r = np.log(prices).diff()
    pos = core.align_dates(dates, prices.index)
    R = r.to_numpy()
    out = []
    for p in pos:
        lo, hi = p + a, p + b
        out.append(np.nan if p < 0 or lo < 1 or hi >= len(R) else R[lo:hi + 1].std(ddof=1) * np.sqrt(252))
    return np.array(out)


def main():
    prices = pd.read_csv(os.path.join(ROOT, "data", "GSPC_daily_close.csv"), index_col=0, parse_dates=True)["close"].sort_index()
    parties = pd.read_csv(os.path.join(ROOT, "data", "us_presidential_elections.csv")).set_index("year")

    years = list(range(1928, 2026))
    dates = pd.Series([core.us_election_day(y) for y in years], index=pd.Index(years, name="year"))
    kind = pd.Series(["midterm" if (y % 2 == 0 and y % 4 != 0) else ("presidential" if y % 4 == 0 else "odd") for y in years], index=dates.index)

    tab = pd.DataFrame({"date": dates, "kind": kind})
    for (a, b) in [(1, 20), (1, 60), (1, 90), (1, 125), (1, 250), (-119, 0)]:
        r = core.window_returns(prices, dates.values, (a, b)); r.index = dates.index
        tab[f"ret[{a},{b}]"] = r
    tab["vol_pre20"] = realised_vol(prices, dates.values, -19, 0)
    tab["vol_post20"] = realised_vol(prices, dates.values, 1, 20)
    tab["vol_change"] = tab["vol_post20"] - tab["vol_pre20"]
    pres_party = {}
    for y in tab.index:
        last = max(e for e in parties.index if e <= y - 2) if y >= 1930 else None
        pres_party[y] = parties.loc[last, "winner_party"] if last is not None else np.nan
    tab["president_party"] = pd.Series(pres_party)
    tab.to_csv(os.path.join(OUT, "windows_by_year.csv"))

    M = tab[tab.kind == "midterm"]
    Cn = tab[tab.kind != "midterm"]
    out = {"n_midterm": int(M["ret[1,90]"].notna().sum()), "n_control": int(Cn["ret[1,90]"].notna().sum()),
           "data_start": str(prices.index[0].date()), "data_end": str(prices.index[-1].date())}

    # ---------------- C31-1
    x, y = M["ret[1,90]"].dropna(), Cn["ret[1,90]"].dropna()
    d, p_perm, dist1 = perm_one_sided(x, y, "greater")
    _, t, dof, p_w = welch(x, y, "greater")
    h1 = M[M.index <= 1974]["ret[1,90]"].dropna(); h2 = M[M.index >= 1978]["ret[1,90]"].dropna()
    dh1, dh2 = h1.mean() - y.mean(), h2.mean() - y.mean()
    passed1 = (p_perm < GATE) and dh1 > 0 and dh2 > 0
    out["C31-1"] = dict(mid_mean=x.mean(), ctrl_mean=y.mean(), diff=d, p_perm=p_perm, welch_t=t, welch_dof=dof, p_welch=p_w,
                        diff_half1_1930_1974=dh1, diff_half2_1978_2022=dh2, n_half1=len(h1), n_half2=len(h2),
                        ci_diff=list(boot_diff_ci(x, y)), passed=bool(passed1))

    # ---------------- C31-2
    x2, y2 = M["ret[-119,0]"].dropna(), Cn["ret[-119,0]"].dropna()
    d2, p2, _ = perm_one_sided(x2, y2, "less")
    _, t2, dof2, pw2 = welch(x2, y2, "less")
    g1 = M[M.index <= 1974]["ret[-119,0]"].dropna().mean() - y2.mean()
    g2 = M[M.index >= 1978]["ret[-119,0]"].dropna().mean() - y2.mean()
    out["C31-2"] = dict(mid_mean=x2.mean(), ctrl_mean=y2.mean(), diff=d2, p_perm=p2, welch_t=t2, p_welch=pw2,
                        diff_half1=g1, diff_half2=g2, ci_diff=list(boot_diff_ci(x2, y2)),
                        passed=bool(p2 < GATE and g1 < 0 and g2 < 0))

    # ---------------- reported: P3-4 replication (unconditional placebo) and same-season placebo
    plc = core.placebo_window_means(prices, len(x), (1, 90), DRAWS, SEED)
    out["P3-4_replication"] = dict(mid_mean=x.mean(), placebo_mean=plc.mean(), placebo_sd=plc.std(),
                                   p_two_sided=core.placebo_pvalue(x.mean(), plc))
    # ---------------- reported: horizons, splits, hit rates
    rows = []
    for col in ["ret[1,20]", "ret[1,60]", "ret[1,90]", "ret[1,125]", "ret[1,250]", "ret[-119,0]"]:
        xm, xc = M[col].dropna(), Cn[col].dropna()
        xp, xo = tab[tab.kind == "presidential"][col].dropna(), tab[tab.kind == "odd"][col].dropna()
        dd, tt, df_ = core.welch_t(xm, xc)
        lo, hi = boot_ci(xm)
        rows.append(dict(window=col, n_mid=len(xm), mid_mean=xm.mean(), mid_median=xm.median(), mid_ci_lo=lo, mid_ci_hi=hi,
                         mid_hit=(xm > 0).mean(), n_ctrl=len(xc), ctrl_mean=xc.mean(), ctrl_median=xc.median(), ctrl_hit=(xc > 0).mean(),
                         pres_mean=xp.mean(), odd_mean=xo.mean(), diff=dd, welch_t=tt,
                         p_two_sided=float(2 * stats.t.sf(abs(tt), df_))))
    hz = pd.DataFrame(rows); hz.to_csv(os.path.join(OUT, "horizons.csv"), index=False)

    k, n = int((x > 0).sum()), len(x)
    out["hit_rate"] = dict(k=k, n=n, mid_hit=k / n, ctrl_hit=float((y > 0).mean()),
                           p_binom_vs_ctrl=float(stats.binomtest(k, n, float((y > 0).mean()), alternative="greater").pvalue))
    party = M.groupby("president_party")["ret[1,90]"].agg(["count", "mean", "median"])
    party.to_csv(os.path.join(OUT, "by_president_party.csv"))
    out["party"] = party.to_dict()
    # control split
    out["control_split"] = {k_: float(tab[tab.kind == k_]["ret[1,90]"].mean()) for k_ in ["presidential", "odd"]}

    # ---------------- reported: volatility
    vm, vc = M["vol_change"].dropna(), Cn["vol_change"].dropna()
    dv, tv, dfv = core.welch_t(vm, vc)
    out["vol"] = dict(mid_pre=M["vol_pre20"].mean(), mid_post=M["vol_post20"].mean(), ctrl_pre=Cn["vol_pre20"].mean(), ctrl_post=Cn["vol_post20"].mean(),
                      mid_change=vm.mean(), ctrl_change=vc.mean(), diff=dv, welch_t=tv,
                      share_mid_falls=float((vm < 0).mean()), share_ctrl_falls=float((vc < 0).mean()))

    # ---------------- paths: midterm vs control mean path, with same-season band
    PRE, POST = 120, 90
    pm = core.event_paths(prices, M["date"].values, PRE, POST); pm.index = M.index
    pc = core.event_paths(prices, Cn["date"].values, PRE, POST); pc.index = Cn.index
    pm.to_csv(os.path.join(OUT, "paths_midterm.csv")); pc.to_csv(os.path.join(OUT, "paths_control.csv"))
    # band: mean over 24 randomly drawn control years, rebased at day 0
    rng = np.random.default_rng(SEED)
    pcv = pc.dropna()
    base0 = (1 + pcv).div(1 + pcv[0], axis=0) - 1
    draws = rng.integers(0, len(base0), size=(2000, len(x)))
    arr = base0.to_numpy()
    means = arr[draws].mean(axis=1)
    band = pd.DataFrame(np.quantile(means, [0.05, 0.5, 0.95], axis=0).T, index=base0.columns, columns=["q05", "q50", "q95"])
    band.to_csv(os.path.join(OUT, "band_control_rebased_day0.csv"))

    # ---------------- forward: 2026
    # (a) return needed in 2026 for the pooled test to clear the gate (Welch approximation, then checked by permutation)
    def pooled_p(r26, n_perm=4000):
        xx = np.append(x.to_numpy(), r26)
        return perm_one_sided(xx, y, "greater", n=n_perm, seed=SEED)[1]

    def pooled_welch(r26):
        xx = np.append(x.to_numpy(), r26)
        return welch(xx, y, "greater")[3]
    grid = np.round(np.arange(-0.30, 0.61, 0.005), 3)
    wp = np.array([pooled_welch(g) for g in grid])
    need = float(grid[np.argmax(wp < GATE)]) if (wp < GATE).any() else None
    keep_p = pooled_welch(x.mean())
    fwd = dict(p_now_welch=p_w, p_if_2026_equals_mid_mean=float(keep_p))
    fwd["needed_r26_welch"] = need
    if need is not None:
        fwd["perm_p_at_needed"] = pooled_p(need)
        fwd["perm_p_at_needed_minus_1pt"] = pooled_p(need - 0.01)
    # the level of r26 at which p gets no better than today's
    worse = grid[wp > p_w]
    fwd["r26_at_which_p_worsens_below"] = float(worse.max()) if len(worse) else None
    # prediction: shrink midterm mean halfway to control mean, spread from control distribution
    shrunk = 0.5 * x.mean() + 0.5 * y.mean()
    dev = y - y.mean()
    q10, q90 = shrunk + np.quantile(dev, 0.10), shrunk + np.quantile(dev, 0.90)
    fwd.update(point=float(shrunk), pi80=[float(q10), float(q90)], p_positive=float(((shrunk + dev) > 0).mean()))
    close_2026 = prices.iloc[-1]
    fwd["last_close"] = float(close_2026); fwd["last_date"] = str(prices.index[-1].date())
    fwd["grid"] = {"r26": grid.tolist(), "p_welch": wp.tolist()}
    out["forward_2026"] = fwd

    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump(out, f, indent=2, default=float)
    printable = {k_: v for k_, v in out.items() if k_ != "forward_2026"}
    print(json.dumps(printable, indent=1, default=float))
    print(json.dumps({k_: v for k_, v in fwd.items() if k_ != "grid"}, indent=1, default=float))
    print(hz.round(4).to_string())


if __name__ == "__main__":
    main()
