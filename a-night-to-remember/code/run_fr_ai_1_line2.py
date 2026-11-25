# -*- coding: utf-8 -*-
"""FR-AI-1 line 2 (signed 21 Nov 2026 12:11; dated note 2): analog forecast of the S&P 500. Run ONCE.
    python code/run_fr_ai_1_line2.py
"""
import json, sys, time
from pathlib import Path
import numpy as np, pandas as pd
ART = Path(__file__).resolve().parent.parent; OUT = ART / "results" / "fr_ai_1_line2.json"
if OUT.exists() and "--again" not in sys.argv: sys.exit("STOP: line 2 has been run. The forecast is in results/fr_ai_1_line2.json.")
W, GAP, K, H = 60, 120, 10, {"3 months": 63, "6 months": 126, "12 months": 252}
g = pd.read_csv(ART / "data" / "GSPC_daily_eodhd.csv", parse_dates=["date"]); g = g[(g.date >= "1950-01-03") & (g.date <= "2026-11-20")].reset_index(drop=True)
c = g.close.values; n = len(c); assert str(g.date.iloc[-1].date()) == "2026-11-20"
z = lambda x: (x - x.mean()) / x.std()
pat = z(c[-W:]); last_ok = int((g.date < "2025-11-20").values.nonzero()[0][-1])
ends = np.arange(W - 1, last_ok + 1); dist = np.array([np.sqrt(((z(c[e - W + 1:e + 1]) - pat) ** 2).sum()) for e in ends])
picked = []
for i in np.argsort(dist):
    e = int(ends[i])
    if all(abs(e - p) >= GAP for p in picked): picked.append(e)
    if len(picked) == K: break
rows = [dict(rank=r + 1, window_end=str(g.date[e].date()), distance=round(float(dist[e - (W - 1)]), 3), **{k: round(float(c[e + h] / c[e] - 1), 4) for k, h in H.items()}) for r, e in enumerate(picked)]
A = pd.DataFrame(rows); lastb = int((g.date <= "2025-12-31").values.nonzero()[0][-1])
res = dict(run=time.strftime("%Y-%m-%d %H:%M"), start_close=float(c[-1]), start_date="2026-11-20", pattern_first_day=str(g.date.iloc[-W].date()), candidates=int(len(ends)), analogs=rows, forecast={}, baseline={})
for k, h in H.items():
    b = c[h:lastb + 1] / c[:lastb + 1 - h] - 1
    res["forecast"][k] = dict(median=round(float(A[k].median()), 4), low=round(float(A[k].min()), 4), high=round(float(A[k].max()), 4), share_up=round(float((A[k] > 0).mean()), 2))
    res["baseline"][k] = dict(median=round(float(np.median(b)), 4), share_up=round(float((b > 0).mean()), 3), n=int(len(b)))
OUT.write_text(json.dumps(res, indent=1)); A.to_csv(ART / "results" / "fr_ai_1_line2_analogs.csv", index=False)
print(A.to_string(index=False)); print(json.dumps(res["forecast"], indent=1)); print(json.dumps(res["baseline"], indent=1))
