# -*- coding: utf-8 -*-
"""A68: figures added after the independent stress test of 21 Nov 2026 (STRESS_TEST_2026-11-21.md). Descriptive; nothing here
is a trial or changes a registered line. The sensitivity of line 2 is computed AFTER the registered run and is not scored.
    python code/extra_checks.py
"""
import json
from pathlib import Path
import numpy as np, pandas as pd
ART = Path(__file__).resolve().parent.parent; RES = ART / "results"; A01 = ART.parent / "A01_Titanic_AI_Bubble" / "data"
G = pd.read_csv(ART / "data" / "GSPC_daily_eodhd.csv", parse_dates=["date"]); G = G[G.date <= "2026-11-20"].reset_index(drop=True)
g = G[G.date >= "1950-01-03"].reset_index(drop=True); c = g.close.values
J = json.load(open(RES / "base_rates_and_line1.json")); L2 = json.load(open(RES / "fr_ai_1_line2.json")); E = pd.read_csv(RES / "corrections_since_1950.csv")
past = E[E.days_to_new_high.notna()]; X = {}

# section 4: the mean beside the median; near-bears; the low on the first day; wait from the first 10% day
lastb = int((g.date <= "2025-12-31").values.nonzero()[0][-1]); allr = c[252:lastb + 1] / c[:lastb + 1 - 252] - 1
nb = past[~past.became_bear]
X["after_corrections"] = dict(mean_12m=float(past.r12.mean()), all_days_mean_12m=float(allr.mean()), all_days_share_up_12m=float((allr > 0).mean()),
    near_bears=int((nb.depth <= -0.18).sum()), near_bear_lo=float(-nb[nb.depth <= -0.18].depth.min()), near_bear_hi=float(-nb[nb.depth <= -0.18].depth.max()),
    low_on_first_day=int((past.further_fall_after_10pct_day == 0).sum()), median_days_first10_to_new_high=float((past.days_to_new_high - past.days_peak_to_10pct).median()))

# the same count with true record highs (the index did not pass its 1929 high until 1954)
def episodes(close):
    ep = []; peak = close[0]; ipk = 0; inside = None
    for i in range(1, len(close)):
        if inside is None:
            if close[i] > peak: peak, ipk = close[i], i
            elif close[i] <= 0.9 * peak: inside = dict(pk=ipk, first=i, low=close[i])
        else:
            inside["low"] = min(inside["low"], close[i])
            if close[i] > peak: inside["rec"] = i; ep.append(inside); inside = None; peak, ipk = close[i], i
    return ep
ca = G.close.values; i50 = int((G.date >= "1950-01-03").values.nonzero()[0][0])
rec = [e for e in episodes(ca) if e["first"] >= i50 and e["first"] + 252 < len(ca)]
X["record_highs"] = dict(n=len(rec), bears=int(sum(e["low"] <= 0.8 * ca[e["pk"]] for e in rec)), median_12m=float(np.median([ca[e["first"] + 252] / ca[e["first"]] - 1 for e in rec])))

# No. 2 Groundhog Day: where the index stands inside the registered range
d = g.set_index("date").close; X["groundhog"] = dict(close_3_nov=float(d["2026-11-03"]), since_3_nov=float(d["2026-11-20"] / d["2026-11-03"] - 1))

# three earlier favourites (all three Titanic compared with), at the basket's depth and at the index's own depth
bdepth = 1 + J["line1"]["since_titanic_published_2026_10_06"]["basket"]; idepth = 1 + J["corrections"]["current"]["fall_from_peak"]; FAV = []
def fav(name, s, pk):
    a = s[pd.Timestamp(pk):]; top = float(a.iloc[0]); row = dict(name=name, peak=pk)
    for lab, dep in (("basket_depth", bdepth), ("index_depth", idepth)):
        i = int((a.values <= dep * top).nonzero()[0][0])
        row[lab] = dict(day=str(a.index[i].date()), below_peak=float(a.iloc[i] / top - 1), r3=float(a.iloc[i + 63] / a.iloc[i] - 1), r6=float(a.iloc[i + 126] / a.iloc[i] - 1),
                        r12=float(a.iloc[i + 252] / a.iloc[i] - 1), low_3y=float(a.iloc[i:i + 756].min() / a.iloc[i] - 1))
    FAV.append(row)
