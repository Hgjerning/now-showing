# -*- coding: utf-8 -*-
"""Turtle Trading rules (Faith 2003/2007) applied stock by stock to an equity universe.

Close-only, event-driven simulator. Signals are computed on the close of day t and filled on the
close of day t+1 (one-day lag, no look-ahead). Everything in local currency.

Rules kept from the original (Faith 2003, "The Original Turtle Trading Rules"):
  N        = 20-day Wilder average of the true range (close-to-close proxy |dP|, no H/L in Sharadar)
  Unit     = RISK x equity / N shares (a 1-N move costs RISK of equity)
  System 1 = 20-day breakout entry, 10-day opposite breakout exit, skip a signal if the previous
             System 1 breakout in that stock would have been a winner; 55-day failsafe breakout
  System 2 = 55-day breakout entry, 20-day opposite breakout exit, no filter
  Stop     = 2N from the most recent unit; pyramid 1 unit every 1/2 N, max 4 units per stock
  Limit    = max 12 units per direction (original "single direction" limit) -> replaced by a
             gross cap because a 500-stock universe produces dozens of breakouts a day (see factsheet)
Equity adaptation (documented in the factsheet):
  RISK = 0.1% (original 1%), gross cap 100% long and 100% short of equity per book,
  oversubscribed days filled in order of breakout strength (distance past the channel in N).
Costs: 10 bp per side on traded notional, 50 bp a year borrow on short notional, no interest on cash.
"""
import numpy as np
import pandas as pd

COST, BORROW = 0.0010, 0.0050


