# FACTSHEET FS17 · Fundamentals outside the US

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

> **In one paragraph.** **Yes, clearly, in both periods.** The fundamental pair earns an alpha of **+6.2% a year (t 4.7)** on top of low beta and momentum across the UK, Denmark and the EU proxy in 2013–2025, and **+18.7% (t 7.0)** across Europe and the UK in 1999–2013. The pre-registered bar (t > 2 in both periods) is **passed**, and the primary test also survives the programme-wide correction across 624 trials. The fundamental pair is only weakly correlated with the price shortlist (0.2–0.4), so adding them lifts the combined Sharpe ratio in every market. Two warnings keep this from being an investable result: the factor returns are **gross of trading costs**, and the ART spreads (1999–2013) are decile spreads whose size (Sharpe ratios near 2) is too large to take at face value.

## 1. 2013–2025 (JKP)

| Market | Pair alpha on the shortlist (t) | R² | Correlation with the shortlist | Shortlist Sharpe | Shortlist + pair Sharpe | Difference t |
|---|---|---|---|---|---|---|
| UK | +7.4% (t +2.6) | 0.17 | +0.34 | 1.08 | 1.45 | +0.1 |
| Denmark | +7.4% (t +2.6) | 0.07 | +0.24 | 0.15 | 0.65 | +2.0 |
| EU (World ex US) | +4.1% (t +3.3) | 0.22 | +0.36 | 0.86 | 1.19 | -1.1 |
| World | +2.4% (t +1.9) | 0.38 | +0.43 | 0.65 | 0.87 | -0.8 |
| US | +1.8% (t +1.1) | 0.28 | +0.30 | 0.38 | 0.50 | -0.2 |


| Theme | Non-US average: alpha (t) | UK t | Denmark t | EU (World ex US) t | World t | US t |
|---|---|---|---|---|---|---|
| Profit growth | +3.4% (t +1.5) | +0.8 | +0.8 | +2.2 | +1.0 | +0.5 |
| Issuance | +9.1% (t +6.0) | +4.3 | +3.4 | +2.7 | +2.7 | +1.4 |
| Value | +6.4% (t +2.4) | +3.4 | +0.0 | +2.1 | +1.9 | +0.5 |
| Profitability | +0.8% (t +0.3) | +1.0 | -0.9 | +1.7 | +1.0 | +0.7 |


*Alpha: annualised intercept, both sides scaled to 10% volatility. Non-US average: UK, Denmark and the EU proxy. The US row is for reference; it is outside the pre-registered test.*

**Issuance (firms that shrink their net financing) carries most of it** after 2013; profit growth adds a little, value helps in the UK, profitability adds nothing.

## 2. 1999–2013 (ART)

| Market | Pair alpha on the shortlist (t) | R² | Correlation with the shortlist | Shortlist Sharpe | Shortlist + pair Sharpe | Difference t |
|---|---|---|---|---|---|---|
| Europe | +20.9% (t +7.1) | 0.20 | +0.34 | 0.83 | 1.99 | +4.6 |
| UK | +17.3% (t +6.4) | 0.10 | +0.23 | 0.99 | 1.92 | +2.3 |
| America | +11.2% (t +4.6) | 0.10 | +0.29 | 0.52 | 1.22 | +3.1 |


| Theme | Non-US average: alpha (t) | Europe t | UK t | America t |
|---|---|---|---|---|
| Profit growth | +23.0% (t +6.2) | +6.9 | +4.7 | +3.7 |
| Issuance | +14.3% (t +4.3) | +3.9 | +4.1 | +3.3 |
| Value | +11.4% (t +4.0) | +4.0 | +2.9 | +4.2 |
| Profitability | +15.8% (t +4.2) | +4.3 | +3.6 | +2.8 |


*Non-US average: Europe and the UK. America for reference.*

Before 2013 every fundamental theme added to the price shortlist, analyst revisions most of all. Their weakening after 2013 matches the decay JKP and McLean & Pontiff (2016) describe.

## 3. What this closes and what it does not

- **Closed at factor level:** the fundamental themes outside the US carry information that low beta and momentum do not, in two independent periods and data sources. The multifactor model should include issuance and profit growth in every market, not only the US.
- **Not closed at stock level:** we still cannot build these signals stock by stock outside the US with filing dates, so we cannot measure their net return after costs and capacity (FS16) in our own universes. Project2's `pit_fundamentals` snapshots, captured weekly since September 2026, will become a usable point-in-time history over the next one to two years; a licensed global fundamentals feed would close it now.

## 4. Caveats

- JKP factors: capped value-weighted, gross, USD; our shortlist: equal-weighted, net, local currency.
- ART spreads: gross decile spreads from the ART segment universes, compounded from weekly returns; costs and the stock universe differ from our books, and their magnitude is implausibly high for a tradable strategy.
- The EU is proxied by World ex US for 2013–2025, which also contains Japan, Canada and Australia.
- FS17 adds 58 trials to the ledger (now 624).

## 5. References

- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance* 78(5), 2465–2518.
- Pontiff, J. & Woodgate, A. (2008). Share issuance and cross-sectional returns. *Journal of Finance* 63(2), 921–945.
- Chan, L. K. C., Jegadeesh, N. & Lakonishok, J. (1996). Momentum strategies. *Journal of Finance* 51(5), 1681–1713.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance* 71(1), 5–32.
- Asness, C. S., Frazzini, A. & Pedersen, L. H. (2019). Quality minus junk. *Review of Accounting Studies* 24(1), 34–112.

## 6. Reproduce

`planning/PREREG_FS17.md` → `code/fs17.py` (→ `results/fs17.json`) → `code/build_fs17.py`. JKP files from Project2 `reporting/style_cache`; ART spreads from Project1 `art_factor_spreads_monthly.csv`.
