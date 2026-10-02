# -*- coding: utf-8 -*-
"""Copy the rebuilt factsheets, teasers and derived results into the repo copy now-showing/factsheets/ (2026-10-02).

Only files that already exist in each now-showing/factsheets/<slug>/ folder are replaced (same names, same layout):
factsheet.md / index.html / factsheet.pdf, card.png / post.txt / teaser.pdf, results/<derived files>, marketing/*.
Folders for factsheets that were not rebuilt (FS15, FS17, FS19) are left alone; FS20/FS21 have no folder there yet.
_code/: replaces the scripts that are there and adds the 1-2 Oct pipeline scripts. Never copies data, caches or
anything from _data_private. Prints every file it writes."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__)); FS = os.path.join(HERE, "..")
NS = os.path.normpath(os.path.join(FS, "..", "now-showing", "factsheets"))
REBUILT = ["FS00", "FS01", "FS02", "FS03", "FS04", "FS05", "FS06", "FS07", "FS08", "FS09", "FS10", "FS11", "FS12",
           "FS13", "FS13b", "FS13c", "FS14", "FS16", "FS18", "FS20", "FS21"]
NEW_CODE = ["rebuild_all.py", "us1999_run.py", "add_us1999_box.py", "ledger.py", "add_changed_box.py", "make_pdfs.py", "decompose.py", "rerun_pit.py", "turtle_full.py",
            "us_universe_check.py", "sync_now_showing.py"]
n = 0


def cp(src, dst):
    global n
    if os.path.exists(src):
        shutil.copy2(src, dst); n += 1; print("  ", os.path.relpath(dst, NS))


def main():
    sheets = {f.split("_")[0]: f.rsplit(".", 1)[0] for f in os.listdir(os.path.join(FS, "factsheets")) if f.endswith(".md") and f.startswith("FS")}
    for code in REBUILT:
        slug = next((d for d in os.listdir(NS) if d.startswith(code.lower() + "-")), None)
        if slug is None or code not in sheets:
            print(code, "-> no folder in now-showing, skipped"); continue
        d, stem, t = os.path.join(NS, slug), sheets[code], code.lower()
        print(code, "->", slug)
        for src, name in ((f"{stem}.md", "factsheet.md"), (f"{stem}.html", "index.html"), (f"{stem}.pdf", "factsheet.pdf")):
            cp(os.path.join(FS, "factsheets", src), os.path.join(d, name))
        for src, name in ((f"{t}_card.png", "card.png"), (f"{t}_post.txt", "post.txt"), (f"{t}_teaser.pdf", "teaser.pdf")):
            if os.path.exists(os.path.join(d, name)):
                cp(os.path.join(FS, "teasers", src), os.path.join(d, name))
        for sub, srcdir in (("results", os.path.join(FS, "results")), ("marketing", os.path.join(FS, "teasers", "marketing"))):
            if os.path.isdir(os.path.join(d, sub)):
                for f in os.listdir(os.path.join(d, sub)):
                    cp(os.path.join(srcdir, f), os.path.join(d, sub, f))
    code_dir = os.path.join(NS, "_code")
    print("_code")
    for f in sorted(set(os.listdir(code_dir)) | set(NEW_CODE)):
        if f.endswith(".py"):
            cp(os.path.join(HERE, f), os.path.join(code_dir, f))
    for f in ("FACTSHEETS_RERUN_2026-10-02.md", "US_UNIVERSE_CHECK_2026-10-01.md"):
        cp(os.path.join(FS, f), os.path.join(NS, f))
    # 2026-10-02: the US 1999-2012 pre-registration with its results, and the rebuilt trial ledger
    cp(os.path.join(FS, "planning", "PREREG_US_1999_2012.md"), os.path.join(NS, "PREREG_US_1999_2012.md"))
    cp(os.path.join(FS, "planning", "FACTSHEET_TRIAL_LEDGER.md"), os.path.join(NS, "TRIAL_LEDGER.md"))
    print(f"{n} files written")


if __name__ == "__main__":
    main()
