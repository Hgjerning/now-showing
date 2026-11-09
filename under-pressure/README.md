# A06 Under Pressure: which distress score sees the crash coming?

Project 10 article series *Now Showing / Now Playing*. Pre-registered (see PREREGISTRATION_*.md, TRIAL_LEDGER.md).

Feature No. 6 (10 Nov 2026). Renumbered from A07 to A06 on 8 Nov 2026, when the original A06 (Minority Report, machine learning) was withdrawn; the pre-registrations, trial IDs (A07-1 ... A07-5) and file names keep their registered A07 labels.

| path | what |
|---|---|
| figures/hero_*.png | the poster card, which is the LinkedIn picture and opens the one-pager |
| linkedin/post.txt, teaser.html, *_teaser.pdf | one-pager |
| article/*.md / .html / .pdf | deep article with tables, figures and references |
| code/ | run_distress.py → run_a07r.py → make_figures.py → make_teaser_drawing.py → build_article.py |
| results/ | every number in the article (summary.json and CSVs) |

Shared helpers (`panel.py`, `features.py`, `stats.py`, `common.py`, `poster.py`) are in `Articles/_shared/lib10/`.
Raw Sharadar prices and fundamentals are licensed and are **not** included. Results files hold only derived statistics.

The corrected point-in-time list (`results_pit/`) is the verdict of record (23 Oct 2026); `results/` is the registered list; `results_a07r/` holds the 8 Oct follow-up (A07-4/5). Per-firm `scores_panel.csv` files are derived from Sharadar and are listed in `.gitignore`.

Pipeline run: 25 September 2026.
Publication slot: Tuesday 10 November 2026 (Now Showing No. 6).
