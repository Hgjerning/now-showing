# FACTSHEET FS01 · The Turtle Traders

### Richard Dennis's 1983 trading rules, applied stock by stock to six equity universes

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 25 September 2026*

> **What changed on 2 October 2026.** Two corrections, both to the universe of stocks, and every number below is re-run on them.
> (1) **US:** the universe is now the actual S&P 500 members at each month-end. Until now it was the 500 largest of every
> company that was *ever* in the index 2012–2026, which includes later winners before they joined.
> (2) **UK and EU:** the price panels now include the index members that stopped trading (UK coverage of members 71% → 92%,
> EU 81% → 89%); before, most of them had no prices. SCANDI stays as registered (OMXC25 + OMXS30 + OMXH25).
> Registered verdicts are unchanged; where a corrected number crosses a gate, the text says so.
> Comparison and method: `FACTSHEETS_RERUN_2026-10-02.md`.

> **US, 1999–2012 (pre-registered second period, run 2 October 2026).** The same rules on Sharadar's point-in-time S&P
> 500 with delisted stocks, 1999–2012, a period this factsheet was not built on. L/S net: t -5.00 (2013–2026: -3.96),
> confirmed. Long-only alpha vs the equal-weight universe: -10.7% a year, t -3.61 (2013–2026: -1.38), confirmed.
> Negative in both halves (1999–2005 and 2006–2012): the most robust result in the whole series, and it is a loss.
> Registered verdicts are unchanged. Pre-registration, method and every result: `PREREG_US_1999_2012.md`.



<div class="kf" markdown="0">
<div><b>Strategy</b>Donchian channel breakout, pyramiding, 2N stops</div>
<div><b>Origin</b>Dennis & Eckhardt, 1983; rules published by Faith (2003)</div>
<div><b>Asset class</b>Single stocks (the Turtles traded futures)</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World</div>
<div><b>Backtest</b>Jan 2013 – Sep 2026, daily, net of costs</div>
<div><b>Books</b>Long/short (headline) and long-only</div>
<div><b>Rebalance</b>Event driven, next-day close fills</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **Verdict in one paragraph.** Dennis's students reportedly made more than $100 million with these rules on 1980s futures (Covel 2007). On single stocks, 2013–2026, the long/short version **lost money in all six universes** (Sharpe -0.91 to -0.17). Nearly all of the loss is the short side: stocks that break to a new low tend to bounce, and a rising market punishes every short. The long-only version made money everywhere, but **had a lower Sharpe than simply owning the equal-weight universe in all six**; its alpha against the universe is between -5.3% and +3.4% a year, and none reaches the 2.87 gate. The trade profile is textbook trend following, about 23% winners with winners 2.8× the size of losers. On stocks, that is not enough to pay for the whipsaws. **What goes wrong (§10):** costs from oversized units, a short book in a bull market, a 2N stop tighter than daily noise and, at the root, no trend in single stocks to follow. Fixing what can be fixed gives a long-only, half-beta book that still trails the equal-weight universe's Sharpe in the 2020–26 holdout (0.50 vs 0.70). **Classification (§11):** a futures trend strategy mis-applied to stocks. **360° view (§12):** the cross-sectional breakout does carry beta-adjusted information, but it is a noisy subset of the 52-week-high and momentum effects.

## 1. Headline performance

| Universe | L/S CAGR | L/S Sharpe | L/S max DD | Long-only CAGR | LO Sharpe | LO max DD | EW universe CAGR | EW Sharpe | EW max DD |
|---|---|---|---|---|---|---|---|---|---|
| US | -16.1% | -0.91 | -92% | +3.3% | 0.32 | -29% | +13.1% | 0.89 | -40% |
| EU | -9.5% | -0.49 | -80% | +7.3% | 0.55 | -37% | +10.8% | 0.80 | -37% |
| UK | -5.3% | -0.17 | -68% | +7.5% | 0.60 | -38% | +9.4% | 0.72 | -41% |
| DK | -6.1% | -0.35 | -68% | +1.0% | 0.13 | -38% | +12.8% | 0.87 | -35% |
| SCANDI | -14.0% | -0.88 | -89% | +2.0% | 0.23 | -36% | +12.9% | 0.93 | -34% |
| World | -15.7% | -0.75 | -93% | +4.0% | 0.36 | -39% | +12.0% | 0.82 | -41% |

*Daily returns, local currency (World in USD), net of 10 bp per side and 50 bp/yr short borrow; no interest on cash; rf = 0. CAGR, maximum drawdown: Project1 `InvestmentLibrary.reporting.generate_standard_report`. Sharpe on monthly returns. The benchmark is the equal-weight universe rebalanced daily (same names, same data).*

![Growth of 1](../figures/fs01_fig1_growth.png)

## 2. Strategy description

The Turtles were 23 novices recruited through a newspaper advert by Richard Dennis and William Eckhardt in 1983-84 to settle a bet: can trading be taught? They were given one mechanical rule set and traded Dennis's money in about 20 liquid futures markets. The rules were kept private until Curtis Faith published them in 2003 ("The Original Turtle Trading Rules"); Faith (2007) and Covel (2007) tell the story. The core is Richard Donchian's channel breakout (Donchian 1960): buy a new N-day high, sell a new N-day low.

| Rule | Original Turtle rule (Faith 2003) | This factsheet |
|---|---|---|
| Volatility unit **N** | 20-day exponential average of the true range | Same, close-to-close true range \|ΔP\| (Sharadar has no high/low) |
| Position unit | 1% of equity per 1 N move | **0.1%** of equity per N (see §5) |
| System 1 | Enter on a 20-day breakout, exit on a 10-day opposite breakout. Skip the signal if the previous 20-day breakout would have been a winner; take the 55-day breakout regardless (failsafe) | Same, including the skip filter, tracked on hypothetical trades |
| System 2 | Enter on a 55-day breakout, exit on a 20-day opposite breakout | Same |
| Stop | 2 N from the latest entry; all units' stops move up with each add | Same |
| Pyramiding | Add 1 unit every ½ N in the trade's favour, maximum 4 units per market | Same |
| Portfolio limit | 12 units per direction (fewer for correlated markets) | Gross cap: 100% long and 100% short of equity per system |
| Capital split | Traders ran both systems | 50% System 1, 50% System 2 |
| Direction | Long and short | Long/short headline; long-only variant; also the index version |

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

Window: signals from January 2012, performance from 2 January 2013 (a year of history needed for eligibility) to 24/25 September 2026. Eligibility: US, member of the S&P 500 at the previous month-end; others, at least 252 days of price history. Cleaning follows Project2's rules: the five series Project2 verified as corrupt (DIA.MC, ATO.PA, ZEG.L, SPM.MI, VPLAY-B.ST) are dropped, and any daily move beyond ±100% is set to missing unless it was verified as real (ABVX.PA, MRNA, ECHO, GME). That removed 12 US and 2 European daily prints.

