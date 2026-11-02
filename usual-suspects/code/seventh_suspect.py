# -*- coding: utf-8 -*-
"""Reported only: add AQR's US Quality-minus-Junk as a seventh factor (1963-07 to 2025-12).
Note the partial circularity: the Buffett recipe uses JKP's own QMJ legs."""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_suspects as rs  # noqa: E402

D, OUT = rs.D, rs.OUT
fus = pd.read_csv(os.path.join(D, "jkp_usa_factors_monthly.csv"), index_col=0, parse_dates=True)
fus.index = pd.to_datetime(fus.index).to_period("M").to_timestamp("M")
fac = rs.french_monthly("french_us_5f_daily.csv", "french_us_mom_daily.csv")
q = pd.read_csv(os.path.join(D, "aqr_qmj_qmj_factors.csv"), index_col=0, parse_dates=True)["USA"].rename("QMJ")
q.index = q.index.to_period("M").to_timestamp("M")
fac = fac.join(q, how="inner")
rs.FAC = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "Mom", "QMJ"]
res = rs.run(fac, fus, end="2025-12-31"); res.index.name = "recipe"
res.to_csv(os.path.join(OUT, "suspects_us_with_qmj.csv"))
S = dict(n_sig=int((res.alpha_t.astype(float).abs() > rs.GATE_T).sum()), sig=list(res.index[res.alpha_t.astype(float).abs() > rs.GATE_T]),
         median_abs_alpha=float(res.alpha_ann.astype(float).abs().median()), median_r2=float(res.r2.astype(float).median()))
json.dump(S, open(os.path.join(OUT, "seventh_suspect.json"), "w"), indent=2)
print(res[["alpha_ann", "alpha_t", "r2", "b_QMJ", "t_QMJ"]].astype(float).round(3).to_string()); print(S)
