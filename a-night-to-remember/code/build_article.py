# -*- coding: utf-8 -*-
"""Render A68 'A Night to Remember' (teaser + article + PDFs). Reads results/ and code/article_template.md only.
Before rendering, every key number in the template is checked against the results files; a mismatch stops the build.
Order:  base_rates.py -> make_figures.py -> make_teaser_drawing.py -> build_article.py
(run_fr_ai_1_line2.py is the registered run of line 2. It was run once on 21 Nov 2026 and refuses to run again.)"""
import json, os, sys
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "lib10"))
from common import click_layout, make_pdfs, write_article, write_readme, write_teaser  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RES = os.path.join(ROOT, "results"); ART = os.path.dirname(ROOT)
REPO = "hgjerning.github.io/now-showing/a-night-to-remember"; STEM = "a_night_to_remember"
J = json.load(open(os.path.join(RES, "base_rates_and_line1.json"))); C, L1, FAV = J["corrections"], J["line1"]["since_titanic_published_2026_10_06"], J["favourites"]
L2 = json.load(open(os.path.join(RES, "fr_ai_1_line2.json"))); F3 = pd.read_csv(os.path.join(RES, "fr_ai_1_line3_freeze_2026-10-30.csv"))
TH = json.load(open(os.path.join(ART, "A13_The_Devil_Wears_Prada", "results", "th1_summary.json")))
A52 = open(os.path.join(ART, "xx_A63_Raise_the_Titanic_Analogs", "TRIAL_LEDGER.md"), encoding="utf-8").read()
GATE = open(os.path.join(ART, "PROGRAMME_GATE.md"), encoding="utf-8").read()
md = open(os.path.join(ROOT, "code", "article_template.md"), encoding="utf-8").read()
# two sentences only Henrik can supply; left out, with a warning, until code/release_fields.json has them
RF = json.load(open(os.path.join(ROOT, "code", "release_fields.json"), encoding="utf-8"))
for key, mark in (("external_proof", "[EXTERNAL_PROOF]"), ("positions", "[POSITIONS]")):
    if not RF.get(key, "").strip(): print(f"NOT READY FOR RELEASE: '{key}' is empty in code/release_fields.json")
    md = md.replace(" " + mark, (" " + RF[key].strip()) if RF.get(key, "").strip() else "")
assert "[EXTERNAL_PROOF]" not in md and "[POSITIONS]" not in md
# 24 Nov 2026: dated update box (what happened after the signature). The body stays on the close of 20 Nov; the box, the byline
# note and one paragraph of the post come from results/update_after_signing.json (update_after_signing.py), text in update_box.py.
UPATH = os.environ.get("A68_UPDATE_JSON", os.path.join(RES, "update_after_signing.json"))
if not os.path.exists(UPATH): sys.exit("STOP: results/update_after_signing.json is missing. Run download_a68_update_prices.py, then update_after_signing.py.")
from update_box import render  # noqa: E402
U = json.load(open(UPATH)); UBOX, UBY, UPOST = render(U)
assert U["index"]["no_higher_close_since_6_oct"], "the index has closed above the 6 October high: section 1 says it has not"
assert md.count("[UPDATE_BOX]") == 1 and md.count("[UPDATE_BYLINE]") == 1
md = md.replace("[UPDATE_BOX]", UBOX).replace("[UPDATE_BYLINE]", UBY)
print(f"update box: to the close of {U['as_of']}, {U['trading_days_since_signature']} trading day(s) after the signature")
XC = json.load(open(os.path.join(RES, "extra_checks.json"))); ST = pd.read_csv(os.path.join(RES, "since_titanic.csv"), index_col=0)
txt = md.replace("−", "-")

