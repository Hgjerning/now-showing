"""
InvestmentLibrary.stats
========================
Return, volatility and risk-adjusted performance statistics.

Consolidated from Backtest/Py/PortfolioStatistics.py, PortfolioAnalytics.py and
support.py, which each carried their own (slightly inconsistent) copies of
portfolio_return / portfolio_vol / annualisation helpers. This module is the
single source of truth going forward.

All functions accept a pandas Series (single asset) or DataFrame (multiple
assets, one column each) of PERIODIC returns (not prices, not cumulative).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def compound(r: pd.Series | pd.DataFrame):
    """Total compounded return of a return series: prod(1+r) - 1."""
    return (1 + r).prod() - 1


def annualize_rets(r: pd.Series | pd.DataFrame, periods_per_year: int):
    """
    Annualizes a set of returns.
    periods_per_year: 252 for daily, 12 for monthly, 52 for weekly, 4 for quarterly.
    """
    compounded_growth = (1 + r).prod()
    n_periods = r.shape[0]
    return compounded_growth ** (periods_per_year / n_periods) - 1


def annualize_vol(r: pd.Series | pd.DataFrame, periods_per_year: int):
    """Annualizes the volatility of a set of returns."""
    return r.std(ddof=0) * (periods_per_year ** 0.5)


def sharpe_ratio(r: pd.Series | pd.DataFrame, riskfree_rate: float, periods_per_year: int):
    """
    Computes the annualized Sharpe ratio of a set of returns.
    riskfree_rate is an ANNUAL rate; it is converted to the periodic rate internally.
    """
    rf_per_period = (1 + riskfree_rate) ** (1 / periods_per_year) - 1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualize_rets(excess_ret, periods_per_year)
    ann_vol = annualize_vol(r, periods_per_year)
    return ann_ex_ret / ann_vol


def sortino_ratio(r: pd.Series | pd.DataFrame, riskfree_rate: float, periods_per_year: int):
    """
    Like sharpe_ratio, but penalizes only downside deviation (semideviation)
    rather than total volatility. New addition vs. the legacy library.
    """
    rf_per_period = (1 + riskfree_rate) ** (1 / periods_per_year) - 1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualize_rets(excess_ret, periods_per_year)
    # Semi-deviation over ALL periods (zero-clipped, squared, mean over N), not the std of just
    # the negative subset -- that variant divides by the count of negative periods instead of N
    # and centers on the negative subset's own mean, which both inflates the ratio and divides
    # by zero whenever there is exactly one negative-excess-return period. Fixed 2026-09-19.
    downside_dev = (excess_ret.clip(upper=0) ** 2).mean() ** 0.5 * (periods_per_year ** 0.5)
    return ann_ex_ret / downside_dev


def calmar_ratio(r: pd.Series, periods_per_year: int):
    """CAGR / max drawdown. New addition; imports risk.drawdown lazily to avoid a cycle."""
    from .risk import drawdown
    cagr = annualize_rets(r, periods_per_year)
    max_dd = drawdown(r)["Drawdown"].min()
    return cagr / abs(max_dd) if max_dd != 0 else np.nan


def portfolio_return(weights: np.ndarray, returns: np.ndarray) -> float:
    """Computes the return on a portfolio from constituent returns and weights."""
    return weights.T @ returns


def portfolio_vol(weights: np.ndarray, covmat: np.ndarray) -> float:
    """Weights -> portfolio volatility, given a covariance matrix."""
    return np.sqrt(weights.T @ covmat @ weights)


def hit_ratio(signal_returns: pd.Series) -> float:
    """Fraction of non-zero-signal periods with a positive return. Common in the
    Quantra 'Trade Level Analytics' notebooks; centralised here instead of being
    re-implemented per course."""
    active = signal_returns[signal_returns != 0]
    if len(active) == 0:
        return np.nan
    return (active > 0).mean()


def turnover(weights: pd.DataFrame) -> pd.Series:
    """Period-over-period one-way turnover of a weights DataFrame (dates x assets)."""
    return weights.diff().abs().sum(axis=1)
