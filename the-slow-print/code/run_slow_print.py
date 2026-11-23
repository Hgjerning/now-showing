# -*- coding: utf-8 -*-
"""A31-S "Slow Print": can the US small-cap machine signal be traded slowly enough?
Pre-registration: ../PREREGISTRATION_A31S_Slow_Print_2026-11-06.md (signed 6 Nov 2026 18:53, hash in
PREREGISTRATION_A31S_SIGNED_HASH.txt). Written 7 Nov 2026, before any slow variant was computed.

Order (each stage stops the run if its check fails; nothing after a failed check is computed):
  1. A31's walk-forward re-run with A31's own code (run_a31.walk_forward, MODELS, FEATS) on the panel A31 ran on
     (the core columns of the a31_panels chunks, built 6-7 Oct 2026 from the pre-2026-10-08 panels). Checkpointed per
     year: rerun the same command to resume.
  2. INTEGRITY: the base book rebuilt with A31's own book() must reproduce A31's saved monthly gross, net and turnover
     (results/U1/*.csv). Those files hold single-precision values (8-9 significant digits), so the test is
     "identical at the saved precision" (float32 equality), the strictest test the files allow (the pre-registration's
     1e-10 is below their resolution). Fail -> STOP, report, no slow variant computed.
  3. ENGINE CHECK: this file's own book engine, in base mode, must equal A31's book() to 1e-7 in gross and turnover
     (A31 works on single-precision returns, this engine in double precision; the gap is rounding, a few 1e-9).
  4. COST INPUTS: 63-day average traded value in USD and the pooled illiquidity rank (US + EU + UK); traded
     stock-months with a traded value must be at least 80%, else STOP.
  5. Trials S-1, S-2, S-3 (ART live-fill costs, DKK 10m), Holm at 5% one-sided; then everything in section 4.

Run on the PC (the cloud has 2 cores): runners\\run_slow_print.ps1. Prints clock time, progress and ETA.
    python run_slow_print.py <a31_panels dir> <A31 results/U1 dir> <pit dir> <fx_daily.pkl> <out dir>
"""
import json, os, sys, time, warnings
import numpy as np, pandas as pd
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from run_a31 import FEATS, MODELS, SPEC, book, walk_forward  # noqa: E402  A31's own code, unchanged
from stats import nw_t, sharpe  # noqa: E402
warnings.filterwarnings("ignore")

T0 = time.time()


class _Stamp:
    """Prefix every printed line with the clock time; walk-forward year lines also get progress and an ETA.
    Lines are buffered until their newline (print() writes its arguments in separate pieces)."""
    def __init__(self, w): self.w, self.buf = w, ""
    def write(self, s):
        import re
        self.buf += s
        while "\n" in self.buf:
            line, self.buf = self.buf.split("\n", 1); now = pd.Timestamp.now()
            m = re.match(r"^(\d{4}) trained on", line)
            if m:
                done = int(m.group(1)) - 2003; tot = 2026 - 2003; left = (time.time() - T0) / done * (tot - done)
                line += f"   [year {done}/{tot}, ETA {(now + pd.Timedelta(seconds=left)):%H:%M}]"
            if line.strip() and not re.match(r"^\d\d:\d\d:\d\d  ", line):
                line = f"{now:%H:%M:%S}  " + line
            self.w.write(line + "\n")
        self.w.flush()
    def flush(self): self.w.flush()


sys.stdout = _Stamp(sys.stdout)
ART = dict(a=6.2, b=8.9, c=36.5, cap=50.0, fee=1.5)     # bp one-way (FS32 Amendment 1; fs32_core.ART)
BOOK_DKK = 10e6
GATED = {"S-1": ("S1", dict(a=0.5)), "S-2": ("S2", dict(exit=0.30)), "S-3": ("S3", dict(n=3))}
CUT = pd.Timestamp("2011-06-01")                          # USS98 -> USS splice date, as build_u1.py


def say(msg, done=None, total=None):
    now = pd.Timestamp.now(); eta = ""
    if done and total:
        left = (time.time() - T0) / done * (total - done)
        eta = f"  [{done}/{total}, ETA {(now + pd.Timedelta(seconds=left)):%H:%M}]"
    print(f"{now:%H:%M:%S}  {msg}{eta}", flush=True)


