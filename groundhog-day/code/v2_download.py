# -*- coding: utf-8 -*-
"""Derive data/shiller_dividends.csv (monthly S&P price and dividend, Shiller) from data/ie_data.xls.

Save ie_data.xls by hand from shillerdata.com into data/ first (scripted downloads are blocked).
The series is cut at September 2023, the vintage used for the version-2 dividend check and for C31-5.
The September 2023 price in that vintage was a partial-month value and differs from later files; no
window in this study uses it. Yahoo series: code/download_data.py.

    python code/v2_download.py
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "data")
x = pd.read_excel(os.path.join(D, "ie_data.xls"), sheet_name="Data", header=7)
x = x[["Date", "P", "D"]].dropna(subset=["Date", "P"])
x = x[pd.to_numeric(x["Date"], errors="coerce").notna()]
yr = x["Date"].astype(float); y = yr.astype(int); mth = ((yr - y) * 100).round().astype(int).clip(1, 12)
out = pd.DataFrame({"date": pd.to_datetime(dict(year=y, month=mth, day=1)), "price": x["P"].astype(float).values,
                    "dividend": pd.to_numeric(x["D"], errors="coerce").values})
out = out[out.date <= "2023-09-01"]
out.to_csv(os.path.join(D, "shiller_dividends_rebuilt.csv"), index=False)
print("Shiller", out.date.iloc[0].date(), out.date.iloc[-1].date(), len(out), "-> data/shiller_dividends_rebuilt.csv")
print("Rename it to shiller_dividends.csv if that file is missing. Only the September 2023 row should differ.")
