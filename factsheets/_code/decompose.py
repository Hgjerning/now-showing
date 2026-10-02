# -*- coding: utf-8 -*-
"""Which change moved the factsheet numbers? (2026-10-01)

results_pit/ differs from the published results/ for two reasons at once:
  A. the US universe: actual S&P 500 members (sp500_pit) instead of the top 500 of every name ever in the index;
  B. the price panels: pit v2 of 2026-10-01 (fresh Yahoo prices for every member, Oslo added to SCANDI) instead of
     the 2026-09-26 panels (now in _data_private/pit/archive_2026-09-26).
This re-runs the sort factsheets (FS03-FS12) and FS18 for the two missing corners:
  v1_top500   -> should reproduce the published numbers (a check that nothing else changed)
  v1_pit      -> A alone
  v2_top500   -> B alone
(v2_pit = results_pit/, already done). Output: results_decomp/<variant>/. Published files are not touched.
Resumable. Run from Factsheets/code:   & "C:\\Python314\\python.exe" decompose.py      (about 1-1.5 hours)
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V1 = ROOT / "_data_private" / "pit" / "archive_2026-09-26"
VARIANTS = {"v1_top500": (V1, "top500"), "v1_pit": (V1, "sp500_pit"), "v2_top500": (None, "top500"),
            # 2026-10-02: Oslo split -- pit v2 + US fix, but SCANDI without Oslo (compare with results_pit = with Oslo)
            "v2_pit_noOslo": (ROOT / "_data_private" / "pit_v2_noOslo", "sp500_pit")}
RS = ["US", "EU", "UK", "DK", "SC", "WD"]
STEPS = ([["signals.py", r] for r in RS] + [["signals2.py", r] for r in RS]
         + [["analyse_xs.py", "FS03", "FS04", "FS06"], ["analyse_xs.py", "FS07", "FS08", "FS09"], ["analyse_xs.py", "FS10", "FS11", "FS12"],
            ["fs18.py"]])


def main():
    base = ROOT / "results_decomp"; base.mkdir(exist_ok=True)
    for name, (pit, us) in VARIANTS.items():
        out = base / name; out.mkdir(exist_ok=True); (out / "logs").mkdir(exist_ok=True)
        for f in (ROOT / "results").iterdir():
            if f.suffix in (".json", ".csv") and not (out / f.name).exists():
                shutil.copy2(f, out / f.name)
        done_f = out / "_done.txt"
        done = set(done_f.read_text(encoding="utf-8").splitlines()) if done_f.exists() else set()
        env = dict(os.environ, FS_RESULTS=str(out), FS_FIGURES=str(out / "figures"), FS_US_UNIVERSE=us, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
        (out / "figures").mkdir(exist_ok=True)
        env.pop("FS_PIT_DIR", None)
        if pit is not None:
            env["FS_PIT_DIR"] = str(pit)
        for st in STEPS:
            key = " ".join(st)
            if key in done:
                continue
            t = time.time(); print(f"[{name}] {key} ...", flush=True)
            r = subprocess.run([sys.executable] + st, cwd=HERE, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
            (out / "logs" / (key.replace(" ", "_").replace(".py", "") + ".log")).write_text(r.stdout + "\n--- stderr ---\n" + r.stderr, encoding="utf-8")
            if r.returncode != 0:
                print(f"[{name}] {key} FAILED: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''}", flush=True); continue
            print(f"[{name}] {key} ok in {time.time() - t:.0f}s", flush=True)
            with open(done_f, "a", encoding="utf-8") as f:
                f.write(key + "\n")
    print("==== done. Tell Claude 'done'.")


if __name__ == "__main__":
    main()
