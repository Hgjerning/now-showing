# A07 Video Killed the Radio Star: does publication kill a factor?

Project 10 article series *Now Showing / Now Playing*. Pre-registered (see PREREGISTRATION_*.md, TRIAL_LEDGER.md).

Feature No. 7 (17 Nov 2026). Renumbered from A08 to A07 on 8 Nov 2026, when the original A06 was withdrawn; the pre-registration, trial IDs (A08-1, A08-2) and file names keep their registered A08 labels.

| path | what |
|---|---|
| figures/hero_*.png | the poster card, which is the LinkedIn picture and opens the one-pager |
| linkedin/post.txt, teaser.html, *_teaser.pdf | one-pager |
| article/*.md / .html / .pdf | deep article with tables, figures and references |
| code/ | run_decay.py → check_pubyears.py → robustness_2026-10-23.py → make_figures.py → build_article.py |
| results/ | every number in the article (summary.json and CSVs) |

Shared helpers (`panel.py`, `features.py`, `stats.py`, `common.py`, `poster.py`) are in `Articles/_shared/lib10/`.
Data: Jensen, Kelly & Pedersen's public US factor returns (jkpfactors.com) and their Factor Details.xlsx; download into data/ (see data/README.md). They are not redistributed here. Results files hold only derived statistics.

Pipeline run: 25 September 2026; robustness checks 23 October 2026.
Publication slot: Tuesday 17 November 2026 (Now Showing No. 7).
