# Marketing kit · FS13 and the factsheet series

## LinkedIn post (FS13) · with `fs13_card.png` or the carousel `fs13_carousel_linkedin.pdf` (upload as a document)

I put every signal in every corner.

19 price signals × 6 markets (US, Europe, UK, Denmark, Scandinavia, World), 2013–2026, point-in-time index members, after costs. Plus the 153 published factors of Jensen, Kelly & Pedersen, by country.

The question: what works everywhere, and not just in one market?

→ After correcting for 38 tests, no price signal earns a positive return that survives on its own. Thirteen years of large caps is too short to prove a single signal.
→ The direction is more consistent than the significance. Momentum is positive in 6 of 6 of my markets and all 4 published segments (t 4.4 there, 1.5 in my large caps after borrow fees).
→ Low beta is positive in 6 of 6, once you remove the market bet and pay for the leverage it needs (2.2× borrowed in the US).
→ 19 signals are really two bets: a low-risk block of nine and a momentum block of four.
→ In the fundamentals, debt issuance (t 6.2) and profit growth (t 2.5) worked in every segment. Short-term reversal, seasonality, investment and accruals faded in the US.
→ Seasonality and skewness lose reliably in large caps (seasonality is the one signal that survives the correction, as a loser).
→ Scandinavia marches to its own drum: its ranking of what works has a 0.29 correlation with the other markets.

Engine check: my US signals correlate 0.8 or more with the published factors for 7 of 12.

Full factsheet with every number, the test design and what goes into the multifactor model next: https://hgjerning.github.io/now-showing/factsheets/fs13-signal-battery

#investing #quant #factorinvesting #momentum #research

## LinkedIn carousel
`fs13_carousel_linkedin.pdf`: 8 slides, 1080×1350 (portrait, LinkedIn's document format).

## Series launch post (FS00–FS13) · use `../fs05_card.png` or the FS00 heatmap

Fourteen factsheets, one set of rules.

Over the past weeks I ran the famous strategies (Turtle Traders, the lottery factor, momentum, low volatility, betting against beta, the 52-week high and low, size, seasonality, reversal, residual momentum, even 10,000 dart-throwing monkeys) through the same code on six point-in-time markets, 2013–2026, after costs.

Each factsheet has the P&L, trade records, drawdowns, factor attribution, what goes wrong and how to fix it, where the strategy fits, and a 360° view of its neighbours.

Three things stood out:
→ Most folklore fails where it fights momentum.
→ Raw long/short numbers in a bull market are mostly a hidden market bet.
→ Six markets are not six tests: they co-move so much that they count as fewer than two.

FS00 sums it all up in one table, with a gap analysis of what is still missing. FS13 asks which signals work in every corner.

https://hgjerning.github.io/now-showing/factsheets

#investing #quant #factorinvesting #backtesting

## X / Twitter thread

1/ I put every signal in every corner: 19 price signals × 6 markets, 2013–26, point-in-time, after costs, plus 153 published JKP factors. What works everywhere?

2/ After correcting for 38 tests, no price signal earns a positive return that survives on its own. 13 years of large caps can't prove one signal alone.

3/ The direction is more consistent. Momentum: positive in 6/6 markets and 4/4 published segments (t 4.4). Low beta: 6/6 after removing beta, borrow fees and leverage costs.

4/ 19 signals ≈ 2 bets. MAX, MIN, range, idio vol, vol and beta are one low-risk block; momentum, 52w high, 52w low distance and the breakout are another.

5/ Fundamentals that worked everywhere since 2013: debt issuance (t 6.2) and profit growth (t 2.5). Faded in the US: short-term reversal, seasonality, investment, accruals.

6/ Scandinavia's ranking of what works has ~0.29 correlation with other markets. Small markets are single-stock stories. Full factsheet: https://hgjerning.github.io/now-showing/factsheets/fs13-signal-battery

## Newsletter / website blurb

**Every signal, every corner (FS13).** I ran all 19 price signals in six markets and set them against the 153 published JKP factors to find what works everywhere. After correcting for 38 tests no price signal earns a positive return that survives on its own; thirteen years of large caps can't prove any one signal. The direction is more consistent: momentum is positive in 6 of 6 markets and every published segment, low beta in 6 of 6 once the market bet is removed, borrow is paid and leverage financed, and debt issuance and profit growth lead the fundamentals. The 19 signals are really two bets, low risk and momentum. Seasonality and skewness lose in large caps, and Scandinavia disagrees with everyone. [Read the factsheet](https://hgjerning.github.io/now-showing/factsheets/fs13-signal-battery)

## Posting notes
- Post the carousel as a LinkedIn *document*; put the link in the first comment if reach matters more than clicks.
- The links point to GitHub Pages under `now-showing/factsheets/`, which is still marked unreleased in `.gitignore`: publish the folder before posting.
- Every number above is generated from `results/common_ground.json` and `results/financing.json` by `code/marketing_fs13.py`; re-run after any rebuild.
