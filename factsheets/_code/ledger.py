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
from battery import DIRECTION
DIRECTION_LAB = {k: v[2] for k, v in DIRECTION.items()}
from jkp_battery import bh

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results"); PLAN = os.path.join(HERE, "..", "planning")
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
    if os.path.exists(os.path.join(RES, "fund_battery.json")):
        FB = json.load(open(os.path.join(RES, "fund_battery.json")))
        for s, v in FB["stats"].items():
            for k, lab in (("t", "L/S net, US"), ("bn_t", "beta-neutral, financed, US"), ("lo_t_alpha", "long-only alpha vs EW, US")):
                R.append(dict(fs="FS13b", strategy=FB["labels"][s], kind="battery", test=lab, t=v[k], sharpe=None, months=None,
                              fund=(s, {"t": "ls_net", "bn_t": "bn_net", "lo_t_alpha": "lo_active"}[k])))
    if os.path.exists(os.path.join(RES, "fmb.json")):
        FM = json.load(open(os.path.join(RES, "fmb.json")))
        for u in U:
            if FM[u]["multi"]:
                for s, v in FM[u]["multi"].items():
                    R.append(dict(fs="FS13c", strategy=FM["labels"][s], kind="fama-macbeth", test=f"multivariate slope, {UN[u]}", t=v["t"], sharpe=None, months=None))
        for s, v in FM["pooled"].items():
            R.append(dict(fs="FS13c", strategy=FM["labels"][s], kind="fama-macbeth", test="multivariate slope, market average", t=v["t"], sharpe=None, months=None))
    if os.path.exists(os.path.join(RES, "fs14.json")):
        F14 = json.load(open(os.path.join(RES, "fs14.json")))
        for u in U:
            for v in F14["variants"]:
                R.append(dict(fs="FS14", strategy=f"Multifactor {v}", kind="multifactor", test=f"net return vs zero, {UN[u]}", t=F14[u][v]["t"], sharpe=F14[u][v]["sharpe"], months=F14[u][v]["months"]))
        R.append(dict(fs="FS14", strategy="Multifactor RP (primary)", kind="multifactor", test="RP minus ALL-EQ, 5-market average (pre-registered primary test)", t=F14["primary"]["t"], sharpe=None, months=None))
        for v, x in F14["vs_alleq"].items():
            R.append(dict(fs="FS14", strategy=f"Multifactor {v}", kind="multifactor", test="minus ALL-EQ, 5-market average", t=x["t"], sharpe=None, months=None))
    if os.path.exists(os.path.join(RES, "art_fs14.json")):
        AB = json.load(open(os.path.join(RES, "art_battery.json")))["pooled"]; AF = json.load(open(os.path.join(RES, "art_fmb.json"))); AM = json.load(open(os.path.join(RES, "art_fs14.json")))
        AN = {"US_A": "US", "EU_A": "EU", "UK_A": "UK", "DK_A": "DK", "WD_A": "World"}
        for s, v in AB.items():
            for k, lab in (("raw", "L/S net"), ("bn", "beta-neutral, financed")):
                R.append(dict(fs="FS15", strategy=DIRECTION_LAB.get(s, s), kind="history 1998-2013", test=f"{lab}, 4-market average, 1999-2013", t=v[k]["t"], sharpe=v[k]["sharpe"], months=None))
        for u in AN:
            if AF[u]["multi"]:
                for s, v in AF[u]["multi"].items():
                    R.append(dict(fs="FS15", strategy=DIRECTION_LAB.get(s, s), kind="history 1998-2013", test=f"Fama-MacBeth slope, {AN[u]}, 1999-2013", t=v["t"], sharpe=None, months=None))
        for s, v in AF["pooled"].items():
            R.append(dict(fs="FS15", strategy=DIRECTION_LAB.get(s, s), kind="history 1998-2013", test="Fama-MacBeth slope, market average, 1999-2013", t=v["t"], sharpe=None, months=None))
        for u in AN:
            for v in AM["variants"]:
                R.append(dict(fs="FS15", strategy=f"Multifactor {v}", kind="history 1998-2013", test=f"net return vs zero, {AN[u]}, 2002-2013", t=AM[u][v]["t"], sharpe=AM[u][v]["sharpe"], months=None))
        R.append(dict(fs="FS15", strategy="Multifactor RP (primary)", kind="history 1998-2013", test="RP minus ALL-EQ, 4-market average, 2002-2013 (pre-registered)", t=AM["primary"]["t"], sharpe=None, months=None))
        if "short_vs_alleq" in AM:
            R.append(dict(fs="FS15", strategy="Fixed shortlist (low beta + momentum)", kind="history 1998-2013", test="SHORT minus ALL-EQ, 4-market average, 2002-2013", t=AM["short_vs_alleq"]["t"], sharpe=None, months=None))
            R.append(dict(fs="FS15", strategy="Fixed shortlist (low beta + momentum)", kind="history 1998-2013", test="net return vs zero, 4-market average, 2002-2013", t=AM["pooled"]["SHORT"]["t"], sharpe=AM["pooled"]["SHORT"]["sharpe"], months=None))
        for v, x in AM["vs_alleq"].items():
            R.append(dict(fs="FS15", strategy=f"Multifactor {v}", kind="history 1998-2013", test="minus ALL-EQ, 4-market average, 2002-2013", t=x["t"], sharpe=None, months=None))
    if os.path.exists(os.path.join(RES, "fs17.json")):
        F7 = json.load(open(os.path.join(RES, "fs17.json")))
        for per, lab in (("B", "2013-2025, JKP"), ("A", "1999-2013, ART")):
            for mk, v in F7[per]["markets"].items():
                for t, x in v["themes"].items():
                    R.append(dict(fs="FS17", strategy=("Fundamental pair" if t == "pair" else t), kind="fundamentals outside the US", test=f"alpha on the shortlist, {F7['names'][mk]}, {lab}", t=x["t"], sharpe=None, months=None))
                R.append(dict(fs="FS17", strategy="Shortlist + fundamental pair", kind="fundamentals outside the US", test=f"minus shortlist, {F7['names'][mk]}, {lab}", t=v["diff_t"], sharpe=None, months=None))
            R.append(dict(fs="FS17", strategy="Fundamental pair (primary)", kind="fundamentals outside the US", test=f"alpha on the shortlist, non-US average, {lab} (pre-registered)", t=F7[per]["pooled"]["t"], sharpe=None, months=None))
            for t, x in F7[per]["pooled_themes"].items():
                R.append(dict(fs="FS17", strategy=t, kind="fundamentals outside the US", test=f"alpha on the shortlist, non-US average, {lab}", t=x["t"], sharpe=None, months=None))
    if os.path.exists(os.path.join(RES, "fs18.json")):
        F8 = json.load(open(os.path.join(RES, "fs18.json")))
        for K, lab in (("5e+07", "$50m per book"), ("2e+08", "$250m per book")):
            for mk, v in F8["markets"].items():
                o = v[K]["overlay"]
                R.append(dict(fs="FS18", strategy="Market + overlay", kind="portfolio", test=f"overlay return, {mk}, {lab}", t=o["t"], sharpe=o["sharpe"], months=v[K]["n"]))
            R.append(dict(fs="FS18", strategy="Market + overlay" + (" (primary)" if K == "5e+07" else ""), kind="portfolio", test=f"overlay return, 5-market average, {lab}" + (" (pre-registered)" if K == "5e+07" else ""), t=F8[f"pooled_{K}"]["t"], sharpe=F8[f"pooled_{K}"]["sharpe"], months=None))
    if os.path.exists(os.path.join(RES, "fs19.json")):
        F9 = json.load(open(os.path.join(RES, "fs19.json")))
        for mk, v in F9["C"]["markets"].items():
            for b in ("low beta", "12-1 momentum", "shortlist"):
                R.append(dict(fs="FS19", strategy=f"{b} (within sectors)", kind="robustness", test=f"net return, {mk}", t=v[f"{b} | sector-neutral"]["t"], sharpe=v[f"{b} | sector-neutral"]["sharpe"], months=None))
                R.append(dict(fs="FS19", strategy=f"{b} (within sectors)", kind="robustness", test=f"minus unrestricted, {mk}", t=v[f"{b} | difference"]["t"], sharpe=None, months=None))
        R.append(dict(fs="FS19", strategy="Shortlist within sectors (primary)", kind="robustness", test="net return, 5-market average (pre-registered)", t=F9["C"]["pooled | sector-neutral"]["t"], sharpe=F9["C"]["pooled | sector-neutral"]["sharpe"], months=None))
        for k, v in F9["B"]["dm"].items():
            if v["bear_months"] >= 12:
                R.append(dict(fs="FS19", strategy="Momentum crash (bear x market)", kind="robustness", test=f"Daniel-Moskowitz, {k}", t=v["t_bear_mkt"], sharpe=None, months=v["n"]))
    if os.path.exists(os.path.join(RES, "fs20.json")):
        F20 = json.load(open(os.path.join(RES, "fs20.json")))
        for k, v in F20["variants"].items():
            prim = k == F20["primary"]
            R.append(dict(fs="FS20", strategy="Checklist proxy" + (" (primary)" if prim else ""), kind="fundamental", test=f"CAPM alpha, US, {v['N']} stocks, {v['freq']}, {v['rank']}" + (" (pre-registered)" if prim else ""), t=v["capm"]["t"], sharpe=v["sharpe_ex"], months=v["capm"]["n"]))
    if os.path.exists(os.path.join(RES, "fs21.json")):
        F21 = json.load(open(os.path.join(RES, "fs21.json")))
        from scipy import stats as _st
        for k, lab in (("T1", "HRP minus equal weight"), ("T2", "HRP minus inverse variance")):
            v = F21[k]; tt = float(_st.norm.ppf(1 - v["p_gt"])) if 0 < v["p_gt"] < 1 else 0.0
            R.append(dict(fs="FS21", strategy="Hierarchical risk parity (primary)", kind="portfolio", test=f"{lab}, pooled Sharpe, 5 markets (pre-registered)", t=tt, sharpe=None, months=v["months"]))
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
    if isinstance(r.get("fund"), tuple):
        s, col = r["fund"]; df = pd.read_pickle(os.path.join(RES, "fund_battery.pkl"))[s]
        if col == "lo_active":
            x = df.lo_net.dropna(); ew = df.ew.reindex(x.index); beta = float(np.cov(x, ew)[0, 1] / np.var(ew, ddof=1)); return x - beta * ew
        return df[col].dropna()
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
    cand = D[(D.t > 0) & D.apply(lambda r: isinstance(r.get("series"), tuple) or isinstance(r.get("pooled"), tuple) or isinstance(r.get("fund"), tuple), axis=1)].sort_values("t", ascending=False).head(6)
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

**Trials: {O['n']}**: primary cells (6 markets × L/S and long-only per strategy), fix-ladder holdout tests, the FS13 battery (19 signals × raw/beta-neutral) the FS13b US fundamental battery (20 signals × raw, beta-neutral and long-only) the FS13c Fama-MacBeth slopes (multivariate, per market and averaged) the pre-registered FS14 multifactor tests the FS15 re-run on 1998–2013 the FS17 factor-level tests of non-US fundamentals the FS18 portfolio overlay, the FS19 robustness tests the FS20 checklist proxy and the FS21 portfolio-construction tests. The 153 JKP factors in FS13 are published factors, tested there with their own correction, and not counted here.

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
