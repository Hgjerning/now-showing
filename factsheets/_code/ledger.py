# -*- coding: utf-8 -*-
"""Programme trial ledger for the factsheets (FS01-FS13): every gated test in one table, with programme-wide
Bonferroni, Benjamini-Hochberg and a deflated Sharpe ratio (Bailey & Lopez de Prado 2014) for the best candidates.
Writes results/trial_ledger.csv, results/trial_ledger.json and planning/FACTSHEET_TRIAL_LEDGER.md."""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats as sst

import specs
from jkp_battery import bh

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); PLAN = os.path.join(HERE, "..", "planning")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
p2 = lambda t: float(2 * (1 - sst.norm.cdf(abs(t))))


def rows():
    R = []
    T = json.load(open(os.path.join(RES, "turtle_summary.json"))); L = json.load(open(os.path.join(RES, "lottery_summary.json")))
    F = json.load(open(os.path.join(RES, "fix_summary.json")))
    for u in U:
        s = T[u]["stats"]
        R.append(dict(fs="FS01", strategy="Turtle Traders", kind="primary", test=f"L/S net mean, {UN[u]}", t=s["Turtle L/S (S1+S2)"]["t_mean"], sharpe=s["Turtle L/S (S1+S2)"]["sharpe"], months=None))
        R.append(dict(fs="FS01", strategy="Turtle Traders", kind="primary", test=f"long-only alpha vs EW, {UN[u]}", t=s["Turtle long-only (S1+S2)"]["t_alpha"], sharpe=s["Turtle long-only (S1+S2)"]["sharpe"], months=None))
        s = L[u]["stats"]
        R.append(dict(fs="FS02", strategy="Lottery (MAX)", kind="primary", test=f"L/S net mean, {UN[u]}", t=s["L/S low minus high MAX (net)"]["t_mean"], sharpe=s["L/S low minus high MAX (net)"]["sharpe"], months=None))
        R.append(dict(fs="FS02", strategy="Lottery (MAX)", kind="primary", test=f"long-only alpha vs EW, {UN[u]}", t=s["Low-MAX long-only (net)"]["t_alpha"], sharpe=s["Low-MAX long-only (net)"]["sharpe"], months=None))
    for key, fs, name in (("turtle", "FS01", "Turtle Traders"), ("lottery", "FS02", "Lottery (MAX)")):
        for step, v in F[key]["pooled"].items():
            if "vs_previous_holdout" in v:
                w = v["vs_previous_holdout"]; lab = f"{step} vs previous step, pooled holdout Sharpe"
            elif "p" in v:
                w = v; lab = step.replace("_", " ") + " (pooled Sharpe difference)"
            else:
                R.append(dict(fs=fs, strategy=name, kind="fix (holdout)", test=step.replace("_", " "), t=v["t"], sharpe=None, months=None)); continue
            p = max(w["p"], 1e-6)
            R.append(dict(fs=fs, strategy=name, kind="fix (holdout)", test=lab, t=float(sst.norm.ppf(1 - p / 2)) * np.sign(w["diff"]), p=p, sharpe=None, months=None))
    for code in specs.ORDER:
        J = json.load(open(os.path.join(RES, f"xs_{code}.json"))); nm = specs.S[code]["title"]
        for u in U:
            s = J["per"][u]["stats"]
            R.append(dict(fs=code, strategy=nm, kind="primary", test=f"L/S net mean, {UN[u]}", t=s["L/S (net)"]["t_mean"], sharpe=s["L/S (net)"]["sharpe"], months=s["L/S (net)"]["months"], series=(code, u, "L/S (net)")))
            R.append(dict(fs=code, strategy=nm, kind="primary", test=f"long-only alpha vs EW, {UN[u]}", t=s["Long-only (net)"]["t_alpha"], sharpe=s["Long-only (net)"]["sharpe"], months=s["Long-only (net)"]["months"], series=(code, u, "Long-only (net)")))
        for step, v in J["pooled"].items():
            p = max(v["holdout"]["p"], 1e-6)
            R.append(dict(fs=code, strategy=nm, kind="fix (holdout)", test=f"{step} vs previous step, pooled holdout Sharpe", t=float(sst.norm.ppf(1 - p / 2)) * np.sign(v["holdout"]["diff"]), p=p, sharpe=None, months=None))
    O = json.load(open(os.path.join(RES, "common_ground.json")))
    for s, v in O["price"].items():
        for k, lab in (("raw", "L/S net"), ("bn", "beta-neutral, financed")):
            R.append(dict(fs="FS13", strategy=v["label"], kind="battery", test=f"{lab}, 6-market average", t=v[k]["t"], sharpe=v[k]["sharpe"], months=None, pooled=(s, k)))
    D = pd.DataFrame(R)
    D["p"] = D.apply(lambda r: r["p"] if "p" in r and pd.notna(r.get("p")) else p2(r["t"]), axis=1)
    return D