pc = lambda v, d=1: f"{v * 100:+.{d}f}%"; need = []
def want(label, s): need.append((label, s))
want("peak close", f"{C['current']['peak_close']:,.2f}"); want("close 20 Nov", f"{C['current']['close_20_nov']:,.2f}"); want("fall from peak", f"{-C['current']['fall_from_peak'] * 100:.1f}%")
want("basket since 6 Oct", f"basket lost {-L1['basket'] * 100:.1f}%"); want("SPY since 6 Oct", f"SPY lost {-L1['spy'] * 100:.1f}%")
for k, v in L1["names"].items(): want(f"name {k}", pc(v))
want("n corrections", f"{C['n_past']} times"); want("bear count", f"{C['became_bear']} of the {C['n_past']} became"); want("bear share", f"That is {C['share_bear'] * 100:.0f}%")
want("further fall", f"{-C['median_further_fall'] * 100:.1f}%"); want("median depth", f"{-C['median_depth'] * 100:.1f}%"); want("days to 10%", f"{C['current']['days_peak_to_10pct']} trading days")
want("median days", f"the median is {C['median_days_peak_to_10pct']}"); want("as fast or faster", f"{C['faster_than_current']} of the"); want("days to new high", f"{C['median_days_to_new_high']} trading days")
CHK = []
for h in ("3 months", "6 months", "12 months"):
    b = C[h]
    for lab, v in (("median", b["median"]), ("p10", b["p10"]), ("p90", b["p90"]), ("no bear", b["median_if_no_bear"]), ("bear", b["median_if_bear"])): want(f"corr {h} {lab}", pc(v))
    want(f"corr {h} share up", f"{b['share_up'] * 100:.0f}%"); CHK.append((h, L2["forecast"][h], L2["baseline"][h]))
g = pd.read_csv(os.path.join(ROOT, "data", "GSPC_daily_eodhd.csv"), parse_dates=["date"]); c = g.close.values; pos = {str(d.date()): i for i, d in enumerate(g.date)}
HH = {"3 months": 63, "6 months": 126, "12 months": 252}; X = {h: [] for h in HH}     # exact values from the index, so that rounding is done once
for a in L2["analogs"]:
    e = pos[a["window_end"]]
    for h, k in HH.items():
        v = c[e + k] / c[e] - 1; assert abs(v - a[h]) < 6e-5, (a, h, v); X[h].append(v); want(f"analog {a['rank']} {h}", pc(v))
    want(f"analog {a['rank']} date", f"{pd.Timestamp(a['window_end']):%-d %b %Y}" if os.name != "nt" else f"{pd.Timestamp(a['window_end']).day} {pd.Timestamp(a['window_end']):%b %Y}")
for h, f, bl in CHK:
    med = float(np.median(X[h])); assert abs(med - f["median"]) < 1.1e-4, (h, med)
    want(f"analog {h} median", pc(med)); want(f"analog {h} low", pc(min(X[h]))); want(f"analog {h} high", pc(max(X[h]))); want(f"baseline {h}", pc(bl["median"])); want(f"midpoint {h}", pc((med + bl["median"]) / 2))
n = F3.group.value_counts(); want("event stocks", f"{n['event']} stocks"); want("control stocks", f"{n['control']:,} had not"); want("left out", f"{n['left out: no price two years back']} had no")
FV = XC["favourites"]
for f in FV:
    b = f["basket_depth"]; d = pd.Timestamp(b["day"]); want(f"fav {f['name']} day", f"| {f['name']} | {d.day} {d:%b %Y} |")
    for k in ("r3", "r6", "r12", "low_3y"): want(f"fav {f['name']} {k}", pc(b[k]))