# ------------------------------------------------------------------ 1. panel and walk-forward
def load_core(d):
    import glob
    cols = ["month", "ticker"] + FEATS + ["y", "fwd", "raw_mom"]
    fs = sorted(glob.glob(os.path.join(d, "U1_wide_*.parquet")))
    if not fs:
        sys.exit(f"STOP: no U1_wide_*.parquet chunks in {d}")
    L = pd.concat([pd.read_parquet(f, columns=cols) for f in fs]).set_index(["month", "ticker"]).sort_index()
    say(f"panel: {len(L):,} stock-months, {L.index.get_level_values(0).min():%Y-%m} to {L.index.get_level_values(0).max():%Y-%m}")
    return L


# ------------------------------------------------------------------ 3. book engine (all variants)
def engine(L, score, mode="base", a=1.0, exit=None, n=1, q=0.1):
    """Monthly long-short. Returns DataFrame(gross, turnover, ic) and dict month -> Series |traded weight| by ticker.
    base : top/bottom decile, equal weight (A31's book).
    S1   : each leg = normalise((1-a) * drifted leg + a * decile target); a=1 is the base.
    S2   : enter top (bottom) q, stay while inside top (bottom) `exit`; equal weight; missing names leave.
    S3   : score = mean of the within-month percentile rank over this month and the n-1 before (fewer if fewer exist),
           then the base decile book.
    Legs are kept separately (long sums to +1, short to -1); net weight = long - short. Leg return = weighted mean
    over names with a next-month return (A31: plain mean = equal weights). Drift as A31: missing return -> 0, then
    each leg renormalised."""
    df = pd.DataFrame({"s": score, "r": L.loc[score.index, "fwd"]})
    if mode == "S3":
        rk = df.s.groupby(level=0).rank(pct=True).unstack()
        sm = rk.rolling(n, min_periods=1).mean()          # calendar months in the index; NaN months skipped
        df["s"] = sm.stack().reindex(df.index)
    prevL = prevS = None; prev_w = None
    rows, traded = [], {}
    for m, g in df.groupby(level=0):
        g = g.droplevel(0); k = g.s.rank(pct=True); present = g.index
        tL = pd.Series(1.0, index=present[k > 1 - q]); tL /= tL.sum()
        tS = pd.Series(1.0, index=present[k <= q]); tS /= tS.sum()
        if mode == "S1" and prevL is not None and a < 1:
            pL = prevL[prevL.index.isin(present)]; pS = prevS[prevS.index.isin(present)]
            Lw = (pL * (1 - a)).add(tL * a, fill_value=0); Sw = (pS * (1 - a)).add(tS * a, fill_value=0)
            Lw, Sw = Lw[Lw > 0] / Lw.sum(), Sw[Sw > 0] / Sw.sum()
        elif mode == "S2" and prevL is not None:
            keepL = prevL.index[prevL.index.isin(present)]; keepL = keepL[k.reindex(keepL) > 1 - exit]
            keepS = prevS.index[prevS.index.isin(present)]; keepS = keepS[k.reindex(keepS) <= exit]
            nl = tL.index.union(keepL); ns = tS.index.union(keepS)
            Lw = pd.Series(1.0 / len(nl), index=nl); Sw = pd.Series(1.0 / len(ns), index=ns)
        else:
            Lw, Sw = tL, tS
        w = Lw.sub(Sw, fill_value=0.0)
        tr = (w.sub(prev_w, fill_value=0).abs() if prev_w is not None else w.abs())
        tr = tr[tr > 0]; traded[m] = tr
        r = g.r.astype("float64")
        def leg(B):
            rr = r.reindex(B.index); ok = rr.notna()
            return float((B[ok] * rr[ok]).sum() / B[ok].sum()) if ok.any() else np.nan
        gross = leg(Lw) - leg(Sw)
        rr0 = r.fillna(0.0)
        dL = Lw * (1 + rr0.reindex(Lw.index).fillna(0.0)); dS = Sw * (1 + rr0.reindex(Sw.index).fillna(0.0))
        if len(dL) and len(dS):
            prevL, prevS = dL / dL.sum(), dS / dS.sum(); prev_w = prevL.sub(prevS, fill_value=0.0)
        else:
            prevL = prevS = prev_w = None
        ic = st.spearmanr(g.s, g.r, nan_policy="omit")[0]
        rows.append(dict(month=m, gross=gross, turnover=float(tr.sum()), ic=ic, n_long=len(Lw), n_short=len(Sw)))
    return pd.DataFrame(rows).set_index("month"), traded


