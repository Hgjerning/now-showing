# FACTSHEET FS13 · The signal battery

### Every signal in every market: where is the common ground?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · price data to 31 August 2026, JKP to December 2025*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

| Key facts | |
|---|---|
| Price battery | 19 price signals × 6 point-in-time universes (US, EU, UK, DK, SCANDI, World), monthly, 2013–2026, our engine, net of 10 bp per side and a size-tiered borrow fee on the short leg |
| Published battery | 153 JKP factors (Jensen, Kelly & Pedersen 2023) × 5 segments (US, UK, Denmark, World ex US, World), 2013–2025, grouped into 13 themes |
| Direction | fixed from the literature before the run (table in §1); no signal was flipped after seeing results |
| Books | long/short (top minus bottom quantile), beta-neutral long/short (charged for the cash it borrows at the USD risk-free rate + 50 bp), long-only vs the equal-weight universe |
| Pooled test | equal-weight average of the markets; its t-statistic includes the co-movement between markets |
| Multiple testing | Benjamini–Hochberg at 5% over 38 price tests (19 signals × raw/beta-neutral) and over 153 JKP factors; Harvey–Liu–Zhu t > 3 as a second bar |

> **In one paragraph.** **No price signal earns a positive return that survives the multiple-testing correction** once short legs pay borrow fees and the beta-neutral books pay for the leverage they use; thirteen years of large caps are too short for more. What does survive is a loser: Same-month seasonality (beta-neutral) reliably loses money. The common ground is in the *direction*. **Low beta** is positive in 6 of 6 of our markets after all costs (t 2.4) but flat in JKP's value-weighted factors. **Momentum** is positive in 6 of 6 of our markets (12-1 momentum 5 of 6, residual momentum 6 of 6) and in all 4 JKP segments (t 4.4); in our large caps it is not significant on its own (t 1.5). Among the fundamental themes we cannot yet build ourselves, **debt issuance** (t 6.2) and **profit growth** (t 2.5) worked in every JKP segment since 2013. **Same-month seasonality** and **tail direction** are reliably negative in our large caps. The 19 price signals hold only a handful of independent bets: one low-risk block of nine and one momentum block of four, the same structure in the US, EU and World (adjusted Rand index 0.87–1.00). SCANDI and UK agree least with the other markets on which signals work. The engine reproduces the published US factors (correlation ≥ 0.8 for 7 of 12 matched signals).

![Common ground map](../figures/fs13_common_map.png)

## 1. What was tested

Two batteries, one question: which signals work across segments, and which only in one corner?

**Price battery (our data, our engine).** Every signal in the library (`code/signals.py`, `signals2.py`) runs through the same sort engine as FS03–FS12 (`code/xs.py`) in all six universes: monthly quantile sort (deciles ≥ 100 names, quintiles 50–99, terciles below), equal weight, 10 bp per side on turnover. Three books per signal: long/short, **beta-neutral** long/short (each leg scaled to beta 1 before netting, so the market bet that dominated FS02 and FS04 is removed), and long-only against owning all stocks equally. The direction of every signal was set from the literature before running:

| Signal | Family | Long the | Direction from |
|---|---|---|---|
| Low MAX (1 day) | Lottery & tails | low | Bali, Cakici & Whitelaw 2011 |
| Low MAX (5 days) | Lottery & tails | low | Bali, Cakici & Whitelaw 2011 |
| Mild worst day (MIN) | Lottery & tails | high | low-risk convention: small crashes |
| Mild worst 5 days | Lottery & tails | high | low-risk convention |
| Narrow daily range | Lottery & tails | low | low-risk convention |
| Low net tail | Lottery & tails | low | Boyer, Mitton & Vorkink 2010 (low skew) |
| Low skewness | Lottery & tails | low | Boyer, Mitton & Vorkink 2010 |
| Low idiosyncratic vol | Low risk | low | Ang, Hodrick, Xing & Zhang 2006 |
| Low volatility (63d) | Low risk | low | Blitz & van Vliet 2007 |
| Low volatility (252d) | Low risk | low | Blitz & van Vliet 2007 |
| Low beta | Low risk | low | Frazzini & Pedersen 2014 |
| Short-term reversal | Reversal | low | Jegadeesh 1990 |
| Momentum 12-1 | Momentum | high | Jegadeesh & Titman 1993 |
| Residual momentum | Momentum | high | Blitz, Huij & Martens 2011 |
| Same-month seasonality | Seasonality | high | Heston & Sadka 2008 |
| Near 52-week high | Momentum | high | George & Hwang 2004 |
| Far above 52-week low | Momentum | high | momentum-consistent (falling knife loses) |
| Near 55-day high | Momentum | high | Turtle breakout, cross-sectional |
| Small size | Size | low | Banz 1981 |


