# FACTSHEET FS14 · The multifactor model

### From a battery of 25 books to one portfolio, step by step, as pre-registered

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS14.md`, written and saved before the first run (27 Sep 2026); no deviations |
| Building blocks | 19 beta-neutral price books per market (FS13), plus 6 US fundamental composites (FS13b); all net of trading costs, borrow fees and financing |
| Walk-forward | every month-end: filter → prune → weight, using only past data; out of sample Feb 2016 – Aug 2026 (127 months) |
| Filter | trailing 36 months: positive mean, probabilistic Sharpe ≥ 0.80, costs < 50% of the gross spread |
| Pruning | rank by trailing Sharpe, drop any book correlated above 0.70 with one already kept |
| Weighting | 11 rules: equal (EQ), risk parity (RP, primary), and mean/variance weights over 12/36/60 months with equal, linear or exponential decay |
| Benchmarks | all books equally weighted (ALL-EQ); the fixed FS13 shortlist (SHORT, chosen with hindsight); the equal-weight market |
| Primary test | RP minus ALL-EQ, 5-market average (World excluded as overlapping), Newey–West t > 2 and positive in both halves |

> **In one paragraph.** The selection process works in the direction it should but not strongly enough to pass its own bar. The pre-registered primary portfolio (risk parity over the books that survive the filter and the pruning) beats owning every book equally by **+2.2% a year** on the five-market average (t 1.4; +2.1% in 2016–19 and +2.3% in 2020–26; better in 4 of 5 markets). The bar was t > 2, so **the claim that the selection adds value is not established**. The mean/variance weighting rules do somewhat better than risk parity (best: W36-L, Sharpe 0.45 against 0.34), but none beats the fixed shortlist of low beta, momentum and the two US fundamentals (Sharpe 0.50), and that shortlist was picked with hindsight from the same data. The filter is strict: in a typical month 1–3 books are held and the portfolio sits in cash for 1–26 of 127 months, depending on the market. None of these market-neutral books comes close to the Sharpe ratio of simply owning the market (0.64–0.95) over the same years.

## Step 1 · The battery

Nineteen beta-neutral long/short price books in every market (FS13): each leg scaled to beta one, net of 10 bp per side, a size-tiered borrow fee on the short leg and financing of the net long cash. In the US the six fundamental composites of FS13b are added, for 25 candidates. Beta-neutral books are used so that the combination is a market-neutral overlay rather than a disguised market bet.

## Step 2 · Filter and Step 3 · Pruning

| Market | Candidates | Pass the filter (median per month) | Kept after pruning (median) | Months in cash (of 127) | Held in the last month |
|---|---|---|---|---|---|
| US | 25 | 2 | 2 | 11 | Profit growth (US), Far above 52-week low, Debt issuance (US), Accruals (US) |
| EU | 19 | 4 | 3 | 11 | Far above 52-week low, Residual momentum, Near 52-week high, Low volatility (252d) |
| UK | 19 | 4 | 3 | 8 | Low volatility (252d), Near 52-week high, Low beta, Residual momentum |
| DK | 19 | 6 | 3 | 18 | Near 55-day high, Mild worst 5 days, Near 52-week high, Low volatility (63d) |
| SCANDI | 19 | 4 | 3 | 1 | Low volatility (252d), Mild worst 5 days, Near 55-day high, Residual momentum, Near 52-week high |
| World | 19 | 1 | 1 | 26 | Far above 52-week low, Near 52-week high, Residual momentum |


![Selection](../figures/fs14_selection.png)

The books selected most often across markets: momentum 12-1 (27%), small size (26%), residual momentum (24%), low max (5 days) (21%), low idiosyncratic vol (20%). The selection moves: momentum and residual momentum dominate some years, low-risk books others, and in the US the fundamental composites (profit growth above all) are held most. The filter's probabilistic-Sharpe bar of 0.80 over 36 months is demanding for books with Sharpe ratios of 0.3–0.6, which is why the portfolio is often small or in cash, especially in World.

## Step 4 · Weighting

| Rule | Sharpe, 5-market average | 2016–19 / 2020–26 | Minus ALL-EQ / yr (t) | Minus SHORT / yr (t) |
|---|---|---|---|---|
| EQ | +0.31 | +0.61 / +0.24 | +2.1% (t +1.4) | -3.5% (t -1.8) |
| RP | +0.34 | +0.75 / +0.24 | +2.2% (t +1.4) | -3.4% (t -1.7) |
| W12-E | +0.43 | +1.05 / +0.26 | +3.3% (t +1.8) | -2.3% (t -1.2) |
| W12-L | +0.39 | +1.09 / +0.20 | +2.9% (t +1.6) | -2.7% (t -1.4) |
| W12-X | +0.39 | +1.11 / +0.19 | +2.9% (t +1.6) | -2.7% (t -1.4) |
| W36-E | +0.44 | +1.15 / +0.24 | +3.0% (t +1.8) | -2.6% (t -1.3) |
| W36-L | +0.45 | +1.14 / +0.26 | +3.2% (t +1.9) | -2.4% (t -1.3) |
| W36-X | +0.44 | +1.17 / +0.24 | +3.1% (t +1.8) | -2.5% (t -1.3) |
| W60-E | +0.39 | +1.11 / +0.18 | +2.6% (t +1.7) | -3.0% (t -1.5) |
| W60-L | +0.42 | +1.16 / +0.22 | +2.9% (t +1.8) | -2.7% (t -1.4) |
| W60-X | +0.42 | +1.16 / +0.22 | +2.9% (t +1.8) | -2.6% (t -1.4) |


![Variants](../figures/fs14_variants.png)

Weighting by recent mean over variance helps a little over equal or risk-parity weights, and the result hardly depends on the window (12, 36 or 60 months) or on the decay (equal, linear, exponential). That insensitivity is reassuring: no single tuning choice drives the result.

## Step 5 · Out of sample, market by market

| Market | RP (primary) Sharpe | W36-L Sharpe | ALL-EQ Sharpe | SHORT* Sharpe | Market Sharpe | RP at 10% vol: return / yr | RP at 10% vol: max drawdown |
|---|---|---|---|---|---|---|---|
| US | -0.08 | -0.03 | -0.49 | +0.29 | +0.95 | +1.5% | -23% |
| EU | +0.43 | +0.34 | +0.19 | +0.65 | +0.79 | +6.0% | -30% |
| UK | +0.22 | +0.54 | +0.08 | +0.63 | +0.69 | +4.8% | -29% |
| DK | +0.19 | +0.28 | +0.35 | +0.27 | +0.64 | +4.9% | -21% |
| SCANDI | +0.35 | +0.33 | -0.06 | -0.16 | +0.86 | +4.9% | -18% |
| World | +0.13 | +0.11 | -0.30 | +0.34 | +0.81 | +1.1% | -41% |
| **5-market average** | +0.34 | +0.45 | +0.03 | +0.50 | — | — | — |


*Net, monthly, Feb 2016 – Aug 2026. SHORT* = low beta and 12-1 momentum (plus debt issuance and profit growth in the US), fixed in advance but chosen from FS13 results that cover the whole period, so it has hindsight. 10% vol = scaled with its own trailing 12-month volatility, capped at 3×.*

![OOS](../figures/fs14_oos.png)

## Step 6 · Is it real?

- **Primary test:** RP − ALL-EQ = +2.2% a year, t 1.43, positive in both halves. **Not passed** (bar: t > 2 and both halves positive).
- **Deflated Sharpe ratio** of the best rule (W36-L, five-market average): 0.51 using the observed spread of the 78 FS14 trials (they are highly correlated variations of one idea) and 0.18 if the 78 trials were independent noise. Both are below the usual bar of 0.95.
- **Programme ledger:** FS14 adds 78 trials (now 409); none of them survives the programme-wide correction.

## Step 7 · Exploratory: the overlay next to the market (not pre-registered)

| Market | Market Sharpe | RP overlay (10% vol) Sharpe | Correlation | Market + overlay Sharpe |
|---|---|---|---|---|
| US | 0.95 | 0.14 | -0.19 | 0.89 |
| EU | 0.79 | 0.48 | -0.06 | 0.93 |
| UK | 0.69 | 0.39 | -0.04 | 0.75 |
| DK | 0.64 | 0.41 | -0.10 | 0.79 |
| SCANDI | 0.86 | 0.43 | -0.04 | 0.89 |
| World | 0.81 | 0.08 | +0.27 | 0.57 |


*Not part of the pre-registration; shown because a market-neutral overlay is meant to be held next to a market portfolio, not instead of it.* Added to the market, the overlay raises the Sharpe ratio in EU, UK, DK, SCANDI and lowers it in US, World.

## Step 8 · What this means

1. **A disciplined process did not beat a simple one here.** Filtering, pruning and weighting beat owning everything, by a margin that the data cannot yet separate from luck; they did not beat a fixed shortlist of two to four well-understood books.
2. **The shortlist's edge is partly hindsight.** It was chosen after looking at 2013–2026 results; the dynamic process had to learn as it went.
3. **Fewer, better-understood books.** For an implementation: low beta (beta-neutral) and one momentum signal in every market, profit growth and debt issuance in the US, sized as an overlay next to the market.
4. **What would change the verdict:** longer history (ART 1996–2013) to double the out-of-sample period, the fundamental themes outside the US, and a cost model with market impact.

## 9. Everything in one table

| Stage | What was tested | What we found | Carried forward |
|---|---|---|---|
| FS01–FS12 | 12 famous strategies × 6 markets, full factsheets | Only betting against beta has a long/short book that passes positively (UK) after borrow and financing; buying 52-week lows, the Turtle rules and seasonality reliably lose | Momentum and low-risk families |
| FS05 | 10,000 random portfolios | Monkeys beat the index where small beat big: a size bet, not skill | Equal-weight universe as the honest benchmark |
| FS00 | All strategies in one table + gap analysis | Six markets count as fewer than two independent tests; gaps in data, costs and validation | Borrow, financing, USD World, ledger (closed) |
| FS13 | 19 price signals × 6 markets + 153 JKP factors | No positive price signal survives the correction; momentum positive almost everywhere; debt issuance and profit growth are the published common ground | Low beta, momentum, debt issuance, profit growth |
| FS13b | 14 US fundamentals, stock level | Profit growth works on every test; debt issuance on the long side; value and investment lost since 2013 | Profit growth, debt issuance (US) |
| FS13c | All signals together (Fama-MacBeth) | 12-1 momentum is the only price signal with a marginal return; its cousins are redundant; low risk lowers risk, not return | One momentum signal |
| FS14 | Pre-registered dynamic selection and weighting | Selection beats owning all books (+2.2% a year, t 1.4) but fails the pre-registered bar; it trails the hindsight shortlist | See §8 |
| Ledger | 409 gated tests across FS01–FS14 | 10 positive and 13 negative survive Benjamini–Hochberg; no candidate reaches a deflated Sharpe of 0.95 | Honest headline claims |


## 10. Caveats

- Out of sample only since 2016 because the filter needs 36 months; 127 months is short for books with Sharpe ratios below 0.6.
- The candidate books themselves were designed before FS14 but on data that overlap the out-of-sample period; the walk-forward protects the selection, not the design of the signals.
- Weight changes between books cost 10 bp per unit of turnover; the books' own trading costs are inside their returns. Market impact is not modelled.
- EU and SCANDI overlap (Nordic blue chips), and World overlaps the US, UK and EU.

## 11. References

- Bailey, D. H. & López de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk* 15(2), 3–44.
- Bailey, D. H. & López de Prado, M. (2014). The deflated Sharpe ratio. *Journal of Portfolio Management* 40(5), 94–107.
- DeMiguel, V., Garlappi, L. & Uppal, R. (2009). Optimal versus naive diversification: how inefficient is the 1/N portfolio strategy? *Review of Financial Studies* 22(5), 1915–1953.
- Asness, C. S., Moskowitz, T. J. & Pedersen, L. H. (2013). Value and momentum everywhere. *Journal of Finance* 68(3), 929–985.
- Harvey, C. R., Liu, Y. & Zhu, H. (2016). … and the cross-section of expected returns. *Review of Financial Studies* 29(1), 5–68.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Moreira, A. & Muir, T. (2017). Volatility-managed portfolios. *Journal of Finance* 72(4), 1611–1644.

## 12. Reproduce

`planning/PREREG_FS14.md` (rules) → `code/fs14.py` (walk-forward → `results/fs14.json`, series in `results/fs14.pkl`) → `code/build_fs14.py`. The candidate books come from `code/battery.py` and `code/fund_battery.py`.