## 4. Signal ("factor") creation

For stock *i* on day *t*, with *P* the total-return index:

- N<sub>t</sub> = (19·N<sub>t−1</sub> + \|P<sub>t</sub> − P<sub>t−1</sub>\|) / 20
- Long entry when P<sub>t</sub> > max(P<sub>t−L</sub> … P<sub>t−1</sub>); short entry when P<sub>t</sub> < min(…); L = 20 (System 1) or 55 (System 2)
- Exit long when P<sub>t</sub> < min of the last X closes (X = 10 or 20), or P<sub>t</sub> ≤ stop; mirror for shorts
- Add a unit when P<sub>t</sub> ≥ last entry + ½ N; stop = last entry − 2 N
- Unit size in shares = 0.001 × equity / N<sub>t</sub>, so a 1 N move in one unit costs 0.1% of equity

The signal is a time-series rule per stock, not a cross-sectional rank. There is no parameter fitting: every number is the 1983 rule.

## 5. Model build (portfolio construction and simulation)

- **Event-driven, close-only simulator** (`code/turtle.py`). Signals on the close of day *t* are filled on the close of day *t+1*, so there is no look-ahead. Positions are held in shares and marked to market daily.
- **Why 0.1% and not 1%.** Close-to-close N is about 1% of a large-cap share price, so a 1% unit would be roughly 100% of equity in one name and the original 12-unit limit 1,200% gross. At 0.1% one unit is about 10% of equity, four units at most about 40%, and the gross cap keeps the book near fully invested.
- **Oversubscription.** A 500-stock universe produces dozens of breakouts on busy days. New units are filled in order of breakout strength (distance past the channel in N) until the gross cap is reached. Adds to open trades go first.
- **Costs.** 10 bp per side on traded notional (commission plus half-spread for large caps), 50 bp a year on short notional, no interest earned on cash (conservative: 2022–26 rates were 4–5%).
- **Delistings.** A position with no price for five trading days is closed at the last price (matters for US point-in-time data).
- **Index version** ("futures-style"): the same System 2 rules applied to the equal-weight universe index as one market, the closest analogue to what the Turtles actually traded; 0.25% per unit so four units ≈ fully invested, 100% cap.

## 6. Performance in detail

**US (S&P 500 members, point-in-time)**, median 502 names; L/S book averages 97% long, 95% short, 16 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -16.1% | 22.9% | -0.91 [-1.47, -0.43] | -0.93 | -92% | -0.17 | 35% | 3.6% | -0.38 | -10.9% (-2.4) |
| System 1 only | -15.7% | 24.4% | -0.82 [-1.45, -0.31] | -0.87 | -93% | -0.17 | 37% | 3.7% | -0.21 | -12.4% (-2.5) |
| System 2 only | -17.3% | 25.7% | -0.81 [-1.27, -0.38] | -0.90 | -94% | -0.19 | 41% | 4.0% | -0.56 | -9.5% (-2.0) |
| Turtle long-only | +3.3% | 15.8% | 0.32 [-0.06, 0.75] | 0.28 | -29% | 0.12 | 57% | 2.5% | 0.57 | -3.5% (-1.4) |
| Index Turtle (S2) | -2.0% | 6.7% | -0.28 [-0.92, 0.27] | -0.39 | -34% | -0.06 | 37% | 1.2% | 0.14 | -3.8% (-2.6) |
| EW universe | +13.1% | 17.6% | 0.89 [0.44, 1.45] | 1.05 | -40% | 0.33 | 68% | 2.6% | 1.00 | – |

**EU (11 national blue-chip indices, point-in-time)**, median 263 names; L/S book averages 96% long, 94% short, 14 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -9.5% | 18.8% | -0.49 [-1.01, -0.03] | -0.69 | -80% | -0.12 | 43% | 2.8% | -0.46 | -3.3% (-0.8) |
| System 1 only | -12.7% | 21.4% | -0.64 [-1.16, -0.15] | -0.82 | -88% | -0.14 | 41% | 3.1% | -0.41 | -7.3% (-1.6) |
| System 2 only | -7.2% | 21.4% | -0.27 [-0.77, 0.16] | -0.46 | -73% | -0.10 | 45% | 3.2% | -0.52 | +0.5% (0.1) |
| Turtle long-only | +7.3% | 14.4% | 0.55 [-0.05, 1.14] | 0.71 | -37% | 0.20 | 59% | 2.2% | 0.57 | +1.7% (0.4) |
| Index Turtle (S2) | -0.7% | 7.4% | -0.05 [-0.67, 0.49] | -0.14 | -29% | -0.03 | 33% | 1.2% | 0.08 | -1.2% (-0.5) |
| EW universe | +10.8% | 15.8% | 0.80 [0.34, 1.33] | 0.94 | -37% | 0.29 | 63% | 2.4% | 1.00 | – |

**UK (FTSE 350, point-in-time)**, median 329 names; L/S book averages 98% long, 95% short, 16 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -5.3% | 21.4% | -0.17 [-0.66, 0.34] | -0.35 | -68% | -0.08 | 44% | 3.1% | -0.60 | +2.7% (0.5) |
| System 1 only | -9.8% | 23.4% | -0.37 [-0.89, 0.16] | -0.59 | -81% | -0.12 | 43% | 3.4% | -0.49 | -3.1% (-0.5) |
| System 2 only | -1.8% | 25.1% | 0.05 [-0.43, 0.52] | -0.10 | -63% | -0.03 | 46% | 3.5% | -0.71 | +8.5% (1.2) |
| Turtle long-only | +7.5% | 15.6% | 0.60 [0.08, 1.10] | 0.71 | -38% | 0.20 | 57% | 2.2% | 0.54 | +3.4% (1.0) |
| Index Turtle (S2) | -1.8% | 6.9% | -0.20 [-0.80, 0.22] | -0.35 | -38% | -0.05 | 33% | 1.2% | -0.02 | -1.2% (-0.5) |
| EW universe | +9.4% | 15.3% | 0.72 [0.23, 1.35] | 0.87 | -41% | 0.23 | 60% | 2.2% | 1.00 | – |