*Two directions are conventions rather than paper results: MIN and the daily range follow the low-risk reading (small tails are good), and "far above the 52-week low" is the momentum reading, which FS12 had already shown. Treat those three as less than fully out-of-sample.*

**Published battery (JKP).** The 153 factors of Jensen, Kelly & Pedersen (2023, *Is There a Replication Crisis in Finance?*), capped value-weighted long/short, in USD, signed so the original paper's prediction is positive, grouped into their 13 themes. JKP covers fundamentals (value, quality, investment, profitability, accruals, debt issuance) that we do not yet have outside the US. Segments: US, UK, Denmark, World ex US (disjoint from the US) and World. **There is no JKP file for EU or Scandinavia in our cache and the JKP site is not reachable from the build environment; World ex US stands in for both where a comparison is needed.**

## 2. The price battery: every signal, every market

![Price heatmap](../figures/fs13_price_heatmap.png)

| Signal | Family | L/S net, 6-market average | L/S > 0 | Beta-neutral, net of costs and financing (✓ = BH) | Beta-neutral > 0 | Long-only beats EW Sharpe | Effective markets | Cost / yr | Beta-neutral Sharpe 2013–19 / 2020–26 |
|---|---|---|---|---|---|---|---|---|---|
| Low beta | Low risk | -6.0% (t -1.2) | 0 / 6 | +10.0% (t +2.4) | 6 / 6 | 5 / 6 | 1.6 | +0.5% | +1.13 / +0.13 |
| Momentum 12-1 | Momentum | +5.1% (t +1.3) | 5 / 6 | +6.5% (t +2.2) | 5 / 6 | 5 / 6 | 1.8 | +1.2% | +0.77 / +0.37 |
| Low volatility (252d) | Low risk | -3.8% (t -0.8) | 1 / 6 | +5.4% (t +1.7) | 6 / 6 | 6 / 6 | 1.7 | +0.4% | +0.67 / +0.24 |
| Low volatility (63d) | Low risk | -3.1% (t -0.7) | 1 / 6 | +4.1% (t +1.3) | 6 / 6 | 6 / 6 | 1.8 | +1.2% | +0.68 / +0.12 |
| Residual momentum | Momentum | +3.5% (t +1.3) | 6 / 6 | +3.1% (t +1.2) | 6 / 6 | 6 / 6 | 1.9 | +2.0% | +0.20 / +0.46 |
| Low idiosyncratic vol | Low risk | -0.1% (t -0.0) | 3 / 6 | +2.7% (t +1.2) | 5 / 6 | 5 / 6 | 2.0 | +2.9% | +0.39 / +0.26 |
| Near 52-week high | Momentum | +0.8% (t +0.2) | 2 / 6 | +3.8% (t +1.1) | 5 / 6 | 5 / 6 | 1.6 | +2.0% | +0.46 / +0.18 |
| Narrow daily range | Lottery & tails | -3.5% (t -1.0) | 1 / 6 | +1.8% (t +0.6) | 4 / 6 | 3 / 6 | 1.9 | +3.1% | +0.32 / +0.06 |
| Low MAX (5 days) | Lottery & tails | -4.5% (t -1.2) | 0 / 6 | +1.5% (t +0.6) | 3 / 6 | 3 / 6 | 2.0 | +3.0% | +0.75 / -0.25 |
| Far above 52-week low | Momentum | +5.1% (t +1.7) | 6 / 6 | +1.0% (t +0.3) | 4 / 6 | 5 / 6 | 1.7 | +1.6% | +0.24 / -0.03 |
| Low MAX (1 day) | Lottery & tails | -4.2% (t -1.3) | 1 / 6 | +0.6% (t +0.2) | 3 / 6 | 2 / 6 | 2.0 | +3.3% | +0.40 / -0.18 |
| Mild worst 5 days | Lottery & tails | -4.8% (t -1.1) | 0 / 6 | +0.7% (t +0.2) | 4 / 6 | 3 / 6 | 1.7 | +3.0% | -0.05 / +0.16 |
| Near 55-day high | Momentum | -2.3% (t -0.7) | 2 / 6 | +0.3% (t +0.1) | 3 / 6 | 3 / 6 | 1.7 | +2.9% | -0.18 / +0.18 |
| Mild worst day (MIN) | Lottery & tails | -4.8% (t -1.4) | 0 / 6 | -0.0% (t -0.0) | 3 / 6 | 3 / 6 | 1.9 | +3.4% | -0.08 / +0.06 |
| Small size | Size | -0.7% (t -0.4) | 1 / 6 | -1.1% (t -0.5) | 2 / 6 | 1 / 6 | 2.9 | +0.3% | +0.59 / -0.64 |
| Low net tail | Lottery & tails | -3.8% (t -2.0) | 1 / 6 | -4.1% (t -2.4) | 1 / 6 | 0 / 6 | 2.4 | +4.0% | -0.27 / -0.94 |
| Short-term reversal | Reversal | -6.3% (t -2.0) | 1 / 6 | -6.8% (t -2.4) | 1 / 6 | 0 / 6 | 2.0 | +3.9% | -0.20 / -1.15 |
| Low skewness | Lottery & tails | -4.4% (t -2.5) | 1 / 6 | -4.7% (t -2.9) | 1 / 6 | 0 / 6 | 2.8 | +4.0% | -0.66 / -0.94 |
| Same-month seasonality | Seasonality | -6.6% (t -2.8) | 1 / 6 | -6.9% (t -3.4) ✓ | 1 / 6 | 1 / 6 | 2.3 | +3.9% | -0.71 / -1.07 |


