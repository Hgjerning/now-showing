# -*- coding: utf-8 -*-
"""A06 reported check: Ridge and gradient boosting retrained on month-shuffled targets (50 runs each)."""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_ml import OUT, long_short, walk_forward  # noqa: E402
from features import panel_long  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from stats import sharpe  # noqa: E402

L = panel_long(); rows = []
for s in range(1, 51):
    Lw, P = walk_forward(L, ["Ridge", "GradBoost"], shuffle_seed=s)
    for n in P:
        ls = long_short(Lw, P[n]).ls
        rows.append(dict(seed=s, model=n, sharpe=sharpe(ls), mean=float(ls.mean())))
    print(s, flush=True)
D = pd.DataFrame(rows); D.to_csv(os.path.join(OUT, "placebo_shuffled.csv"), index=False)
B = pd.read_csv(os.path.join(OUT, "scoreboard.csv"), index_col=0)
out = {n: dict(real_sharpe=float(B.loc[n, "sharpe"]), placebo_mean=float(g.sharpe.mean()), placebo_sd=float(g.sharpe.std()),
               p=float((1 + (g.sharpe >= B.loc[n, "sharpe"]).sum()) / (len(g) + 1)), runs=int(len(g))) for n, g in D.groupby("model")}
json.dump(out, open(os.path.join(OUT, "placebo_summary.json"), "w"), indent=2); print(out)
