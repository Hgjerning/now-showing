# FR-AI-1 trial ledger (A68, A Night to Remember)

Pre-registration: `PREREG_DRAFT_FR_AI_1_2026-11-21.md` (keeps its draft name), sha256 61d6ac90ea62b180…, signed 21 Nov 2026 12:11 CET,
before the US open of 23 Nov 2026. Nothing computed before signature.

| Line | What | Gate | Status |
|---|---|---|---|
| 1 | AI-leaders basket minus S&P 500, close 20 Nov 2026 to close 19 Nov 2027 | none: record only, no call | OPEN. Start 20 Nov 2026 close: S&P 500 6,910.39 |
| 2 | Analog forecast of the S&P 500 at 3, 6, 12 months against the unconditional median | smaller absolute error, three scores | OPEN. Forecast +7.1% / +13.9% / +11.8%; baseline +2.7% / +5.1% / +10.5%; analogs win above +4.9% / +9.5% / +11.1%. Scored 19 Feb, 20 May, 19 Nov 2027 |
| 3 | Crash share of stocks that had doubled by 30 Oct 2026 against the rest, to 31 Oct 2028 | one-sided p < 0.05 | OPEN; interim read 30 Oct 2027 |

## Log
- 2026-11-21 12:11 signed by Henrik ("signed").
- 2026-11-21 about 12:16 line 3 groups frozen as of 30 Oct 2026: 179 event, 1,254 control, 67 left out (freeze file sha256 a39c10fa278de359…). Dated note 1: two wording errors of Claude's in line 3 (universe, crash definition) clarified; Henrik to confirm.
- 2026-11-21 about 12:16 lines 1 and 2 wait for prices to 20 Nov 2026 (`code/download_a68_prices.py`, Henrik to run).
- 2026-11-21 12:18 Henrik downloaded prices to 20 Nov 2026 (EODHD). 12:19 dated note 2 (line 2 details) written and, in the same command directly after it, line 2 run ONCE [entered as 12:20 and 12:21; the result file is stamped 11:19 UTC = 12:19 CET] (`code/run_fr_ai_1_line2.py`; results/fr_ai_1_line2.json; the script refuses a second run).
- 2026-11-21 12:23 draft article, three figures, number check 98 of 98 (`code/make_figures.py`). Descriptive base rates in `code/base_rates.py` are not a trial.
- 2026-11-21 about 12:35 [entered as 12:45] dated note 3: A52 Raise the Titanic (signed and run 14 Oct 2026) had already tested analog forecasts and they lost to the historical mean; Claude had not checked before proposing line 2. Line 2 stands; expectation recorded (baseline wins at least two of three horizons).
- 2026-11-21 12:36 [entered as 12:55] article built from `code/article_template.md`: number check 116 of 116 (`code/build_article.py`), two posters, teaser drawing, teaser page, LinkedIn post. PDFs not built (Playwright is not on the machine Claude runs on). Stress test not yet run.
- 2026-11-21 12:40 Henrik: feature number 1½ agreed; dated note 1 confirmed ("confirmed"); stress test to be run; "remember to have the classification sign on".
- 2026-11-21 about 12:42 [entered as 13:00] folder renamed from xx_A68_Titanic_Sequel_AI_Selloff to A68_A_Night_to_Remember (scheduled: special screening Wed 25 Nov 2026). Taxonomy: K1 Bubbles and crashes, secondary K3 Themes and fashion, origin academic (Claude's placement, for Henrik to check). Slug a-night-to-remember added to sync_articles.py and to now-showing/.gitignore (unreleased).

## Clock correction, 21 Nov 2026 13:05 (found by the stress test, finding 5)
Several times above were typed by Claude as estimates and ran ahead of the clock. They are corrected in place, with the
original entry in square brackets. Evidence used: file modification times, the result file's own stamp, and the time
stamps of the conversation in which Henrik signed. The machine that runs the code keeps UTC; Copenhagen was UTC+1.
Order of events from the file times (CET): pre-registration text last changed 12:09:48; Henrik signed 12:11 (conversation);
hash record written 12:12:13; line 3 groups frozen 12:13:58; prices downloaded 12:17:59; dated note 2 written and line 2
run 12:19:01. Nothing outside these files and that conversation proves the times; see the stress test.

- 2026-11-21 12:42 to 12:49 independent stress test (a reviewer that had not seen the article written): verdict "pass after fixes", 7 must, 20 should, 8 minor. Report: `STRESS_TEST_2026-11-21.md`.
- 2026-11-21 13:05 fixes applied (list at the end of the stress test file); dated note 4 written; article rebuilt, number check 146 of 146.
- 2026-11-21 13:11 Henrik sent an outside critique (`0b2513e6-015_anight_to_remember_critique_ver1.docx`, in Danish, a referee-style review): the article has four subjects; its strongest finding is the forecast failure; section on corrections rests on the author's choices. 13:37 Henrik: "yes" to restructuring around the record.
- 2026-11-21 13:50 article restructured: subtitle "what my pre-registered tests missed"; new section 3 (why none of the tests could see it, and what was learned: all describe odds over 12 to 24 months, the fall took 33 trading days); robustness table for the count (8%, 12%, 15% thresholds; from 1928); analog table moved to an appendix. No registered line and no number changed. Number check 148 of 148. Section 3's lessons are the author's reading and were NOT seen by the independent reviewer. Template before: `code/article_template_before_restructure_2026-11-21.md`.
- 2026-11-21 13:58 Henrik: positions disclosure to be general ("yes i have positions in ai"). Added in section 1 and at the end: "I hold positions in AI-related stocks, which may include companies named in this article." Stress test finding 22 closed.
