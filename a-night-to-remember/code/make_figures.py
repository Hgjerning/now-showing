# -*- coding: utf-8 -*-
"""A68 A Night to Remember: figures and the number check (21 Nov 2026). Reads results only; nothing here is a trial.
fig1_since_titanic.png      basket of eight and SPY since 6 Oct 2026
fig2_after_corrections.png  12-month return after each earlier 10% correction
fig3_analogs.png            the ten analog paths of FR-AI-1 line 2
    python code/make_figures.py
"""
import json, sys
from datetime import datetime
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent; ART = HERE.parent; RES = ART / "results"; FIG = ART / "figures"; FIG.mkdir(exist_ok=True)
sys.path.insert(0, str(ART.parent / "_shared" / "lib10"))
from common import AQUA, BLUE, GREY, INK, INK2, mpl_style   # noqa: E402
mpl_style(plt)
def stamp(m): print(f"[A68 fig] {datetime.now():%H:%M:%S}  {m}", flush=True)
J = json.load(open(RES / "base_rates_and_line1.json")); C = J["corrections"]; L1 = J["line1"]["since_titanic_published_2026_10_06"]; L2 = json.load(open(RES / "fr_ai_1_line2.json"))
F3 = pd.read_csv(RES / "fr_ai_1_line3_freeze_2026-10-30.csv")

s = pd.read_csv(RES / "since_titanic.csv", index_col=0, parse_dates=True)
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.plot(s.index, s.spy, color=GREY, lw=2.2, label="S&P 500 (SPY)"); ax.plot(s.index, s.basket, color=BLUE, lw=2.6, label="Eight AI leaders, equal weight")
for col, c in (("spy", INK2), ("basket", BLUE)): ax.text(s.index[-1], s[col].iloc[-1], f"  {s[col].iloc[-1] - 100:+.1f}%", color=c, fontsize=10.5, fontweight="bold", va="center")
ax.axhline(100, color=INK2, lw=0.7); ax.set_ylabel("6 October 2026 = 100"); ax.legend(frameon=False, loc="lower left", fontsize=10); ax.margins(x=0.09); ax.set_ylim(73, 101.5)
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.TU)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%-d %b"))
ax.set_title("Since Titanic was published: the market fell, the favourites fell twice as far", loc="left", fontsize=12.5, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(FIG / "fig1_since_titanic.png"); plt.close(fig); stamp("fig1")

E = pd.read_csv(RES / "corrections_since_1950.csv"); E = E[E.r12.notna()].sort_values("r12").reset_index(drop=True)
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=200)
ax.bar(range(len(E)), E.r12 * 100, color=[INK if b else AQUA for b in E.became_bear])
ax.set_xticks(range(len(E))); ax.set_xticklabels([f"{pd.Timestamp(d):%b %Y}" for d in E.first_10pct_day], rotation=60, fontsize=7.5, ha="right"); ax.axhline(0, color=INK2, lw=0.8)
ax.axhline(C["12 months"]["median"] * 100, color=BLUE, lw=1.2, ls="--"); ax.text(2.6, C["12 months"]["median"] * 100 + 1.2, f"median {C['12 months']['median'] * 100:+.1f}%", color=BLUE, fontsize=10)
ax.bar([0], [0], color=INK, label=f"became a bear market, known only later ({C['became_bear']})"); ax.bar([0], [0], color=AQUA, label=f"did not ({C['n_past'] - C['became_bear']})"); ax.legend(frameon=False, loc="lower right", fontsize=10)
ax.set_ylabel("S&P 500, % over the next 12 months"); ax.set_title("After the first close 10% below a high: 26 cases since 1950", loc="left", fontsize=12.5, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(FIG / "fig2_after_corrections.png"); plt.close(fig); stamp("fig2")

g = pd.read_csv(ART / "data" / "GSPC_daily_eodhd.csv", parse_dates=["date"]); c = g.close.values; pos = {str(d.date()): i for i, d in enumerate(g.date)}
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=200); P = []
for a in L2["analogs"]:
    e = pos[a["window_end"]]; path = (c[e:e + 253] / c[e] - 1) * 100; P.append(path)
    ax.plot(path, color=GREY, lw=1.1, alpha=0.9)
