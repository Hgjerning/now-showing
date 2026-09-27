"""Post-hoc (not a trial): beta-neutral legs + turnover buffer on the ORIGINAL MAX1 signal, the combination recommended in FS02 §10.3."""
import json, os, pandas as pd, numpy as np
import data, perf, lottery_fix
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
S = pd.read_pickle(os.path.join(RES, "lottery_fix_series.pkl")); out = {}; M = {}; B = {}
for R in data.REGIONS:
    I = lottery_fix.monthly_inputs(R); x = lottery_fix.build(I, beta_neutral=True, buffer=True).loc["2013-02-28":]
    M[R] = x.ls_net; B[R] = S[R]["L1 beta-neutral"].loc["2013-02-28":].ls_net
    out[R] = dict(cost=float(x.cost.mean() * 12), holdout_sharpe=perf.sharpe(x.ls_net.loc["2020":]), design_sharpe=perf.sharpe(x.ls_net.loc[:"2019"]))
M = pd.DataFrame(M); B = pd.DataFrame(B)
h = M.loc["2020":].mean(axis=1); d = M.loc[:"2019"].mean(axis=1)
out["pooled"] = dict(holdout_ann=float(h.mean() * 12), holdout_t=perf.nw_t(h)["t"], holdout_sharpe=perf.sharpe(h), design_sharpe=perf.sharpe(d),
                     l1_holdout_sharpe=perf.sharpe(B.loc["2020":].mean(axis=1)), cost=float(np.mean([out[R]["cost"] for R in data.REGIONS])),
                     l1_cost=None)
json.dump(out, open(os.path.join(RES, "lottery_posthoc.json"), "w"), indent=1); print(json.dumps(out["pooled"], indent=1))
