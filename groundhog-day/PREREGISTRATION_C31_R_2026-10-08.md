# Pre-registration: Case 31 revisited, the midterm rally: election or business cycle? (2026-10-08)

**SIGNED by Henrik Gjerning, 8 October 2026, before any number in it was computed.** The ledger rows were entered at signing, before the run. Project10, theme T01. Follows `PREREGISTRATION_C31_2026-09-25.md` and the version 2 article
(8 October 2026). This does **not** change C31-1, C31-2 or the forward re-run C31-3 (16 March 2027).

## 0. Why, and what is already known

The external review (critique ver3) and the v2 rewrite left one question open: is the C31-1 gap
(+5.7 pts, p 0.0056) an election-cycle effect or a business-cycle effect that happens to fall on
midterms? What is **already seen** (reported in `v2_checks.json`, not trials):

- Five of 24 midterms had a recession at the vote (1930, 1970, 1974, 1982, 1990). Leaving out all
  recession-at-vote years: gap +3.2 pts, p 0.079. Matched on recession status: +6.2 pts, p 0.0073.
- The 120 days into a midterm are weaker than in control years (C31-2: −2.4 pts, failed).
- Since 2003 the gap is +2.6 pts on five elections.

Because those numbers are known, trial C31-4 is partly informed by the data. It adds controls that
have **not** been looked at (valuation, inflation, prior-year return) and states its prediction
with that in mind. Trial C31-5 uses a period that has **never** been examined in this programme:
the midterms before 1928.

## 1. Data (fixed)

- S&P 500 `^GSPC` daily close, 1927-12-30 to 2026-09-11 (same file as C31).
- Shiller, `ie_data.xls` (shillerdata.com), monthly: price P (monthly average of daily closes; before
  1926 the Cowles index), CPI, CAPE. Downloaded once, saved as `data/shiller_ie_2026-10.csv` before
  any computation, with its sha256 recorded in the ledger.
- NBER business-cycle dates from 1854 (peaks and troughs, NBER convention: recession months are
  peak+1 to trough). The 1926–2020 list already in `v2_checks.py`, extended back to 1854 from the
  NBER table.
- Election day rule unchanged: first Tuesday after the first Monday of November.

## 2. Trials (two; Bonferroni 2 → one-sided gate p < 0.025 each)

| trial | hypothesis | statistic | gate |
|---|---|---|---|
| **C31-4** | The midterm gap survives macro controls | OLS on 98 years (24 midterms, 74 controls, 1928–2025, same windows as C31-1): ret[+1,+90] = a + **b**·midterm + c·recession_at_vote + d·ret[−249,0] + e·log CAPE(Oct) + f·CPI inflation (Sep, y/y) + ε. Test b > 0. | Freedman–Lane permutation p (10,000 shuffles of the midterm label on the residuals of the controls-only model, seed 42) < 0.025. HC3 t reported alongside. |
| **C31-5** | The midterm gap exists in the unseen pre-1928 sample | Shiller monthly price, 1871–1927. Window = P(March, year y+1) ÷ P(November, year y) − 1 (monthly averages: roughly mid-November to mid-March). Midterm years 1874, 1878, …, 1926 (14); controls = every other year 1871–1927 (43). Mean midterm minus mean control. | One-sided label-permutation p (10,000 shuffles, seed 42) < 0.025. No halves rule: with 14 midterms each half would have 7. |

**Reported, not gated (no verdict from any of them):**

- **C31-4 variants:**
  - each control added alone;
  - recession_in_window instead of recession_at_vote;
  - a recession × midterm interaction.
- **Decomposition table and figure:** gap and permutation p for each sample.
  - full sample;
  - without recession-at-vote years;
  - post-1945;
  - post-2003.
- **Calibration of the monthly proxy:** the C31-5 window (P(Mar)/P(Nov), Shiller) computed for the
  1930–2022 midterms against their controls. This shows whether the proxy reproduces the daily result.
- **C31-5 extended:** the same test with the NBER recession-at-vote control.

## 3. Known weaknesses (stated now)

- **C31-4 uses ex-post recession dates.** NBER announces them months later. That is fine for a
  confounder control, but it is not a trading rule.
- **CAPE and CPI are as Shiller reports them today.** Real-time vintages are not used.
- **Pre-1928 prices are monthly averages.** Averaging smooths returns (Working 1960), but it does
  so equally for midterms and controls. Before about 1880 some states voted in September or
  October, so the November window is a less clean event date.
- **C31-5 has low power.** With 14 midterms and a 4-month sd of about 9%, the standard error of the
  gap is about 2.8 pts. A true +5.7 pt gap would be detected only about half the time.

## 4. My expected outcomes (to be scored)

- **C31-4: fail, narrowly (pass about 40%).** The recession control alone already brought p to
  0.079 by exclusion. Prior-year return is likely to absorb a little more, because midterm years
  start from weak markets (C31-2). Expected b: +3.5 to +5 pts, p 0.02–0.08.
- **C31-5: fail (pass about 20%).** Expected gap 0 to +4 pts, p 0.1–0.5, mainly because of low power.
  A pass would be the strongest evidence so far that the effect is about elections.
- **Calibration:** the monthly proxy reproduces a gap of +4 to +6 pts for 1930–2022.

Henrik's expectation: not stated.

## 5. Ledger rows (entered in `TRIAL_LEDGER.md` at signing, before the run)

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| C31-4 | 2026-10-08 (signed …) | Midterm gap > 0 after macro controls (recession, prior-year return, CAPE, inflation), 1928–2025 | `PREREGISTRATION_C31_R_2026-10-08.md` | *registered* |
| C31-5 | 2026-10-08 (signed …) | Midterm gap > 0 in the unseen pre-1928 sample (Shiller monthly, 1871–1927) | same | *registered* |

Programme count: two new trials. Across the three "revisited" pre-registrations (C31-4/5, A07-4/5,
A12-3/4) a family-wide one-sided Bonferroni gate would be 0.0083; it will be reported next to each
verdict.

**Signed:** Henrik Gjerning, 2026-10-08. The sha256 of this file is recorded in `TRIAL_LEDGER.md`.

## Clarification 1 (2026-10-08, written after signing and before any computation)

1. **C31-4 is deferred.** The Shiller `ie_data.xls` download (CAPE, CPI) is blocked from Claude's
   environment (HTTP 403 from both the cloud and the local proxy). Nothing of C31-4 has been computed. It
   runs unchanged once Henrik saves `ie_data.xls` from shillerdata.com into `data/`.
2. **C31-5 data.** C31-5 uses Shiller's price column P from `data/shiller_dividends.csv`. That file was
   taken from the same `ie_data.xls` by `code/v2_download.py` on 2026-10-07 (sha256 7ca61a86…). Only its
   1930–2022 dividend yields were used before; no pre-1928 window has been computed. The rest of C31-5
   is unchanged:
   - window P(March, y+1) / P(November, y) − 1;
   - midterms 1874–1926 (14);
   - controls = all other years 1871–1927 (43).
3. **Calibration (reported).** Same file and window, for the C31 years 1928–2025 (24 midterms, 74
   controls).
4. **NBER dates before 1926** (for the reported extension only). Peak / trough months, NBER chronology:
   - 1869-06/1870-12, 1873-10/1879-03, 1882-03/1885-05, 1887-03/1888-04, 1890-07/1891-05;
   - 1893-01/1894-06, 1895-12/1897-06, 1899-06/1900-12, 1902-09/1904-08, 1907-05/1908-06;
   - 1910-01/1912-01, 1913-01/1914-12, 1918-08/1919-03, 1920-01/1921-07, 1923-05/1924-07.
