# A68 A Night to Remember: what my pre-registered tests missed

Project 10 article series *Now Showing / Now Playing*. Pre-registered (see PREREGISTRATION_*.md, TRIAL_LEDGER.md).

| path | what |
|---|---|
| figures/hero_*.png | the poster card, which is the LinkedIn picture and opens the one-pager |
| linkedin/post.txt, teaser.html, *_teaser.pdf | one-pager |
| article/*.md / .html / .pdf | deep article with tables, figures and references |
| code/ | base_rates.py → extra_checks.py → make_figures.py → make_teaser_drawing.py → build_article.py |
| results/ | every number in the article (summary.json and CSVs) |

Shared helpers (`panel.py`, `features.py`, `stats.py`, `common.py`, `poster.py`) are in `Articles/_shared/lib10/`.
Raw Sharadar prices and fundamentals are licensed and are **not** included. Results files hold only derived statistics.

Now Showing No. 1½, sequel to No. 1 Titanic, special screening Wed 25 Nov 2026 (number agreed by Henrik 21 Nov 2026). Forward record FR-AI-1, signed 21 Nov 2026 12:11 CET: `PREREG_DRAFT_FR_AI_1_2026-11-21.md`, `DATED_NOTES_FR_AI_1.md`, `TRIAL_LEDGER.md`. Line 2 was run once (`code/run_fr_ai_1_line2.py`). results/ holds derived statistics and the frozen line 3 groups (tickers and two-year returns, no prices).

Pipeline run: 25 September 2026.
