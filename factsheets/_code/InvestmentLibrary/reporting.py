"""
InvestmentLibrary.reporting
=============================
ONE standard reporting call for the Templates/ notebooks, replacing the
`pd.DataFrame({name: il.backtest.performance_report(...) for name in ...})`
pattern used across most of the 83 numbered Templates notebooks (87/94 already
call `performance_report` at least once). Built 2026-08-27 directly from:
"streamline the reporting for the main project[,] the 83 workbooks."

`performance_report()` already gives CAGR/Vol/Sharpe/Max Drawdown/Hit Rate as
one printed row. `generate_standard_report()` adds what notebooks were
otherwise hand-rolling every time they wanted more than that single row:
equity curves, drawdown curves, Sortino/Calmar (both already in
stats.py/risk.py, just not wired into performance_report), and turnover-based
PnL stats -- as one call that both plots and returns the underlying data.

Generalises "strategy vs benchmark" (2 series) and "N-way variant comparison"
(the pattern already used in e.g. Templates/1.0, /22.0, /23.0, /33.0) as the
same shape: a name -> net-return-series mapping. Pass
{"Strategy": bt["net_returns"], "Benchmark": spy_returns} for the former, or
{"TSMOM": bt_tsmom["net_returns"], "CSMOM": bt_csmom["net_returns"]} for the
latter -- no special-casing needed either way.

Deliberate adaptation from a discrete "trade sheet" (entry/exit pairs) to
turnover-based PnL stats: backtest.py's engine is a continuous, multi-asset
target-WEIGHT vectorized backtester, not a discrete per-instrument signal
engine -- a single "trade" isn't a well-defined concept for, say, an HRP or
risk-parity weight vector that rebalances fractionally every period. Turnover
(and the transaction cost it implies) is the equivalent unit of trading
activity here, so "trade stats" becomes "turnover/PnL stats": average and
total turnover, rebalance count, and average turnover per rebalance.

Metric names deliberately match `backtest.performance_report()`'s own naming
(CAGR / Annualized Vol / Sharpe / Max Drawdown / Hit Rate / Periods), not
`risk.summary_stats()`'s naming ("Annualized Return" / "Sharpe Ratio" / ...),
specifically so a row of this function's `metrics` can be passed straight into
`experiments.log_experiment(performance=metrics.loc[name])` with no renaming --
Sortino and Calmar are simply extra columns log_experiment doesn't look for
and ignores.

`save_report()`/`load_all_reports()` (added 2026-08-28) persist every workbook's
`generate_standard_report()` output to one CSV, for the concluding roll-up
workbook over all 87 Templates notebooks -- see their own docstrings for how
this differs from (and complements) `experiments.py`'s hand-curated registry.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .stats import annualize_rets, annualize_vol, sharpe_ratio, sortino_ratio, calmar_ratio
from .risk import drawdown


def generate_standard_report(
    returns: dict[str, pd.Series],
    periods_per_year: int = 252,
    riskfree_rate: float = 0.0,
    turnover: dict[str, pd.Series] | None = None,
    title: str = "Strategy Comparison",
    show_plots: bool = True,
) -> dict:
    """
    returns: {name: net_return_series}. Series need NOT share a common start
        date -- each name's metrics/equity/drawdown are computed on that
        name's own history (via .dropna()), never padded with fake 0% returns
        for periods before it existed. A shorter-history name's CAGR/vol is
        therefore never diluted by years it wasn't actually running, and the
        equity/drawdown plots simply start each line where its own data
        starts rather than showing a misleading flat run-up to 1.0.
    turnover: optional {name: turnover_series} (bt["turnover"] from
        backtest_weights) for names that have one. A name with no entry here
        (e.g. a raw benchmark return series with no associated backtest) is
        just skipped in the turnover table, not an error.
    title: used in plot titles only.
    show_plots: set False to compute silently (e.g. inside a parameter sweep
        or when logging many configurations in a loop) -- the returned dict
        is identical either way.

    Returns {"equity", "drawdown", "metrics", "turnover_stats"} -- every value
    is real data (a DataFrame, not just a printed table), so this composes
    with experiments.log_experiment() (pass metrics.loc[name] as its
    `performance` argument) instead of only being human-readable output.
    """
    if not returns:
        raise ValueError("returns must have at least one entry")

    clean = {name: r.dropna() for name, r in returns.items()}
    for name, r in clean.items():
        if r.empty:
            raise ValueError(f"'{name}' has no non-NaN observations")

    combined_index = pd.Index(sorted(set().union(*(r.index for r in clean.values()))))

    equity = pd.DataFrame({
        name: (1 + r).cumprod().reindex(combined_index) for name, r in clean.items()
    })
    dd = pd.DataFrame({
        name: drawdown(r)["Drawdown"].reindex(combined_index) for name, r in clean.items()
    })

    rows = {}
    for name, r in clean.items():
        rows[name] = {
            "CAGR": annualize_rets(r, periods_per_year),
            "Annualized Vol": annualize_vol(r, periods_per_year),
            "Sharpe": sharpe_ratio(r, riskfree_rate, periods_per_year),
            "Sortino": sortino_ratio(r, riskfree_rate, periods_per_year),
            "Calmar": calmar_ratio(r, periods_per_year),
            "Max Drawdown": drawdown(r)["Drawdown"].min(),
            "Hit Rate": (r > 0).mean(),
            "Periods": len(r),
        }
    metrics = pd.DataFrame(rows).T

    turnover_stats = None
    if turnover:
        t_rows = {}
        for name, t in turnover.items():
            if t is None or len(t) == 0:
                continue
            active = t[t > 0]
            t_rows[name] = {
                "Avg Turnover": t.mean(),
                "Total Turnover": t.sum(),
                "Rebalances (>0 turnover)": int((t > 0).sum()),
                "Avg Turnover per Rebalance": active.mean() if len(active) else float("nan"),
            }
        if t_rows:
            turnover_stats = pd.DataFrame(t_rows).T

    if show_plots:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 5))
        equity.plot(ax=ax)
        ax.set_title(f"{title}: Equity Curve")
        ax.set_ylabel("Cumulative Return (1.0 = each series' own start)")
        plt.show()

        fig, ax = plt.subplots(figsize=(12, 4))
        dd.plot(ax=ax)
        ax.set_title(f"{title}: Drawdown")
        ax.set_ylabel("Drawdown")
        plt.show()

        display_metrics = metrics.copy()
        pct_cols = [c for c in display_metrics.columns
                    if any(k in c for k in ("CAGR", "Vol", "Drawdown", "Hit Rate"))]
        for c in pct_cols:
            display_metrics[c] = display_metrics[c].map(lambda v: f"{v:.2%}" if pd.notna(v) else "n/a")
        print("Performance Metrics:")
        print(display_metrics.T)

        if turnover_stats is not None:
            print("\nTurnover / PnL Stats:")
            print(turnover_stats)

    return {"equity": equity, "drawdown": dd, "metrics": metrics, "turnover_stats": turnover_stats}


# ---------------------------------------------------------------------------------------------
# Save / load, for the concluding roll-up workbook -- added 2026-08-28 directly from "build the
# concluding roll up book over all 87". Deliberately separate from experiments.py's registry:
# that one is a hand-curated, dimension-tagged log of specific test configurations someone chose
# to record (universe/selection_method/tilt/...), populated by explicit log_experiment() calls in
# a subset of notebooks. This is the opposite -- a blanket, mechanical capture of every single
# generate_standard_report() call across all 87 notebooks, keyed only by (Workbook, Strategy), no
# manual tagging required. The two are complementary, not overlapping: log_experiment for
# considered findings worth annotating, save_report for "what did every notebook actually show".
# ---------------------------------------------------------------------------------------------

def save_report(report: dict, name: str, out_dir: str | Path = "Reports") -> Path:
    """
    Persist one workbook's generate_standard_report() output to <out_dir>/_all_metrics.csv.

    A single notebook's report often covers several named strategies at once (the N-way
    comparison shape -- e.g. Templates/45.0 has 8), so each row of `report["metrics"]` becomes
    its OWN row here, tagged with both `name` (the workbook) and that row's own strategy name --
    never collapsed to one row per notebook. Calling this again for the same `name` replaces
    that workbook's previous rows (by exact Workbook match) rather than duplicating them, so
    re-running a notebook after a fix doesn't leave stale rows behind.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics_rows = report["metrics"].copy()
    metrics_rows.insert(0, "Workbook", name)
    metrics_rows.insert(1, "Strategy", metrics_rows.index)
    metrics_rows = metrics_rows.reset_index(drop=True)

    metrics_path = out_dir / "_all_metrics.csv"
    if metrics_path.exists():
        existing = pd.read_csv(metrics_path)
        existing = existing[existing["Workbook"] != name]  # replace a prior run of this workbook
        metrics_rows = pd.concat([existing, metrics_rows], ignore_index=True)
    metrics_rows.to_csv(metrics_path, index=False)

    return metrics_path


def load_all_reports(out_dir: str | Path = "Reports") -> pd.DataFrame:
    """Read back every workbook's saved metrics (see save_report) as one comparison table --
    one row per (Workbook, Strategy) pair, every metric as a column. Empty DataFrame, not an
    error, if nothing has been saved yet."""
    path = Path(out_dir) / "_all_metrics.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)
