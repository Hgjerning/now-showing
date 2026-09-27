# FACTSHEET FS01 · The Turtle Traders

### Richard Dennis's 1983 trading rules, applied stock by stock to six equity universes

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 25 September 2026*

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

> **Verdict in one paragraph.** Dennis's students reportedly made more than $100 million with these rules on 1980s futures (Covel 2007). On single stocks, 2013–2026, the long/short version **lost money in all six universes** (Sharpe -0.86 to -0.25). Nearly all of the loss is the short side: stocks that break to a new low tend to bounce, and a rising market punishes every short. The long-only version made money everywhere, but **had a lower Sharpe than simply owning the equal-weight universe in all six**; its alpha against the universe is between -5.4% and -0.1% a year, and none reaches the 2.87 gate. The trade profile is textbook trend following, about 23% winners with winners 2.8× the size of losers. On stocks, that is not enough to pay for the whipsaws. **What goes wrong (§10):** costs from oversized units, a short book in a bull market, a 2N stop tighter than daily noise and, at the root, no trend in single stocks to follow. Fixing what can be fixed gives a long-only, half-beta book that still trails the equal-weight universe's Sharpe in the 2020–26 holdout (0.64 vs 0.75). **Classification (§11):** a futures trend strategy mis-applied to stocks. **360° view (§12):** the cross-sectional breakout does carry beta-adjusted information, but it is a noisy subset of the 52-week-high and momentum effects.

## 1. Headline performance

| Universe | L/S CAGR | L/S Sharpe | L/S max DD | Long-only CAGR | LO Sharpe | LO max DD | EW universe CAGR | EW Sharpe | EW max DD |
|---|---|---|---|---|---|---|---|---|---|
| US | -16.6% | -0.86 | -92% | +2.9% | 0.27 | -36% | +14.8% | 1.01 | -39% |
| EU | -8.8% | -0.47 | -81% | +5.1% | 0.44 | -37% | +11.4% | 0.83 | -37% |
| UK | -10.6% | -0.53 | -85% | +5.4% | 0.49 | -23% | +10.3% | 0.79 | -40% |
| DK | -4.9% | -0.25 | -60% | +2.6% | 0.25 | -37% | +13.1% | 0.87 | -35% |
| SCANDI | -13.0% | -0.83 | -87% | +2.2% | 0.23 | -30% | +13.4% | 0.97 | -33% |
| World | -15.3% | -0.79 | -92% | +6.4% | 0.48 | -37% | +13.6% | 0.92 | -40% |

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
| US | Sharadar SEP `closeadj` (total return), 805 tickers incl. delisted | **Point-in-time**: top 500 by market cap each month-end (Sharadar filings × price, A06 method) | ~499 | USD |
| EU | Project1 yfinance cache, Adj Close (TR) | **Point-in-time**: union of 11 national blue-chip indices (CAC 40, DAX, AEX, IBEX 35, FTSE MIB, OMXS30, OMXC25, OMXH25, BEL 20, PSI-20, WIG20), quarterly Wikipedia snapshots 2012–2026; 83% of member-quarters priced | ~238 | local (EUR, SEK, DKK, PLN) |
| UK | Project1 cache, Close + pence dividends (Yahoo under-adjusts LSE ~100×) | **Point-in-time**: FTSE 100 + FTSE 250, quarterly snapshots; 75% priced | ~242 | GBP |
| DK | Project1 cache, Adj Close | **Point-in-time**: OMX Copenhagen 25, quarterly snapshots; 91% priced | ~19 | DKK |
| SCANDI | Project1 cache, Adj Close | **Point-in-time**: OMXC25 + OMXS30 + OMXH25 (Oslo has no snapshot history); 88% priced | ~62 | local (DKK, SEK, EUR) |
| World | US Sharadar + UK + EU above | **Point-in-time** union of the three; local-currency returns summed, not converted | ~963 | mixed |

*Membership comes from Project2's cache of dated Wikipedia index pages (the same parsing as `run_wiki_pit.py` / `run_eu_pit.py`), with a short list of verified ticker renames (e.g. NZYM-B → NSIS-B, WDH → DEMANT, DAI → MBG). A name is eligible from the day after the snapshot that lists it, once it has 60 days of prices. Member-quarters without a price are mostly delisted names that Yahoo no longer serves, so some survivorship remains; see §13.*

Window: signals from January 2012, performance from 2 January 2013 (a year of history needed for eligibility) to 24/25 September 2026. Eligibility: US, member of the point-in-time top 500 at the previous month-end; others, at least 252 days of price history. Cleaning follows Project2's rules: the five series Project2 verified as corrupt (DIA.MC, ATO.PA, ZEG.L, SPM.MI, VPLAY-B.ST) are dropped, and any daily move beyond ±100% is set to missing unless it was verified as real (ABVX.PA, MRNA, ECHO, GME). That removed 12 US and 2 European daily prints.

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

