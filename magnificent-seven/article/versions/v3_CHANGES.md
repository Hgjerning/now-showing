# A03 The Magnificent Seven: version 3 (19 October 2026)

Base: version 2 (8 October). Requested by Henrik after the Copilot comparison of v1 and v2. **No trials added**; everything new is reported, not tested.

1. **Year-by-year table restored** (Table 3, from v1, plus the share of start months the top 10 won).
2. **The Interval opening and closing joke** back in (added by `write_article` from THE_INTERVAL.json), plus a closing line under the Verdict.
3. **Then and now (section 3, Table 1):** Nifty Fifty 1972-74, dot-com 2000-02 and today, from published, cited figures (Goldman Sachs, Siegel, Bridgeway, MFS, RBC, Nasdaq). No sourced top-10 share was found for 1972, and the article says so.
4. **What explains the lead, and what did it cost? (section 5, Figure 4, Table 4):** the monthly-rebalanced top-10 minus rest spread: +5.5%/yr, vol 12.1%, IR 0.45, NW t 1.69, max drawdown -28% (to Dec 2022), worst 12m -25%. FF5 + momentum: alpha +2.6%/yr (t 1.1), R² 0.43; loadings market +0.17, SMB -0.38, HML -0.32, CMA -0.41 (t -2.0), RMW and momentum about zero. Market + size alone: alpha +1.2% (t 0.4).
5. **Interaction (Henrik, 19 Oct):** Fama-MacBeth across the top 500, next-month return on size, 12-1 momentum and size × momentum (standardised): size -4.5 bp (t -1.0), momentum +23.6 bp (t 2.1), interaction +2.6 bp (t 0.5). No interaction; the lead belongs to the extreme top, not a smooth size slope. A matched-characteristics benchmark is listed as the next step.
6. Limitations updated ("Size or something else?" now measured; the comparison is borrowed; risk only partly measured). FUTURE_RESEARCH.json A03 updated.
7. LinkedIn post: "Neither showed up" (v2 wording), plus the factor, drawdown and 1972/2000 price lines.

Code: `code/run_v3_extras.py`, `code/make_fig4_v3.py`, `code/build_article_v3.py`. Results: `results/v3_extras.json`, `results/v3_monthly_spread.csv`. v1 and v2 files in `article/_archive/`.