def dsr(x, n_trials, var_sr):
    """Deflated Sharpe ratio (per-period Sharpe). x: return series."""
    x = pd.Series(x).dropna(); T = len(x); sr = x.mean() / x.std()
    g3 = float(sst.skew(x)); g4 = float(sst.kurtosis(x, fisher=False)); em = 0.5772156649
    sr0 = np.sqrt(var_sr) * ((1 - em) * sst.norm.ppf(1 - 1 / n_trials) + em * sst.norm.ppf(1 - 1 / (n_trials * np.e)))
    z = (sr - sr0) * np.sqrt(T - 1) / np.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr ** 2)
    return dict(sr_ann=float(sr * np.sqrt(12)), sr0_ann=float(sr0 * np.sqrt(12)), dsr=float(sst.norm.cdf(z)), T=T, skew=g3, kurt=g4)


def series_of(r):
    if isinstance(r.get("series"), tuple):
        code, u, b = r["series"]; P = pd.read_pickle(os.path.join(RES, f"xs_{code}.pkl"))
        x = P[u]["books"][b].dropna()
        if b.startswith("Long-only"):     # the test is alpha vs the EW universe: use the beta-adjusted active return
            ew = P[u]["books"]["EW universe"].reindex(x.index)
            beta = float(np.cov(x, ew)[0, 1] / np.var(ew, ddof=1)); x = x - beta * ew
        return x
    if isinstance(r.get("pooled"), tuple):
        s, k = r["pooled"]; B = pd.read_pickle(os.path.join(RES, "battery_price.pkl"))
        col = "ls_net" if k == "raw" else "bn_net"
        df = pd.DataFrame({u: B[u][s][col] for u in U}).dropna()
        return df.mean(axis=1)
    return None


def build():
    D = rows(); n = len(D)
    D["bonferroni"] = D.p < 0.05 / n; D["bh"] = bh(D.p.values)
    zb = float(sst.norm.ppf(1 - 0.025 / n))
    own = D[D.kind != "fix (holdout)"]
    # variance of per-period (monthly) Sharpe across trials, estimated as t / sqrt(T) with T = 163 months
    sr_m = own.t / np.sqrt(163); var_sr = float(sr_m.var())
    cand = D[(D.t > 0) & D.apply(lambda r: isinstance(r.get("series"), tuple) or isinstance(r.get("pooled"), tuple), axis=1)].sort_values("t", ascending=False).head(6)
    DS = []
    for _, r in cand.iterrows():
        x = series_of(r)
        if x is not None:
            d0 = dsr(x, n, 1 / len(x.dropna()))
            DS.append(dict(fs=r.fs, strategy=r.strategy, test=r.test, t=float(r.t), **dsr(x, n, var_sr), sr0_null_ann=d0["sr0_ann"], dsr_null=d0["dsr"]))
    by = D.groupby("fs").agg(trials=("t", "size"), local_pass=("t", lambda t: int((t.abs() > 2.87).sum())), bonf=("bonferroni", "sum"), bh=("bh", "sum")).reset_index()
    keep = ["fs", "strategy", "kind", "test", "t", "p", "sharpe", "bonferroni", "bh"]
    D[keep].to_csv(os.path.join(RES, "trial_ledger.csv"), index=False)
    pos = D[(D.bh | D.bonferroni) & (D.t > 0)]; neg = D[(D.bh | D.bonferroni) & (D.t < 0)]
    out = dict(n=n, z_bonf=zb, var_sr_month=var_sr, by=by.to_dict("records"), dsr=DS, n_pos=int(len(pos)), n_neg=int(len(neg)),
               n_pos_bonf=int((pos.bonferroni).sum()), pos_list=[f"{r.strategy}: {r.test}" for r in pos.itertuples()],
               passes=D[D.bh | D.bonferroni][keep].to_dict("records"), n_own=int((D.kind != "battery").sum()), n_battery=int((D.kind == "battery").sum()))
    json.dump(out, open(os.path.join(RES, "trial_ledger.json"), "w"), indent=1, default=float)
    md(D, out)
    return D, out


