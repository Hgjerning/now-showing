> **Note added 14 October 2026, not part of the signed text below.** The articles were renumbered to match the Now Showing feature numbers. This pre-registration keeps the codes it was signed with: A13 is now A08 (trial IDs follow, e.g. A13-1 is now A08-1). Full map: `Articles/RENUMBERING_2026-10-14.md`.

# Pre-registration: A13 "Video Killed the Radio Star": does publication kill a factor? (2026-09-25)

**Written before any number below was computed.** This replicates McLean & Pontiff (2016)
on 29 well-known US factors.

## 1. Data (fixed)

- Jensen, Kelly & Pedersen (2023) US factor returns, monthly, through Dec 2025. These are
  capped value-weighted tercile long-short portfolios, signed so the long leg is the side the
  original paper predicts will earn more. Local copy.
- **29 factors and the paper that made each one famous** (the publication year is the
  journal year):
  size (Banz 1981), book/market (Rosenberg, Reid & Lanstein 1985), earnings/price (Basu 1977),
  sales/price (Barbee, Mukherji & Raines 1996), dividend yield (Litzenberger & Ramaswamy 1979),
  12-1 momentum (Jegadeesh & Titman 1993), 12-7 momentum (Novy-Marx 2012), short-term reversal
  (Jegadeesh 1990), long-term reversal (De Bondt & Thaler 1985), residual momentum (Blitz, Huij &
  Martens 2011), seasonality (Heston & Sadka 2008), 52-week high (George & Hwang 2004),
  gross profitability (Novy-Marx 2013), operating profitability (Fama & French 2015),
  cash-based profitability (Ball et al. 2016), quality minus junk (Asness, Frazzini & Pedersen 2019),
  F-score (Piotroski 2000), O-score (Dichev 1998), accruals (Sloan 1996), net operating assets
  (Hirshleifer et al. 2004), asset growth (Cooper, Gulen & Schill 2008), net share issuance
  (Pontiff & Woodgate 2008), earnings surprise (Foster, Olsen & Shevlin 1984), R&D/market
  (Chan, Lakonishok & Sougiannis 2001), idiosyncratic volatility (Ang et al. 2006), MAX
  (Bali, Cakici & Whitelaw 2011), betting against beta (Frazzini & Pedersen 2014), Amihud
  illiquidity (Amihud 2002), share turnover (Datar, Naik & Radcliffe 1998).
- **Pre-publication:** first available month → December of the publication year.
  **Post-publication:** January of the following year → Dec 2025.

## 2. Trials (two; gate p < 0.025)

| trial | hypothesis | statistic |
|---|---|---|
| **A13-1** | Returns fall after publication | pooled regression of monthly factor returns on a post-publication dummy with factor fixed effects; standard errors clustered by month; coefficient < 0 (one-sided) |
| **A13-2** | Factors still earn a positive return after publication | equal-weighted average of all factors in their post-publication months; NW t (6 lags) > 0 |

**Reported:** decay per factor; a placebo with randomly assigned publication years (1,000 draws),
which separates a publication effect from a general downward trend; and the share of factors
still positive after publication.

## 3. Expected outcomes

- **A13-1: pass (about 70%).** McLean & Pontiff found a 58% decline on 97 anomalies.
- **A13-2: pass (about 65%).**

## 4. Ledger

Two trials. Programme total before: 42. After: 44.
