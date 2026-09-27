# -*- coding: utf-8 -*-
"""FS05 Monkey (dartboard) portfolios.
Every January each of 10,000 monkeys picks k stocks at random from the eligible universe (k = 30; SCANDI 20; DK 10),
equal weight, held for the year (monthly returns of the chosen names; a name that stops trading earns 0 after its
last price). Compared with the size-weighted universe (the 'index': US market cap, elsewhere traded value as proxy)
and with the equal-weight universe. 10 bp per side on the annual rebalance.
"""
import json
import os

import numpy as np
import pandas as pd

import data
import perf
import xs

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
U = data.REGIONS
NM = 10000


def run(R, seed=42):
    I = xs.inputs(R); fwd, E = I["fwd"], I["E"]
    k = 30 if R not in ("DK", "SC") else (10 if R == "DK" else 20)
    rng = np.random.default_rng(seed + U.index(R))
    sw = xs.size_weighted(I)
    years = range(2013, 2027); M = []
    idx = []
    for y in years:
        t0 = pd.Period(f"{y - 1}-12")
        if t0 not in E.index:
            continue
        el = E.loc[t0][E.loc[t0]].index
        months = [pd.Period(f"{y}-{m:02d}") for m in range(1, 13) if pd.Period(f"{y}-{m:02d}") in fwd.index and pd.Period(f"{y}-{m:02d}") <= pd.Period("2026-08")]
        if not months:
            continue
        Rm = fwd.loc[months, el].fillna(0).values          # months x N
        pick = np.argsort(rng.random((NM, len(el))), axis=1)[:, :k]
        W = np.zeros((NM, len(el))); np.put_along_axis(W, pick, 1.0 / k, axis=1)
        # buy-and-hold within the year: weights drift with returns
        grow = np.cumprod(1 + Rm, axis=0)                  # months x N
        val = W @ grow.T                                    # NM x months (portfolio value)
        prev = np.hstack([np.ones((NM, 1)), val[:, :-1]])
        r = val / prev - 1
        r[:, 0] -= 0.002                                    # 10 bp in and 10 bp out per year, charged in January
        M.append(r); idx += [m.to_timestamp("M") for m in months]
    Mr = np.hstack(M)                                       # NM x T
    ew = pd.Series({t.to_timestamp("M"): v for t, v in I["ew"].items()}).reindex(idx)
    sw = sw.reindex(idx)
    keep = sw.notna().values & ew.notna().values           # Jan 2013 has no size-weighted benchmark (formation starts Jan 2013)
    Mr = Mr[:, keep]; idx = [t for t, k_ in zip(idx, keep) if k_]; ew = ew[keep]; sw = sw[keep]
    mean_monkey = pd.Series(Mr.mean(axis=0), index=idx)
    T = len(idx)
    cagr = (np.prod(1 + Mr, axis=1)) ** (12 / T) - 1
    sh = Mr.mean(axis=1) / Mr.std(axis=1, ddof=1) * np.sqrt(12)
    sw_c = float((1 + sw).prod() ** (12 / T) - 1); ew_c = float((1 + ew).prod() ** (12 / T) - 1)
    sw_s = perf.sharpe(sw.values); ew_s = perf.sharpe(ew.values)
    med = pd.Series(np.median(Mr, axis=0), index=idx)
    # yearly share of monkeys beating the index vs the EW-minus-SW spread that year
    yr = pd.Index([t.year for t in idx]); yearly = []
    for y in sorted(set(yr)):
        mm = yr == y
        mret = np.prod(1 + Mr[:, mm], axis=1) - 1; sret = float(np.prod(1 + sw.values[mm]) - 1); eret = float(np.prod(1 + ew.values[mm]) - 1)
        yearly.append(dict(year=int(y), share_beat=float((mret > sret).mean()), ew_minus_sw=eret - sret, median=float(np.median(mret)), index=sret))
    dd = [float(perf.drawdown(pd.Series(Mr[i])).min()) for i in range(0, NM, 50)]
    res = dict(k=k, months=T, start=str(idx[0].date()), end=str(idx[-1].date()), sw_cagr=sw_c, ew_cagr=ew_c, sw_sharpe=sw_s, ew_sharpe=ew_s,
               monkey_cagr_pct={p: float(np.percentile(cagr, p)) for p in (5, 25, 50, 75, 95)},
               monkey_sharpe_pct={p: float(np.percentile(sh, p)) for p in (5, 25, 50, 75, 95)},
               share_beat_cagr=float((cagr > sw_c).mean()), share_beat_sharpe=float((sh > sw_s).mean()),
               share_beat_ew_cagr=float((cagr > ew_c).mean()), mean_monkey_cagr=float((1 + mean_monkey).prod() ** (12 / len(idx)) - 1), maxdd_median=float(np.median(dd)), sw_maxdd=float(perf.drawdown(sw).min()),
               yearly=yearly, corr_share_spread=float(np.corrcoef([y["share_beat"] for y in yearly], [y["ew_minus_sw"] for y in yearly])[0, 1]))
    return res, dict(cagr=cagr, sharpe=sh, median=med, mean=mean_monkey, ew=ew, sw=sw)


if __name__ == "__main__":
    out, ser = {}, {}
    for R in U:
        out[R], ser[R] = run(R)
        o = out[R]; print(R, "k", o["k"], "median CAGR %.1f%% index %.1f%% EW %.1f%% | beat index %.0f%% (Sharpe %.0f%%)" % (o["monkey_cagr_pct"][50] * 100, o["sw_cagr"] * 100, o["ew_cagr"] * 100, o["share_beat_cagr"] * 100, o["share_beat_sharpe"] * 100))
    json.dump(out, open(os.path.join(RES, "monkey_summary.json"), "w"), indent=1, default=float)
    pd.to_pickle(ser, os.path.join(RES, "monkey_series.pkl"))
