# Pre-registration · FS17 Fundamentals outside the US

Written 27 September 2026, before any FS17 result was computed.

## Why this route

Stock-level fundamentals with filing dates exist here only for the US (Sharadar, FS13b). Project2's `pit_fundamentals` holds non-US snapshots only from September 2026, too short for a backtest. What does exist outside the US is **factor-level** fundamental returns: the JKP factors for the UK, Denmark, World ex US and World (2013–2025) and the ART database's own fundamental factor spreads for Europe, the UK and America (1996–2013). FS17 uses these to answer the multifactor question at factor level.

## Themes (fixed)

| Theme | 2013–2025 (JKP, equal-weight average of the cluster's factors) | 1999–2013 (ART composite, top minus bottom decile) |
|---|---|---|
| Profit growth / earnings momentum | JKP "Profit Growth" | ART "Revision (composite)" (analyst revisions, I/B/E/S) |
| Issuance | JKP "Debt Issuance" | ART "Buyback (composite)" |
| Value | JKP "Value" | ART "Value (composite)" |
| Profitability | JKP "Profitability" | ART "Profitability (composite)" |

The **fundamental pair** = profit growth + issuance, the two themes FS13 found positive in every JKP segment.

## Markets

2013–2025: UK (JKP gbr ↔ our UK books), Denmark (dnk ↔ DK), EU (World ex US as proxy ↔ EU), World (world ↔ World); the US (usa ↔ US) as reference. 1999–2013: Europe (↔ EU_A), UK (↔ UK_A); America (↔ US_A) as reference. Non-US markets: UK, DK, EU (2013–25) and Europe, UK (1999–2013).

## Tests (fixed)

Every theme is scaled to 10% annual volatility with its own trailing 12-month volatility (ex ante, cap 3×); the shortlist legs (low beta and 12-1 momentum, beta-neutral, net) come from FS13 (`battery_price.pkl`) and FS15 (`battery_art.pkl`).

1. **Primary:** regression of the scaled fundamental pair (equal weights) on the two shortlist legs, monthly, Newey–West t (6 lags). Pooled over the non-US markets (average of the market series). Claim: alpha t > 2 in **both** periods.
2. Per theme and market: the same spanning regression (alpha, t, R²).
3. Combination: shortlist + fundamental pair (equal risk: each of the four series scaled to 10% vol, equal weights) versus the shortlist alone: Sharpe ratios and the paired difference.

## Caveats stated in advance

JKP factors are capped value-weighted, gross of costs and in USD; ART spreads are decile spreads, gross of costs, in ART's segment universes. Our shortlist books are net, equal-weighted, local currency. A positive result shows the fundamental information is not in the price signals; it does not show a net, investable return. All tests enter the trial ledger.