**US (top 500, point-in-time)**, median 499 names; L/S book averages 97% long, 95% short, 16 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -16.6% | 23.9% | -0.86 [-1.54, -0.33] | -0.93 | -92% | -0.18 | 35% | 3.7% | -0.13 | -13.8% (-3.1) |
| System 1 only | -20.2% | 24.6% | -1.00 [-1.71, -0.40] | -1.11 | -96% | -0.21 | 32% | 3.7% | -0.03 | -19.1% (-3.5) |
| System 2 only | -13.9% | 27.8% | -0.53 [-1.12, -0.09] | -0.67 | -89% | -0.16 | 40% | 4.3% | -0.22 | -8.5% (-1.8) |
| Turtle long-only | +2.9% | 17.2% | 0.27 [-0.18, 0.72] | 0.23 | -36% | 0.08 | 55% | 2.7% | 0.64 | -5.4% (-1.6) |
| Index Turtle (S2) | -1.0% | 8.5% | -0.08 [-0.70, 0.38] | -0.17 | -30% | -0.03 | 38% | 1.3% | 0.06 | -1.6% (-0.6) |
| EW universe | +14.8% | 17.3% | 1.01 [0.54, 1.57] | 1.20 | -39% | 0.38 | 68% | 2.6% | 1.00 | – |

**EU (11 national blue-chip indices, point-in-time)**, median 236 names; L/S book averages 95% long, 92% short, 14 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -8.8% | 19.4% | -0.47 [-0.93, -0.03] | -0.63 | -81% | -0.11 | 37% | 2.9% | -0.46 | -2.4% (-0.6) |
| System 1 only | -11.9% | 20.9% | -0.58 [-1.05, -0.15] | -0.78 | -86% | -0.14 | 41% | 3.1% | -0.47 | -5.3% (-1.2) |
| System 2 only | -6.5% | 22.5% | -0.25 [-0.77, 0.28] | -0.40 | -81% | -0.08 | 41% | 3.3% | -0.45 | +0.5% (0.1) |
| Turtle long-only | +5.1% | 13.5% | 0.44 [-0.11, 0.97] | 0.53 | -37% | 0.14 | 57% | 2.0% | 0.53 | -0.7% (-0.2) |
| Index Turtle (S2) | -1.2% | 7.2% | -0.13 [-0.69, 0.33] | -0.24 | -26% | -0.05 | 32% | 1.2% | 0.07 | -1.8% (-0.8) |
| EW universe | +11.4% | 16.0% | 0.83 [0.36, 1.35] | 0.98 | -37% | 0.31 | 63% | 2.4% | 1.00 | – |

**UK (FTSE 350, point-in-time)**, median 231 names; L/S book averages 97% long, 92% short, 14 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -10.6% | 19.0% | -0.53 [-1.03, -0.09] | -0.76 | -85% | -0.12 | 45% | 2.8% | -0.54 | -3.7% (-0.8) |
| System 1 only | -13.8% | 20.7% | -0.61 [-1.17, -0.11] | -0.91 | -93% | -0.15 | 43% | 3.1% | -0.46 | -7.6% (-1.3) |
| System 2 only | -8.2% | 22.2% | -0.31 [-0.78, 0.14] | -0.51 | -80% | -0.10 | 45% | 3.3% | -0.62 | +0.4% (0.1) |
| Turtle long-only | +5.4% | 13.9% | 0.49 [0.05, 0.99] | 0.54 | -23% | 0.23 | 61% | 2.1% | 0.57 | -0.1% (-0.0) |
| Index Turtle (S2) | -1.7% | 6.2% | -0.24 [-0.75, 0.25] | -0.37 | -36% | -0.05 | 32% | 1.1% | 0.09 | -2.5% (-1.5) |
| EW universe | +10.3% | 15.2% | 0.79 [0.29, 1.40] | 0.96 | -40% | 0.26 | 60% | 2.2% | 1.00 | – |

