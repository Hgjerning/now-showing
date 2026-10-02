# -*- coding: utf-8 -*-
"""US 1999-2012 on Sharadar, as pre-registered in planning/PREREG_US_1999_2012.md (written 2026-10-02, before any run).

Same engines and metrics as the 2013-2026 factsheets; only the window and the US data path change. Writes to
results_us1999/ so nothing published is touched. Steps (each cached; rerun skips finished ones):
    python us1999_run.py xs       T1: FS03-FS12, X0 baseline (as analyse_xs.py)
    python us1999_run.py turtle   T1: FS01 (as run_turtle.py + analyse.run_turtle_all)
    python us1999_run.py lottery  T1: FS02 (as run_lottery.py + analyse.run_lottery_all)
    python us1999_run.py report   T1 verdict table vs the 2013-2026 values frozen in the pre-registration
"""
import json, os, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent; FS = HERE.parent
P2 = FS.parent.parent / "Project2 Investment Strategy" / "reporting" / "sharadar_cache" / "backfill_1998"
SENS = os.environ.get("US1999_SENS", "")   # "" | "delist" | "lag"  (section 6 sensitivities)
OUT = FS / "results_us1999" / (f"sens_{SENS}" if SENS else ""); OUT.mkdir(parents=True, exist_ok=True)
if SENS == "delist":
    os.environ.update(FS_DELIST_HAIRCUT="0.30", FS_DELIST_TICKERS=str(P2 / "delist_bankrupt_tickers.json"))
elif SENS == "lag":
    os.environ.update(FS_US_LAG="2")
os.environ.update(FS_DATA=str(FS / "_data_private" / "us1998"), FS_SP500_HISTORY=str(P2 / "sp500_events_full.csv"),
                  FS_SP500_START="1990-01-01", FS_START="1998-01-01", FS_END="2012-12-31", FS_US_UNIVERSE="sp500_pit",
                  FS_RESULTS=str(OUT), MPLBACKEND="Agg", P10_PIT=str(FS / "_data_private" / "us1998" / "pit"))
import numpy as np, pandas as pd   # noqa: E402
import data, xs, specs, analyse, perf   # noqa: E402

data.REGIONS = ["US"]
xs.START, xs.END = pd.Period("1998-12"), pd.Period("2012-11")      # first return month 1999-01, last 2012-12
analyse.END_M = "2012-12-31"
R = "US"
FROZEN = {  # 2013-2026 US values copied into PREREG_US_1999_2012.md section 5, T1 (L/S net t, long-only alpha t)
    "FS01": (-3.96, -1.38), "FS02": (-2.17, 0.29), "FS03": (0.31, 1.74), "FS04": (-1.36, 1.73), "FS06": (-2.83, -3.17),
    "FS07": (-0.55, -2.66), "FS08": (-1.62, -4.06), "FS09": (-1.00, 0.05), "FS10": (1.17, 1.93), "FS11": (1.22, 2.30), "FS12": (-3.07, -2.94)}
HALVES = (("1999-01-01", "2005-12-31"), ("2006-01-01", "2012-12-31"))


def cell(ls, lo, ew):
    """The two registered statistics + sub-periods; same function as the factsheets (analyse.metrics -> perf.summary)."""
    a = analyse.metrics(None, monthly=ls.dropna(), bench_m=ew); b = analyse.metrics(None, monthly=lo.dropna(), bench_m=ew)
    sub = {}
    for h0, h1 in HALVES:
        x, y, e = ls.loc[h0:h1].dropna(), lo.loc[h0:h1].dropna(), ew.loc[h0:h1]
        sub[h0[:4]] = dict(ls_t=perf.nw_t(x)["t"], lo_alpha_t=perf.summary(y, e).get("t_alpha"))
    return dict(months=a["months"], start=a["start"], end=a["end"], ls_t=a["t_mean"], ls_sharpe=a["sharpe"], ls_ann=a["ann_mean"],
                lo_alpha_t=b["t_alpha"], lo_alpha=b["alpha"], lo_sharpe=b["sharpe"], ew_sharpe=perf.sharpe(ew.dropna()), sub=sub)


def save(name, d):
    json.dump(d, open(OUT / f"{name}.json", "w"), indent=1, default=float)


def step_xs():
    f = OUT / "t1_xs.json"; done = json.load(open(f)) if f.exists() else {}
    I = xs.inputs(R)
    for code in specs.ORDER:
        if code in done: continue
        sp = specs.S[code]
        P = xs.run(I, sp["sig"], sp["long_high"], sp["construction"])
        P.to_pickle(OUT / f"xs_{code}.pkl")
        done[code] = cell(P.ls_net, P.good_net, P.ew); save("t1_xs", done)
        print(code, {k: round(v, 2) for k, v in done[code].items() if k in ("ls_t", "lo_alpha_t", "months")}, flush=True)


