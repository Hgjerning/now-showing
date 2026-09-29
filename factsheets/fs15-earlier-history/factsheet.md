# FACTSHEET FS15 · The earlier history

### Do the conclusions hold in 1998–2013, with two bear markets they never saw?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · ART data January 1998 – March 2013*

| Key facts | |
|---|---|
| Pre-registration | `planning/PREREG_FS15.md`, written and saved before any 1998–2013 return was computed; no deviations |
| Data | ART research database extract (Project2): daily total-return indices and traded value, as reported, including stocks that later delisted |
| Markets | US, EU (EU member states excl. UK, Poland, Greece), UK, Denmark; World = US + UK + EU in USD; no Scandinavia (Finland not identifiable in the extract) |
| Universes | top 494 US, 344 UK, 239 EU, 25 DK stocks by 63-day traded value each month (median eligible names); a liquidity universe, not an index |
| Engine | identical to FS13/FS13c/FS14: same 19 signals and directions, costs, borrow fees, financing, filter, pruning and weighting rules |
| Periods | signals Jan 1999 – Feb 2013; the FS14 walk-forward holds portfolios from Feb 2002 (36 months of history needed) |

> **In one paragraph.** The earlier period mostly agrees with the later one, and where it disagrees it is informative. **Low risk is confirmed**: beta-neutral low beta and low volatility earn t 2.2 and 2.3 across the four markets, positive in all four and in both halves. **Momentum is consistent but weaker** (12-1: t 1.0; flat through the 2008 crash, then hit hard in the spring 2009 rebound), and in the joint regression it again adds return (t 2.2, confirming FS13c). **Tail direction is confirmed as a loser** (low skewness t -5.1). **Seasonality reverses**: it paid before 2013 (joint slope t 4.3) and failed after, the pattern of a published anomaly that faded. The **FS14 dynamic selection fails again**: +0.6% a year over owning every book (t 0.2), positive before 2007 and negative after. The strongest result is the **fixed shortlist of low beta and 12-1 momentum**, chosen from 2013–2026 results and therefore genuinely out of sample here: Sharpe 0.81, +9.1% a year over owning every book (t 2.6), positive in all four markets, with a correlation of +0.03 to the market. It does not survive the programme-wide correction over 566 trials.

![Periods](../figures/fs15_periods.png)

## 1. The price battery, 1999–2013

| Signal | 2013–26 beta-neutral t | 1999–2013 beta-neutral, net / yr (t) | Markets positive | Sharpe 1999–2005 / 2006–13 | 1999–2013 raw L/S t | Verdict |
|---|---|---|---|---|---|---|
| Low volatility (252d) | +1.1 | +15.9% (t +2.3) | 4 / 4 | +0.65 / +0.88 | +0.9 | confirmed |
| Low beta | +2.4 | +19.5% (t +2.2) | 4 / 4 | +0.81 / +0.67 | +0.9 | confirmed |
| Small size | +0.4 (weak) | +6.1% (t +1.6) | 4 / 4 | +0.79 / +0.32 | +1.6 | consistent |
| Low MAX (5 days) | +0.1 (weak) | +8.6% (t +1.6) | 4 / 4 | +0.47 / +0.60 | +0.8 | consistent |
| Low volatility (63d) | +1.0 (weak) | +10.0% (t +1.6) | 4 / 4 | +0.42 / +0.58 | +0.7 | consistent |
| Residual momentum | +1.2 | +5.8% (t +1.4) | 4 / 4 | +0.80 / +0.21 | +1.5 | consistent |
| Mild worst 5 days | +0.1 (weak) | +6.8% (t +1.2) | 4 / 4 | +0.27 / +0.54 | +1.0 | consistent |
| Low idiosyncratic vol | +0.4 (weak) | +5.2% (t +1.2) | 4 / 4 | +0.22 / +0.66 | +0.9 | consistent |
| Low MAX (1 day) | -0.2 (weak) | +5.7% (t +1.1) | 4 / 4 | +0.33 / +0.39 | +0.4 | reversed |
| Narrow daily range | +0.2 (weak) | +5.2% (t +1.0) | 4 / 4 | +0.18 / +0.46 | +0.6 | consistent |
| Momentum 12-1 | +2.0 | +5.9% (t +1.0) | 4 / 4 | +0.23 / +0.34 | +1.0 | consistent |
| Mild worst day (MIN) | -0.2 (weak) | +3.6% (t +0.7) | 3 / 4 | +0.11 / +0.35 | +0.7 | reversed |
| Near 52-week high | +0.8 (weak) | +3.1% (t +0.5) | 3 / 4 | -0.01 / +0.34 | +0.8 | consistent |
| Same-month seasonality | -3.4 | +1.0% (t +0.4) | 2 / 4 | -0.15 / +0.44 | +0.4 | reversed |
| Near 55-day high | -0.1 (weak) | -2.7% (t -0.5) | 1 / 4 | -0.31 / +0.04 | +0.3 | consistent |
| Far above 52-week low | +0.6 (weak) | -7.7% (t -1.4) | 0 / 4 | -0.65 / -0.11 | +0.1 | reversed |
| Short-term reversal | -1.9 | -6.7% (t -1.5) | 0 / 4 | -0.24 / -0.80 | -2.6 | consistent |
| Low net tail | -2.1 | -7.6% (t -2.7) | 0 / 4 | -0.62 / -1.12 | -2.9 | confirmed |
| Low skewness | -2.8 | -10.8% (t -5.1) | 0 / 4 | -1.58 / -1.48 | -4.2 | confirmed |


