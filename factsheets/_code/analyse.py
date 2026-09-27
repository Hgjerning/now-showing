# -*- coding: utf-8 -*-
"""Performance, inference, trade statistics and factor attribution for both factsheets.

Headline metrics use Project1's InvestmentLibrary (reporting.generate_standard_report, risk.var/cvar)
on daily returns, rf = 0. Inference on monthly returns: Newey-West t (6 lags), stationary-bootstrap
95% CI of the Sharpe ratio (mean block 6, 5,000 draws), probabilistic Sharpe ratio vs 0,
CAPM alpha vs the equal-weight universe, and factor attribution (JKP themes or French 5F + WML).
"""
import json
import os

import numpy as np
import pandas as pd

import data
import perf
import turtle
from InvestmentLibrary.reporting import generate_standard_report
from InvestmentLibrary.risk import cvar_historic, var_historic

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
FAC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "factors")
NAMES = {"US": "US (S&P 500 PIT)", "EU": "EU (STOXX 600 ex UK)", "UK": "UK (FTSE 350*)", "DK": "DK (C25)", "SC": "SCANDI (Nordic STOXX 600)", "WD": "WD (World)"}
END_M = "2026-08-31"
GATE_T = 2.87          # Bonferroni: 12 cells (6 universes x 2 strategies), two-sided 0.05/12

# ---------- factor sets ----------
def _jkp(c):
    f = pd.read_csv(os.path.join(FAC, f"jkp_{c}_themes_daily.csv"), index_col=0, parse_dates=True)
    f = f[["mkt", "size", "value", "momentum", "low_risk", "quality", "short_term_reversal"]]
    return perf.to_monthly(f.loc["2012":])


def _french(c):
    f = pd.read_csv(os.path.join(FAC, f"french_{c}_5f_daily.csv"), index_col=0, parse_dates=True)
    m = pd.read_csv(os.path.join(FAC, f"french_{c}_mom_daily.csv"), index_col=0, parse_dates=True)
    f = f.join(m).drop(columns=["RF"]).loc["2012":]
    return perf.to_monthly(f)


FACTORS = {"US": ("JKP USA 7 themes", lambda: _jkp("usa")), "UK": ("JKP GBR 7 themes", lambda: _jkp("gbr")),
           "DK": ("JKP DNK 7 themes", lambda: _jkp("dnk")), "WD": ("JKP World 7 themes", lambda: _jkp("world")),
           "EU": ("French Europe 5F + WML", lambda: _french("europe")), "SC": ("French Europe 5F + WML", lambda: _french("europe"))}


def attribution(m, R):
    label, fn = FACTORS[R]
    F = fn(); d = pd.concat([m.rename("y"), F], axis=1, join="inner").dropna()
    y = d.y.values; X = d.drop(columns="y").values
    Xc = np.column_stack([np.ones(len(y)), X]); b = np.linalg.lstsq(Xc, y, rcond=None)[0]; u = y - Xc @ b
    n = len(y); XtXi = np.linalg.inv(Xc.T @ Xc); Xu = Xc * u[:, None]; S = Xu.T @ Xu / n
    for L in range(1, 7):
        G = Xu[L:].T @ Xu[:-L] / n; S += (1 - L / 7) * (G + G.T)
    se = np.sqrt(np.diag(n * XtXi @ S @ XtXi)); t = b / se
    r2 = 1 - u @ u / ((y - y.mean()) @ (y - y.mean()))
    cols = ["alpha"] + list(d.columns[1:])
    return dict(model=label, months=n, end=str(d.index[-1].date()), r2=float(r2),
                coef={c: float(v * (12 if c == "alpha" else 1)) for c, v in zip(cols, b)}, t={c: float(v) for c, v in zip(cols, t)})