def step_turtle():
    import turtle
    o = data.load(R); res = {}
    for name, kw in [("S1", dict(system=1)), ("S2", dict(system=2)), ("S1_long", dict(system=1, allow_short=False)), ("S2_long", dict(system=2, allow_short=False))]:
        p = OUT / f"turtle_{name}.pkl"
        if p.exists(): res[name] = pd.read_pickle(p); continue
        res[name] = turtle.run(o["ret"], o["elig"], start="1999-01-01", **kw); pd.to_pickle(res[name], p); print("turtle", name, flush=True)
    ew = perf.to_monthly(o["ret"].where(o["elig"]).mean(axis=1).loc["1999-01-01":]).loc[:"2012-12-31"]
    ls = perf.to_monthly(0.5 * res["S1"]["ret"] + 0.5 * res["S2"]["ret"]).loc[:"2012-12-31"]
    lo = perf.to_monthly(0.5 * res["S1_long"]["ret"] + 0.5 * res["S2_long"]["ret"]).loc[:"2012-12-31"]
    save("t1_turtle", {"FS01": cell(ls, lo, ew)}); print("FS01 done", flush=True)


def step_lottery():
    import lottery
    o = data.load(R); p = OUT / "lottery_max1.pkl"
    P = pd.read_pickle(p) if p.exists() else lottery.build(o, start="1998-12-31", R=R)[0]
    P.to_pickle(p); P = P.loc["1999-01-31":"2012-12-31"]
    save("t1_lottery", {"FS02": cell(P.ls_net, P.low_net, P.EW)}); print("FS02 done", flush=True)


def verdict(t_old, t_new):
    if abs(t_old) < 1: return "no prior"
    if np.sign(t_old) != np.sign(t_new): return "reversed"
    return "confirmed" if abs(t_new) > 2 else "consistent"


def step_costs():
    """Section 6.2: costs doubled before April 2001 (FS03-FS12; xs keeps the cost column)."""
    out = {}
    for code in specs.ORDER:
        P = pd.read_pickle(OUT / f"xs_{code}.pkl"); pre = P.index < pd.Timestamp("2001-04-01")
        ls = P.ls_net - P.cost.where(pre, 0.0); lo = P.good_net - (xs.COST * P.to_good).where(pre, 0.0)
        out[code] = cell(ls, lo, P.ew)
    save("t1_xs_costs2x", out); print({k: (round(v["ls_t"], 2), round(v["lo_alpha_t"], 2)) for k, v in out.items()})


def step_report():
    allc = {}
    for n in ("t1_turtle", "t1_lottery", "t1_xs"):
        if (OUT / f"{n}.json").exists(): allc.update(json.load(open(OUT / f"{n}.json")))
    rows = ["| Factsheet | Months | L/S t 2013-26 | L/S t 1999-2012 | Verdict | LO alpha t 2013-26 | LO alpha t 1999-2012 | Verdict | New edge (abs t > 2.87) |", "|---|---|---|---|---|---|---|---|---|"]
    for code in sorted(FROZEN):
        if code not in allc: rows.append(f"| {code} | not run | | | | | | | |"); continue
        c = allc[code]; a, b = FROZEN[code]
        new = [lab for lab, t in (("L/S", c["ls_t"]), ("LO", c["lo_alpha_t"])) if abs(t) > 2.87]
        rows.append(f"| {code} | {c['months']} | {a:+.2f} | {c['ls_t']:+.2f} | {verdict(a, c['ls_t'])} | {b:+.2f} | {c['lo_alpha_t']:+.2f} | {verdict(b, c['lo_alpha_t'])} | {', '.join(new) or '-'} |")
    txt = "\n".join(rows); (OUT / "T1_verdicts.md").write_text(txt, encoding="utf-8"); print(txt)


# ---------------- T2 FS13 price battery, T3 FS13b fundamental battery, T4 FS13c Fama-MacBeth ----------------
RES0 = FS / "results"   # the 2013-2026 values the signs are compared with (read, never written)


def sign_test(old, new, need):
    rows, keep = {}, 0
    for s in old:
        if s not in new: rows[s] = dict(old=old[s], new=None, same=None); continue
        same = bool(np.sign(old[s]) == np.sign(new[s])); keep += same
        rows[s] = dict(old=old[s], new=new[s], same=same)
    return dict(rows=rows, kept=keep, n=len(old), need=need, passed=keep >= need)


def step_battery():
    import battery as BT
    f = OUT / "battery_US.pkl"
    B = pd.read_pickle(f) if f.exists() else BT.one(R)
    pd.to_pickle(B, f)
    new = {s: BT.stats(B[s].loc["1999-01-31":"2012-12-31"])["bn_t"] for s in BT.SIGS}
    old = {s: v["bn_t"] for s, v in json.load(open(RES0 / "battery_price.json"))["stats"]["US"].items()}
    out = sign_test(old, new, 14); save("t2_battery", out); print("T2", out["kept"], "of", out["n"], "passed" if out["passed"] else "failed")


