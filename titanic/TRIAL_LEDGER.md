# Case 1 (Every bubble rhymes) trial ledger

Rows added **before** the run. Programme total before this case: 17 run (Project3 15 + Case 31 2).
Case 33 spent none.

| # | date | hypothesis | spec | outcome |
|---|---|---|---|---|
| C1-1 | 2026-09-25 | Nasdaq-100 explosive now (GSADF and last-month BSADF above the 98.33% critical value) | `PREREGISTRATION_C1_2026-09-25.md` | **failed**: GSADF 1.33 vs cv 2.71 (MC p 0.413); last BSADF 0.67 vs 1.18. Only episode 2021-04→2021-08. Prediction (fail) held. |
| C1-2 | 2026-09-25 | AI-leaders basket explosive now | same | **failed**: GSADF 2.21 vs cv 2.80 (MC p 0.062); last BSADF 0.31 vs 1.34. Dated episodes 2013-12→2014-09, 2016-07→2018-09, 2021-10→2021-12. **None in 2023–2026.** Prediction (about 50/50) resolved to fail; lag 0 and the 95% level agree. |
| C1-3 | 2026-09-25 | 24-month crash probability after a 100% two-year run-up exceeds the unconditional rate (US panel 2011–2026), both halves | same | **PASSED**: 48.0% vs 38.3% (n 3053 vs 10954), z 9.6; both halves higher (40/32, 55/47). Prediction held. **Second prediction WRONG:** forward returns after run-ups are significantly *lower* than the control (24m mean 23% vs 34%, t -4.3), though still positive. |

**Legibility:** Nikkei 1989 passed and Nasdaq 2000 passed. **S&P 500 1929 FAILED**: GSADF 2.07 vs 2.16, and the only flagged episode was 1932 (the post-crash rebound). The data start in Dec 1927, only 21 months before the peak, too short for the minimum window. One failure of three is allowed by §4, so the trials stand.

**Spent in this ledger: 3. Programme total: 20 run, 1 registered (C31-3).**

**Update 2026-10-07 (after external review):** `code/valuation_table.py` adds a valuation snapshot (section 8: eight AI leaders at 2026-09-30 vs Cisco, Microsoft, Oracle, Intel, NVIDIA at 2000-03-10, Sharadar). Reported, not gated, **not a trial**; trial count unchanged. Text: "Why these eight?" box, Figure 1 caption, precise conclusion ("under this definition no evidence of an active bubble"). No pre-registered number changed.
