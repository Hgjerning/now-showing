# FACTSHEET FS05 · Monkey portfolios

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

> **The claim.** Burton Malkiel (1973): a blindfolded monkey throwing darts at the stock pages could pick a portfolio that does as well as the experts. Arnott, Hsu, Kalesnik & Tindall (2013) found that random, and even 'upside-down', portfolios beat the cap-weighted US index over 1964–2012. **What we find:** the share of 10,000 monkeys that beat the index ranged from 16% to 86% across the six markets: US 16%, EU 71%, UK 85%, DK 85%, SCANDI 86%, World 72%. Measured by Sharpe ratio, the same or fewer monkeys win (US 3%, EU 64%, UK 64%, DK 85%, SCANDI 77%, World 57% beat the index's Sharpe). **What decides it (§10):** whether small beats big that year. The yearly share of winning monkeys moves with the gap between the equal-weight universe and the index (correlation 0.56 to 0.94). The average monkey *is* the equal-weight universe; the typical (median) monkey lags it by the cost of holding only 30 names. **Classification (§11):** a benchmark lesson, not a strategy: a random portfolio is an equal-weight portfolio, and equal weight is a size tilt.

## 1. Headline performance

| Universe | Stocks per monkey | Median monkey CAGR | 5th–95th percentile | Average monkey CAGR | Index CAGR | EW universe CAGR | Monkeys beating the index (return) | Beating on Sharpe | Median Sharpe monkey / index | Max DD median monkey / index |
|---|---|---|---|---|---|---|---|---|---|---|
| US | 30 | +13.7% | +11.2% to +16.5% | +13.8% | +15.3% | +14.7% | 16% | 3% | 0.90 / 1.07 | -25% / -24% |
| EU | 30 | +10.9% | +8.6% to +13.5% | +11.0% | +10.1% | +11.6% | 71% | 64% | 0.78 / 0.75 | -27% / -26% |
| UK | 30 | +10.1% | +7.7% to +12.6% | +10.2% | +8.5% | +10.4% | 85% | 64% | 0.74 / 0.71 | -30% / -27% |
| DK | 10 | +12.4% | +9.0% to +15.8% | +12.6% | +10.3% | +12.9% | 85% | 85% | 0.79 / 0.68 | -33% / -40% |
| SCANDI | 20 | +12.3% | +9.9% to +14.6% | +12.4% | +10.7% | +13.3% | 86% | 77% | 0.87 / 0.80 | -29% / -27% |
| World | 30 | +11.7% | +9.2% to +14.5% | +11.9% | +10.8% | +13.9% | 72% | 57% | 0.78 / 0.76 | -30% / -28% |

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

| Universe | Prices | Membership | Names eligible (median) | Currency |
|---|---|---|---|---|
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: top 500 by market cap each month-end (Sharadar filings × price, A06 method) | ~499 | USD |
| EU | Project1 yfinance cache, Adj Close (TR) | **Point-in-time**: union of 11 national blue-chip indices (CAC 40, DAX, AEX, IBEX 35, FTSE MIB, OMXS30, OMXC25, OMXH25, BEL 20, PSI-20, WIG20), quarterly Wikipedia snapshots 2012–2026; 83% of member-quarters priced | ~238 | local (EUR, SEK, DKK, PLN) |
| UK | Project1 cache, Close + pence dividends (Yahoo under-adjusts LSE ~100×) | **Point-in-time**: FTSE 100 + FTSE 250, quarterly snapshots; 75% priced | ~242 | GBP |
| DK | Project1 cache, Adj Close | **Point-in-time**: OMX Copenhagen 25, quarterly snapshots; 91% priced | ~19 | DKK |
| SCANDI | Project1 cache, Adj Close | **Point-in-time**: OMXC25 + OMXS30 + OMXH25 (Oslo has no snapshot history); 88% priced | ~62 | local (DKK, SEK, EUR) |
| World | US Sharadar + UK + EU above | **Point-in-time** union of the three; local-currency returns summed, not converted | ~963 | mixed |

*Membership comes from Project2's cache of dated Wikipedia index pages (the same parsing as `run_wiki_pit.py` / `run_eu_pit.py`), with a short list of verified ticker renames (e.g. NZYM-B → NSIS-B, WDH → DEMANT, DAI → MBG). A name is eligible from the day after the snapshot that lists it, once it has 60 days of prices. Member-quarters without a price are mostly delisted names that Yahoo no longer serves, so some survivorship remains; see §13.*

- **Data gap:** no market caps outside the US; the index is proxied by traded-value weights, which over-weight the most traded (not necessarily largest) stocks.

## 4. "Signal" creation

None: each January 10,000 monkeys draw their stocks uniformly at random from the names eligible at the end of December (seeded, reproducible).

## 5. Model build

Equal weight at formation, buy and hold for the calendar year; a name that stops trading earns zero after its last price. 20 bp round trip charged each January. Code: `code/monkey.py`, `code/build_monkey.py`.

## 6. Performance in detail

**Share of monkeys beating the index each year (equal-weight universe minus index in brackets)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | 59% (+2%) | 75% (+4%) | 99% (+12%) | 63% (+11%) | 79% (+6%) | 88% (+10%) |
| 2014 | 62% (+2%) | 19% (-2%) | 96% (+8%) | 7% (-2%) | 35% (+3%) | 92% (+8%) |
| 2015 | 32% (-2%) | 65% (+2%) | 100% (+16%) | 8% (-14%) | 55% (+0%) | 80% (+5%) |
| 2016 | 63% (+2%) | 52% (-5%) | 45% (-4%) | 97% (+9%) | 83% (-3%) | 59% (+1%) |
| 2017 | 30% (-1%) | 60% (+1%) | 96% (+10%) | 71% (+3%) | 77% (+3%) | 55% (+3%) |
| 2018 | 26% (-2%) | 65% (+2%) | 58% (+2%) | 83% (+4%) | 81% (+4%) | 64% (+2%) |
| 2019 | 37% (+1%) | 24% (-2%) | 83% (+6%) | 12% (-6%) | 71% (+4%) | 58% (+4%) |
| 2020 | 17% (-1%) | 15% (-1%) | 85% (+10%) | 55% (+2%) | 64% (+4%) | 40% (+6%) |
| 2021 | 51% (+2%) | 45% (+2%) | 36% (-1%) | 63% (+2%) | 32% (+1%) | 63% (+7%) |
| 2022 | 92% (+7%) | 74% (+5%) | 0% (-17%) | 4% (-9%) | 22% (-1%) | 48% (+1%) |
| 2023 | 11% (-10%) | 42% (+0%) | 60% (+0%) | 11% (-7%) | 7% (-3%) | 31% (-1%) |
| 2024 | 12% (-9%) | 68% (+2%) | 12% (-4%) | 96% (+7%) | 67% (-0%) | 37% (-1%) |
| 2025 | 20% (-4%) | 91% (+10%) | 12% (-11%) | 100% (+25%) | 97% (+13%) | 28% (-4%) |
| 2026 | 57% (+3%) | 30% (+1%) | 33% (-0%) | 70% (+5%) | 31% (+3%) | 43% (+2%) |

![Years](../figures/fs05_years.png)

## 7. Trading record

Each monkey trades once a year. The average of all monkeys equals the equal-weight universe held from January (differences come from mid-year index changes and costs). The median monkey lags the average (US -0.2%, EU -0.1%, UK -0.1%, DK -0.2%, SCANDI -0.1%, World -0.2% a year) because a concentrated portfolio compounds below its average return: the more volatile the stocks, the larger the gap.

## 8. Risk and attribution

Median monkey minus index, regressed on the equal-weight universe minus index (monthly, Newey-West t):

| Universe | Slope on EW − index | Alpha / yr | t | Correlation of EW − index with the small-minus-big size sort |
|---|---|---|---|---|
| US | 0.94 | -1.2% | -3.49 | +0.69 |
| EU | 0.80 | -0.7% | -1.24 | +0.71 |
| UK | 0.92 | -0.4% | -0.96 | +0.80 |
| DK | 1.00 | +0.1% | 0.19 | +0.61 |
| SCANDI | 0.70 | -0.4% | -0.43 | +0.57 |
| World | 0.74 | -1.5% | -3.56 | +0.52 |

The slope near 1 says the monkey is the equal-weight universe; what is left (the alpha) is mostly the concentration drag from holding few names.

## 9. Statistical verdict

- No hypothesis test is needed for the headline: the monkeys' expected return equals the equal-weight universe by construction. The question is only how equal weight compares with size weight in each market, and that is the size effect (FS07).
- The share beating the index is above 50% in 5 of 6 markets, which are the markets where the equal-weight universe beat the index over the period.

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

The monkey's neighbourhood is the equal-weight universe (identical in expectation) and the size sort: the equal-weight-minus-index spread correlates US +0.69, EU +0.71, UK +0.80, DK +0.61, SCANDI +0.57, World +0.52 with the small-minus-big size sort of the signal library. Everything the monkey "knows" is size.

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