*Averages are the equal-weight mean of the six market series; t is Newey–West on that mean. Effective markets = 36 / sum of the 6×6 correlation matrix. ✓ = discovery under Benjamini–Hochberg at 5% over 38 tests.*

**Reading it.**

1. **The raw long/short numbers are mostly a beta story.** 9 of the 9 low-risk and tail-size signals have a negative raw average and 8 of 9 turn positive once the legs are beta-neutral and financed. Their raw books are short the market in a market that rose.
2. **Beta-neutral low-risk books need a lot of leverage.** To bring the low-beta leg up to a beta of one, the low-beta book borrows on average 0.8–2.9 units of cash per unit of capital (US 2.2, EU 2.4, UK 2.9, DK 0.8, SCANDI 1.2, World 2.4). Charged at the USD risk-free rate plus 50 bp, low beta still earns +10.0% a year (Sharpe 0.48, t 2.4, positive in 6 of 6), the strongest positive price signal, but it no longer clears the correction. The charge is conservative for EU and Denmark, where short rates were negative for 2015–21.
3. **After the correction: 1 discovery out of 38**: Same-month seasonality (beta-neutral) (t -3.4). The strongest positive candidates are low beta (t +2.4) and 12-1 momentum (t +2.2); neither clears the bar.
4. **Momentum holds in most markets in both books**: 12-1 momentum is positive raw in 5 and beta-neutral in 5 of six markets, residual momentum in 6 and 6. Positive raw in all six: Residual momentum, Far above 52-week low.
5. **Tail direction is not priced the way the lottery literature expects** in our large caps: low skewness and low net tail lose in most markets, raw and beta-neutral.
6. **Costs sort the families**: the within-month signals (MAX, MIN, skewness, reversal, seasonality) cost 3–4% a year; volatility, beta, momentum and size cost 0–2%.