**DK (OMXC25, point-in-time)**, median 20 names; L/S book averages 73% long, 47% short, 7 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -6.1% | 17.0% | -0.35 [-0.83, 0.11] | -0.50 | -68% | -0.09 | 43% | 2.5% | 0.03 | -5.6% (-1.3) |
| System 1 only | -8.6% | 18.1% | -0.47 [-0.97, 0.02] | -0.66 | -75% | -0.12 | 41% | 2.7% | 0.02 | -7.8% (-1.6) |
| System 2 only | -4.1% | 18.3% | -0.19 [-0.70, 0.31] | -0.31 | -69% | -0.06 | 46% | 2.8% | 0.04 | -3.6% (-0.8) |
| Turtle long-only | +1.0% | 13.1% | 0.13 [-0.37, 0.63] | 0.10 | -38% | 0.03 | 48% | 2.0% | 0.53 | -5.3% (-2.2) |
| Index Turtle (S2) | +1.4% | 8.2% | 0.25 [-0.29, 0.78] | 0.24 | -21% | 0.07 | 35% | 1.4% | 0.18 | -0.5% (-0.3) |
| EW universe | +12.8% | 17.2% | 0.87 [0.34, 1.49] | 1.05 | -35% | 0.37 | 65% | 2.5% | 1.00 | – |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 70 names; L/S book averages 89% long, 74% short, 11 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -14.0% | 17.1% | -0.88 [-1.47, -0.35] | -1.10 | -89% | -0.16 | 41% | 2.6% | -0.10 | -12.3% (-2.8) |
| System 1 only | -18.6% | 18.4% | -1.07 [-1.64, -0.55] | -1.34 | -94% | -0.20 | 35% | 2.8% | -0.15 | -16.7% (-3.5) |
| System 2 only | -9.6% | 19.1% | -0.53 [-1.11, -0.00] | -0.69 | -81% | -0.12 | 45% | 2.9% | -0.05 | -8.0% (-1.8) |
| Turtle long-only | +2.0% | 14.0% | 0.23 [-0.27, 0.75] | 0.20 | -36% | 0.06 | 53% | 2.1% | 0.55 | -4.1% (-1.4) |
| Index Turtle (S2) | +0.3% | 7.9% | 0.09 [-0.53, 0.63] | 0.06 | -26% | 0.01 | 37% | 1.3% | 0.11 | -0.8% (-0.4) |
| EW universe | +12.9% | 16.0% | 0.93 [0.44, 1.52] | 1.14 | -34% | 0.38 | 66% | 2.4% | 1.00 | – |

**World (US + UK + EU, point-in-time)**, median 1086 names; L/S book averages 99% long, 98% short, 18 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -15.7% | 21.5% | -0.75 [-1.32, -0.26] | -0.98 | -93% | -0.17 | 43% | 3.3% | -0.47 | -9.4% (-1.5) |
| System 1 only | -17.4% | 23.5% | -0.73 [-1.30, -0.24] | -1.02 | -95% | -0.18 | 39% | 3.4% | -0.41 | -11.6% (-1.6) |
| System 2 only | -15.1% | 25.4% | -0.57 [-1.13, -0.05] | -0.81 | -94% | -0.16 | 43% | 3.9% | -0.52 | -7.1% (-1.0) |
| Turtle long-only | +4.0% | 15.4% | 0.36 [-0.16, 0.94] | 0.35 | -39% | 0.10 | 55% | 2.4% | 0.60 | -2.4% (-0.7) |
| Index Turtle (S2) | -2.1% | 6.5% | -0.26 [-0.92, 0.33] | -0.43 | -35% | -0.06 | 34% | 1.1% | 0.12 | -3.4% (-1.7) |
| EW universe | +12.0% | 15.9% | 0.82 [0.34, 1.40] | 1.05 | -41% | 0.29 | 63% | 2.3% | 1.00 | – |

*Sharpe 95% CI: stationary bootstrap of monthly returns (Politis & Romano 1994; mean block 6, 5,000 draws). Beta and alpha: OLS of monthly returns on the equal-weight universe, Newey-West t (6 lags). CVaR: mean of the worst 5% of days (InvestmentLibrary.risk.cvar_historic).*

![Drawdowns](../figures/fs01_fig2_drawdown.png)

**Calendar-year returns, Turtle long/short**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -22.3% | -13.3% | +29.7% | -1.7% | -4.6% | -12.7% |
| 2014 | +6.3% | +0.8% | -7.8% | -10.3% | -11.2% | -13.4% |
| 2015 | -12.3% | -20.0% | +2.4% | -8.0% | -28.7% | -9.9% |
| 2016 | -20.2% | -22.3% | -35.6% | -25.7% | -20.5% | -18.6% |
| 2017 | -4.0% | -22.7% | +40.5% | +7.6% | +0.3% | +0.9% |
| 2018 | -22.9% | +8.7% | -11.0% | +0.6% | -21.0% | -25.4% |
| 2019 | -36.8% | -32.5% | -18.0% | -12.0% | -25.7% | -30.2% |
| 2020 | -23.2% | -0.5% | -18.7% | +16.8% | +2.2% | -11.3% |
| 2021 | -19.8% | -16.1% | -3.6% | -14.0% | -6.3% | -28.0% |
| 2022 | -30.9% | -2.6% | -1.6% | -27.0% | -11.9% | -25.1% |
| 2023 | -1.0% | +4.2% | -0.2% | -7.5% | -28.5% | -20.5% |
| 2024 | -7.4% | -3.5% | +11.3% | -4.1% | -14.8% | +2.2% |
| 2025 | -19.1% | -8.2% | -7.4% | +4.0% | -8.1% | -9.3% |
| 2026 | +5.5% | +8.7% | -26.0% | +9.7% | -5.4% | -11.9% |

**Calendar-year returns, Turtle long-only**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +16.9% | +6.2% | +20.1% | +15.9% | +3.4% | +21.0% |
| 2014 | +11.5% | +3.9% | +2.8% | +3.3% | +12.7% | -2.1% |
| 2015 | -3.0% | +0.0% | +17.3% | +6.2% | -7.8% | +1.8% |
| 2016 | +3.6% | +15.5% | +17.0% | -14.9% | +0.1% | +18.3% |
| 2017 | +12.3% | +17.5% | +52.4% | +10.8% | +23.4% | +39.7% |
| 2018 | -20.0% | +13.4% | -13.0% | -13.6% | -17.0% | -8.6% |
| 2019 | +23.3% | -1.7% | -7.9% | +14.5% | +0.2% | +4.4% |
| 2020 | +2.5% | +2.0% | +11.3% | +21.2% | +3.6% | +0.2% |
| 2021 | +14.1% | +7.6% | +11.5% | -6.4% | +17.1% | -2.6% |
| 2022 | -13.4% | -28.5% | -14.7% | -19.5% | -8.4% | -20.9% |
| 2023 | +21.5% | +10.9% | +7.8% | +0.5% | +1.2% | +4.2% |
| 2024 | +0.7% | +16.0% | +8.2% | -1.6% | +2.3% | +2.1% |
| 2025 | -7.6% | +32.0% | -1.6% | +2.7% | +9.7% | -1.0% |
| 2026 | -5.9% | +18.6% | +8.4% | +3.7% | -5.7% | +12.4% |

## 7. Trading record

Every trade is in `results/turtle_trades_<universe>.csv` (ticker, direction, entry and exit date, units, prices, P&L in % of equity at entry, R multiple, exit reason). 1R = the risk of the first unit, 2 N.