def metrics(daily, bench_daily=None, monthly=None, bench_m=None):
    rep = generate_standard_report({"s": daily.dropna()}, periods_per_year=252 if monthly is None else 12, show_plots=False) \
        if monthly is None else generate_standard_report({"s": monthly.dropna()}, periods_per_year=12, show_plots=False)
    il = rep["metrics"].loc["s"].to_dict()
    m = monthly if monthly is not None else perf.to_monthly(daily).loc[:END_M]
    bm = bench_m if bench_m is not None else (perf.to_monthly(bench_daily).loc[:END_M] if bench_daily is not None else None)
    s = perf.summary(m, bm)
    src = daily.dropna() if daily is not None else m
    s.update(il_cagr=float(il["CAGR"]), il_vol=float(il["Annualized Vol"]), il_sharpe=float(il["Sharpe"]), il_sortino=float(il["Sortino"]),
             il_calmar=float(il["Calmar"]), il_maxdd=float(il["Max Drawdown"]), il_hit=float(il["Hit Rate"]),
             var95=float(var_historic(src, 5)), cvar95=float(cvar_historic(src, 5)), freq="daily" if daily is not None else "monthly")
    return s


def trade_stats(tl, years):
    if len(tl) == 0:
        return {}
    w, l = tl[tl.pnl_pct > 0], tl[tl.pnl_pct <= 0]
    top = tl.sort_values("pnl_pct", ascending=False)
    pos_sum = w.pnl_pct.sum()
    return dict(n=int(len(tl)), per_year=float(len(tl) / years), win_rate=float(len(w) / len(tl)),
                avg_win=float(w.pnl_pct.mean()), avg_loss=float(l.pnl_pct.mean()), payoff=float(w.pnl_pct.mean() / -l.pnl_pct.mean()),
                profit_factor=float(pos_sum / -l.pnl_pct.sum()), expectancy_R=float(tl.R.mean()), median_R=float(tl.R.median()),
                days_win=float(w.days.mean()), days_loss=float(l.days.mean()), avg_units=float(tl.units.mean()),
                share_long=float((tl.dir == "long").mean()), pnl_long=float(tl[tl.dir == "long"].pnl_pct.sum()), pnl_short=float(tl[tl.dir == "short"].pnl_pct.sum()),
                top10_share=float(top.head(max(1, len(tl) // 10)).pnl_pct.sum() / tl.pnl_pct.sum()) if tl.pnl_pct.sum() > 0 else np.nan,
                stop_share=float((tl.reason == "2N stop").mean()))


def run_turtle_all():
    out = {}; series = {}
    for R in data.REGIONS:
        o = data.load(R); res = pd.read_pickle(os.path.join(RES, f"turtle_{R}.pkl"))
        bench = o["ret"].where(o["elig"]).mean(axis=1).loc["2013-01-01":]
        ls = 0.5 * res["S1"]["ret"] + 0.5 * res["S2"]["ret"]
        lo = 0.5 * res["S1_long"]["ret"] + 0.5 * res["S2_long"]["ret"]
        # futures-style: Turtle System 2 on the universe index as ONE market; unit 0.25% risk so 4 units ~ fully invested, 100% gross cap
        idx_r = o["ret"].where(o["elig"]).mean(axis=1).to_frame("EWINDEX")
        ix = turtle.run(idx_r, pd.DataFrame(True, index=idx_r.index, columns=idx_r.columns), system=2, risk=0.0025, gross_cap=1.0)
        books = {"Turtle L/S (S1+S2)": ls, "Turtle long-only (S1+S2)": lo, "System 1 L/S": res["S1"]["ret"], "System 2 L/S": res["S2"]["ret"],
                 "Index Turtle (S2 on EW index)": ix["ret"], "EW universe (benchmark)": bench}
        st = {k: metrics(v, bench) for k, v in books.items()}
        for k, v in books.items():
            st[k]["calendar"] = {int(y): float(x) for y, x in perf.calendar_table(v.dropna()).items()}
        yrs = (ls.index[-1] - ls.index[0]).days / 365.25
        tl = pd.concat([res["S1"]["trades"].assign(system="S1"), res["S2"]["trades"].assign(system="S2")])
        tlo = pd.concat([res["S1_long"]["trades"].assign(system="S1"), res["S2_long"]["trades"].assign(system="S2")])
        tl.to_csv(os.path.join(RES, f"turtle_trades_{R}.csv"), index=False)
        tlo.to_csv(os.path.join(RES, f"turtle_trades_longonly_{R}.csv"), index=False)
        expo = (0.5 * res["S1"]["expo"] + 0.5 * res["S2"]["expo"])
        op = pd.concat([res["S1"]["open"].assign(system="S1"), res["S2"]["open"].assign(system="S2")])
        op.to_csv(os.path.join(RES, f"turtle_open_{R}.csv"), index=False)
        out[R] = dict(name=NAMES[R], stats=st, trades=trade_stats(tl, yrs), trades_longonly=trade_stats(tlo, yrs),
                      exposure=dict(long=float(expo["long"].mean()), short=float(expo["short"].mean()), npos=float(expo["npos"].mean()),
                                    net=float((expo["long"] - expo["short"]).mean())),
                      attribution={"Turtle L/S (S1+S2)": attribution(perf.to_monthly(ls).loc[:END_M], R),
                                   "Turtle long-only (S1+S2)": attribution(perf.to_monthly(lo).loc[:END_M], R)},
                      open_positions=int(len(op)), n_names=int(o["elig"].sum(axis=1).median()))
        series[R] = pd.DataFrame(books)
        print(R, {k: round(v["sharpe"], 2) for k, v in st.items()})
    pd.to_pickle(series, os.path.join(RES, "turtle_series.pkl"))
    json.dump(out, open(os.path.join(RES, "turtle_summary.json"), "w"), indent=1, default=float)
    return out


def run_lottery_all():
    out = {}; series = {}
    for R in data.REGIONS:
        res = pd.read_pickle(os.path.join(RES, f"lottery_{R}.pkl"))
        P = res["max1"].loc["2013-02-28":END_M]; q = int(P.q.iloc[-1]); P5 = res["max5"].loc["2013-02-28":END_M]
        books = {"L/S low minus high MAX (net)": P.ls_net, "Low-MAX long-only (net)": P.low_net, f"High-MAX leg (Q{q}, gross)": P[f"Q{q}"],
                 "L/S MAX5 (net)": P5.ls_net, "EW universe (benchmark)": P.EW}
        if "max1_vw" in res:
            books["L/S value-weighted (net)"] = res["max1_vw"].loc["2013-02-28":END_M].ls_net
        st = {k: metrics(None, monthly=v, bench_m=P.EW) for k, v in books.items()}
        for k, v in books.items():
            st[k]["calendar"] = {int(y): float(x) for y, x in perf.calendar_table(v).items()}
        # leg betas vs EW
        legb = {f"Q{k}": perf.nw_ols(P[f"Q{k}"].values, P.EW.values)["beta"] for k in range(1, q + 1)}
        quant = {f"Q{k}": float(P[f"Q{k}"].mean() * 12) for k in range(1, q + 1)}
        qsh = {f"Q{k}": perf.sharpe(P[f"Q{k}"]) for k in range(1, q + 1)}
        lo, hi = res["current"]
        rec = P[["n", "max_low", "max_high", "to_low", "to_high", "Q1", f"Q{q}", "ls_gross", "ls_net"]]
        rec.to_csv(os.path.join(RES, f"lottery_monthly_record_{R}.csv"))
        # beta-hedged L/S: remove the market exposure difference ex post (diagnostic, uses full-sample beta)
        b = perf.nw_ols(P.ls_net.values, P.EW.values)
        out[R] = dict(name=NAMES[R], q=q, n_names=int(P.n.median()), stats=st, quantile_ann=quant, quantile_sharpe=qsh, quantile_beta=legb,
                      max_low=float(P.max_low.mean()), max_high=float(P.max_high.mean()), to_low=float(P.to_low.mean()), to_high=float(P.to_high.mean()),
                      cost_drag=float((P.ls_gross - P.ls_net).mean() * 12),
                      capm_ls=b, attribution={"L/S low minus high MAX (net)": attribution(P.ls_net, R), "Low-MAX long-only (net)": attribution(P.low_net, R)},
                      meme=float(P.ls_net.loc["2020-04-30":"2021-12-31"].mean() * 12),
                      current_low=[(t, float(v)) for t, v in lo.head(12).items()], current_high=[(t, float(v)) for t, v in hi.head(12).items()],
                      current_counts=(int(len(lo)), int(len(hi))))
        series[R] = pd.DataFrame(books)
        print(R, {k: round(v["sharpe"], 2) for k, v in st.items()})
    pd.to_pickle(series, os.path.join(RES, "lottery_series.pkl"))
    json.dump(out, open(os.path.join(RES, "lottery_summary.json"), "w"), indent=1, default=float)
    return out


if __name__ == "__main__":
    import sys
    if "turtle" in sys.argv: run_turtle_all()
    if "lottery" in sys.argv: run_lottery_all()