want("fav depths", "the three were " + ", ".join(f"{-f['basket_depth']['below_peak'] * 100:.1f}%" for f in FV[:2]) + f" and {-FV[2]['basket_depth']['below_peak'] * 100:.1f}% down")
want("fav index depth", "none rallied: " + ", ".join(pc(f["index_depth"]["r3"]) for f in FV[:2]) + " and " + pc(FV[2]["index_depth"]["r3"]) + " after three months")
assert sum(f["basket_depth"]["r3"] > 0.005 for f in FV) == 2 and all(f["basket_depth"]["r12"] < 0 for f in FV); want("fav two of three", "Two of the three rose over the first three months, and all three were lower a year later")
AC, RH = XC["after_corrections"], XC["record_highs"]
want("mean 12m", f"The mean return over the year after these 26 falls was {pc(AC['mean_12m'])}, against {pc(AC['all_days_mean_12m'])}"); want("share up all days", f"69% against {AC['all_days_share_up_12m'] * 100:.0f}%")
want("mean in answers", f"the mean {pc(AC['mean_12m'])}")
want("near bears", f"{AC['near_bears']} more stopped between {AC['near_bear_hi'] * 100:.1f}% and {AC['near_bear_lo'] * 100:.1f}%"); want("not low on first day", f"In {AC['not_low_on_first_day']} of the 26 the first 10% day was not the low"); assert AC["not_low_on_first_day"] + AC["low_on_first_day"] == 26
want("wait from 10% day", f"{AC['median_days_first10_to_new_high']:.0f} trading days from the first 10% day")
want("groundhog now", f"stood {-XC['groundhog']['since_3_nov'] * 100:.1f}% below the 3 November close"); want("index since 30 Oct", "8.7% lower")
SS = XC["line2_sensitivity"]; want("sens range", f"runs from {pc(XC['line2_3m_range'][0])} (five nearest) to {pc(XC['line2_3m_range'][1])} (three nearest)")
assert abs(SS["five nearest"]["3 months"] - XC["line2_3m_range"][0]) < 1e-12 and abs(SS["three nearest"]["3 months"] - XC["line2_3m_range"][1]) < 1e-12
want("sens 40", f"a 40-day pattern gives {pc(SS['40-day pattern']['3 months'])}"); want("sens returns", f"daily returns in place of closes give {pc(SS['daily returns in place of closes']['3 months'])}")
BS = XC["baseline_side_share"]; want("baseline side row", "| " + " | ".join(f"{BS[h] * 100:.0f}%" for h in ("3 months", "6 months", "12 months")) + " |")
want("basket on 5 Nov", f"already {100 - ST.loc['2026-11-05', 'basket']:.1f}% down on 5 November"); want("basket on 14 Oct", f"already {100 - ST.loc['2026-10-14', 'basket']:.1f}% down"); want("basket on 27 Oct", f"by 27 October {100 - ST.loc['2026-10-27', 'basket']:.1f}%")
P = pd.read_csv(os.path.join(ART, "..", "Factsheets", "_data_private", "a68", "a68_start_prices.csv")); sp = P[P.ticker == "SPY"].set_index("date").adjusted_close
assert abs(sp["2026-11-20"] / sp["2026-10-30"] - 1 + 0.087) < 0.0006, "SPY since 30 Oct"
TA = open(os.path.join(ART, "A01_Titanic_AI_Bubble", "article", "earlier_versions", "every_bubble_rhymes_v2.md"), encoding="utf-8").read()
assert "| NVIDIA | +83% |" in TA and "AMD, Alphabet and Broadcom meet the doubling test" in TA and "a flicker, not a pass" in TA
assert "the gap falls from +19 to +4 points (NW t 0.69" in GATE; want("C1-3 volatility check", "the gap fell from 19 points to 4 and was not significant (t 0.69)")
F3r = F3.set_index("ticker").ret_2y; want("NVDA 2y", f"Nvidia was up {F3r['NVDA'] * 100:.0f}%"); want("ORCL 2y", f"Oracle was down {-F3r['ORCL'] * 100:.0f}%")
A58 = open(os.path.join(ART, "A47_Last_Man_Standing_Hedging", "TRIAL_LEDGER.md"), encoding="utf-8").read(); assert "6 of 15 (40%) vs 30% for shifted alarms" in A58 and "signed 22 Oct 2026" in A58
CH = open(os.path.join(ART, "A01_Titanic_AI_Bubble", "article", "CHANGES_v2.md"), encoding="utf-8").read(); assert "there is no evidence of an active one" in CH
ROB = XC["robustness"]; meds = [v["median_12m"] for v in ROB.values()]
for lab, k in (("8% below a high, since 1950", "8% since 1950"), ("10% below a high, since 1950 (as above)", "10% since 1950"), ("12% below a high, since 1950", "12% since 1950"), ("15% below a high, since 1950", "15% since 1950"), ("10% below a record high, since 1928", "10% since 1928")):
    v = ROB[k]; want(f"robustness {k}", f"| {lab} | {v['n']} | {v['bears']} ({v['share_bear'] * 100:.0f}%) | {pc(v['median_12m'])} | {pc(v['mean_12m'])} | {pc(v['median_further_fall'])} |")