| Universe | Trades | Per yr | Win rate | Avg win | Avg loss | Payoff | Profit factor | Expectancy (R) | Days held win / loss | Avg units | Stopped out | Summed P&L long / short |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 7,651 | 557 | 22% | +0.97% | -0.35% | 2.75 | 0.79 | -0.30 | 28 / 10 | 1.8 | 74% | +77% / -523% |
| EU | 6,787 | 495 | 24% | +1.06% | -0.38% | 2.78 | 0.86 | -0.20 | 28 / 10 | 1.9 | 75% | +141% / -412% |
| UK | 7,372 | 537 | 24% | +1.21% | -0.39% | 3.11 | 0.96 | -0.06 | 30 / 10 | 1.9 | 74% | +305% / -397% |
| DK | 3,560 | 259 | 23% | +1.29% | -0.45% | 2.90 | 0.88 | -0.21 | 27 / 9 | 2.1 | 77% | +84% / -231% |
| SCANDI | 5,366 | 391 | 24% | +1.01% | -0.41% | 2.50 | 0.78 | -0.34 | 27 / 10 | 1.9 | 75% | +103% / -472% |
| World | 8,544 | 622 | 23% | +1.01% | -0.37% | 2.76 | 0.82 | -0.25 | 29 / 11 | 1.9 | 74% | +94% / -526% |

**Long-only book**

| Universe | Trades | Win rate | Payoff | Profit factor | Expectancy (R) | Days held win / loss |
|---|---|---|---|---|---|---|
| US | 2,787 | 29% | 2.81 | 1.15 | +0.19 | 32 / 10 |
| EU | 2,575 | 28% | 3.29 | 1.30 | +0.43 | 30 / 10 |
| UK | 2,878 | 27% | 3.50 | 1.31 | +0.44 | 30 / 10 |
| DK | 1,751 | 27% | 2.94 | 1.09 | +0.15 | 29 / 10 |
| SCANDI | 2,384 | 28% | 2.93 | 1.12 | +0.19 | 29 / 10 |
| World | 3,220 | 28% | 2.97 | 1.17 | +0.23 | 29 / 10 |

*Summed P&L adds each trade's P&L in % of equity at entry; it shows where the money went, not a compounded return.*

![Trades](../figures/fs01_fig3_trades.png)

The shape is the classic trend-follower's: most trades are small losses, stopped at about −1 to −2 R, and a thin right tail of 10–40 R winners carries the book. Across all universes the best ~23% of trades earn everything; the other 77% give it back and more.

**Open book, US, 24 September 2026 (largest 8 of 49)**

| Ticker | Side | System | Units | Entered | Weight |
|---|---|---|---|---|---|
| META | long | S1 | 3 | 2026-09-10 | 18.9% |
| AAPL | long | S1 | 2 | 2026-09-14 | 17.5% |
| LYV | short | S1 | 2 | 2026-09-08 | 15.8% |
| CASY | short | S1 | 4 | 2026-08-27 | 15.4% |
| STZ | short | S1 | 2 | 2026-09-09 | 12.7% |
| PCG | short | S1 | 4 | 2026-09-01 | 11.7% |
| CRWD | long | S1 | 3 | 2026-09-15 | 10.3% |
| BLDR | short | S1 | 3 | 2026-09-09 | 10.0% |

Open books for every universe: `results/turtle_open_<universe>.csv`.

## 8. Risk and factor attribution

Monthly returns regressed on seven factor themes: JKP (Jensen, Kelly & Pedersen 2023) market, size, value, momentum, low risk, quality and short-term reversal for the US, UK, DK and World; French Europe 5 factors plus momentum (WML) for EU and SCANDI (JKP has no Europe series; World ex-US is Asia-heavy, which Project2 learned the hard way). Factor data to Dec 2025 (JKP) or Jul 2026 (French). Newey-West t, 6 lags.

**Turtle long/short**

| Universe | Factor model | Months | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|---|
| US | JKP USA 7 themes | 156 | -15.5% | -4.05 | 0.31 | value -0.42 (-3.1), short_term_reversal -1.46 (-6.3) |
| EU | French Europe 5F + WML | 163 | -10.9% | -3.15 | 0.20 | Mkt-RF -0.37 (-4.2), WML +0.37 (+2.3) |
| UK | JKP GBR 7 themes | 156 | -2.6% | -0.49 | 0.36 | momentum +0.49 (+2.4), short_term_reversal -1.55 (-5.0) |
| DK | JKP DNK 7 themes | 156 | -10.0% | -2.49 | 0.11 | momentum +0.26 (+2.1), short_term_reversal -0.36 (-2.1) |
| SCANDI | French Europe 5F + WML | 163 | -17.2% | -3.90 | 0.07 | WML +0.38 (+2.1) |
| World | JKP World 7 themes | 156 | -15.9% | -2.59 | 0.26 | value -0.53 (-2.1), momentum +0.46 (+2.1), short_term_reversal -1.34 (-2.6) |

**Turtle long-only**

| Universe | Factor model | Months | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|---|
| US | JKP USA 7 themes | 156 | -3.3% | -1.33 | 0.52 | mkt +0.77 (+11.0) |
| EU | French Europe 5F + WML | 163 | +2.0% | 0.44 | 0.23 | Mkt-RF +0.46 (+4.9) |
| UK | JKP GBR 7 themes | 156 | +4.7% | 1.26 | 0.31 | mkt +0.35 (+4.8), momentum +0.29 (+2.6), low_risk -0.59 (-2.4), quality +0.39 (+2.0) |
| DK | JKP DNK 7 themes | 156 | -3.7% | -1.48 | 0.33 | mkt +0.44 (+6.6) |
| SCANDI | French Europe 5F + WML | 163 | -2.1% | -0.58 | 0.21 | Mkt-RF +0.44 (+6.3) |
| World | JKP World 7 themes | 156 | -0.3% | -0.08 | 0.44 | mkt +0.67 (+8.4), short_term_reversal -0.56 (-2.0) |

**Reading the loadings.** The long/short book loads on momentum, as it should, and **negatively on short-term reversal** in every JKP universe: US -1.46 (t -6.3), UK -1.55 (t -5.0), DK -0.36 (t -2.1), World -1.34 (t -2.6); significant (|t| ≥ 2) in US, UK, DK, World. Entering the day after a breakout means buying last week's winners and shorting last week's losers, which is exactly the trade that one-month reversal (Jegadeesh 1990) punishes in single stocks. Futures markets do not have that reversal, which is one reason the rules worked there.

## 9. Statistical verdict

