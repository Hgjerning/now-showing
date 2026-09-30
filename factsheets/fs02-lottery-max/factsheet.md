# FACTSHEET FS02 · The lottery factor (MAX)

### Do investors overpay for stocks that just had one huge day? Six universes, 2013–2026

*Henrik Gjerning · Rude Investment Consulting · Project 10 sidebar: strategy factsheets · data to 31 August 2026*

<div class="kf" markdown="0">
<div><b>Strategy</b>Buy low-MAX, sell high-MAX stocks</div>
<div><b>Origin</b>Bali, Cakici & Whitelaw (2011), JFE</div>
<div><b>Signal</b>Largest daily return in the past month</div>
<div><b>Universes</b>US · EU · UK · DK · SCANDI · World</div>
<div><b>Backtest</b>Feb 2013 – Aug 2026, 163 months, net of costs</div>
<div><b>Books</b>Long/short (headline) and low-MAX long-only</div>
<div><b>Rebalance</b>Monthly, equal-weighted</div>
<div><b>Status</b>Descriptive factsheet, not a registered trial</div>
</div>

> **Verdict in one paragraph.** Bali, Cakici & Whitelaw found that US stocks with the largest one-day jump last month earned about 1% a month *less* the next month, in 1962–2005. Investors pay up for lottery tickets. In 2013–2026 the effect is gone: **after costs the long/short lost money in all six universes** (-14.4% to -1.6% a year); before costs it was slightly positive only in EU, UK, SCANDI, and clearly negative in the US and World, where the lottery stocks won. The reason is beta. The high-MAX group has a beta of 1.17–1.34 against the universe, the low-MAX group 0.65–0.82, and markets rose strongly. Adjusted for that one number, the CAPM alpha of the long/short is between -5.5% and +4.7% a year and passes the gate in 0 of 6. The low-MAX long-only book delivered what low-risk investing promises: a beta of 0.65–0.82, a shallower drawdown than the universe in 6 of 6, a higher Sharpe in 2 of 6 (EU, UK), and alphas of -1.4% to +3.2% that do not pass the gate. **What goes wrong (§10):** an unhedged beta bet plus a signal that, in large caps, mostly measures volatility. Beta-neutral legs remove most of the loss in both the design and the 2020–26 holdout window, and what remains is a premium of about zero. **Classification (§11):** a member of the low-risk family, not a factor of its own. **360° view (§12):** lottery and falling knife are the two tails of the same volatility, mirrors in their returns but not in the stocks they pick; neither tail is priced on its own once volatility and beta are in the model, and MAX is fully spanned by its neighbours.

## 1. Headline performance

| Universe | Names / groups | L/S return / yr | L/S t | L/S CAPM alpha (t) | L/S beta | Low-MAX CAGR | Low-MAX Sharpe | Low-MAX max DD | EW CAGR | EW Sharpe | EW max DD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | 503 / 10 | -14.4% | -2.75 | -5.5% (-1.3) | -0.62 | +9.6% | 0.80 | -18% | +14.2% | 0.96 | -25% |
| EU | 238 / 10 | -1.6% | -0.41 | +4.7% (1.5) | -0.55 | +9.4% | 0.85 | -23% | +10.9% | 0.79 | -26% |
| UK | 242 / 10 | -3.6% | -0.77 | +2.5% (0.6) | -0.57 | +9.9% | 0.95 | -22% | +9.9% | 0.74 | -30% |
| DK | 19 / 3 | -4.6% | -1.15 | -0.2% (-0.1) | -0.34 | +8.3% | 0.61 | -26% | +12.3% | 0.82 | -33% |
| SCANDI | 62 / 5 | -2.4% | -0.67 | +2.9% (0.9) | -0.41 | +8.7% | 0.73 | -26% | +12.5% | 0.90 | -29% |
| World | 975 / 10 | -9.8% | -2.54 | -2.8% (-1.0) | -0.56 | +7.9% | 0.70 | -22% | +12.0% | 0.80 | -29% |

*Monthly, local currency (World in USD). L/S = equal-weighted lowest-MAX group minus highest-MAX group, net of 10 bp per side on turnover and a size-tiered borrow fee on the high-MAX leg. Newey-West t (6 lags). CAPM alpha and beta against the equal-weight universe. Metrics from Project1 InvestmentLibrary where applicable.*

![Growth](../figures/fs02_fig1_growth.png)

## 2. Strategy description

**The idea.** Many investors like lottery-like payoffs: a small chance of a very large gain. Cumulative prospect theory predicts that people overweight small probabilities (Tversky & Kahneman 1992). Barberis & Huang (2008) show that this makes positively skewed stocks overpriced, so they earn low future returns. Kumar (2009) documents that retail investors tilt towards lottery-type stocks. Bali, Cakici & Whitelaw (2011) proposed the simplest proxy for "lottery-ness": **MAX, the largest daily return in the previous month.** In US data 1962–2005 the highest-MAX decile underperformed the lowest by over 1% a month, value-weighted, and the effect subsumed idiosyncratic volatility (Ang et al. 2006). European evidence followed (Annaert, De Ceuster & Verstegen 2013; Walkshäusl 2014). Bali, Brown, Murray & Tang (2017) argue that lottery demand explains the beta anomaly (Frazzini & Pedersen 2014), which is why beta sits at the centre of this factsheet.

**The trade.** Each month-end, rank stocks by MAX, buy the calmest group, sell the most lottery-like group, hold one month.

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

Same cleaning as FS01: the five verified corrupt series are dropped and daily moves beyond ±100% are removed unless verified real. This matters more here than anywhere else, because a single bad print *is* a MAX signal.

## 4. Factor creation

For stock *i* in month *t*, with *r<sub>i,d</sub>* the daily total return:

