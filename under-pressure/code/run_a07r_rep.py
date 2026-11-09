# Reported (not gated) items for A07 revisited: published universe, 30%/50% thresholds, Altman without MVE/TL.
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import run_a07r as R  # noqa: E402
from stats import auc, block_boot_mean
out = {}
for U in ["sp500_pit", "top500"]:
    D = pd.read_csv(f"ext_{U}/scores_panel_ext.csv", parse_dates=["date"])
    D["crash30"] = (D.minr <= 0.7).astype(float); D["crash50"] = (D.minr <= 0.5).astype(float)
    D.loc[D.minr.isna(), ["crash30", "crash50"]] = np.nan
    o = {}
    E = R.prep(D); o["check_n_obs"] = int(len(E)); o["main"] = R.tests(R.oos(E))
    if U == "sp500_pit":
        for c in ["crash30", "crash50"]:
            Et = R.prep(D, c); o[c] = {"base_rate": float(Et.y.mean()), **R.tests(R.oos(Et))}
        E2 = R.prep(D).dropna(subset=["Z_nm"]).copy(); E2["r_Znm"] = E2.groupby("date").Z_nm.rank(pct=True, ascending=False)
        R.MODELS["V+Znm"] = ["r_vol", "r_Znm"]; P = R.oos(E2)
        d = (P["auc_V+Znm"] - P["auc_V"]).dropna(); b = block_boot_mean(d, 4, 10000, 42, 0.0)
        per = [dict(Z=auc(-g.Z, g.y.astype(bool)), Znm=auc(-g.Z_nm, g.y.astype(bool))) for _, g in E2.groupby("date")]
        per = pd.DataFrame(per)
        o["altman_without_mve"] = {"auc_Z_full_mean": float(per.Z.mean()), "auc_Z_without_MVE_TL_mean": float(per.Znm.mean()),
                                   "oos_V+Znm_minus_V": b}
        del R.MODELS["V+Znm"]
        # crash rate by volatility decile (pooled, within-date deciles)
        E["vdec"] = E.groupby("date").vol.transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False) + 1)
        o["crash_rate_by_vol_decile"] = E.groupby("vdec").y.mean().round(4).to_dict()
    out[U] = o
json.dump(out, open("results_a07r/reported_a07r.json", "w"), indent=2, default=float)
print(json.dumps(out, indent=1, default=float))