- **Gate.** 12 strategy × universe cells across the two factsheets; Bonferroni two-sided 0.05/12 gives |t| > 2.87.
- **Long/short:** negative Sharpe in 6 of 6. The negative factor alphas are significant in several universes, so this is evidence the rule *loses*, not just that it fails to win.
- **Long-only:** higher Sharpe than the equal-weight universe in 0 of 6; alpha vs the universe passes the gate in 0 of 6. Its appeal is a lower beta (0.53–0.60) and a shallower maximum drawdown than the universe in 3 of 6, not extra return. Results lean on a few trades: single positions such as Abivax (ABVX.PA, the verified +561% trial-result week in 2025) or Rheinmetall can make a year.
- **Index version:** Sharpe between -0.28 and 0.25. Small either way: timing the index with breakouts does not add value in a 13-year bull market, the same result as A11 *A Beautiful Mind* for moving-average rules.
- **Probabilistic Sharpe** (Bailey & López de Prado 2012), P(true Sharpe > 0): L/S US 0.00, EU 0.04, UK 0.27, DK 0.10, SCANDI 0.00, World 0.00.

## 10. What goes wrong, and how to fix it

**Method.** Diagnose on the *design* window (2013–2019) only, write down the fixes in a fixed order, then judge each fix on the untouched *holdout* (Jan 2020 – Aug 2026). Every fix stays inside the Turtle rulebook: it changes a knob Faith (2003, 2007) describes (direction, system, stop width, a trend filter), not the idea. Each step is one trial, tested on the equal-weighted average of the six universes with a paired stationary-bootstrap test of the Sharpe difference against the previous step; with 7 fix trials across both factsheets the gate is p < 0.0071. Honest caveat: I had seen the full-sample results in §1–9 before choosing the fixes, so the holdout is clean for the *numbers* but not for the *ideas*.

### 10.1 Diagnosis: five things go wrong

**1. Costs eat the book.** Close-to-close N is small for large caps (median about 1% of the price), so a 0.1%-risk unit is about 10% of equity; with ~500 trades a year and pyramiding, the book trades well over 100× its equity a year. At 10 bp per side that is a double-digit drag:

| Universe | L/S before costs | L/S after costs | Cost drag / yr |
|---|---|---|---|
| US | -9.3% | -20.3% | -10.9% |
| EU | -7.3% | -15.4% | -8.2% |
| DK | -1.9% | -7.0% | -5.1% |
| World | -9.4% | -9.7% | -0.3% |

*Design window 2013–2019, S1+S2 long/short, re-run with costs and borrow set to zero.* Costs explain 3–73% of the loss; the rest is below. (Novy-Marx & Velikov 2016 show the same for high-turnover anomalies in general.)

**2. The short side does all the damage.** Summed trade P&L a year, 2013–2019: short trades -43% to -22% of equity, long trades +1% to +27%. Shorting single stocks in markets rising 10–15% a year, with no stock-specific edge (point 4), loses roughly the market return on the short book.

**3. The 2N stop is too tight for single stocks.** 72–77% of trades end on the 2N stop, and their summed P&L is -99% to -54% of equity a year (summed across trades, not compounded); trades that reach the channel exit sum to +42% to +88%. With a close-to-close N, 2N is only about 2% below the entry, a move the median large cap makes every few days, so the stop harvests noise and multiplies trading.

**4. There is no trend to follow in single stocks at these horizons.** After a fresh 55-day breakout, the stock's return *in excess of its universe* is small and mostly insignificant at every horizon, and where it is significant it is as often negative as positive (t-statistics in brackets):

| Universe | Long: t+1 | t+2..5 | t+6..20 | t+21..60 | Short: t+2..5 | t+6..20 |
|---|---|---|---|---|---|---|
| US | -0.00% (-0.3) | -0.00% (-0.2) | -0.07% (-2.0) | +0.02% (0.4) | -0.05% (-1.6) | +0.06% (1.0) |
| EU | +0.04% (2.5) | +0.00% (0.1) | +0.10% (1.9) | +0.13% (1.5) | +0.00% (0.1) | -0.03% (-0.4) |
| UK | -0.01% (-0.6) | +0.04% (1.3) | -0.12% (-2.4) | +0.10% (1.1) | +0.03% (0.5) | -0.00% (-0.0) |
| DK | -0.09% (-1.5) | +0.21% (2.1) | +0.10% (0.5) | +0.48% (1.5) | -0.05% (-0.3) | -0.06% (-0.2) |
| SCANDI | -0.03% (-1.1) | +0.00% (0.0) | -0.02% (-0.3) | +0.09% (0.6) | +0.02% (0.2) | +0.01% (0.1) |
| World | -0.05% (-6.5) | -0.03% (-2.1) | -0.01% (-0.4) | +0.09% (2.2) | +0.08% (3.5) | -0.02% (-0.5) |

Variance ratios (Lo & MacKinlay 1988) say the same thing: the median single stock has VR(20) = 0.86 and VR(60) = 0.79, net of the market 0.90 and 0.86. Values below 1 mean mild mean reversion, not trend. Breakout rules need VR > 1 (Figure 4, panel C). This is the root cause, and no parameter inside the rulebook can create a trend that is not in the data.

**5. Not the culprit: the one-day fill lag.** The fill-day column (t+1) is a few basis points either way (largest 0.09%), so waiting for the next close costs next to nothing. A "confirmation delay" fix I had coded was dropped before testing, because the diagnosis gave it nothing to fix.

![Diagnosis](../figures/fs01_fig4_diagnosis.png)

### 10.2 The fixes, one step at a time

T0 → T1 drop the shorts (point 2) → T2 keep System 2 only, fewer and longer trades (point 1) → T3 widen the stop from 2N to 4N (point 3) → T4 add a market trend filter: only take new longs when the universe index's 25-day EMA is above its 350-day EMA, a filter of the kind Faith (2007) tests.

| Step | Design Sharpe (avg of 6) | Δ vs previous, design (p) | Holdout Sharpe (6-universe book) | Δ vs previous, holdout (p) | Holdout: universes improved | Holdout return / yr | Holdout max DD | Alpha vs EW / yr (t) | Beta |
|---|---|---|---|---|---|---|---|---|---|
| T0 baseline L/S | -0.79 | – | -0.62 | – | – | -8.6% | -57% | -3.7% (-0.7) | -0.42 |
| T1 long-only | 0.50 | +1.90 (p 0.000) | 0.33 | +0.94 (p 0.018) | 6 of 6 | +3.7% | -21% | -2.1% (-0.9) | 0.50 |
| T2 + System 2 only | 0.50 | +0.11 (p 0.142) | 0.43 | +0.10 (p 0.102) | 4 of 6 | +5.1% | -19% | -0.6% (-0.3) | 0.49 |
| T3 + 4N stop | 0.56 | +0.04 (p 0.406) | 0.50 | +0.06 (p 0.328) | 2 of 6 | +6.0% | -20% | -0.1% (-0.1) | 0.53 |
| T4 + market trend filter | 0.60 | +0.08 (p 0.306) | 0.42 | -0.08 (p 0.672) | 1 of 6 | +4.5% | -19% | +0.5% (0.2) | 0.34 |
| *EW universe (reference)* |  |  | 0.70 |  |  | +11.7% | -25% | – | 1.00 |

