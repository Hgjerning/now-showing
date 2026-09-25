# -*- coding: utf-8 -*-
"""Shared helpers for the Project 10 'Now Showing / Now Playing' article series."""
import base64
import os
import re

import markdown

LIB = os.path.dirname(os.path.abspath(__file__))
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
BLUE, ORANGE, AQUA, GOLD, GREY, RED, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#8a8984", "#e34948", "#4a3aa7"


def mpl_style(plt):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                         "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                         "axes.grid": True, "grid.color": GRID, "grid.linewidth": 1, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.spines.left": False, "axes.axisbelow": True})


CSS = open(os.path.join(LIB, "style.css")).read()
TEASER_CSS = open(os.path.join(LIB, "teaser.css")).read()


def embed(html, figdir):
    for f in sorted(os.listdir(figdir)):
        html = html.replace(f"../figures/{f}", "data:image/png;base64," + base64.b64encode(open(os.path.join(figdir, f), "rb").read()).decode())
    return html


def write_article(root, stem, md, title):
    open(os.path.join(root, "article", f"{stem}.md"), "w").write(md)
    body = markdown.markdown(md, extensions=["tables", "fenced_code"]).replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"
    open(os.path.join(root, "article", f"{stem}.html"), "w").write(embed(html, os.path.join(root, "figures")))


def write_teaser(root, post, hero, title, date_label="September 2026"):
    """One-pager: the hero picture FIRST, then the post text."""
    open(os.path.join(root, "linkedin", "post.txt"), "w").write(post)
    paras = post.strip().split("\n\n")[:-1]
    hp = [f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paras]
    hp[-1] = hp[-1].replace("<p>", "<p class='link'>")
    html = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}: teaser</title><style>{TEASER_CSS}</style></head><body>"
            f"<img class='hero' src='../figures/{hero}' alt='{title}'><div class='by'>Henrik Gjerning · LinkedIn · {date_label}</div>{''.join(hp)}</body></html>")
    open(os.path.join(root, "linkedin", "teaser.html"), "w").write(embed(html, os.path.join(root, "figures")))


def image_first(teaser_path):
    """Retrofit an existing teaser.html so the first picture opens the page."""
    h = open(teaser_path).read()
    m = re.search(r"<img [^>]*>", h)
    if not m:
        return False
    img = m.group(0)
    h = h.replace(img, "", 1)
    img = img.replace("<img ", "<img class='hero' ", 1) if "class=" not in img else img
    h = h.replace("<body>", "<body>" + img, 1) if "<body>" in h else re.sub(r"(<body[^>]*>)", r"\1" + img, h, count=1)
    if "img.hero" not in h:
        h = h.replace("</style>", "img.hero{width:52%;display:block;margin:0 auto 12px;border-radius:4px}@media print{img.hero{width:50%}}</style>", 1)
    open(teaser_path, "w").write(h)
    return True


def make_pdfs(root, stem):
    from playwright.sync_api import sync_playwright
    jobs = [("linkedin/teaser.html", f"linkedin/{stem}_teaser.pdf"), (f"article/{stem}.html", f"article/{stem}.pdf")]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(color_scheme="light")
        for src, dst in jobs:
            if os.path.exists(os.path.join(root, src)):
                pg.goto("file://" + os.path.join(root, src)); pg.wait_for_load_state("networkidle")
                pg.pdf(path=os.path.join(root, dst), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()


def write_readme(root, title, scripts, extra=""):
    s = f"""# {title}

Project 10 article series *Now Showing / Now Playing*. Pre-registered (see PREREGISTRATION_*.md, TRIAL_LEDGER.md).

| path | what |
|---|---|
| figures/hero_*.png | the poster card, which is the LinkedIn picture and opens the one-pager |
| linkedin/post.txt, teaser.html, *_teaser.pdf | one-pager |
| article/*.md / .html / .pdf | deep article with tables, figures and references |
| code/ | {' → '.join(scripts)} |
| results/ | every number in the article (summary.json and CSVs) |

Shared helpers (`panel.py`, `features.py`, `stats.py`, `common.py`, `poster.py`) are in `Articles/_shared/lib10/`.
Raw Sharadar prices and fundamentals are licensed and are **not** included. Results files hold only derived statistics.
{extra}
Pipeline run: 25 September 2026.
"""
    open(os.path.join(root, "README.md"), "w").write(s)
