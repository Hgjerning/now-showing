# Now Showing / Now Playing

Sixteen investment theses, each named after a film or a song, each **pre-registered before the data were opened**
and tested with placebo, bootstrap and multiple-testing corrections. One article a week on LinkedIn, Tuesdays 08:00 CET,
6 October 2026 to 2 February 2027. The finale scores all of them.

**Read the series:** https://hgjerning.github.io/now-showing

| No. | LinkedIn | Article | Kind | Question | Folder |
|---|---|---|---|---|---|
| 1 | 6 Oct 2026 | [Titanic](https://hgjerning.github.io/now-showing/titanic) | Film | Every bubble was unsinkable. Is this one? | [`titanic/`](titanic/) |
| 2 | 13 Oct 2026 | [Back to the Future](https://hgjerning.github.io/now-showing/back-to-the-future) | Film | My strategy beat the market by 5% a year. In the past. | [`back-to-the-future/`](back-to-the-future/) |
| 3 | 20 Oct 2026 | [Groundhog Day](https://hgjerning.github.io/now-showing/groundhog-day) | Film | The rally that comes back every four years | [`groundhog-day/`](groundhog-day/) |
| 4 | 27 Oct 2026 | [The Magnificent Seven](https://hgjerning.github.io/now-showing/magnificent-seven) | Film | Does concentration come back to bite? | [`magnificent-seven/`](magnificent-seven/) |
| 5 | 3 Nov 2026 | [Viva Las Vegas](https://hgjerning.github.io/now-showing/viva-las-vegas) | Song | Do lottery stocks still lose? | [`viva-las-vegas/`](viva-las-vegas/) |
| 6 | 10 Nov 2026 | [The Usual Suspects](https://hgjerning.github.io/now-showing/usual-suspects) | Film | Fifteen legends, one Fool, one regression | [`usual-suspects/`](usual-suspects/) |
| 7 | 17 Nov 2026 | [Minority Report](https://hgjerning.github.io/now-showing/minority-report) | Film | Can machine-learning precogs see next month's winners? | [`minority-report/`](minority-report/) |
| 8 | 24 Nov 2026 | [Under Pressure](https://hgjerning.github.io/now-showing/under-pressure) | Song | Which distress score sees the crash coming? | [`under-pressure/`](under-pressure/) |
| 9 | 1 Dec 2026 | [Video Killed the Radio Star](https://hgjerning.github.io/now-showing/video-killed-the-radio-star) | Song | Does publication kill a factor? | [`video-killed-the-radio-star/`](video-killed-the-radio-star/) |
| 10 | 8 Dec 2026 | [Miracle on 34th Street](https://hgjerning.github.io/now-showing/miracle-on-34th-street) | Film | Does Santa Claus visit Wall Street? | [`miracle-on-34th-street/`](miracle-on-34th-street/) |
| 11 | 15 Dec 2026 | [Inception](https://hgjerning.github.io/now-showing/inception) | Film | What happens when you mine 1,000 trading rules? | [`inception/`](inception/) |
| 12 | 5 Jan 2027 | [Money for Nothing](https://hgjerning.github.io/now-showing/money-for-nothing) | Song | Does trading less pay? | [`money-for-nothing/`](money-for-nothing/) |
| 13 | 12 Jan 2027 | [A Beautiful Mind](https://hgjerning.github.io/now-showing/a-beautiful-mind) | Film | Do chart rules still time the market? | [`a-beautiful-mind/`](a-beautiful-mind/) |
| 14 | 19 Jan 2027 | [Stormy Weather](https://hgjerning.github.io/now-showing/stormy-weather) | Song | Does cutting risk after volatile months pay? | [`stormy-weather/`](stormy-weather/) |
| 15 | 26 Jan 2027 | [Free Fallin'](https://hgjerning.github.io/now-showing/free-fallin) | Song | Should you catch a falling knife? | [`free-fallin/`](free-fallin/) |
| 16 | 2 Feb 2027 | [The Good, the Bad and the Ugly](https://hgjerning.github.io/now-showing/good-bad-ugly) | Film | What did 15 theses teach us? | [`good-bad-ugly/`](good-bad-ugly/) |

A folder appears here on the Monday before its post. Groundhog Day's sequel (pre-registered trial C31-3) runs on 16 March 2027.

## What is in each folder

| path | what |
|---|---|
| `index.html` | the article as a web page (GitHub Pages) |
| `article/` | the article as Markdown, HTML and PDF |
| `PREREGISTRATION_*.md`, `TRIAL_LEDGER.md` | the tests as written down before the run, and every trial that was run |
| `code/` | everything from data to figures to article; no number in the text is typed in |
| `results/` | the outputs the article is built from |
| `figures/` | charts and the poster |
| `linkedin/` | the post text and the one-page teaser PDF |
| `data/` | notes on where the inputs come from (public files included, licensed files not) |

Shared code is in `_shared/lib10/` (point-in-time panel, statistics, posters, page builders).

## Running it

```bash
pip install -r requirements.txt
python -m playwright install chromium   # only for the PDFs
export P10_DATA=/path/to/your/sharadar/files   # only for the stock-level articles
```

Then run the scripts in each folder's `code/` in the order given in that folder's README.

## Data

Price and fundamental data come from Sharadar (Nasdaq Data Link), Yahoo Finance, MSCI, the Kenneth R. French
Data Library, Jensen-Kelly-Pedersen (jkpfactors.com) and AQR. Licensed and per-stock files are **not** in this repo;
each `data/README.md` lists what to download. Stock-level results use the current Sharadar master list, which
leaves out some companies that later disappeared; the affected articles say so.

## Licence

Code: MIT. Text and figures: CC BY 4.0. Nothing here is investment advice.

Henrik Gjerning · Rude Investment Consulting · [LinkedIn](https://www.linkedin.com/in/henrikgjerning)
