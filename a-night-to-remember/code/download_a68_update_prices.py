# -*- coding: utf-8 -*-
"""A68 A Night to Remember: prices AFTER the signature of FR-AI-1, for the dated update box only (24 Nov 2026).

The article body and every registered number stay on the close of 20 Nov 2026 (a68_start_prices.csv and
data/GSPC_daily_eodhd.csv are NOT touched). This file only feeds code/update_after_signing.py.

Downloads from EODHD (10 calls, about 15 seconds), 1 Sep 2026 to the latest close:
  S&P 500 index, SPY and the eight AI-leaders -> Factsheets/_data_private/a68/a68_update_prices.csv

Run in PowerShell from this folder. Key from EODHD_API_KEY or asked for:
    python download_a68_update_prices.py
"""
import sys, time
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent; ART = HERE.parent; P10 = ART.parents[1]
sys.path.insert(0, str(P10 / "DataCockpit"))
import download_eodhd_eu_fundamentals as DF  # noqa: E402

BASKET = ["NVDA", "AVGO", "AMD", "MSFT", "META", "GOOGL", "AMZN", "ORCL"]
PRIV = P10 / "Factsheets" / "_data_private" / "a68"; PRIV.mkdir(parents=True, exist_ok=True)
T0 = time.time()
def clock(m): print(f"{time.strftime('%H:%M:%S')} {m}", flush=True)

names = ["GSPC.INDX", "SPY.US"] + [b + ".US" for b in BASKET]; rows = []
clock(f"start: {len(names)} series from EODHD")
for i, s in enumerate(names, 1):
    js = DF.get(f"eod/{s}", **{"from": "2026-09-01"}); time.sleep(0.05)
    if not isinstance(js, list) or not js: sys.exit(f"STOP: no data for {s}: {js}")
    d = pd.DataFrame(js)
    if "adjusted_close" not in d: d["adjusted_close"] = d["close"]
    d = d[["date", "close", "adjusted_close"]]; d.insert(0, "ticker", s.split(".")[0]); rows.append(d)
    eta = (time.time() - T0) / i * (len(names) - i)
    clock(f"  {i} of {len(names)}  {s}: last day {d.date.iloc[-1]}, close {d.close.iloc[-1]}  (about {eta:.0f}s left)")
P = pd.concat(rows); P.to_csv(PRIV / "a68_update_prices.csv", index=False)
last = P.groupby("ticker").date.max()
if last.nunique() != 1: clock(f"NOTE: the series do not all end on the same day ({dict(last)}); the update uses the last day they share.")
clock(f"Done in {time.time() - T0:.0f}s. Last shared day: {last.min()}. Next: python update_after_signing.py")
