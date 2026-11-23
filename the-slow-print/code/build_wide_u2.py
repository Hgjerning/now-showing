# -*- coding: utf-8 -*-
"""A31 reported extension, U2 European blue chips: wide features added to long_U2.pkl -> long_U2_wide.pkl.
Same prices (EUR), membership and EODHD as-of rules as build_u2.py."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, ".")
from universes import clean_yahoo, snapshot_membership
from wide_features import price_wide, fund_wide
import build_u2_common as C   # prices / FX / as-of helpers shared with build_u2.py

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
px, pxe, pm, months, uni, tick = C.prices()
L = pd.read_pickle(f"{OUT}/long_U2.pkl")
R = C.fundamentals_table(tick)
FL = {"rev": "totalRevenue", "ni": "netIncome", "gp": "grossProfit", "ebit": "ebit", "cfo": "totalCashFromOperatingActivities",
      "capex": "capitalExpenditures", "div": "dividendsPaid"}
ST = {"assets": "totalAssets", "equity": "totalStockholderEquity", "debt": "shortLongTermDebtTotal", "cash": "cash",
      "ca": "totalCurrentAssets", "cl": "totalCurrentLiabilities", "ppe": "propertyPlantAndEquipmentNet", "shares": "commonStockSharesOutstanding"}
R = C.add_ttm(R, FL); R["liab"] = R.totalAssets - R.totalStockholderEquity
for k, c in ST.items():
    R[k] = R[c]
R = C.add_ly(R, ["rev", "ni", "gp", "assets", "shares", "liab"])
ccyf = C.asof_monthly(R.assign(c=R.currency), "c", months, tick)
G = {}
MONEY = {"rev", "ni", "gp", "ebit", "cfo", "capex", "div", "debt"}   # used against market cap -> EUR
for k in list(FL) + list(ST) + ["liab", "rev_ly", "ni_ly", "gp_ly", "assets_ly", "shares_ly", "liab_ly"]:
    v = C.asof_monthly(R, k, months, tick)
    G[k] = C.eur_of(v, ccyf, months) if k in MONEY else v
mc = G["shares"] * pm
F = fund_wide(G, mc)
F.update(price_wide(pxe.astype("float32"), pm.astype("float32"), months))
C.finish(L, F, uni, OUT, "U2")
