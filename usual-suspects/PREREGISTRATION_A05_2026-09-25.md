> **Note added 14 October 2026, not part of the signed text below.** The articles were renumbered to match the Now Showing feature numbers. This pre-registration keeps the codes it was signed with: A04 is now A05 (trial IDs follow, e.g. A04-1 is now A05-1). Full map: `Articles/RENUMBERING_2026-10-14.md`.

# Pre-registration: A04 "The Usual Suspects": 15 legends, one Fool, one regression (2026-09-25)

**Written before any number below was computed.** The question: once the standard academic
factors are controlled for, do famous investors' rules add anything? The factors are market,
size, value, profitability, investment (Fama & French 2015) and momentum (Carhart 1997).

## 1. Data (fixed, local copies; nothing downloaded)

- **Guru recipes**: the 16 guru recipes of Project1 `factor_recipes.py` (pre-registered there on
  2026-09-09 and amended 2026-09-11). Each recipe is the equal-weight average of JKP
  long-short factor legs, US (`jkp_usa_factors_monthly.csv`, capped value-weighted, USD, to
  2025-12). The legs are copied verbatim into `code/run_suspects.py`. They are proxies for each
  investor's published rules, not the investors' own portfolios. Fifteen are named people; the
  sixteenth is the Motley Fool.
- **Factors**: Kenneth French US research factors, daily, compounded to calendar months:
  Mkt-RF, SMB, HML, RMW, CMA (from 1963-07) and Mom. French's construction is independent of
  JKP's, which is why these are the controls.
- Sample: each recipe from max(its first month, 1963-07) to 2025-12.

## 2. The regression (the "one regression")

Monthly recipe return = α + β·(Mkt-RF, SMB, HML, RMW, CMA, Mom) + ε. OLS with Newey–West
standard errors, 6 lags. The recipes are long-short, zero-cost portfolios, so no risk-free rate
is subtracted.

## 3. Trial (one trial, a family of 16 tests with Bonferroni inside, as for Project3's P3-5)

**A04-1:** at least one guru recipe has a six-factor alpha that is non-zero **and** robust.
Per recipe: |NW t(α)| > **2.955** (two-sided 0.05/32, Bonferroni over 16), **and** the same
sign of α in both halves (1963–1994 and 1995–2025). The trial passes if one or more recipes
pass. Each recipe's verdict is reported.

**Reported, not gated:** R²; factor loadings; the raw premium (mean, NW t) against the
six-factor alpha; α since 2012; a developed-markets version (JKP `world` recipes on French
Developed 5 factors + Mom, 1990-07 → 2025-12); and the stock-level evidence already on file
(Project1 ART and live-universe attribution, the ART pre-registered recipes). Those numbers
are copied, not re-estimated.

## 4. Expected outcomes, stated before running

- **Most recipes are explained by the six factors.** I expect R² above 0.6 for the value-type
  recipes (Graham, Neff, Dreman, O'Shaughnessy value, Carlisle, Fisher) and for O'Neil through
  momentum.
- **A04-1: pass is plausible for one or two recipes**, most likely something with profitability
  or accruals content that RMW/CMA do not fully span: Greenblatt, P. O'Shaughnessy millennial,
  or Buffett quality (QMJ is known to carry alpha against FF5; Asness, Frazzini & Pedersen
  2019). My guess: 1–3 recipes pass, and the rest show |α| < 2%/yr.
- α since 2012: smaller than the full-sample α for almost every recipe.

## 5. Ledger

A04-1 is one trial. Programme total before it: 20 run. After: 21.
