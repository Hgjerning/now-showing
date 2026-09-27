# -*- coding: utf-8 -*-
"""Common ground across segments and signals: price battery (19 signals x 6 universes, our engine)
and JKP battery (153 published factors x 5 segments). Writes results/common_ground.json and figures."""
import json
import os

import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats as sst
from scipy.cluster.hierarchy import linkage, fcluster, leaves_list
from scipy.spatial.distance import squareform
from sklearn.metrics import adjusted_rand_score

import perf
from battery import DIRECTION, SIGS
from jkp_battery import bh, SEG
from nbh_figs import DIV

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "..", "results"); FIG = os.path.join(HERE, "..", "figures")
U = ["US", "EU", "UK", "DK", "SC", "WD"]; UN = {"US": "US", "EU": "EU", "UK": "UK", "DK": "DK", "SC": "SCANDI", "WD": "World"}
SURF, INK, INK2, BLUE, ORANGE, GREY = "#fcfcfb", "#0b0b0b", "#52514e", "#2a78d6", "#eb6834", "#8a8984"
LAB = {s: DIRECTION[s][2] for s in SIGS}
# JKP stand-in for each of our universes (EU and SCANDI are proxies)
JMAP = {"US": "usa", "UK": "gbr", "DK": "dnk", "WD": "world", "EU": "world_ex_us", "SC": "world_ex_us"}
REPL = {"mom": "ret_12_1", "resmom": "resff3_12_1", "r1": "ret_1_0", "size": "market_equity", "vol": "rvol_21d", "ivol": "ivol_capm_21d",
        "beta": "beta_60m", "max1": "rmax1_21d", "max5": "rmax5_21d", "skew": "rskew_21d", "hi52": "prc_highprc_252d", "seas": "seas_1_1an"}
# themes that link our price signals to JKP clusters
THEMES = [("Momentum", ["mom", "resmom", "hi52", "lo52"], "Momentum"),
          ("Low risk", ["vol", "vol252", "ivol", "beta"], "Low Risk"),
          ("Lottery & tails (size of tails)", ["max1", "max5", "min1", "min5", "range"], None),
          ("Tail direction (skewness)", ["skew", "asym"], None),
          ("Short-term reversal", ["r1"], "Short-Term Reversal"),
          ("Seasonality", ["seas"], "Seasonality"),
          ("Size", ["size"], "Size"),
          ("Breakout", ["brk55"], None),
          ("Value", [], "Value"), ("Quality", [], "Quality"), ("Profitability", [], "Profitability"), ("Profit growth", [], "Profit Growth"),
          ("Investment", [], "Investment"), ("Debt issuance", [], "Debt Issuance"), ("Accruals", [], "Accruals"), ("Low leverage", [], "Low Leverage")]
JDIS = ["usa", "gbr", "dnk", "world_ex_us"]


def pooled(dfs):
    """dfs: {universe: series}. Equal-weight average; t of the average includes the co-movement."""
    df = pd.DataFrame(dfs).dropna(); x = df.mean(axis=1); C = df.corr().values
    return dict(ann=float(x.mean() * 12), sharpe=perf.sharpe(x), t=perf.nw_t(x)["t"], pos=int((df.mean() > 0).sum()), neff=float(len(df.columns) ** 2 / C.sum()),
                design=perf.sharpe(x.loc[:"2019-12-31"]), holdout=perf.sharpe(x.loc["2020-01-01":])), x


def clusters(corr, cut=0.5):
    d = 1 - corr.values; np.fill_diagonal(d, 0); d = (d + d.T) / 2
    Z = linkage(squareform(d, checks=False), "average"); return fcluster(Z, cut, "distance"), Z


