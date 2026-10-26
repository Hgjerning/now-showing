# -*- coding: utf-8 -*-
"""Print the teaser and the deep article to PDF with headless Chromium (light theme)."""
import os
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobs = [("linkedin/teaser.html", "linkedin/usual_suspects_teaser.pdf"), ("article/usual_suspects.html", "article/usual_suspects.pdf")]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(color_scheme="light")
    for src, dst in jobs:
        pg.goto("file://" + os.path.join(ROOT, src)); pg.wait_for_load_state("networkidle")
        pg.pdf(path=os.path.join(ROOT, dst), format="A4", print_background=True, prefer_css_page_size=True)
        print("wrote", dst)
    b.close()
