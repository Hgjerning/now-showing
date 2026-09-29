# -*- coding: utf-8 -*-
"""FS19: robustness — engine tests, stress episodes, sector neutrality (planning/PREREG_FS19.md)."""
import json
import os

import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

import build_factsheets as BF
import fs19

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); FIG = os.path.join(HERE, "..", "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "Denmark", "SC": "SCANDI", "WD": "World"}
ART = {"US_A": "America 1999–2013", "EU_A": "Europe 1999–2013", "UK_A": "UK 1999–2013", "DK_A": "Denmark 1999–2013", "ART pooled": "ART pooled"}
SURF = "#fcfcfb"
p = lambda x, d=1: "—" if x is None else f"{x * 100:+.{d}f}%"
BOOKS = ["low beta", "12-1 momentum", "overlay"]


def fig(B):
    E = list(fs19.EPIS); rows, lab = [], []
    for R in U:
        for b in BOOKS:
            rows.append([B["episodes"][R][e][b] if B["episodes"][R][e][b] is not None else np.nan for e in E]); lab.append(f"{UN[R]} · {b}")
    M = np.array(rows) * 100
    f, ax = plt.subplots(figsize=(9.5, 8.6)); f.patch.set_facecolor(SURF)
    im = ax.imshow(M, cmap="RdBu", norm=TwoSlopeNorm(0, -30, 30), aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{M[i, j]:+.0f}", ha="center", va="center", fontsize=8.5, color="black" if abs(M[i, j]) < 20 else "white")
    ax.set_xticks(range(len(E))); ax.set_xticklabels(E, fontsize=9); ax.set_yticks(range(len(lab))); ax.set_yticklabels(lab, fontsize=8.5)
    for k in range(1, len(U)):
        ax.axhline(k * 3 - 0.5, color=SURF, lw=3)
    ax.set_title("Cumulative return in each episode, % (net of costs at $50m per book)", loc="left", fontsize=11)
    for s in ax.spines.values(): s.set_visible(False)
    f.tight_layout(); f.savefig(os.path.join(FIG, "fs19_episodes.png"), dpi=140, facecolor=SURF); plt.close(f)


def build():
    e = json.load(open(os.path.join(RES, "fs19_engine.json"))); r = json.load(open(os.path.join(RES, "fs19.json"))); B, C = r["B"], r["C"]
    LG = json.load(open(os.path.join(RES, "trial_ledger.json"))); fig(B)
    # A. engine
    tr_ok = all(v["max_abs_diff"] is not None and v["max_abs_diff"] <= 1e-9 and v["n_full"] == v["n_trunc"] for R in e["truncation"].values() for T in R.values() for v in T.values())
    ntr = sum(len(T) for R in e["truncation"].values() for T in R.values())
    n = e["noise"]; noise_ok = 0.01 <= n["share_abs_t_gt_1_96"] <= 0.10 and n["max_abs_t"] < 4
    ch = n["cheat"]; nxt = min(v for k, v in ch.items() if "next" in k); now = max(abs(v) for k, v in ch.items() if "now" in k)
    cheat_ok = nxt > 20 and now < 4
    co = e["costs"]; cost_ok = all(max(v.values()) < 1e-12 for v in co.values())
    bt = e["betas"]; flag = [f"{UN[R]} {k.split(' (')[0]} ({v['beta']:+.2f})" for R in U for k, v in bt[R].items() if abs(v["beta"]) > 0.3]
    ok = lambda b: "**pass**" if b else "**fail**"
    A = [["1. Truncation (look-ahead)", f"19 signals rebuilt from data cut at Dec 2015, 2019, 2023 (US, EU, UK): {ntr} comparisons", "identical signal values and name counts", ok(tr_ok)],
         ["2. Noise", f"19 signals on iid noise, 5 seeds × US, EU: {n['n']} gross L/S t-statistics", f"{n['share_abs_t_gt_1_96'] * 100:.1f}% have |t| > 1.96 (expected 5%); max |t| {n['max_abs_t']:.2f}", ok(noise_ok)],
         ["3. Cheat (timing)", "next month's return as the signal vs this month's return", f"next month: t ≥ {nxt:.0f}; this month: |t| ≤ {now:.1f}", ok(cheat_ok)],
         ["4. Cost accounting", "gross − net = cost + borrow + financing; cost = 10 bp × 2 × turnover", f"largest error {max(max(v.values()) for v in co.values()):.0e}", ok(cost_ok)],
         ["5. Beta neutrality", "realised beta of the 'beta-neutral' books on the equal-weight universe", "flagged if |beta| > 0.3: " + (", ".join(flag) or "none"), "**flag**" if flag else "**pass**"]]
    btab = [[UN[R], f"{bt[R]['low beta (bn)']['beta']:+.2f}", f"{bt[R]['12-1 momentum (bn)']['beta']:+.2f}"] for R in U]
    # B. episodes
    E = list(fs19.EPIS)
    ep = []
    for R in U:
        for b in ["market", "low beta", "12-1 momentum", "overlay", "market + overlay"]:
            ep.append([UN[R] if b == "market" else "", b] + [p(B["episodes"][R][x][b], 0) for x in E])
    dmrows = [[UN.get(k, ART.get(k, k)), str(v["bear_months"]), f"{v['b_bear_mkt']:+.2f} (t {v['t_bear_mkt']:+.1f})" + (" *" if v["bear_months"] < 12 else ""), f"{v['b_mkt']:+.2f}"] for k, v in B["dm"].items()]
    # C. sector
    M = C["markets"]; ps, pr = C["pooled | sector-neutral"], C["pooled | raw"]
    crow = []
    for R in U:
        m = M[R]
        crow.append([UN[R], f"{m['coverage'] * 100:.0f}%", p(m["shortlist | raw"]["ann"]), f"{p(m['shortlist | sector-neutral']['ann'])} (t {m['shortlist | sector-neutral']['t']:+.1f})",
                     p(m["shortlist | sector component"]["ann"]), f"{m['shortlist | difference']['corr']:.2f}",
                     p(m["low beta | sector-neutral"]["ann"]), p(m["12-1 momentum | sector-neutral"]["ann"])])
    nfs = next(x['trials'] for x in LG['by'] if x['fs'] == 'FS19')
    md = f"""# FACTSHEET FS19 · Robustness

### Is it a bug, a few lucky episodes, or a sector bet?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · 2013–2026, momentum crashes also 1999–2013*

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS19.md`, saved to the Factsheets folder before any FS19 number was computed; no deviations |
| A. Engine tests | truncation (look-ahead), iid-noise, cheat-timing, cost accounting, beta neutrality |
| B. Stress episodes | 2015–16 sell-off, Q4 2018, COVID crash, COVID rebound, 2022 rate shock; momentum-crash regression (Daniel & Moskowitz 2016) |
| C. Sector neutrality | low beta and 12-1 momentum ranked within 11 sectors (static Morningstar/Yahoo map); **primary test** of FS19 |
| Primary test | pooled sector-neutral shortlist (US, EU, UK, Denmark, SCANDI): NW t > 2 and at least half the unrestricted return |

> **In one paragraph.** **The engine is clean and the result is not a sector bet, but "beta-neutral" low beta is not market-neutral.** The signals are identical when rebuilt from truncated data, they earn nothing on random noise, and the cost arithmetic adds up to the last decimal. Ranked within sectors, the shortlist keeps **{p(ps['ann'])} a year (t {ps['t']:.2f})** of its unrestricted {p(pr['ann'])}, so the primary test is **{'passed' if C['passed'] else 'not passed'}**. The warning is in the crash tests. The low-beta book, scaled to beta-neutral with estimated betas, still carries a realised market beta of about +0.3 to +0.6 in the US, UK, EU and World, because low betas drift up and high betas drift down. It lost 29% in the US in the COVID crash and 24% in 2022. Momentum did the hedging. The FS18 overlay as a whole stayed within a few per cent in every episode.

## A. Engine tests

{BF.table(["Test", "What", "Result", "Verdict"], A)}

{BF.table(["Market", "Low beta (beta-neutral): realised beta", "12-1 momentum (beta-neutral): realised beta"], btab)}

*Realised beta: full-sample regression of the gross book return on the equal-weight universe, 2013–2026. The legs are scaled with 12-month ex-ante betas, clipped to 0.2–3. Frazzini & Pedersen (2014) shrink betas towards 1 for exactly this reason; our books do not, so "beta-neutral" means ex ante, not realised.*

## B. Stress episodes

![Episodes](../figures/fs19_episodes.png)

{BF.table(["Market", "Book"] + E, ep)}

*Books as in FS18: beta-neutral with the turnover buffer, FS16 costs at $50m per book, borrow and financing; overlay at 5% volatility; market = size-weighted universe (World in USD).*

- **Low beta** protects in slow sell-offs (2015–16) but not in fast crashes or rate shocks: it fell with the market in the COVID crash and in 2022 in the US, EU and World.
- **Momentum** was positive in the COVID crash in all six markets and mostly lost only a few per cent in the rebound.
- **The overlay** kept every episode within ±8%. It adds little protection to a market portfolio; its job is return per unit of risk (FS18).

### Momentum crashes (Daniel & Moskowitz 2016)

{BF.table(["Sample", "Bear months", "Bear × market coefficient (t)", "Market coefficient"], dmrows)}

*Momentum (beta-neutral, net) regressed on the equal-weight market, a bear dummy (market down over the previous 24 months) and their product; Newey–West t (ART pooled: White). A negative bear × market coefficient means momentum loses when markets rebound after a bear market. \\* fewer than 12 bear months: not interpretable (the US t of −12 rests on 3 months).*

2013–2026 has almost no bear-market states, so the crash risk cannot be tested there. In 1999–2013 the sign is the one Daniel & Moskowitz report (pooled coefficient {B['dm']['ART pooled']['b_bear_mkt']:+.2f}, t {B['dm']['ART pooled']['t_bear_mkt']:.1f}), and FS15 showed the spring-2009 momentum loss of −42%. The risk is real, it just did not show up in our main sample.

## C. Sector neutrality

{BF.table(["Market", "Sector coverage", "Shortlist, unrestricted", "Shortlist, within sectors (t)", "Sector component", "Correlation within vs unrestricted", "Low beta, within sectors", "Momentum, within sectors"], crow)}

*Net of 10 bp per side, borrow and financing; beta-neutral legs, no buffer. Coverage: share of stocks with a sector label; the rest form one "unclassified" group. UK coverage is low because many FTSE 250 members are investment trusts missing from the sector caches. Sector component: book sorted on the sector-average signal.*

Across the five markets, about two thirds of the shortlist's return comes from picking stocks within sectors, and the sector bets add the rest. The within-sector book is highly correlated with the unrestricted one. The exception is Denmark, where 19 stocks spread over 11 sectors leave nothing to rank within a sector.

## Caveats

- Sector labels are today's, applied to all years.
- The truncation test covers the price library, not the US fundamental composites (their point-in-time logic is the filing-date lag in FS13b).
- The noise test checks the engine's timing and statistics, not the economic content of any signal.
- FS19 adds {nfs} trials to the ledger (now {LG['n']}).

## References

- Daniel, K. & Moskowitz, T. J. (2016). Momentum crashes. *Journal of Financial Economics* 122(2), 221–247.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics* 111(1), 1–25.
- Moskowitz, T. J. & Grinblatt, M. (1999). Do industries explain momentum? *Journal of Finance* 54(4), 1249–1290.
- Asness, C. S., Frazzini, A. & Pedersen, L. H. (2014). Low-risk investing without industry bets. *Financial Analysts Journal* 70(4), 24–41.
- Bailey, D. H., Borwein, J., López de Prado, M. & Zhu, Q. J. (2014). Pseudo-mathematics and financial charlatanism. *Notices of the AMS* 61(5), 458–471.

## Reproduce

`planning/PREREG_FS19.md` → `code/fs19_engine.py` (→ `results/fs19_engine.json`), `code/fs19.py` (→ `results/fs19.json`; uses `sectors.py`, `fs18.py`) → `code/build_fs19.py`. Sector source files are private.
"""
    BF.write("FS19_Robustness", md, "FS19 Robustness")
    BF.pdf("FS19_Robustness")


if __name__ == "__main__":
    build(); print("built FS19")