## 3. Common ground among signals: two blocks

![Correlation](../figures/fs13_corr.png)

Clustering the beta-neutral long/short returns (average correlation over the six markets, average linkage, cut at correlation 0.5) gives:

| Signals in the group | Size |
|---|---|
| Low MAX (1 day), Low MAX (5 days), Mild worst day (MIN), Mild worst 5 days, Narrow daily range, Low idiosyncratic vol, Low volatility (63d), Low volatility (252d), Low beta | 9 |
| Momentum 12-1, Near 52-week high, Far above 52-week low, Near 55-day high | 4 |
| Low net tail, Low skewness | 2 |
| Short-term reversal | 1 |
| Residual momentum | 1 |
| Same-month seasonality | 1 |
| Small size | 1 |


**The nineteen signals hold far fewer independent bets.** Everything that measures the *size* of price moves — MAX, MIN, the daily range, idiosyncratic volatility, volatility and beta — is one block. Momentum, 52-week high, 52-week low distance and the breakout are a second block. Residual momentum, reversal, seasonality, tail direction and size stand alone.

**Is the structure the same in every market?** Adjusted Rand index between each market's own clustering and the pooled one: US 1.00, EU 0.87, UK 0.53, DK 0.68, SCANDI 0.76, World 0.91 (1 = identical, 0 = random). The two-block structure is almost identical in the US, EU and World and looser in the UK and Scandinavia, where small groups and fewer names make correlations noisier.

## 4. Common ground among segments: do markets agree on what works?

Spearman rank correlation between markets of the 19 beta-neutral Sharpe ratios (average against the other five markets):

| Market | Average agreement with the other markets |
|---|---|
| US | 0.61 |
| EU | 0.60 |
| UK | 0.45 |
| DK | 0.47 |
| SCANDI | 0.29 |
| World | 0.69 |


The same test on the 153 JKP factors (2013–2025 Sharpe ratios):

| Segment | Average agreement with the other segments |
|---|---|
| US | 0.55 |
| UK | 0.59 |
| Denmark | 0.24 |
| World ex US | 0.65 |
| World | 0.69 |


**SCANDI is the odd one out.** In the price battery SCANDI (0.29) and UK (0.45) agree least; in JKP it is Denmark (0.24). With ~19 stocks in OMXC25, ~62 in SCANDI and a JKP Danish universe dominated by a few large names, factor returns there are driven by single companies. The US, EU/World ex US and World agree most, partly because they overlap. The median correlation of the same JKP factor across segments: US–World ex US 0.56, US–UK 0.43, US–Denmark 0.18; factor returns are mostly local, so a signal that works in several segments is genuine breadth, not one bet counted twice.

## 5. The published factors: 153 JKP factors since 2013

![JKP themes](../figures/fs13_jkp_themes.png)

Pooled over the four disjoint segments (US, UK, Denmark, World ex US), **19 of 153 factors** are discoveries under Benjamini–Hochberg at 5% and 14 clear the Harvey–Liu–Zhu bar of t > 3. The strongest twelve:

