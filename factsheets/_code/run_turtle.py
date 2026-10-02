import sys, time, json, os, pandas as pd, numpy as np
import data, turtle
R = sys.argv[1]; o = data.load(R); OUT = os.environ.get("FS_RESULTS") or "../results"
t0 = time.time(); res = {}
for name, kw in [("S1", dict(system=1)), ("S2", dict(system=2)), ("S1_long", dict(system=1, allow_short=False)), ("S2_long", dict(system=2, allow_short=False))]:
    res[name] = turtle.run(o["ret"], o["elig"], **kw)
    print(R, name, f"{time.time()-t0:.0f}s", "ann ret %.3f" % (res[name]["ret"].mean()*252), "vol %.3f" % (res[name]["ret"].std()*np.sqrt(252)), "trades", len(res[name]["trades"]))
pd.to_pickle(res, f"{OUT}/turtle_{R}.pkl")