def run(ret, elig, system=2, risk=0.001, gross_cap=1.0, allow_short=True, start="2013-01-01",
        use_stop=True, stop_mult=2.0, regime=None, confirm=0):
    """regime: daily bool Series (True = market up-trend): longs only when True, shorts only when False.
    confirm: enter only if the price is still beyond the breakout level `confirm` days after the breakout."""
    P = (1 + ret.fillna(0)).cumprod().where(ret.notna().cumsum() > 0)   # TR index
    alive = ret.notna()
    Pf = P.ffill()
    L, X = (20, 10) if system == 1 else (55, 20)
    hiL = Pf.shift(1).rolling(L, min_periods=L).max().to_numpy()
    loL = Pf.shift(1).rolling(L, min_periods=L).min().to_numpy()
    hiX = Pf.shift(1).rolling(X, min_periods=X).max().to_numpy()
    loX = Pf.shift(1).rolling(X, min_periods=X).min().to_numpy()
    hi55 = Pf.shift(1).rolling(55, min_periods=55).max().to_numpy()
    lo55 = Pf.shift(1).rolling(55, min_periods=55).min().to_numpy()
    tr = Pf.diff().abs()
    N = tr.ewm(alpha=1 / 20, adjust=False, min_periods=20).mean().to_numpy()
    days, tick = P.index, P.columns
    BL = (Pf.to_numpy() > hiL); BS = (Pf.to_numpy() < loL)
    up = regime.reindex(days).ffill().fillna(False).to_numpy() if regime is not None else None
    p = Pf.to_numpy(); al = alive.to_numpy(); el = elig.reindex(index=days, columns=tick).fillna(False).to_numpy()
    last_seen = np.full(len(tick), -1)
    T, K = p.shape
    i0 = days.searchsorted(pd.Timestamp(start))

    E = 1.0
    sh = np.zeros(K); units = np.zeros(K, int); stop = np.full(K, np.nan); last_add = np.full(K, np.nan)
    N_ent = np.full(K, np.nan); ent_i = np.full(K, -1); cost_basis = np.zeros(K); pnl_acc = np.zeros(K)
    risk0 = np.zeros(K); maxu = np.zeros(K, int); E_ent = np.ones(K)
    # System 1 hypothetical-trade tracker for the skip filter
    h_dir = np.zeros(K, int); h_ent = np.full(K, np.nan); h_stop = np.full(K, np.nan); last_win = np.zeros(K, bool)
    pend_exit = np.zeros(K, bool); pend_add = np.zeros(K, bool); pend_ent = np.zeros(K, int); pend_sz = np.zeros(K); pend_prio = np.zeros(K)

    out_ret, out_long, out_short, out_npos = [], [], [], []
    trades = []

    def close_trade(k, i, px, reason):
        nonlocal E
        notional = abs(sh[k]) * px
        c = COST * notional
        E -= c; pnl_acc[k] -= c
        trades.append(dict(ticker=tick[k], dir="long" if sh[k] > 0 else "short", entry=days[ent_i[k]], exit=days[i],
                           days=int(i - ent_i[k]), units=int(maxu[k]), entry_px=cost_basis[k] / abs(sh[k]) if sh[k] else np.nan,
                           exit_px=px, pnl_pct=pnl_acc[k] / E_ent[k], R=pnl_acc[k] / risk0[k] if risk0[k] > 0 else np.nan, reason=reason))
        sh[k] = 0; units[k] = 0; stop[k] = np.nan; last_add[k] = np.nan; N_ent[k] = np.nan; ent_i[k] = -1
        cost_basis[k] = 0; pnl_acc[k] = 0; risk0[k] = 0; maxu[k] = 0

    nN = N[0]; pend_stop = np.zeros(K, bool)
    for i in range(1, T):
        pi = p[i]; pp = p[i - 1]
        last_seen = np.where(al[i], i, last_seen)
        # 1. mark to market
        dp = np.nan_to_num(pi - pp)
        pnl = sh * dp
        shortnot = np.sum(np.where(sh < 0, -sh * np.nan_to_num(pi), 0))
        borrow = BORROW / 252 * shortnot
        pnl_tot = pnl.sum() - borrow
        E_prev = E
        E += pnl_tot; pnl_acc += pnl
        if shortnot > 0:
            pnl_acc -= np.where(sh < 0, -sh * np.nan_to_num(pi), 0) / shortnot * borrow
        # 2. execute orders from yesterday's close at today's close
        dead = (sh != 0) & (i - last_seen > 5)            # delisted / stale: exit at last price
        for k in np.where(dead)[0]:
            close_trade(k, i, p[last_seen[k], k], "delisted/stale")
        for k in np.where(pend_exit & (sh != 0) & al[i])[0]:
            close_trade(k, i, pi[k], "2N stop" if pend_stop[k] else "channel exit")
        pend_exit[:] = False
        longnot = np.sum(np.where(sh > 0, sh * np.nan_to_num(pi), 0))
        shortnot = np.sum(np.where(sh < 0, -sh * np.nan_to_num(pi), 0))
        cand = np.where((pend_add | (pend_ent != 0)) & al[i])[0]
        cand = cand[np.argsort(-pend_prio[cand])]
        for k in cand:
            d = int(np.sign(sh[k])) if pend_add[k] else pend_ent[k]
            q = pend_sz[k]; notional = q * pi[k]
            if d > 0 and longnot + notional > gross_cap * E:
                continue
            if d < 0 and shortnot + notional > gross_cap * E:
                continue
            c = COST * notional; E -= c
            if sh[k] == 0:
                ent_i[k] = i; E_ent[k] = E
                risk0[k] = q * 2 * nN[k] if not np.isnan(nN[k]) else 0
            sh[k] += d * q; units[k] += 1; maxu[k] = max(maxu[k], units[k])
            cost_basis[k] += notional; pnl_acc[k] -= c
            last_add[k] = pi[k]; N_ent[k] = nN[k]
            stop[k] = pi[k] - d * stop_mult * nN[k] if use_stop else np.nan                # all units' stops move to 2N from the newest unit
            if d > 0: longnot += notional
            else: shortnot += notional
        pend_add[:] = False; pend_ent[:] = 0; pend_prio[:] = 0
        out_ret.append((days[i], (E - E_prev) / E_prev if i >= i0 else 0.0))
        out_long.append(np.sum(np.where(sh > 0, sh * np.nan_to_num(pi), 0)) / E)
        out_short.append(np.sum(np.where(sh < 0, -sh * np.nan_to_num(pi), 0)) / E)
        out_npos.append(int((sh != 0).sum()))
        # 3. signals on today's close for tomorrow
        nN = N[i]
        ok = al[i] & ~np.isnan(nN) & (nN > 0)
        lg = sh > 0; st = sh < 0
        ex_l = lg & ok & ((pi < loX[i]) | (pi <= stop))
        ex_s = st & ok & ((pi > hiX[i]) | (pi >= stop))
        pend_exit = ex_l | ex_s
        pend_stop = (lg & ok & (pi <= stop)) | (st & ok & (pi >= stop))
        add_l = lg & ~pend_exit & ok & (units < 4) & (pi >= last_add + 0.5 * N_ent)
        add_s = st & ~pend_exit & ok & (units < 4) & (pi <= last_add - 0.5 * N_ent)
        pend_add = add_l | add_s
        brk_l = ok & (pi > hiL[i]); brk_s = ok & (pi < loL[i])
        if system == 1:
            # hypothetical S1 trades (taken or not) decide the skip filter
            hx = (h_dir > 0) & ok & ((pi < loX[i]) | (pi <= h_stop))
            hx |= (h_dir < 0) & ok & ((pi > hiX[i]) | (pi >= h_stop))
            last_win = np.where(hx, (pi - h_ent) * h_dir > 0, last_win)
            h_dir = np.where(hx, 0, h_dir)
            newh = (h_dir == 0) & (brk_l | brk_s)
            h_dir = np.where(newh, np.where(brk_l, 1, -1), h_dir)
            h_ent = np.where(newh, pi, h_ent); h_stop = np.where(newh, pi - h_dir * 2 * nN, h_stop)
            take_l = brk_l & (~last_win | (pi > hi55[i])); take_s = brk_s & (~last_win | (pi < lo55[i]))
        else:
            take_l, take_s = brk_l, brk_s
        if confirm > 0 and i - confirm >= 0:
            j = i - confirm
            take_l = BL[j] & ok & (pi > hiL[j]); take_s = BS[j] & ok & (pi < loL[j])
        if up is not None:
            take_l = take_l & up[i]; take_s = take_s & (~up[i])
        flat = (sh == 0) & el[i] & ok
        pend_ent = np.where(flat & take_l, 1, np.where(flat & take_s & allow_short, -1, 0))
        pend_sz = np.where(ok, risk * E / np.where(ok, nN, 1.0), 0.0)
        prio_l = (pi - hiL[i]) / nN; prio_s = (loL[i] - pi) / nN
        pend_prio = np.where(pend_ent > 0, prio_l, np.where(pend_ent < 0, prio_s, np.where(pend_add, 99.0, 0.0)))
        pend_prio = np.nan_to_num(pend_prio)

    r = pd.Series(dict(out_ret)).loc[start:]
    expo = pd.DataFrame({"long": out_long, "short": out_short, "npos": out_npos}, index=days[1:]).loc[start:]
    tl = pd.DataFrame(trades)
    tl = tl[tl.exit >= pd.Timestamp(start)] if len(tl) else tl
    openpos = pd.DataFrame(dict(ticker=tick[sh != 0], dir=np.where(sh[sh != 0] > 0, "long", "short"), units=units[sh != 0],
                                entry=[days[j] for j in ent_i[sh != 0]], weight=(sh * np.nan_to_num(p[-1]) / E)[sh != 0],
                                open_pnl_pct=(pnl_acc / E_ent)[sh != 0]))
    return dict(ret=r, expo=expo, trades=tl, open=openpos.sort_values("weight", key=abs, ascending=False))


