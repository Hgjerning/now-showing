# -*- coding: utf-8 -*-
"""A04, reported (not gated), added after the stress test of 22 Oct 2026. Reads the decile series of record
(results/ = published universe, results_pit/ = actual S&P 500 members) and Ken French's daily factors. Writes
results_pit/reported_stress.json. Adds no trials.
  sharpe:  excess-return Sharpe ratios (French RF) of the steadiest and lottery deciles; moving-block bootstrap
           (block 6 months, 5,000 draws, seed 20261022) of the difference D1 - D10 on each universe.
  meme:    April 2020 -> December 2021: raw low-minus-high spread and its CAPM alpha (it starts at the Covid low)."""
import json, os
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "data")
fr = pd.read_csv(os.path.join(D, "french_us_5f_daily.csv"), index_col=0, parse_dates=True)
FM = (1 + fr).resample("ME").prod(min_count=1) - 1
rng = np.random.default_rng(20261022)


def sr(x): return float(x.mean() / x.std(ddof=1) * np.sqrt(12))


def boot(a, b, B=5000, L=6):
    n = len(a); out = []
    for _ in range(B):
        st = rng.integers(0, n - L + 1, size=int(np.ceil(n / L))); ix = np.concatenate([np.arange(s, s + L) for s in st])[:n]
        out.append(sr(a[ix]) - sr(b[ix]))
    out = np.array(out); return float(np.quantile(out, .025)), float(np.quantile(out, .975)), float(np.mean(out <= 0))


res = {}
for key, sub in (("published", "results"), ("corrected", "results_pit")):
    P = pd.read_csv(os.path.join(ROOT, sub, "max_deciles_top500.csv"), index_col=0, parse_dates=True)
    x = P.join(FM[["RF", "Mkt-RF"]], how="inner")
    e1, e10 = (x.D1 - x.RF).values, (x.D10 - x.RF).values
    lo, hi, p = boot(e1, e10)
    m = x.loc["2020-04-30":"2021-12-31"]; y = (m.D1 - m.D10).values
    X = np.c_[np.ones(len(m)), m["Mkt-RF"].values]; b = np.linalg.lstsq(X, y, rcond=None)[0]
    res[key] = {"months": int(len(x)), "sharpe_excess_D1": sr(e1), "sharpe_excess_D10": sr(e10), "diff": sr(e1) - sr(e10),
                "diff_ci95": [lo, hi], "share_boot_diff_le_0": p,
                "meme": {"months": int(len(m)), "spread_ann": float(y.mean() * 12), "capm_alpha_ann": float(b[0] * 12), "capm_beta": float(b[1]),
                         "mkt_excess_cum": float((1 + m["Mkt-RF"]).prod() - 1)}}
json.dump(res, open(os.path.join(ROOT, "results_pit", "reported_stress.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
