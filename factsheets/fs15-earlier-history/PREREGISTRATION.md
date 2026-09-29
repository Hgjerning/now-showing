# Pre-registration · FS15 The earlier history (1998–2013)

Written 27 September 2026, before any 1998–2013 signal or strategy return was computed. Everything is copied from the 2013–2026 work; nothing is re-tuned.

## Question

Do the conclusions of FS13 (price battery), FS13c (momentum is the price signal that adds return) and FS14 (the pre-registered multifactor procedure) hold in an earlier, independent period that includes the 2000–02 and 2008 bear markets?

## Data

The ART research database extract in Project2 (`reporting/art_cache`): daily total-return indices and daily traded value per stock, as reported, including stocks that later delisted, January 1998 – March 2013, for four regions: US, EU (EU member states excluding the UK, Poland and Greece), UK and Denmark. World = US + UK + EU, converted to USD with Fed H.10 rates. No Scandinavia (the extract does not identify Finnish stocks) and no fundamentals (not in the extract).

## Universes (fixed now)

The extract has no index-membership dates, so each month-end the universe is the largest stocks by 63-day average traded value (USD), among stocks with at least 60 trading days of history and a price in the last five trading days: US 500, UK 350, EU 240, Denmark 25. A stock is eligible in month m if it was in the universe at the end of month m−1. This is a liquidity-defined universe, not an index; it is stated as such.

## Signals, books and costs

Identical to FS13 (`code/battery.py`): the 19 price signals with the same pre-declared directions; long/short, beta-neutral long/short and long-only books; 10 bp per side, the size-tiered borrow fee and financing of net long cash at the USD risk-free rate + 0.5%. Sort period Jan 1999 – Feb 2013 (the first year of data builds the 252-day signals).

## Tests

1. **FS13 replication:** for each signal, the pooled beta-neutral book (average of the markets, t including co-movement). Claim to check: the momentum family (12-1, residual momentum, 52-week high) is positive in the earlier period too; seasonality and tail direction are not positive.
2. **FS13c replication:** Fama-MacBeth with the same 10 cluster representatives. Claim to check: 12-1 momentum has a positive multivariate slope, t > 2 on the market average.
3. **FS14 replication:** the FS14 procedure exactly as in `PREREG_FS14.md` (filter, pruning, 11 weighting rules, benchmarks ALL-EQ and the same fixed shortlist of low beta and 12-1 momentum), walk-forward, first portfolio month = first month with 36 months of history. Primary test: RP minus ALL-EQ, average over US, EU, UK, DK, t > 2 and positive in both halves of the period.
4. All tests enter the factsheet trial ledger.

## What counts as confirmation

A 2013–2026 result is "confirmed" when the same sign holds in 1998–2013 with t > 2 on the pooled test; "consistent" when the sign holds with t between 0 and 2; "reversed" when the sign flips.