- **MAX1<sub>i,t</sub> = max<sub>d∈t</sub> r<sub>i,d</sub>**, requiring at least 15 valid days in the month
- **MAX5<sub>i,t</sub>** = mean of the five largest daily returns (robustness, Bali et al.'s alternative)
- Eligible: in the universe at month-end *t* (US point-in-time top 500; others survivor list, ≥ 252 days of history)
- Sort into equal-count groups: **deciles** with ≥ 100 names (US, EU, UK, World), **quintiles** with 50–99 (SCANDI), **terciles** below 50 (DK). The number of groups is fixed per universe for the whole sample.

Average MAX in the extreme groups: US 1.5% vs 8.9%, EU 1.4% vs 8.5%, UK 1.3% vs 9.4%, DK 2.2% vs 6.2%, SCANDI 1.8% vs 6.8%, World 1.5% vs 9.1%.

## 5. Model build

- Equal-weighted groups, formed at month-end *t*, held through month *t+1* (compounded daily total returns; a stock that stops trading earns its return up to its last price).
- **Long/short** = group 1 − last group. **Long-only** = group 1. **Benchmark** = equal-weighted universe, same month.
- **Costs:** 10 bp per side × one-way turnover of each leg. Average monthly one-way turnover: low-MAX US 76%, EU 74%, UK 64%, DK 52%, SCANDI 68%, World 74%; the high-MAX leg turns over about as much. Cost drag on the L/S: US 4.4%, EU 4.5%, UK 4.1%, DK 3.2%, SCANDI 4.1%, World 4.4% a year.
- **Robustness books:** MAX5 signal; US value-weighted (Sharadar market caps), which is closest to the original paper.
- Code: `code/lottery.py` (portfolio build), `run_lottery.py`, `analyse.py lottery`.

## 6. Performance in detail

**US (top 500, point-in-time)**, median 503 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S low − high MAX (net) | -14.4% | -14.9% | 17.8% | -0.81 [-1.33, -0.26] | -0.95 | -90% | 40% | -2.75 | -0.62 | -5.5% (-1.3) | 14.6% |
| L/S MAX5 (net) | -14.8% | -15.8% | 20.9% | -0.71 [-1.26, -0.14] | -0.88 | -91% | 42% | -2.41 | -0.70 | -4.7% (-0.9) | 16.1% |
| L/S value-weighted (net) | -15.1% | -16.2% | 21.5% | -0.71 [-1.25, -0.20] | -0.90 | -93% | 42% | -2.64 | -0.51 | -7.8% (-1.4) | 16.9% |
| Low-MAX long-only (net) | +9.9% | +9.6% | 12.5% | 0.80 [0.38, 1.26] | 1.24 | -18% | 65% | 4.07 | 0.72 | -0.5% (-0.3) | 7.2% |
| High-MAX group (gross) | +21.7% | +21.0% | 22.9% | 0.95 [0.46, 1.50] | 1.67 | -31% | 62% | 3.81 | 1.34 | +2.4% (0.8) | 12.2% |
| EW universe | +14.5% | +14.2% | 15.1% | 0.96 [0.52, 1.53] | 1.52 | -25% | 67% | 4.79 | 1.00 | – | 8.9% |

**EU (11 national blue-chip indices, point-in-time)**, median 238 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S low − high MAX (net) | -1.6% | -2.6% | 14.4% | -0.11 [-0.63, 0.42] | -0.24 | -44% | 47% | -0.41 | -0.55 | +4.7% (1.5) | 9.0% |
| L/S MAX5 (net) | -4.2% | -5.4% | 15.8% | -0.27 [-0.84, 0.29] | -0.44 | -60% | 47% | -0.98 | -0.61 | +2.7% (0.8) | 10.3% |
| Low-MAX long-only (net) | +9.6% | +9.4% | 11.3% | 0.85 [0.41, 1.40] | 1.30 | -23% | 63% | 4.18 | 0.66 | +2.1% (1.3) | 7.2% |
| High-MAX group (gross) | +8.5% | +6.8% | 19.5% | 0.44 [-0.03, 0.94] | 0.57 | -39% | 54% | 1.78 | 1.21 | -5.3% (-2.4) | 10.4% |
| EW universe | +11.4% | +10.9% | 14.5% | 0.79 [0.33, 1.33] | 1.22 | -26% | 64% | 3.35 | 1.00 | – | 8.3% |

**UK (FTSE 350, point-in-time)**, median 242 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S low − high MAX (net) | -3.6% | -4.7% | 15.5% | -0.23 [-0.83, 0.33] | -0.40 | -62% | 46% | -0.77 | -0.57 | +2.5% (0.6) | 10.5% |
| L/S MAX5 (net) | -3.5% | -5.0% | 17.8% | -0.20 [-0.79, 0.33] | -0.38 | -61% | 50% | -0.71 | -0.74 | +4.3% (1.0) | 11.5% |
| Low-MAX long-only (net) | +10.1% | +9.9% | 10.6% | 0.95 [0.50, 1.53] | 1.50 | -22% | 65% | 5.12 | 0.65 | +3.2% (2.3) | 6.5% |
| High-MAX group (gross) | +11.1% | +9.3% | 20.6% | 0.54 [0.03, 1.14] | 0.71 | -37% | 58% | 2.03 | 1.23 | -1.9% (-0.6) | 11.8% |
| EW universe | +10.5% | +9.9% | 14.2% | 0.74 [0.26, 1.35] | 1.08 | -30% | 59% | 3.24 | 1.00 | – | 8.8% |

**DK (OMXC25, point-in-time)**, median 19 names, 3 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S low − high MAX (net) | -4.6% | -5.8% | 16.5% | -0.28 [-0.82, 0.21] | -0.47 | -55% | 47% | -1.15 | -0.34 | -0.2% (-0.1) | 10.1% |
| L/S MAX5 (net) | -4.2% | -5.5% | 17.3% | -0.24 [-0.87, 0.32] | -0.43 | -63% | 47% | -0.88 | -0.40 | +1.0% (0.3) | 10.9% |
| Low-MAX long-only (net) | +9.2% | +8.3% | 15.0% | 0.61 [0.18, 1.14] | 0.82 | -26% | 61% | 2.78 | 0.82 | -1.4% (-0.8) | 9.2% |
| High-MAX group (gross) | +11.7% | +10.0% | 20.9% | 0.56 [0.02, 1.20] | 0.79 | -43% | 56% | 2.09 | 1.17 | -3.3% (-1.3) | 12.5% |
| EW universe | +12.9% | +12.3% | 15.6% | 0.82 [0.30, 1.44] | 1.26 | -33% | 64% | 3.21 | 1.00 | – | 9.3% |

**SCANDI (OMXC25 + OMXS30 + OMXH25, point-in-time)**, median 62 names, 5 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S low − high MAX (net) | -2.4% | -3.3% | 13.2% | -0.18 [-0.73, 0.35] | -0.33 | -44% | 45% | -0.67 | -0.41 | +2.9% (0.9) | 8.4% |
| L/S MAX5 (net) | -0.3% | -1.3% | 13.8% | -0.02 [-0.55, 0.49] | -0.13 | -36% | 48% | -0.09 | -0.45 | +5.4% (1.6) | 8.7% |
| Low-MAX long-only (net) | +9.1% | +8.7% | 12.4% | 0.73 [0.24, 1.27] | 1.14 | -26% | 62% | 2.96 | 0.77 | -0.7% (-0.5) | 6.7% |
| High-MAX group (gross) | +9.1% | +7.6% | 18.7% | 0.49 [-0.03, 1.08] | 0.64 | -44% | 56% | 1.84 | 1.18 | -6.1% (-2.7) | 11.6% |
| EW universe | +12.8% | +12.5% | 14.2% | 0.90 [0.38, 1.54] | 1.41 | -29% | 68% | 3.59 | 1.00 | – | 8.5% |

**World (US + UK + EU, point-in-time)**, median 975 names, 10 groups

| Book | Mean / yr | CAGR | Vol | Sharpe [95% CI] | Sortino | Max DD | Hit | t(mean) | Beta | Alpha/yr (t) | CVaR 95% (month) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L/S low − high MAX (net) | -9.8% | -10.3% | 14.3% | -0.69 [-1.22, -0.16] | -0.85 | -79% | 44% | -2.54 | -0.56 | -2.8% (-1.0) | 11.1% |
| L/S MAX5 (net) | -10.8% | -11.6% | 16.8% | -0.64 [-1.16, -0.11] | -0.81 | -83% | 44% | -2.37 | -0.63 | -2.8% (-0.8) | 13.0% |
| Low-MAX long-only (net) | +8.4% | +7.9% | 12.0% | 0.70 [0.30, 1.19] | 1.00 | -22% | 66% | 3.77 | 0.70 | -0.4% (-0.4) | 7.6% |
| High-MAX group (gross) | +15.6% | +14.2% | 21.2% | 0.73 [0.25, 1.29] | 1.14 | -36% | 58% | 3.04 | 1.26 | -0.3% (-0.2) | 11.8% |
| EW universe | +12.6% | +12.0% | 15.7% | 0.80 [0.34, 1.38] | 1.20 | -29% | 64% | 3.54 | 1.00 | – | 9.4% |

*Sharpe CI: stationary bootstrap, mean block 6 months, 5,000 draws. Max drawdown on monthly returns. The equal-weight universe here is rebalanced monthly, so its figures differ slightly from FS01's daily-rebalanced version.*

![Quantiles](../figures/fs02_fig3_quantiles.png)

![Beta](../figures/fs02_fig4_beta.png)

The beta chart is the whole story in one picture: across 48 MAX groups in six universes, average return rises with beta, and the lottery groups sit at the top right simply because they carry the most market risk.

![Drawdowns](../figures/fs02_fig2_drawdown.png)

**Calendar-year returns, L/S low − high MAX (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | -15.9% | -22.0% | -3.6% | -33.5% | -23.6% | -13.4% |
| 2014 | -7.0% | +25.5% | +10.3% | -12.0% | -0.6% | +1.0% |
| 2015 | +4.8% | +2.1% | +30.1% | -8.2% | -0.2% | +8.4% |
| 2016 | -0.2% | -15.2% | -36.3% | -13.9% | -9.3% | -17.0% |
| 2017 | -5.2% | -4.0% | -13.3% | -1.0% | -10.3% | -9.1% |
| 2018 | -1.6% | +14.1% | -3.7% | -4.9% | +1.6% | +0.8% |
| 2019 | -3.8% | +4.1% | +3.7% | +18.6% | +4.1% | -4.0% |
| 2020 | -34.5% | -0.6% | +9.5% | -5.0% | -4.8% | -19.3% |
| 2021 | -6.7% | +3.2% | -12.2% | +0.7% | +12.6% | -4.4% |
| 2022 | +13.8% | +0.7% | +11.5% | +4.0% | +3.2% | +13.2% |
| 2023 | -28.7% | -20.3% | +0.5% | -8.2% | -14.5% | -21.5% |
| 2024 | -14.7% | +11.1% | -9.6% | +0.8% | +24.9% | -10.1% |
| 2025 | -44.2% | -17.0% | -4.9% | +16.1% | -7.3% | -28.2% |
| 2026 | -35.9% | -4.8% | -26.0% | -19.3% | -10.6% | -25.7% |

**Calendar-year returns, low-MAX long-only (net)**

| Year | US | EU | UK | DK | SCANDI | World |
|---|---|---|---|---|---|---|
| 2013 | +18.8% | +11.4% | +12.8% | +13.6% | +14.3% | +17.4% |
| 2014 | +15.5% | +13.6% | +11.8% | +10.4% | +12.0% | +9.9% |
| 2015 | -1.4% | +13.1% | +15.5% | +22.2% | +6.3% | +3.4% |
| 2016 | +13.8% | +4.9% | +17.8% | -2.8% | +12.7% | +3.7% |
| 2017 | +18.1% | +11.0% | +16.4% | +20.0% | +10.3% | +20.8% |
| 2018 | -5.7% | +1.6% | -1.5% | -10.7% | -10.2% | -6.9% |
| 2019 | +30.5% | +25.1% | +29.4% | +20.9% | +29.9% | +25.7% |
| 2020 | +10.2% | +1.0% | +4.8% | +21.4% | +12.9% | +6.7% |
| 2021 | +25.9% | +12.4% | +12.7% | +19.2% | +21.7% | +13.5% |
| 2022 | -6.4% | -4.4% | -7.9% | -12.0% | -13.2% | -8.3% |
| 2023 | +4.1% | +8.3% | +8.6% | +3.7% | -3.6% | +7.8% |
| 2024 | +12.4% | +9.9% | +5.7% | +2.3% | +10.9% | +6.4% |
| 2025 | -4.1% | +12.3% | +11.9% | +9.4% | +12.9% | +9.1% |
| 2026 | +6.1% | +9.9% | +1.4% | +3.7% | +9.0% | +3.9% |

## 7. Trading record

A factor has no discrete trades; its record is the monthly rebalance log, `results/lottery_monthly_record_<universe>.csv` (names, average MAX per leg, turnover, leg returns, gross and net L/S).

| Universe | Rebalances | Names | Names per leg | Turnover low leg | Turnover high leg | L/S months positive | Worst L/S month | When | L/S during the 2020–21 retail boom / yr |
|---|---|---|---|---|---|---|---|---|---|
| US | 163 | 503 | 50 | 76% | 75% | 40% | -19.6% | 2026-04 | -32.5% |
| EU | 163 | 238 | 24 | 74% | 76% | 47% | -17.9% | 2020-11 | -4.5% |
| UK | 163 | 242 | 24 | 64% | 76% | 46% | -18.5% | 2020-11 | -5.2% |
| DK | 163 | 19 | 6 | 52% | 56% | 47% | -13.9% | 2023-11 | -1.0% |
| SCANDI | 163 | 62 | 12 | 68% | 70% | 45% | -15.7% | 2022-10 | -2.2% |
| World | 163 | 975 | 98 | 74% | 76% | 44% | -17.5% | 2020-11 | -19.7% |

**Current book** (formed on 31 August 2026 for September; first 8 names per leg, sorted by MAX)

| Universe | Long: calmest (lowest MAX) | Short: most lottery-like (highest MAX) |
|---|---|---|
| US | AES, TECH, CMS, AEP, KIM, AEE, PNC, PNW | MRNA, PLTR, ZBRA, CRM, CRWD, SMCI, WDAY, ABNB |
| EU | IVG.MI, ENG.MC, BRS.WA, TRYG.CO, DANSKE.CO, SHB-A.ST, OBEL.BR, LOG.MC | QTCOM.HE, VWS.CO, ADYEN.AS, AGFB.BR, TESB.BR, NSIS-B.CO, NOKIA.HE, MAERSK-B.CO |
| DK | TRYG.CO, DANSKE.CO, NDA-DK.CO, CARL-B.CO, JYSK.CO, RBREW.CO, DEMANT.CO, DSV.CO | VWS.CO, NSIS-B.CO, MAERSK-B.CO, BAVA.CO, MAERSK-A.CO, PNDORA.CO, GMAB.CO, AMBU-B.CO |
| SCANDI | TRYG.CO, DANSKE.CO, SHB-A.ST, SEB-A.ST, KESKOB.HE, SAMPO.HE, NDA-FI.HE, LIFCO-B.ST | QTCOM.HE, VWS.CO, NSIS-B.CO, NOKIA.HE, MAERSK-B.CO, BAVA.CO, NIBE-B.ST, MAERSK-A.CO |

## 8. Risk and factor attribution

Same factor sets as FS01: JKP 7 themes (market, size, value, momentum, low risk, quality, short-term reversal) for US, UK, DK and World; French Europe 5 factors + WML for EU and SCANDI. Newey-West t, 6 lags. JKP's own `rmax1_21d` factor (the MAX factor itself) sits inside the low-risk theme.

**L/S low − high MAX**

| Universe | Factor model | Months | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|---|
| US | JKP USA 7 themes | 155 | -11.2% | -6.84 | 0.83 | size +0.29 (+2.3), value -0.27 (-3.9), low_risk +1.47 (+14.6), short_term_reversal +0.87 (+4.9) |
| EU | French Europe 5F + WML | 162 | -3.4% | -0.93 | 0.40 | Mkt-RF -0.33 (-4.3), RMW +0.83 (+2.4), WML +0.32 (+2.4) |
| UK | JKP GBR 7 themes | 155 | -3.1% | -0.85 | 0.57 | low_risk +1.39 (+5.9), short_term_reversal +0.51 (+2.7) |
| DK | JKP DNK 7 themes | 155 | -1.5% | -0.49 | 0.52 | size -0.24 (-2.1), value +0.22 (+2.8), low_risk +1.11 (+6.8), short_term_reversal +0.66 (+5.4) |
| SCANDI | French Europe 5F + WML | 162 | -2.3% | -0.64 | 0.19 | Mkt-RF -0.28 (-4.3) |
| World | JKP World 7 themes | 155 | -10.5% | -4.42 | 0.63 | momentum +0.41 (+3.1), low_risk +1.11 (+8.1) |

**Low-MAX long-only**

| Universe | Factor model | Months | Alpha / yr | t(alpha) | R² | Loadings with &#124;t&#124; ≥ 2 (t) |
|---|---|---|---|---|---|---|
| US | JKP USA 7 themes | 155 | +0.0% | 0.05 | 0.90 | mkt +0.92 (+35.2), size -0.17 (-3.0), momentum +0.16 (+3.0), low_risk +0.58 (+6.7), short_term_reversal +0.47 (+5.1) |
| EU | French Europe 5F + WML | 162 | +4.3% | 1.88 | 0.58 | Mkt-RF +0.54 (+8.5), RMW +0.46 (+2.7) |
| UK | JKP GBR 7 themes | 155 | +6.0% | 3.04 | 0.60 | mkt +0.41 (+8.8), quality +0.37 (+2.6), short_term_reversal +0.36 (+3.1) |
| DK | JKP DNK 7 themes | 155 | +2.9% | 1.12 | 0.65 | mkt +0.71 (+14.0), value +0.18 (+3.0), short_term_reversal +0.38 (+3.2) |
| SCANDI | French Europe 5F + WML | 162 | +5.0% | 1.89 | 0.49 | Mkt-RF +0.53 (+9.1), RMW +0.42 (+2.3) |
| World | JKP World 7 themes | 155 | +2.0% | 1.15 | 0.78 | mkt +0.68 (+16.6), momentum +0.20 (+3.1), low_risk +0.45 (+4.8) |

**Reading it.** Once beta is removed, most of the L/S loss disappears (CAPM alpha t between -1.3 and 1.5). The L/S is, above all, a low-risk position: its loading on JKP's low-risk theme is 1.11 to 1.47 with t up to 15. Where the JKP alpha is negative (US, UK, DK, World), the L/S earned less than that low-risk exposure would predict: net-of-cost, equal-weighted large-cap sorts are a costly way to hold low risk.

**The low-MAX long-only alphas need a warning.** Against the factor models it shows +2.0% to +6.0% a year outside the US (largest t 3.04, UK, which formally clears the gate). Against its own equal-weight universe, in the same currency, the alphas are smaller (-1.4% to +3.2%). The factor returns are in USD (JKP) or USD-based (French) while the book is in local currency, so I read the universe-relative alpha as the honest number.

## 9. Statistical verdict

- **Gate:** |t| > 2.87 (12 cells, Bonferroni 0.05/12, two-sided).
- **Raw L/S:** negative after costs in 6 of 6; before costs positive in 3 of 6. The US gross spread (-10.0% a year; -14.4% net, t -2.75) reproduces A15 *Viva Las Vegas* (A15-2: −9.2%/yr gross, t −1.93, same top-500 deciles on price returns).
- **CAPM alpha of the L/S:** -5.5% to +4.7%, passes in 0 of 6. Once beta is priced the anomaly is neither alive nor reversed: the raw result is a beta bet in disguise.
- **Low-MAX long-only:** alpha between -1.4% and +3.2% (largest t 2.34), none past the gate; beta 0.65–0.82.
- **Probabilistic Sharpe** of the L/S, P(true Sharpe > 0): US 0.00, EU 0.34, UK 0.20, DK 0.15, SCANDI 0.25, World 0.00.
- **Publication decay.** JKP's broad US MAX factor earned +4.0%/yr before 2006 (t 1.48) and +2.0%/yr in 2012–2025 (t 0.55), from A15. McLean & Pontiff (2016) predict roughly this post-publication shrinkage.

## 10. What goes wrong, and how to fix it

**Method.** As in FS01: diagnose on the design window (Feb 2013 – Dec 2019), fix in a pre-declared order, judge on the holdout (Jan 2020 – Aug 2026), one trial per step, pooled six-universe test of the Sharpe difference, gate p < 0.0071 (7 fix trials across both factsheets). The fixes stay inside the MAX strategy: they change how the two legs are sized, how MAX is measured, and how often names change, not what the strategy bets on.

### 10.1 Diagnosis: four things go wrong

**1. A hidden short on the market.** The L/S has a beta of about −0.6 because low-MAX stocks are low-beta and high-MAX stocks high-beta. With equal-weight universes rising 10–15% a year, beta alone costs -8.9% to -4.4% a year (beta × the universe's return), comparable to or larger than the raw loss (larger in EU, UK, SCANDI); §1 shows CAPM alphas within 5%. The original paper sorted on MAX without neutralising beta; in a 1962–2005 sample that averaged out, in a 13-year bull market it does not.

**2. MAX in large caps is mostly volatility.** The cross-sectional rank correlation of MAX with 60-day volatility is 0.52 to 0.69, and with beta 0.30 to 0.43 (table below). Among blue-chip stocks, a big up-day usually means a volatile stock or news (earnings, M&A), not a retail lottery ticket. The lottery premium lives in small, retail-held stocks (Kumar 2009; Bali et al. 2011), which these universes exclude by construction and which no fix inside them can bring back.

**3. Turnover.** The low leg turns over 52% to 76% a month and the high leg about as much, so costs take 3.2% to 4.5% a year.

**4. Waiting does not help.** The spread is no better, and mostly worse, two to six months after formation, so a longer holding period will not rescue it:

| Universe | L/S, month t+1 (ann.) | t+2..3 | t+4..6 | Rank corr MAX vs volatility | Rank corr MAX vs beta |
|---|---|---|---|---|---|
| US | +0.5% | -0.8% | -1.7% | 0.62 | 0.42 |
| EU | +4.8% | +2.1% | -1.1% | 0.62 | 0.36 |
| UK | +0.5% | -4.5% | -3.6% | 0.69 | 0.35 |
| DK | -4.4% | -4.9% | -3.5% | 0.55 | 0.43 |
| SCANDI | -0.1% | -5.3% | -2.1% | 0.52 | 0.30 |
| World | -0.4% | -1.3% | -1.3% | 0.65 | 0.37 |

*Design window, gross, equal-weighted extreme groups.*

### 10.2 The fixes, one step at a time

L0 baseline → L1 **beta-neutral legs**: each leg scaled by 1/its ex-ante 252-day beta, so the L/S has zero expected beta (the Frazzini & Pedersen 2014 construction; point 1) → L2 **vol-scaled MAX**: rank on MAX5 / 21-day volatility (JKP's `rmax5_rvol_21d`), lottery-ness net of plain volatility (point 2) → L3 **turnover buffer**: enter the extreme 1/q, keep a name until it leaves the extreme 3/q (point 3).

| Step | Design Sharpe (avg of 6) | Δ vs previous, design (p) | Holdout Sharpe (6-universe book) | Δ vs previous, holdout (p) | Holdout: universes improved | Holdout return / yr | Holdout max DD | t(mean) |
|---|---|---|---|---|---|---|---|---|
| L0 baseline | -0.33 | – | -0.57 | – | – | -7.9% | -50% | -1.53 |
| L1 beta-neutral | 0.24 | +0.82 (p 0.000) | -0.41 | +0.17 (p 0.248) | 6 of 6 | -4.3% | -36% | -1.27 |
| L2 + vol-scaled MAX | -0.06 | -0.40 (p 0.795) | -1.20 | -0.79 (p 0.968) | 1 of 6 | -12.8% | -63% | -3.38 |
| L3 + turnover buffer | -0.04 | +0.02 (p 0.381) | -0.99 | +0.22 (p 0.029) | 5 of 6 | -9.6% | -55% | -2.89 |

*Pooled test on the equal-weighted six-universe L/S. ✔ = passes p < 0.0071.*

**Per universe, Sharpe design / holdout**

| Universe | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| US | -0.38 / -1.13 | 0.40 / -1.04 | -0.08 / -0.78 | -0.08 / -0.79 |
| EU | -0.00 / -0.24 | 0.54 / 0.05 | -0.15 / -1.13 | -0.13 / -1.05 |
| UK | -0.22 / -0.31 | 0.60 / -0.13 | -0.09 / -0.65 | -0.16 / -0.45 |
| DK | -0.57 / 0.00 | -0.30 / 0.09 | 0.12 / -0.86 | 0.24 / -0.69 |
| SCANDI | -0.39 / 0.13 | -0.09 / 0.20 | 0.20 / -0.86 | 0.19 / -0.35 |
| World | -0.45 / -0.88 | 0.30 / -0.74 | -0.34 / -1.08 | -0.29 / -0.92 |

![Fix ladder](../figures/fs02_fig5_fixes.png)

### 10.3 What the fixes achieve

- **Beta-neutral legs are the real fix.** Sharpe +0.82 in the design window (p 0.0002, passes) and +0.17 in the holdout (p 0.248, does not pass the gate); better in 6 of 6 universes in the design window and 6 of 6 in the holdout. The fixed L/S earns -4.3% a year in the holdout (t -1.3): the beta drag is gone, and what is left is statistically zero.
- **Vol-scaled MAX failed out of sample.** It helped in 2 of 6 universes in the design window and hurt in 5 of 6 in the holdout (-0.79). once plain volatility is removed, large-cap lottery-ness carries no premium.
- **The turnover buffer** cuts costs from 4.4% to 3.4% a year (+0.02 design, +0.22 holdout, p 0.03), not significant.

**Bottom line.** What went wrong is not the idea but the packaging: an unhedged beta bet and a signal that, in large caps, measures volatility. Fixing the beta turns a -7.9%/yr loser (six-universe book, holdout) into a market-neutral book earning -4.3% (t -1.3), statistically zero. The lottery premium itself is not present in these universes after 2012. Recommended specification if you want the exposure: **L1 (beta-neutral) with the turnover buffer on the original MAX signal**. That exact combination was not in the pre-declared ladder, so I report it post hoc and count it as nothing: costs fall to 2.3% a year and the holdout L/S earns -2.1% (t -0.7, Sharpe -0.20 vs -0.41 for L1). Treat it as a defensive, low-risk tilt with an expected premium near zero; for a long-only investor, the low-MAX portfolio is a reasonable low-beta equity sleeve, not an alpha source.

## 11. Classification: where does it fit?

Evidence as in FS01: correlations with the JKP themes or French Europe factors, a Treynor–Mazuy convexity regression on the equal-weight universe, and behaviour in the worst and best 10% of market months.

| Dimension | Lottery factor (MAX) |
|---|---|
| Series family (Content_ver2 'Odd ideas') | **Lottery & attention** |
| Academic style | Low-risk / defensive anomaly (the family of betting-against-beta, low volatility, idiosyncratic volatility); behavioural origin in probability weighting |
| Signal | Price only: one statistic of last month's daily returns |
| Cross-section vs time series | **Cross-sectional**: stocks ranked against each other, always long one group and short another |
| Horizon and turnover | One month; 52% to 76% of the low leg replaced monthly; cost drag 3.2% to 4.5% a year |
| Market exposure | Beta -0.62 to -0.34 as published (low-MAX 0.65 to 0.82, high-MAX 1.17 to 1.34); zero by construction after fix L1 |
| Book-level payoff | **Concave**: Treynor–Mazuy γ -1.87 to -0.11 (t -5.4 to -0.1); earns +2.3% to +3.5% a month in the worst 10% of market months and loses -7.2% to -3.5% in the best 10%. A defensive profile: it pays in sell-offs and bleeds in rallies |
| Nearest JKP theme | **Low risk** (correlation 0.62 to 0.87; still 0.38 to 0.62 after beta-neutralising). Momentum 0.18 to 0.47 |
| Economic rationale | Behavioural: cumulative prospect theory and probability weighting (Tversky & Kahneman 1992; Barberis & Huang 2008), retail gambling demand (Kumar 2009). Constraint-based: leverage-constrained investors buy high-beta stocks (Frazzini & Pedersen 2014); Bali, Brown, Murray & Tang (2017) tie the two together |
| Where the premium lives | Small, illiquid, retail-held stocks; weak in the 500 largest US stocks and in large-cap Europe |
| Capacity and crowding | Large-cap version: high capacity, low premium. Low-risk ETFs and defensive funds hold the long leg in size |
| Publication | Bali, Cakici & Whitelaw 2011 (data to 2005); European evidence 2013–14; post-publication decay per McLean & Pontiff (2016) |
| Where it fits | **A member of the low-risk family, not a separate factor.** In large caps it is a noisier, costlier version of low volatility / betting-against-beta. It belongs in a defensive sleeve next to those, sized by its beta, and should be judged on beta-neutral terms |

![Classification map](../figures/fs_class_map.png)

On the map the MAX long/short sits high on the low-risk axis; beta-neutralising moves it toward the centre but keeps it in the defensive half. The Turtle books from FS01 sit in the opposite corner. The two strategies are close to mirror images: a breakout rule buys exactly the volatile, recently jumping stocks that the MAX rule sells.

## 12. 360° view: lottery, falling knife and everything in between

A factor is only understood next to its neighbours: the signals that pick the same stocks (lookalikes), the signal that should pick the opposite stocks (the mirror), the same idea at another speed (cousins), and the pieces it is made of (decomposition). MAX is the up-tail of last month's daily returns; its natural mirror is **MIN, the worst day**, which is the fast version of a *falling knife*. The slow version is a stock sitting at its 52-week low. This section tests all of them on the same six point-in-time universes, same months, same construction: equal-weighted top quantile minus bottom quantile, gross, Feb 2013 – Aug 2026 (`code/signals.py`, `code/neighbourhood.py`). Signs are raw: the MAX line is *most lottery-like minus calmest*, the MIN line is *mildest worst day minus deepest crash*, the 52-week-low line is *far above the low minus at the low*.

### 12.1 The neighbourhood in one table

| Signal (top minus bottom) | Role | Likeness to MAX (best day): stocks | Likeness: L/S returns | Raw L/S, avg of 6 | CAPM alpha range | Universes with alpha t ≥ +2 / ≤ −2 |
|---|---|---|---|---|---|---|
| MAX (best day) | target: the lottery signal | +1.00 | +1.00 | +1.9% | -9.3% to +1.0% | 0 / 2 |
| MAX5 (5 best days) | lookalike (robust MAX) | +0.89 | +0.90 | +2.6% | -8.5% to +0.4% | 0 / 2 |
| Skewness | lookalike: up-tail shape | +0.51 | +0.34 | -0.2% | -5.4% to +4.5% | 0 / 1 |
| Net tail (MAX + MIN) | decomposition: direction of the tails | +0.55 | +0.32 | -1.0% | -5.3% to +4.2% | 0 / 0 |
| Range (MAX − MIN) | decomposition: size of the tails | +0.79 | +0.88 | +1.2% | -11.3% to -2.3% | 0 / 4 |
| Idiosyncratic volatility | lookalike: stock-specific risk | +0.66 | +0.79 | -1.5% | -10.4% to -0.8% | 0 / 3 |
| Volatility (63 days) | lookalike: total risk | +0.62 | +0.82 | +3.0% | -10.3% to -3.7% | 0 / 5 |
| Beta (252 days) | lookalike: market risk | +0.39 | +0.70 | +5.5% | -15.7% to -2.6% | 0 / 3 |
| MIN (worst day) | mirror: the fast falling knife | -0.32 | -0.66 | -1.5% | +2.9% to +11.0% | 3 / 0 |
| MIN5 (5 worst days) | mirror (robust MIN) | -0.38 | -0.69 | -2.0% | +2.4% to +13.2% | 4 / 0 |
| Price / 52-week low | cousin: the slow falling knife | +0.24 | +0.17 | +8.8% | +4.4% to +13.8% | 4 / 0 |
| Price / 52-week high | cousin: anchoring to the high | -0.15 | -0.55 | +2.5% | +8.3% to +18.8% | 6 / 0 |
| Last month's return | cousin: one-month reversal | +0.33 | +0.01 | +0.9% | -3.2% to +8.4% | 0 / 0 |
| Momentum 12-1 | cousin: momentum | -0.09 | -0.33 | +7.7% | +3.9% to +17.8% | 5 / 0 |
| Price / prior 55-day high | cousin: breakout (FS01) | -0.03 | -0.42 | +0.7% | +5.6% to +12.6% | 3 / 0 |

*Likeness to MAX, stocks = average cross-sectional rank correlation of the signal with MAX; returns = correlation of the monthly long/short returns. CAPM alpha vs the equal-weight universe, Newey-West t.*

![360 map](../figures/nbh_max_map.png)

### 12.2 Are lottery and falling knife mirrors?

**In the stocks they pick: no.** The rank correlation of MAX and MIN is only -0.32. A stock with a huge best day usually also has a deep worst day, because both come from volatility: MAX correlates +0.79 with the range and +0.66 with idiosyncratic volatility; MIN correlates -0.77 with the range. What separates them is direction: MAX is +0.55 correlated with the net tail and MIN +0.50. So each signal is roughly half "how big are the tails" and half "which tail is bigger".

**In the returns they earn: nearly.** The MAX and MIN long/short returns correlate -0.66, because the shared volatility half is also a market bet: MAX's long/short correlates +0.82 with the volatility sort and +0.70 with the beta sort. In rising markets the lottery side wins and the crashed side wins; in falling markets both lose:

![Up and down markets](../figures/nbh_max_updown.png)

| Top-minus-bottom sort | Months the market rose, % a year | Months it fell, % a year |
|---|---|---|
| MAX (most lottery-like minus calmest) | +15% | -22% |
| MIN (mildest minus deepest crash) | -17% | +26% |
| Range (biggest minus smallest tails) | +18% | -28% |
| Net tail (up-tail minus down-tail dominated) | -3% | +2% |

The size of the tails swings with the market; the direction of the tails hardly does.

**The double sort settles it.** Sorting stocks independently into three MAX groups and three MIN groups (universes with at least 60 names, averaged):

![Double sort](../figures/nbh_max_dsort.png)

Holding the worst day fixed (down a column), the best day adds little: the spread from calmest to most lottery-like is +0.3, +1.6 and -0.1 points a year. Holding the best day fixed (along a row), the worst day matters more: deep crashes out-earned mild worst days by +1.5, +1.6 and +1.9 points, a beta effect again (§12.3). MAX carries no information that MIN and volatility do not already carry.

### 12.3 What is actually priced

![Alpha grid](../figures/nbh_max_alpha.png)

- **The size of the tails is priced, negatively, once beta is removed.** Range has a negative CAPM alpha in all six universes (-11.3% to -2.3%; t ≤ −2 in 4). So do idiosyncratic volatility (3 of 6 at t ≤ −2), volatility (5) and beta (3). This is the low-risk anomaly (Frazzini & Pedersen 2014; Ang et al. 2006), and it is where MAX's negative alphas (2 of 6 at t ≤ −2) come from.
- **The direction of the tails is not priced.** Net tail and skewness have alphas of -5.3% to +4.2% and -5.4% to +4.5% (universes with |t| ≥ 2: net tail 0, skewness 1). The genuinely "lottery" part of MAX, a big up-day that is *not* matched by a big down-day, earns nothing in these large-cap universes.
- **Spanning.** Regressing the MAX long/short on MIN, idiosyncratic volatility, volatility, beta, skewness, last month's return and the market explains 0.71 to 0.95 of its variance and leaves an alpha of -2.5% to +1.2% (|t| ≤ 1.4). **MAX is redundant.** The MIN long/short against MAX and the same neighbours leaves -1.5% to +3.4% (largest t 2.2).

| Universe | MAX alpha after neighbours / yr | t | R² | Neighbours with &#124;t&#124; ≥ 2 (loading, t) |
|---|---|---|---|---|
| US | +0.9% | 0.66 | 0.92 | MIN -0.32 (-3.3), Idiosyncratic volatility +0.27 (+4.5), Volatility +0.27 (+4.6), Skewness +0.37 (+5.6), Last month's return +0.22 (+6.9) |
| EU | -2.5% | -1.39 | 0.80 | MIN -0.20 (-2.9), Idiosyncratic volatility +0.20 (+4.4), Volatility +0.33 (+4.2), Skewness +0.24 (+3.0), Last month's return +0.22 (+5.4) |
| UK | +0.7% | 0.46 | 0.88 | MIN -0.30 (-4.1), Idiosyncratic volatility +0.38 (+4.6), Volatility +0.12 (+2.1), Beta +0.08 (+2.2), Skewness +0.35 (+4.2), Last month's return +0.22 (+6.9) |
| DK | +0.5% | 0.22 | 0.71 | MIN -0.24 (-3.1), Idiosyncratic volatility +0.33 (+4.2), Beta +0.14 (+2.6), Skewness +0.36 (+5.9), Last month's return +0.17 (+3.8) |
| SCANDI | +1.2% | 0.63 | 0.75 | MIN -0.25 (-2.7), Idiosyncratic volatility +0.37 (+4.6), Volatility +0.19 (+3.4), Beta +0.12 (+2.6), Skewness +0.50 (+7.3), Last month's return +0.18 (+3.4) |
| World | +0.5% | 0.54 | 0.95 | MIN -0.40 (-5.8), Idiosyncratic volatility +0.15 (+2.5), Volatility +0.32 (+5.3), Skewness +0.37 (+8.7), Last month's return +0.29 (+14.3) |

- **Persistence.** The MAX spread is about as large 2, 3, 4 and 6 months after formation as in the first month (US: t+1 +10%, t+2 +12%, t+3 +8%, t+4 +13%, t+6 +11%). A mispricing that gets corrected would fade; a stable characteristic such as volatility does not. That fits MAX measuring a lasting trait of the stock rather than a passing overreaction.

### 12.4 The falling knife at two speeds

| | Fast knife: MIN, a big one-day crash | Slow knife: sitting at the 52-week low |
|---|---|---|
| Stocks it picks | Volatile stocks (rank corr with volatility -0.59) | Losers (rank corr with momentum +0.66) |
| Raw return of *avoiding* the knife, avg of 6 | -1.5% a year (knives won, via beta) | +8.8% a year |
| CAPM alpha of avoiding it | +2.9% to +11.0%, t ≥ 2 in 3 of 6 | +4.4% to +13.8%, t ≥ 2 in 4 of 6 |
| What explains it | Low risk: crashed stocks are high-beta, high-vol | Momentum: losers keep losing (correlation of returns with momentum +0.65) |

Both speeds say the same thing once beta is removed: **the knife keeps falling relative to the market.** Only its beta makes a fast knife look like a bargain in a bull market. This matches A10 *Free Fallin'*, where knives rebounded only in market-wide crashes (0 of 3 tests passed), and it is the reverse of the "blood in the streets" folklore.

### 12.5 Verdict of the 360° view, and what is still missing

**Lottery and falling knife are the two tails of the same volatility.** They are mirrors in their returns (-0.66) but not in the stocks they pick (-0.32). Neither tail carries a premium of its own once volatility and beta are in the model (largest exception: MIN in UK, t 2.2 after its neighbours); what remains priced is the low-risk anomaly (avoid large tails of either sign) and, for the slow knife, momentum. For the multifactor battery this means: keep the root signals (volatility or beta, momentum), not MAX or MIN.

Not covered, and why:

| Missing angle | Why it matters | Why it is not here |
|---|---|---|
| Size and liquidity | The lottery effect lives in small, illiquid stocks | No market caps outside the US; the universes are blue chips by design |
| News versus non-news jumps | An earnings jump is information, a no-news jump is closer to gambling | No announcement dates outside the US in the data set |
| Retail attention and flows (search volume, broker app data) | The behavioural story is about retail demand | No attention data |
| Option-implied skewness | Forward-looking lottery-ness (Conrad, Dittmar & Ghysels 2013) | No option data |
| Nominal share price | Kumar (2009): lottery stocks are cheap per share | Only adjusted prices for most markets |
| Short interest and borrow fees | Limits to arbitrage on the short leg | Not in the data set |

## 13. Caveats

1. **Survivorship, and it cut in a particular direction here.** The first edition used today's index members outside the US. A high-MAX stock that jumped and later collapsed out of the index was missing, while one that jumped and kept rising was present, which flattered the high-MAX leg. This edition uses point-in-time membership (§3), and the table confirms the direction (survivor list → point-in-time; the universe definitions also changed):

| Universe | EW universe CAGR | L/S return / yr (net) | Low-MAX Sharpe | EW Sharpe |
|---|---|---|---|---|
| EU | +14.0% → +10.9% | -4.3% → -1.6% | 0.89 → 0.85 | 0.95 → 0.79 |
| UK | +12.7% → +9.9% | -9.9% → -3.6% | 0.70 → 0.95 | 0.95 → 0.74 |
| DK | +17.6% → +12.3% | -5.0% → -4.6% | 0.99 → 0.61 | 1.18 → 0.82 |
| SCANDI | +15.3% → +12.5% | -4.9% → -2.4% | 1.02 → 0.73 | 1.09 → 0.90 |
| World | +16.1% → +12.0% | -12.4% → -9.8% | 0.99 → 0.70 | 1.13 → 0.80 |

The non-US L/S numbers moved towards zero and the low-MAX book improved relative to its universe. About a fifth of member-quarters still have no price (mostly delisted names), so a residual bias of the same sign remains.
2. **Large caps only.** The effect is strongest in small, retail-held stocks; these universes are blue chips. DK (3 groups of ~6) and SCANDI (5 groups of ~12) are thin and noisy.
3. **Equal-weighting** (except the US value-weighted robustness book). The original paper's headline is value-weighted.
4. **Currency:** local; World mixes currencies.
5. **Not a registered trial.** A15 carries the registered tests (A15-1, A15-2); this factsheet extends them descriptively to five more universes. The fix ladder in §10 is counted inside the factsheets (7 trials, gate 0.05/7).

## 14. Academic references

- Bali, T. G., Cakici, N. & Whitelaw, R. F. (2011). Maxing out: Stocks as lotteries and the cross-section of expected returns. *Journal of Financial Economics*, 99(2), 427–446.
- Barberis, N. & Huang, M. (2008). Stocks as lotteries: The implications of probability weighting for security prices. *American Economic Review*, 98(5), 2066–2100.
- Kumar, A. (2009). Who gambles in the stock market? *Journal of Finance*, 64(4), 1889–1933.
- Tversky, A. & Kahneman, D. (1992). Advances in prospect theory: Cumulative representation of uncertainty. *Journal of Risk and Uncertainty*, 5(4), 297–323.
- Ang, A., Hodrick, R., Xing, Y. & Zhang, X. (2006). The cross-section of volatility and expected returns. *Journal of Finance*, 61(1), 259–299.
- Annaert, J., De Ceuster, M. & Verstegen, K. (2013). Are extreme returns priced in the stock market? European evidence. *Journal of Banking & Finance*, 37(9), 3401–3411.
- Walkshäusl, C. (2014). The MAX effect: European evidence. *Journal of Banking & Finance*, 42, 1–10.
- Bali, T. G., Brown, S., Murray, S. & Tang, Y. (2017). A lottery-demand-based explanation of the beta anomaly. *Journal of Financial and Quantitative Analysis*, 52(6), 2369–2397.
- Frazzini, A. & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics*, 111(1), 1–25.
- McLean, R. D. & Pontiff, J. (2016). Does academic research destroy stock return predictability? *Journal of Finance*, 71(1), 5–32.
- Jensen, T. I., Kelly, B. & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5), 2465–2518.
- Harvey, C., Liu, Y. & Zhu, H. (2016). …and the cross-section of expected returns. *Review of Financial Studies*, 29(1), 5–68.
- Novy-Marx, R. & Velikov, M. (2016). A taxonomy of anomalies and their trading costs. *Review of Financial Studies*, 29(1), 104–147.
- Treynor, J. & Mazuy, K. (1966). Can mutual funds outguess the market? *Harvard Business Review*, 44(4), 131–136.
- Boyer, B., Mitton, T. & Vorkink, K. (2010). Expected idiosyncratic skewness. *Review of Financial Studies*, 23(1), 169–202.
- Conrad, J., Dittmar, R. & Ghysels, E. (2013). Ex ante skewness and expected stock returns. *Journal of Finance*, 68(1), 85–124.
- George, T. & Hwang, C.-Y. (2004). The 52-week high and momentum investing. *Journal of Finance*, 59(5), 2145–2176.
- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns. *Journal of Finance*, 45(3), 881–898.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1), 65–91.
- Newey & West (1987); Politis & Romano (1994); Bailey & López de Prado (2012): as in FS01.

## 15. Reproduce

`code/data.py` → `lottery.py` + `run_lottery.py <U>` → `analyse.py lottery` → §10–11: `lottery_fix.py`, `fix_analysis.py` → §12: `signals.py`, `neighbourhood.py max`, `nbh_figs.py`, `nbh_section.py` → `make_figures.py` → `build_factsheets.py`. Metrics call Project1 `InvestmentLibrary`. Licensed prices are not included.
