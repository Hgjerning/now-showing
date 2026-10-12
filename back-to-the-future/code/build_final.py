# -*- coding: utf-8 -*-
"""Render the hand-revised article (article/backtest_vs_reality.md, version 3) and the teaser (linkedin/post.txt) to HTML.
Replaces build_article.py, which generated the superseded version 1 (kept in code/_archive/)."""
import base64, os, re
import markdown
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FIG = os.path.join(ROOT, "figures")
def embed(html):
    for f in sorted(os.listdir(FIG)):
        html = html.replace(f"../figures/{f}", "data:image/png;base64," + base64.b64encode(open(os.path.join(FIG, f), "rb").read()).decode())
    return html
md = open(os.path.join(ROOT, "article", "backtest_vs_reality.md")).read()
CSS = open(os.path.join(ROOT, "code", "style.css")).read()
body = markdown.markdown(md, extensions=["tables", "fenced_code"]).replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
open(os.path.join(ROOT, "article", "backtest_vs_reality.html"), "w").write(embed(
    f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Back to the Future</title><style>{CSS}</style></head><body>{body}</body></html>"))
post = open(os.path.join(ROOT, "linkedin", "post.txt")).read()
paras = post.strip().split("\n\n")[:-1]
hp = [f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paras]; hp[-1] = hp[-1].replace("<p>", "<p class='link'>")
tcss = open(os.path.join(ROOT, "code", "teaser.css")).read() + "img.hero{width:52%;display:block;margin:0 auto 12px;border-radius:4px}@media print{img.hero{width:48%}}"
teaser = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Back to the Future: teaser</title><style>{tcss}</style></head><body>"
          f"<img class='hero' src='../figures/hero_back_to_the_future.png' alt='Back to the Future: now showing'><div class='by'>Henrik Gjerning · LinkedIn · 13 October 2026</div>{''.join(hp)}</body></html>")
open(os.path.join(ROOT, "linkedin", "teaser.html"), "w").write(embed(teaser))
print("words in teaser:", len(post.split()))