def run():
    B = pd.read_pickle(os.path.join(RES, "battery_price.pkl")); J = json.load(open(os.path.join(RES, "battery_price.json")))["stats"]
    JK = pd.read_pickle(os.path.join(RES, "battery_jkp.pkl"))
    F = {s: pd.read_csv(os.path.join(HERE, "..", "factors", f"jkp_{s}_factors_monthly.csv"), index_col=0, parse_dates=True) for s in SEG}
    # financing of net long cash is now charged inside xs.run (27 Sep 2026); bn_net already includes it
    out = {}
    # 1. pooled evidence per price signal, raw and beta-neutral
    PS = {}; series = {}
    for s in SIGS:
        a, xa = pooled({R: B[R][s].ls_net for R in U}); b, xb = pooled({R: B[R][s].bn_net for R in U})
        lo = sum(J[R][s]["lo_minus_ew_sharpe"] > 0 for R in U)
        PS[s] = dict(label=LAB[s], family=DIRECTION[s][1], raw=a, bn=b, lo_beats=int(lo), cost=float(np.mean([J[R][s]["cost"] for R in U])),
                     sh={R: J[R][s]["sharpe"] for R in U}, bn_sh={R: perf.sharpe(B[R][s].bn_net.dropna()) for R in U}, t_alpha={R: J[R][s]["t_alpha"] for R in U})
        series[s] = (xa, xb)
    p = np.array([2 * (1 - sst.norm.cdf(abs(PS[s][k]["t"]))) for s in SIGS for k in ("raw", "bn")]); d = bh(p)
    for i, s in enumerate(SIGS):
        PS[s]["raw"]["bh"] = bool(d[2 * i]); PS[s]["bn"]["bh"] = bool(d[2 * i + 1])
    out["price"] = PS
    # 2. correlation structure: average across universes, clusters, stability (ARI)
    CR = {R: pd.DataFrame({s: B[R][s].bn_net for s in SIGS}).corr() for R in U}
    avg = sum(CR.values()) / len(U); lab_all, Z = clusters(avg)
    ari = {R: float(adjusted_rand_score(lab_all, clusters(CR[R])[0])) for R in U}
    groups = {}
    for s, g in zip(SIGS, lab_all):
        groups.setdefault(int(g), []).append(s)
    out["clusters"] = dict(groups=groups, ari=ari)
    # 3. do the segments agree on which signals work? Spearman of Sharpe vectors (beta-neutral)
    SH = pd.DataFrame({R: {s: perf.sharpe(B[R][s].bn_net.dropna()) for s in SIGS} for R in U}); agree = SH.corr(method="spearman")
    out["agree_price"] = agree.round(3).to_dict(); out["agree_price_mean"] = {R: float(agree[R].drop(R).mean()) for R in U}
    ag_j = JK["agree"]; out["agree_jkp"] = ag_j.round(3).to_dict(); out["agree_jkp_mean"] = {s: float(ag_j[s].drop(s).mean()) for s in SEG}
    # 4. replication: our L/S vs the JKP factor in the matched segment
    RP = {}
    for s, k in REPL.items():
        RP[s] = {}
        for R in U:
            ours = B[R][s].ls_gross.copy(); ours.index = ours.index.to_period("M"); j = F[JMAP[R]][k].copy(); j.index = j.index.to_period("M")
            df = pd.concat([ours, j], axis=1).dropna().loc["2013-02":"2025-12"]
            RP[s][R] = float(df.corr().iloc[0, 1])
    out["replication"] = RP
    # 5. themes: price composite (EW of member signals, beta-neutral) + JKP cluster in 4 disjoint segments
    TH = []
    CL = JK["CL"]
    for name, sigs, jc in THEMES:
        row = dict(theme=name, signals=sigs, jkp=jc)
        if sigs:
            comp = {R: pd.concat([B[R][s].bn_net for s in sigs], axis=1).mean(axis=1) for R in U}
            row["price"], _ = pooled(comp)
            row["price_sh"] = {R: perf.sharpe(comp[R].dropna()) for R in U}
        if jc:
            row["jkp_sh"] = {s: float(CL.loc[(s, jc), "sharpe"]) for s in SEG}; row["jkp_pre"] = {s: float(CL.loc[(s, jc), "pre_sharpe"]) for s in SEG}
            facs = [k for k in JK["facs"] if JK["cl"][k] == jc]
            comp = {s: F[s][facs].loc["2013-01":"2025-12"].mean(axis=1) for s in JDIS}
            row["jkp"], _ = pooled(comp)
            P = JK["P"]; row["jkp_bh"] = int(P[P.cluster == jc].bh.sum()); row["jkp_n"] = int((P.cluster == jc).sum())
        TH.append(row)
    for r in TH:
        pr, jk = r.get("price"), r.get("jkp")
        srcs = [x for x in (pr, jk) if x]; full = {id(pr): 6, id(jk): 4}
        allpos = all(x["pos"] == full[id(x)] for x in srcs); sig_any = any(x["t"] > 2 for x in srcs); sig_all = all(x["t"] > 2 for x in srcs)
        if allpos and sig_all:
            v = "Common ground (significant in both sources)" if len(srcs) == 2 else "Common ground (significant; JKP only)"
        elif allpos and sig_any:
            v = "Common ground (positive everywhere, significant in " + ("JKP" if jk and jk["t"] > 2 else "our data") + ")"
        elif any(x["t"] < -2 for x in srcs):
            v = "Reliably negative"
        elif all(x["t"] > 0 for x in srcs) and sum(x["pos"] for x in srcs) >= sum(full[id(x)] for x in srcs) - 1:
            v = "Positive almost everywhere, not significant"
        elif any(x["t"] > 2 for x in srcs):
            v = "Works pooled, not everywhere"
        else:
            v = "No common ground"
        if jk and r["jkp_pre"]["usa"] > 0.3 and r["jkp_sh"]["usa"] < 0.15:
            v += " · faded in the US"
        r["verdict"] = v
    out["themes"] = TH
    out["jkp_summary"] = dict(n=int(len(JK["P"])), bh=int(JK["P"].bh.sum()), hlz=int(JK["P"].hlz.sum()), co=JK["co"],
                              top=JK["P"].sort_values("t", ascending=False).head(12)[["cluster", "ann", "sharpe", "t", "pos", "neff", "pre_ann", "bh"]].reset_index().rename(columns={"index": "factor"}).to_dict("records"))
    json.dump(out, open(os.path.join(RES, "common_ground.json"), "w"), indent=1, default=float)
    figs(PS, avg, Z, CL, TH, RP, agree, ag_j)
    return out


