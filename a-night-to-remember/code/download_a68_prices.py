# -*- coding: utf-8 -*-
"""A68 A Night to Remember, forward record FR-AI-1 (signed 21 Nov 2026 12:11): the prices the three lines start from.

Downloads from EODHD (11 calls, about 15 seconds):
  - S&P 500 index, daily closes, as far back as EODHD has it     -> data/GSPC_daily_eodhd.csv        (for line 2)
  - SPY and the eight AI-leaders, daily, 1 Sep to 20 Nov 2026    -> Factsheets/_data_private/a68/a68_start_prices.csv (line 1)
Nothing is computed here. Prices after 20 Nov 2026 are not asked for.

Run in PowerShell from this folder (Articles\\A68_A_Night_to_Remember\\code). Key from EODHD_API_KEY or asked for:
    python download_a68_prices.py
Then tell Claude "a68 prices done".
"""
import sys, time
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent; ART = HERE.parent; P10 = ART.parents[1]
sys.path.insert(0, str(P10 / "DataCockpit"))
import download_eodhd_eu_fundamentals as DF  # noqa: E402

END = "2026-11-20"; BASKET = ["NVDA", "AVGO", "AMD", "MSFT", "META", "GOOGL", "AMZN", "ORCL"]
PRIV = P10 / "Factsheets" / "_data_private" / "a68"; PRIV.mkdir(parents=True, exist_ok=True); (ART / "data").mkdir(exist_ok=True)
def clock(m): print(f"{time.strftime('%H:%M:%S')} {m}", flush=True)

js = DF.get("eod/GSPC.INDX", **{"from": "1927-01-01", "to": END})
if not isinstance(js, list) or not js: sys.exit(f"STOP: no S&P 500 index data from EODHD: {js}")
g = pd.DataFrame(js)[["date", "close"]]; g.to_csv(ART / "data" / "GSPC_daily_eodhd.csv", index=False)
clock(f"S&P 500: {len(g):,} days, {g.date.iloc[0]} to {g.date.iloc[-1]}, last close {g.close.iloc[-1]}")
rows = []
for i, t in enumerate(["SPY"] + BASKET, 1):
    js = DF.get(f"eod/{t}.US", **{"from": "2026-09-01", "to": END}); time.sleep(0.05)
    if not isinstance(js, list) or not js: sys.exit(f"STOP: no data for {t}: {js}")
    d = pd.DataFrame(js)[["date", "close", "adjusted_close"]]; d.insert(0, "ticker", t); rows.append(d)
    clock(f"  {i} of 9  {t}: last day {d.date.iloc[-1]}, close {d.close.iloc[-1]}")
P = pd.concat(rows); P.to_csv(PRIV / "a68_start_prices.csv", index=False)
last = P.groupby("ticker").date.max()
if g.date.iloc[-1] != END or (last != END).any(): clock(f"WARNING: not every series ends on {END}. Paste this to Claude.")
clock('Done. Tell Claude "a68 prices done".')