| Factor | Theme | Average return / yr | Sharpe | t | Positive in | Before 2013 (4-segment average) | BH |
|---|---|---|---|---|---|---|---|
| nfna_gr1a | Debt Issuance | +4.5% | 1.34 | +5.3 | 4 / 4 | +3.3% | ✓ |
| fnl_gr1a | Debt Issuance | +4.3% | 1.20 | +5.1 | 4 / 4 | +3.8% | ✓ |
| noa_at | Debt Issuance | +5.0% | 1.07 | +5.0 | 4 / 4 | +4.1% | ✓ |
| resff3_12_1 | Momentum | +5.3% | 1.06 | +4.2 | 4 / 4 | +7.9% | ✓ |
| seas_1_1na | Momentum | +8.7% | 1.02 | +4.2 | 4 / 4 | +3.9% | ✓ |
| rd_me | Size | +6.8% | 1.00 | +3.9 | 4 / 4 | +3.9% | ✓ |
| ret_9_1 | Momentum | +7.4% | 0.84 | +3.8 | 4 / 4 | +6.1% | ✓ |
| saleq_su | Profit Growth | +5.6% | 1.01 | +3.8 | 4 / 4 | +0.2% | ✓ |
| ret_6_1 | Momentum | +5.7% | 0.74 | +3.7 | 4 / 4 | +4.0% | ✓ |
| capx_gr1 | Investment | +4.2% | 0.87 | +3.3 | 4 / 4 | +3.2% | ✓ |
| niq_be_chg1 | Profit Growth | +4.4% | 0.93 | +3.2 | 4 / 4 | +4.1% | ✓ |
| ret_12_1 | Momentum | +7.3% | 0.83 | +3.1 | 4 / 4 | +8.1% | ✓ |


**Reading it.** The winners since 2013 come from three themes: **momentum** (12-1, 9-1, 6-1, residual momentum, 52-week high, seasonality at lag 1), **debt issuance** (firms that shrink net financing, debt or net operating assets beat those that raise them) and **profit growth** (sales and earnings surprises and changes). Value, investment and accruals, stars of the pre-2013 literature, weakened sharply in the US; short-term reversal fell from a Sharpe of 0.67 to 0.10 there.

## 6. Replication check: does our engine match the published factors?

![Replication](../figures/fs13_replication.png)

| Our signal | JKP factor | US | EU (proxy) | UK | DK | SCANDI (proxy) | World |
|---|---|---|---|---|---|---|---|
| Momentum 12-1 | ret_12_1 | 0.90 | 0.63 | 0.84 | 0.82 | 0.41 | 0.85 |
| Residual momentum | resff3_12_1 | 0.72 | 0.37 | 0.51 | 0.55 | 0.25 | 0.65 |
| Short-term reversal | ret_1_0 | 0.83 | 0.55 | 0.79 | 0.74 | 0.44 | 0.81 |
| Small size | market_equity | 0.59 | 0.13 | 0.55 | 0.34 | 0.03 | 0.55 |
| Low volatility (63d) | rvol_21d | 0.80 | 0.64 | 0.83 | 0.72 | 0.58 | 0.74 |
| Low idiosyncratic vol | ivol_capm_21d | 0.77 | 0.47 | 0.76 | 0.67 | 0.33 | 0.65 |
| Low beta | beta_60m | 0.92 | 0.73 | 0.84 | 0.59 | 0.70 | 0.86 |
| Low MAX (1 day) | rmax1_21d | 0.81 | 0.58 | 0.76 | 0.71 | 0.47 | 0.71 |
| Low MAX (5 days) | rmax5_21d | 0.82 | 0.56 | 0.76 | 0.74 | 0.48 | 0.72 |
| Low skewness | rskew_21d | 0.67 | 0.29 | 0.45 | 0.62 | 0.22 | 0.57 |
| Near 52-week high | prc_highprc_252d | 0.90 | 0.73 | 0.89 | 0.73 | 0.57 | 0.88 |
| Same-month seasonality | seas_1_1an | 0.41 | 0.22 | 0.50 | 0.31 | 0.17 | 0.39 |


