# -*- coding: utf-8 -*-
"""Performance and inference helpers for the strategy factsheets (monthly statistics)."""
import numpy as np
import pandas as pd
from scipy import stats as st


def nw_t(x, lags=6):
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x); m = x.mean(); e = x - m
    s = e @ e / n
    for L in range(1, lags + 1):
        s += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / n
    se = np.sqrt(s / n)
    return dict(mean=float(m), t=float(m / se), p2=float(2 * (1 - st.norm.cdf(abs(m / se)))))


def nw_ols(y, x, lags=6):
    y = np.asarray(y, float); X = np.column_stack([np.ones(len(y)), np.asarray(x, float)])
    ok = ~np.isnan(y) & ~np.isnan(X).any(1); y, X = y[ok], X[ok]; n = len(y)
    XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y; u = y - X @ b
    Xu = X * u[:, None]; S = Xu.T @ Xu / n
    for L in range(1, lags + 1):
        G = Xu[L:].T @ Xu[:-L] / n; S += (1 - L / (lags + 1)) * (G + G.T)
    V = n * XtXi @ S @ XtXi; se = np.sqrt(np.diag(V))
    return dict(alpha=float(b[0]), beta=float(b[1]), t_alpha=float(b[0] / se[0]), t_beta=float(b[1] / se[1]))


def to_monthly(daily):
    return (1 + daily).resample("ME").prod() - 1


def drawdown(r):
    w = (1 + r.fillna(0)).cumprod(); return w / w.cummax() - 1


def stationary_idx(n, b, rng):
    idx = np.empty(n, int); idx[0] = rng.integers(n)
    for i in range(1, n):
        idx[i] = rng.integers(n) if rng.random() < 1 / b else (idx[i - 1] + 1) % n
    return idx


def sharpe(x):
    x = np.asarray(x, float); return float(x.mean() / x.std(ddof=1) * np.sqrt(12))


def boot_sharpe(m, b=6, draws=5000, seed=42):
    x = np.asarray(m, float); x = x[~np.isnan(x)]; rng = np.random.default_rng(seed); n = len(x)
    d = [sharpe(x[stationary_idx(n, b, rng)]) for _ in range(draws)]
    return [float(v) for v in np.percentile(d, [2.5, 97.5])]


def psr(m, sr_star=0.0):
    """Probabilistic Sharpe ratio (Bailey & Lopez de Prado 2012) on monthly data; sr_star annual."""
    x = np.asarray(m, float); x = x[~np.isnan(x)]; n = len(x)
    s = x.mean() / x.std(ddof=1); g3 = st.skew(x); g4 = st.kurtosis(x, fisher=False)
    z = (s - sr_star / np.sqrt(12)) * np.sqrt(n - 1) / np.sqrt(1 - g3 * s + (g4 - 1) / 4 * s ** 2)
    return float(st.norm.cdf(z))


def summary(m, bench=None, daily=None):
    """m: monthly returns. daily (optional) used for max drawdown and daily vol."""
    m = m.dropna(); n = len(m)
    cagr = float((1 + m).prod() ** (12 / n) - 1)
    vol = float(m.std(ddof=1) * np.sqrt(12))
    dd = drawdown(daily if daily is not None else m)
    down = m[m < 0]
    out = dict(start=str(m.index[0].date()), end=str(m.index[-1].date()), months=n, cagr=cagr, ann_mean=float(m.mean() * 12), vol=vol,
               sharpe=sharpe(m), sharpe_ci=boot_sharpe(m), psr0=psr(m), sortino=float(m.mean() * 12 / (np.sqrt((down ** 2).sum() / n) * np.sqrt(12))) if len(down) else np.nan,
               maxdd=float(dd.min()), maxdd_date=str(dd.idxmin().date()), calmar=float(cagr / abs(dd.min())) if dd.min() < 0 else np.nan,
               hit=float((m > 0).mean()), best=float(m.max()), worst=float(m.min()), skew=float(st.skew(m)), t_mean=nw_t(m)["t"])
    if bench is not None:
        b = bench.reindex(m.index)
        reg = nw_ols(m.values, b.values)
        out.update(alpha=reg["alpha"] * 12, t_alpha=reg["t_alpha"], beta=reg["beta"], corr=float(np.corrcoef(m, b)[0, 1]))
        ex = m - b
        out.update(excess=float(ex.mean() * 12), te=float(ex.std() * np.sqrt(12)), ir=float(ex.mean() / ex.std() * np.sqrt(12)) if ex.std() > 1e-12 else np.nan)
    return out


def calendar_table(m):
    y = (1 + m).groupby(m.index.year).prod() - 1
    return y
