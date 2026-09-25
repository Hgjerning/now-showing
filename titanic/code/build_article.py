# -*- coding: utf-8 -*-
"""Render Case 1 'Every bubble rhymes' (teaser + deep article) from ../results. No result typed in."""
import base64
import json
import os

import markdown
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES, FIG = os.path.join(ROOT, "results"), os.path.join(ROOT, "figures")
S = json.load(open(os.path.join(RES, "summary.json"))); X = json.load(open(os.path.join(RES, "reported_extra.json")))
B = json.load(open(os.path.join(RES, "breadth.json")))
REPO = "hgjerning.github.io/now-showing/titanic"
pc = lambda v, d=0: f"{v * 100:+.{d}f}%"
L = {r["name"]: r for r in S["legibility"]}; t1, t2 = S["trials"]["C1-1"], S["trials"]["C1-2"]
c3, gr, gs, sp = S["C1-3"], S["gsy_reported"], S["gsy_splits"], S["sp500_now"]
ai = pd.DataFrame(S["ai_today"]); buckets = pd.read_csv(os.path.join(RES, "gsy_by_runup_bucket.csv"))
rh = X["rhyme"]; nv = X["NVDA"]
names = {"NVDA": "NVIDIA", "AVGO": "Broadcom", "AMD": "AMD", "MSFT": "Microsoft", "META": "Meta", "GOOGL": "Alphabet", "AMZN": "Amazon", "ORCL": "Oracle", "QQQ": "Nasdaq-100 (QQQ)", "SPY": "S&P 500 (SPY)", "AI basket": "**AI-leaders basket**"}
eps = lambda r: "; ".join(f"{a} → {b}" for a, b in r["episodes"]) or "none"
dbl = ai[(ai.run24 >= 1.0) & ai.name.isin(names) & ~ai.name.isin(["QQQ", "SPY", "AI basket"])].sort_values("run24", ascending=False)

def bucket_for(r):
    for b in buckets.itertuples():
        lo, hi = b.bucket.split("..")
        lo = -1e9 if lo == "<" else float(lo); hi = 1e9 if hi == "+" else float(hi)
        if lo <= r < hi:
            return b.crash
    return float("nan")

# ------------------------------------------------------------------ tables
T1 = "| Episode | Months | GSADF | 95% critical value | Explosive phase(s) dated by BSADF | Covers peak − 3 months? | Verdict |\n|---|---:|---:|---:|---|---|---|\n"
T1 += "\n".join(f"| {r['name']} (peak {r['peak']}) | {r['T']} | {r['gsadf']:.2f} | {r['gsadf_cv']:.2f} | {eps(r)} | {'yes' if r['covers_check'] else 'no'} ({r['check_month']}) | {'**pass**' if r['passes'] else '**fail**'} |" for r in S["legibility"])
T2 = "| Trial | Series | Sample | GSADF | Critical value (98.33%) | MC p | BSADF, last month | Critical value, last month | Explosive episodes dated | Verdict |\n|---|---|---|---:|---:|---:|---:|---:|---|---|\n"
for tid, r in (("C1-1", t1), ("C1-2", t2)):
    T2 += f"| {tid} | {r['name']} | {r['start']} → {r['end']} | {r['gsadf']:.2f} | {r['gsadf_cv']:.2f} | {r['gsadf_p']:.3f} | {r['last_bsadf']:.2f} | {r['last_cv']:.2f} | {eps(r)} | {'PASS' if r['passed'] else 'fail'} |\n"
