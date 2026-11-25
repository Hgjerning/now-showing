# -*- coding: utf-8 -*-
"""A68 A Night to Remember: what happened after FR-AI-1 was signed, for the dated update box (24 Nov 2026).

Reads Factsheets/_data_private/a68/a68_update_prices.csv (download_a68_update_prices.py) and writes derived
statistics only to results/update_after_signing.json. Nothing registered is recomputed or changed: the script first
checks that the new download reproduces the article's 20 November figures, and stops if it does not.
    python update_after_signing.py              # to the last close all series share
    python update_after_signing.py 2026-11-23   # to a given close
"""
import json, os, sys, time
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent; ART = HERE.parent; P10 = ART.parents[1]; RES = ART / "results"
SRC = Path(os.environ.get("A68_UPDATE_PRICES", P10 / "Factsheets" / "_data_private" / "a68" / "a68_update_prices.csv"))
OUT = Path(os.environ.get("A68_UPDATE_JSON", RES / "update_after_signing.json"))
BK = ["NVDA", "AVGO", "AMD", "MSFT", "META", "GOOGL", "AMZN", "ORCL"]; T, S, M = "2026-10-06", "2026-11-20", "2026-11-23"
def clock(m): print(f"{time.strftime('%H:%M:%S')} {m}", flush=True)

p = pd.read_csv(SRC); J = json.load(open(RES / "base_rates_and_line1.json")); XC = json.load(open(RES / "extra_checks.json")); L2 = json.load(open(RES / "fr_ai_1_line2.json"))
D = sys.argv[1] if len(sys.argv) > 1 else p.groupby("ticker").date.max().min()
p = p[p.date <= D]
if D <= S: sys.exit(f"STOP: the price file ends on {D}; nothing after the signature to report.")
if M not in set(p.date): sys.exit(f"STOP: no prices for Monday {M} in the file.")
w = p.pivot(index="date", columns="ticker", values="adjusted_close"); gs = p[p.ticker == "GSPC"].set_index("date").close
miss = [t for t in BK + ["SPY", "GSPC"] if t not in w or pd.isna(w.loc[D, t])]
if miss: sys.exit(f"STOP: no price on {D} for {miss}")

# 1. the new download must reproduce what the article says about 20 November
L1 = J["line1"]["since_titanic_published_2026_10_06"]; C = J["corrections"]["current"]; r20 = w.loc[S] / w.loc[T] - 1
chk = {"basket": (float(r20[BK].mean()), L1["basket"]), "SPY": (float(r20["SPY"]), L1["spy"]), "NVDA": (float(r20["NVDA"]), L1["names"]["NVDA"]),
       "index close 20 Nov": (float(gs[S]) / C["close_20_nov"] - 1, 0.0), "index close 6 Oct": (float(gs[T]) / C["peak_close"] - 1, 0.0)}
bad = {k: v for k, v in chk.items() if abs(v[0] - v[1]) > 0.0015}
for k, (a, b) in chk.items(): clock(f"  check {k}: new download {a:+.4f}, article {b:+.4f}  {'OK' if k not in bad else 'DIFFERS'}")
if bad: sys.exit("STOP: the new download does not reproduce the article's 20 November figures (a dividend adjustment?). Paste this to Claude.")

# 2. since Titanic (6 Oct) and since the signature (close of 20 Nov), to D
rT = w.loc[D] / w.loc[T] - 1; rS = w.loc[D] / w.loc[S] - 1; rM = w.loc[M] / w.loc[S] - 1
days = [d for d in gs.index if d > S]
hist = pd.read_csv(ART / "data" / "GSPC_daily_eodhd.csv").set_index("date").close      # registered file, ends 20 Nov 2026
full = pd.concat([hist[hist.index <= S], gs[gs.index > S]]); ret = full.pct_change()
big = ret[(ret.index < M) & (ret >= ret[M])]
f3 = L2["forecast"]["3 months"]["median"]; b3 = L2["baseline"]["3 months"]["median"]
U = dict(as_of=D, trading_days_since_signature=len(days),
         index=dict(close=round(float(gs[D]), 2), below_peak=round(float(gs[D]) / C["peak_close"] - 1, 6), since_20_nov=round(float(gs[D]) / C["close_20_nov"] - 1, 6),
                    monday_return=round(float(ret[M]), 6), monday_best_day_since=big.index.max(), monday_close=round(float(gs[M]), 2),
                    highest_close_since_6_oct=round(float(gs[gs.index > T].max()), 2), no_higher_close_since_6_oct=bool(gs[gs.index > T].max() < C["peak_close"]),
                    since_3_nov=round(float(gs[D] / gs["2026-11-03"] - 1), 6)),
         since_titanic=dict(basket=round(float(rT[BK].mean()), 6), spy=round(float(rT["SPY"]), 6), names={k: round(float(rT[k]), 6) for k in BK}),
         since_signature=dict(basket_equal_weight=round(float(rS[BK].mean()), 6), spy=round(float(rS["SPY"]), 6), names={k: round(float(rS[k]), 6) for k in BK}),
         monday=dict(names={k: round(float(rM[k]), 6) for k in BK}, spy=round(float(rM["SPY"]), 6)),
         line2_3m=dict(analog_median=f3, baseline_median=b3, analogs_score_above=round((f3 + b3) / 2, 6)),
         low_on_first_day_cases=XC["after_corrections"]["low_on_first_day"], checks_vs_article={k: round(v[0], 6) for k, v in chk.items()},
         note="Derived statistics only. Written after the signature of FR-AI-1; nothing here is scored.")
json.dump(U, open(OUT, "w"), indent=1)
clock(f"as of {D} ({len(days)} trading day(s) after the signature): S&P 500 {U['index']['close']:,.2f}, {U['index']['below_peak']*100:+.1f}% from the 6 Oct high, {U['index']['since_20_nov']*100:+.1f}% since 20 Nov")
clock(f"basket since 6 Oct {U['since_titanic']['basket']*100:+.1f}% (was {L1['basket']*100:+.1f}%), NVDA {U['since_titanic']['names']['NVDA']*100:+.1f}% (was {L1['names']['NVDA']*100:+.1f}%), NVDA on Monday {U['monday']['names']['NVDA']*100:+.1f}%")
clock(f"written {OUT.name}. Next: python build_article.py")