def md(D, O):
    t = lambda h, rows: "| " + " | ".join(h) + " |\n|" + "|".join(["---"] * len(h)) + "|\n" + "".join("| " + " | ".join(str(x) for x in r) + " |\n" for r in rows)
    by = [[b["fs"], b["trials"], b["local_pass"], b["bonf"], b["bh"]] for b in O["by"]]
    ps = [[r["fs"], r["strategy"], r["test"], f"{r['t']:+.2f}", f"{r['p']:.4f}", "✓" if r["bonferroni"] else "", "✓" if r["bh"] else ""] for r in O["passes"]]
    ds = [[d["fs"], d["strategy"], d["test"], f"{d['t']:+.2f}", f"{d['sr_ann']:.2f}", f"{d['sr0_ann']:.2f}", f"{d['dsr']:.2f}", f"{d['sr0_null_ann']:.2f}", f"{d['dsr_null']:.2f}"] for d in O["dsr"]]
    txt = f"""# Factsheet trial ledger (FS01–FS13)

Built {pd.Timestamp.today().date()} by `code/ledger.py` from the results files; re-run after every rebuild. This ledger is separate from the article programme's `TRIAL_LEDGER.md` files (which count pre-registered hypotheses); here every gated cell of every factsheet is a trial.

**Trials: {O['n']}**: primary cells (6 markets × L/S and long-only per strategy), fix-ladder holdout tests, and the FS13 battery (19 signals × raw/beta-neutral). The 153 JKP factors in FS13 are published factors, tested there with their own correction, and not counted here.

Programme-wide bars: Bonferroni at 5% over {O['n']} trials needs |t| > {O['z_bonf']:.2f}; Benjamini–Hochberg at 5% controls the false-discovery rate instead.

## Trials per factsheet

{t(["Factsheet", "Trials", "Passed the factsheet's own gate (|t| > 2.87)", "Pass programme Bonferroni", "Pass programme BH"], by)}

## What survives the programme-wide correction

{O['n_pos'] + O['n_neg']} of {O['n']} trials survive Benjamini–Hochberg: **{O['n_pos']} positive** ({O['n_pos_bonf']} also Bonferroni) and {O['n_neg']} negative. Every positive survivor is a long-only book beating its own equal-weight universe after beta, a single-market long/short, or a fix step; no pooled price signal in FS13 survives on the positive side.

{t(["Factsheet", "Strategy", "Test", "t", "p", "Bonferroni", "BH"], ps) if ps else "Nothing."}

*Negative t = significantly worse than zero (a strategy that reliably loses).*

## Deflated Sharpe ratio of the best positive candidates

The deflated Sharpe ratio (Bailey & López de Prado 2014) asks how likely the best Sharpe is to be real given {O['n']} trials, the spread of Sharpe ratios across them (estimated as t/√T) and the candidate's skewness and fat tails. For long-only tests the Sharpe is that of the beta-adjusted return over the equal-weight universe, which is what the test measures. SR₀ is the Sharpe ratio the best of {O['n']} worthless strategies would show by luck. DSR > 0.95 is the usual bar.

{t(["Factsheet", "Strategy", "Test", "t", "Sharpe (annual)", "SR₀, observed spread", "DSR, observed spread", "SR₀, null spread", "DSR, null spread"], ds)}

*Two versions of SR₀. "Observed spread" uses the dispersion of all {O['n']} trials, which is wide because many trials measure strategies that reliably lose; it is conservative. "Null spread" assumes every trial is noise (variance 1/T); it is the lenient bound. The truth lies between: a candidate that fails the lenient bound is not credible, one that passes only the lenient bound is promising but unproven.*

## Rules from now on

1. Every new factsheet adds its gated cells here before its results are written up.
2. The multifactor battery (FS14) is pre-registered: filters, correlation cut-off, windows and weights are fixed in writing before the run, and its selection counts as trials in this ledger.
3. Headline claims in posts use the programme-wide result, not only the factsheet's own gate.
"""
    open(os.path.join(PLAN, "FACTSHEET_TRIAL_LEDGER.md"), "w").write(txt)


if __name__ == "__main__":
    D, O = build()
    print(O["n"], O["z_bonf"]); print(pd.DataFrame(O["by"])); print(pd.DataFrame(O["passes"])); print(pd.DataFrame(O["dsr"]))