# ------------------------------------------------------------------ 4. cost inputs
def monthly_adv(pit, fx):
    """63-day average traded value in USD, last value in each calendar month. Returns (adv_small, pool)."""
    def rd(f):
        x = pd.read_parquet(os.path.join(pit, f)).sort_index(); x.index = pd.to_datetime(x.index); return x.where(x > 0)
    a, b = rd("USS98_pit_tradedvalue_pre20261008.parquet"), rd("USS_pit_tradedvalue_pre20261008.parquet")
    cols = sorted(set(a.columns) | set(b.columns))
    tv = pd.concat([a.reindex(columns=cols).loc[a.index < CUT], b.reindex(columns=cols).loc[b.index >= CUT]]).sort_index()
    tv = tv[~tv.index.duplicated()]
    big = rd("USS1500_pit_tradedvalue_pre20261008.parquet")
    me = lambda x: x.rolling(63, min_periods=40).mean().resample("ME").last()
    adv_small = me(tv); say(f"ADV US small caps: {adv_small.shape[1]} stocks, {adv_small.index.min():%Y-%m} to {adv_small.index.max():%Y-%m}")
    pool = [adv_small, me(big).drop(columns=[c for c in big.columns if c in adv_small.columns], errors="ignore")]
    fxm = fx.resample("ME").last()
    sys.path.insert(0, os.path.join(pit, "..", "..", "code"))
    try:
        import eu_value_prof as EVP
        ccy_of = EVP.price_ccy
    except Exception as e:
        sys.exit(f"STOP: cannot load the EU/UK currency map (eu_value_prof.price_ccy): {e}")
    for R in ("EU", "UK"):
        x = rd(f"{R}_pit_tradedvalue.parquet")
        if R == "UK":
            x.loc[:, [c for c in x.columns if str(c).endswith(".L")]] /= 100.0      # pence
        m = me(x); F = fxm.reindex(m.index).ffill()
        m = pd.DataFrame({c: m[c] / (F[ccy_of(c)] if ccy_of(c) in F else 1.0) for c in m.columns})
        pool.append(m); say(f"ADV {R}: {m.shape[1]} stocks from {m.dropna(how='all').index.min():%Y-%m}")
    P = pd.concat(pool, axis=1); P = P.loc[:, ~P.columns.duplicated()]
    illiq = 1 - P.rank(axis=1, pct=True)                  # (100 - rank)/100, pooled US + EU + UK each month
    return adv_small, illiq


def cost_month(tr, adv, il, book_usd, kind, scale=1.0):
    """Sum over stocks of |traded weight| x one-way cost (fraction)."""
    if kind.startswith("flat"):
        return float(tr.sum() * float(kind[4:]))
    a = adv.reindex(tr.index).to_numpy(); i = il.reindex(tr.index).fillna(0.5).to_numpy()
    part = np.minimum(ART["cap"], 100 * tr.to_numpy() * book_usd / np.where(a > 0, a, np.nan))
    part = np.where(np.isfinite(part), part, ART["cap"])
    bp = scale * (ART["a"] + ART["c"] * i + ART["b"] * np.sqrt(part) + ART["fee"])
    return float((tr.to_numpy() * bp / 1e4).sum())


def net_series(res, traded, ADV, IL, BUSD, kind="art", scale=1.0, book_dkk=BOOK_DKK):
    c = {}
    for m, tr in traded.items():
        if kind == "art":
            adv = ADV.loc[m] if m in ADV.index else pd.Series(dtype=float); il = IL.loc[m] if m in IL.index else pd.Series(dtype=float)
            c[m] = cost_month(tr, adv, il, BUSD.get(m, np.nan) * book_dkk / BOOK_DKK, "art", scale)
        else:
            c[m] = cost_month(tr, None, None, None, kind)
    cost = pd.Series(c).reindex(res.index)
    return res.gross - cost, cost