*✔ = passes the gate (p < 0.0071). Design Sharpe = average across the six universes; the Δ tests and the holdout columns use the six-universe equal-weighted book. Alpha and beta vs the six-universe equal-weight benchmark, Newey-West t.*

**Per universe, Sharpe design / holdout**

| Universe | T0 | T1 | T2 | T3 | T4 |
|---|---|---|---|---|---|
| US | -1.10 / -0.75 | 0.52 / 0.18 | 0.41 / 0.35 | 0.57 / 0.34 | 0.71 / 0.42 |
| EU | -0.92 / -0.09 | 0.55 / 0.55 | 0.49 / 0.42 | 0.47 / 0.43 | 0.49 / 0.40 |
| UK | -0.06 / -0.26 | 0.78 / 0.41 | 0.82 / 0.54 | 1.11 / 0.44 | 0.91 / 0.19 |
| DK | -0.52 / -0.20 | 0.26 / 0.02 | 0.30 / 0.16 | 0.65 / 0.01 | 0.51 / -0.05 |
| SCANDI | -1.21 / -0.60 | 0.17 / 0.29 | 0.35 / 0.36 | 0.41 / 0.32 | 0.51 / 0.06 |
| World | -0.92 / -0.64 | 0.71 / 0.05 | 0.64 / -0.06 | 0.17 / 0.52 | 0.48 / 0.49 |

![Fix ladder](../figures/fs01_fig5_fixes.png)

### 10.3 What the fixes achieve

- **Dropping the shorts is the big step:** design +1.90 (p 0.000, passes), holdout +0.94 (p 0.018, does not pass the gate).
- **System 2 only:** +0.11 design, +0.10 holdout. Fewer trades, no reliable gain.
- **The 4N stop:** +0.04 design, +0.06 holdout (p 0.33). Positive in both windows, too small to pass.
- **The market trend filter is not trustworthy:** -0.08 in the holdout but +0.08 in the design window. The market was in an up-trend 81–91% of the time, so the filter rarely binds, and its result rests on one or two episodes.
- **Where it ends:** T3 (long-only, System 2, 4N stop) has a holdout Sharpe of 0.50 against 0.70 for the equal-weight universe (difference -0.20, p 0.82) with a beta of about 0.53. T4 reaches 0.42 (-0.28 vs the universe, p 0.85).

**Bottom line.** The fixes remove self-inflicted damage (shorting a bull market, a stop tighter than daily noise, a cost bill from oversized units). What remains is a stop-protected, half-beta equity book, not an edge. The Turtle rules need assets that trend, which is why they were built for, and still work in, diversified futures (Moskowitz, Ooi & Pedersen 2012; Hurst, Ooi & Pedersen 2017). Recommended specification if you insist on stocks: **T3** (long-only, System 2, 4N stop; no market filter, because that filter failed in the design window), and judge it against a half-beta equal-weight portfolio, not against cash.

## 11. Classification: where does it fit?

Evidence: correlations of monthly returns with the 13 JKP factor themes (US, UK, DK, World) or the French Europe factors (EU, SCANDI), a Treynor–Mazuy regression r = a + b·m + γ·m² on the equal-weight universe (γ > 0 = convex, the trend-follower's signature), and returns in the worst and best 10% of market months.

| Dimension | Turtle Traders on stocks |
|---|---|
| Series family (Content_ver2 'Odd ideas') | **Breakout & trend** |
| Academic style | Trend following / time-series momentum (Moskowitz, Ooi & Pedersen 2012); Donchian (1960) breakout |
| Signal | Price only (technical); each stock against its own past, not ranked against other stocks |
| Cross-section vs time series | **Time series.** Position depends on the stock's own channel; the book's net exposure floats (L/S average net +0% to +26%) |
| Horizon and turnover | Medium term: winners held ~28 days, losers ~10; 477 trades a year; very high turnover |
| Trade-level payoff | Positively skewed: 23% winners, payoff ratio 2.8, roughly the best quarter of trades carries the book |
| Book-level payoff | No convexity on stocks: Treynor–Mazuy γ ranges -1.64 to +4.41 (t -3.5 to 4.2); futures trend books show a clear 'smile'. In the worst 10% of market months the L/S earns +0.3% to +3.3% a month: a weak hedge, not crisis alpha |
| Nearest JKP theme (L/S) | **Momentum** (correlation 0.24 to 0.38); low risk 0.08 to 0.44 |
| Nearest theme (long-only, T3) | **Market beta**: correlation with the market 0.37 to 0.56, *negative* with low risk (-0.44 to -0.22): breakouts select volatile stocks |
| Economic rationale | Behavioural: under-reaction then herding (Barberis, Shleifer & Vishny 1998; Hong & Stein 1999). No risk-based story. In futures, also hedging pressure and slow-moving capital |
| Capacity and crowding | High capacity in large caps, but the turnover makes it cost-bound. Crowded in futures (the CTA industry), not in single stocks |
| Publication | Donchian 1960; Turtle rules private 1983, published 2003 (Faith); TSMOM formalised 2012 |
| Where it fits | **A futures strategy mis-applied to stocks.** On single stocks it becomes a momentum-flavoured, high-beta, high-cost book. The correct home is the index/futures level; on stocks, the related evidence-based sibling is cross-sectional 12-1 momentum (Jegadeesh & Titman 1993), not channel breakouts |

![Classification map](../figures/fs_class_map.png)

The map places every book from both factsheets in the same space. The Turtle long/short sits on the momentum axis; its long-only and fixed versions drop into the high-beta corner (negative correlation with low risk), the exact opposite of where the lottery factor lives. The two factsheets are, in factor terms, mirror images: breakouts buy what MAX sells.

## 12. 360° view: the breakout neighbourhood

The Turtle book trades each stock's own channel over time. Its cross-sectional twin ranks stocks by how close they are to their prior 55-day high (**price / 55-day high**, top = at a breakout). Placing that signal among its neighbours shows what a breakout really selects, and whether the information survives outside the Turtle's execution. Same six point-in-time universes, equal-weighted top minus bottom quantile, gross, Feb 2013 – Aug 2026.

| Signal (top minus bottom) | Role | Likeness to Price / prior 55-day high: stocks | Likeness: L/S returns | Raw L/S, avg of 6 | CAPM alpha range | Universes with alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| Price / prior 55-day high | target: the cross-sectional breakout | +1.00 | +1.00 | +1.4% | +4.1% to +13.0% | 4 / 0 |
| Price / 52-week high | lookalike: near the 52-week high | +0.74 | +0.83 | +3.7% | +9.3% to +22.3% | 6 / 0 |
| Last month's return | lookalike: last month's winner | +0.68 | +0.70 | +1.8% | -3.2% to +11.0% | 2 / 0 |
| Momentum 12-1 | cousin: slow momentum | +0.20 | +0.58 | +7.2% | +4.3% to +19.4% | 5 / 0 |
| Price / 52-week low | mirror: at the 52-week low (short breakout) | +0.36 | +0.41 | +7.5% | +5.2% to +13.6% | 4 / 0 |
| MIN (worst day) | cousin: no crash lately | +0.54 | +0.73 | -0.7% | +3.3% to +11.1% | 4 / 0 |
| MAX (best day) | cousin: lottery | -0.04 | -0.48 | +0.1% | -13.3% to -2.0% | 0 / 2 |
| Volatility (63 days) | lookalike (inverse): calm stocks | -0.38 | -0.69 | +1.1% | -13.7% to -7.9% | 0 / 5 |
| Beta (252 days) | lookalike (inverse): low beta | -0.22 | -0.60 | +4.4% | -12.6% to -4.2% | 0 / 4 |

![360 map](../figures/nbh_brk_map.png)

**What a breakout selects.** Stocks at a 55-day high are last month's winners (rank corr with last month's return +0.68), close to their 52-week high (+0.74), calm rather than volatile (-0.38 with volatility) and without recent crashes (+0.54 with MIN). It is *not* the lottery signal (-0.04 with MAX).

