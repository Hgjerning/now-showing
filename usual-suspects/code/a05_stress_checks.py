# -*- coding: utf-8 -*-
"""A05, added after the stress test of 23 Oct 2026: REPORTED, NOT GATED (no trial spent). Writes ../results/a05_stress.json.

1. Structure-preserving fake-guru placebo. The real 16 recipes share legs (ni_me in 4, qmj in 2, ...), so a panel of 16
   independent fakes understates how much the pass count can vary. Here each panel maps each of the 27 distinct base legs
   to a different random factor from the same 153-factor pool and rebuilds all 16 recipes with the real overlaps.
   Variant A: every leg in its published direction. Variant B: the real recipes' signs (e.g. -debt_me) applied to the
   mapped factor. Same A05-1 procedure as fake_gurus.test(). 1,000 panels per variant, seeds 5051 and 5052.
2. Newey-West lag sensitivity of the real pass count (0, 3, 6, 12, 24 lags).
3. Medians for the 11 non-passing recipes; prediction scorecard; developed-markets sample window."""
import json, os, sys, time
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from run_suspects import RECIPES, FAC, GATE_T, D, OUT, recipe, nw_ols  # noqa: E402
import fake_gurus as fg  # noqa: E402  (loads fus, fac; test())

T0 = time.time(); X = {}; NP = 1000
real = pd.read_csv(os.path.join(OUT, "suspects_us.csv"), index_col=0); real["pass"] = real["pass"].astype(str) == "True"
pool = [c for c in fg.fus.columns if fg.fus.loc["1963-07":"2025-12", c].notna().sum() >= 600]
bases = sorted({l.lstrip("-") for v in RECIPES.values() for l in v})
X["n_base_legs"] = len(bases); X["pool"] = len(pool)
leg_use = pd.Series([l.lstrip("-") for v in RECIPES.values() for l in v]).value_counts()
X["shared_legs"] = {k: int(v) for k, v in leg_use.items() if v > 1}
for var, seed in (("published_direction", 5051), ("real_signs", 5052)):
    rng = np.random.default_rng(seed); counts = []
    for _ in range(NP):
        mp = dict(zip(bases, rng.choice(pool, size=len(bases), replace=False)))
        n = 0
        for legs in RECIPES.values():
            cols = [(-1.0 if (var == "real_signs" and l.startswith("-")) else 1.0) * fg.fus[mp[l.lstrip("-")]] for l in legs]
            x = fg.test(pd.concat(cols, axis=1).dropna().mean(axis=1))
            n += int(bool(x and x["passed"]))
        counts.append(n)
    c = np.array(counts)
    X[f"placebo_{var}"] = {"panels": NP, "mean": float(c.mean()), "sd": float(c.std(ddof=1)), "q05": float(np.quantile(c, 0.05)),
                           "q95": float(np.quantile(c, 0.95)), "p_le_5": float((c <= 5).mean()), "mc_se_p": float(np.sqrt((c <= 5).mean() * (1 - (c <= 5).mean()) / NP))}
FG = json.load(open(os.path.join(OUT, "fake_gurus.json")))
X["independent_placebo_mc_se_p"] = float(np.sqrt(FG["p_le_real"] * (1 - FG["p_le_real"]) / FG["panels"]))
# 2. NW lag sensitivity
fac = fg.fac
lag_rows = {}
for L in (0, 3, 6, 12, 24):
    n = 0; tt = {}
    for name, legs in RECIPES.items():
        r = recipe(fg.fus, legs); r.index = r.index.to_period("M").to_timestamp("M")
        df = pd.concat([r.rename("r"), fac[FAC]], axis=1, join="inner").dropna().loc[:"2025-12-31"]
        b, t, _ = nw_ols(df.r.values, df[FAC].values, lags=L); tt[name] = round(float(t[0]), 2)
        n += int(abs(t[0]) > GATE_T and np.sign(real.loc[name, "alpha_h1"]) == np.sign(real.loc[name, "alpha_h2"]))
    lag_rows[L] = {"n_pass": n, "t_Greenblatt": tt["Greenblatt"], "t_Carlisle": tt["Carlisle"]}
X["nw_lag_sensitivity"] = lag_rows
# 3. medians and scorecard
np_ = real[~real["pass"]]
X["medians_11_nonpassers"] = {"r2": float(np_.r2.median()), "abs_alpha": float(np_.alpha_ann.abs().median()), "abs_raw": float(np_.raw_ann.abs().median())}
X["medians_all_16"] = {"r2": float(real.r2.median()), "abs_alpha": float(real.alpha_ann.abs().median()), "abs_raw": float(real.raw_ann.abs().median())}
X["raw_not_significant_at_2"] = sorted(real.index[real.raw_t.abs() < 2].tolist())
smaller = (real.alpha_2012 < real.alpha_ann)
VAL = ["Graham", "Neff", "Dreman", "O'Shaughnessy value", "Carlisle", "Fisher (price/sales)"]
X["scorecard"] = {
    "R2_above_0.6_value_type_and_ONeil": {r: round(float(real.loc[r, "r2"]), 3) for r in VAL + ["O'Neil CAN SLIM"]},
    "passes_1_to_3": int(real["pass"].sum()),
    "rest_abs_alpha_below_2pct": {r: round(float(real.loc[r, "alpha_ann"]), 4) for r in np_.index if abs(real.loc[r, "alpha_ann"]) >= 0.02},
    "alpha_since_2012_smaller": {"n_smaller": int(smaller.sum()), "of": int(len(real)),
                                 "survivors_smaller": int(smaller[real["pass"]].sum()), "larger": sorted(real.index[~smaller].tolist())}}
dev = pd.read_csv(os.path.join(OUT, "suspects_developed.csv"), index_col=0)
X["developed_window"] = {"first": str(dev["first"].min()), "last": str(dev["last"].max()),
                         "by_t": dev.alpha_t.astype(float).sort_values(ascending=False).round(2).to_dict()}
X["seconds"] = round(time.time() - T0)
json.dump(X, open(os.path.join(OUT, "a05_stress.json"), "w"), indent=1, default=str)
print(json.dumps(X, indent=1, default=str)[:3500])