*Verdict as pre-registered: confirmed = same sign as 2013–26 and |t| > 2 in 1999–2013; consistent = same sign, |t| ≤ 2; reversed = opposite sign. "(weak)" marks a 2013–26 result with |t| < 1, which barely had a sign to confirm. Averages over US, EU, UK and DK; World is left out because it overlaps.*

**Confirmed:** Low net tail, Low skewness, Low volatility (252d), Low beta. **Reversed:** Low MAX (1 day), Mild worst day (MIN), Same-month seasonality, Far above 52-week low. Everything else keeps its sign with a t below 2.

## 2. All signals together (Fama-MacBeth), 1999–2013

| Signal | 2013–26 joint slope t | 1999–2013 joint slope t | Markets positive | Verdict |
|---|---|---|---|---|
| Low beta | -0.9 | +0.2 | 1 / 3 | reversed |
| Low volatility (252d) | -1.2 | +1.2 | 3 / 3 | reversed |
| Low MAX (1 day) | +0.7 | +3.2 | 3 / 3 | confirmed |
| Momentum 12-1 | +2.7 | +2.2 | 3 / 3 | confirmed |
| Residual momentum | -0.4 | +0.4 | 2 / 3 | reversed |
| Near 52-week high | +0.2 | -1.7 | 1 / 3 | reversed |
| Short-term reversal | -0.4 | +1.2 | 3 / 3 | reversed |
| Same-month seasonality | -0.6 | +4.3 | 3 / 3 | reversed |
| Low skewness | +0.7 | -3.8 | 0 / 3 | reversed |
| Small size | +1.4 | +3.4 | 3 / 3 | confirmed |


12-1 momentum keeps a positive joint slope in both periods, the one price signal that does. The earlier period also rewards signals that are weak or negative after 2013: seasonality, low MAX and small size.

## 3. The FS14 procedure, 1999–2013

| Market | RP (primary) | W12-X | All books equal | Fixed shortlist | Market | Books held (median) | Months in cash |
|---|---|---|---|---|---|---|---|
| US | -0.01 | +0.20 | -0.00 | +0.27 | +0.37 | 2 | 17 |
| EU | +0.22 | +0.25 | +0.36 | +0.67 | +0.27 | 3 | 12 |
| UK | +0.67 | +0.93 | +0.69 | +0.75 | +0.52 | 3 | 16 |
| DK | +0.32 | +0.71 | +0.69 | +0.93 | +0.66 | 3 | 7 |
| World | +0.17 | +0.42 | +0.40 | +0.74 | +0.43 | 2 | 19 |
| **4-market average** | +0.46 | +0.79 | +0.54 | +0.81 | +0.48 | — | — |


*Sharpe ratios, net, Feb 2002 – Mar 2013. Fixed shortlist = low beta and 12-1 momentum, beta-neutral, equal weights.*

![FS14 on 1999–2013](../figures/fs15_fs14.png)

|  | 2016–2026 (FS14) | 2002–2013 (FS15) |
|---|---|---|
| Primary: RP minus ALL-EQ | +2.2% (t +1.4) | +0.6% (t +0.2) |
| Best weighting rule, Sharpe | 0.45 | 0.79 (W12-X) |
| RP, Sharpe | 0.34 | 0.46 |
| All books equal, Sharpe | 0.03 | 0.54 |
| Fixed shortlist, Sharpe | 0.50 (hindsight) | 0.81 (out of sample) |


**Primary test:** RP − ALL-EQ = +0.6% a year, t 0.25 (+5.3% up to 2007-09, -4.3% after): **not passed**, for the second time.

**The shortlist:** +9.1% a year over owning every book (t 2.62), positive in 4 of 4 markets and in both halves (+12.9% / +5.1%). Because the shortlist was chosen from 2013–2026 results, this is a clean out-of-sample test of that choice.

## 4. Bear markets

| Book (4-market average) | Dot-com bust (Apr 2000 – Sep 2002) | Financial crisis (Nov 2007 – Feb 2009) | Momentum crash (Mar – May 2009) | Euro crisis (May – Sep 2011) |
|---|---|---|---|---|
| Market (equal weight) | -42% | -56% | +34% | -23% |
| Low beta, beta-neutral | +124% | -29% | -21% | +11% |
| 12-1 momentum, beta-neutral | +1% | +2% | -42% | +4% |
| Shortlist (low beta + momentum) | +60% | -14% | -32% | +8% |
| Low skewness, beta-neutral | -31% | -5% | +1% | -7% |


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
- **Multiple testing.** FS15 adds 157 trials to the ledger (now 566).

## 7. References

- Daniel, K. & Moskowitz, T. J. (2016). Momentum crashes. *Journal of Financial Economics* 122(2), 221–247.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance* 71(1), 5–32.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics* 111(1), 1–25.
- Heston, S. L. & Sadka, R. (2008). Seasonality in the cross-section of stock returns. *Journal of Financial Economics* 87(2), 418–445.
- Asness, C. S., Moskowitz, T. J. & Pedersen, L. H. (2013). Value and momentum everywhere. *Journal of Finance* 68(3), 929–985.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.

## 8. Reproduce

`planning/PREREG_FS15.md` → `code/data.py` (`load_art`, universes) → `code/signals.py`, `signals2.py` (regions `US_A`, `EU_A`, `UK_A`, `DK_A`, `WD_A`) → `code/art_run.py` (battery, Fama-MacBeth, FS14 procedure → `results/art_*.json`) → `code/build_fs15.py`. The ART extract is private and not published.