def stats_row(gross, net, to, base_gross=None, base_to=None):
    x, g = net.dropna(), gross.dropna(); h = len(x) // 2; t = nw_t(x, 3)
    sub = x[x.index >= "2017-01-01"]; to_m = to.iloc[1:].mean()
    out = dict(net_ann=x.mean() * 12, net_t=t["t"], p_one_sided=t["p_gt"], net_sharpe=sharpe(x), gross_ann=g.mean() * 12,
               gross_t=nw_t(g, 3)["t"], gross_sharpe=sharpe(g), turnover_m=to_m, breakeven_cost=g.mean() / to_m,
               net_ann_h1=x.iloc[:h].mean() * 12, net_ann_h2=x.iloc[h:].mean() * 12,
               net_ann_2017=sub.mean() * 12, net_t_2017=nw_t(sub, 3)["t"], months=len(x))
    if base_gross is not None:
        out.update(alpha_kept=g.mean() / base_gross.dropna().mean(), turnover_kept=to_m / base_to.iloc[1:].mean())
    return out


def holm(ps, alpha=0.05):
    items = sorted(ps.items(), key=lambda kv: kv[1]); m = len(items); out = {}; stop = False
    for i, (k, p) in enumerate(items):
        bar = alpha / (m - i); ok = (not stop) and p < bar; stop = stop or not ok
        out[k] = dict(p=p, bar=bar, passes=bool(ok))
    return out


def decay(L, score, H=6):
    """Mean monthly rank IC of month-t scores against the return of month t+h (h=1..H)."""
    fwd = L["fwd"].unstack(); S = score.unstack(); out = {}
    for h in range(1, H + 1):
        F = fwd.shift(-(h - 1)); ics = []
        for m in S.index:
            if m not in F.index:
                continue
            a, b = S.loc[m], F.loc[m].reindex(S.columns); ok = a.notna() & b.notna()
            if ok.sum() > 50:
                ics.append(st.spearmanr(a[ok], b[ok])[0])
        out[h] = float(np.mean(ics))
    return out


