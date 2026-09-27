"""
InvestmentLibrary.risk
========================
Drawdown, tail-risk (VaR/CVaR) and distribution-shape statistics.

Ported and cleaned from Backtest/Py/PortfolioRisk.py (the legacy file had
var_gaussian and var_gaussian_CornishFisher as two near-identical functions
with different defaults for the same "modified" argument -- collapsed into one
function here with an explicit `modified` flag).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import scipy.stats
from scipy.stats import norm


def drawdown(return_series: pd.Series, start: float = 1000.0) -> pd.DataFrame:
    """
    Takes a time series of asset returns.
    Returns a DataFrame with the Wealth index, running Peaks, and Drawdown (%).

    Guards a real edge case, found in Templates/7.0 ML Driven Options Signal.ipynb's
    100%-position-sizing case: if wealth is wiped out at or before its running peak
    (e.g. a -100% return in the first period, or any period straight after an earlier
    total loss), Peaks is 0 there too -- (0 - 0) / 0 would otherwise silently produce
    NaN instead of the correct -100% drawdown. Peaks (a running max of Wealth, which
    can't go negative from a >=-100% return) is 0 only where Wealth is genuinely 0, so
    it's safe to fix the drawdown to -1.0 exactly there. This does NOT mask a
    different, legitimate source of NaN -- a return_series with its own missing-data
    gaps (e.g. an incomplete-history ticker) produces NaN Wealth/Peaks at those points,
    not a Peaks of 0, so those stay correctly NaN.
    """
    wealth_index = start * (1 + return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks) / previous_peaks
    drawdowns = drawdowns.mask(previous_peaks == 0, -1.0)
    return pd.DataFrame({
        "Wealth": wealth_index,
        "Peaks": previous_peaks,
        "Drawdown": drawdowns,
    })


def max_drawdown(return_series: pd.Series) -> float:
    return drawdown(return_series)["Drawdown"].min()


def is_normal(r, level: float = 0.01):
    """
    Jarque-Bera test for normality, applied at the given significance level
    (1% by default). Returns True if normality is NOT rejected.
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(is_normal, level=level)
    statistic, p_value = scipy.stats.jarque_bera(r)
    return p_value > level


def semideviation(r):
    """Downside (negative) semideviation of r."""
    is_negative = r < 0
    return r[is_negative].std(ddof=0)


def skewness(r):
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    return (demeaned_r ** 3).mean() / sigma_r ** 3


def kurtosis(r):
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    return (demeaned_r ** 4).mean() / sigma_r ** 4


def var_historic(r, level: float = 5):
    """Historic VaR: the loss such that `level` percent of returns fall below it."""
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_historic, level=level)
    elif isinstance(r, pd.Series):
        return -np.percentile(r, level)
    raise TypeError("Expected r to be a Series or DataFrame")


def var_gaussian(r, level: float = 5, modified: bool = False):
    """
    Parametric Gaussian VaR of a Series or DataFrame.
    If modified=True, applies the Cornish-Fisher expansion using the sample's
    own skewness and kurtosis (this replaces the old duplicate
    var_gaussian_CornishFisher function, which just hard-coded modified=True).
    """
    z = norm.ppf(level / 100)
    if modified:
        s = skewness(r)
        k = kurtosis(r)
        z = (z +
             (z ** 2 - 1) * s / 6 +
             (z ** 3 - 3 * z) * (k - 3) / 24 -
             (2 * z ** 3 - 5 * z) * (s ** 2) / 36)
    return -(r.mean() + z * r.std(ddof=0))


def cvar_historic(r, level: float = 5):
    """Historic Conditional VaR (expected shortfall beyond the VaR threshold)."""
    if isinstance(r, pd.Series):
        is_beyond = r <= -var_historic(r, level=level)
        return -(r[is_beyond].mean())
    elif isinstance(r, pd.DataFrame):
        return r.aggregate(cvar_historic, level=level)
    raise TypeError("Expected r to be a Series or DataFrame")


def summary_stats(r: pd.DataFrame, riskfree_rate: float = 0.03, periods_per_year: int = 252) -> pd.DataFrame:
    """
    One-shot tear-sheet style summary: annualised return/vol, Sharpe, Sortino,
    skew, kurtosis, historic VaR/CVaR and max drawdown, for each column of r.
    Mirrors Backtest/Py/PortfolioBacktest.py::summary_stats but adds Sortino
    and Calmar and is periods_per_year-aware instead of hard-coded to monthly.
    """
    from .stats import annualize_rets, annualize_vol, sharpe_ratio, sortino_ratio, calmar_ratio

    ann_r = r.aggregate(annualize_rets, periods_per_year=periods_per_year)
    ann_vol = r.aggregate(annualize_vol, periods_per_year=periods_per_year)
    ann_sr = r.aggregate(sharpe_ratio, riskfree_rate=riskfree_rate, periods_per_year=periods_per_year)
    sortino = r.aggregate(sortino_ratio, riskfree_rate=riskfree_rate, periods_per_year=periods_per_year)
    calmar = r.aggregate(calmar_ratio, periods_per_year=periods_per_year)
    dd = r.aggregate(lambda rr: drawdown(rr)["Drawdown"].min())
    skew = r.aggregate(skewness)
    kurt = r.aggregate(kurtosis)
    cf_var5 = r.aggregate(var_gaussian, modified=True)
    hist_cvar5 = r.aggregate(cvar_historic)
    return pd.DataFrame({
        "Annualized Return": ann_r,
        "Annualized Vol": ann_vol,
        "Sharpe Ratio": ann_sr,
        "Sortino Ratio": sortino,
        "Calmar Ratio": calmar,
        "Skewness": skew,
        "Kurtosis": kurt,
        "Cornish-Fisher VaR (5%)": cf_var5,
        "Historic CVaR (5%)": hist_cvar5,
        "Max Drawdown": dd,
    })
