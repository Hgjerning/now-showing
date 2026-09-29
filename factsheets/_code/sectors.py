# -*- coding: utf-8 -*-
"""Static sector map (Morningstar/Yahoo 11-sector taxonomy) from Sharadar TICKERS (2019 snapshot, incl. delisted)
and the Project1/Project2 Yahoo sector caches. Private source files live in data/sectors (not published)."""
import json
import os

import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "sectors")
_M = None


def sector_map():
    global _M
    if _M is not None:
        return _M
    m = {}
    t = pd.read_csv(os.path.join(D, "Sharadar_tickers.csv"), usecols=["table", "ticker", "sector"], dtype=str, engine="python", on_bad_lines="skip")
    t = t[t.table == "SF1"].dropna()
    for a, b in zip(t.ticker, t.sector):
        m.setdefault(a, b)
    for f in ["sector_country_classification_2026-09-17.csv", "EU_sectors.csv", "US_sectors.csv", "scandi_sectors.csv"]:
        x = pd.read_csv(os.path.join(D, f), dtype=str)
        for a, b in zip(x.Ticker, x.Sector):
            if isinstance(b, str) and b not in ("Unknown", ""):
                m[a] = b
    for a, v in json.load(open(os.path.join(D, "sectors_WD.json"))).items():
        if v.get("Sector") not in (None, "Unknown", ""):
            m[a] = v["Sector"]
    _M = m
    return m
