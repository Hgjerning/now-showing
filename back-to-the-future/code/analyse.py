# -*- coding: utf-8 -*-
"""Case 33: re-derive the headline numbers from the stored series and collect everything the
article quotes into results/summary.json. No new trial is spent: every statistic here either
reproduces a Project2 number of record or applies a textbook correction to one.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D, P, OUT = (os.path.join(ROOT, x) for x in ("data", "data_private", "results"))
os.makedirs(OUT, exist_ok=True)
S = {}

# ---------------------------------------------------------------- waterfall
wf = pd.read_csv(os.path.join(D, "waterfall_sources.csv"))
avu = pd.read_csv(os.path.join(D, "alpha_vs_urth.csv")).iloc[0]
wf.loc[wf.step == 4, ["alpha_ann", "t_stat"]] = [avu.alpha_ann, avu.t_block]
wf.to_csv(os.path.join(OUT, "waterfall.csv"), index=False)
S["waterfall"] = wf.to_dict(orient="records")
S["record"] = dict(alpha=avu.alpha_ann, t_block=avu.t_block, t_ols=avu.t_ols, ci=[avu.ci_lo_ann, avu.ci_hi_ann], beta=avu.beta,
                   trials=int(avu.trials), bonferroni_t=avu.bonferroni_t, n=int(avu.n))

# ---------------------------------------------------------------- in-sample series (epoch 11), independent re-derivation
cp = pd.read_csv(os.path.join(P, "current_performance_returns.csv"), index_col=0, parse_dates=True)
x = cp[["BOOK", "URTH"]].dropna()
X = np.column_stack([np.ones(len(x)), x.URTH.values]); b, *_ = np.linalg.lstsq(X, x.BOOK.values, rcond=None)
res = x.BOOK.values - X @ b; se = np.sqrt(res.var(ddof=2) * np.linalg.inv(X.T @ X)[0, 0])
sr = lambda r: r.mean() / r.std(ddof=1) * np.sqrt(52)
def mdd(r):
    w = (1 + r).cumprod(); return float((w / w.cummax() - 1).min())
def cagr(r):
    return float((1 + r).prod() ** (52 / len(r)) - 1)
S["insample_rederived"] = dict(n=len(x), alpha_ann=b[0] * 52, t_ols=b[0] / se, beta=b[1], sharpe_book=sr(x.BOOK), sharpe_urth=sr(x.URTH),
                               mdd_book=mdd(x.BOOK), mdd_urth=mdd(x.URTH), cagr_book=cagr(x.BOOK), cagr_urth=cagr(x.URTH),
                               start=str(x.index[0].date()), end=str(x.index[-1].date()))
g = pd.DataFrame({"BOOK": (1 + x.BOOK).cumprod(), "URTH": (1 + x.URTH).cumprod()}); g.to_csv(os.path.join(OUT, "insample_growth.csv"))

# ---------------------------------------------------------------- out of sample (ART, 1995-2011)
oo = pd.read_csv(os.path.join(P, "art_oos_returns.csv"), index_col=0, parse_dates=True)
oo["bench"] = oo[["bench_EU", "bench_AM"]].mean(axis=1)
o = oo[["COMBINED", "bench"]].dropna()
X = np.column_stack([np.ones(len(o)), o.bench.values]); b2, *_ = np.linalg.lstsq(X, o.COMBINED.values, rcond=None)
res2 = o.COMBINED.values - X @ b2; se2 = np.sqrt(res2.var(ddof=2) * np.linalg.inv(X.T @ X)[0, 0])
rec = pd.read_csv(os.path.join(D, "art_oos_result.csv")).set_index("arm")
comb = rec.loc[[i for i in rec.index if i.startswith("COMBINED")][0]]
S["oos"] = dict(record_alpha=comb.alpha_ann, record_t=comb.t, record_ci=[comb.ci_lo, comb.ci_hi], record_mdd=comb.strat_maxdd, record_bench_mdd=comb.bench_maxdd,
                record_sharpe=comb.strat_sharpe, record_bench_sharpe=comb.bench_sharpe, record_beta=comb.beta, n=int(comb.n),
                rederived_alpha_ols=b2[0] * 52, rederived_t_ols=b2[0] / se2, rederived_beta=b2[1], mdd=mdd(o.COMBINED), bench_mdd=mdd(o.bench),
                cagr=cagr(o.COMBINED), bench_cagr=cagr(o.bench), start=str(o.index[0].date()), end=str(o.index[-1].date()),
                per_region={k: dict(alpha=rec.loc[k, "alpha_ann"], t=rec.loc[k, "t"]) for k in rec.index if not k.startswith("COMBINED")})
dd = pd.DataFrame({"strategy": (1 + o.COMBINED).cumprod(), "benchmark": (1 + o.bench).cumprod()})
(dd / dd.cummax() - 1).to_csv(os.path.join(OUT, "oos_drawdown.csv"))

# ---------------------------------------------------------------- multiple testing: what t is needed, and HLZ haircut
t0 = float(wf.loc[wf.step == 1, "t_stat"].iloc[0])
p0 = 2 * stats.norm.sf(t0)
need = {int(n): float(stats.norm.isf(0.05 / n / 2)) for n in (1, 5, 13, 24, 33, 100, 235)}
def hlz(t, n):  # Harvey, Liu & Zhu (2016) Bonferroni haircut of the Sharpe ratio
    padj = min(1.0, 2 * stats.norm.sf(t) * n); tadj = stats.norm.isf(padj / 2) if padj < 1 else 0.0
    return tadj, 1 - tadj / t
S["multiple_testing"] = dict(t_first=t0, p_first=p0, t_needed=need,
                             hlz_24=dict(zip(("t_adj", "haircut"), hlz(t0, 24))), hlz_33=dict(zip(("t_adj", "haircut"), hlz(t0, 33))))

# ---------------------------------------------------------------- haircuts, this project vs the literature
a1 = float(wf.loc[wf.step == 1, "alpha_ann"].iloc[0]); sh1 = float(wf.loc[wf.step == 1, "sharpe_book"].iloc[0])
S["haircuts"] = dict(alpha_first_to_record=1 - avu.alpha_ann / a1, alpha_first_to_oos=1 - comb.alpha_ann / a1,
                     sharpe_first_to_record=1 - S["insample_rederived"]["sharpe_book"] / sh1)

# ---------------------------------------------------------------- survivorship
eu = pd.read_csv(os.path.join(D, "eu_pit_result.csv")).iloc[0]; wk = pd.read_csv(os.path.join(D, "wiki_pit_result.csv")).set_index("region")
oth = pd.read_csv(os.path.join(D, "other_sources.csv")).set_index("item")["value"]
surv = pd.DataFrame([
    dict(region="US (S&P 500)", biased=oth["us_sharpe_live_universe"], pit=oth["us_sharpe_point_in_time"], note="today's members vs point-in-time members, Sharadar"),
    dict(region="Europe (STOXX 600)", biased=eu.sharpe_union_no_mask, pit=eu.sharpe_union_pit, note="same panel, point-in-time mask off vs on"),
    dict(region="UK", biased=wk.loc["UK", "sharpe_current_only"], pit=wk.loc["UK", "sharpe_union_pit"], note="current members vs point-in-time"),
    dict(region="Denmark", biased=wk.loc["DK", "sharpe_current_only"], pit=wk.loc["DK", "sharpe_union_pit"], note="current members vs point-in-time; small, noisy"),
])
surv["overstatement"] = surv.biased / surv.pit - 1
surv["haircut"] = 1 - surv.pit / surv.biased
surv.to_csv(os.path.join(OUT, "survivorship.csv"), index=False)
S["survivorship"] = surv.to_dict(orient="records")
S["placebo"] = dict(z_live=oth["placebo_z_live_universe"], z_pit=oth["placebo_z_point_in_time"], pct_pit=oth["placebo_pct_point_in_time"])

# ---------------------------------------------------------------- random books (frozen-book null)
nb = pd.read_csv(os.path.join(D, "dd_selection_alpha_null.csv"))
S["random_books"] = dict(n=len(nb), mean_t=float(nb.t.mean()), sd_t=float(nb.t.std()), share_t_gt_2=float((nb.t > 2).mean()),
                         share_t_gt_frozen=float((nb.t > oth["frozen_book_t"]).mean()), frozen_t=oth["frozen_book_t"], mean_alpha=float(nb.alpha.mean()))

# ---------------------------------------------------------------- what survived: the no-trade band
bb = pd.read_csv(os.path.join(D, "band_bootstrap_book.csv")).iloc[0]; br = pd.read_csv(os.path.join(D, "band_bootstrap_results.csv"))
S["band"] = dict(book_diff=bb["diff"], ci=[bb.ci_lo, bb.ci_hi], sharpe0=bb.sharpe_band0, sharpe200=bb.sharpe_band200,
                 regions=br[["region", "diff", "ci_lo", "ci_hi"]].to_dict(orient="records"))

# ---------------------------------------------------------------- rolling alpha
ra = pd.read_csv(os.path.join(D, "alpha_rolling_book_urth.csv"), index_col=0, parse_dates=True).iloc[:, 0]
neg = ra[ra < 0]
S["rolling"] = dict(last=float(ra.iloc[-1]), last_date=str(ra.index[-1].date()), first_neg=str(neg.index[0].date()) if len(neg) else None,
                    share_neg_since_2019=float((ra[ra.index >= "2019-01-01"] < 0).mean()))
S["dsr_best_of_24"] = oth["dsr_best_of_24_pit"]
json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=2, default=float)
print(json.dumps({k: v for k, v in S.items() if k not in ("waterfall",)}, indent=1, default=float))