In the US, where the universes are closest (our S&P 500 members vs JKP's capped value-weighted full market), **7 of 12 matched signals correlate 0.8 or more** with the published factor (Momentum 12-1, Short-term reversal, Low volatility (63d), Low beta, Low MAX (1 day), Low MAX (5 days), Near 52-week high). This closes the replication gap raised in FS00: the engine produces the known factors. The weaker matches have known reasons: our seasonality averages up to 13 years of same-month returns while JKP's `seas_1_1an` uses only last year's; our size sort is within the 500 largest (JKP spans micro caps). EU and Scandinavia are compared with World ex US, so their lower numbers measure the proxy, not the engine.

## 7. Where is the common ground?

| Theme | Our price data: t (markets > 0) | JKP: t (segments > 0) | JKP US Sharpe before 2013 → since | JKP factors that are BH discoveries | Verdict |
|---|---|---|---|---|---|
| Momentum | +1.5 (6/6) | +4.4 (4/4) | +0.28 → +0.42 | 6 / 8 | Common ground (positive everywhere, significant in JKP) |
| Low risk | +2.0 (6/6) | +0.2 (3/4) | +0.07 → +0.07 | 0 / 18 | Positive almost everywhere, not significant |
| Lottery & tails (size of tails) | +0.4 (3/6) | — | — | — | No common ground |
| Tail direction (skewness) | -2.8 (1/6) | — | — | — | Reliably negative |
| Short-term reversal | -2.4 (1/6) | -0.5 (2/4) | +0.67 → +0.10 | 0 / 6 | Reliably negative · faded in the US |
| Seasonality | -3.4 (1/6) | -0.5 (1/4) | +0.38 → -0.08 | 1 / 12 | Reliably negative · faded in the US |
| Size | -0.5 (2/6) | +1.1 (3/4) | +0.27 → -0.15 | 1 / 5 | No common ground |
| Breakout | +0.1 (3/6) | — | — | — | No common ground |
| Value | — | +1.0 (4/4) | +0.29 → +0.15 | 1 / 18 | Positive almost everywhere, not significant |
| Quality | — | +1.2 (3/4) | +0.19 → +0.46 | 0 / 17 | Positive almost everywhere, not significant |
| Profitability | — | +0.9 (3/4) | +0.29 → +0.31 | 0 / 11 | Positive almost everywhere, not significant |
| Profit growth | — | +2.5 (4/4) | +0.44 → +0.34 | 4 / 12 | Common ground (significant; JKP only) |
| Investment | — | +1.2 (4/4) | +0.42 → +0.12 | 1 / 22 | Positive almost everywhere, not significant · faded in the US |
| Debt issuance | — | +6.2 (4/4) | +1.07 → +0.43 | 4 / 7 | Common ground (significant; JKP only) |
| Accruals | — | -0.4 (3/4) | +0.76 → +0.03 | 1 / 6 | No common ground · faded in the US |
| Low leverage | — | +0.2 (2/4) | +0.01 → +0.10 | 0 / 11 | No common ground |


*Price t: beta-neutral composite of the theme's signals, average of 6 markets. JKP t: equal-weight theme portfolio, average of 4 disjoint segments, 2013–2025. "Common ground" = positive in every segment of every source that covers the theme, and pooled t > 2 in at least one source. "Faded in the US" = JKP US Sharpe above 0.3 before 2013 and below 0.15 since.*

**Common ground:** Momentum, Profit growth, Debt issuance. **Positive almost everywhere, not significant:** Low risk, Value, Quality, Profitability, Investment. **Works pooled, not everywhere:** none. **Reliably negative:** Tail direction (skewness), Short-term reversal, Seasonality. **Faded in the US:** Short-term reversal, Seasonality, Investment, Accruals.

**Momentum is the strongest theme across both sources**: positive in 6 of six of our markets and all 4 JKP segments; significant in JKP (t +4.4) but not in our large caps once short legs pay borrow fees (t +1.5). **Low risk** is positive in 6 of six of our markets after financing (t 2.0) but only 3 of 4 JKP segments (t 0.2); JKP's low-risk factors are value-weighted and not beta-neutral, so they carry the short-market drag that our beta-neutral books remove. **Debt issuance** (t 6.2) and **profit growth** (t 2.5) are the only themes positive in every segment with a significant pooled return, and both are fundamental themes to add first. Value, quality, profitability and investment were positive in most JKP segments but not significant since 2013.

## 8. What this means for the multifactor model

The battery gives a pre-selection that is transparent and grounded in more than one segment:

1. **Carry forward:** low beta (beta-neutral, financed) as the low-risk representative, and 12-1 momentum, residual momentum and the 52-week high from the momentum block; the other signals in each block are near-duplicates.
2. **Add from fundamentals next** (US stock level from Sharadar; JKP factor level elsewhere): debt issuance and profit growth first, then quality and value as diversifiers even though they were weak since 2013.
3. **Drop:** same-month seasonality, short-term reversal and tail direction (skewness, net tail) in large caps; the lottery/tail-size signals add nothing beyond low beta and volatility.
4. **Treat Denmark as a robustness market, not a selection market**: its signal ranking agrees least with the others.
5. The next factsheet applies the planned filters (net return, Sharpe, turnover per segment), rolling 3-year correlations and the dynamic weighting to this shortlist, walk-forward.

## 9. Caveats

- **Different construction.** Our books are equal-weighted, net, local currency (World in USD), large caps; JKP's are capped value-weighted, gross, USD, broad market. Agreement across the two is therefore stronger evidence than either alone, but numbers are not comparable one-to-one.
- **Proxies.** EU and Scandinavia have no JKP data here; World ex US stands in. World overlaps US, UK and EU in both batteries; the pooled tests use disjoint segments for JKP and report the effective number of markets for the price battery.
- **Periods.** Price battery Feb 2013 – Aug 2026; JKP Jan 2013 – Dec 2025. JKP's "before 2013" history starts in the 1920s for the US and in 1987 for the UK, Denmark and World ex US.
- **Multiple testing.** 38 price tests and 153 JKP factors are corrected with Benjamini–Hochberg; the earlier factsheets' fix ladders are not in this count (see the FS00 gap on a programme-level ledger).
- **Three directions are conventions** (MIN, range, 52-week low distance); see §1.
- **Costs.** 10 bp per side, a size-tiered borrow fee on every short leg and financing of net long cash (USD risk-free + 50 bp) are charged; market impact is not (FS00).

## 10. References

- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Hou, K., Xue, C. & Zhang, L. (2020). Replicating anomalies. *Review of Financial Studies* 33(5), 2019–2133.
- Harvey, C. R., Liu, Y. & Zhu, H. (2016). … and the cross-section of expected returns. *Review of Financial Studies* 29(1), 5–68.
- Benjamini, Y. & Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society B* 57(1), 289–300.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance* 71(1), 5–32.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics* 111(1), 1–25.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance* 48(1), 65–91.
- Blitz, D., Huij, J. & Martens, M. (2011). Residual momentum. *Journal of Empirical Finance* 18(3), 506–521.
- George, T. J. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance* 59(5), 2145–2176.
- Bali, T. G., Cakici, N. & Whitelaw, R. F. (2011). Maxing out. *Journal of Financial Economics* 99(2), 427–446.
- Ang, A., Hodrick, R. J., Xing, Y. & Zhang, X. (2006). The cross-section of volatility and expected returns. *Journal of Finance* 61(1), 259–299.
- Boyer, B., Mitton, T. & Vorkink, K. (2010). Expected idiosyncratic skewness. *Review of Financial Studies* 23(1), 169–202.
- Heston, S. L. & Sadka, R. (2008). Seasonality in the cross-section of stock returns. *Journal of Financial Economics* 87(2), 418–445.
- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns. *Journal of Finance* 45(3), 881–898.
- Banz, R. W. (1981). The relationship between return and market value of common stocks. *Journal of Financial Economics* 9(1), 3–18.
- Blitz, D. & van Vliet, P. (2007). The volatility effect. *Journal of Portfolio Management* 34(1), 102–113.

## 11. Reproduce

`code/battery.py` (price battery → `results/battery_price.json/.pkl`), `code/jkp_battery.py` (JKP battery → `results/battery_jkp_*.csv`), `code/financing.py` (financing charge for the beta-neutral books), `code/common_ground.py` (pooled tests, clusters, agreement, replication, themes, figures → `results/common_ground.json`), `code/build_fs13.py` (this factsheet). JKP monthly factor files come from Project2's `reporting/style_cache`.
