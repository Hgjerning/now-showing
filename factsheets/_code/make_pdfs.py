# -*- coding: utf-8 -*-
"""Re-render the PDFs of the rebuilt factsheets from their final HTML (after add_changed_box.py). 2026-10-02."""
import os

from add_changed_box import OUT, REBUILT

from playwright.sync_api import sync_playwright

stems = [f[:-5] for f in sorted(os.listdir(OUT)) if f.endswith(".html") and f.split("_")[0] in REBUILT]
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(color_scheme="light")
    for s in stems:
        pg.goto("file:///" + os.path.abspath(os.path.join(OUT, s + ".html")).replace("\\", "/")); pg.wait_for_load_state("networkidle")
        pg.pdf(path=os.path.join(OUT, s + ".pdf"), format="A4", print_background=True, prefer_css_page_size=True)
        print("pdf", s, flush=True)
    b.close()
