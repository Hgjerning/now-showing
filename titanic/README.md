Part of [Now Showing](https://hgjerning.github.io/now-showing) · read the article: https://hgjerning.github.io/now-showing/titanic

# Case 1: Every bubble rhymes. Does this one?

**Theme T02, Cycles, bubbles and crashes.** Project 10. Written September 2026. Pre-registered; three trials
(C1-1 and C1-2 failed, C1-3 passed); legibility 2 of 3. Programme trial count is now 20.

| path | what |
|---|---|
| `PREREGISTRATION_C1_2026-09-25.md`, `TRIAL_LEDGER.md` | spec written before the run; outcomes |
| `linkedin/post.txt` | paste-ready teaser (222 words); attach `figures/fig1_every_bubble_rhymes.png` |
| `linkedin/teaser.html`, `linkedin/every_bubble_rhymes_teaser.pdf` | one-page teaser |
| `article/every_bubble_rhymes.md` / `.html` / `.pdf` | deep article: 7 tables, 4 figures, references |
| `code/run_bubbles.py` | GSADF/BSADF engine (from scratch, cumulative sums, Monte Carlo critical values) and all trials |
| `code/reported_extra.py`, `make_figures.py`, `build_article.py`, `make_pdfs.py` | reported extras, figures, text, PDFs |
| `data/` | S&P 500, Nikkei and Nasdaq Composite closes; `us_monthly_adjclose_panel.csv` (2,504 US tickers from the Project1 price cache) |
| `results/` | every number: `summary.json`, `reported_extra.json`, BSADF sequences, GSY tables |

Rebuild: `python code/run_bubbles.py && python code/reported_extra.py && python code/make_figures.py && python code/build_article.py && python code/make_pdfs.py`

Before publishing: push this folder to `Hgjerning/now-showing` as `titanic/` (page: hgjerning.github.io/now-showing/titanic). Publication slot: Tuesday 6 October 2026 (No. 1). The data run to 18 September 2026;
refresh the panel and re-run once, just before posting. A refresh is a new trial if any verdict is re-read.