T2 += f"| (reported) | NVIDIA | 2011-06 → {S['as_of']} | {nv['gsadf']:.2f} | {nv['gsadf_cv']:.2f} (95%) | {nv['gsadf_p']:.3f} | {nv['last_bsadf']:.2f} | {nv['last_cv']:.2f} | {eps(nv)} | explosive before, not now |\n"
T2 += f"| (reported) | S&P 500 | {sp['start']} → {sp['end']} | {sp['gsadf']:.2f} | {sp['gsadf_cv']:.2f} (95%) | {sp['gsadf_p']:.3f} | {sp['last_bsadf']:.2f} | {sp['last_cv']:.2f} | {eps(sp)} | a flicker, not a pass |"
T3 = "| | Two-year run-up before the event | Crash probability (40% fall within 24 months) | n | z | p (one-sided) |\n|---|---|---:|---:|---:|---:|\n"
T3 += f"| **C1-3** | ≥ 100% | **{c3['p_event'] * 100:.1f}%** vs {c3['p_ctrl'] * 100:.1f}% | {c3['n_event']:,} vs {c3['n_ctrl']:,} | {c3['z']:.1f} | {c3['p_one_sided']:.1e} |\n"
for k, lab in (("half_2013_2019", "2013–2019 events"), ("half_2020_2024", "2020–2024 events")):
    h = c3[k]; T3 += f"| {lab} | ≥ 100% | {h['p_event'] * 100:.1f}% vs {h['p_ctrl'] * 100:.1f}% | {h['n_event']:,} vs {h['n_ctrl']:,} | {h['z']:.1f} | {h['p_one_sided']:.1e} |\n"
a150 = gr["at150"]; T3 += f"| reported | ≥ 150% | {a150['p_event'] * 100:.1f}% vs {a150['p_ctrl'] * 100:.1f}% | {a150['n_event']:,} vs {a150['n_ctrl']:,} | {a150['z']:.1f} | {a150['p_one_sided']:.1e} |"
T4 = f"""| After a ≥100% run-up vs all windows | Event | Control | Welch t | p |
|---|---:|---:|---:|---:|
| Mean return, next 12 months | {pc(gr['fwd12_event_mean'], 1)} | {pc(gr['fwd12_ctrl_mean'], 1)} | {gr['fwd12_welch'][0]:.2f} | {gr['fwd12_welch'][1]:.3f} |
| Mean return, next 24 months | {pc(gr['fwd24_event_mean'], 1)} | {pc(gr['fwd24_ctrl_mean'], 1)} | {gr['fwd24_welch'][0]:.2f} | {gr['fwd24_welch'][1]:.1e} |
| Median return, next 24 months | {pc(gr['fwd24_event_median'], 1)} | {pc(gr['fwd24_ctrl_median'], 1)} | | |
| Crash probability, high vs low **acceleration** (share of the run-up earned in the last 12 months) | {gs['accel_high'] * 100:.0f}% | {gs['accel_low'] * 100:.0f}% | | |
| Crash probability, high vs low **volatility** | {gs['vol_high'] * 100:.0f}% | {gs['vol_low'] * 100:.0f}% | | |"""
T5 = "| Two-year return | n | Crash probability | Mean 24-month return after |\n|---|---:|---:|---:|\n"
lbl = ["fell", "0 to 50%", "50 to 100%", "100 to 150%", "150% or more"]
T5 += "\n".join(f"| {l} | {r.n:,} | {r.crash * 100:.0f}% | {pc(r.fwd24)} |" for l, r in zip(lbl, buckets.itertuples()))
crate = lambda r: "n/a (index)" if r.name in ("QQQ", "SPY", "AI basket") else f"{bucket_for(r.run24) * 100:.0f}%"
T6 = "| Name | 24-month return | 12-month return | From peak | Peak month | Historical crash rate for this run-up bucket |\n|---|---:|---:|---:|---|---:|\n"
T6 += "\n".join(f"| {names[r.name]} | {pc(r.run24)} | {pc(r.run12)} | {pc(r.from_peak)} | {r.peak_month} | {crate(r)} |" for r in ai.itertuples())
T7 = "| Episode | Rise over the 60 months into the peak | 12 months after | 36 months after | Worst point within 36 months |\n|---|---:|---:|---:|---:|\n"
for k, v in rh.items():
    f = lambda x: "n/a" if x is None or x != x else pc(x)
    months = "" if v["first"] == -60 else f" (only {-v['first']} months of data)"
    T7 += f"| {k} | {pc(v['runup_to_peak'])}{months} | {f(v['after_12m'])} | {f(v['after_36m'])} | {f(v['trough_36m'])} |\n"

