# -*- coding: utf-8 -*-
"""US stock-level fundamental signals from Sharadar SF1 (ARQ, as reported quarterly), point in time.

A filing is usable from its filing date (`date`); at month-end t each stock carries its latest filing with
date <= t, and only if that filing is at most 200 days old. Flows are trailing four quarters (TTM) where a
level is needed, single quarters where the definition is quarterly. Definitions follow Jensen, Kelly &
Pedersen (2023) as closely as SF1 allows; the JKP column in FUND lists the matching factor.

Signals (direction = long the high or the low end, from the original papers):
  Debt issuance    dbt_gr   debt growth over 4 quarters                      low   (debt_gr1 / Lyandres et al.)
                   noa_at   net operating assets / lagged assets             low   (noa_at, Hirshleifer et al. 2004)
                   nfna_gr  change in net financial assets / lagged assets    high  (nfna_gr1a, Richardson et al. 2005)
  Profit growth    sale_su  standardised quarterly sales surprise (8q std)    high  (saleq_su, Jegadeesh & Livnat 2006)
                   ni_be_ch change in quarterly net income / book equity      high  (niq_be_chg1)
                   ni_at_ch change in quarterly net income / assets           high  (niq_at_chg1)
  Value            bm       book equity / market cap                          high  (be_me, Fama & French 1992)
                   ep       TTM earnings / market cap                         high  (ni_me, Basu 1977)
                   cfp      TTM operating cash flow / market cap              high  (ocf_me)
  Profitability    gp_at    TTM gross profit / assets                         high  (gp_at, Novy-Marx 2013)
                   op_be    TTM operating income / book equity                high  (ope_be, Fama & French 2015)
  Investment       at_gr    asset growth over 4 quarters                      low   (at_gr1, Cooper et al. 2008)
                   capx_gr  capex growth over 4 quarters                      low   (capx_gr1)
  Accruals         acc_at   (TTM net income - TTM operating cash flow)/assets low   (oaccruals_at, Sloan 1996)
Composites per theme: average cross-sectional percentile rank of the members, each signed so that high = good."""
import os

import numpy as np
import pandas as pd

import data

HERE = os.path.dirname(os.path.abspath(__file__)); D = data.D; CACHE = data.CACHE   # 2026-10-01: follows data.py
FUND = {  # signal: (theme, long_high, label, JKP match)
    "dbt_gr": ("Debt issuance", False, "Debt growth", "debt_gr3"),
    "noa_at": ("Debt issuance", False, "Net operating assets", "noa_at"),
    "nfna_gr": ("Debt issuance", True, "Net financial asset growth", "nfna_gr1a"),
    "sale_su": ("Profit growth", True, "Sales surprise", "saleq_su"),
    "ni_be_ch": ("Profit growth", True, "Earnings change / equity", "niq_be_chg1"),
    "ni_at_ch": ("Profit growth", True, "Earnings change / assets", "niq_at_chg1"),
    "bm": ("Value", True, "Book-to-market", "be_me"),
    "ep": ("Value", True, "Earnings yield", "ni_me"),
    "cfp": ("Value", True, "Cash-flow yield", "ocf_me"),
    "gp_at": ("Profitability", True, "Gross profitability", "gp_at"),
    "op_be": ("Profitability", True, "Operating profitability", "ope_be"),
    "at_gr": ("Investment", False, "Asset growth", "at_gr1"),
    "capx_gr": ("Investment", False, "Capex growth", "capx_gr1"),
    "acc_at": ("Accruals", False, "Accruals", "oaccruals_at"),
}
THEMES = ["Debt issuance", "Profit growth", "Value", "Profitability", "Investment", "Accruals"]
COMP = {t: "c_" + t.lower().replace(" ", "_") for t in THEMES}
JKP_CLUSTER = {"Debt issuance": "Debt Issuance", "Profit growth": "Profit Growth", "Value": "Value", "Profitability": "Profitability", "Investment": "Investment", "Accruals": "Accruals"}
COLS = ["ticker", "calendardate", "date", "revenue", "netinccmn", "gp", "opinc", "ncfo", "assets", "equity", "debt", "cashneq", "investments", "liabilities", "capex"]