def fully_invested(res, cost=COST):
    """Long-only book scaled to 100% invested (Henrik, 2026-10-01: "scale to 1").

    The rules above size each position by risk (RISK x equity / N) and leave the rest in cash at 0%, so a long-only book
    is often well below 100% invested. Here every position is scaled by the same factor so that the long book is 100% of
    equity at every close: scale = 1 / (long notional / equity). Positions keep their relative sizes; only the total
    changes. Re-scaling each day is charged at `cost` on the notional it moves, |1 - exposure before / 100%|, where the
    exposure before is yesterday's 100% book after one day of price drift and today's entries, add-ons and exits.
    Days with no position at all stay in cash (0%): there is nothing to scale. Returns dict(ret, scale, cash_days).
    """
    r, e = res["ret"], res["expo"].reindex(res["ret"].index)
    L = e["long"].fillna(0).to_numpy(); npos = e["npos"].fillna(0).to_numpy()
    out = np.zeros(len(r)); scale = np.zeros(len(r))
    k = 0.0          # factor applied to today's return = 1 / exposure at yesterday's close
    for i in range(len(r)):
        out[i] = r.iloc[i] * k
        scale[i] = k
        new_k = 1.0 / L[i] if L[i] > 1e-9 else 0.0
        if k > 0 and new_k > 0:
            out[i] -= cost * abs(1 - L[i] * k)   # re-size the whole book back to 100%
        k = new_k
    return dict(ret=pd.Series(out, index=r.index), scale=pd.Series(scale, index=r.index), cash_days=float((npos == 0).mean()))
