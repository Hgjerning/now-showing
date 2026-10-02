# -*- coding: utf-8 -*-
"""Insert the "US, 1999-2012" box (PREREG_US_1999_2012.md, run 2 October 2026) into the factsheets it tested, right after
the 2 October corrections box (md + html). Text is generated from results_us1999/ and the Project2 T7 result.
Idempotent: an existing US 1999-2012 box is replaced. Then: make_pdfs.py and sync_now_showing.py."""
import json, os, re
import specs

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
OUT, U99 = os.path.join(ROOT, "factsheets"), os.path.join(ROOT, "results_us1999")
P7 = os.path.join(ROOT, "..", "..", "Project2 Investment Strategy", "us_oos_1999_result.json")
MARK = "US, 1999–2012"
REF = " Pre-registration, method and every result: `PREREG_US_1999_2012.md`."
INTRO = (f"**{MARK} (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time "
         "S&P 500 with delisted stocks, 1999–2012, a period this factsheet was not built on. ")
J = lambda f: json.load(open(os.path.join(U99, f + ".json"), encoding="utf-8"))
FROZEN = {"FS01": (-3.96, -1.38), "FS02": (-2.17, 0.29), "FS03": (0.31, 1.74), "FS04": (-1.36, 1.73), "FS06": (-2.83, -3.17),
          "FS07": (-0.55, -2.66), "FS08": (-1.62, -4.06), "FS09": (-1.00, 0.05), "FS10": (1.17, 1.93), "FS11": (1.22, 2.30), "FS12": (-3.07, -2.94)}
EXTRA = {"FS01": " Negative in both halves (1999–2005 and 2006–2012): the most robust result in the whole series, and it is a loss.",
         "FS03": " US momentum shows nothing in 1999–2012, a period that includes the 2009 momentum crash.",
         "FS04": " The one positive long-only result that holds in both periods.",
         "FS06": " The 2013–2026 US loss did not repeat; it reads as specific to that period.",
         "FS11": " Positive in 2000–2005, negative in 2006–2012 (the 2009 momentum crash).",
         "FS12": " The 2013–2026 US losses did not repeat; they read as specific to that period."}


def word(old, new):
    if abs(old) < 1: return "no 2013–2026 effect to test"
    if (old > 0) != (new > 0): return "reversed"
    return "confirmed" if abs(new) > 2 else "same sign, weaker"