def filings():
    f = pd.read_csv(data._us("us_fundamentals.csv"), usecols=COLS, parse_dates=["calendardate", "date"])
    f = f.sort_values(["ticker", "calendardate", "date"]).drop_duplicates(["ticker", "calendardate"], keep="first")
    g = f.groupby("ticker", group_keys=False)
    ttm = lambda c: g[c].transform(lambda s: s.rolling(4, min_periods=4).sum())
    lag4 = lambda c: g[c].shift(4)
    # a 4-quarter lag must be ~1 year back, otherwise quarters are missing
    gap = (f.calendardate - g["calendardate"].shift(4)).dt.days
    ok4 = gap.between(330, 400)
    for c in ["revenue", "netinccmn", "gp", "opinc", "ncfo"]:
        f[c + "_ttm"] = ttm(c).where(ok4 | g["calendardate"].shift(3).notna())
    pos = lambda s: s.where(s > 0)
    A4 = pos(lag4("assets")).where(ok4)
    nfa = f.cashneq.fillna(0) + f.investments.fillna(0) - f.debt.fillna(0)
    noa = (f.assets - f.cashneq.fillna(0) - f.investments.fillna(0)) - (f.liabilities - f.debt.fillna(0))
    out = pd.DataFrame({"ticker": f.ticker, "date": f.date})
    out["dbt_gr"] = (f.debt / pos(lag4("debt")) - 1).where(ok4)
    out["noa_at"] = noa / A4
    out["nfna_gr"] = (nfa - g.apply(lambda d: (d.cashneq.fillna(0) + d.investments.fillna(0) - d.debt.fillna(0)).shift(4)).reset_index(level=0, drop=True).reindex(f.index)) / A4
    dq = (f.revenue - lag4("revenue")).where(ok4)
    sd = dq.groupby(f.ticker).transform(lambda s: s.rolling(8, min_periods=6).std())
    out["sale_su"] = dq / sd.where(sd > 0)
    dn = (f.netinccmn - lag4("netinccmn")).where(ok4)
    out["ni_be_ch"] = dn / pos(f.equity)
    out["ni_at_ch"] = dn / pos(f.assets)
    out["gp_at"] = f.gp_ttm / pos(f.assets)
    out["op_be"] = f.opinc_ttm / pos(f.equity)
    out["at_gr"] = (f.assets / A4 - 1)
    capx = f.capex.abs(); capx4 = lag4("capex").abs()
    out["capx_gr"] = (capx / capx4.where(capx4 > 0) - 1).where(ok4)
    out["acc_at"] = (f.netinccmn_ttm - f.ncfo_ttm) / pos(f.assets)
    # level items for the value ratios (divided by month-end market cap later)
    out["be"] = pos(f.equity); out["ni_ttm"] = f.netinccmn_ttm; out["cfo_ttm"] = f.ncfo_ttm
    return out


def monthly(out, cols, months, tickers, max_age=200):
    """Latest filing per stock at each month-end, if not older than max_age days."""
    res = {}
    o = out.sort_values("date")
    for c in cols:
        w = o.pivot_table(index="date", columns="ticker", values=c, aggfunc="last").reindex(columns=tickers)
        dt = pd.DataFrame(np.where(w.notna(), w.index.values[:, None], np.datetime64("NaT")), index=w.index, columns=w.columns)
        u = w.index.union(months)
        v = w.reindex(u).ffill().reindex(months); a = dt.reindex(u).ffill().reindex(months)
        age = pd.DataFrame(np.repeat(months.values[:, None], len(tickers), 1), index=months, columns=tickers) - a.apply(pd.to_datetime)
        res[c] = v.where(age <= pd.Timedelta(days=max_age))
    return res


def winsor(df, q=0.01):
    lo = df.quantile(q, axis=1); hi = df.quantile(1 - q, axis=1)
    return df.clip(lower=lo, upper=hi, axis=0)


def build():
    f = os.path.join(CACHE, "fund_US.pkl")
    if os.path.exists(f):
        return pd.read_pickle(f)
    o = data.load("US"); mc = o["mcap"]                      # month-end market cap (Timestamp index)
    months = mc.index; tickers = list(mc.columns)
    F = filings()
    M = monthly(F, [c for c in F.columns if c not in ("ticker", "date")], months, tickers)
    mcp = mc.where(mc > 0)
    M["bm"] = M.pop("be") / mcp; M["ep"] = M.pop("ni_ttm") / mcp; M["cfp"] = M.pop("cfo_ttm") / mcp
    S = {}
    for k in FUND:
        x = winsor(M[k].replace([np.inf, -np.inf], np.nan)); x.index = x.index.to_period("M"); S[k] = x
    for t in THEMES:
        ks = [k for k in FUND if FUND[k][0] == t]
        rk = [S[k].rank(axis=1, pct=True) * (1 if FUND[k][1] else -1) + (0 if FUND[k][1] else 1) for k in ks]
        S[COMP[t]] = sum(r.fillna(r.mean(axis=1).values[:, None] * 0 + 0.5) if False else r for r in rk) / len(rk) if len(rk) == 1 else pd.concat(rk).groupby(level=0).mean()
    pd.to_pickle(S, f)
    return S


if __name__ == "__main__":
    S = build()
    for k, v in S.items():
        print(f"{k:14s} coverage median {int(v.loc['2013':].notna().sum(axis=1).median())}")