# ------------------------------------------------------------------ main
def main():
    panels, a31dir, pit, fxf, OUT = sys.argv[1:6]; os.makedirs(OUT, exist_ok=True); sp = SPEC["U1"]
    say("A31-S Slow Print, stage 1: walk-forward (A31's code; checkpointed per year)")
    L = load_core(panels)
    Lw, P = walk_forward(L, list(MODELS), sp["start"], sp["first_oos"], ckpt=os.path.join(OUT, "_ckpt_core.pkl"))
    P.to_pickle(os.path.join(OUT, "oos_predictions_core_this_machine.pkl"))
    ov = os.environ.get("A31S_PRED_OVERRIDE")
    if ov:
        # NOTE_A31S_IMPLEMENTATION (addendum 7 Nov 2026): models whose fitted predictions depend on the platform (kNN
        # tie-breaking; checked model by model) are taken from a re-run of the same code on Linux, where A31 ran.
        Q = pd.read_pickle(ov)
        for c in Q.columns:
            if c not in P.columns:
                sys.exit(f"STOP: override column {c} is not a model")
            q = Q[c].reindex(P.index)
            if q.isna().any():
                sys.exit(f"STOP: override for {c} misses {int(q.isna().sum())} predictions")
            P[c] = q
        say(f"predictions for {', '.join(Q.columns)} taken from {ov} (same code, run on Linux)")
    # The Ensemble is built from a table laid out exactly as in A31's run_a31.py (DataFrame from a dict of the model
    # Series, then dropna). The row mean of the eight ranks rounds in the last digit according to the table's memory
    # layout, and exact ties at the decile cut are common, so a frame with a replaced column flips names in 15 of 271
    # months (NOTE_A31S_IMPLEMENTATION, addendum 8 Nov 2026).
    M = pd.DataFrame({n: P[n] for n in MODELS}).dropna()
    P["Ensemble"] = M.groupby(level=0).rank(pct=True).mean(axis=1).reindex(P.index); P["Momentum"] = Lw.loc[P.index, "raw_mom"]
    P.to_pickle(os.path.join(OUT, "oos_predictions_core.pkl")); say(f"walk-forward done: {len(P):,} predictions")

    # ---- 2. integrity
    say("stage 2: integrity check against A31's saved series")
    rep = {"integrity": {}}
    B = {n: book(Lw, P[n].dropna(), sp["cost"]) for n in P.columns}
    saved = {k: pd.read_csv(os.path.join(a31dir, f"{k}_monthly.csv"), index_col=0, parse_dates=True) for k in ("gross", "net", "turnover")}
    ok_all = True
    for n in P.columns:
        for k in ("gross", "net", "turnover"):
            new = B[n][k]; old = saved[k][n].reindex(new.index)
            same = bool((new.astype("float32").values == old.astype("float32").values).all() and len(new) == saved[k][n].dropna().shape[0])
            d = float((new - old).abs().max())
            rep["integrity"][f"{n}.{k}"] = dict(identical_at_saved_precision=same, max_abs_diff=d)
            if n == "Ensemble" and not same:
                ok_all = False
    json.dump(rep, open(os.path.join(OUT, "integrity.json"), "w"), indent=1)
    for n in P.columns:
        r = rep["integrity"]
        say(f"  {n:12s} gross {'OK' if r[n + '.gross']['identical_at_saved_precision'] else 'DIFF'} "
            f"(max {r[n + '.gross']['max_abs_diff']:.2e})  net {'OK' if r[n + '.net']['identical_at_saved_precision'] else 'DIFF'}  "
            f"turnover {'OK' if r[n + '.turnover']['identical_at_saved_precision'] else 'DIFF'}")
    if not ok_all:
        say("STOP: the Ensemble does not reproduce A31's saved series. No slow variant was computed (pre-registration "
            "section 1). Per-model differences are in integrity.json.")
        sys.exit(2)
    say("integrity check PASSED: the Ensemble reproduces A31's saved gross, net and turnover")

    # ---- 3. engine check
    E0, tr0 = engine(Lw, P["Ensemble"].dropna(), "base")
    b = B["Ensemble"]; dg = float((E0.gross - b.gross).abs().max()); dt = float((E0.turnover - b.turnover).abs().max())
    say(f"stage 3: engine check vs A31 book(): max |gross diff| {dg:.1e}, max |turnover diff| {dt:.1e}")
    # A31 works on single-precision returns (gross means and drift), this engine in double precision: differences of
    # a few 1e-9 are rounding (synthetic test 7 Nov 2026: 7e-9 gross, 4e-9 turnover). Bar: 1e-7 for both.
    if dg > 1e-7 or dt > 1e-7:
        say("STOP: the variant engine does not reproduce A31's base book; no slow variant computed."); sys.exit(3)

    # ---- 4. cost inputs
    say("stage 4: cost inputs (traded value, FX, pooled illiquidity)")
    fx = pd.read_pickle(fxf); fx.index = pd.to_datetime(fx.index)
    if fx["DKK"].first_valid_index() > pd.Timestamp("2003-12-31"):
        sys.exit("STOP: DKK FX does not cover 2004 onwards")
    ADV, IL = monthly_adv(pit, fx)
    BUSD = (BOOK_DKK / fx["DKK"].resample("ME").last().ffill()).to_dict()
    hit = tot = 0
    for m, tr in tr0.items():
        if m in ADV.index:
            hit += int(ADV.loc[m].reindex(tr.index).notna().sum())
        tot += len(tr)
    cov = hit / tot; rep["cost_inputs"] = dict(traded_stock_months_with_adv=cov)
    say(f"  traded stock-months with a traded value: {cov:.1%}")
    if cov < 0.8:
        json.dump(rep, open(os.path.join(OUT, "integrity.json"), "w"), indent=1)
        say("STOP: traded value covers under 80% of traded stock-months; the ART cost model would be wrong."); sys.exit(4)

    # ---- 5. trials
    base_net, base_cost = net_series(E0, tr0, ADV, IL, BUSD)
    R = {"base_ART": stats_row(E0.gross, base_net, E0.turnover), "trials": {}, "reported": {}}
    runs = {}
    for i, (tid, (mode, kw)) in enumerate(GATED.items(), 1):
        say(f"stage 5: trial {tid} ({mode} {kw})", i, len(GATED))
        res, tr = engine(Lw, P["Ensemble"].dropna(), mode, **kw); net, _ = net_series(res, tr, ADV, IL, BUSD)
        runs[tid] = (res, tr, net)
        R["trials"][tid] = stats_row(res.gross, net, res.turnover, E0.gross, E0.turnover)
        d = (net - base_net).dropna(); R["trials"][tid]["minus_base_net_ann"] = d.mean() * 12; R["trials"][tid]["minus_base_t"] = nw_t(d, 3)["t"]
        pd.DataFrame({"gross": res.gross, "net_art": net, "turnover": res.turnover, "ic": res.ic}).to_csv(os.path.join(OUT, f"monthly_{tid}.csv"))
    H = holm({k: v["p_one_sided"] for k, v in R["trials"].items()})
    for k in R["trials"]:
        R["trials"][k]["holm"] = H[k]
    json.dump(R, open(os.path.join(OUT, "slow_print_results.json"), "w"), indent=1, default=float)
    say("TRIALS: " + "  ".join(f"{k} net {v['net_ann']:+.1%} t {v['net_t']:.2f} {'PASS' if v['holm']['passes'] else 'fail'}"
                               for k, v in R["trials"].items()))

    # ---- reported, not gated
    say("reported: cost sensitivity, grids, decay, momentum")
    sens = {}
    for tid, (res, tr, _) in list(runs.items()) + [("base", (E0, tr0, None))]:
        s = {}
        for lab, kind, sc, bk in (("flat0.50", "flat0.005", 1, BOOK_DKK), ("flat0.40", "flat0.004", 1, BOOK_DKK),
                                  ("ART_x0.5", "art", 0.5, BOOK_DKK), ("ART_x2", "art", 2.0, BOOK_DKK),
                                  ("ART_DKK1m", "art", 1, 1e6), ("ART_DKK100m", "art", 1, 1e8)):
            n_, _ = net_series(res, tr, ADV, IL, BUSD, kind, sc, bk); x = n_.dropna()
            s[lab] = dict(net_ann=x.mean() * 12, net_t=nw_t(x, 3)["t"])
        sens[tid] = s
    R["reported"]["cost_sensitivity"] = sens
    grid = {}
    for lab, mode, kw in (("S1_a0.25", "S1", dict(a=0.25)), ("S1_a0.75", "S1", dict(a=0.75)), ("S2_exit0.20", "S2", dict(exit=0.20)),
                          ("S2_exit0.40", "S2", dict(exit=0.40)), ("S3_n2", "S3", dict(n=2)), ("S3_n6", "S3", dict(n=6))):
        res, tr = engine(Lw, P["Ensemble"].dropna(), mode, **kw); net, _ = net_series(res, tr, ADV, IL, BUSD)
        grid[lab] = stats_row(res.gross, net, res.turnover, E0.gross, E0.turnover); say(f"  grid {lab}: net {grid[lab]['net_ann']:+.1%}")
    R["reported"]["grids"] = grid
    R["reported"]["alpha_decay_ic"] = decay(Lw, P["Ensemble"].dropna())
    mom = {}
    M0, mtr0 = engine(Lw, P["Momentum"].dropna(), "base"); mnet0, _ = net_series(M0, mtr0, ADV, IL, BUSD)
    mom["base"] = stats_row(M0.gross, mnet0, M0.turnover)
    for tid, (mode, kw) in GATED.items():
        res, tr = engine(Lw, P["Momentum"].dropna(), mode, **kw); net, _ = net_series(res, tr, ADV, IL, BUSD)
        mom[tid] = stats_row(res.gross, net, res.turnover, M0.gross, M0.turnover)
    R["reported"]["momentum"] = mom
    R["minutes"] = round((time.time() - T0) / 60, 1)
    json.dump(R, open(os.path.join(OUT, "slow_print_results.json"), "w"), indent=1, default=float)
    say(f"DONE in {R['minutes']} min -> {os.path.join(OUT, 'slow_print_results.json')}")


if __name__ == "__main__":
    main()
