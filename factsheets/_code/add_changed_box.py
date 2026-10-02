# -*- coding: utf-8 -*-
"""Insert the dated "What changed on 2 October 2026" box into every rebuilt factsheet (md + html), right after the
title, and re-append the FS01 "100% invested" addendum (results/turtle_full_*.json). Idempotent: a factsheet that
already carries the box is left alone. Run after the builders (rebuild_all.py does)."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
OUT, RES = os.path.join(ROOT, "factsheets"), os.path.join(ROOT, "results")
MARK = "What changed on 2 October 2026"
REBUILT = ["FS00", "FS01", "FS02", "FS03", "FS04", "FS05", "FS06", "FS07", "FS08", "FS09", "FS10", "FS11", "FS12",
           "FS13", "FS13b", "FS13c", "FS14", "FS16", "FS18", "FS20", "FS21"]
BOX = f"""> **{MARK}.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.{{extra}}
"""
EXTRA = {"FS18": " **FS18 on the corrected universe: t 1.72 (published 1.85), still below the gate.**",
         "FS06": " On the corrected universe the pooled holdout spread is more clearly negative (t −2.21): beyond 2, though not past this factsheet's 2.87 gate."}


def box_md(code):
    return BOX.replace("{extra}", EXTRA.get(code, ""))


def box_html(code):
    t = box_md(code).replace("> ", "").replace("\n>", " ").strip()
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t); t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t); t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return f"<blockquote class='changed'>{t}</blockquote>"


def turtle_addendum():
    rows = []
    for R in ["US", "EU", "UK", "DK", "SC", "WD"]:
        f = os.path.join(RES, f"turtle_full_{R}.json")
        if not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        for name, b in d["books"].items():
            a, c = b["raw"]["full"], b["invested_100"]["full"]; ah, ch = b["raw"]["holdout"], b["invested_100"]["holdout"]
            rows.append(f"| {R} | {name} | {b['avg_invested_raw']:.0%} | {a['cagr']:+.1%} / {c['cagr']:+.1%} | {a['sharpe']:.2f} / {c['sharpe']:.2f} | "
                        f"{a['maxdd']:.0%} / {c['maxdd']:.0%} | {ah['sharpe']:.2f} / {ch['sharpe']:.2f} |")
    if not rows:
        return ""
    return ("\n\n## Addendum: the long-only books at 100% invested\n\nThe Turtle rules size each position by risk (0.1% of equity per N) "
            "and leave the rest in cash at 0%. Here every position is scaled by the same factor so the long book is 100% of equity at "
            "every close (`code/turtle.py: fully_invested`, `code/turtle_full.py`); re-scaling is charged 10 bp on the notional it moves; "
            "days with no position stay in cash. Same four pre-declared steps, 2013–2026; a restatement, not a new trial.\n\n"
            "| Universe | Long-only book | Invested as designed | CAGR, as designed / 100% | Sharpe, as designed / 100% | Max drawdown, as designed / 100% | Holdout 2020+ Sharpe, as designed / 100% |\n"
            "|---|---|---:|---:|---:|---:|---:|\n" + "\n".join(rows) +
            "\n\n**Reading.** The books are already mostly invested, so scaling adds little exposure but a lot of concentration on the days "
            "the system holds only one or two names (after mass exits in sell-offs). That is where the extra drawdown comes from. "
            "A fully invested Turtle book would need a minimum number of positions or a cap on the scale factor: a new, pre-declared specification.\n")


def main():
    import markdown
    for fn in sorted(os.listdir(OUT)):
        m = re.match(r"(FS\d\d[bc]?)_", fn)
        if not m or m.group(1) not in REBUILT or not fn.endswith(".md"):
            continue
        code, stem = m.group(1), fn[:-3]
        md = open(os.path.join(OUT, fn), encoding="utf-8").read()
        if MARK in md:
            continue
        lines = md.split("\n"); i = next((k for k, L in enumerate(lines) if L.startswith("# ")), 0)
        j = i + 1
        while j < len(lines) and (lines[j].startswith("#") or lines[j].startswith("*") or not lines[j].strip()) and j < i + 6:
            j += 1
        add = turtle_addendum() if code == "FS01" else ""
        md = "\n".join(lines[:j] + [box_md(code)] + lines[j:]) + add
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(md)
        hf = os.path.join(OUT, stem + ".html")
        if os.path.exists(hf):
            h = open(hf, encoding="utf-8").read()
            if MARK not in h:
                h = h.replace("</h1>", "</h1>" + box_html(code), 1)
                if add:
                    h = h.replace("</body>", markdown.markdown(add, extensions=["tables"]).replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>") + "</body>", 1)
                if ".changed{" not in h:
                    h = h.replace("</style>", "blockquote.changed{border-left:4px solid #eb6834;background:var(--box,#f6f4ef);padding:10px 14px;margin:12px 0;font-size:13px}</style>", 1)
                open(hf, "w", encoding="utf-8").write(h)
        print("box added:", stem)


if __name__ == "__main__":
    main()
