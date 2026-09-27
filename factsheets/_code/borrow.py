# -*- coding: utf-8 -*-
"""Borrow-fee proxy for short legs (pre-declared, 27 Sep 2026; closes the FS00 'free shorting' gap).

Tiers by size rank within the month's universe (US: market cap; elsewhere traded value, as in signals2):
  largest 50%       0.25% a year  (general collateral; D'Avolio 2002: ~91% of US loans at GC, median ~0.25%)
  next 30%          0.75% a year
  smallest 20%      2.00% a year  (warm/special names are concentrated among small, volatile stocks;
                                    D'Avolio 2002, Kolasinski, Reed & Ringgenberg 2013, Muravyev, Pearson & Pollet 2022)
  size unknown      2.00% a year
Charged monthly on the short leg's gross weights (after beta scaling). No availability constraint (recalls ignored).
Our universes are large caps, so this is a mid-range proxy; no stock-level short-interest data are used."""
import os

import numpy as np
import pandas as pd

import signals2 as SG2

TIERS = [(0.5, 0.0025), (0.2, 0.0075), (0.0, 0.0200)]
UNKNOWN = 0.0200
_cache = {}


def size_pct(R):
    if R not in _cache:
        s = SG2.build(R)["S"]["size"]
        _cache[R] = s.rank(axis=1, pct=True)
    return _cache[R]


def rates(R, t, names):
    """Annual borrow rate per name at month t (Period)."""
    P = size_pct(R)
    p = P.loc[t].reindex(names) if t in P.index else pd.Series(np.nan, index=names)
    out = pd.Series(UNKNOWN, index=names)
    for lo, r in reversed(TIERS):
        out[p > lo] = r
    out[p.isna()] = UNKNOWN
    # the largest tier must include rank exactly above 0.5
    return out


def monthly_fee(R, t, w):
    """w: short-leg weights (Series, positive, index = names). Returns the fee for one month."""
    if R is None or len(w) == 0:
        return 0.0
    return float((w * rates(R, t, w.index)).sum() / 12)


# --- financing of net long cash (beta-neutral and BAB books), USD risk-free + 50 bp; no credit on net short cash ---
SPREAD = 0.005
_rf = None


def rf_monthly():
    global _rf
    if _rf is None:
        f = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "factors", "french_developed_5f_daily.csv"), index_col=0, parse_dates=True)["RF"]
        _rf = (1 + f).groupby(f.index.to_period("M")).prod() - 1
    return _rf


def financing(t, netcash):
    """Charge for month t+1 on net long cash (sum of long weights minus short weights), if positive."""
    if not np.isfinite(netcash) or netcash <= 1e-9:
        return 0.0
    r = rf_monthly().get(t + 1, np.nan)
    if not np.isfinite(r):
        r = float(rf_monthly().iloc[-1])
    return float(netcash * (r + SPREAD / 12))
