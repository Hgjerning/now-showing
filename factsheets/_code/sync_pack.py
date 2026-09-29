# -*- coding: utf-8 -*-
"""Pack the device folder Factsheets/ and the repo copy now-showing/factsheets/ into zip parts (< 19 MB) for transfer.
Private data never leaves: no data/, no factors/, no pickles, no per-stock trade logs in the repo copy."""
import glob
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import specs

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ST = "/tmp/claude-0/-home-claude/4022484c-d15a-5588-a38a-9a59d3138178/scratchpad/syncall"
OUT = "/mnt/user-data/outputs"
U = "US EU UK DK SC WD".split()


def main():
    shutil.rmtree(ST, ignore_errors=True)
    F = f"{ST}/Factsheets"; N = f"{ST}/now-showing/factsheets"
    os.chdir(ROOT)
    for d in ["code", "factsheets", "figures", "teasers", "planning"]:
        shutil.copytree(d, f"{F}/{d}", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "Strategy_Factsheets_note.md"))
    os.makedirs(f"{F}/results")
    for f in glob.glob("results/*"):
        if f.endswith((".json", ".csv")):
            shutil.copy(f, f"{F}/results/")
    os.makedirs(f"{N}/_code/InvestmentLibrary")
    for f in glob.glob("code/*.py") + ["code/style.css"] + glob.glob("code/*.sh"):
        shutil.copy(f, f"{N}/_code/")
    for f in glob.glob("code/InvestmentLibrary/*.py"):
        shutil.copy(f, f"{N}/_code/InvestmentLibrary/")
    shutil.copy("planning/FACTSHEET_TRIAL_LEDGER.md", f"{N}/TRIAL_LEDGER.md")
    items = [("FS00", "fs00-overview-and-gaps", "FS00_Overview_and_Gap_Analysis", None, ["fs00_summary.json", "trial_ledger.json", "trial_ledger.csv"]),
             ("FS01", "fs01-turtle-traders", "FS01_Turtle_Traders", "fs01", ["fix_summary.json", "nbh_brk.json", "turtle_diagnostics.json", "turtle_summary.json", "turtle_cost_check.json"]),
             ("FS02", "fs02-lottery-max", "FS02_Lottery_MAX", "fs02", ["fix_summary.json", "nbh_max.json", "lottery_summary.json", "lottery_diagnostics.json", "lottery_posthoc.json"] + [f"lottery_monthly_record_{u}.csv" for u in U]),
             ("FS05", "fs05-monkey-portfolios", "FS05_Monkey_Portfolios", "fs05", ["monkey_summary.json"]),
             ("FS13", "fs13-signal-battery", "FS13_Signal_Battery", "fs13", ["common_ground.json", "battery_price.json", "battery_jkp_pooled.csv", "battery_jkp_factors.csv", "financing.json"]),
             ("FS13b", "fs13b-us-fundamentals", "FS13b_US_Fundamentals", None, ["fund_battery.json"]),
             ("FS13c", "fs13c-all-signals-together", "FS13c_All_Signals_Together", None, ["fmb.json"]),
             ("FS14", "fs14-multifactor-model", "FS14_Multifactor_Model", "fs14", ["fs14.json"]),
             ("FS15", "fs15-earlier-history", "FS15_Earlier_History", "fs15", ["art_battery.json", "art_fmb.json", "art_fs14.json"]),
             ("FS16", "fs16-costs-and-capacity", "FS16_Costs_And_Capacity", "fs16", ["impact.json", "impact_buffer.json", "impact_liquid.json"]),
             ("FS17", "fs17-fundamentals-outside-us", "FS17_Fundamentals_Outside_US", None, ["fs17.json"]),
             ("FS18", "fs18-portfolio-i-would-run", "FS18_Portfolio_I_Would_Run", "fs18", ["fs18.json"]),
             ("FS19", "fs19-robustness", "FS19_Robustness", "fs19", ["fs19.json", "fs19_engine.json"])]
    for c in specs.ORDER:
        stem = os.path.basename(glob.glob(f"factsheets/{c}_*.md")[0])[:-3]
        items.append((c, specs.S[c]["slug"], stem, c.lower(), [f"xs_{c}.json"] + [f"xs_{c}_record_{u}.csv" for u in U]))
    for c, slug, stem, t, res in sorted(items):
        d = f"{N}/{slug}"; os.makedirs(f"{d}/results")
        shutil.copy(f"factsheets/{stem}.md", f"{d}/factsheet.md"); shutil.copy(f"factsheets/{stem}.pdf", f"{d}/factsheet.pdf"); shutil.copy(f"factsheets/{stem}.html", f"{d}/index.html")
        if t:
            for src, dst in [(f"teasers/{t}_card.png", "card.png"), (f"teasers/{t}_post.txt", "post.txt"), (f"teasers/{t}_teaser.pdf", "teaser.pdf")]:
                if os.path.exists(src):
                    shutil.copy(src, f"{d}/{dst}")
        for r in res:
            shutil.copy(f"results/{r}", f"{d}/results/")
    shutil.copy("planning/PREREG_FS14.md", f"{N}/fs14-multifactor-model/PREREGISTRATION.md")
    shutil.copy("planning/PREREG_FS15.md", f"{N}/fs15-earlier-history/PREREGISTRATION.md")
    shutil.copy("planning/PREREG_FS16.md", f"{N}/fs16-costs-and-capacity/PREREGISTRATION.md")
    shutil.copy("planning/PREREG_FS17.md", f"{N}/fs17-fundamentals-outside-us/PREREGISTRATION.md")
    shutil.copy("planning/PREREG_FS18.md", f"{N}/fs18-portfolio-i-would-run/PREREGISTRATION.md")
    shutil.copy("planning/PREREG_FS19.md", f"{N}/fs19-robustness/PREREGISTRATION.md")
    os.makedirs(f"{N}/fs13-signal-battery/marketing", exist_ok=True)
    for f in ["fs13_carousel_linkedin.pdf", "fs13_x_thread.txt", "fs13_newsletter.md", "MARKETING_KIT.md", "series_launch_post.txt"]:
        shutil.copy(f"teasers/marketing/{f}", f"{N}/fs13-signal-battery/marketing/")
    for p in glob.glob(f"{OUT}/fs_all.part*"):
        os.remove(p)
    subprocess.run(f"cd {ST} && zip -qr {OUT}/fs_all.zip Factsheets now-showing && cd {OUT} && split -b 19m -d fs_all.zip fs_all.part && rm fs_all.zip", shell=True, check=True)
    print(sorted(os.path.basename(p) for p in glob.glob(f"{OUT}/fs_all.part*")))


if __name__ == "__main__":
    main()
