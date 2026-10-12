Part of [Now Showing](https://hgjerning.github.io/now-showing) · read the article: https://hgjerning.github.io/now-showing/groundhog-day

# Case 31: Groundhog Day, does the market rally every four years?

**Read the article: [article/midterm_rally.html](article/midterm_rally.html)** (Markdown: [article/midterm_rally.md](article/midterm_rally.md)).

**Now Showing No. 2, published Tuesday 13 October 2026.** Project 10 (LinkedIn teaser + GitHub deep article).
Theme T01, calendar and event anomalies. Continues Project3 trial P3-4. Version 3 (9 October 2026, after a hostile-referee stress test).

**Question:** is the post-midterm rally a midterm effect, or just November? The 90 trading days after each
US midterm (1930–2022) are compared with the same 90 days in the other 74 years.

**Results:**

| Trial | Result | Verdict |
|---|---|---|
| C31-1 | +7.6% vs +1.9%, gap +5.7 pts, permutation p 0.006 (gate 0.025), positive in both halves | passed (prediction wrong) |
| C31-2 | run-up into the midterm weaker, −2.4 pts, p 0.21 | failed (as predicted) |
| C31-4 | gap with macro controls +7.4 pts, Freedman–Lane p 0.0002 | passed |
| C31-5 | pre-1928, 14 midterms, gap −0.1 pts, p 0.52 | failed |
| C31-3 | forward re-run with 2026 added | runs 16 March 2027; scoring rule in `PREREGISTRATION_C31_3_scoring_2026-10-09.md` |

Programme-wide: 19 trials run, one-sided Bonferroni gate 0.0026. C31-4 clears it, C31-1 does not.

## Layout

| path | what |
|---|---|
| `PREREGISTRATION_C31_2026-09-25.md` | C31-1/2/3, gates and predictions, before the run |
| `PREREGISTRATION_C31_R_2026-10-08.md` | C31-4/5 (revisited), signed 8 Oct 2026 |
| `PREREGISTRATION_C31_3_scoring_2026-10-09.md` | how the 2026 forecast is scored (sign before publication) |
| `TRIAL_LEDGER.md` | outcomes |
| `STRESS_TEST_2026-10-09.md/.pdf` | hostile-referee stress test and what was changed |
| `linkedin/post.txt`, `teaser.html`, `midterm_rally_teaser.pdf` | LinkedIn teaser |
| `article/midterm_rally.md/.html/.pdf` | deep article, version 3; older versions in `article/_archive/` |
| `figures/` | `hero_groundhog_day.png` is the LinkedIn picture; fig1–fig5 in the article |
| `results/`, `results_r/` | every number: `summary.json`, `windows_by_year.csv`, `v2_checks.json`, `v3_checks.json`, `summary_c31_4/5.json` |
| `code/` | see below; superseded scripts in `code/_archive/` |
| `data/` | election list and `SHA256SUMS`. Price files are not redistributed: run `code/download_data.py` |

## Rebuild

```bash
python code/download_data.py   # Yahoo series; save Shiller's ie_data.xls by hand, then python code/v2_download.py
python code/run_midterm.py && python code/robustness.py && python code/v2_checks.py && python code/v3_checks.py
python code/run_c31_4.py && python code/run_c31_5.py
python code/make_figures.py && python code/make_hero.py
python code/build_final.py && python code/make_pdfs.py
```

Needs pandas, numpy, scipy, statsmodels, matplotlib, markdown, yfinance; `make_pdfs.py` needs playwright + Chromium.

## Before publishing

1. Henrik signs `PREREGISTRATION_C31_3_scoring_2026-10-09.md`.
2. Push this folder to `Hgjerning/now-showing` as `groundhog-day/` on Monday 12 October 2026.
3. Post the teaser on Tuesday 13 October 2026 with `figures/hero_groundhog_day.png`.
4. On 16 March 2027: refresh the data, add 2026, run C31-3 once, score the forecast.

**Note on dates.** This repository has no commit history before 12 October 2026, so the registration dates are self-attested. Each pre-registration's sha256 is recorded in `TRIAL_LEDGER.md` at signing.

*Not investment advice.*
