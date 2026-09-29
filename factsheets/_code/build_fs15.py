# -*- coding: utf-8 -*-
"""FS15: the earlier history (1998-2013), as pre-registered in planning/PREREG_FS15.md."""
import json
import os

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF
import perf
from battery import DIRECTION, SIGS

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); FIG = os.path.join(HERE, "..", "figures")
SURF, INK, INK2, GRID, BLUE, ORANGE, GREY, GREEN = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0", "#2a78d6", "#eb6834", "#8a8984", "#2c7a4b"
UA = ["US_A", "EU_A", "UK_A", "DK_A", "WD_A"]; M4 = UA[:4]; AN = {"US_A": "US", "EU_A": "EU", "UK_A": "UK", "DK_A": "DK", "WD_A": "World"}
LAB = {s: DIRECTION[s][2] for s in SIGS}
p = lambda x, d=1: f"{x * 100:+.{d}f}%"


def verdict(t_new, t_old):
    if np.sign(t_new) != np.sign(t_old):
        return "reversed"
    return "confirmed" if abs(t_new) > 2 else "consistent"


def episodes(B):
    eps = {"Dot-com bust (Apr 2000 – Sep 2002)": ("2000-04-30", "2002-09-30"), "Financial crisis (Nov 2007 – Feb 2009)": ("2007-11-30", "2009-02-28"),
           "Momentum crash (Mar – May 2009)": ("2009-03-31", "2009-05-31"), "Euro crisis (May – Sep 2011)": ("2011-05-31", "2011-09-30")}
    books = {"Market (equal weight)": lambda R: B[R]["mom"].ew, "Low beta, beta-neutral": lambda R: B[R]["beta"].bn_net, "12-1 momentum, beta-neutral": lambda R: B[R]["mom"].bn_net,
             "Shortlist (low beta + momentum)": lambda R: (B[R]["beta"].bn_net + B[R]["mom"].bn_net) / 2, "Low skewness, beta-neutral": lambda R: B[R]["skew"].bn_net}
    rows = []
    for name, f in books.items():
        x = pd.DataFrame({R: f(R) for R in M4}).mean(axis=1)
        rows.append([name] + [p(float((1 + x.loc[a:b]).prod() - 1), 0) for a, b in eps.values()])
    return list(eps), rows