def step_fund():
    import fund_battery as FB
    f = OUT / "fund_battery.pkl"
    if f.exists():
        out = pd.read_pickle(f)
    else:
        FB.RES = str(OUT); out = FB.run()
    import battery as BT
    new = {s: BT.stats(out[s].loc["1999-01-31":"2012-12-31"])["lo_t_alpha"] for s in FB.SIGS}
    old = {s: v["lo_t_alpha"] for s, v in json.load(open(RES0 / "fund_battery.json"))["stats"].items() if s in FB.SIGS}
    res = sign_test(old, new, 15); save("t3_fund", res); print("T3", res["kept"], "of", res["n"], "passed" if res["passed"] else "failed")


def step_fmb():
    import fmb as FM
    FM.START, FM.END = xs.START, xs.END
    I = xs.inputs(R); E = I["E"]
    for k in list(I["S"]):
        m = E.reindex(index=I["S"][k].index, columns=I["S"][k].columns).fillna(False).astype(bool); I["S"][k] = I["S"][k].where(m)
    G = FM.fm(I, list(FM.PRICE)); G.to_pickle(OUT / "fmb_US.pkl")
    sm = FM.summarise(G, list(FM.PRICE)); mom = sm["mom"]
    res = dict(multi=sm, mom_t=mom["t"], passed=bool(mom["t"] > 2 and mom["ann"] > 0), months=mom["months"])
    save("t4_fmb", res); print("T4 mom slope t %.2f" % mom["t"], "passed" if res["passed"] else "failed")


# ---------------- T5 FS18 overlay (US, $50m), T6 FS20 checklist (primary + 11 variants) ----------------
def step_fs18():
    import fs18 as F18
    I, nets, turn = F18.books(R)
    B = pd.DataFrame(nets[5e7]); ov, raw, scale, w = F18.overlay(B)
    ov = ov.loc["1999-01-31":"2012-12-31"]; ov.to_pickle(OUT / "fs18_overlay_US.pkl")
    t = perf.nw_t(ov)["t"]
    res = dict(start=str(ov.index[0].date()), months=len(ov), ann=float(ov.mean() * 12), sharpe=perf.sharpe(ov), t=t, passed=bool(t > 2),
               books={n: dict(ann=float(B[n].loc["1999":"2012"].mean() * 12), sharpe=perf.sharpe(B[n].loc["1999":"2012"].dropna())) for n in B})
    save("t5_fs18", res); print("T5 overlay t %.2f ann %.2f%%" % (t, res["ann"] * 100), "passed" if res["passed"] else "failed")


def step_fs20():
    import fs20 as F20
    F20.START_REVIEW = "1998-12-31"
    if SENS == "delist":          # fs20 reads prices itself, so the haircut is applied here as in data.load
        _p = F20.prices
        def prices():
            px, r = _p(); hit = 0
            for tk in json.load(open(os.environ["FS_DELIST_TICKERS"])):
                if tk in r.columns and r[tk].notna().any():
                    last = r[tk].last_valid_index(); i = r.index.get_loc(last)
                    if i + 1 < len(r.index) and last < r.index[-1] - pd.Timedelta(days=10):
                        r.iloc[i + 1, r.columns.get_loc(tk)] = -0.30; hit += 1
            print("fs20 delisting haircut on", hit, "names"); return px, r
        F20.prices = prices
    if SENS == "lag":
        _m = F20.membership
        F20.membership = lambda px: (lambda u, mc: (u.shift(1, fill_value=False), mc))(*_m(px))
    ctx = F20.context(); rf, mkt = ctx["rf"], ctx["mkt"]; out = {}
    for N, fq, rb in [(N, fq, rb) for rb in ("fcf", "ey") for fq in ("annual", "quarterly") for N in (12, 25, 50)]:
        P, to, nq, log = F20.run_variant(N, fq, rb, ctx)
        n = P.net.loc["1999-01-31":"2012-12-31"].dropna()
        a = F20.alpha(n, mkt.reindex(n.index), rf.reindex(n.index))
        a1 = F20.alpha(n[:"2005"], mkt.reindex(n[:"2005"].index), rf.reindex(n[:"2005"].index))
        a2 = F20.alpha(n["2006":], mkt.reindex(n["2006":].index), rf.reindex(n["2006":].index))
        out[f"N{N}_{fq}_{rb}"] = dict(capm=a, h1=a1, h2=a2, passed=bool(a["t"] > 2 and a1["alpha"] > 0 and a2["alpha"] > 0),
                                      qualifiers_mean=float(nq.mean()), cost=float(P.cost.loc["1999":"2012"].mean() * 12))
        print(f"N{N}_{fq}_{rb}", "alpha %+.2f%% t %.2f" % (a["alpha"] * 100, a["t"]), flush=True)
    prim = out["N12_annual_fcf"]; save("t6_fs20", dict(primary="N12_annual_fcf", passed=prim["passed"], variants=out))
    print("T6 primary", "passed" if prim["passed"] else "failed")


if __name__ == "__main__":
    {"xs": step_xs, "turtle": step_turtle, "lottery": step_lottery, "report": step_report, "battery": step_battery, "fund": step_fund, "fmb": step_fmb, "fs18": step_fs18, "fs20": step_fs20, "costs": step_costs}[sys.argv[1]]()
