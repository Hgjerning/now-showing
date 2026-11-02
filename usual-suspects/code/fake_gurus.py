# -*- coding: utf-8 -*-
"""A05, added 7 Oct 2026 after external review: two checks, REPORTED, NOT GATED (no trial spent).

1. Fake gurus (placebo). Is 5 of 16 more than random recipes of the same size would deliver?
   A fake guru draws k legs at random from JKP's 153 US factors, each in JKP's own published direction (so the fakes
   are 'informed', like a guru who reads the literature), k drawn from the real recipes' leg counts, equal weight.
   Exactly the A05-1 procedure: FF5 + momentum, Newey-West t (6 lags), pass if |t(alpha)| > 2.955 and the alpha has
   the same sign in 1963-94 and 1995-2025. 10,000 fakes, seed 42; panels of 16 to get P(>= 5 pass).
2. Where the legends died. Each recipe's alpha as the six factors (then quality) enter one at a time:
   none -> market -> size -> value -> profitability -> investment -> momentum -> + AQR quality (QMJ).
   The order is a choice; the last step before quality equals Table 1.
Writes ../results/fake_gurus.json and ../results/where_legends_died.csv."""
import json, os, sys, time
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from run_suspects import RECIPES, FAC, GATE_T, D, OUT, recipe, french_monthly, nw_ols, nw_mean_t  # noqa: E402

SEED, N = 42, 10000
fus = pd.read_csv(os.path.join(D, "jkp_usa_factors_monthly.csv"), index_col=0, parse_dates=True)
fus.index = pd.to_datetime(fus.index).to_period("M").to_timestamp("M")
fac = french_monthly("french_us_5f_daily.csv", "french_us_mom_daily.csv")
fac.index = fac.index.to_period("M").to_timestamp("M")
q = pd.read_csv(os.path.join(D, "aqr_qmj_qmj_factors.csv"), index_col=0, parse_dates=True)["USA"].rename("QMJ")
q.index = pd.to_datetime(q.index).to_period("M").to_timestamp("M")


def test(r):
    df = pd.concat([r.rename("r"), fac[FAC]], axis=1, join="inner").dropna().loc[:"2025-12-31"]
    if len(df) < 600:
        return None
    b, t, r2 = nw_ols(df.r.values, df[FAC].values)
    h1 = df.loc[:"1994-12-31"]; h2 = df.loc["1995-01-01":]
    a1 = nw_ols(h1.r.values, h1[FAC].values)[0][0]; a2 = nw_ols(h2.r.values, h2[FAC].values)[0][0]
    raw = df.r.mean() * 12
    return dict(alpha=b[0] * 12, t=t[0], raw=raw, r2=r2, passed=bool(abs(t[0]) > GATE_T and np.sign(a1) == np.sign(a2)))


def main():
    T0 = time.time()
    # ---- 1. fake gurus
    pool = [c for c in fus.columns if fus.loc["1963-07":"2025-12", c].notna().sum() >= 600]
    ks = [len(v) for v in RECIPES.values()]
    rng = np.random.default_rng(SEED)
    F = fus[pool]
    rows = []
    for i in range(N):
        k = int(rng.choice(ks)); legs = list(rng.choice(pool, size=k, replace=False))
        x = test(F[legs].dropna().mean(axis=1))
        if x: rows.append(dict(x, k=k, legs=" ".join(legs)))
    R = pd.DataFrame(rows)
    p = R.passed.mean()
    panels = R.passed.values[: len(R) // 16 * 16].reshape(-1, 16).sum(axis=1)
    real = pd.read_csv(os.path.join(OUT, "suspects_us.csv"), index_col=0)
    out = dict(note="Added 7 Oct 2026 after external review. Reported, not gated.", n_fakes=int(len(R)), pool=len(pool),
               leg_counts=ks, pass_rate=float(p), expected_of_16=float(16 * p),
               p_ge_5=float((panels >= 5).mean()), p_ge_real=float((panels >= int(real["pass"].sum())).mean()),
               panels=int(len(panels)), panel_mean=float(panels.mean()), panel_q95=float(np.quantile(panels, 0.95)),
               fake_median_raw=float(R.raw.abs().median()), fake_median_alpha=float(R.alpha.abs().median()),
               fake_median_r2=float(R.r2.median()),
               real_median_raw=float(real.raw_ann.abs().median()), real_median_alpha=float(real.alpha_ann.abs().median()),
               real_median_r2=float(real.r2.median()), real_n_pass=int(real["pass"].sum()),
               fake_share_abs_t_gt_2=float((R.t.abs() > 2).mean()))
    # pass rate by number of legs (fakes) and real share by legs
    out["fake_pass_by_k"] = {int(k): float(g.passed.mean()) for k, g in R.groupby("k")}
    # variant B: shuffle the legends' own ingredients (the legs the 16 recipes use, with their signs)
    own = sorted({l for v in RECIPES.values() for l in v})
    rngb = np.random.default_rng(SEED + 1); rb = []
    for i in range(N // 5):
        k = int(rngb.choice(ks)); legs = list(rngb.choice(own, size=k, replace=False))
        x = test(recipe(fus, legs).rename(None))
        if x: rb.append(x)
    RB = pd.DataFrame(rb); pb = RB.passed.values[: len(RB) // 16 * 16].reshape(-1, 16).sum(axis=1)
    out["own_ingredients"] = dict(n=int(len(RB)), n_legs=len(own), pass_rate=float(RB.passed.mean()), expected_of_16=float(16 * RB.passed.mean()),
                                  p_le_real=float((pb <= int(real["pass"].sum())).mean()), p_ge_real=float((pb >= int(real["pass"].sum())).mean()),
                                  median_alpha=float(RB.alpha.abs().median()))
    out["p_le_real"] = float((panels <= int(real["pass"].sum())).mean())
    R.to_csv(os.path.join(OUT, "fake_gurus_draws.csv"), index=False)
    # ---- 2. where the legends died
    steps = [("Raw premium", []), ("+ Market", ["Mkt-RF"]), ("+ Size", ["Mkt-RF", "SMB"]), ("+ Value", ["Mkt-RF", "SMB", "HML"]),
             ("+ Profitability", ["Mkt-RF", "SMB", "HML", "RMW"]), ("+ Investment", ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]),
             ("+ Momentum", FAC), ("+ Quality (QMJ)", FAC + ["QMJ"])]
    W = []
    X = fac.join(q, how="inner")
    for name, legs in RECIPES.items():
        r = recipe(fus, legs); r.index = r.index.to_period("M").to_timestamp("M")
        df = pd.concat([r.rename("r"), X], axis=1, join="inner").dropna().loc[:"2025-12-31"]
        for lab, cols in steps:
            b, t, _ = nw_ols(df.r.values, df[cols].values) if cols else (lambda m: (np.array([m[0]]), np.array([m[1]]), 0))(nw_mean_t(df.r.values))
            W.append(dict(recipe=name, step=lab, alpha=b[0] * 12, t=t[0], n=len(df)))
    pd.DataFrame(W).to_csv(os.path.join(OUT, "where_legends_died.csv"), index=False)
    json.dump(out, open(os.path.join(OUT, "fake_gurus.json"), "w"), indent=1)
    print(json.dumps(out, indent=1)); print("t=%.0fs" % (time.time() - T0))


if __name__ == "__main__":
    main()
