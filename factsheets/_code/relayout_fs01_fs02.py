# -*- coding: utf-8 -*-
"""Layout v2 for FS01 (Turtle) and FS02 (Lottery), applied to the built page (their own builders need Windows-only caches).
Same sections and numbers; verdict/scorecard, Sharpe anatomy and fit added; detail moved to the appendix. Idempotent."""
import json, os
import build_factsheets as BF
import factsheet_v2 as V2

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); OUT = os.path.join(HERE, "..", "factsheets")
U = V2.U
JOBS = {"FS01": ("FS01_Turtle_Traders", "turtle_summary.json", ("Turtle L/S (S1+S2)", "Turtle long-only (S1+S2)", "EW universe (benchmark)"), "FS01 Turtle Traders: factsheet"),
        "FS02": ("FS02_Lottery_MAX", "lottery_summary.json", ("L/S low minus high MAX (net)", "Low-MAX long-only (net)", "EW universe (benchmark)"), "FS02 Lottery (MAX): factsheet")}


def rng(v):
    v = [x for x in v if x == x]; return f"{V2.p(min(v))} to {V2.p(max(v))}"


for code, (stem, js, books, title) in JOBS.items():
    md = open(os.path.join(OUT, stem + ".md"), encoding="utf-8").read()
    if "## 1. Verdict and scorecard" in md:
        print(code, "already in layout v2"); continue
    per = json.load(open(os.path.join(RES, js)))
    LS = books[0]
    attr = [per[R]["attribution"][LS]["coef"]["alpha"] for R in U if LS in per[R].get("attribution", {})]
    capm = [per[R]["stats"][LS]["alpha"] for R in U]
    V2.panel(code)
    md = V2.reorganise(md, code, per, rng(attr), rng(capm), books=books)
    md = md.replace(f"](../figures/xs_{code}_panel.png)", f"](../figures/xs_{code}_panel.png)")
    BF.write(stem, md, title)
    print(code, "relaid")