ends = sorted(((p[-1], f"{pd.Timestamp(a['window_end']):%b %Y}") for p, a in zip(P, L2["analogs"])), key=lambda x: x[0]); y = -1e9
for v, lab in ends:
    y = max(v, y + 4.2); ax.text(255, y, lab, fontsize=8.5, color=INK2, va="center")
ax.plot(np.median(np.array(P), axis=0), color=BLUE, lw=2.8, label="median of the ten"); ax.axhline(0, color=INK2, lw=0.8)
for h in (63, 126, 252): ax.axvline(h, color=INK2, lw=0.5, ls=":")
ax.set_xlim(0, 282); ax.set_xlabel("trading days after the stretch"); ax.set_ylabel("S&P 500, % change"); ax.legend(frameon=False, loc="upper left", fontsize=10)
ax.set_title("The ten most similar past markets, and what followed", loc="left", fontsize=12.5, fontweight="bold", color=INK)
fig.tight_layout(); fig.savefig(FIG / "fig3_analogs.png"); plt.close(fig); stamp("fig3")

# ---------------------------------------------------------------- posters (film: A Night to Remember, 1958)
from poster import BOLD, DIM, poster   # noqa: E402
from poster import INK as PINK         # noqa: E402
import os
NO, REL = os.environ.get("A68_NO", "1½"), os.environ.get("A68_RELEASE", "SPECIAL SCREENING  ·  25 NOVEMBER 2026")
CR = ("FEATURING  THE S&P 500 SINCE 1950, EIGHT AI LEADERS, 26 CORRECTIONS\n"
      "A SEQUEL TO  TITANIC  ·  FORWARD RECORD SIGNED 21 NOVEMBER 2026, MARKET CLOSED")
def sinking(ax, acc, answer):
    x = range(len(s))
    ax.plot(x, s.spy.values, color=DIM, lw=4); ax.plot(x, s.basket.values, color=acc, lw=5.5)
    ax.axhline(100, color=DIM, lw=1.2, ls=(0, (4, 4)))
    ax.text(0, 101.2, "6 OCT: TITANIC PUBLISHED, S&P 500 AT ITS HIGH", color=DIM, fontproperties=BOLD, fontsize=14, va="bottom")
    ax.text(len(s) - 0.6, s.spy.iloc[-1], f"  S&P 500 (SPY)\n  {s.spy.iloc[-1] - 100:+.1f}%" if answer else "  S&P 500 (SPY)", color=DIM, fontproperties=BOLD, fontsize=15, va="center")
    ax.text(len(s) - 0.6, s.basket.iloc[-1], f"  AI leaders\n  {s.basket.iloc[-1] - 100:+.1f}%" if answer else "  AI leaders\n  next ?", color=PINK, fontproperties=BOLD, fontsize=17, va="center")
    ax.set_xlim(-0.5, len(s) + 8.5); ax.set_ylim(72, 104); ax.set_xticks([]); ax.set_yticks([80, 90, 100]); ax.tick_params(labelsize=13)
poster(FIG / "hero_a_night_to_remember.png", NO, "A NIGHT\nTO REMEMBER", "My tests gave no warning. The next ones are signed.",
       lambda ax, acc: sinking(ax, acc, True), CR, "RATED  TWO TESTS AND ONE RECORD REGISTERED  ·  FIRST SCORE 19 FEBRUARY 2027", REL, accent="#3987e5", title_size=74)
poster(FIG / "hero_a_night_to_remember_teaser.png", NO, "A NIGHT\nTO REMEMBER", "What did my own tests miss, and why?",
       lambda ax, acc: sinking(ax, acc, False), CR, "RATED  SIGNED BEFORE MONDAY'S OPEN  ·  THE RECORD IS IN THE ARTICLE", REL, accent="#3987e5", title_size=74)
stamp("posters")
