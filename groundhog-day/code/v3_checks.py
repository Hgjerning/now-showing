# -*- coding: utf-8 -*-
"""Checks added on 9 October 2026 after the hostile-referee stress test (version 3).
Reported, not gated: none of these can change a verdict. Reads results/ and results_r/, writes results/v3_checks.json."""
import json, os
import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = pd.read_csv(os.path.join(ROOT, "results", "windows_by_year.csv"), index_col="year")
W = W[(W.index >= 1928) & (W.index <= 2025)]
r = W["ret[1,90]"]; mid = W["kind"] == "midterm"
S = json.load(open(os.path.join(ROOT, "results", "summary.json")))
C4 = json.load(open(os.path.join(ROOT, "results_r", "summary_c31_4.json")))
C5 = json.load(open(os.path.join(ROOT, "results_r", "summary_c31_5.json")))
out = {"note": "Added 9 Oct 2026 after the stress test. Reported, not gated."}

def welch(a, b):
    return stats.ttest_ind(a, b, equal_var=False).statistic

# 1. Studentized permutation (Chung & Romano 2013) and Monte Carlo SE of the primary p
rng = np.random.default_rng(42); N = 10_000
x = r.values; lab = mid.values; t_obs = welch(x[lab], x[~lab]); d_obs = x[lab].mean() - x[~lab].mean()
ts = np.empty(N); ds = np.empty(N)
for i in range(N):
    p = rng.permutation(lab); ts[i] = welch(x[p], x[~p]); ds[i] = x[p].mean() - x[~p].mean()
p_primary = S["C31-1"]["p_perm"] if "p_perm" in S["C31-1"] else 0.0056
out["studentized_perm_p"] = float((1 + (ts >= t_obs).sum()) / (N + 1))
out["primary_p"] = float(p_primary)
out["mc_se_primary_p"] = float(np.sqrt(p_primary * (1 - p_primary) / N))

# 2. Multiple testing: Holm within Case 31, Bonferroni across the programme
fam = {"C31-1": float(p_primary), "C31-2": float(S["C31-2"].get("p_perm", 0.2075)),
       "C31-4": C4["C31-4"]["perm_p"], "C31-5": C5["C31-5"]["perm_p"]}
order = sorted(fam, key=fam.get); holm = []; still = True
for k, name in enumerate(order):
    thr = 0.05 / (len(order) - k); ok = still and fam[name] < thr; still = ok
    holm.append({"trial": name, "p": fam[name], "holm_threshold": thr, "rejected": bool(ok)})
out["holm_case31"] = holm
out["programme_trials_run"] = 15 + 4
out["programme_bonferroni_gate"] = 0.05 / 19

# 3. Four cycle positions: only the midterm year is positive against the rest
pos = {"midterm": W["kind"] == "midterm", "presidential": W["kind"] == "presidential"}
cyc = ((W.index - 1930) % 4)  # 0 midterm, 1 pre-election, 2 election, 3 post-election
names = {0: "midterm", 1: "pre-election year", 2: "presidential election", 3: "post-election year"}
out["cycle_positions"] = {names[k]: {"n": int((cyc == k).sum()), "gap_vs_rest_pts": float(100 * (r[cyc == k].mean() - r[cyc != k].mean()))} for k in range(4)}

# 4. Recession midterms: all five vs the four whose recession ended soon after
rec5 = [1930, 1970, 1974, 1982, 1990]; rec4 = [1970, 1974, 1982, 1990]
out["recession_midterms"] = {str(y): float(r[y]) for y in rec5}
out["recession_mean_all5"] = float(r[rec5].mean()); out["recession_mean_4_ended"] = float(r[rec4].mean())

# 5. Dropping the five best midterms (comparison with dropping the five recession midterms)
best5 = r[mid].sort_values(ascending=False).index[:5].tolist()
out["drop_best5_years"] = best5
out["drop_best5_gap_pts"] = float(100 * (r[mid].drop(best5).mean() - r[~mid].mean()))

# 6. Post-2003 interval (daily window)
a = r[mid & (W.index >= 2003)]; b = r[~mid & (W.index >= 2003)]
se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
dfw = (a.var(ddof=1)/len(a) + b.var(ddof=1)/len(b))**2 / ((a.var(ddof=1)/len(a))**2/(len(a)-1) + (b.var(ddof=1)/len(b))**2/(len(b)-1))
q = stats.t.ppf(0.975, dfw); g = a.mean() - b.mean()
out["post2003"] = {"n_mid": len(a), "n_ctrl": len(b), "gap_pts": float(100*g), "ci95_pts": [float(100*(g - q*se)), float(100*(g + q*se))]}

# 7. C31-5: realised SE, CI, power against the modern monthly gap, and the era difference
c5 = C5["C31-5"]; by = pd.Series({int(k): v for k, v in c5["by_year"].items()})
m5 = by[by.index.isin(c5["midterm_years"])]; k5 = by[~by.index.isin(c5["midterm_years"])]
se5 = np.sqrt(m5.var(ddof=1)/len(m5) + k5.var(ddof=1)/len(k5)); d5 = m5.mean() - k5.mean()
cal = C5["calibration_1928_2025"]; se_cal = cal["diff"] / cal["welch_t"]
out["C31_5"] = {"gap_pts": float(100*d5), "se_pts": float(100*se5), "ci95_pts": [float(100*(d5 - 1.96*se5)), float(100*(d5 + 1.96*se5))],
                "power_vs_modern_gap": float(stats.norm.cdf(cal["diff"]/se5 - stats.norm.ppf(0.975))),
                "modern_monthly_gap_pts": float(100*cal["diff"]),
                "era_difference_z": float((cal["diff"] - d5) / np.sqrt(se5**2 + se_cal**2))}

# 8. Forecast scoring rule (to be registered as a dated clarification before 3 Nov 2026)
f = S["forward_2026"]; ctrl = float(r[~mid].mean())
out["forecast"] = {"point": f["point"], "pi80": f["pi80"], "control_only_forecast": ctrl,
                   "midterm_specific_part_pts": float(100*(f["point"] - ctrl)),
                   "breakeven_return_for_squared_error": float((f["point"] + ctrl) / 2)}

json.dump(out, open(os.path.join(ROOT, "results", "v3_checks.json"), "w"), indent=2)
print(json.dumps(out, indent=1))
