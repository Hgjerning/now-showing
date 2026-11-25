# -*- coding: utf-8 -*-
"""A68: the dated update box, the byline note and the post paragraph, written from results/update_after_signing.json
(24 Nov 2026). Text only; every number comes from that file. Used by build_article.py."""
import pandas as pd

def _d(s, wd=False):
    d = pd.Timestamp(s); return (f"{d:%A} " if wd else "") + f"{d.day} {d:%B}"
def _pc(v, d=1): return f"{v * 100:+.{d}f}%".replace("-", "−")
def _down(v): assert v < 0, v; return f"{-v * 100:.1f}%"

def render(U, published="25 November 2026"):
    ix, st, ss, mo = U["index"], U["since_titanic"], U["since_signature"], U["monday"]; k = U["trading_days_since_signature"]
    best = pd.Timestamp(ix["monday_best_day_since"]); nv = mo["names"]["NVDA"]
    state = "no longer 10% down" if ix["below_peak"] > -0.10 else "again more than 10% down"
    side = "above" if ix["since_20_nov"] >= 0 else "below"; days = "one trading day" if k == 1 else f"{k} trading days"
    box = (f"> **Update, {published}: what happened after I signed.** This article was written on prices to Friday 20 November, and nothing below this box has been changed. "
           f"On Monday 23 November Nvidia's board reinstated the chief executive who had resigned on 12 November. Nvidia rose {nv * 100:.1f}% that day and the S&P 500 {ix['monday_return'] * 100:.1f}%, "
           f"its best day since {best.day} {best:%B %Y}. At the close of {_d(U['as_of'], True)} the index stood at {ix['close']:,.2f}, {_down(ix['below_peak'])} below the high of 6 October and {state}. "
           f"The basket of eight is {_down(st['basket'])} below 6 October (it was 23.8% on Friday) and Nvidia {_down(st['names']['NVDA'])} (it was 47.5%). "
           f"My tests did not see this coming either: nothing I had signed says anything about a single day. Three things for the reader. "
           f"The count in section 4 starts from the first close 10% below a high, which was Friday; in {U['low_on_first_day_cases']} of the 26 earlier cases that day was also the low, so a rebound from it is one of the ordinary outcomes. "
           f"The forward record in section 5 was signed, and committed in public, before Monday's open and starts from Friday's close: after {days} the S&P 500 is {abs(ix['since_20_nov']) * 100:.1f}% {side} it, "
           f"against the {_pc(U['line2_3m']['analogs_score_above'])} the analog forecast needs at three months, and the basket is {_pc(ss['basket_equal_weight'])} against {_pc(ss['spy'])} for SPY. "
           f"That is {days} of a year, and I read nothing into it. And the line in section 6 that a rally may settle nothing was written before this one.")
    byline = f" · update box to the close of {_d(U['as_of'])} 2026"
    post = (f"On Monday Nvidia's chief executive came back and the stock rose {nv * 100:.0f}% in a day. My tests did not see that coming either.")
    return box, byline, post
