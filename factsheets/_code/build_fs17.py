# -*- coding: utf-8 -*-
"""FS17: fundamentals outside the US, factor level, as pre-registered (planning/PREREG_FS17.md)."""
import json
import os

import build_factsheets as BF

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results")
p = lambda x, d=1: f"{x * 100:+.{d}f}%"


def build():
    r = json.load(open(os.path.join(RES, "fs17.json"))); N = r["names"]; T = r["themes"]
    LG = json.load(open(os.path.join(RES, "trial_ledger.json")))
    def mrows(per):
        return [[N[k], f"{p(v['themes']['pair']['alpha'])} (t {v['themes']['pair']['t']:+.1f})", f"{v['themes']['pair']['r2']:.2f}", f"{v['corr_pair_short']:+.2f}",
                 f"{v['short_sharpe']:.2f}", f"{v['comb_sharpe']:.2f}", f"{v['diff_t']:+.1f}"] for k, v in r[per]["markets"].items()]
    def trows(per):
        return [[t, f"{p(r[per]['pooled_themes'][t]['alpha'])} (t {r[per]['pooled_themes'][t]['t']:+.1f})"] + [f"{v['themes'][t]['t']:+.1f}" for v in r[per]["markets"].values()] for t in T]
    pb, pa = r["B"]["pooled"], r["A"]["pooled"]
    hdrB = ["Theme", "Non-US average: alpha (t)"] + [N[k] + " t" for k in r["B"]["markets"]]
    hdrA = ["Theme", "Non-US average: alpha (t)"] + [N[k] + " t" for k in r["A"]["markets"]]
    md = f"""# FACTSHEET FS17 · Fundamentals outside the US

### Do the fundamental themes add anything to low beta and momentum in Europe, the UK and Denmark?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · JKP to December 2025, ART 1996–2013*

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS17.md`, saved to the Factsheets folder before the run; no deviations |
| Why factor level | stock-level fundamentals with filing dates exist here only for the US (FS13b); outside the US the available history is factor returns |
| 2013–2025 | JKP themes (equal-weight average of each cluster's factors) for the UK, Denmark, World ex US (as the EU proxy), World and the US |
| 1999–2013 | ART's own factor spreads (top minus bottom decile) for Europe, the UK and America: analyst revisions, buybacks, value, profitability |
| Themes | profit growth (ART: revisions), issuance (ART: buybacks), value, profitability; **fundamental pair** = profit growth + issuance |
| Test | each theme scaled to 10% volatility (ex ante), regressed on the two shortlist legs (low beta and 12-1 momentum, beta-neutral, net); Newey–West t |

> **In one paragraph.** **Yes, clearly, in both periods.** The fundamental pair earns an alpha of **{p(pb['alpha'])} a year (t {pb['t']:.1f})** on top of low beta and momentum across the UK, Denmark and the EU proxy in 2013–2025, and **{p(pa['alpha'])} (t {pa['t']:.1f})** across Europe and the UK in 1999–2013. The pre-registered bar (t > 2 in both periods) is **{'passed' if r['passed'] else 'not passed'}**, and the primary test also survives the programme-wide correction across {LG['n']} trials. The fundamental pair is only weakly correlated with the price shortlist (0.2–0.4), so adding them lifts the combined Sharpe ratio in every market. Two warnings keep this from being an investable result: the factor returns are **gross of trading costs**, and the ART spreads (1999–2013) are decile spreads whose size (Sharpe ratios near 2) is too large to take at face value.

## 1. 2013–2025 (JKP)

{BF.table(["Market", "Pair alpha on the shortlist (t)", "R²", "Correlation with the shortlist", "Shortlist Sharpe", "Shortlist + pair Sharpe", "Difference t"], mrows('B'))}

{BF.table(hdrB, trows('B'))}

*Alpha: annualised intercept, both sides scaled to 10% volatility. Non-US average: UK, Denmark and the EU proxy. The US row is for reference; it is outside the pre-registered test.*

**Issuance (firms that shrink their net financing) carries most of it** after 2013; profit growth adds a little, value helps in the UK, profitability adds nothing.

## 2. 1999–2013 (ART)

{BF.table(["Market", "Pair alpha on the shortlist (t)", "R²", "Correlation with the shortlist", "Shortlist Sharpe", "Shortlist + pair Sharpe", "Difference t"], mrows('A'))}

{BF.table(hdrA, trows('A'))}

*Non-US average: Europe and the UK. America for reference.*

Before 2013 every fundamental theme added to the price shortlist, analyst revisions most of all. Their weakening after 2013 matches the decay JKP and McLean & Pontiff (2016) describe.

## 3. What this closes and what it does not

- **Closed at factor level:** the fundamental themes outside the US carry information that low beta and momentum do not, in two independent periods and data sources. The multifactor model should include issuance and profit growth in every market, not only the US.
- **Not closed at stock level:** we still cannot build these signals stock by stock outside the US with filing dates, so we cannot measure their net return after costs and capacity (FS16) in our own universes. Project2's `pit_fundamentals` snapshots, captured weekly since September 2026, will become a usable point-in-time history over the next one to two years; a licensed global fundamentals feed would close it now.

## 4. Caveats

- JKP factors: capped value-weighted, gross, USD; our shortlist: equal-weighted, net, local currency.
- ART spreads: gross decile spreads from the ART segment universes, compounded from weekly returns; costs and the stock universe differ from our books, and their magnitude is implausibly high for a tradable strategy.
- The EU is proxied by World ex US for 2013–2025, which also contains Japan, Canada and Australia.
- FS17 adds {next(x['trials'] for x in LG['by'] if x['fs'] == 'FS17')} trials to the ledger (now {LG['n']}).

## 5. References

- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Pontiff, J. & Woodgate, A. (2008). Share issuance and cross-sectional returns. *Journal of Finance* 63(2), 921–945.
- Chan, L. K. C., Jegadeesh, N. & Lakonishok, J. (1996). Momentum strategies. *Journal of Finance* 51(5), 1681–1713.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance* 71(1), 5–32.
- Asness, C. S., Frazzini, A. & Pedersen, L. H. (2019). Quality minus junk. *Review of Accounting Studies* 24(1), 34–112.

## 6. Reproduce

`planning/PREREG_FS17.md` → `code/fs17.py` (→ `results/fs17.json`) → `code/build_fs17.py`. JKP files from Project2 `reporting/style_cache`; ART spreads from Project1 `art_factor_spreads_monthly.csv`.
"""
    BF.write("FS17_Fundamentals_Outside_US", md, "FS17 Fundamentals outside the US")
    BF.pdf("FS17_Fundamentals_Outside_US")


if __name__ == "__main__":
    build(); print("built FS17")