want("robustness median range", f"medians between {pc(min(meds))} and {pc(max(meds))}")
want("A62 H1", f"{-TH['H1_hot_24m_excess']['mean'] * 100:.1f}% behind over 24 months, p {TH['H1_hot_24m_excess']['p_one_sided']:.2f}"); want("A62 H2", f"{-TH['H2_rising_12m_excess']['mean'] * 100:.1f}% behind over 12 months"); assert TH["H2_rising_12m_excess"]["n_themes"] == 18
want("A62 AI hot", f"were {TH['by_theme']['ai_robotics']['hot_x24'] * 100:.1f}% ahead of developed markets"); want("A62 AI all", f"{TH['by_theme']['ai_robotics']['all_x24'] * 100:.1f}% ahead after all months"); want("A62 ETFs", f"{TH['ben_david_first60m']['n_etfs']} funds")
assert "out-of-sample R² -0.21" in A52 and "| A52-21 |" in A52 and "| A52-22 |" not in A52; assert "3 passed their family gate: A52-13, A52-19, A52-20" in A52; want("A52 R2", "out-of-sample R² -0.21"); want("A52 trials", "21 trials on analog forecasts, 3 passed their gate")
assert "(305 trials run," in GATE and "counted as 328" in GATE; want("programme count", "stands at 305 trials run, 328 counted")
bad = [(l, s) for l, s in need if s not in txt]
if bad:
    for l, s in bad: print("NUMBER CHECK FAILED:", l, "expected text:", s)
    sys.exit(1)
print(f"number check: {len(need)} of {len(need)} agree with results/")

write_article(ROOT, STEM, md, "A Night to Remember")

post = f"""A NIGHT TO REMEMBER: did my pre-registered tests see the AI sell-off coming?

On 6 October I published Titanic, three pre-registered tests of the AI boom. The S&P 500 closed at its high that same day. That is luck, not a forecast. By Friday 20 November SPY, the S&P 500 fund, was 11.5% lower and eight AI leaders had lost 23.8%.

{UPOST}

So this is not a forecast. It is the record: what I had signed and dated before the fall, why none of it gave a warning, and a new forward record signed on Saturday, with the market closed and before the rebound. Its first number is scored on 19 February 2027.

Three questions:
1. Did my own tests see it coming?
2. What were they built to see, and over what horizon?
3. What usually follows the first 10% fall?

Your answer to question 1 in the comments, then check it here, with tables, code and the pre-registration: {REPO}

#investing #AI #stockmarket #statistics
"""
write_teaser(ROOT, post, "hero_a_night_to_remember_teaser.png", "A Night to Remember", "November 2026")
click_layout(ROOT, "teaser_log.png", alt="Drawing: a ship's log lying open, entries dated before and after the fall, the last one still blank")
write_readme(ROOT, "A68 A Night to Remember: what my pre-registered tests missed",
             ["base_rates.py", "extra_checks.py", "make_figures.py", "make_teaser_drawing.py", "build_article.py"],
             extra="\nNow Showing No. 1½, sequel to No. 1 Titanic, special screening Wed 25 Nov 2026 (number agreed by Henrik 21 Nov 2026). Forward record FR-AI-1, signed 21 Nov 2026 12:11 CET: "
                   "`PREREG_DRAFT_FR_AI_1_2026-11-21.md`, `DATED_NOTES_FR_AI_1.md`, `TRIAL_LEDGER.md`. Line 2 was run once (`code/run_fr_ai_1_line2.py`). "
                   "results/ holds derived statistics and the frozen line 3 groups (tickers and two-year returns, no prices).\n")
make_pdfs(ROOT, STEM)
print(post); print("words", len(post.split()))