**DK (OMXC25, point-in-time)**, median 19 names; L/S book averages 72% long, 44% short, 7 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -4.9% | 16.9% | -0.25 [-0.74, 0.22] | -0.40 | -60% | -0.08 | 43% | 2.5% | 0.00 | -3.9% (-0.9) |
| System 1 only | -6.3% | 17.9% | -0.32 [-0.82, 0.19] | -0.50 | -64% | -0.10 | 45% | 2.6% | -0.01 | -5.1% (-1.0) |
| System 2 only | -3.8% | 18.3% | -0.16 [-0.67, 0.31] | -0.29 | -64% | -0.06 | 45% | 2.8% | 0.01 | -2.8% (-0.6) |
| Turtle long-only | +2.6% | 13.1% | 0.25 [-0.27, 0.78] | 0.27 | -37% | 0.07 | 47% | 2.0% | 0.53 | -3.8% (-1.5) |
| Index Turtle (S2) | +1.7% | 8.0% | 0.29 [-0.27, 0.83] | 0.30 | -18% | 0.10 | 35% | 1.3% | 0.18 | -0.4% (-0.3) |
| EW universe | +13.1% | 17.6% | 0.87 [0.33, 1.49] | 1.06 | -35% | 0.38 | 64% | 2.5% | 1.00 | – |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names; L/S book averages 87% long, 71% short, 10 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -13.0% | 17.0% | -0.83 [-1.36, -0.36] | -1.03 | -87% | -0.15 | 37% | 2.6% | -0.13 | -10.9% (-2.8) |
| System 1 only | -12.1% | 18.6% | -0.71 [-1.23, -0.19] | -0.88 | -86% | -0.14 | 42% | 2.8% | -0.14 | -9.4% (-2.2) |
| System 2 only | -14.5% | 19.0% | -0.79 [-1.29, -0.33] | -1.03 | -90% | -0.16 | 37% | 2.9% | -0.13 | -12.4% (-2.7) |
| Turtle long-only | +2.2% | 14.1% | 0.23 [-0.24, 0.72] | 0.21 | -30% | 0.07 | 51% | 2.1% | 0.54 | -4.4% (-1.7) |
| Index Turtle (S2) | +1.7% | 7.9% | 0.29 [-0.29, 0.83] | 0.30 | -21% | 0.08 | 40% | 1.3% | 0.11 | +0.6% (0.3) |
| EW universe | +13.4% | 16.1% | 0.97 [0.46, 1.56] | 1.18 | -33% | 0.40 | 68% | 2.4% | 1.00 | – |

**World (US + UK + EU, point-in-time)**, median 959 names; L/S book averages 99% long, 98% short, 17 positions

