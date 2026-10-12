# -*- coding: utf-8 -*-
"""Fetch the price data used in Case 31 (not redistributed in this repository) and compare with data/SHA256SUMS.

    python code/download_data.py

Yahoo series (^GSPC, ^FTSE, ^GDAXI) come from yfinance, cut at the dates used in the article.
Yahoo revises history now and then, so a hash mismatch is reported, not treated as an error:
check the numbers in results/ instead. Shiller's ie_data.xls must be saved by hand from
shillerdata.com into data/; code/v2_download.py then derives data/shiller_dividends.csv from it.
"""
import hashlib, os
import yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "data")
SERIES = [("^GSPC", "GSPC_daily_close.csv", "1927-01-01", "2026-09-12"),
          ("^FTSE", "FTSE_daily_close.csv", "1984-01-01", "2026-10-06"),
          ("^GDAXI", "GDAXI_daily_close.csv", "1987-01-01", "2026-10-06"),
          ("^N225", "N225_daily_close.csv", "1964-01-01", "2026-10-06")]
for tic, fn, start, end in SERIES:
    h = yf.download(tic, start=start, end=end, auto_adjust=False, progress=False)
    s = h["Close"].squeeze().dropna(); s.index = s.index.tz_localize(None).normalize()
    s.rename("close").rename_axis("date").to_csv(os.path.join(D, fn))
    print(tic, s.index[0].date(), s.index[-1].date(), len(s))
ref = dict(l.split()[::-1] for l in open(os.path.join(D, "SHA256SUMS")) if l.strip())
for fn, h in ref.items():
    p = os.path.join(D, fn)
    if not os.path.exists(p): print("missing:", fn); continue
    ok = hashlib.sha256(open(p, "rb").read()).hexdigest() == h
    print(("match   " if ok else "DIFFERS ") + fn)
