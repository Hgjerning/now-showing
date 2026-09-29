# -*- coding: utf-8 -*-
"""FS13b: US fundamentals at stock level (Sharadar, point in time) through the factsheet engine."""
import json
import os

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

import build_factsheets as BF
import fundamentals as FU
import perf

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); FIG = os.path.join(HERE, "..", "figures")
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
TC = {"Debt issuance": "#2a78d6", "Profit growth": "#0f8a6a", "Value": "#c0392b", "Profitability": "#8e5bb5", "Investment": "#d4880f", "Accruals": "#6b6a66"}
p = lambda x, d=1: f"{x * 100:+.{d}f}%"


def figs(R, out):
    S = R["stats"]; order = [k for t in FU.THEMES for k in list(FU.FUND) + [FU.COMP[t]] if R["theme"][k] == t]
    fig, axs = plt.subplots(1, 2, figsize=(13, 7.2), sharey=True); fig.patch.set_facecolor(SURF)
    y = np.arange(len(order))[::-1]
    for ax, key, title in ((axs[0], "bn_t", "Beta-neutral long/short, t-statistic"), (axs[1], "lo_t_alpha", "Long-only alpha vs equal-weight universe, t")):
        v = [S[k][key] for k in order]
        ax.barh(y, v, color=[TC[R["theme"][k]] for k in order], alpha=[1 if k.startswith("c_") else 0.55 for k in order][0] if False else None)
        for yi, k, vi in zip(y, order, v):
            if k.startswith("c_"):
                ax.barh(yi, vi, color=TC[R["theme"][k]], edgecolor=INK, linewidth=1.2)
        for g in (-2, 2):
            ax.axvline(g, color=INK2, lw=0.8, ls=":")
        ax.axvline(0, color=INK2, lw=1); ax.set_title(title, loc="left", fontsize=11.5); ax.set_facecolor(SURF); ax.grid(axis="x", color=GRID)
        for sp_ in ax.spines.values(): sp_.set_visible(False)
    axs[0].set_yticks(y); axs[0].set_yticklabels([R["labels"][k] for k in order], fontsize=9)
    fig.suptitle("US top 500, 2013–2026, net of costs, borrow and financing (outlined bars = theme composites)", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs13b_signals.png"), dpi=140, facecolor=SURF); plt.close(fig)
    fig, ax = plt.subplots(figsize=(11, 5.2)); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    for t in FU.THEMES:
        s = out[FU.COMP[t]].bn_net.dropna(); ax.plot((1 + s).cumprod(), color=TC[t], lw=2, label=t)
    ax.set_yscale("log"); ax.axhline(1, color=INK2, lw=0.8); ax.legend(frameon=False, ncol=3, fontsize=9); ax.grid(color=GRID)
    for sp_ in ax.spines.values(): sp_.set_visible(False)
    ax.set_title("Growth of 1 in the beta-neutral theme composites, US top 500, net", loc="left", fontsize=11.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs13b_themes.png"), dpi=140, facecolor=SURF); plt.close(fig)


def build():
    R = json.load(open(os.path.join(RES, "fund_battery.json"))); out = pd.read_pickle(os.path.join(RES, "fund_battery.pkl")); S = R["stats"]
    figs(R, out)
    C = {t: S[FU.COMP[t]] for t in FU.THEMES}
    O = json.load(open(os.path.join(RES, "common_ground.json"))); TH = {r["theme"]: r for r in O["themes"]}
    jmap = {"Debt issuance": "Debt issuance", "Profit growth": "Profit growth", "Value": "Value", "Profitability": "Profitability", "Investment": "Investment", "Accruals": "Accruals"}
    best = max(FU.THEMES, key=lambda t: C[t]["bn_t"]); worst = min(FU.THEMES, key=lambda t: C[t]["bn_t"])
    pg, di, va, inv = C["Profit growth"], C["Debt issuance"], C["Value"], C["Investment"]
    LG = json.load(open(os.path.join(RES, "trial_ledger.json"))); fb_pass = [f"{r['strategy']} ({r['test']})" for r in LG["passes"] if r["fs"] == "FS13b"]
    dd = [d for d in LG["dsr"] if d["fs"] == "FS13b"]
    dsr_txt = (f"its deflated Sharpe ratio is {dd[0]['dsr_null']:.2f} on the lenient bound, below the 0.95 bar" if dd else "no FS13b signal is among the strongest candidates for the deflated Sharpe check")
    pos_both = [t for t in FU.THEMES if C[t]["design"] > 0 and C[t]["holdout"] > 0]
    def_rows = [[FU.FUND[k][2], FU.FUND[k][0], "high" if FU.FUND[k][1] else "low", f"`{k}`", f"`{FU.FUND[k][3]}`"] for k in FU.FUND]
    rows = []
    for t in FU.THEMES:
        for k in [k for k in FU.FUND if FU.FUND[k][0] == t] + [FU.COMP[t]]:
            v = S[k]; b = k.startswith("c_")
            nm = f"**{R['labels'][k]}**" if b else R["labels"][k]
            rows.append([nm, f"{p(v['ann'])} (t {v['t']:+.1f})", f"{p(v['bn_ann'])} (t {v['bn_t']:+.1f})", f"{v['lo_t_alpha']:+.1f}", f"{v['design']:+.2f} / {v['holdout']:+.2f}", p(v["cost"]), f"{v['repl']:.2f}"])
    span = [[R["labels"][FU.COMP[t]], p(C[t]["bn_ann"]), f"{p(C[t]['span_alpha'])} (t {C[t]['span_t']:+.1f})", f"{C[t]['span_r2']:.2f}", ", ".join(f"{k} {v:+.2f}" for k, v in S[FU.COMP[t]]["nearest_price"])] for t in FU.THEMES]
    cc = pd.DataFrame(R["comp_corr"]).loc[FU.THEMES, FU.THEMES]
    cc_rows = [[t] + [f"{cc.loc[t, u]:+.2f}" for u in FU.THEMES] for t in FU.THEMES]
    jk_rows = [[t, f"{TH[jmap[t]]['jkp_pre']['usa']:+.2f}", f"{TH[jmap[t]]['jkp_sh']['usa']:+.2f}", f"{perf.sharpe(out[FU.COMP[t]].bn_net.dropna()):+.2f}", f"{C[t]['repl']:.2f}"] for t in FU.THEMES]
    md = f"""# FACTSHEET FS13b · US fundamentals, stock by stock

### Do the published fundamental themes work in our own US engine?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

| Key facts | |
|---|---|
| Universe | US, point-in-time top 500 by market cap (Sharadar), monthly, Feb 2013 – Aug 2026 |
| Data | Sharadar SF1 as-reported quarterly filings (ARQ), used from the filing date; a filing older than 200 days is dropped |
| Signals | 14 fundamental signals in 6 themes (debt issuance, profit growth, value, profitability, investment, accruals) plus one composite per theme |
| Books | top-minus-bottom decile, equal weight; long/short, beta-neutral long/short, long-only vs the equal-weight universe |
| Costs | 10 bp per side, size-tiered borrow fee on the short leg, financing of net long cash (USD risk-free + 0.5%) |
| Checks | correlation with the matching JKP US factor; spanning by the price shortlist (low beta, momentum, residual momentum, 52-week high) |

> **In one paragraph.** FS13 found that the published JKP factors put **debt issuance** and **profit growth** on common ground in every segment. Built stock by stock in our US universe, **profit growth** holds up: the composite earns {p(pg['bn_ann'])} a year beta-neutral (t {pg['bn_t']:.1f}), its long-only book beats the equal-weight universe after beta (alpha t {pg['lo_t_alpha']:.1f}), it is positive in both the 2013–19 design and the 2020–26 holdout window, and it keeps an alpha of {p(pg['span_alpha'])} (t {pg['span_t']:.1f}) after the price shortlist. **Debt issuance** is weaker here: {p(di['ann'])} a year long/short (t {di['t']:.1f}), mostly carried by the long side (long-only alpha t {di['lo_t_alpha']:.1f}). **Value** ({p(va['ann'])}, t {va['t']:.1f}) and **investment** ({p(inv['bn_ann'])} beta-neutral, t {inv['bn_t']:.1f}) lost money in US large caps since 2013, matching JKP's "faded in the US". Our books track the published JKP US themes closely for value, profit growth and investment (correlation {min(S[FU.COMP[t]]['repl'] for t in ['Value','Profit growth','Investment']):.2f}–{max(S[FU.COMP[t]]['repl'] for t in ['Value','Profit growth','Investment']):.2f}) and more loosely for debt issuance, profitability and accruals ({min(S[FU.COMP[t]]['repl'] for t in ['Debt issuance','Profitability','Accruals']):.2f}–{max(S[FU.COMP[t]]['repl'] for t in ['Debt issuance','Profitability','Accruals']):.2f}), where SF1's aggregated lines differ from JKP's inputs. Profit growth and investment are strongly opposed (correlation {cc.loc['Profit growth', 'Investment']:+.2f}): growing firms improve their profits and also grow their assets.

![Signals](../figures/fs13b_signals.png)

## 1. Data and point-in-time rules

Sharadar SF1, dimension ARQ: each quarterly report as first filed, with its filing date. At every month-end a stock carries the latest filing dated on or before that day; filings older than 200 days are dropped, so a stock that stops reporting drops out. Flows (revenue, net income, gross profit, operating income, operating cash flow) are summed over the last four quarters where a level ratio needs a year; four-quarter changes require the earlier quarter to be 330–400 days back. Market capitalisation is the month-end value from the same source used for the universe. Every signal is winsorised at the 1st and 99th percentile each month. Coverage: about 620–650 of the ~800 stocks that are ever in the top 500 have a value in a typical month; the sort uses the stocks that are in the top 500 that month.

## 2. Definitions

{BF.table(["Signal", "Theme", "Long the", "Code", "JKP match"], def_rows)}

*Composites average the members' percentile ranks, each signed so that high means good. Definitions follow JKP (Jensen, Kelly & Pedersen 2023) where SF1 has the inputs; net operating assets, net financial assets and the debt measures use SF1's aggregate balance-sheet lines, so they are approximations.*

## 3. Results

{BF.table(["Signal", "L/S net / yr", "Beta-neutral net / yr", "Long-only alpha t", "Beta-neutral Sharpe 2013–19 / 2020–26", "Cost / yr", "Correlation with JKP US"], rows)}

*Monthly, Feb 2013 – Aug 2026, USD. Newey–West t (6 lags). Long-only alpha: CAPM against the equal-weight universe. JKP correlation: our gross long/short against the matching JKP US factor (theme average for composites), Feb 2013 – Dec 2025.*

![Themes](../figures/fs13b_themes.png)

**Reading it.**

1. **Profit growth is the one theme that works on every test.** Earnings changes scaled by assets or equity carry it; the sales surprise adds little on its own.
2. **Debt issuance works mainly on the long side.** Firms that shrink debt and net operating assets beat the universe, but the short leg (firms raising debt) is not reliably bad in large caps, so the beta-neutral book is flat.
3. **Value and investment lost** in the growth-led US market of 2013–2026. Book-to-market has the highest replication with JKP ({S['bm']['repl']:.2f}), so this is the premium, not the code.
4. **Profitability** is positive once beta-neutral but not significant; **accruals** are positive and weak.
5. Themes that are positive in both the design and the holdout window: {', '.join(pos_both) or 'none'}.

## 4. Against the published factors

{BF.table(["Theme", "JKP US Sharpe before 2013", "JKP US Sharpe 2013–25", "Our beta-neutral Sharpe 2013–26", "Correlation of our L/S with JKP"], jk_rows)}

Both sources agree that profit growth kept working after 2013. JKP shows investment and accruals fading in the US; in our large-cap books value and investment went further and lost money. JKP's debt issuance is stronger than ours, partly because its definitions use detailed financing lines that SF1 aggregates.

## 5. Do they add anything to the price signals?

{BF.table(["Composite", "Beta-neutral return / yr", "Alpha after the price shortlist (t)", "R² on the price shortlist", "Closest price signals (correlation)"], span)}

*Regression of each beta-neutral composite on the beta-neutral low-beta, 12-1 momentum, residual momentum and 52-week-high books (FS13), Newey–West t.*

Profit growth keeps most of its return after the price signals: it is related to momentum (firms with rising earnings tend to have rising prices) but not explained by it. This makes it the strongest candidate to add to the multifactor model.

## 6. How the themes relate

{BF.table(["", *FU.THEMES], cc_rows)}

*Correlation of the beta-neutral theme composites, monthly.*

## 7. What goes into the multifactor model (FS14)

- **Add:** the profit-growth composite; debt issuance as a long-side tilt.
- **Keep as diversifiers, not as return sources:** profitability (low correlation with momentum), value (negatively correlated with profit growth and momentum, so it may pay in the next reversal but has cost money since 2013).
- **Leave out:** investment and accruals on their own; their information is largely inside profit growth and value.
- All of this is US only. For the other five markets, JKP factor returns remain the only fundamental source until a global fundamentals feed is added (FS00).

## 8. Caveats

- **Financials are included**; ratios such as gross profitability and net operating assets mean little for banks and insurers. A sector filter needs industry codes (FS00 gap).
- **US only**, top 500, equal weight; JKP is value-weighted over the whole market.
- **Aggregated balance-sheet lines** make the debt-issuance measures approximate (JKP correlation {min(S[k]['repl'] for k in ['dbt_gr', 'noa_at', 'nfna_gr']):.2f}–{max(S[k]['repl'] for k in ['dbt_gr', 'noa_at', 'nfna_gr']):.2f}).
- **Multiple testing.** 20 signals × three books add 60 trials to the factsheet ledger, now {LG['n']} in all. Programme-wide, {('none of the 60 survives the correction; the closest is profit growth' + chr(39) + 's long-only alpha (t ' + format(pg['lo_t_alpha'], '.1f') + ')') if not fb_pass else (str(len(fb_pass)) + ' of the 60 survive' + ('s' if len(fb_pass) == 1 else '') + ' the Benjamini–Hochberg correction: ' + ', '.join(fb_pass))}; {dsr_txt} (`planning/FACTSHEET_TRIAL_LEDGER.md`).

## 9. References

- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Novy-Marx, R. (2013). The other side of value: the gross profitability premium. *Journal of Financial Economics* 108(1), 1–28.
- Fama, E. F. & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics* 116(1), 1–22.
- Cooper, M. J., Gulen, H. & Schill, M. J. (2008). Asset growth and the cross-section of stock returns. *Journal of Finance* 63(4), 1609–1651.
- Hirshleifer, D., Hou, K., Teoh, S. H. & Zhang, Y. (2004). Do investors overvalue firms with bloated balance sheets? *Journal of Accounting and Economics* 38, 297–331.
- Richardson, S. A., Sloan, R. G., Soliman, M. T. & Tuna, I. (2005). Accrual reliability, earnings persistence and stock prices. *Journal of Accounting and Economics* 39(3), 437–485.
- Jegadeesh, N. & Livnat, J. (2006). Revenue surprises and stock returns. *Journal of Accounting and Economics* 41(1–2), 147–171.
- Sloan, R. G. (1996). Do stock prices fully reflect information in accruals and cash flows about future earnings? *The Accounting Review* 71(3), 289–315.
- Fama, E. F. & French, K. R. (1992). The cross-section of expected stock returns. *Journal of Finance* 47(2), 427–465.
- Basu, S. (1977). Investment performance of common stocks in relation to their price-earnings ratios. *Journal of Finance* 32(3), 663–682.

## 10. Reproduce

`code/fundamentals.py` (point-in-time signals from `us_fundamentals.csv`, licensed, not published) → `code/fund_battery.py` (engine, replication, spanning → `results/fund_battery.json`) → `code/build_fs13b.py`.
"""
    BF.write("FS13b_US_Fundamentals", md, "FS13b US fundamentals")
    BF.pdf("FS13b_US_Fundamentals")


if __name__ == "__main__":
    build(); print("built FS13b")
