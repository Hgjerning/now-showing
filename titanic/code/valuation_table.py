# -*- coding: utf-8 -*-
"""Version 2 (7 Oct 2026, after external review): how expensive are the eight AI leaders, against
the tech leaders at the Nasdaq peak in March 2000? REPORTED, NOT GATED: no trial is spent.

Inputs (licensed Sharadar files in Project2's cache, not published):
  SF1 ARQ 2009-2026 (us_fundamentals.csv), SF1 ARQ 1997-2012 and SEP prices (backfill_1998/),
  daily closes 2026 (us_master_universe_prices.csv).
Output: ../results/valuation.json (derived ratios only).
Method: trailing four quarters known at the date (filing date <= date). Market value = market value
at the latest filing x price change from that filing to the date (split-consistent price series).
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "..", "..", "..", "Project2 Investment Strategy", "reporting", "sharadar_cache")
TODAY_NAMES = ["NVDA", "AVGO", "AMD", "MSFT", "META", "GOOGL", "AMZN", "ORCL"]
Y2K_NAMES = ["CSCO", "MSFT", "ORCL", "INTC", "NVDA"]
Y2K_DATE = pd.Timestamp("2000-03-10")  # Nasdaq Composite peak close
COLS = ["ticker", "calendardate", "date", "marketcap", "revenue", "netinc", "fcf", "capex", "ebit"]


def ttm(f, tic, when):
    q = f[(f.ticker == tic) & (f.date <= when)].sort_values("calendardate").drop_duplicates("calendardate", keep="last")
    if len(q) < 4:
        return None
    last4, prev4 = q.iloc[-4:], (q.iloc[-8:-4] if len(q) >= 8 else None)
    return dict(rev=last4.revenue.sum(), rev_prev=(prev4.revenue.sum() if prev4 is not None else np.nan), ni=last4.netinc.sum(), fcf=last4.fcf.sum(),
                capex=-last4.capex.sum(), ebit=last4.ebit.sum(), mcap_filing=q.iloc[-1].marketcap,
                filing=q.iloc[-1].date, quarter=str(q.iloc[-1].calendardate.date()))


def row(t, mcap):
    return dict(mcap_bn=round(mcap / 1e9, 0), ps=round(mcap / t["rev"], 1),
                pe=(round(mcap / t["ni"], 0) if t["ni"] > 0 else None),
                fcf_yield=round(t["fcf"] / mcap * 100, 1), rev_growth=(None if np.isnan(t["rev_prev"]) else round((t["rev"] / t["rev_prev"] - 1) * 100, 0)),
                net_margin=round(t["ni"] / t["rev"] * 100, 0), op_margin=round(t["ebit"] / t["rev"] * 100, 0),
                capex_to_rev=round(t["capex"] / t["rev"] * 100, 0), last_quarter=t["quarter"])


def agg(rows):
    """Basket as one company: sums, so big names weigh in proportion to size."""
    s = {k: sum(r[k] for r in rows) for k in ["mcap", "rev", "ni", "fcf", "capex", "ebit"]}
    g = [r for r in rows if not np.isnan(r["rev_prev"])]
    gr = sum(r["rev"] for r in g) / sum(r["rev_prev"] for r in g) - 1
    return dict(mcap_bn=round(s["mcap"] / 1e9, 0), ps=round(s["mcap"] / s["rev"], 1), pe=round(s["mcap"] / s["ni"], 0),
                fcf_yield=round(s["fcf"] / s["mcap"] * 100, 1), rev_growth=round(gr * 100, 0),
                net_margin=round(s["ni"] / s["rev"] * 100, 0), op_margin=round(s["ebit"] / s["rev"] * 100, 0),
                capex_to_rev=round(s["capex"] / s["rev"] * 100, 0))


def main():
    out = {"note": "Added in version 2 (7 Oct 2026). Reported, not gated. Trailing four quarters known at the date."}
    # ---- today
    f = pd.read_csv(os.path.join(CACHE, "us_fundamentals.csv"), usecols=COLS, parse_dates=["calendardate", "date"])
    f = f[f.ticker.isin(TODAY_NAMES)]
    px = pd.read_csv(os.path.join(CACHE, "us_master_universe_prices.csv"), usecols=["date"] + TODAY_NAMES,
                     index_col="date", parse_dates=True).sort_index()
    when = px.loc[:"2026-09-30"].dropna(how="all").index[-1]
    rows, raw = {}, []
    for tic in TODAY_NAMES:
        t = ttm(f, tic, when)
        p = px[tic].dropna()
        mcap = t["mcap_filing"] * p.loc[:when].iloc[-1] / p.loc[:t["filing"]].iloc[-1]
        rows[tic] = row(t, mcap); raw.append(dict(t, mcap=mcap))
    out["today"] = dict(date=str(when.date()), names=rows, basket=agg(raw))
    # ---- March 2000
    g = pd.read_parquet(os.path.join(CACHE, "backfill_1998", "sf1_arq_1997_2012.parquet"), columns=COLS)
    g["calendardate"] = pd.to_datetime(g.calendardate); g["date"] = pd.to_datetime(g.date)
    g = g[g.ticker.isin(Y2K_NAMES)]
    sep = pd.read_parquet(os.path.join(CACHE, "backfill_1998", "sep_1997_2012.parquet"), columns=["ticker", "date", "closeadj"])
    sep = sep[sep.ticker.isin(Y2K_NAMES)]; sep["date"] = pd.to_datetime(sep.date)
    rows, raw = {}, []
    for tic in Y2K_NAMES:
        t = ttm(g, tic, Y2K_DATE)
        p = sep[sep.ticker == tic].set_index("date").closeadj.sort_index()
        mcap = t["mcap_filing"] * p.loc[:Y2K_DATE].iloc[-1] / p.loc[:t["filing"]].iloc[-1]
        rows[tic] = row(t, mcap); raw.append(dict(t, mcap=mcap))
    out["march_2000"] = dict(date=str(Y2K_DATE.date()), names=rows, basket=agg(raw))
    json.dump(out, open(os.path.join(ROOT, "results", "valuation.json"), "w"), indent=1)
    for k in ["today", "march_2000"]:
        print(k, out[k]["date"]); print(pd.DataFrame(out[k]["names"]).T.to_string()); print("basket", out[k]["basket"])


if __name__ == "__main__":
    main()