def text(code):
    T1 = {}; [T1.update(J(f)) for f in ("t1_turtle", "t1_lottery", "t1_xs")]
    if code in FROZEN:
        c = T1[code]; a, b = FROZEN[code]
        return (INTRO + f"L/S net: t {c['ls_t']:+.2f} (2013–2026: {a:+.2f}), {word(a, c['ls_t'])}. Long-only alpha vs the equal-weight "
                f"universe: {c['lo_alpha'] * 100:+.1f}% a year, t {c['lo_alpha_t']:+.2f} (2013–2026: {b:+.2f}), {word(b, c['lo_alpha_t'])}."
                + EXTRA.get(code, "") + " Registered verdicts are unchanged." + REF)
    if code == "FS13":
        d = J("t2_battery"); flip = [s for s, r in d["rows"].items() if r["same"] is False]
        return (INTRO + f"{d['kept']} of 19 signals keep their US sign in the beta-neutral book (the pass mark was 14): **fail**. "
                f"Signs that flipped: {', '.join(flip)}." + REF)
    if code == "FS13b":
        d = J("t3_fund"); pg = d["rows"]["c_profit_growth"]
        return (INTRO + f"{d['kept']} of 20 fundamental signals keep their long-only sign (the pass mark was 15): passes exactly at the bar, "
                "and the six composites are built from the fourteen single signals, so this is weaker evidence than 20 independent tests. "
                f"Profit growth, this factsheet's strongest US result: t {pg['new']:+.2f} (2013–2026: {pg['old']:+.2f})." + REF)
    if code == "FS13c":
        d = J("t4_fmb")
        return INTRO + f"12-1 momentum's multivariate slope: t {d['mom_t']:+.2f} (pass mark t > 2): **fail**." + REF
    if code == "FS18":
        d = J("t5_fs18")
        return INTRO + f"US overlay at $50m: {d['ann'] * 100:+.1f}% a year, t {d['t']:+.2f}: **fail**, as in 2013–2026." + REF
    if code == "FS20":
        p = J("t6_fs20")["variants"]["N12_annual_fcf"]; n2 = sum(v["capm"]["t"] > 2 for v in J("t6_fs20")["variants"].values())
        return (INTRO + f"Primary checklist: CAPM alpha {p['capm']['alpha'] * 100:+.1f}% a year, t {p['capm']['t']:+.2f}, positive in both halves "
                f"({p['h1']['alpha'] * 100:+.1f}% in 1999–2005, {p['h2']['alpha'] * 100:+.1f}% in 2006–2012): **passes the registered rule** "
                f"(2013–2026: −0.6%, t −0.24). {n2} of 12 variants have t > 2. Below the 2.87 gate used across these factsheets and below the "
                "programme-wide bar; it reads as value and quality recovering after the 2000 bubble, not as an edge that holds in every period." + REF)
    if code == "FS15":
        x = J("art_crosscheck")
        return (f"**{MARK}: a second source for this study's US cells (2 October 2026).** The pre-registered US re-run on Sharadar's "
                f"point-in-time S&P 500 (1999–2012) agrees in sign with this ART study for {x['same_sign']} of {x['n']} battery signals; "
                f"the correlation of the 19 t-values is {x['t_corr']:.2f}." + REF)
    if code == "FS00":
        t7 = json.load(open(P7, encoding="utf-8"))["decision"]
        return (INTRO.replace("this factsheet was", "these factsheets were") + "65 trials. What holds: the Turtle loss (FS01) and the "
                "low-volatility long-only alpha (FS04). What does not: momentum in every form (FS03, FS11, FS13c), and the 2013–2026 US "
                "losses for seasonality and the 52-week low. The checklist (FS20) passes in 1999–2012 only. The live book's US leg does "
                f"not replicate (alpha t {t7['t']:+.2f}, needed 2). The trial ledger now holds 772 trials (Bonferroni |t| > 3.99)." + REF)
    return None


def md_box(t):
    return "\n".join("> " + L for L in re.sub(r"(.{1,118})(\s|$)", r"\1\n", t).strip().split("\n"))


def html_box(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t); t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return f"<blockquote class='us1999'>{t}</blockquote>"


def main():
    for fn in sorted(os.listdir(OUT)):
        m = re.match(r"(FS\d\d[bc]?)_", fn)
        if not m or not fn.endswith(".md"): continue
        code = m.group(1); t = text(code)
        if not t: continue
        stem = fn[:-3]; p = os.path.join(OUT, fn); md = open(p, encoding="utf-8").read()
        md = re.sub(r"\n> \*\*" + re.escape(MARK) + r".*?(?=\n(?!> ))", "", md, flags=re.S)
        L = md.split("\n"); k = next((i for i, x in enumerate(L) if "What changed on 2 October 2026" in x), None)
        if k is not None:
            while k < len(L) and L[k].startswith(">"): k += 1
        else:
            k = next((i for i, x in enumerate(L) if x.startswith("# ")), 0) + 1
        L = L[:k] + ["", md_box(t)] + L[k:]
        open(p, "w", encoding="utf-8").write("\n".join(L))
        hf = os.path.join(OUT, stem + ".html")
        if os.path.exists(hf):
            h = open(hf, encoding="utf-8").read()
            h = re.sub(r"<blockquote class='us1999'>.*?</blockquote>", "", h, flags=re.S)
            if "<blockquote class='changed'>" in h:
                i = h.index("</blockquote>", h.index("<blockquote class='changed'>")) + len("</blockquote>")
            else:
                i = h.index("</h1>") + 5
            h = h[:i] + html_box(t) + h[i:]
            if ".us1999{" not in h:
                h = h.replace("</style>", "blockquote.us1999{border-left:4px solid #2a78d6;background:var(--box,#f3f2ee);padding:10px 14px;margin:12px 0;font-size:13px}</style>", 1)
            open(hf, "w", encoding="utf-8").write(h)
        print("US 1999-2012 box:", stem)


if __name__ == "__main__":
    main()