dbl_txt = ", ".join(f"{names[r.name]} ({pc(r.run24)})" for r in dbl.itertuples())
md = f"""# Titanic: every bubble was unsinkable. Is this one?

### A pre-registered bubble test of the AI boom, against Tokyo 1989, Nasdaq 2000 and 1929

![Now Showing](../figures/hero_titanic.png)

*Henrik Gjerning · Rude Investment Consulting · September 2026 · Project 10, Case 1*

> **In one paragraph.** Over the last five years an equal-weight basket of eight AI leaders rose **{pc(rh['AI-leaders basket, today']['runup_to_peak'])}**. The Nikkei rose {pc(rh['Nikkei 225, peak Dec 1989']['runup_to_peak'])} into its 1989 peak and the Nasdaq Composite {pc(rh['Nasdaq Composite, peak Mar 2000']['runup_to_peak'])} into March 2000. The gains are bubble-sized. I tested whether the *shape* is bubble-like with the Phillips–Shi–Yu GSADF test, which asks whether a price rises faster than any random walk can explain. The test dates Tokyo 1989 and Nasdaq 2000 in real time; it misses 1929 only because my data start 21 months before that peak. **Pre-registered result: neither the Nasdaq-100 nor the AI basket is explosive now** (basket GSADF p = {t2['gsadf_p']:.2f}, and no explosive phase since 2021). NVIDIA alone was explosive in 2024–25 and has since cooled. The second, older fact about bubbles holds strongly. Among {c3['n_event']:,} US stocks that doubled in two years, **{c3['p_event'] * 100:.0f}% then fell 40%** within the next two, against {c3['p_ctrl'] * 100:.0f}% for all stocks. Yet their average returns afterwards stayed positive. Three of the eight AI names meet that doubling test today.

**Statistics box.** Trials 3 (Bonferroni: 98.33% critical values; p < 0.0167). C1-1 Nasdaq-100: GSADF {t1['gsadf']:.2f} vs {t1['gsadf_cv']:.2f}, fail. C1-2 AI basket: GSADF {t2['gsadf']:.2f} vs {t2['gsadf_cv']:.2f} (MC p {t2['gsadf_p']:.3f}), fail. C1-3 crash probability after a doubling: {c3['p_event'] * 100:.1f}% vs {c3['p_ctrl'] * 100:.1f}%, z {c3['z']:.1f}, **pass**, both halves. Legibility: 2 of 3 historic bubbles dated. Monte Carlo critical values: 2,000 draws per sample length, seed 42. Programme trial count: 20.

![Figure 1](../figures/fig1_every_bubble_rhymes.png)

---

## 1. Why ask, and why now

Whether AI is a bubble is the market question of 2026. Most answers are analogies: price charts overlaid on 1999, or valuation multiples set against Cisco. Analogies rhyme by construction, because any strong rally looks like the first half of a bubble. This article instead applies the two most-tested empirical definitions of a bubble. Before running anything, it writes down what would count as a yes.

**Definition 1: explosiveness.** Under rational pricing, a log price should behave at worst like a random walk with drift. A bubble makes it grow *explosively*, faster than any such walk. Phillips, Wu & Yu (2011) and Phillips, Shi & Yu (2015) built recursive right-tailed unit-root tests (SADF, GSADF) that detect this and date it in real time. The BSADF statistic at each month uses only data up to that month.

**Definition 2: what happens after a run-up.** Fama (2014) argues that "bubble" should mean *predictably* negative returns after a run-up. Greenwood, Shleifer & You (2019, "Bubbles for Fama") tested this on US industries since 1926. A 100% two-year run-up does not predict negative average returns, but it sharply raises the probability of a crash, and acceleration, volatility and issuance raise it further.

## 2. Pre-registration

The specification (`PREREGISTRATION_C1_2026-09-25.md`) was written before any statistic was computed. It fixes the series, the AI basket's eight members, the lag, the Monte Carlo, three trials with a Bonferroni gate, and a **legibility check**. The legibility check says the tool must date at least two of three known bubbles, or its verdict on AI is not read. My predictions:

- C1-1 (Nasdaq-100 explosive now) fails.
- C1-2 (AI basket explosive now) is about 50/50.
- C1-3 (crash probability after a doubling) passes.
- Returns after run-ups are not significantly lower.

## 3. Can the test recognise a bubble?

**Table 1. Legibility: dating the famous three**

{T1}

The test dates Tokyo from 1984 to mid-1990 and the Nasdaq from June 1999 to April 2000, before both peaks. It **misses 1929**. My S&P 500 series starts in December 1927, only 21 months before the peak, which is shorter than the test's minimum window at that sample size. It flags the 1932 rebound instead. The pre-registration allows one miss.

![Figure 2](../figures/fig2_bsadf_panels.png)

## 4. Is the AI boom explosive now?

**Table 2. The trials, plus two reported series**

{T2}

**Neither trial passes, and not narrowly.** The AI basket's explosive phases, as the test dates them, were 2013–14, 2016–18 and late 2021, not 2023–26. That sounds wrong until you look at the arithmetic. The basket compounded quickly for the whole fifteen years, so its recent gains are large but not *faster than its own history*. That is what explosiveness measures. NVIDIA is the one name that did go explosive in this cycle, twice in 2024–25, and its BSADF has since fallen back below the critical value. The S&P 500 shows a six-month flicker above its 95% line since April 2026. With a whole-sample GSADF p of {sp['gsadf_p']:.2f}, that is a watch item, not a result.

Robustness: with 0 lags instead of 1, and at the 95% level instead of 98.33%, the trial verdicts are unchanged.

## 5. The rhyme, and what it assumes

**Table 3. Sixty months into the peak, and after**

{T7}

The hero chart aligns every episode at its peak and treats *today* as the AI basket's peak. That is the worst case for AI by construction, and it is what analogy charts do without saying so. On the way up the AI run sits between Tokyo and the Nasdaq. What followed the historic peaks was a 57–85% fall within three years. **The chart cannot tell you whether today is a peak. Only the explosiveness test addresses that, and it says the shape of the last three years is not the shape of 1989 or 1999.**

## 6. What happens after a run-up: Greenwood–Shleifer–You on US stocks

**Table 4. Trial C1-3, crash probability after a doubling**

{T3}

**Table 5. By size of the run-up (reported)**

{T5}

![Figure 3](../figures/fig3_gsy_crash_by_runup.png)

**Table 6. Returns and characteristics after a doubling (reported)**

{T4}

This replicates GSY's central finding at the stock level. After a doubling, the chance of a 40% crash is materially higher, and higher still after a 150% run and in fast-accelerating, high-volatility names. Their second finding needs a qualifier. Returns after a run-up are **not negative**: the mean was {pc(gr['fwd24_event_mean'])} over 24 months. But they are significantly **lower** than for other stocks, and the median is only {pc(gr['fwd24_event_median'])}. **My prediction that they would not differ was wrong.**

Two cautions. First, the panel contains only today's listed stocks. Firms that crashed and were delisted are missing, so crash rates are understated and forward returns overstated. Second, a 40% drawdown is partly a volatility measure: the "fell" bucket crashes often too, because falling stocks are volatile stocks.

## 7. Relevance: the AI names today, and how broad the mania is

**Table 7. The eight AI leaders, as of {S['as_of']}**

{T6}

By the GSY yardstick, the names that meet the doubling test are {dbl_txt}. In the panel, stocks with run-ups like these went on to fall 40% within two years in {buckets.crash.iloc[3] * 100:.0f}–{buckets.crash.iloc[4] * 100:.0f}% of cases. The basket itself (+{ai.loc[ai.name == 'AI basket', 'run24'].iloc[0] * 100:.0f}% over 24 months, {pc(ai.loc[ai.name == 'AI basket', 'from_peak'].iloc[0])} from its peak) does not meet it.

![Figure 4](../figures/fig4_breadth_of_doublings.png)

**Breadth.** GSY also find that bubbles come with broad participation and new issuance. Today {B['share_now']:.1f}% of the US stocks in the panel have doubled over two years. The panel average is {B['share_mean']:.1f}%, and the peak was {B['share_max']:.0f}% in {B['share_max_date']}, the post-Covid rebound. The market is above its average, but nowhere near a broad mania.

## 8. What this does and does not show

- **Not a valuation study.** No earnings or dividend data are used, because the sandbox has no access to them. PSY originally applied the test to the price-dividend ratio. On log prices the test can confuse a strong fundamental trend with a bubble, and here it did the opposite: it declined to call one.
- **The AI basket was chosen ex post** as today's leaders. That biases *towards* finding a bubble, and none was found.
- **One legibility miss** (1929), explained by the data window.
- **Survivorship** in the stock panel understates crash rates.
- **Not a timing signal.** An explosiveness test says whether a price path is unusual, not when it ends.

## 9. So, does this one rhyme?

In size, yes: five years, +300%, between Tokyo and the Nasdaq. In shape, not yet: the statistic that dated both of those bubbles in real time does not fire on the AI basket or the Nasdaq-100 today. What the data do say is that individual names after a doubling carry crash risk of roughly one in two. That is a statement about position sizing, not about the index.

## Reproduce

```bash
python code/run_bubbles.py      # legibility, C1-1, C1-2, C1-3 (about 4 minutes, Monte Carlo)
python code/reported_extra.py   # NVIDIA and AMD, rhyme paths
python code/make_figures.py && python code/build_article.py && python code/make_pdfs.py
```

## References

- Brunnermeier, M. K. & Nagel, S. (2004). Hedge funds and the technology bubble. *Journal of Finance*, 59(5).
- Diba, B. T. & Grossman, H. I. (1988). Explosive rational bubbles in stock prices? *American Economic Review*, 78(3).
- Fama, E. F. (2014). Two pillars of asset pricing. *American Economic Review*, 104(6).
- Greenwood, R., Shleifer, A. & You, Y. (2019). Bubbles for Fama. *Journal of Financial Economics*, 131(1).
- Homm, U. & Breitung, J. (2012). Testing for speculative bubbles in stock markets: a comparison of alternative methods. *Journal of Financial Econometrics*, 10(1).
- Kindleberger, C. P. & Aliber, R. Z. (2011). *Manias, Panics and Crashes* (6th ed.). Palgrave Macmillan.
- Ofek, E. & Richardson, M. (2003). DotCom mania: the rise and fall of internet stock prices. *Journal of Finance*, 58(3).
- Pástor, Ľ. & Veronesi, P. (2009). Technological revolutions and stock prices. *American Economic Review*, 99(4).
- Phillips, P. C. B., Wu, Y. & Yu, J. (2011). Explosive behavior in the 1990s Nasdaq: when did exuberance escalate asset values? *International Economic Review*, 52(1).
- Phillips, P. C. B., Shi, S. & Yu, J. (2015). Testing for multiple bubbles: historical episodes of exuberance and collapse in the S&P 500. *International Economic Review*, 56(4).
- Shiller, R. J. (2000). *Irrational Exuberance*. Princeton University Press.

*Not investment advice.*
"""
open(os.path.join(ROOT, "article", "every_bubble_rhymes.md"), "w").write(md)

