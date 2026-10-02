# -*- coding: utf-8 -*-
"""FS16: costs that grow with size (spread + square-root impact) and capacity."""
import json
import os

import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.environ.get("FS_RESULTS") or os.path.join(HERE, "..", "results"); FIG = os.environ.get("FS_FIGURES") or os.path.join(HERE, "..", "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
COL = {"US": "#2a78d6", "EU": "#0f8a6a", "UK": "#c0392b", "DK": "#8e5bb5", "SC": "#d4880f", "WD": "#52514e"}
SZ = ["$1m", "$10m", "$100m", "$1bn", "$10bn"]


def money(x):
    if x is None:
        return "—"
    if not np.isfinite(x):
        return "> $10bn"
    if x < 1e6:
        return "< $1m"
    return f"${x / 1e9:.1f}bn" if x >= 1e9 else f"${x / 1e6:.0f}m"


def fig(r, rb):
    fig, ax = plt.subplots(figsize=(10, 5.6)); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    x = np.log10(r["aums"])
    for R in U:
        ax.plot(x, r[R]["shortlist"]["Y07"]["sharpe"], color=COL[R], lw=2.2, marker="o", label=f"{UN[R]}")
        ax.plot(x, rb[R]["sharpe"], color=COL[R], lw=1.3, ls="--")
    ax.axhline(0, color=INK2, lw=1); ax.set_xticks(x); ax.set_xticklabels(SZ); ax.grid(color=GRID)
    ax.set_ylim(-2.2, 1.1); ax.set_xlabel("capital in the book"); ax.set_ylabel("Sharpe ratio, net of spread, impact, borrow and financing")
    ax.legend(frameon=False, ncol=3, fontsize=9, title="solid: as pre-registered · dashed: with a turnover buffer", title_fontsize=8.5)
    for sp_ in ax.spines.values(): sp_.set_visible(False)
    ax.set_title("The shortlist (low beta + 12-1 momentum, beta-neutral), 2013–2026: Sharpe ratio against size", loc="left", fontsize=11.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs16_capacity.png"), dpi=140, facecolor=SURF); plt.close(fig)


def build():
    r = json.load(open(os.path.join(RES, "impact.json"))); rb = json.load(open(os.path.join(RES, "impact_buffer.json"))); rl = json.load(open(os.path.join(RES, "impact_liquid.json")))
    fig(r, rb)
    books = r["books"]
    sl_rows = [[UN[R], *[f"{v:+.2f}" for v in r[R]["shortlist"]["Y07"]["sharpe"]], money(r[R]["shortlist"]["Y07"]["capacity"]["half"]), money(r[R]["shortlist"]["Y07"]["capacity"]["zero"])] for R in U]
    bf_rows = [[UN[R], f"{rb[R]['turnover']:.2f}", *[f"{v:+.2f}" for v in rb[R]["sharpe"][:4]], money(rb[R]["capacity"]["half"]), money(rb[R]["capacity"]["zero"])] for R in U]
    lq_rows = [[UN[R], rl[R]["n_med"], *[f"{v:+.2f}" for v in rl[R]["sharpe"][:4]], money(rl[R]["capacity"]["half"]), money(rl[R]["capacity"]["zero"])] for R in U]
    bk_rows = []
    for b in books:
        for R in U:
            q = r[R][b]
            bk_rows.append([b if R == "US" else "", UN[R], f"{q['flat']['sharpe']:+.2f}", f"{q['Y07']['sharpe'][0]:+.2f}", f"{q['Y07']['sharpe'][2]:+.2f}", f"{q['Y07']['sharpe'][3]:+.2f}", f"{q['Y10']['sharpe'][2]:+.2f}",
                            f"{q['spread_cost'] * 100:.1f}%", f"{q['Y07']['cost'][2] * 100:.1f}%", f"{q['turnover']:.2f}", money(q["Y07"]["capacity"]["zero"])])
    us, wd = r["US"]["shortlist"]["Y07"], r["WD"]["shortlist"]["Y07"]
    eu_uk = [money(r[R]["shortlist"]["Y07"]["capacity"]["zero"]) for R in ("EU", "UK", "DK")]
    fast = {R: r[R]["short-term reversal (L/S)"]["Y07"]["sharpe"][1] for R in U}
    md = f"""# FACTSHEET FS16 · Costs that grow with size

### How much money can these strategies hold before trading costs eat them?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

| Key facts | |
|---|---|
| Rules | `planning/PREREG_FS16.md`, written in the build environment before the run (10:13) and copied to the Factsheets folder right after it (the run finished 10:16); no changes |
| Cost per trade | half-spread 5 bp × (ADV / $50m)^−0.3, 2–50 bp, plus square-root impact 0.7 × daily volatility × √(trade / ADV); sensitivity 1.0 |
| ADV | 63-day average traded value in USD per stock (US: price × volume where the Project1 cache has it; otherwise market cap × the size-quintile median ratio) |
| Sizes | $1m, $10m, $100m, $1bn, $10bn of capital per book |
| Books | the shortlist (low beta + 12-1 momentum, beta-neutral) and four raw long/short books, six markets, 2013–2026; borrow fees and financing as before |
| Replaces | the flat 10 bp per side used in FS01–FS15 |

> **In one paragraph.** Capacity is the binding constraint for these books, far more than the flat-cost results suggested. The shortlist keeps a positive Sharpe ratio up to about **{money(us['capacity']['zero'])} in the US** and **{money(wd['capacity']['zero'])} across World**, but only **{eu_uk[0]} in the EU, {eu_uk[1]} in the UK and {eu_uk[2]} in Denmark**, and nothing in Scandinavia. The UK and EU books look best at small size because their low-beta legs sit in thinly traded stocks, which is also why they fill up first. The fast signals are uninvestable: short-term reversal has a Sharpe ratio of {min(fast.values()):+.2f} to {max(fast.values()):+.2f} already at $10m. Two exploratory fixes help: a turnover buffer (hold a stock until it leaves the top 30%) halves turnover and raises the size at which the Sharpe ratio halves {min(rb[R]['capacity']['half'] / r[R]['shortlist']['Y07']['capacity']['half'] for R in U if r[R]['shortlist']['Y07']['capacity']['half'] and rb[R]['capacity']['half']):.0f}–{max(rb[R]['capacity']['half'] / r[R]['shortlist']['Y07']['capacity']['half'] for R in U if r[R]['shortlist']['Y07']['capacity']['half'] and rb[R]['capacity']['half']):.0f} times with little loss at small size; a liquidity screen raises capacity in the EU and World but removes most of the UK result.

![Capacity](../figures/fs16_capacity.png)

## 1. The shortlist, as pre-registered

{BF.table(["Market", *SZ, "Sharpe halves at", "Net return reaches zero at"], sl_rows)}

*Sharpe ratio, net of spread, impact (Y = 0.7), borrow fees and financing, 2013–2026. Capital per book; the combined shortlist puts half in each leg.*

## 2. Every book, every market

{BF.table(["Book", "Market", "Flat 10 bp", "$1m", "$100m", "$1bn", "$100m, Y = 1.0", "Spread cost / yr", "All-in cost / yr at $100m", "Monthly turnover", "Net return reaches zero at"], bk_rows)}

**Reading it.**

1. **At $1m the model is close to the flat 10 bp in large-cap markets and harsher in small ones**: the spread alone costs more than 10 bp per side in the UK, EU and Scandinavian small caps.
2. **Impact grows with the square root of size**, so costs rise about three times for every tenfold increase in capital, and far faster in markets where the traded stocks are thin.
3. **Slow signals scale; fast ones do not.** Low volatility and low beta change little from month to month; reversal and low MAX replace most of the book every month and collapse even at $10m.
4. **Beta-neutral books pay twice**: their low-beta leg is levered up (about 2× in most markets), so its trades are twice as large as the capital suggests.

## 3. Exploratory fix 1 · A turnover buffer (not pre-registered)

{BF.table(["Market", "Monthly turnover (was about 0.5)", "$1m", "$10m", "$100m", "$1bn", "Sharpe halves at", "Net return reaches zero at"], bf_rows)}

*The FS03–FS12 fix ladder's buffer: a stock enters in the top decile (quintile, tercile) and is sold only when it leaves the top 30%.*

## 4. Exploratory fix 2 · A liquidity screen (not pre-registered)

{BF.table(["Market", "Stocks left (median)", "$1m", "$10m", "$100m", "$1bn", "Sharpe halves at", "Net return reaches zero at"], lq_rows)}

*Stocks with less than $5m average daily traded value removed before sorting.*

## 5. What it means

1. **The factsheet results are small-fund results.** Outside the US and World, the shortlist's edge disappears somewhere between $10m and $100m per book with monthly rebalancing.
2. **A buffer is the cheapest capacity there is**: it keeps most of the small-size Sharpe ratio and multiplies capacity.
3. **The UK low-beta premium lives in thin stocks.** Screened for liquidity, it largely goes away: a warning for anyone reading FS10's UK result as investable at scale.
4. **For the multifactor model**, cost-aware construction (buffers, trading towards targets over several days, liquidity-weighted positions) matters more than the choice of signals.

## 6. Caveats

- One cost model with textbook parameters; real costs depend on execution skill, venue and timing. Y = 1.0 is shown as the harsher case.
- US volume data are missing for about a third of the stocks ever in the US universe (mostly delisted names); their ADV comes from market cap, a proxy.
- Trades are costed as if done in one day; spreading large trades over several days lowers impact but adds tracking error.
- The exploratory sections were decided after seeing the pre-registered results and are not tests.

## 7. References

- Almgren, R., Thum, C., Hauptmann, E. & Li, H. (2005). Direct estimation of equity market impact. *Risk* 18(7), 58–62.
- Frazzini, A., Israel, R. & Moskowitz, T. J. (2018). Trading costs. Working paper, AQR Capital Management.
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies* 29(1), 104–147.
- Korajczyk, R. A. & Sadka, R. (2004). Are momentum profits robust to trading costs? *Journal of Finance* 59(3), 1039–1082.
- Bouchaud, J.-P., Bonart, J., Donier, J. & Gould, M. (2018). *Trades, Quotes and Prices*. Cambridge University Press.

## 8. Reproduce

`planning/PREREG_FS16.md` → `code/impact.py` (`run`, and the exploratory `run_buffer`, `run_liquid`) → `code/build_fs16.py`. US volume from the Project1 price cache (`_data_private/pit/US_tradedvalue.parquet`, private).
"""
    BF.write("FS16_Costs_And_Capacity", md, "FS16 Costs that grow with size")
    BF.pdf("FS16_Costs_And_Capacity")


if __name__ == "__main__":
    build(); print("built FS16")
