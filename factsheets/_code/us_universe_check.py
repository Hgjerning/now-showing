# -*- coding: utf-8 -*-
"""US universe check for the factsheets (2026-10-01). The US books in FS03-FS12 draw from the 500 largest of every
name EVER in the S&P 500 (2012-2026), so later additions are present before they joined. This re-runs each factsheet's
baseline book (X0, xs.run with its pre-declared signal and direction) on US under the universe rule in FS_US_UNIVERSE
("top500" as published, or "sp500_pit": actual members at each month-end). Not a new trial.
    FS_US_UNIVERSE=top500    python us_universe_check.py
    FS_US_UNIVERSE=sp500_pit python us_universe_check.py
    python us_universe_check.py --compare
"""
import json
import os
import sys

import numpy as np

RES = os.environ.get("FS_RESULTS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def st(x):
    x = x.dropna()
    m, s = x.mean(), x.std()
    return dict(ann=float(m * 12), t=float(m / s * np.sqrt(len(x))) if s > 0 else None, sharpe=float(m / s * np.sqrt(12)) if s > 0 else None,
                cagr=float((1 + x).prod() ** (12 / len(x)) - 1), n=int(len(x)))


def run():
    import data
    import specs
    import xs
    I = xs.inputs("US")
    out = {"universe": data.US_UNIVERSE, "ew": st(xs.pd.Series(I["ew"]).loc[xs.START:xs.END]) if False else None, "books": {}}
    for code in specs.ORDER:
        sp = specs.S[code]
        P = xs.run(I, sp["sig"], sp["long_high"], sp["construction"])
        out["books"][code] = dict(title=sp["title"], ls_net=st(P.ls_net), long_only=st(P.good_net), ew=st(P.ew), n_good=float(P.n_good.mean()))
        print(code, sp["title"], "L/S %.1f%% t %.2f | LO Sharpe %.2f" % (out["books"][code]["ls_net"]["ann"] * 100, out["books"][code]["ls_net"]["t"],
                                                                          out["books"][code]["long_only"]["sharpe"]), flush=True)
    json.dump(out, open(os.path.join(RES, f"us_universe_check_{data.US_UNIVERSE}.json"), "w"), indent=1)


def compare():
    a = json.load(open(os.path.join(RES, "us_universe_check_top500.json")))["books"]
    b = json.load(open(os.path.join(RES, "us_universe_check_sp500_pit.json")))["books"]
    L = ["| Factsheet | L/S net, % a year (t): published rule | point-in-time S&P 500 | Long-only Sharpe: published rule | point-in-time | EW universe Sharpe: published rule | point-in-time |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for k in a:
        x, y = a[k], b[k]
        L.append(f"| {k} {x['title']} | {x['ls_net']['ann'] * 100:+.1f} ({x['ls_net']['t']:.2f}) | {y['ls_net']['ann'] * 100:+.1f} ({y['ls_net']['t']:.2f}) | "
                 f"{x['long_only']['sharpe']:.2f} | {y['long_only']['sharpe']:.2f} | {x['ew']['sharpe']:.2f} | {y['ew']['sharpe']:.2f} |")
    t = "\n".join(L); open(os.path.join(RES, "us_universe_check.md"), "w", encoding="utf-8").write(t + "\n"); print(t)


if __name__ == "__main__":
    compare() if "--compare" in sys.argv else run()