bask = ai.loc[ai.name == "AI basket"].iloc[0]
post = f"""TITANIC: every bubble was unsinkable. Is this one?

Over the last five years, an equal-weight basket of eight AI leaders (NVIDIA, Broadcom, AMD, Microsoft, Meta, Alphabet, Amazon, Oracle) rose {rh['AI-leaders basket, today']['runup_to_peak'] * 100:.0f}%. The Nikkei rose {rh['Nikkei 225, peak Dec 1989']['runup_to_peak'] * 100:.0f}% into its 1989 peak. The Nasdaq rose {rh['Nasdaq Composite, peak Mar 2000']['runup_to_peak'] * 100:.0f}% into 2000.

So I ran the test that dated both of those bubbles in real time: Phillips-Shi-Yu's GSADF, which asks whether a price is rising faster than any random walk can explain. It caught Tokyo and the Nasdaq before their peaks. (It missed 1929. My data start too late.)

On the AI basket today: not explosive (p = {t2['gsadf_p']:.2f}), and nothing flagged since 2021. NVIDIA alone was explosive in 2024-25 and has since cooled. The Nasdaq-100: nothing.

Then the part that matters for a portfolio. Of {c3['n_event']:,} US stocks that doubled in two years, {c3['p_event'] * 100:.0f}% then fell 40% within the next two, against {c3['p_ctrl'] * 100:.0f}% for all stocks. After a 150% run: {a150['p_event'] * 100:.0f}%. Yet average returns afterwards stayed positive.

Today {len(dbl)} of the 8 AI names meet that doubling test: {dbl_txt}.

So: a boom with bubble-sized gains, but not a bubble-shaped path. The statistics point to crash risk in individual names rather than a collapse of the whole group.

All three tests were pre-registered before I looked. Code, tables and the pre-registration: {REPO}

#AI #investing #markets #bubbles #statistics
"""
open(os.path.join(ROOT, "linkedin", "post.txt"), "w").write(post)

