# -*- coding: utf-8 -*-
"""Reported-only extras (no verdicts): single-name GSADF for NVDA and AMD, and the rhyme paths
built from the full histories (so the post-peak paths are complete)."""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_bubbles as rb  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, "results")
panel = pd.read_csv(os.path.join(D, "us_monthly_adjclose_panel.csv"), index_col=0, parse_dates=True)
X = {}
for t in ("NVDA", "AMD"):
    r, seq = rb.run_series(t, panel[t].loc["2011-06":].dropna(), 1, 0.95)
    X[t] = {k: r[k] for k in ("gsadf", "gsadf_cv", "gsadf_p", "last_bsadf", "last_cv", "last_explosive", "episodes")}
    seq.to_csv(os.path.join(OUT, f"bsadf_{t}.csv"))

ixic = pd.read_csv(os.path.join(D, "ixic.csv"), index_col=0, parse_dates=True)["Adj Close"].sort_index().resample("ME").last().dropna()
spx = rb.monthly(os.path.join(D, "GSPC_daily_close.csv")); nik = rb.monthly(os.path.join(D, "N225_daily_close.csv"))
basket = pd.read_csv(os.path.join(OUT, "ai_basket_index.csv"), index_col=0, parse_dates=True).iloc[:, 0]
paths = {}
for name, s, peak in (("S&P 500, peak Sep 1929", spx, "1929-09"), ("Nikkei 225, peak Dec 1989", nik, "1989-12"), ("Nasdaq Composite, peak Mar 2000", ixic, "2000-03")):
    i = s.index.get_loc(s.loc[peak].index[0])
    lo = max(0, i - 60); seg = s.iloc[lo: i + 37]
    paths[name] = pd.Series(seg.values / s.iloc[i] * 100, index=np.arange(lo - i, lo - i + len(seg)))
paths["AI-leaders basket, today"] = pd.Series(basket.iloc[-61:].values / basket.iloc[-1] * 100, index=np.arange(-60, 1))
P = pd.DataFrame(paths); P.to_csv(os.path.join(OUT, "rhyme_paths.csv"))
X["rhyme"] = {k: dict(first=int(s.dropna().index[0]), runup_to_peak=float(100 / s.dropna().iloc[0] - 1),
                      after_12m=float(s.get(12, np.nan) / 100 - 1), after_36m=float(s.get(36, np.nan) / 100 - 1), trough_36m=float(s.loc[0:36].min() / 100 - 1) if 36 in s.index else None)
              for k, s in paths.items()}
json.dump(X, open(os.path.join(OUT, "reported_extra.json"), "w"), indent=2, default=float)
print(json.dumps(X, indent=1, default=float))
