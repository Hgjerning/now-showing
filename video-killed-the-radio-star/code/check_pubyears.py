"""Check A08's 29 publication years against JKP's factor-details table (reported check, not a trial).
Needs data/Factor Details.xlsx from github.com/bkelly-lab/ReplicationCrisis (GlobalFactors/Factor Details.xlsx).
Writes results/pubyear_check.csv; the sensitivity run (JKP's years for Basu 1983 and QMJ 2018) is
run_decay.py with those two years changed, saved as results/pubyear_sensitivity.json."""
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "run_decay.py")).read(); s = src.index("PUB = {"); e = src.index("}", s) + 1
ns = {}; exec(src[s:e], ns); PUB = ns["PUB"]
d = pd.read_excel(os.path.join(ROOT, "data", "Factor Details.xlsx")); d = d[d.abr_jkp.notna()].set_index("abr_jkp")
rows = []
for f, (lab, paper, y) in PUB.items():
    cite = str(d.loc[f, "cite"]) if f in d.index else ""
    m = re.findall(r"(19\d\d|20\d\d)", cite); jy = int(m[-1]) if m else None
    rows.append((f, lab, paper, y, cite, jy, "OK" if jy == y else "DIFF"))
pd.DataFrame(rows, columns=["factor", "label", "our_paper", "our_year", "jkp_cite", "jkp_year", "check"]).to_csv(
    os.path.join(ROOT, "results", "pubyear_check.csv"), index=False)
