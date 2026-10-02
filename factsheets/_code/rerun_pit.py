# -*- coding: utf-8 -*-
"""Re-run the factsheet analyses on the point-in-time US universe (2026-10-01). Not a new trial.

Why: until today the US books drew from the 500 largest of every name EVER in the S&P 500 (2012-2026), which knows
which companies would succeed (US_UNIVERSE_CHECK_2026-10-01.md). data.py now defaults to the actual S&P 500 members
at each month-end (FS_US_UNIVERSE=sp500_pit). World (WD) contains the US names and changes too.

Output goes to results_pit/ (FS_RESULTS); the published results/, figures/ and factsheets/ are NOT touched and no
factsheet is rebuilt here. results/*.json and *.csv are copied into results_pit/ first so that steps reading earlier
outputs find them; every step below then overwrites its own outputs. ART (FS15) and non-US fundamentals (FS17) do not
use the US stock universe and are not re-run.

Resumable: a step that finished is skipped on a re-run (results_pit/_done.txt). Log: results_pit/_rerun_log.txt.
Run from the Factsheets/code folder, with a Python that has pandas, scipy, scikit-learn, statsmodels, cvxpy, matplotlib,
pyarrow and markdown:
    cd "...\\Project10_Articles\\Factsheets\\code"
    & "C:\\Python314\\python.exe" rerun_pit.py
Expect 1-3 hours (World and the batteries are the slow steps).
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUB, OUT = HERE.parent / "results", HERE.parent / "results_pit"
RS = ["US", "EU", "UK", "DK", "SC", "WD"]
STEPS = ([["signals.py", r] for r in RS] + [["signals2.py", r] for r in RS] + [["library.py", r] for r in RS]
         + [["run_lottery.py", r] for r in RS] + [["run_turtle.py", r] for r in RS] + [["turtle_fix.py", r] for r in RS]
         + [["lottery_fix.py"], ["posthoc_lottery.py"], ["analyse.py", "turtle", "lottery"], ["fix_analysis.py"], ["diag_turtle.py"],
            ["cost_check.py"], ["neighbourhood.py", "max"], ["neighbourhood.py", "brk"], ["monkey.py"],
            ["analyse_xs.py", "FS03", "FS04", "FS06"], ["analyse_xs.py", "FS07", "FS08", "FS09"], ["analyse_xs.py", "FS10", "FS11", "FS12"],
            ["battery.py", "US", "EU", "UK"], ["battery.py", "DK", "SC"], ["battery.py", "WD"], ["jkp_battery.py"],
            ["financing.py"], ["common_ground.py"], ["fmb.py"], ["fund_battery.py"], ["fs14.py"], ["fs18.py"], ["fs19.py"],
            ["fs19_engine.py"], ["fs20.py"], ["fs21.py"], ["impact.py"]])
NEED = ["pandas", "scipy", "sklearn", "statsmodels", "cvxpy", "matplotlib", "pyarrow", "markdown"]


def log(m):
    print(m, flush=True)
    with open(OUT / "_rerun_log.txt", "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + m + "\n")


def main():
    OUT.mkdir(exist_ok=True)
    import importlib.util
    miss = [m for m in NEED if importlib.util.find_spec(m) is None]
    if miss:
        sys.exit(f"Missing packages: {miss}. Install with:  & \"{sys.executable}\" -m pip install " + " ".join(
            {"sklearn": "scikit-learn"}.get(m, m) for m in miss))
    for f in PUB.iterdir():
        if f.suffix in (".json", ".csv") and not (OUT / f.name).exists():
            shutil.copy2(f, OUT / f.name)
    done_f = OUT / "_done.txt"
    done = set(done_f.read_text(encoding="utf-8").splitlines()) if done_f.exists() else set()
    (HERE.parent / "figures_pit").mkdir(exist_ok=True)
    env = dict(os.environ, FS_RESULTS=str(OUT), FS_FIGURES=str(HERE.parent / "figures_pit"), FS_US_UNIVERSE="sp500_pit", MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    (OUT / "logs").mkdir(exist_ok=True)
    for st in STEPS:
        key = " ".join(st)
        if key in done:
            continue
        t = time.time(); log(f"{key} ...")
        r = subprocess.run([sys.executable] + st, cwd=HERE, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (OUT / "logs" / (key.replace(" ", "_").replace(".py", "") + ".log")).write_text(r.stdout + "\n--- stderr ---\n" + r.stderr, encoding="utf-8")
        if r.returncode != 0:
            last = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "(no stderr)"
            log(f"{key} FAILED after {time.time() - t:.0f}s: {last}  (continuing)")
            continue
        log(f"{key} ok in {time.time() - t:.0f}s")
        with open(done_f, "a", encoding="utf-8") as f:
            f.write(key + "\n")
    log("==== done. Tell Claude 'done'.")


if __name__ == "__main__":
    main()
