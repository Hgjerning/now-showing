# -*- coding: utf-8 -*-
"""Small, dependency-light statistics used across A06-A10."""
import numpy as np
from scipy import stats as st


def nw_t(x, lags):
    """Mean, Newey-West (Bartlett) standard error, t-stat and one-sided p (mean > 0)."""
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x); m = x.mean(); e = x - m
    s = e @ e / n
    for L in range(1, lags + 1):
        s += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / n
    se = np.sqrt(s / n); t = m / se
    return dict(mean=float(m), se=float(se), t=float(t), p_gt=float(1 - st.norm.cdf(t)), p_lt=float(st.norm.cdf(t)), n=int(n))


def nw_ols(y, X, lags):
    """OLS with Newey-West covariance. X without constant; returns coef, t (incl. constant first)."""
    y = np.asarray(y, float); X = np.column_stack([np.ones(len(y)), np.asarray(X, float)])
    ok = ~np.isnan(y) & ~np.isnan(X).any(1); y, X = y[ok], X[ok]; n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y; u = y - X @ b
    Xu = X * u[:, None]; S = Xu.T @ Xu / n
    for L in range(1, lags + 1):
        G = Xu[L:].T @ Xu[:-L] / n; S += (1 - L / (lags + 1)) * (G + G.T)
    V = n * XtXi @ S @ XtXi; se = np.sqrt(np.diag(V))
    r2 = 1 - (u @ u) / ((y - y.mean()) @ (y - y.mean()))
    return dict(coef=b, se=se, t=b / se, n=n, r2=float(r2))


def sharpe(x, ann=12):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    return float(x.mean() / x.std(ddof=1) * np.sqrt(ann))


def stationary_idx(n, mean_block, rng):
    idx = np.empty(n, int); idx[0] = rng.integers(n); p = 1 / mean_block
    for i in range(1, n):
        idx[i] = rng.integers(n) if rng.random() < p else (idx[i - 1] + 1) % n
    return idx


def paired_sharpe_diff(a, b, draws=10000, mean_block=6, seed=42, ann=12):
    """Sharpe(a) - Sharpe(b), stationary bootstrap (Politis-Romano). p = one-sided (diff > 0),
    computed on the centred bootstrap distribution."""
    a, b = np.asarray(a, float), np.asarray(b, float); ok = ~np.isnan(a) & ~np.isnan(b); a, b = a[ok], b[ok]
    obs = sharpe(a, ann) - sharpe(b, ann); rng = np.random.default_rng(seed); n = len(a); d = np.empty(draws)
    for k in range(draws):
        i = stationary_idx(n, mean_block, rng); d[k] = sharpe(a[i], ann) - sharpe(b[i], ann)
    p = (1 + np.sum(d - d.mean() >= obs)) / (draws + 1)
    lo, hi = np.percentile(d, [2.5, 97.5])
    return dict(diff=float(obs), p=float(p), lo=float(lo), hi=float(hi))


def block_boot_mean(x, block=4, draws=10000, seed=42, null=0.0):
    """Moving-block bootstrap of a mean; one-sided p for mean > null (centred)."""
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x); rng = np.random.default_rng(seed)
    nb = int(np.ceil(n / block)); m = np.empty(draws)
    for k in range(draws):
        s = rng.integers(0, n - block + 1, nb); i = (s[:, None] + np.arange(block)).ravel()[:n]; m[k] = x[i].mean()
    obs = x.mean(); p = (1 + np.sum(m - m.mean() >= obs - null)) / (draws + 1)
    lo, hi = np.percentile(m, [2.5, 97.5])
    return dict(mean=float(obs), p=float(p), lo=float(lo), hi=float(hi), n=int(n))


def auc(score, y):
    """P(score of a positive > score of a negative), ties count half."""
    score, y = np.asarray(score, float), np.asarray(y, bool)
    ok = ~np.isnan(score); score, y = score[ok], y[ok]
    n1, n0 = y.sum(), (~y).sum()
    if n1 == 0 or n0 == 0:
        return np.nan
    r = st.rankdata(score)
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def deflated_sharpe(sr_best, sr_all, T, skew, kurt):
    """Bailey & Lopez de Prado (2014). Per-period Sharpe ratios. kurt = non-excess kurtosis."""
    N = len(sr_all); v = np.var(sr_all, ddof=1); g = 0.5772156649
    sr0 = np.sqrt(v) * ((1 - g) * st.norm.ppf(1 - 1 / N) + g * st.norm.ppf(1 - 1 / (N * np.e)))
    z = (sr_best - sr0) * np.sqrt(T - 1) / np.sqrt(1 - skew * sr_best + (kurt - 1) / 4 * sr_best ** 2)
    return dict(sr0=float(sr0), dsr=float(st.norm.cdf(z)), psr0=float(st.norm.cdf(sr_best * np.sqrt(T - 1) / np.sqrt(1 - skew * sr_best + (kurt - 1) / 4 * sr_best ** 2))))