def figs(A, CG, MF, ser):
    P = A["pooled"]
    order = sorted(SIGS, key=lambda s: -CG["price"][s]["bn"]["t"])
    fig, ax = plt.subplots(figsize=(10, 7)); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    y = np.arange(len(order))[::-1]
    ax.barh(y + 0.2, [CG["price"][s]["bn"]["t"] for s in order], 0.4, color=BLUE, label="2013–2026 (6 markets)")
    ax.barh(y - 0.2, [P[s]["bn"]["t"] for s in order], 0.4, color=ORANGE, label="1999–2013 (4 markets)")
    ax.set_yticks(y); ax.set_yticklabels([LAB[s] for s in order], fontsize=9); ax.axvline(0, color=INK2, lw=1)
    for g in (-2, 2):
        ax.axvline(g, color=GREY, lw=0.8, ls=":")
    ax.legend(frameon=False, fontsize=9, loc="lower right"); ax.grid(axis="x", color=GRID)
    for sp_ in ax.spines.values(): sp_.set_visible(False)
    ax.set_title("Beta-neutral long/short, t of the cross-market average: two independent periods", loc="left", fontsize=11.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs15_periods.png"), dpi=140, facecolor=SURF); plt.close(fig)
    fig, ax = plt.subplots(figsize=(11, 5)); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    for c, col, lab in (("SHORT", ORANGE, "Fixed shortlist: low beta + 12-1 momentum (chosen on 2013–2026)"), ("RP", BLUE, "FS14 dynamic selection (RP)"), ("ALL-EQ", GREY, "All 19 books, equal"), ("MARKET", INK, "Market, equal weight (long-only)")):
        x = pd.DataFrame({R: ser[R][c] for R in M4}).dropna().mean(axis=1)
        ax.plot((1 + x).cumprod(), color=col, lw=2 if c in ("SHORT", "RP") else 1.4, label=lab)
    ax.set_yscale("log"); ax.axhline(1, color=INK2, lw=0.7); ax.legend(frameon=False, fontsize=8.5); ax.grid(color=GRID)
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
    tk = [0.7, 1, 1.5, 2, 3, 4]; ax.yaxis.set_major_locator(FixedLocator(tk)); ax.yaxis.set_major_formatter(FixedFormatter([str(t) for t in tk])); ax.yaxis.set_minor_locator(NullLocator())
    for sp_ in ax.spines.values(): sp_.set_visible(False)
    ax.set_title("1999–2013 walk-forward (portfolios from Feb 2002), average of US, EU, UK, DK: growth of 1, net", loc="left", fontsize=11.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs15_fs14.png"), dpi=140, facecolor=SURF); plt.close(fig)


def build():
    A = json.load(open(os.path.join(RES, "art_battery.json"))); F = json.load(open(os.path.join(RES, "art_fmb.json"))); MF = json.load(open(os.path.join(RES, "art_fs14.json")))
    CG = json.load(open(os.path.join(RES, "common_ground.json"))); F13 = json.load(open(os.path.join(RES, "fmb.json"))); F14 = json.load(open(os.path.join(RES, "fs14.json")))
    ser = pd.read_pickle(os.path.join(RES, "art_fs14.pkl")); B = pd.read_pickle(os.path.join(RES, "battery_art.pkl"))
    LG = json.load(open(os.path.join(RES, "trial_ledger.json")))
    figs(A, CG, MF, ser); P = A["pooled"]
    import data
    nmed = {R: int(data.load(R)["elig"].resample("ME").last().sum(axis=1).loc["1999":].median()) for R in UA}
    rows, V = [], {}
    for s in sorted(SIGS, key=lambda s: -P[s]["bn"]["t"]):
        t_old, t_new = CG["price"][s]["bn"]["t"], P[s]["bn"]["t"]; v = verdict(t_new, t_old); V[s] = v
        rows.append([LAB[s], f"{t_old:+.1f}" + (" (weak)" if abs(t_old) < 1 else ""), f"{p(P[s]['bn']['ann'])} (t {t_new:+.1f})", f"{P[s]['bn']['pos']} / 4", f"{P[s]['bn']['s1']:+.2f} / {P[s]['bn']['s2']:+.2f}", f"{P[s]['raw']['t']:+.1f}", v])
    fm_rows = [[LAB[s], f"{F13['pooled'][s]['t']:+.1f}", f"{F['pooled'][s]['t']:+.1f}", f"{F['pooled'][s]['pos']} / {F['pooled'][s]['n']}", verdict(F["pooled"][s]["t"], F13["pooled"][s]["t"])] for s in F["pooled"]]
    pr, po = MF["primary"], MF["pooled"]; sh = MF["short_vs_alleq"]; best = max(MF["variants"], key=lambda v: po[v]["sharpe"])
    mf_rows = [[AN[R], f"{MF[R]['RP']['sharpe']:+.2f}", f"{MF[R][best]['sharpe']:+.2f}", f"{MF[R]['ALL-EQ']['sharpe']:+.2f}", f"{MF[R]['SHORT']['sharpe']:+.2f}", f"{MF[R]['MARKET']['sharpe']:+.2f}", f"{MF[R]['_sel']['kept_med']:.0f}", MF[R]["_sel"]["cash_months"]] for R in UA]
    mf_rows.append(["**4-market average**", f"{po['RP']['sharpe']:+.2f}", f"{po[best]['sharpe']:+.2f}", f"{po['ALL-EQ']['sharpe']:+.2f}", f"{po['SHORT']['sharpe']:+.2f}", f"{po['MARKET']['sharpe']:+.2f}", "—", "—"])
    cmp_rows = [["Primary: RP minus ALL-EQ", f"{p(F14['primary']['ann'])} (t {F14['primary']['t']:+.1f})", f"{p(pr['ann'])} (t {pr['t']:+.1f})"],
                ["Best weighting rule, Sharpe", f"{max(F14['pooled'][v]['sharpe'] for v in F14['variants']):.2f}", f"{po[best]['sharpe']:.2f} ({best})"],
                ["RP, Sharpe", f"{F14['pooled']['RP']['sharpe']:.2f}", f"{po['RP']['sharpe']:.2f}"],
                ["All books equal, Sharpe", f"{F14['pooled']['ALL-EQ']['sharpe']:.2f}", f"{po['ALL-EQ']['sharpe']:.2f}"],
                ["Fixed shortlist, Sharpe", f"{F14['pooled']['SHORT']['sharpe']:.2f} (hindsight)", f"{po['SHORT']['sharpe']:.2f} (out of sample)"]]
    ep_cols, ep_rows = episodes(B)
    conf = [LAB[s] for s in SIGS if V[s] == "confirmed"]; rev = [LAB[s] for s in SIGS if V[s] == "reversed"]
    sh_led = [x for x in LG["passes"] if "shortlist" in x["strategy"]]
    md = f"""# FACTSHEET FS15 · The earlier history

### Do the conclusions hold in 1998–2013, with two bear markets they never saw?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · ART data January 1998 – March 2013*

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS15.md`, written and saved before any 1998–2013 return was computed; no deviations |
| Data | ART research database extract (Project2): daily total-return indices and traded value, as reported, including stocks that later delisted |
| Markets | US, EU (EU member states excl. UK, Poland, Greece), UK, Denmark; World = US + UK + EU in USD; no Scandinavia (Finland not identifiable in the extract) |
| Universes | top {nmed['US_A']} US, {nmed['UK_A']} UK, {nmed['EU_A']} EU, {nmed['DK_A']} DK stocks by 63-day traded value each month (median eligible names); a liquidity universe, not an index |
| Engine | identical to FS13/FS13c/FS14: same 19 signals and directions, costs, borrow fees, financing, filter, pruning and weighting rules |
| Periods | signals Jan 1999 – Feb 2013; the FS14 walk-forward holds portfolios from Feb 2002 (36 months of history needed) |

> **In one paragraph.** The earlier period mostly agrees with the later one, and where it disagrees it is informative. **Low risk is confirmed**: beta-neutral low beta and low volatility earn t {P['beta']['bn']['t']:.1f} and {P['vol252']['bn']['t']:.1f} across the four markets, positive in all four and in both halves. **Momentum is consistent but weaker** (12-1: t {P['mom']['bn']['t']:.1f}; flat through the 2008 crash, then hit hard in the spring 2009 rebound), and in the joint regression it again adds return (t {F['pooled']['mom']['t']:.1f}, confirming FS13c). **Tail direction is confirmed as a loser** (low skewness t {P['skew']['bn']['t']:.1f}). **Seasonality reverses**: it paid before 2013 (joint slope t {F['pooled']['seas']['t']:.1f}) and failed after, the pattern of a published anomaly that faded. The **FS14 dynamic selection fails again**: {p(pr['ann'])} a year over owning every book (t {pr['t']:.1f}), positive before 2007 and negative after. The strongest result is the **fixed shortlist of low beta and 12-1 momentum**, chosen from 2013–2026 results and therefore genuinely out of sample here: Sharpe {po['SHORT']['sharpe']:.2f}, {p(sh['ann'])} a year over owning every book (t {sh['t']:.1f}), positive in all four markets, with a correlation of {MF['short_corr_market']:+.2f} to the market. {'It does not survive the programme-wide correction over ' + str(LG['n']) + ' trials.' if not sh_led else 'It survives the programme-wide correction.'}

![Periods](../figures/fs15_periods.png)

## 1. The price battery, 1999–2013

{BF.table(["Signal", "2013–26 beta-neutral t", "1999–2013 beta-neutral, net / yr (t)", "Markets positive", "Sharpe 1999–2005 / 2006–13", "1999–2013 raw L/S t", "Verdict"], rows)}

*Verdict as pre-registered: confirmed = same sign as 2013–26 and |t| > 2 in 1999–2013; consistent = same sign, |t| ≤ 2; reversed = opposite sign. "(weak)" marks a 2013–26 result with |t| < 1, which barely had a sign to confirm. Averages over US, EU, UK and DK; World is left out because it overlaps.*

**Confirmed:** {', '.join(conf) or 'none'}. **Reversed:** {', '.join(rev) or 'none'}. Everything else keeps its sign with a t below 2.

## 2. All signals together (Fama-MacBeth), 1999–2013

{BF.table(["Signal", "2013–26 joint slope t", "1999–2013 joint slope t", "Markets positive", "Verdict"], fm_rows)}

12-1 momentum keeps a positive joint slope in both periods, the one price signal that does. The earlier period also rewards signals that are weak or negative after 2013: seasonality, low MAX and small size.

## 3. The FS14 procedure, 1999–2013

{BF.table(["Market", "RP (primary)", f"{best}", "All books equal", "Fixed shortlist", "Market", "Books held (median)", "Months in cash"], mf_rows)}

*Sharpe ratios, net, Feb 2002 – Mar 2013. Fixed shortlist = low beta and 12-1 momentum, beta-neutral, equal weights.*

![FS14 on 1999–2013](../figures/fs15_fs14.png)

{BF.table(["", "2016–2026 (FS14)", "2002–2013 (FS15)"], cmp_rows)}

**Primary test:** RP − ALL-EQ = {p(pr['ann'])} a year, t {pr['t']:.2f} ({pr['s1'] * 100:+.1f}% up to {pr['split'][:7]}, {pr['s2'] * 100:+.1f}% after): **not passed**, for the second time.

**The shortlist:** {p(sh['ann'])} a year over owning every book (t {sh['t']:.2f}), positive in {sh['pos']} of 4 markets and in both halves ({sh['s1'] * 100:+.1f}% / {sh['s2'] * 100:+.1f}%). Because the shortlist was chosen from 2013–2026 results, this is a clean out-of-sample test of that choice.

## 4. Bear markets

{BF.table(["Book (4-market average)", *ep_cols], ep_rows)}

*Cumulative return over each episode. The beta-neutral books are long/short and market-neutral by construction.*

Low beta was the great protector in the dot-com bust and paid in the euro crisis, but lost in the financial crisis, when its leveraged low-beta leg fell with everything else. Momentum held flat through 2008 and then lost heavily in the spring 2009 rebound, when its short leg of beaten-down stocks rallied hardest (Daniel & Moskowitz 2016). The two legs fail at different times, which is why the pair beats either alone.

## 5. What this adds to the series

1. **Low beta and momentum keep their sign across 27 years and two independent samples** (low beta significant in both, momentum only in the joint regression before 2013), and together they beat both the dynamic selection and owning everything.
2. **The dynamic selection process (FS14) failed its pre-registered test twice.** A rules-based filter on trailing Sharpe ratios chases what just worked and lags turning points.
3. **Seasonality and low MAX worked before 2013 and not after** (small size weakened), the decay McLean & Pontiff (2016) and JKP describe after publication and wider use.
4. **Tail direction (low skewness) loses in both periods**: in large caps the stocks with the most positive skew kept earning more, not less.

## 6. Caveats

- **Liquidity universe.** Without membership dates, the universe is the most traded stocks each month, larger than the 2013–26 index universes in the UK and US and not identical to them.
- **As-reported prices** from one research database; bad ticks are filtered (daily moves above 100%, and +50%/−33% one-day reversals), but data quality is below today's vendors.
- **Currency.** Traded value is converted to USD with Fed H.10 rates for ranking; pre-1999 euro-area values use the first euro rate.
- **Overlap.** The ART extract ends in March 2013 and the 2013–26 sample starts in February 2013: two months overlap.
- **Multiple testing.** FS15 adds {sum(1 for x in LG['by'] if x['fs'] == 'FS15') and next(x['trials'] for x in LG['by'] if x['fs'] == 'FS15')} trials to the ledger (now {LG['n']}).

## 7. References

- Daniel, K. & Moskowitz, T. J. (2016). Momentum crashes. *Journal of Financial Economics* 122(2), 221–247.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance* 71(1), 5–32.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics* 111(1), 1–25.
- Heston, S. L. & Sadka, R. (2008). Seasonality in the cross-section of stock returns. *Journal of Financial Economics* 87(2), 418–445.
- Asness, C. S., Moskowitz, T. J. & Pedersen, L. H. (2013). Value and momentum everywhere. *Journal of Finance* 68(3), 929–985.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.

## 8. Reproduce

`planning/PREREG_FS15.md` → `code/data.py` (`load_art`, universes) → `code/signals.py`, `signals2.py` (regions `US_A`, `EU_A`, `UK_A`, `DK_A`, `WD_A`) → `code/art_run.py` (battery, Fama-MacBeth, FS14 procedure → `results/art_*.json`) → `code/build_fs15.py`. The ART extract is private and not published.
"""
    BF.write("FS15_Earlier_History", md, "FS15 The earlier history")
    BF.pdf("FS15_Earlier_History")


if __name__ == "__main__":
    build(); print("built FS15")