def figs(PS, avg, Z, CL, TH, RP, agree, ag_j):
    # A: heatmap raw and beta-neutral Sharpe, 19 x 6, ordered by the cluster tree
    order = [SIGS[i] for i in leaves_list(Z)]
    fig, axs = plt.subplots(1, 2, figsize=(13, 8)); fig.patch.set_facecolor(SURF)
    for ax, key, title in ((axs[0], "sh", "Long/short Sharpe, net"), (axs[1], "bn_sh", "Beta-neutral L/S Sharpe, after costs and financing")):
        M = np.array([[PS[s][key][R] for R in U] for s in order])
        ax.imshow(M, cmap=DIV, vmin=-1, vmax=1, aspect="auto"); ax.set_title(title, loc="left", fontsize=12)
        ax.set_xticks(range(6)); ax.set_xticklabels([UN[R] for R in U]); ax.set_yticks(range(len(order))); ax.set_yticklabels([LAB[s] for s in order], fontsize=9); ax.grid(False)
        for i in range(M.shape[0]):
            for j in range(6):
                ax.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=7.5, color=INK)
    fig.suptitle("19 price signals × 6 markets, 2013–2026 (rows ordered by return similarity)", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs13_price_heatmap.png"), dpi=140, facecolor=SURF); plt.close(fig)
    # B: average correlation matrix
    fig, ax = plt.subplots(figsize=(8.5, 7.5)); fig.patch.set_facecolor(SURF)
    M = avg.loc[order, order].values; ax.imshow(M, cmap=DIV, vmin=-1, vmax=1); ax.grid(False)
    ax.set_xticks(range(len(order))); ax.set_xticklabels([LAB[s] for s in order], rotation=90, fontsize=8); ax.set_yticks(range(len(order))); ax.set_yticklabels([LAB[s] for s in order], fontsize=8)
    ax.set_title("Correlation of beta-neutral long/short returns, average of 6 markets", loc="left", fontsize=11)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs13_corr.png"), dpi=140, facecolor=SURF); plt.close(fig)
    # C: JKP clusters x segments, 2013-25 vs before
    cl = sorted(set(c for _, c in CL.index)); segs = list(SEG)
    fig, axs = plt.subplots(1, 2, figsize=(12, 6.5)); fig.patch.set_facecolor(SURF)
    for ax, key, title in ((axs[0], "pre_sharpe", "Before 2013 (each segment's own history)"), (axs[1], "sharpe", "2013–2025")):
        M = np.array([[CL.loc[(s, c), key] for s in segs] for c in cl])
        ax.imshow(M, cmap=DIV, vmin=-1.2, vmax=1.2, aspect="auto"); ax.set_title(title, loc="left", fontsize=12); ax.grid(False)
        ax.set_xticks(range(len(segs))); ax.set_xticklabels([SEG[s] for s in segs], fontsize=9); ax.set_yticks(range(len(cl))); ax.set_yticklabels(cl, fontsize=9)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                ax.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=8, color=INK)
    fig.suptitle("JKP's 13 themes (153 published factors, equal-weighted within theme): Sharpe ratio by segment", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs13_jkp_themes.png"), dpi=140, facecolor=SURF); plt.close(fig)
    # D: common ground map: pooled t price (x) vs pooled t JKP (y) per theme
    fig, ax = plt.subplots(figsize=(9, 6.5)); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    jonly = sorted([r for r in TH if r.get("jkp") and not r.get("price")], key=lambda r: r["jkp"]["t"]); last = -99
    for r in jonly:
        y = r["jkp"]["t"]; ly = max(y, last + 0.38); last = ly
        ax.scatter(-4.6, y, s=60, color=GREY, marker="s", zorder=3); ax.annotate(f"{r['theme']} ({y:+.1f})", (-4.6, y), xytext=(-4.35, ly - 0.1), textcoords="data", fontsize=8.5, color=INK2,
                                                                                 arrowprops=dict(arrowstyle="-", color=GREY, lw=0.5) if abs(ly - y) > 0.05 else None)
    for r in TH:
        x = r["price"]["t"] if r.get("price") else None; y = r["jkp"]["t"] if r.get("jkp") else None
        if x is not None and y is not None:
            ax.scatter(x, y, s=90, color=BLUE, zorder=3); ax.annotate(r["theme"], (x, y), xytext=(6, 4), textcoords="offset points", fontsize=9)
        elif x is not None:
            ax.scatter(x, -3.6, s=60, color=ORANGE, marker="D", zorder=3); ax.annotate(r["theme"], (x, -3.6), xytext=(4, 6), textcoords="offset points", fontsize=8.5, color=INK2, rotation=20)
    for v in (-2, 2):
        ax.axvline(v, color=GREY, lw=0.8, ls=":"); ax.axhline(v, color=GREY, lw=0.8, ls=":")
    ax.axvline(0, color=INK2, lw=1); ax.axhline(0, color=INK2, lw=1); ax.set_xlim(-5, 6); ax.set_ylim(-4, 7)
    ax.set_xlabel("Our price engine: t of the 6-market average (beta-neutral, net of costs and financing)"); ax.set_ylabel("JKP: t of the 4-segment average (US, UK, DK, World ex US)")
    ax.text(5.9, 6.6, "blue: in both sources", fontsize=8.5, color=BLUE, ha="right"); ax.text(5.9, 6.2, "grey squares (left): fundamentals, JKP only", fontsize=8.5, color=INK2, ha="right"); ax.text(5.9, 5.8, "orange diamonds (bottom): price only", fontsize=8.5, color=ORANGE, ha="right")
    ax.set_title("Common ground: themes that work in both our data and the published factors", loc="left", fontsize=12)
    for sp_ in ax.spines.values(): sp_.set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs13_common_map.png"), dpi=140, facecolor=SURF); plt.close(fig)
    # E: replication bars
    fig, ax = plt.subplots(figsize=(10, 5)); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    ks = list(RP); w = 0.13; cols = ["#2a78d6", "#8ab4ea", "#eb6834", "#f3b393", "#52514e", "#b5b4ae"]
    for j, R in enumerate(U):
        ax.bar(np.arange(len(ks)) + (j - 2.5) * w, [RP[k][R] for k in ks], w, color=cols[j], label=UN[R] + (" (proxy: World ex US)" if R in ("EU", "SC") else ""))
    ax.set_xticks(range(len(ks))); ax.set_xticklabels([LAB[k] for k in ks], rotation=35, ha="right", fontsize=8.5); ax.axhline(0, color=INK2, lw=1); ax.axhline(0.7, color=GREY, lw=0.8, ls=":")
    ax.set_ylabel("correlation, monthly, 2013–2025"); ax.legend(fontsize=7.5, ncol=3, frameon=False); ax.set_title("Replication: our long/short (gross) vs the matching JKP factor", loc="left", fontsize=12)
    for sp_ in ax.spines.values(): sp_.set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fs13_replication.png"), dpi=140, facecolor=SURF); plt.close(fig)


if __name__ == "__main__":
    o = run()
    for s, v in o["price"].items():
        print(f"{v['label']:28s} raw t {v['raw']['t']:+.2f} pos {v['raw']['pos']}  bn t {v['bn']['t']:+.2f} pos {v['bn']['pos']} bh {v['bn']['bh']} lo {v['lo_beats']}")
    print(o["clusters"]); print(o["agree_price_mean"]); print(o["agree_jkp_mean"])
    for k, v in o["replication"].items(): print(k, {R: round(x, 2) for R, x in v.items()})
    for r in o["themes"]:
        print(r["theme"], r["verdict"], round(r["price"]["t"], 2) if r.get("price") else "-", round(r["jkp"]["t"], 2) if r.get("jkp") else "-")
