# FACTSHEET FS05 · Monkey portfolios

### Can a blindfolded monkey beat the index?

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

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

> **The claim.** Burton Malkiel (1973): a blindfolded monkey throwing darts at the stock pages could pick a portfolio that does as well as the experts. Arnott, Hsu, Kalesnik & Tindall (2013) found that random, and even 'upside-down', portfolios beat the cap-weighted US index over 1964–2012. **What we find:** the share of 10,000 monkeys that beat the index ranged from 3% to 83% across the six markets: US 3%, EU 57%, UK 76%, DK 83%, SCANDI 77%, World 48%. Measured by Sharpe ratio, the same or fewer monkeys win (US 0%, EU 44%, UK 59%, DK 86%, SCANDI 58%, World 30% beat the index's Sharpe). **What decides it (§10):** whether small beats big that year. The yearly share of winning monkeys moves with the gap between the equal-weight universe and the index (correlation 0.65 to 0.94). The average monkey *is* the equal-weight universe; the typical (median) monkey lags it by the cost of holding only 30 names. **Classification (§11):** a benchmark lesson, not a strategy: a random portfolio is an equal-weight portfolio, and equal weight is a size tilt.

## 1. Headline performance

| Universe | Stocks per monkey | Median monkey CAGR | 5th–95th percentile | Average monkey CAGR | Index CAGR | EW universe CAGR | Monkeys beating the index (return) | Beating on Sharpe | Median Sharpe monkey / index | Max DD median monkey / index |
|---|---|---|---|---|---|---|---|---|---|---|
| US | 30 | +12.1% | +9.8% to +14.4% | +12.2% | +14.9% | +13.0% | 3% | 0% | 0.81 / 1.05 | -27% / -24% |
| EU | 30 | +10.4% | +8.0% to +13.0% | +10.6% | +10.2% | +11.0% | 57% | 44% | 0.76 / 0.77 | -27% / -25% |
| UK | 30 | +8.9% | +6.3% to +11.8% | +9.1% | +7.8% | +9.4% | 76% | 59% | 0.67 / 0.65 | -31% / -28% |
| DK | 10 | +12.2% | +8.8% to +15.7% | +12.4% | +10.2% | +12.6% | 83% | 86% | 0.81 / 0.68 | -32% / -40% |
| SCANDI | 20 | +12.0% | +9.7% to +14.6% | +12.2% | +11.0% | +13.0% | 77% | 58% | 0.86 / 0.84 | -27% / -26% |
| World | 30 | +10.2% | +7.7% to +13.0% | +10.4% | +10.3% | +12.3% | 48% | 30% | 0.69 / 0.74 | -31% / -28% |

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
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: the S&P 500 members at each month-end (Sharadar add/remove history; corrected 2 Oct 2026) | ~503 | USD |
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
| 2013 | 71% (+2%) | 86% (+5%) | 97% (+10%) | 51% (+7%) | 92% (+8%) | 91% (+10%) |
| 2014 | 50% (+1%) | 11% (-6%) | 95% (+7%) | 14% (-2%) | 19% (+0%) | 81% (+6%) |
| 2015 | 22% (-4%) | 44% (-0%) | 100% (+14%) | 11% (-13%) | 51% (-0%) | 67% (+2%) |
| 2016 | 65% (+4%) | 48% (-3%) | 43% (-4%) | 96% (+9%) | 90% (-1%) | 54% (+1%) |
| 2017 | 23% (-4%) | 63% (+1%) | 92% (+10%) | 77% (+4%) | 78% (+3%) | 57% (+3%) |
| 2018 | 24% (-3%) | 47% (-0%) | 50% (+2%) | 84% (+4%) | 61% (+1%) | 51% (+1%) |
| 2019 | 26% (-1%) | 18% (-4%) | 73% (+5%) | 13% (-7%) | 50% (+1%) | 47% (+2%) |
| 2020 | 3% (-5%) | 18% (-2%) | 78% (+9%) | 48% (-2%) | 50% (+2%) | 23% (+2%) |
| 2021 | 50% (+2%) | 41% (+1%) | 39% (-0%) | 54% (-0%) | 24% (-0%) | 59% (+6%) |
| 2022 | 94% (+7%) | 71% (+5%) | 0% (-16%) | 6% (-8%) | 23% (-2%) | 46% (+0%) |
| 2023 | 2% (-13%) | 42% (+1%) | 54% (-0%) | 19% (-4%) | 9% (-2%) | 20% (-3%) |
| 2024 | 1% (-12%) | 68% (+3%) | 19% (-3%) | 95% (+7%) | 70% (-0%) | 27% (-2%) |
| 2025 | 15% (-6%) | 92% (+10%) | 13% (-10%) | 100% (+26%) | 97% (+14%) | 27% (-5%) |
| 2026 | 55% (+3%) | 29% (+1%) | 30% (-0%) | 69% (+5%) | 26% (+2%) | 39% (+1%) |

![Years](../figures/fs05_years.png)

## 7. Trading record

Each monkey trades once a year. The average of all monkeys equals the equal-weight universe held from January (differences come from mid-year index changes and costs). The median monkey lags the average (US -0.1%, EU -0.2%, UK -0.2%, DK -0.2%, SCANDI -0.1%, World -0.2% a year) because a concentrated portfolio compounds below its average return: the more volatile the stocks, the larger the gap.

## 8. Risk and attribution

Median monkey minus index, regressed on the equal-weight universe minus index (monthly, Newey-West t):

| Universe | Slope on EW − index | Alpha / yr | t | Correlation of EW − index with the small-minus-big size sort |
|---|---|---|---|---|
| US | 0.93 | -1.0% | -3.01 | +0.79 |
| EU | 0.82 | -0.7% | -1.59 | +0.66 |
| UK | 0.88 | -0.6% | -1.45 | +0.80 |
| DK | 0.99 | -0.5% | -0.88 | +0.58 |
| SCANDI | 0.77 | -0.6% | -0.71 | +0.58 |
| World | 0.71 | -1.6% | -3.73 | +0.68 |

The slope near 1 says the monkey is the equal-weight universe; what is left (the alpha) is mostly the concentration drag from holding few names.

## 9. Statistical verdict

- No hypothesis test is needed for the headline: the monkeys' expected return equals the equal-weight universe by construction. The question is only how equal weight compares with size weight in each market, and that is the size effect (FS07).
- The share beating the index is above 50% in 4 of 6 markets, which are the markets where the equal-weight universe beat the index over the period.

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

The monkey's neighbourhood is the equal-weight universe (identical in expectation) and the size sort: the equal-weight-minus-index spread correlates US +0.79, EU +0.66, UK +0.80, DK +0.58, SCANDI +0.58, World +0.68 with the small-minus-big size sort of the signal library. Everything the monkey "knows" is size.

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