CSS = open(os.path.join(ROOT, "code", "style.css")).read()
def embed(html):
    for f in sorted(os.listdir(FIG)):
        html = html.replace(f"../figures/{f}", "data:image/png;base64," + base64.b64encode(open(os.path.join(FIG, f), "rb").read()).decode())
    return html
body = markdown.markdown(md, extensions=["tables", "fenced_code"]).replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
open(os.path.join(ROOT, "article", "every_bubble_rhymes.html"), "w").write(embed(
    f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Every bubble rhymes</title><style>{CSS}</style></head><body>{body}</body></html>"))
paras = post.strip().split("\n\n")[:-1]
hp = [f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paras]; hp[-1] = hp[-1].replace("<p>", "<p class='link'>")
teaser = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Every bubble rhymes: teaser</title><style>{open(os.path.join(ROOT, 'code', 'teaser.css')).read()}</style></head><body>
<div class='by'>Henrik Gjerning · LinkedIn · 6 October 2026</div>{hp[0]}<img src='../figures/hero_titanic.png' alt='Titanic: now showing'>{''.join(hp[1:])}</body></html>"""
open(os.path.join(ROOT, "linkedin", "teaser.html"), "w").write(embed(teaser))
print(post); print("words:", len(post.split()))

# ---- picture first: the hero card opens the one-pager (series rule, 2026-09-25)
import re as _re
_tp = os.path.join(ROOT, "linkedin", "teaser.html")
_h = open(_tp).read(); _m = _re.search(r"<img [^>]*>", _h)
if _m:
    _img = _m.group(0); _h = _h.replace(_img, "", 1)
    _h = _re.sub(r"(<body[^>]*>)", lambda mm: mm.group(1) + _img.replace("<img ", "<img class='hero' ", 1), _h, count=1)
    _h = _h.replace("</style>", "img.hero{width:52%;display:block;margin:0 auto 12px;border-radius:4px}@media print{img.hero{width:48%}}</style>", 1)
    open(_tp, "w").write(_h)