**Is there information?** Yes, once beta is removed: the breakout sort has a CAPM alpha of +4.1% to +13.0% (t ≥ 2 in 4 of 6), because breakout stocks are low-beta and the raw spread is dragged down in a bull market. But it is a weaker copy of its neighbours: nearness to the 52-week high earns +9.3% to +22.3% (t ≥ 2 in 6) and 12-1 momentum +4.3% to +19.4% (t ≥ 2 in 5).

**Spanning.** Against momentum, the 52-week high, last month's return, volatility, MAX and the market, the breakout sort keeps an alpha of -3.3% to +3.1% (|t| ≤ 1.6), with R² 0.66 to 0.95. **The breakout is redundant given the 52-week high and one-month return.**

| Universe | Breakout alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 (loading, t) |
|---|---|---|---|---|
| US | +0.3% | 0.21 | 0.93 | Momentum 12-1 -0.09 (-2.1), Price / 52-week high +0.59 (+7.8), Last month's return +0.41 (+10.1), MAX -0.13 (-2.1) |
| EU | -3.3% | -1.43 | 0.83 | Momentum 12-1 -0.13 (-3.0), Price / 52-week high +0.58 (+7.6), Last month's return +0.41 (+9.1) |
| UK | -0.5% | -0.23 | 0.90 | Price / 52-week high +0.51 (+6.4), Last month's return +0.40 (+9.0), Volatility -0.21 (-2.4) |
| DK | +3.1% | 0.99 | 0.66 | Price / 52-week high +0.38 (+4.3), Last month's return +0.54 (+5.5), Volatility -0.28 (-4.2) |
| SCANDI | +0.7% | 0.29 | 0.66 | Price / 52-week high +0.46 (+5.5), Last month's return +0.39 (+6.1), Volatility -0.20 (-2.0) |
| World | -2.0% | -1.56 | 0.95 | Momentum 12-1 -0.14 (-3.4), Price / 52-week high +0.65 (+9.9), Last month's return +0.39 (+9.2) |

![Double sort](../figures/nbh_brk_dsort.png)

**Mirror.** The short-side mirror, a stock at its 52-week low, is the stronger signal: holding the breakout fixed, stocks far above their 52-week low out-earn stocks at the low by +6.0, +6.0 and +2.2 points a year, while the breakout adds little within each column. That is consistent with §10: the Turtle's short breakouts lost because the stock was high-beta in a rising market, not because the cross-sectional information pointed the wrong way.

**Verdict of the 360° view.** The breakout carries real, beta-adjusted information, but it is a noisy subset of the 52-week-high and momentum effects (George & Hwang 2004; Jegadeesh & Titman 1993). The Turtle rules waste it through time-series execution, stops and shorts (§10). For the factor battery, FS09 (52-week high) and FS03 (momentum) are the signals to carry forward, not the breakout itself.

## 13. Caveats

1. **Survivorship: fixed as far as the data allow.** The first edition of this factsheet used today's index members outside the US. This edition uses point-in-time membership everywhere (§3). The table shows the change, same code, same period (survivor list → point-in-time). Note that the universes also changed definition (national blue-chip indices instead of STOXX 600), so the difference is survivorship plus composition.

| Universe | EW universe CAGR | L/S Sharpe | Long-only Sharpe | Long-only alpha vs EW |
|---|---|---|---|---|
| EU | +14.5% → +10.8% | -0.91 → -0.49 | 0.66 → 0.55 | +1.8% → +1.7% |
| UK | +13.1% → +9.4% | -0.45 → -0.17 | 0.72 → 0.60 | +2.7% → +3.4% |
| DK | +18.2% → +12.8% | -0.21 → -0.35 | 0.44 → 0.13 | -4.5% → -5.3% |
| SCANDI | +15.8% → +12.9% | -0.69 → -0.88 | 0.39 → 0.23 | -3.4% → -4.1% |
| World | +16.8% → +12.0% | -0.96 → -0.75 | 0.80 → 0.36 | +1.3% → -2.4% |

The equal-weight universes lose 2–5 percentage points a year once survivors are removed, which is the survivorship bias Project2 measured. The conclusions do not change. About a fifth of member-quarters have no price (mostly delisted names Yahoo no longer serves), so a residual bias remains; it flatters long books and hurts short books.
2. **Close-only simulation.** The Turtles entered intraday at the breakout price; here the fill is the next day's close. That is conservative for entries and exits alike.
3. **Close-to-close N** ignores intraday highs and lows, so it understates the true range and makes units somewhat larger than the original rule.
4. **Currency.** Local currency; World sums local-currency returns without converting them.
5. **Sizing is an adaptation.** The 0.1% unit and the gross cap are my choices, set once on mechanics (leverage), never tuned on returns. Other choices would change the level of returns, not the sign of the short side.
6. **Not a registered trial.** This factsheet is descriptive and is not added to the programme's trial ledger. The fix ladder in §10 is counted inside the factsheets (7 trials, gate 0.05/7). The *Trading Places* article (Season 2) will pre-register a single test.

## 14. Academic references

