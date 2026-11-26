import sys, os, json
sys.path.insert(0, os.path.expanduser("~/mnt/Project10_Articles/Factsheets/code"))
os.chdir(os.path.expanduser("~/mnt/Project10_Articles/Factsheets/code"))
import numpy as np, pandas as pd
import xs, data
def nw_t(x, L=6):
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x); e = x - x.mean()
    v = (e @ e) / n
    for l in range(1, L + 1):
        v += 2 * (1 - l / (L + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / np.sqrt(v / n)
R = sys.argv[1]
I = xs.inputs(R); fwd = I["fwd"]; S0 = I["S"]["seas"]
print(R, "fwd", fwd.index.min(), fwd.index.max(), fwd.shape, "seas", S0.index.min(), S0.shape)
# monthly returns: fwd.loc[m] = return in month m
mret = fwd
def seas_from(t, ks, minobs=1):
    tg = [(t + 1) - 12 * k for k in ks if ((t + 1) - 12 * k) in mret.index]
    if not tg: return None
    M = mret.loc[tg]; c = M.notna().sum()
    return M.mean().where(c >= minobs)
idx = S0.index
def build(ks, minobs=1, shift=0):
    out = pd.DataFrame(np.nan, index=idx, columns=S0.columns)
    for t in idx:
        tg = [(t + 1 + shift) - 12 * k for k in ks]
        tg = [m for m in tg if m in mret.index and m <= t]
        if tg:
            M = mret.loc[tg].reindex(columns=S0.columns); c = M.notna().sum()
            out.loc[t] = M.mean().where(c >= minobs)
    E = I["E"].reindex(index=idx, columns=S0.columns).fillna(False).astype(bool)
    return out.where(E)
V = {"baseline (rebuilt)": build(range(1, 21)),
     "min 5 same-month obs": build(range(1, 21), 5),
     "lag 12 only (HS cleanest)": build([1]),
     "lags 2-5 years": build(range(2, 6)),
     "placebo: month t, not t+1 (shift -1)": build(range(1, 21), 1, -1),
     "placebo: month t+2 (shift +1)": build(range(1, 21), 1, 1)}
b=V["baseline (rebuilt)"]; print("corr", round(b.stack().corr(S0.stack()),4), "notna rebuilt/orig", int(b.notna().sum().sum()), int(S0.notna().sum().sum()))
out = {}
for k, sig in V.items():
    I["S"]["_v"] = sig
    P = xs.run(I, "_v", True)
    h = P.loc["2020-01-01":]
    out[k] = dict(n=len(P), gross=float(P.ls_gross.mean()*12), t_gross=float(nw_t(P.ls_gross)), net=float(P.ls_net.mean()*12), t_net=float(nw_t(P.ls_net)),
                  gross_hold=float(h.ls_gross.mean()*12), t_gross_hold=float(nw_t(h.ls_gross)), names=float(P.n_good.median()))
    print(R, k, {a: round(b, 3) for a, b in out[k].items()})
json.dump(out, open(os.path.expanduser(f"~/fs06s/sens_{R}.json"), "w"), indent=1)