sp = G.set_index("date").close; pk29 = str(sp["1929-01-01":"1929-12-31"].idxmax().date()); fav("S&P 500, 1929", sp, pk29)
x = pd.read_csv(A01 / "N225_daily_close.csv", index_col=0, parse_dates=True).iloc[:, 0].dropna().sort_index(); fav("Nikkei 225, 1989", x, "1989-12-29")
x = pd.read_csv(A01 / "ixic.csv", index_col=0, parse_dates=True)["Adj Close"].dropna().sort_index(); fav("Nasdaq Composite, 2000", x, "2000-03-10")
X["favourites"] = FAV

# line 2: how often the baseline side wins on history alone, and how much the forecast moves with one setting changed (NOT scored)
H = {"3 months": 63, "6 months": 126, "12 months": 252}; z = lambda v: (v - v.mean()) / v.std()
def analog(W=60, K=10, GAP=120, returns=False):
    series = np.diff(np.log(c)) if returns else c; off = 1 if returns else 0          # returns[i] ends on day i + 1
    pat = z(series[-W:]); last_ok = int((g.date < "2025-11-20").values.nonzero()[0][-1]); ends = np.arange(W - 1 + off, last_ok + 1)
    dist = np.array([np.sqrt(((z(series[e - off - W + 1:e - off + 1]) - pat) ** 2).sum()) for e in ends]); picked = []
    for i in np.argsort(dist, kind="stable"):
        e = int(ends[i])
        if all(abs(e - p) >= GAP for p in picked): picked.append(e)
        if len(picked) == K: break
    return {k: float(np.median([c[e + h] / c[e] - 1 for e in picked])) for k, h in H.items()}
base = analog(); assert all(abs(base[k] - L2["forecast"][k]["median"]) < 1.1e-4 for k in H), base
S = {"as registered (60 closes, ten nearest)": base, "three nearest": analog(K=3), "five nearest": analog(K=5), "40-day pattern": analog(W=40), "90-day pattern": analog(W=90), "daily returns in place of closes": analog(returns=True)}
X["line2_sensitivity"] = S; X["line2_3m_range"] = [min(v["3 months"] for v in S.values()), max(v["3 months"] for v in S.values())]
be = {k: (base[k] + L2["baseline"][k]["median"]) / 2 for k in H}
X["baseline_side_share"] = {k: float(((c[h:lastb + 1] / c[:lastb + 1 - h] - 1) < be[k]).mean()) for k, h in H.items()}
# robustness of the count in section 3 (added 21 Nov 2026 after the outside critique): other thresholds, and a start in 1928
def count(close, first_ok, thr):
    ep = []; peak = close[0]; ipk = 0; inside = None
    for i in range(1, len(close)):
        if inside is None:
            if close[i] > peak: peak, ipk = close[i], i
            elif close[i] <= (1 - thr) * peak: inside = dict(pk=ipk, first=i, low=close[i])
        else:
            inside["low"] = min(inside["low"], close[i])
            if close[i] > peak: ep.append(inside); inside = None; peak, ipk = close[i], i
    ep = [e for e in ep if e["first"] >= first_ok and e["first"] + 252 < len(close)]      # completed cases with a known next year
    r = np.array([close[e["first"] + 252] / close[e["first"]] - 1 for e in ep]); bear = np.array([e["low"] <= 0.8 * close[e["pk"]] for e in ep])
    return dict(n=len(ep), bears=int(bear.sum()), share_bear=float(bear.mean()), median_12m=float(np.median(r)), mean_12m=float(r.mean()), share_up=float((r > 0).mean()),
                median_further_fall=float(np.median([e["low"] / close[e["first"]] - 1 for e in ep])))
ROB = {f"{int(t * 100)}% since 1950": count(c, 0, t) for t in (0.08, 0.10, 0.12, 0.15)}
ROB["10% since 1928"] = count(ca, 1, 0.10)
assert ROB["10% since 1950"]["n"] == 26 and ROB["10% since 1950"]["bears"] == 11, ROB["10% since 1950"]
X["robustness"] = ROB; X["after_corrections"]["not_low_on_first_day"] = int(len(past) - X["after_corrections"]["low_on_first_day"])
json.dump(X, open(RES / "extra_checks.json", "w"), indent=1); print(json.dumps(X["robustness"], indent=1))