| Book | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Calmar | Hit (mo) | CVaR 95% (day) | Beta | Alpha/yr (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Turtle L/S (S1+S2) | -15.3% | 20.7% | -0.79 [-1.34, -0.30] | -0.99 | -92% | -0.17 | 41% | 3.1% | -0.47 | -8.1% (-1.6) |
| System 1 only | -16.0% | 22.7% | -0.67 [-1.23, -0.19] | -0.95 | -94% | -0.17 | 42% | 3.4% | -0.47 | -8.3% (-1.3) |
| System 2 only | -15.6% | 23.8% | -0.70 [-1.27, -0.16] | -0.88 | -92% | -0.17 | 41% | 3.6% | -0.48 | -7.9% (-1.4) |
| Turtle long-only | +6.4% | 15.7% | 0.48 [-0.04, 1.04] | 0.57 | -37% | 0.17 | 55% | 2.4% | 0.65 | -2.0% (-0.6) |
| Index Turtle (S2) | -1.0% | 6.2% | -0.11 [-0.72, 0.43] | -0.21 | -28% | -0.04 | 38% | 1.1% | 0.13 | -2.7% (-1.9) |
| EW universe | +13.6% | 15.7% | 0.92 [0.44, 1.50] | 1.21 | -40% | 0.34 | 65% | 2.3% | 1.00 | – |

*Sharpe 95% CI: stationary bootstrap of monthly returns (Politis & Romano 1994; mean block 6, 5,000 draws). Beta and alpha: OLS of monthly returns on the equal-weight universe, Newey-West t (6 lags). CVaR: mean of the worst 5% of days (InvestmentLibrary.risk.cvar_historic).*

![Drawdowns](../figures/fs01_fig2_drawdown.png)

**Calendar-year returns, Turtle long/short**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -33.0% | -16.8% | +32.8% | -5.6% | -8.4% | -21.9% |
| 2014 | -4.8% | -12.5% | -0.8% | -13.7% | -12.6% | +5.3% |
| 2015 | -21.5% | -14.1% | -4.4% | +6.6% | -18.1% | -3.8% |
| 2016 | -16.8% | -8.7% | -34.1% | -23.9% | -12.4% | -23.9% |
| 2017 | -12.2% | -20.0% | -6.8% | +5.4% | -6.5% | -4.8% |
| 2018 | -20.9% | -2.1% | -5.9% | -3.9% | -23.2% | +5.2% |
| 2019 | -24.0% | -31.4% | -7.5% | -13.9% | -23.5% | -24.8% |
| 2020 | -27.0% | +3.0% | -17.8% | +30.0% | +6.9% | -24.2% |
| 2021 | -22.8% | -23.1% | -27.1% | -14.1% | -9.8% | -27.0% |
| 2022 | -24.4% | -11.7% | -9.1% | -19.2% | -19.5% | -19.7% |
| 2023 | -2.3% | +9.8% | -3.7% | -9.0% | -18.9% | -30.0% |
| 2024 | +21.5% | -3.1% | -2.5% | -2.7% | -12.4% | -10.2% |
| 2025 | -20.4% | +7.7% | -18.3% | +0.8% | -6.3% | -15.8% |
| 2026 | -6.6% | +13.8% | -23.9% | +9.7% | -10.3% | -9.4% |

**Calendar-year returns, Turtle long-only**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +9.9% | +1.1% | +24.3% | +12.1% | +12.0% | +17.1% |
| 2014 | +10.5% | -1.9% | +0.1% | -0.9% | +8.3% | +9.5% |
| 2015 | -12.6% | -6.1% | +14.8% | +12.4% | -4.8% | -2.1% |
| 2016 | -0.7% | +31.5% | -0.3% | -13.4% | +4.0% | +0.1% |
| 2017 | +10.6% | +2.9% | +27.7% | +6.5% | +15.3% | +44.9% |
| 2018 | -17.6% | +8.3% | -6.1% | -11.9% | -18.7% | -13.9% |
| 2019 | +6.7% | +5.2% | +10.3% | +12.5% | +4.3% | -1.1% |
| 2020 | +0.8% | -1.2% | +8.1% | +30.6% | +5.3% | +8.2% |
| 2021 | +6.6% | +15.1% | +22.4% | +7.8% | +12.5% | +17.8% |
| 2022 | -22.6% | -18.4% | -14.5% | -15.4% | -16.4% | -22.0% |
| 2023 | +13.4% | +7.3% | +8.9% | -4.1% | +5.6% | -6.2% |
| 2024 | +17.7% | +0.2% | +2.9% | +2.1% | +5.1% | +13.7% |
| 2025 | +5.2% | +8.2% | -14.1% | +2.3% | +3.3% | +7.4% |
| 2026 | +23.7% | +28.5% | +0.5% | +3.3% | +1.1% | +35.6% |

## 7. Trading record

Every trade is in `results/turtle_trades_<universe>.csv` (ticker, direction, entry and exit date, units, prices, P&L in % of equity at entry, R multiple, exit reason). 1R = the risk of the first unit, 2 N.

| Universe | Trades | Per yr | Win rate | Avg win | Avg loss | Payoff | Profit factor | Expectancy (R) | Days held win / loss | Avg units | Stopped out | Summed P&L long / short |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 7,643 | 557 | 22% | +0.98% | -0.36% | 2.72 | 0.79 | -0.30 | 28 / 10 | 1.8 | 74% | +75% / -527% |
| EU | 6,692 | 488 | 23% | +1.11% | -0.38% | 2.93 | 0.89 | -0.17 | 29 / 10 | 1.8 | 76% | +170% / -394% |
| UK | 6,927 | 505 | 23% | +1.16% | -0.39% | 2.98 | 0.87 | -0.19 | 29 / 10 | 1.9 | 75% | +193% / -456% |
| DK | 3,420 | 249 | 23% | +1.35% | -0.45% | 3.03 | 0.90 | -0.18 | 27 / 9 | 2.1 | 77% | +98% / -218% |
| SCANDI | 5,135 | 374 | 24% | +1.04% | -0.42% | 2.51 | 0.79 | -0.32 | 26 / 10 | 1.9 | 76% | +83% / -418% |
| World | 8,375 | 610 | 23% | +0.99% | -0.36% | 2.71 | 0.82 | -0.25 | 29 / 11 | 1.8 | 74% | +50% / -463% |

**Long-only book**

| Universe | Trades | Win rate | Payoff | Profit factor | Expectancy (R) | Days held win / loss |
|---|---|---|---|---|---|---|
| US | 2,950 | 28% | 2.93 | 1.15 | +0.20 | 31 / 10 |
| EU | 2,503 | 28% | 3.22 | 1.26 | +0.37 | 31 / 9 |
| UK | 2,638 | 29% | 3.11 | 1.26 | +0.37 | 30 / 10 |
| DK | 1,685 | 28% | 3.06 | 1.17 | +0.30 | 30 / 9 |
| SCANDI | 2,348 | 29% | 2.86 | 1.15 | +0.22 | 29 / 10 |
| World | 3,170 | 28% | 3.26 | 1.26 | +0.35 | 31 / 10 |

*Summed P&L adds each trade's P&L in % of equity at entry; it shows where the money went, not a compounded return.*

![Trades](../figures/fs01_fig3_trades.png)

The shape is the classic trend-follower's: most trades are small losses, stopped at about −1 to −2 R, and a thin right tail of 10–40 R winners carries the book. Across all universes the best ~23% of trades earn everything; the other 77% give it back and more.

**Open book, US, 24 September 2026 (largest 8 of 54)**

| Ticker | Side | System | Units | Entered | Weight |
|---|---|---|---|---|---|
| HWM | short | S1 | 3 | 2026-09-09 | 14.4% |
| A | long | S1 | 2 | 2026-09-23 | 13.7% |
| STZ | short | S1 | 2 | 2026-09-09 | 13.3% |
| PEG | short | S1 | 1 | 2026-09-24 | 10.9% |
| NEE | short | S1 | 1 | 2026-09-24 | 10.8% |
| HPE | long | S1 | 3 | 2026-09-14 | 9.8% |
| WBD | long | S1 | 1 | 2026-09-22 | 9.2% |
| MCD | short | S1 | 1 | 2026-09-24 | 8.3% |

Open books for every universe: `results/turtle_open_<universe>.csv`.

## 8. Risk and factor attribution

Monthly returns regressed on seven factor themes: JKP (Jensen, Kelly & Pedersen 2023) market, size, value, momentum, low risk, quality and short-term reversal for the US, UK, DK and World; French Europe 5 factors plus momentum (WML) for EU and SCANDI (JKP has no Europe series; World ex-US is Asia-heavy, which Project2 learned the hard way). Factor data to Dec 2025 (JKP) or Jul 2026 (French). Newey-West t, 6 lags.

**Turtle long/short**

| Universe | Factor model | Months | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|---|
| US | JKP USA 7 themes | 156 | -18.4% | -4.76 | 0.19 | momentum +0.40 (+2.5), short_term_reversal -1.21 (-4.0) |
| EU | French Europe 5F + WML | 163 | -9.1% | -2.65 | 0.19 | Mkt-RF -0.39 (-3.8) |
| UK | JKP GBR 7 themes | 156 | -9.2% | -2.65 | 0.33 | momentum +0.36 (+2.2), short_term_reversal -1.07 (-4.2) |
| DK | JKP DNK 7 themes | 156 | -8.3% | -1.98 | 0.13 | momentum +0.30 (+2.4), short_term_reversal -0.38 (-2.4) |
| SCANDI | French Europe 5F + WML | 163 | -15.4% | -3.64 | 0.07 | WML +0.33 (+2.2) |
| World | JKP World 7 themes | 156 | -16.5% | -3.47 | 0.26 | quality +0.63 (+2.7), short_term_reversal -1.02 (-2.0) |

**Turtle long-only**

| Universe | Factor model | Months | Alpha / yr | t(alpha) | R² | Loadings with |t| ≥ 2 (t) |
|---|---|---|---|---|---|---|
| US | JKP USA 7 themes | 156 | -7.0% | -2.35 | 0.52 | mkt +0.78 (+11.3), size -0.38 (-2.2), momentum +0.50 (+3.7), short_term_reversal -0.52 (-2.1) |
| EU | French Europe 5F + WML | 163 | +0.8% | 0.20 | 0.24 | Mkt-RF +0.40 (+5.9) |
| UK | JKP GBR 7 themes | 156 | +2.6% | 0.90 | 0.36 | mkt +0.37 (+5.7), low_risk -0.38 (-2.2), quality +0.50 (+2.6) |
| DK | JKP DNK 7 themes | 156 | -1.9% | -0.69 | 0.31 | mkt +0.43 (+6.0) |
| SCANDI | French Europe 5F + WML | 163 | -2.0% | -0.63 | 0.23 | Mkt-RF +0.41 (+5.9) |
| World | JKP World 7 themes | 156 | -0.3% | -0.09 | 0.44 | mkt +0.61 (+9.9), momentum +0.38 (+3.1) |

**Reading the loadings.** The long/short book loads on momentum, as it should, and **negatively on short-term reversal** in every JKP universe: US -1.21 (t -4.0), UK -1.07 (t -4.2), DK -0.38 (t -2.4), World -1.02 (t -2.0); significant (|t| ≥ 2) in US, UK, DK, World. Entering the day after a breakout means buying last week's winners and shorting last week's losers, which is exactly the trade that one-month reversal (Jegadeesh 1990) punishes in single stocks. Futures markets do not have that reversal, which is one reason the rules worked there.

## 9. Statistical verdict

- **Gate.** 12 strategy × universe cells across the two factsheets; Bonferroni two-sided 0.05/12 gives |t| > 2.87.
- **Long/short:** negative Sharpe in 6 of 6. The negative factor alphas are significant in several universes, so this is evidence the rule *loses*, not just that it fails to win.
- **Long-only:** higher Sharpe than the equal-weight universe in 0 of 6; alpha vs the universe passes the gate in 0 of 6. Its appeal is a lower beta (0.53–0.65) and a shallower maximum drawdown than the universe in 4 of 6, not extra return. Results lean on a few trades: single positions such as Abivax (ABVX.PA, the verified +561% trial-result week in 2025) or Rheinmetall can make a year.
- **Index version:** Sharpe between -0.24 and 0.29. Small either way: timing the index with breakouts does not add value in a 13-year bull market, the same result as A11 *A Beautiful Mind* for moving-average rules.
- **Probabilistic Sharpe** (Bailey & López de Prado 2012), P(true Sharpe > 0): L/S US 0.00, EU 0.05, UK 0.03, DK 0.18, SCANDI 0.00, World 0.00.

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

**2. The short side does all the damage.** Summed trade P&L a year, 2013–2019: short trades -46% to -22% of equity, long trades +3% to +23%. Shorting single stocks in markets rising 10–15% a year, with no stock-specific edge (point 4), loses roughly the market return on the short book.

**3. The 2N stop is too tight for single stocks.** 73–78% of trades end on the 2N stop, and their summed P&L is -93% to -51% of equity a year (summed across trades, not compounded); trades that reach the channel exit sum to +38% to +77%. With a close-to-close N, 2N is only about 2% below the entry, a move the median large cap makes every few days, so the stop harvests noise and multiplies trading.

**4. There is no trend to follow in single stocks at these horizons.** After a fresh 55-day breakout, the stock's return *in excess of its universe* is small and mostly insignificant at every horizon, and where it is significant it is as often negative as positive (t-statistics in brackets):

| Universe | Long: t+1 | t+2..5 | t+6..20 | t+21..60 | Short: t+2..5 | t+6..20 |
|---|---|---|---|---|---|---|
| US | -0.00% (-0.2) | -0.02% (-1.0) | -0.08% (-2.4) | -0.04% (-0.8) | -0.04% (-1.2) | +0.10% (1.8) |
| EU | +0.05% (3.3) | -0.01% (-0.4) | +0.06% (1.0) | +0.08% (0.9) | -0.04% (-0.8) | +0.05% (0.6) |
| UK | -0.04% (-2.0) | +0.01% (0.3) | -0.16% (-2.8) | +0.18% (1.7) | +0.02% (0.3) | +0.05% (0.5) |
| DK | -0.09% (-1.3) | +0.22% (2.1) | +0.09% (0.4) | +0.52% (1.5) | -0.12% (-0.7) | +0.07% (0.2) |
| SCANDI | -0.01% (-0.2) | +0.04% (0.7) | +0.06% (0.6) | +0.08% (0.5) | +0.04% (0.4) | +0.02% (0.1) |
| World | -0.04% (-5.6) | -0.04% (-2.9) | -0.04% (-1.4) | +0.06% (1.5) | +0.09% (4.0) | +0.04% (1.0) |

Variance ratios (Lo & MacKinlay 1988) say the same thing: the median single stock has VR(20) = 0.86 and VR(60) = 0.79, net of the market 0.90 and 0.84. Values below 1 mean mild mean reversion, not trend. Breakout rules need VR > 1 (Figure 4, panel C). This is the root cause, and no parameter inside the rulebook can create a trend that is not in the data.

**5. Not the culprit: the one-day fill lag.** The fill-day column (t+1) is a few basis points either way (largest 0.09%), so waiting for the next close costs next to nothing. A "confirmation delay" fix I had coded was dropped before testing, because the diagnosis gave it nothing to fix.

![Diagnosis](../figures/fs01_fig4_diagnosis.png)

### 10.2 The fixes, one step at a time

T0 → T1 drop the shorts (point 2) → T2 keep System 2 only, fewer and longer trades (point 1) → T3 widen the stop from 2N to 4N (point 3) → T4 add a market trend filter: only take new longs when the universe index's 25-day EMA is above its 350-day EMA, a filter of the kind Faith (2007) tests.

| Step | Design Sharpe (avg of 6) | Δ vs previous, design (p) | Holdout Sharpe (6-universe book) | Δ vs previous, holdout (p) | Holdout: universes improved | Holdout return / yr | Holdout max DD | Alpha vs EW / yr (t) | Beta |
|---|---|---|---|---|---|---|---|---|---|
| T0 baseline L/S | -0.81 | – | -0.74 | – | – | -9.6% | -56% | -5.0% (-1.1) | -0.37 |
| T1 long-only | 0.40 | +1.75 (p 0.001) | 0.46 | +1.20 (p 0.008) | 6 of 6 | +5.2% | -21% | -1.2% (-0.4) | 0.51 |
| T2 + System 2 only | 0.53 | +0.27 (p 0.015) | 0.46 | +0.01 (p 0.470) | 3 of 6 | +5.4% | -20% | -0.5% (-0.2) | 0.47 |
| T3 + 4N stop | 0.57 | -0.00 (p 0.489) | 0.64 | +0.17 (p 0.135) | 4 of 6 | +8.4% | -24% | +1.9% (0.5) | 0.52 |
| T4 + market trend filter | 0.45 | -0.17 (p 0.902) | 0.72 | +0.09 (p 0.342) | 3 of 6 | +9.2% | -18% | +4.3% (1.1) | 0.39 |
| *EW universe (reference)* |  |  | 0.75 |  |  | +12.5% | -25% | – | 1.00 |

*✔ = passes the gate (p < 0.0071). Design Sharpe = average across the six universes; the Δ tests and the holdout columns use the six-universe equal-weighted book. Alpha and beta vs the six-universe equal-weight benchmark, Newey-West t.*

**Per universe, Sharpe design / holdout**

| Universe | T0 | T1 | T2 | T3 | T4 |
|---|---|---|---|---|---|
| US | -1.54 / -0.48 | 0.09 / 0.40 | 0.34 / 0.25 | 0.37 / 0.77 | 0.00 / 0.82 |
| EU | -0.91 / -0.02 | 0.45 / 0.42 | 0.47 / 0.53 | 0.47 / 0.31 | 0.38 / 0.31 |
| UK | -0.24 / -0.82 | 0.88 / 0.19 | 1.14 / 0.09 | 1.20 / 0.38 | 1.00 / 0.57 |
| DK | -0.48 / -0.05 | 0.21 / 0.29 | 0.31 / 0.36 | 0.50 / 0.16 | 0.47 / -0.04 |
| SCANDI | -1.13 / -0.58 | 0.25 / 0.22 | 0.34 / 0.14 | 0.29 / 0.25 | 0.33 / 0.33 |
| World | -0.58 / -0.98 | 0.54 / 0.44 | 0.57 / 0.49 | 0.60 / 0.62 | 0.52 / 0.57 |

![Fix ladder](../figures/fs01_fig5_fixes.png)

### 10.3 What the fixes achieve

- **Dropping the shorts is the big step:** design +1.75 (p 0.001, passes), holdout +1.20 (p 0.008, does not pass the gate).
- **System 2 only:** +0.27 design, +0.01 holdout. Fewer trades, no reliable gain.
- **The 4N stop:** -0.00 design, +0.17 holdout (p 0.13). Positive in both windows, too small to pass.
- **The market trend filter is not trustworthy:** +0.09 in the holdout but -0.17 in the design window. The market was in an up-trend 84–93% of the time, so the filter rarely binds, and its result rests on one or two episodes.
- **Where it ends:** T3 (long-only, System 2, 4N stop) has a holdout Sharpe of 0.64 against 0.75 for the equal-weight universe (difference -0.11, p 0.66) with a beta of about 0.52. T4 reaches 0.72 (-0.02 vs the universe, p 0.52).

**Bottom line.** The fixes remove self-inflicted damage (shorting a bull market, a stop tighter than daily noise, a cost bill from oversized units). What remains is a stop-protected, half-beta equity book, not an edge. The Turtle rules need assets that trend, which is why they were built for, and still work in, diversified futures (Moskowitz, Ooi & Pedersen 2012; Hurst, Ooi & Pedersen 2017). Recommended specification if you insist on stocks: **T3** (long-only, System 2, 4N stop; no market filter, because that filter failed in the design window), and judge it against a half-beta equal-weight portfolio, not against cash.

## 11. Classification: where does it fit?

Evidence: correlations of monthly returns with the 13 JKP factor themes (US, UK, DK, World) or the French Europe factors (EU, SCANDI), a Treynor–Mazuy regression r = a + b·m + γ·m² on the equal-weight universe (γ > 0 = convex, the trend-follower's signature), and returns in the worst and best 10% of market months.

| Dimension | Turtle Traders on stocks |
|---|---|
| Series family (Content_ver2 'Odd ideas') | **Breakout & trend** |
| Academic style | Trend following / time-series momentum (Moskowitz, Ooi & Pedersen 2012); Donchian (1960) breakout |
| Signal | Price only (technical); each stock against its own past, not ranked against other stocks |
| Cross-section vs time series | **Time series.** Position depends on the stock's own channel; the book's net exposure floats (L/S average net +1% to +27%) |
| Horizon and turnover | Medium term: winners held ~28 days, losers ~10; 464 trades a year; very high turnover |
| Trade-level payoff | Positively skewed: 23% winners, payoff ratio 2.8, roughly the best quarter of trades carries the book |
| Book-level payoff | No convexity on stocks: Treynor–Mazuy γ ranges -1.40 to +4.47 (t -1.6 to 3.8); futures trend books show a clear 'smile'. In the worst 10% of market months the L/S earns -0.3% to +3.0% a month: a weak hedge, not crisis alpha |
| Nearest JKP theme (L/S) | **Momentum** (correlation 0.24 to 0.33); low risk 0.07 to 0.45 |
| Nearest theme (long-only, T3) | **Market beta**: correlation with the market 0.38 to 0.58, *negative* with low risk (-0.36 to -0.23): breakouts select volatile stocks |
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
| Price / prior 55-day high | target: the cross-sectional breakout | +1.00 | +1.00 | +0.7% | +5.6% to +12.6% | 3 / 0 |
| Price / 52-week high | lookalike: near the 52-week high | +0.74 | +0.83 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| Last month's return | lookalike: last month's winner | +0.68 | +0.69 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Momentum 12-1 | cousin: slow momentum | +0.19 | +0.54 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Price / 52-week low | mirror: at the 52-week low (short breakout) | +0.35 | +0.40 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| MIN (worst day) | cousin: no crash lately | +0.54 | +0.71 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| MAX (best day) | cousin: lottery | -0.03 | -0.42 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| Volatility (63 days) | lookalike (inverse): calm stocks | -0.37 | -0.65 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Beta (252 days) | lookalike (inverse): low beta | -0.22 | -0.56 | +5.5% | -15.7% to -2.6% | 0 / 3 |

![360 map](../figures/nbh_brk_map.png)

**What a breakout selects.** Stocks at a 55-day high are last month's winners (rank corr with last month's return +0.68), close to their 52-week high (+0.74), calm rather than volatile (-0.37 with volatility) and without recent crashes (+0.54 with MIN). It is *not* the lottery signal (-0.03 with MAX).

**Is there information?** Yes, once beta is removed: the breakout sort has a CAPM alpha of +5.6% to +12.6% (t ≥ 2 in 3 of 6), because breakout stocks are low-beta and the raw spread is dragged down in a bull market. But it is a weaker copy of its neighbours: nearness to the 52-week high earns +8.3% to +18.8% (t ≥ 2 in 6) and 12-1 momentum +3.9% to +17.8% (t ≥ 2 in 5).

**Spanning.** Against momentum, the 52-week high, last month's return, volatility, MAX and the market, the breakout sort keeps an alpha of -3.0% to +4.8% (|t| ≤ 1.5), with R² 0.64 to 0.93. **The breakout is redundant given the 52-week high and one-month return.**

| Universe | Breakout alpha after neighbours / yr | t | R² | Neighbours with |t| ≥ 2 (loading, t) |
|---|---|---|---|---|
| US | -0.0% | -0.02 | 0.91 | Momentum 12-1 -0.16 (-3.6), Price / 52-week high +0.61 (+8.2), Last month's return +0.41 (+11.5) |
| EU | -3.0% | -1.20 | 0.82 | Momentum 12-1 -0.14 (-3.0), Price / 52-week high +0.63 (+7.1), Last month's return +0.32 (+5.8) |
| UK | +0.4% | 0.15 | 0.89 | Price / 52-week high +0.60 (+9.2), Last month's return +0.41 (+7.6) |
| DK | +4.8% | 1.52 | 0.64 | Price / 52-week high +0.34 (+3.4), Last month's return +0.57 (+5.3), Volatility -0.33 (-4.8) |
| SCANDI | +1.9% | 0.96 | 0.71 | Price / 52-week high +0.55 (+9.8), Last month's return +0.37 (+8.0) |
| World | -1.0% | -0.76 | 0.93 | Momentum 12-1 -0.18 (-4.4), Price / 52-week high +0.70 (+10.0), Last month's return +0.37 (+7.2) |

![Double sort](../figures/nbh_brk_dsort.png)

**Mirror.** The short-side mirror, a stock at its 52-week low, is the stronger signal: holding the breakout fixed, stocks far above their 52-week low out-earn stocks at the low by +6.1, +6.3 and +3.9 points a year, while the breakout adds little within each column. That is consistent with §10: the Turtle's short breakouts lost because the stock was high-beta in a rising market, not because the cross-sectional information pointed the wrong way.

**Verdict of the 360° view.** The breakout carries real, beta-adjusted information, but it is a noisy subset of the 52-week-high and momentum effects (George & Hwang 2004; Jegadeesh & Titman 1993). The Turtle rules waste it through time-series execution, stops and shorts (§10). For the factor battery, FS09 (52-week high) and FS03 (momentum) are the signals to carry forward, not the breakout itself.

## 13. Caveats

1. **Survivorship: fixed as far as the data allow.** The first edition of this factsheet used today's index members outside the US. This edition uses point-in-time membership everywhere (§3). The table shows the change, same code, same period (survivor list → point-in-time). Note that the universes also changed definition (national blue-chip indices instead of STOXX 600), so the difference is survivorship plus composition.

| Universe | EW universe CAGR | L/S Sharpe | Long-only Sharpe | Long-only alpha vs EW |
|---|---|---|---|---|
| EU | +14.5% → +11.4% | -0.91 → -0.47 | 0.66 → 0.44 | +1.8% → -0.7% |
| UK | +13.1% → +10.3% | -0.45 → -0.53 | 0.72 → 0.49 | +2.7% → -0.1% |
| DK | +18.2% → +13.1% | -0.21 → -0.25 | 0.44 → 0.25 | -4.5% → -3.8% |
| SCANDI | +15.8% → +13.4% | -0.69 → -0.83 | 0.39 → 0.23 | -3.4% → -4.4% |
| World | +16.8% → +13.6% | -0.96 → -0.79 | 0.80 → 0.48 | +1.3% → -2.0% |

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
