# -*- coding: utf-8 -*-
"""FS05 Monkey (dartboard) portfolios: factsheet from results/monkey_summary.json and monkey_series.pkl."""
import json
import os

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF
import library
import perf

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); FIG = os.path.join(HERE, "..", "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = BF.UN; UNL = BF.UNL; table = BF.table
SURF, INK, INK2, BLUE, ORANGE, GREY = "#fcfcfb", "#0b0b0b", "#52514e", "#2a78d6", "#eb6834", "#8a8984"
p = lambda x, d=1: f"{x * 100:+.{d}f}%"; pu = lambda x, d=0: f"{x * 100:.{d}f}%"


def build():
    M = json.load(open(os.path.join(RES, "monkey_summary.json"))); S = pd.read_pickle(os.path.join(RES, "monkey_series.pkl"))
    # figure 1: CAGR distributions
    fig, axs = plt.subplots(2, 3, figsize=(12, 6.4))
    for ax, R in zip(axs.flat, U):
        c = S[R]["cagr"] * 100; ax.hist(c, bins=60, color="#b9b8b2", edgecolor=SURF, linewidth=0.5)
        for v, col, lab in ((M[R]["sw_cagr"] * 100, BLUE, "index (size-weighted)"), (M[R]["ew_cagr"] * 100, ORANGE, "equal-weight universe")):
            ax.axvline(v, color=col, lw=2, label=lab)
        ax.set_title(f"{UN[R]}: {pu(M[R]['share_beat_cagr'])} of monkeys beat the index", loc="left", fontsize=10.5, color=INK)
        ax.xaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda v, q: f"{v:.0f}%")); ax.set_yticks([])
    axs.flat[0].legend(frameon=False, fontsize=8)
    fig.suptitle("10,000 dartboard portfolios per market: annual return 2013–2026", x=0.01, ha="left", fontsize=13, fontweight="bold", color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(os.path.join(FIG, "fs05_dist.png"), dpi=150); plt.close(fig)
    # figure 2: yearly share beating vs EW-minus-index spread
    fig, ax = plt.subplots(figsize=(8, 5))
    cols = dict(zip(U, [BLUE, ORANGE, "#1baf7a", "#4a3aa7", "#eda100", GREY]))
    for R in U:
        y = M[R]["yearly"]; ax.scatter([v["ew_minus_sw"] * 100 for v in y], [v["share_beat"] * 100 for v in y], color=cols[R], s=36, label=UN[R], edgecolor=SURF)
    ax.axhline(50, color=INK2, lw=0.8, ls="--"); ax.axvline(0, color=INK2, lw=0.8)
    ax.set_xlabel("equal-weight universe minus index that year (percentage points)"); ax.set_ylabel("share of monkeys beating the index that year (%)")
    ax.legend(frameon=False, fontsize=8, ncol=3); ax.set_title("Monkeys win in the years small beats big: one dot per market-year", loc="left", fontsize=10.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs05_years.png"), dpi=150); plt.close(fig)
    # attribution: median monkey minus index on (EW - index) and the library size L/S
    att = {}
    for R in U:
        med, sw, ew = S[R]["median"], S[R]["sw"], S[R]["ew"]
        y = (med - sw).values; x = (ew - sw).values
        reg = perf.nw_ols(y, x, 6)
        size_ls = library.build(R)["L"]["size"].reindex(med.index)
        att[R] = dict(alpha=reg["alpha"] * 12, t=reg["t_alpha"], slope=reg["beta"], corr_size=float(np.corrcoef((ew - sw).values[~size_ls.isna().values], -size_ls.dropna().values)[0, 1]))
    beat = [M[R]["share_beat_cagr"] for R in U]
    head = [[UN[R], M[R]["k"], p(M[R]["monkey_cagr_pct"]['50']), f"{p(M[R]['monkey_cagr_pct']['5'])} to {p(M[R]['monkey_cagr_pct']['95'])}", p(M[R]["mean_monkey_cagr"]), p(M[R]["sw_cagr"]), p(M[R]["ew_cagr"]),
             pu(M[R]["share_beat_cagr"]), pu(M[R]["share_beat_sharpe"]), f"{M[R]['monkey_sharpe_pct']['50']:.2f} / {M[R]['sw_sharpe']:.2f}", f"{pu(M[R]['maxdd_median'])} / {pu(M[R]['sw_maxdd'])}"] for R in U]
    yearly = table(["Year"] + [UN[R] for R in U], [[str(y["year"])] + [f"{pu(M[R]['yearly'][i]['share_beat'])} ({p(M[R]['yearly'][i]['ew_minus_sw'], 0)})" for R in U] for i, y in enumerate(M["US"]["yearly"])])
    md = f"""# FACTSHEET FS05 · Monkey portfolios

### Can a blindfolded monkey beat the index?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Random stock picks, equal weight, rebalanced yearly</div>
<div><b>Origin</b>Malkiel (1973), <i>A Random Walk Down Wall Street</i></div>
<div><b>Family</b>Portfolio folklore</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World (point-in-time)</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, 10,000 monkeys per market</div>
<div><b>Benchmark</b>Size-weighted universe ("the index") and equal-weight universe</div>
<div><b>Rebalance</b>Every January</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **The claim.** Burton Malkiel (1973): a blindfolded monkey throwing darts at the stock pages could pick a portfolio that does as well as the experts. Arnott, Hsu, Kalesnik & Tindall (2013) found that random, and even 'upside-down', portfolios beat the cap-weighted US index over 1964–2012. **What we find:** the share of 10,000 monkeys that beat the index ranged from {pu(min(beat))} to {pu(max(beat))} across the six markets: {', '.join(f"{UN[R]} {pu(M[R]['share_beat_cagr'])}" for R in U)}. Measured by Sharpe ratio, the same or fewer monkeys win ({', '.join(f"{UN[R]} {pu(M[R]['share_beat_sharpe'])}" for R in U)} beat the index's Sharpe). **What decides it (§10):** whether small beats big that year. The yearly share of winning monkeys moves with the gap between the equal-weight universe and the index (correlation {min(M[R]['corr_share_spread'] for R in U):.2f} to {max(M[R]['corr_share_spread'] for R in U):.2f}). The average monkey *is* the equal-weight universe; the typical (median) monkey lags it by the cost of holding only {M['US']['k']} names. **Classification (§11):** a benchmark lesson, not a strategy: a random portfolio is an equal-weight portfolio, and equal weight is a size tilt.

## 1. Headline performance

{table(["Universe", "Stocks per monkey", "Median monkey CAGR", "5th–95th percentile", "Average monkey CAGR", "Index CAGR", "EW universe CAGR", "Monkeys beating the index (return)", "Beating on Sharpe", "Median Sharpe monkey / index", "Max DD median monkey / index"], head)}
*Index = size-weighted universe: market-cap weights in the US (Sharadar), traded-value weights elsewhere (a proxy; no shares outstanding outside the US). 10 bp in and out each January.*

![Distribution](../figures/fs05_dist.png)

## 2. Strategy description

Malkiel's line in *A Random Walk Down Wall Street* (1973) became a test. The Wall Street Journal ran a Dartboard contest from 1988 to 2002 in which professionals' picks were set against darts; the pros won more often, but part of their edge was the publicity of being named in the paper (Barber & Loeffler 1993; Metcalf & Malkiel 1994). Arnott, Hsu, Kalesnik & Tindall (2013) showed why random portfolios tend to beat cap-weighted indices: any weighting that ignores market cap tilts towards smaller and cheaper stocks.

| Rule | Original | This factsheet |
|---|---|---|
| Selection | Darts at the stock pages | Uniform random draw from the point-in-time universe |
| Size of portfolio | 30 stocks in Arnott et al. | 30 (US, EU, UK, World), 20 (SCANDI), 10 (DK) |
| Weighting and holding | Equal weight, rebalanced yearly | Same; buy and hold within the year |
| Benchmark | Cap-weighted index | Size-weighted universe (see note) and equal-weight universe |

## 3. Data load

{BF.universe_table()}
- **Data gap:** no market caps outside the US; the index is proxied by traded-value weights, which over-weight the most traded (not necessarily largest) stocks.

## 4. "Signal" creation

None: each January 10,000 monkeys draw their stocks uniformly at random from the names eligible at the end of December (seeded, reproducible).

## 5. Model build

Equal weight at formation, buy and hold for the calendar year; a name that stops trading earns zero after its last price. 20 bp round trip charged each January. Code: `code/monkey.py`, `code/build_monkey.py`.

## 6. Performance in detail

**Share of monkeys beating the index each year (equal-weight universe minus index in brackets)**

{yearly}
![Years](../figures/fs05_years.png)

## 7. Trading record

Each monkey trades once a year. The average of all monkeys equals the equal-weight universe held from January (differences come from mid-year index changes and costs). The median monkey lags the average ({', '.join(f"{UN[R]} {p(M[R]['monkey_cagr_pct']['50'] - M[R]['mean_monkey_cagr'])}" for R in U)} a year) because a concentrated portfolio compounds below its average return: the more volatile the stocks, the larger the gap.

## 8. Risk and attribution

Median monkey minus index, regressed on the equal-weight universe minus index (monthly, Newey-West t):

{table(["Universe", "Slope on EW − index", "Alpha / yr", "t", "Correlation of EW − index with the small-minus-big size sort"], [[UN[R], f"{att[R]['slope']:.2f}", p(att[R]['alpha']), f"{att[R]['t']:.2f}", f"{att[R]['corr_size']:+.2f}"] for R in U])}
The slope near 1 says the monkey is the equal-weight universe; what is left (the alpha) is mostly the concentration drag from holding few names.

## 9. Statistical verdict

- No hypothesis test is needed for the headline: the monkeys' expected return equals the equal-weight universe by construction. The question is only how equal weight compares with size weight in each market, and that is the size effect (FS07).
- The share beating the index is above 50% in {sum(b > 0.5 for b in beat)} of 6 markets, which are the markets where the equal-weight universe beat the index over the period.

## 10. What goes wrong, and how to fix it

Nothing goes wrong: the monkey does exactly what equal weighting does. It wins when small stocks beat big ones (UK, DK, EU over this period) and loses when mega-caps lead (the US). Two lessons for any stock-picking strategy: (1) **always compare with the equal-weight universe as well as the index**, otherwise a size tilt looks like skill; (2) **concentration costs**: the typical 30-stock portfolio compounds below the average one. The "fix" is simply to hold more names, which moves the monkey towards the equal-weight universe.

## 11. Classification: where does it fit?

| Dimension | Monkey portfolios |
|---|---|
| Series family | **Portfolio folklore** |
| Academic style | Benchmark test; non-cap weighting (Arnott et al. 2013) |
| Signal | None (random) |
| Exposure | Equal-weight minus cap-weight: small-cap tilt (and value, per Arnott et al.) |
| Where it fits | A **benchmark**, not a factor. It belongs in the factor battery only as the equal-weight reference against which every other strategy is judged |

![Classification map](../figures/battery_map.png)

## 12. 360° view

The monkey's neighbourhood is the equal-weight universe (identical in expectation) and the size sort: the equal-weight-minus-index spread correlates {', '.join(f"{UN[R]} {att[R]['corr_size']:+.2f}" for R in U)} with the small-minus-big size sort of the signal library. Everything the monkey "knows" is size.

## 13. Caveats

1. **Index proxy.** Outside the US the index is traded-value weighted, which differs from free-float cap weights.
2. **Residual survivorship.** 9–25% of member-quarters outside the US lack a price; delisted names are the most likely missing.
3. **Currency.** Local currency; World mixes currencies.
4. **Not a registered trial.**

## 14. Academic references

- Malkiel, B. (1973). *A Random Walk Down Wall Street*. W. W. Norton.
- Arnott, R., Hsu, J., Kalesnik, V. & Tindall, P. (2013). The surprising alpha from Malkiel's monkey and upside-down strategies. *Journal of Portfolio Management*, 39(4), 91–105.
- Barber, B. & Loeffler, D. (1993). The "Dartboard" column: Second-hand information and price pressure. *Journal of Financial and Quantitative Analysis*, 28(2), 273–284.
- Metcalf, G. & Malkiel, B. (1994). The Wall Street Journal contests: The experts, the darts, and the efficient market hypothesis. *Applied Financial Economics*, 4(5), 371–374.
- Banz, R. (1981). The relationship between return and market value of common stocks. *Journal of Financial Economics*, 9(1), 3–18.

## 15. Reproduce

`code/xs.py` (inputs) → `monkey.py` → `build_monkey.py`.
"""
    BF.write("FS05_Monkey_Portfolios", md, "FS05 Monkey portfolios: factsheet")
    BF.pdf("FS05_Monkey_Portfolios")


if __name__ == "__main__":
    build(); print("built FS05")
