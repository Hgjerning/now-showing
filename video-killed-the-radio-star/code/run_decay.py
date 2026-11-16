# -*- coding: utf-8 -*-
"""A08 Video Killed the Radio Star: McLean-Pontiff style publication decay on 29 JKP US factors."""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "_shared", "lib10")); sys.path.insert(0, "/home/claude/lib10")
from stats import nw_t  # noqa: E402

D, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, "results"); os.makedirs(OUT, exist_ok=True)
GATE = 0.025
PUB = {  # factor: (label, paper, year)
    "market_equity": ("Size", "Banz", 1981), "be_me": ("Book/market", "Rosenberg, Reid & Lanstein", 1985),
    "ni_me": ("Earnings/price", "Basu", 1977), "sale_me": ("Sales/price", "Barbee, Mukherji & Raines", 1996),
    "div12m_me": ("Dividend yield", "Litzenberger & Ramaswamy", 1979), "ret_12_1": ("Momentum 12-1", "Jegadeesh & Titman", 1993),
    "ret_12_7": ("Momentum 12-7", "Novy-Marx", 2012), "ret_1_0": ("Short-term reversal", "Jegadeesh", 1990),
    "ret_60_12": ("Long-term reversal", "De Bondt & Thaler", 1985), "resff3_12_1": ("Residual momentum", "Blitz, Huij & Martens", 2011),
    "seas_1_1an": ("Seasonality", "Heston & Sadka", 2008), "prc_highprc_252d": ("52-week high", "George & Hwang", 2004),
    "gp_at": ("Gross profitability", "Novy-Marx", 2013), "ope_be": ("Operating profitability", "Fama & French", 2015),
    "cop_at": ("Cash-based profitability", "Ball et al.", 2016), "qmj": ("Quality minus junk", "Asness, Frazzini & Pedersen", 2019),
    "f_score": ("Piotroski F-score", "Piotroski", 2000), "o_score": ("Ohlson O-score", "Dichev", 1998),
    "oaccruals_at": ("Accruals", "Sloan", 1996), "noa_at": ("Net operating assets", "Hirshleifer et al.", 2004),
    "at_gr1": ("Asset growth", "Cooper, Gulen & Schill", 2008), "chcsho_12m": ("Net share issuance", "Pontiff & Woodgate", 2008),
    "niq_su": ("Earnings surprise", "Foster, Olsen & Shevlin", 1984), "rd_me": ("R&D/market", "Chan, Lakonishok & Sougiannis", 2001),
    "ivol_ff3_21d": ("Idiosyncratic volatility", "Ang et al.", 2006), "rmax1_21d": ("MAX (lottery)", "Bali, Cakici & Whitelaw", 2011),
    "betabab_1260d": ("Betting against beta", "Frazzini & Pedersen", 2014), "ami_126d": ("Amihud illiquidity", "Amihud", 2002),
    "turnover_126d": ("Share turnover", "Datar, Naik & Radcliffe", 1998),
}


def pooled(J, years):
    """Stacked regression r = a_i + b*post + e; SE clustered by month. Returns b, t, mean pre (pooled avg of factor means)."""
    rows = []
    for f, y in years.items():
        s = J[f].dropna(); rows.append(pd.DataFrame({"f": f, "r": s.values, "post": (s.index.year > y).astype(float), "m": s.index}))
    Z = pd.concat(rows, ignore_index=True)
    Z["r_dm"] = Z.r - Z.groupby("f").r.transform("mean"); Z["p_dm"] = Z.post - Z.groupby("f").post.transform("mean")
    b = (Z.p_dm * Z.r_dm).sum() / (Z.p_dm ** 2).sum()
    Z["u"] = Z.r_dm - b * Z.p_dm
    g = (Z.p_dm * Z.u).groupby(Z.m).sum()
    se = np.sqrt((g ** 2).sum()) / (Z.p_dm ** 2).sum()
    return float(b), float(b / se)


def main():
    J = pd.read_csv(os.path.join(D, "jkp_usa_factors_monthly.csv"), index_col=0, parse_dates=True)[list(PUB)]
    J = J.loc[:"2025-12-31"]
    years = {f: v[2] for f, v in PUB.items()}
    rows = []
    for f, (lab, paper, y) in PUB.items():
        s = J[f].dropna(); pre, post = s[s.index.year <= y], s[s.index.year > y]
        rows.append(dict(factor=f, label=lab, paper=paper, year=y, first=str(s.index[0].date()), pre_n=len(pre), post_n=len(post),
                         pre_ann=pre.mean() * 12, post_ann=post.mean() * 12, pre_t=nw_t(pre, 6)["t"], post_t=nw_t(post, 6)["t"] if len(post) > 12 else np.nan,
                         decay=1 - post.mean() / pre.mean() if pre.mean() > 0 else np.nan))
    T = pd.DataFrame(rows).set_index("factor"); T.to_csv(os.path.join(OUT, "decay_by_factor.csv"))
    b, t = pooled(J, years)
    pre_avg = float(T.pre_ann.mean() / 12)
    S = {"A08-1": {"coef_monthly": b, "coef_ann": b * 12, "t": t, "p_lt": float(st.norm.cdf(t)), "pre_mean_ann": pre_avg * 12,
                   "decay_share": float(-b / pre_avg), "passed": bool(st.norm.cdf(t) < GATE)}}
    # A08-2: equal-weighted average across factors in their post-publication months
    post = pd.DataFrame({f: J[f].where(J.index.year > y) for f, y in years.items()})
    ew = post.mean(axis=1).dropna(); a2 = nw_t(ew, 6)
    S["A08-2"] = {**a2, "ann": a2["mean"] * 12, "first": str(ew.index[0].date()), "passed": bool(a2["p_gt"] < GATE)}
    # placebo: random publication years drawn within each factor's own sample (keep >= 10 years each side)
    rng = np.random.default_rng(42); pb = []
    for _ in range(1000):
        ry = {}
        for f in years:
            s = J[f].dropna(); lo, hi = s.index.year.min() + 10, 2015
            ry[f] = int(rng.integers(lo, hi + 1))
        pb.append(pooled(J, ry)[0])
    pb = np.array(pb)
    S["reported"] = {"placebo_coef_mean_ann": float(pb.mean() * 12), "placebo_share_below_actual": float((pb <= b).mean()),
                     "share_positive_post": float((T.post_ann > 0).mean()), "median_decay": float(T.decay.median()),
                     "n_factors": len(T), "share_decayed": float((T.post_ann < T.pre_ann).mean())}
    np.save(os.path.join(OUT, "placebo_coef.npy"), pb)
    ew.to_csv(os.path.join(OUT, "post_pub_ew.csv"), header=["ret"])
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=2)
    print(T[["label", "year", "pre_ann", "post_ann", "decay"]].round(3).to_string()); print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
