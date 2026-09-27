#!/bin/sh
# full rebuild after borrow fees (all short legs) + World in USD (27 Sep 2026)
cd "$(dirname "$0")"
L=../results/logs2; mkdir -p $L
python3 signals.py WD > $L/sig_WD.log 2>&1; python3 signals2.py WD > $L/sig2_WD.log 2>&1
for R in US EU UK DK SC WD; do python3 library.py $R > $L/lib_$R.log 2>&1 & done
for R in US EU UK DK SC WD; do python3 run_lottery.py $R > $L/rl_$R.log 2>&1 & done
python3 run_turtle.py WD > $L/rt_WD.log 2>&1 &
wait
python3 turtle_fix.py WD > $L/tf_WD.log 2>&1 &
python3 lottery_fix.py > $L/lf.log 2>&1 &
wait
python3 posthoc_lottery.py > $L/ph.log 2>&1
python3 analyse.py turtle lottery > $L/an.log 2>&1
python3 fix_analysis.py > $L/fa.log 2>&1
python3 diag_turtle.py > $L/dt.log 2>&1 &
python3 cost_check.py > $L/cc.log 2>&1 &
python3 neighbourhood.py max > $L/nbmax.log 2>&1 &
python3 neighbourhood.py brk > $L/nbbrk.log 2>&1 &
python3 monkey.py > $L/monkey.log 2>&1 &
python3 analyse_xs.py FS03 FS04 FS06 > $L/ax1.log 2>&1 &
python3 analyse_xs.py FS07 FS08 FS09 > $L/ax2.log 2>&1 &
python3 analyse_xs.py FS10 FS11 FS12 > $L/ax3.log 2>&1 &
python3 battery.py > $L/bat.log 2>&1 &
wait
python3 financing.py > $L/fin.log 2>&1
python3 common_ground.py > $L/cg.log 2>&1
python3 nbh_figs.py > $L/nbf.log 2>&1
python3 make_figures.py > $L/mf.log 2>&1
echo ALLDONE > $L/done.log