- Faith, C. (2003). *The Original Turtle Trading Rules*. OriginalTurtles.org (free PDF).
- Faith, C. (2007). *Way of the Turtle: The Secret Methods that Turned Ordinary People into Legendary Traders*. McGraw-Hill.
- Covel, M. (2007). *The Complete TurtleTrader*. HarperCollins.
- Donchian, R. D. (1960). High finance in copper. *Financial Analysts Journal*, 16(6), 133–142.
- Wilcox, C. & Crittenden, E. (2005). Does trend-following work on stocks? Blackstar Funds white paper.
- Moskowitz, T., Ooi, Y. H. & Pedersen, L. H. (2012). Time series momentum. *Journal of Financial Economics*, 104(2), 228–250.
- Hurst, B., Ooi, Y. H. & Pedersen, L. H. (2017). A century of evidence on trend-following investing. *Journal of Portfolio Management*, 44(1), 15–29.
- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns. *Journal of Finance*, 45(3), 881–898.
- George, T. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance*, 59(5), 2145–2176.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5), 2465–2518.
- Fama, E. & French, K. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1–22.
- Newey, W. & West, K. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.
- Politis, D. & Romano, J. (1994). The stationary bootstrap. *Journal of the American Statistical Association*, 89(428), 1303–1313.
- Bailey, D. & López de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk*, 15(2), 3–44.
- Lo, A. & MacKinlay, A. C. (1988). Stock market prices do not follow random walks: Evidence from a simple specification test. *Review of Financial Studies*, 1(1), 41–66.
- Barberis, N., Shleifer, A. & Vishny, R. (1998). A model of investor sentiment. *Journal of Financial Economics*, 49(3), 307–343.
- Hong, H. & Stein, J. (1999). A unified theory of underreaction, momentum trading, and overreaction in asset markets. *Journal of Finance*, 54(6), 2143–2184.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1), 65–91.
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies*, 29(1), 104–147.
- Treynor, J. & Mazuy, K. (1966). Can mutual funds outguess the market? *Harvard Business Review*, 44(4), 131–136.

## 15. Reproduce

`code/data.py` (universes) → `code/turtle.py` + `run_turtle.py <U>` (simulator) → `analyse.py turtle` (statistics, attribution) → §10–11: `diag_turtle.py`, `cost_check.py`, `turtle_fix.py <U>`, `fix_analysis.py` → §12: `signals.py`, `neighbourhood.py brk`, `nbh_figs.py`, `nbh_section.py` → `make_figures.py` → `build_factsheets.py` (sections 10–11 in `sections_fix_class.py`). Metrics call Project1 `InvestmentLibrary` (stats, risk, reporting). Licensed Sharadar and cached Yahoo prices are not included; results files hold derived numbers only.


## Addendum: the long-only books at 100% invested

The Turtle rules size each position by risk (0.1% of equity per N) and leave the rest in cash at 0%. Here every position is scaled by the same factor so the long book is 100% of equity at every close (`code/turtle.py: fully_invested`, `code/turtle_full.py`); re-scaling is charged 10 bp on the notional it moves; days with no position stay in cash. Same four pre-declared steps, 2013–2026; a restatement, not a new trial.

| Universe | Long-only book | Invested as designed | CAGR, as designed / 100% | Sharpe, as designed / 100% | Max drawdown, as designed / 100% | Holdout 2020+ Sharpe, as designed / 100% |
|---|---|---:|---:|---:|---:|---:|
| US | T1 long-only | 96% | +3.3% / +2.8% | 0.29 / 0.25 | -29% / -36% | 0.15 / 0.17 |
| US | T2 + System 2 only | 96% | +4.7% / +3.8% | 0.35 / 0.30 | -30% / -37% | 0.32 / 0.30 |
| US | T3 + 4N stop | 97% | +5.9% / +5.8% | 0.41 / 0.39 | -34% / -40% | 0.32 / 0.31 |
| US | T4 + market trend filter | 93% | +9.1% / +8.4% | 0.54 / 0.50 | -43% / -45% | 0.43 / 0.37 |
| EU | T1 long-only | 95% | +7.3% / +4.4% | 0.56 / 0.35 | -37% / -50% | 0.53 / 0.26 |
| EU | T2 + System 2 only | 95% | +6.6% / +3.6% | 0.48 / 0.29 | -39% / -48% | 0.42 / 0.24 |
| EU | T3 + 4N stop | 96% | +5.7% / +5.4% | 0.44 / 0.40 | -36% / -43% | 0.38 / 0.28 |
| EU | T4 + market trend filter | 88% | +5.8% / +4.1% | 0.45 / 0.33 | -33% / -41% | 0.38 / 0.21 |
| UK | T1 long-only | 97% | +7.5% / +4.9% | 0.54 / 0.37 | -38% / -57% | 0.33 / 0.06 |
| UK | T2 + System 2 only | 96% | +11.0% / +8.8% | 0.65 / 0.53 | -36% / -54% | 0.50 / 0.26 |
| UK | T3 + 4N stop | 97% | +12.1% / +10.6% | 0.74 / 0.63 | -27% / -42% | 0.39 / 0.26 |
| UK | T4 + market trend filter | 85% | +7.7% / +6.2% | 0.56 / 0.45 | -22% / -34% | 0.16 / -0.01 |
| DK | T1 long-only | 73% | +1.0% / -6.1% | 0.14 / -0.23 | -38% / -74% | 0.03 / -0.45 |
| DK | T2 + System 2 only | 72% | +2.4% / -1.6% | 0.24 / 0.03 | -36% / -68% | 0.18 / -0.08 |
| DK | T3 + 4N stop | 79% | +3.9% / +3.6% | 0.33 / 0.27 | -44% / -64% | 0.03 / -0.01 |
| DK | T4 + market trend filter | 70% | +2.6% / +1.2% | 0.25 / 0.16 | -45% / -57% | -0.00 / -0.15 |
| SC | T1 long-only | 88% | +2.0% / +0.5% | 0.21 / 0.11 | -36% / -50% | 0.25 / 0.17 |
| SC | T2 + System 2 only | 88% | +3.9% / +2.8% | 0.33 / 0.24 | -37% / -54% | 0.31 / 0.31 |
| SC | T3 + 4N stop | 91% | +4.4% / +5.5% | 0.35 / 0.39 | -32% / -44% | 0.32 / 0.41 |
| SC | T4 + market trend filter | 83% | +3.3% / +3.0% | 0.29 / 0.26 | -38% / -47% | 0.10 / 0.02 |
| WD | T1 long-only | 98% | +4.0% / +3.2% | 0.33 / 0.27 | -39% / -45% | 0.01 / -0.05 |
| WD | T2 + System 2 only | 98% | +2.8% / +2.3% | 0.25 / 0.21 | -52% / -55% | -0.14 / -0.16 |
| WD | T3 + 4N stop | 98% | +4.9% / +4.3% | 0.35 / 0.32 | -40% / -44% | 0.51 / 0.46 |
| WD | T4 + market trend filter | 91% | +6.0% / +5.3% | 0.42 / 0.37 | -31% / -36% | 0.40 / 0.34 |

**Reading.** The books are already mostly invested, so scaling adds little exposure but a lot of concentration on the days the system holds only one or two names (after mass exits in sell-offs). That is where the extra drawdown comes from. A fully invested Turtle book would need a minimum number of positions or a cap on the scale factor: a new, pre-declared specification.
