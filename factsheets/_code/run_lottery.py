import sys, pandas as pd, numpy as np, time
import data, lottery
R = sys.argv[1]; o = data.load(R); t0 = time.time()
res = {}
res["max1"], res["hold"] = lottery.build(o, R=R)
res["max5"], _ = lottery.build(o, signal="max5", R=R)
if R == "US":
    res["max1_vw"], _ = lottery.build(o, vw=True, R=R)
for k in ("max1", "max5", "max1_vw"):
    if k in res: res[k] = res[k].loc[:"2026-08-31"]
res["current"] = lottery.current_portfolio(o)
pd.to_pickle(res, f"../results/lottery_{R}.pkl")
P = res["max1"]; q = P.q.iloc[-1]
print(R, f"{time.time()-t0:.0f}s", P.index[0].date(), P.index[-1].date(), "n", int(P.n.median()), "q", q,
      "LS gross %.3f net %.3f" % (P.ls_gross.mean()*12, P.ls_net.mean()*12), "Q1 %.3f Qn %.3f EW %.3f" % (P.Q1.mean()*12, P[f"Q{q}"].mean()*12, P.EW.mean()*12),
      "to_low %.2f to_high %.2f" % (P.to_low.mean(), P.to_high.mean()))
