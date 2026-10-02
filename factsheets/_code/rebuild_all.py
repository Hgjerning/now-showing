# -*- coding: utf-8 -*-
"""Rebuild the factsheets on the corrected universe (2 October 2026; FACTSHEETS_RERUN_2026-10-02.md).

Basis: US = actual S&P 500 members (data.py default sp500_pit); UK/EU/DK = pit v2 panels, which include the members
that stopped trading; SCANDI = as registered, without Oslo (data.py default). World = US + UK + EU in USD.

1. Archives the published state once: results/, figures/, factsheets/ -> _published_2026-09-27/ (copies).
2. Re-runs every analysis step into results/ and figures/ (same steps as rerun_pit.py, plus figures and turtle_full).
3. Rebuilds FS00-FS14, FS16, FS18, FS20, FS21 (md + html; PDFs only if Playwright is installed).
   Not rebuilt: FS15 (ART history) and FS17 (non-US fundamentals) do not use these universes; FS19 needs the ART
   battery file, which is not on this PC. The trial ledger (results/trial_ledger.*) is not rewritten.
4. Inserts the dated "What changed" box (add_changed_box.py).
Resumable (factsheets/_rebuild_done.txt). Log: factsheets/_rebuild_log.txt. About 1.5-2 hours.
    cd "...\\Project10_Articles\\Factsheets\\code"
    & "C:\\Python314\\python.exe" rebuild_all.py
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARCH = ROOT / "_published_2026-09-27"
RS = ["US", "EU", "UK", "DK", "SC", "WD"]
STEPS = ([["signals.py", r] for r in RS] + [["signals2.py", r] for r in RS] + [["library.py", r] for r in RS]
         + [["run_lottery.py", r] for r in RS] + [["run_turtle.py", r] for r in RS] + [["turtle_fix.py", r] for r in RS]
         + [["turtle_full.py", r] for r in RS]
         + [["lottery_fix.py"], ["posthoc_lottery.py"], ["analyse.py", "turtle", "lottery"], ["fix_analysis.py"], ["diag_turtle.py"],
            ["cost_check.py"], ["neighbourhood.py", "max"], ["neighbourhood.py", "brk"], ["monkey.py"],
            ["analyse_xs.py", "FS03", "FS04", "FS06"], ["analyse_xs.py", "FS07", "FS08", "FS09"], ["analyse_xs.py", "FS10", "FS11", "FS12"],
            ["battery.py", "US", "EU", "UK"], ["battery.py", "DK", "SC"], ["battery.py", "WD"], ["jkp_battery.py"],
            ["financing.py"], ["common_ground.py"], ["fmb.py"], ["fund_battery.py"], ["fs14.py"], ["fs18.py"],
            ["fs19_engine.py"], ["fs20.py"], ["fs21.py"], ["impact.py"],
            ["nbh_figs.py"], ["make_figures.py"],
            ["build_factsheets.py"], ["build_xs.py"], ["build_monkey.py"], ["build_fs13.py"], ["build_fs13b.py"], ["build_fs13c.py"],
            ["build_fs14.py"], ["build_fs16.py"], ["build_fs18.py"], ["build_fs20.py"], ["build_fs21.py"], ["build_overview.py"],
            ["add_changed_box.py"], ["make_pdfs.py"],
            # 2026-10-02: LinkedIn teasers and the FS13 marketing kit (FS15/FS19 teasers unchanged), then the repo copy
            ["build_teasers.py"], ["build_teasers_xs.py"], ["teaser_fs14.py"], ["teaser_fs16.py"], ["teaser_fs18.py"],
            ["marketing_fs13.py"], ["sync_now_showing.py"]])
NEED = ["pandas", "scipy", "sklearn", "statsmodels", "cvxpy", "matplotlib", "pyarrow", "markdown"]


def log(m):
    print(m, flush=True)
    with open(ROOT / "factsheets" / "_rebuild_log.txt", "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + m + "\n")


def main():
    import importlib.util
    miss = [m for m in NEED if importlib.util.find_spec(m) is None]
    if miss:
        sys.exit("Missing packages: " + " ".join({"sklearn": "scikit-learn"}.get(m, m) for m in miss))
    if not ARCH.exists():
        for d in ("results", "figures", "factsheets"):
            shutil.copytree(ROOT / d, ARCH / d)
        (ARCH / "README.txt").write_text("The factsheets as published (built 26-27 Sep 2026), copied before the 2 Oct rebuild.\n", encoding="utf-8")
        log(f"archived the published state to {ARCH.name}/")
    done_f = ROOT / "factsheets" / "_rebuild_done.txt"
    done = set(done_f.read_text(encoding="utf-8").splitlines()) if done_f.exists() else set()
    env = {k: v for k, v in os.environ.items() if k not in ("FS_RESULTS", "FS_FIGURES", "FS_PIT_DIR", "FS_US_UNIVERSE", "FS_SC_OSLO")}
    env.update(MPLBACKEND="Agg", PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    (ROOT / "results" / "logs_rebuild").mkdir(exist_ok=True)
    for st in STEPS:
        key = " ".join(st)
        if key in done:
            continue
        t = time.time(); log(f"{key} ...")
        r = subprocess.run([sys.executable] + st, cwd=HERE, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (ROOT / "results" / "logs_rebuild" / (key.replace(" ", "_").replace(".py", "") + ".log")).write_text(r.stdout + "\n--- stderr ---\n" + r.stderr, encoding="utf-8")
        if r.returncode != 0:
            last = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "(no stderr)"
            log(f"{key} FAILED after {time.time() - t:.0f}s: {last}  (continuing)"); continue
        log(f"{key} ok in {time.time() - t:.0f}s")
        with open(done_f, "a", encoding="utf-8") as f:
            f.write(key + "\n")
    log("==== done. Tell Claude 'done'.")


if __name__ == "__main__":
    main()
