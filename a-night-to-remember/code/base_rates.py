# -*- coding: utf-8 -*-
"""A68: what followed earlier 10% corrections in the S&P 500 (descriptive; not a trial, nothing gated), and the
starting values of FR-AI-1 line 1. Reads data/GSPC_daily_eodhd.csv and the private start prices.
    python code/base_rates.py
"""
import json
from pathlib import Path
import numpy as np, pandas as pd
ART = Path(__file__).resolve().parent.parent; P10 = ART.parents[1]
g = pd.read_csv(ART / "data" / "GSPC_daily_eodhd.csv", parse_dates=["date"]); g = g[(g.date >= "1950-01-03") & (g.date <= "2026-11-20")].reset_index(drop=True)
c = g.close.values; d = g.date
ep = []; peak = c[0]; ipk = 0; inside = None
for i in range(1, len(c)):
    if inside is None:
        if c[i] > peak: peak, ipk = c[i], i
        elif c[i] <= 0.9 * peak: inside = dict(peak_day=ipk, first10=i, low=c[i], ilow=i)
    else:
        if c[i] < inside["low"]: inside["low"], inside["ilow"] = c[i], i
        if c[i] > peak:
            inside["recovered"] = i; ep.append(inside); inside = None; peak, ipk = c[i], i
if inside: inside["recovered"] = None; ep.append(inside)
rows = []
for e in ep:
    i = e["first10"]; f = lambda h: float(c[i + h] / c[i] - 1) if i + h < len(c) else None
    rows.append(dict(peak=str(d[e["peak_day"]].date()), first_10pct_day=str(d[i].date()), days_peak_to_10pct=int(i - e["peak_day"]), depth=round(float(e["low"] / c[e["peak_day"]] - 1), 6),
                     became_bear=bool(e["low"] <= 0.8 * c[e["peak_day"]]), further_fall_after_10pct_day=round(float(e["low"] / c[i] - 1), 6),
                     r3=f(63), r6=f(126), r12=f(252), days_to_new_high=None if e["recovered"] is None else int(e["recovered"] - e["peak_day"])))
E = pd.DataFrame(rows); E.to_csv(ART / "results" / "corrections_since_1950.csv", index=False)
past = E.iloc[:-1] if E.days_to_new_high.isna().iloc[-1] else E; cur = E.iloc[-1]
q = lambda s, p: round(float(np.nanpercentile(s.dropna(), p)), 6)
B = dict(n_past=int(len(past)), became_bear=int(past.became_bear.sum()), share_bear=round(float(past.became_bear.mean()), 3),
         current=dict(peak=cur.peak, peak_close=float(c[ep[-1]["peak_day"]]), first_10pct_day=cur.first_10pct_day, close_20_nov=float(c[-1]), fall_from_peak=round(float(c[-1] / c[ep[-1]["peak_day"]] - 1), 6), days_peak_to_10pct=int(cur.days_peak_to_10pct)),
         median_days_peak_to_10pct=float(past.days_peak_to_10pct.median()), faster_than_current=int((past.days_peak_to_10pct <= cur.days_peak_to_10pct).sum()),
         median_further_fall=q(past.further_fall_after_10pct_day, 50), median_depth=q(past.depth, 50), median_days_to_new_high=float(past.days_to_new_high.median()))
for k, lab in (("r3", "3 months"), ("r6", "6 months"), ("r12", "12 months")):
    s = past[k]; B[lab] = dict(median=q(s, 50), p10=q(s, 10), p90=q(s, 90), share_up=round(float((s.dropna() > 0).mean()), 3), n=int(s.notna().sum()))
    nb = past[~past.became_bear][k]; bb = past[past.became_bear][k]; B[lab].update(median_if_no_bear=q(nb, 50), median_if_bear=q(bb, 50))
p = pd.read_csv(P10 / "Factsheets" / "_data_private" / "a68" / "a68_start_prices.csv"); w = p.pivot(index="date", columns="ticker", values="adjusted_close")
bk = ["NVDA", "AVGO", "AMD", "MSFT", "META", "GOOGL", "AMZN", "ORCL"]; r = w.loc["2026-11-20"] / w.loc["2026-10-06"] - 1
idx = (w / w.loc["2026-10-06"]); path = pd.DataFrame({"basket": idx[bk].mean(axis=1) * 100, "spy": idx["SPY"] * 100}).loc["2026-10-06":]   # equal weight, buy and hold over six weeks
path.round(4).to_csv(ART / "results" / "since_titanic.csv")
L1 = dict(start="2026-11-20", end="2027-11-19", since_titanic_published_2026_10_06=dict(basket=round(float(r[bk].mean()), 6), spy=round(float(r["SPY"]), 6), names={k: round(float(r[k]), 6) for k in bk},
          worst=min(bk, key=lambda k: r[k]), best=max(bk, key=lambda k: r[k])))
# the two favourites Titanic compared with: what followed the first close as far below the peak as the basket is now (descriptive; two cases)
A01 = ART.parent / "A01_Titanic_AI_Bubble" / "data"; FAV = []; depth = 1 + L1["since_titanic_published_2026_10_06"]["basket"]
for name, f, col, pk in (("Nasdaq Composite", "ixic.csv", "Adj Close", "2000-03-10"), ("Nikkei 225", "N225_daily_close.csv", None, "1989-12-29")):
    x = pd.read_csv(A01 / f, index_col=0, parse_dates=True); s = (x[col] if col else x.iloc[:, 0]).dropna().sort_index(); a = s[pd.Timestamp(pk):]; top = float(a.iloc[0])
    assert top == float(s[pd.Timestamp(pk) - pd.Timedelta(days=400):pd.Timestamp(pk)].max()), name
    i = int((a.values <= depth * top).nonzero()[0][0])
    FAV.append(dict(name=name, peak=pk, day=str(a.index[i].date()), trading_days_from_peak=i, below_peak=round(float(a.iloc[i] / top - 1), 6),
                    r3=round(float(a.iloc[i + 63] / a.iloc[i] - 1), 6), r6=round(float(a.iloc[i + 126] / a.iloc[i] - 1), 6), r12=round(float(a.iloc[i + 252] / a.iloc[i] - 1), 6),
                    low_3y=round(float(a.iloc[i:i + 756].min() / a.iloc[i] - 1), 6)))
json.dump(dict(corrections=B, line1=L1, favourites=FAV), open(ART / "results" / "base_rates_and_line1.json", "w"), indent=1); print(json.dumps(FAV, indent=1))
print(json.dumps(B, indent=1)); print(json.dumps(L1, indent=1)); print(E.tail(6).to_string(index=False))
