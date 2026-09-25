# -*- coding: utf-8 -*-
"""Case 1: every bubble rhymes. Runs PREREGISTRATION_C1_2026-09-25.md and writes ../results/.

GSADF/BSADF (Phillips, Shi & Yu 2015) are implemented from scratch with cumulative sums, so
every (start, end) ADF regression costs O(1) and the Monte Carlo critical values are exact for
each sample length. Nothing is downloaded.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, "results")
os.makedirs(OUT, exist_ok=True)
SEED, NSIM = 42, 2000
Q_TRIAL, Q_LEG = 1 - 0.05 / 3, 0.95
BASKET = ["NVDA", "AVGO", "AMD", "MSFT", "META", "GOOGL", "AMZN", "ORCL"]


# ------------------------------------------------------------------ GSADF engine
def _cums(y, lag):
    dy = np.diff(y)
    z = dy[lag:]
    cols = [np.ones(len(z)), y[lag:-1]] + [dy[lag - k:len(dy) - k] for k in range(1, lag + 1)]
    X = np.column_stack(cols)
    P = X[:, :, None] * X[:, None, :]
    Sxx = np.concatenate([np.zeros((1,) + P.shape[1:]), np.cumsum(P, 0)])
    Sxz = np.concatenate([np.zeros((1, X.shape[1])), np.cumsum(X * z[:, None], 0)])
    Szz = np.concatenate([[0.0], np.cumsum(z * z)])
    return Sxx, Sxz, Szz, len(z)


def bsadf(y, lag=1, r0=None):
    """BSADF sequence (NaN before the minimum window) and GSADF for a level series y."""
    T = len(y)
    r0 = r0 if r0 is not None else 0.01 + 1.8 / np.sqrt(T)
    w0 = int(np.floor(r0 * T))
    Sxx, Sxz, Szz, N = _cums(np.asarray(y, float), lag)
    k = Sxx.shape[1]
    s_idx, e_idx = np.triu_indices(N)
    keep = (e_idx - s_idx + 1) >= max(w0, k + 2)
    s_idx, e_idx = s_idx[keep], e_idx[keep]
    A = Sxx[e_idx + 1] - Sxx[s_idx]; b = Sxz[e_idx + 1] - Sxz[s_idx]; zz = Szz[e_idx + 1] - Szz[s_idx]
    n = e_idx - s_idx + 1
    Ainv = np.linalg.inv(A)
    beta = np.einsum("nij,nj->ni", Ainv, b)
    ssr = zz - np.einsum("ni,ni->n", beta, b)
    s2 = np.maximum(ssr, 1e-300) / (n - k)
    adf = beta[:, 1] / np.sqrt(s2 * Ainv[:, 1, 1])
    out = np.full(N, -np.inf)
    np.maximum.at(out, e_idx, adf)
    out[np.isinf(out)] = np.nan
    return out, np.nanmax(out), N


def mc_critical(T, lag=1, nsim=NSIM, seed=SEED):
    rng = np.random.default_rng(seed + T * 7 + lag)
    gs, bs = [], []
    for _ in range(nsim):
        e = rng.standard_normal(T)
        y = np.cumsum(1.0 / T + e)
        b, g, _ = bsadf(y, lag)
        gs.append(g); bs.append(b)
    return np.array(gs), np.vstack(bs)


def episodes(dates, stat, cv, min_len=3):
    above = (stat > cv) & ~np.isnan(stat)
    eps, start = [], None
    for i, a in enumerate(above):
        if a and start is None:
            start = i
        if (not a or i == len(above) - 1) and start is not None:
            end = i if a else i - 1
            if end - start + 1 >= min_len:
                eps.append((str(dates[start].date())[:7], str(dates[end].date())[:7]))
            start = None
    return eps


def run_series(name, s, lag=1, q=Q_LEG):
    y = np.log(s.values)
    b, g, N = bsadf(y, lag)
    G, B = mc_critical(len(y), lag)
    cvg = float(np.quantile(G, q)); cvb = np.nanquantile(B, q, axis=0)
    dates = s.index[len(s) - N:]
    res = dict(name=name, T=len(y), start=str(s.index[0].date())[:7], end=str(s.index[-1].date())[:7], lag=lag, q=q,
               gsadf=float(g), gsadf_cv=cvg, gsadf_p=float((G >= g).mean()), last_bsadf=float(b[-1]), last_cv=float(cvb[-1]),
               last_explosive=bool(b[-1] > cvb[-1]), episodes=episodes(dates, b, cvb))
    seq = pd.DataFrame({"bsadf": b, "cv": cvb}, index=dates)
    return res, seq


def monthly(path, col="close", start=None, end=None):
    d = pd.read_csv(path, index_col=0, parse_dates=True)
    s = d[col] if col in d else d.iloc[:, 0]
    s = s.sort_index().resample("ME").last().dropna()
    return s.loc[start:end]


def main():
    S = {}
    # ---------------- legibility
    ixic = pd.read_csv(os.path.join(D, "ixic.csv"), index_col=0, parse_dates=True)["Adj Close"].sort_index().resample("ME").last().dropna()
    leg = {"S&P 500 1927-1934": (monthly(os.path.join(D, "GSPC_daily_close.csv"), start="1927-12", end="1934-12"), "1929-09"),
           "Nikkei 225 1970-1992": (monthly(os.path.join(D, "N225_daily_close.csv"), start="1970-01", end="1992-12"), "1989-12"),
           "Nasdaq Composite 1985-2002": (ixic.loc["1985-01":"2002-12"], "2000-03")}
    S["legibility"] = []
    seqs = {}
    for k, (s, peak) in leg.items():
        r, seq = run_series(k, s, 1, Q_LEG)
        chk = (pd.Period(peak, "M") - 3).strftime("%Y-%m")
        r["peak"] = peak; r["check_month"] = chk
        r["covers_check"] = any(a <= chk <= b for a, b in r["episodes"])
        r["passes"] = bool(r["gsadf"] > r["gsadf_cv"] and r["covers_check"])
        S["legibility"].append(r); seqs[k] = seq
    # ---------------- trials C1-1, C1-2
    panel = pd.read_csv(os.path.join(D, "us_monthly_adjclose_panel.csv"), index_col=0, parse_dates=True)
    qqq = panel["QQQ"].loc["2005-01":].dropna()
    rets = panel[BASKET].loc["2011-06":].pct_change().iloc[1:]
    basket = (1 + rets.mean(axis=1)).cumprod() * 100
    basket.to_csv(os.path.join(OUT, "ai_basket_index.csv"), header=["index"])
    S["trials"] = {}
    for tid, name, s in (("C1-1", "Nasdaq-100 (QQQ)", qqq), ("C1-2", "AI-leaders basket", basket)):
        r, seq = run_series(name, s, 1, Q_TRIAL)
        r["passed"] = bool(r["gsadf"] > r["gsadf_cv"] and r["last_explosive"])
        S["trials"][tid] = r; seqs[name] = seq
        r0, _ = run_series(name, s, 0, Q_TRIAL); S["trials"][tid]["lag0"] = {k: r0[k] for k in ("gsadf", "gsadf_cv", "last_bsadf", "last_cv", "last_explosive", "episodes")}
        r95, _ = run_series(name, s, 1, 0.95); S["trials"][tid]["at95"] = {k: r95[k] for k in ("gsadf_cv", "last_cv", "last_explosive", "episodes")}
    # the S&P 500 now, reported
    spx = monthly(os.path.join(D, "GSPC_daily_close.csv"), start="2005-01")
    r, seq = run_series("S&P 500 2005-2026", spx, 1, Q_LEG); S["sp500_now"] = r; seqs["S&P 500 2005-2026"] = seq
    for k, v in seqs.items():
        v.to_csv(os.path.join(OUT, "bsadf_" + "".join(c if c.isalnum() else "_" for c in k) + ".csv"))

    # ---------------- C1-3: Greenwood-Shleifer-You on the survivor panel
    P = panel.loc["2011-06":]
    lp = P.values
    rows = []
    for j, t in enumerate(P.columns):
        x = lp[:, j]
        ok = np.where(~np.isnan(x))[0]
        if len(ok) < 49:
            continue
        i0, i1 = ok[0], ok[-1]
        i = i0 + 24
        next_event = -1
        while i + 24 <= i1:
            past = x[i] / x[i - 24] - 1
            if np.isnan(past):
                i += 1; continue
            fut = x[i:i + 25]
            if np.isnan(fut).any():
                i += 1; continue
            path = fut / np.maximum.accumulate(fut)
            crash = bool(path.min() <= 0.60)
            r12, r24 = fut[12] / fut[0] - 1, fut[24] / fut[0] - 1
            r12past = x[i] / x[i - 12] - 1
            vol = np.nanstd(np.diff(np.log(x[i - 24:i + 1])), ddof=1) * np.sqrt(12)
            rows.append(dict(ticker=t, date=P.index[i], past24=past, past12=r12past, crash=crash, fwd12=r12, fwd24=r24, vol=vol))
            i += 1
    ev = pd.DataFrame(rows)
    ev["year"] = ev.date.dt.year

    def non_overlap(df, cond):
        out = []
        for t, g in df.groupby("ticker"):
            last = None
            for r in g[cond(g)].itertuples():
                if last is None or (r.date.to_period("M") - last.to_period("M")).n >= 24:
                    out.append(r._asdict()); last = r.date
        return pd.DataFrame(out)
    events100 = non_overlap(ev, lambda g: g.past24 >= 1.0)
    events150 = non_overlap(ev, lambda g: g.past24 >= 1.5)
    ctrl = non_overlap(ev, lambda g: g.past24 > -np.inf)
    def prop_test(a, b):
        p1, p2, n1, n2 = a.crash.mean(), b.crash.mean(), len(a), len(b)
        p = (a.crash.sum() + b.crash.sum()) / (n1 + n2)
        z = (p1 - p2) / np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
        return dict(p_event=float(p1), p_ctrl=float(p2), n_event=n1, n_ctrl=n2, z=float(z), p_one_sided=float(stats.norm.sf(z)))
    main_t = prop_test(events100, ctrl)
    h1 = prop_test(events100[events100.year <= 2019], ctrl[ctrl.year <= 2019])
    h2 = prop_test(events100[events100.year >= 2020], ctrl[ctrl.year >= 2020])
    S["C1-3"] = dict(main_t, half_2013_2019=h1, half_2020_2024=h2,
                     passed=bool(main_t["p_one_sided"] < 0.05 / 3 and h1["p_event"] > h1["p_ctrl"] and h2["p_event"] > h2["p_ctrl"]))
    S["gsy_reported"] = {
        "at150": prop_test(events150, ctrl),
        "fwd12_event_mean": float(events100.fwd12.mean()), "fwd12_ctrl_mean": float(ctrl.fwd12.mean()),
        "fwd24_event_mean": float(events100.fwd24.mean()), "fwd24_ctrl_mean": float(ctrl.fwd24.mean()),
        "fwd24_event_median": float(events100.fwd24.median()), "fwd24_ctrl_median": float(ctrl.fwd24.median()),
        "fwd12_welch": [float(v) for v in stats.ttest_ind(events100.fwd12, ctrl.fwd12, equal_var=False)],
        "fwd24_welch": [float(v) for v in stats.ttest_ind(events100.fwd24, ctrl.fwd24, equal_var=False)],
    }
    # acceleration and volatility splits (GSY's characteristics)
    e = events100.copy()
    e["accel"] = (1 + e.past12) / (1 + e.past24)  # share of the run-up earned in the last 12 months (price ratio)
    hi_acc = e.accel >= e.accel.median(); hi_vol = e.vol >= e.vol.median()
    S["gsy_splits"] = {"accel_high": float(e[hi_acc].crash.mean()), "accel_low": float(e[~hi_acc].crash.mean()),
                       "vol_high": float(e[hi_vol].crash.mean()), "vol_low": float(e[~hi_vol].crash.mean()), "n": len(e)}
    by_run = []
    for lo, hi in ((-np.inf, 0), (0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, np.inf)):
        g = ctrl[(ctrl.past24 >= lo) & (ctrl.past24 < hi)]
        by_run.append(dict(bucket=f"{lo if np.isfinite(lo) else '<'}..{hi if np.isfinite(hi) else '+'}", n=len(g), crash=float(g.crash.mean()) if len(g) else np.nan,
                           fwd24=float(g.fwd24.mean()) if len(g) else np.nan))
    pd.DataFrame(by_run).to_csv(os.path.join(OUT, "gsy_by_runup_bucket.csv"), index=False)
    events100.to_csv(os.path.join(OUT, "gsy_events100.csv"), index=False)

    # ---------------- the AI names today
    last = panel.index[-1]
    rows = []
    for t in BASKET + ["QQQ", "SPY"]:
        s = panel[t].dropna()
        rows.append(dict(name=t, run24=float(s.iloc[-1] / s.iloc[-25] - 1), run12=float(s.iloc[-1] / s.iloc[-13] - 1),
                         from_peak=float(s.iloc[-1] / s.max() - 1), peak_month=str(s.idxmax().date())[:7]))
    b = basket
    rows.append(dict(name="AI basket", run24=float(b.iloc[-1] / b.iloc[-25] - 1), run12=float(b.iloc[-1] / b.iloc[-13] - 1),
                     from_peak=float(b.iloc[-1] / b.max() - 1), peak_month=str(b.idxmax().date())[:7]))
    ai = pd.DataFrame(rows); ai.to_csv(os.path.join(OUT, "ai_names_today.csv"), index=False)
    S["ai_today"] = ai.to_dict(orient="records"); S["as_of"] = str(last.date())[:7]
    # share of the panel's 100%-runup events that are 'now' (last month)
    now = ev[ev.date == ev.date.max()]
    S["panel_last_full_month"] = str(ev.date.max().date())[:7]

    # ---------------- rhyme paths: aligned at peak
    paths = {}
    for k, (s, peak) in leg.items():
        full = s
        p = pd.Timestamp(peak) + pd.offsets.MonthEnd(0)
        i = full.index.get_indexer([p], method="nearest")[0]
        seg = full.iloc[max(0, i - 60): i + 37]
        paths[k.split(" 19")[0].split(" 1985")[0]] = pd.Series(seg.values / full.iloc[i] * 100, index=np.arange(max(0, i - 60) - i, max(0, i - 60) - i + len(seg)))
    i = len(basket) - 1
    paths["AI-leaders basket (today = 0)"] = pd.Series(basket.iloc[i - 60:].values / basket.iloc[-1] * 100, index=np.arange(-60, 1))
    pd.DataFrame(paths).to_csv(os.path.join(OUT, "rhyme_paths.csv"))
    for k, s in paths.items():
        pass
    S["rhyme_runup_60m"] = {k: float(100 / s.loc[-60] - 1) if -60 in s.index else None for k, s in paths.items()}
    S["rhyme_after_36m"] = {k: float(s.loc[36] / 100 - 1) if 36 in s.index else None for k, s in paths.items()}
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=2, default=float)
    print(json.dumps({k: v for k, v in S.items() if k not in ("ai_today",)}, indent=1, default=float))
    print(ai.round(3).to_string())


if __name__ == "__main__":
    main()
