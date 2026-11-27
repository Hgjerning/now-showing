# -*- coding: utf-8 -*-
"""Add the GoatCounter page counter to every published HTML page in now-showing.

Run before each push:  python _shared/add_analytics.py
Idempotent: pages that already carry the counter are left alone, so rebuilt pages
(whose builders do not add it) simply get it back. LinkedIn teaser/card pages are
skipped because they are rendered to images/PDFs, not published as pages.
Counter: https://hgjerning.goatcounter.com (no cookies, no personal data).
"""
import os
import sys
import time

CODE = "hgjerning"
MARK = "<!-- goatcounter -->"
TAG = (MARK + f'<script data-goatcounter="https://{CODE}.goatcounter.com/count" '
       'async src="https://gc.zgo.at/count.js"></script>')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "linkedin", "__pycache__"}


def main():
    t0 = time.time(); added = kept = nohead = 0
    print(f"{time.strftime('%H:%M:%S')} scanning {ROOT}")
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".html") or ".bak" in f:
                continue
            p = os.path.join(d, f)
            s = open(p, encoding="utf-8").read()
            if MARK in s:
                kept += 1; continue
            i = s.lower().find("</head>")
            if i < 0:
                nohead += 1; print("  no </head>, skipped:", os.path.relpath(p, ROOT)); continue
            open(p, "w", encoding="utf-8").write(s[:i] + TAG + s[i:])
            added += 1
    print(f"{time.strftime('%H:%M:%S')} done in {time.time() - t0:.1f}s: added {added}, already had it {kept}, skipped {nohead}")


if __name__ == "__main__":
    sys.exit(main())
