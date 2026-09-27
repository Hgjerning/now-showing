#!/bin/sh
# full rebuild after the month-end eligibility fix
cd "$(dirname "$0")"
L=../results/logs; mkdir -p $L
for R in US EU UK SC WD; do python3 signals.py $R > $L/sig_$R.log 2>&1 & done; wait
for R in US EU UK DK SC WD; do python3 signals2.py $R > $L/sig2_$R.log 2>&1 & done; wait
for R in US EU UK DK SC WD; do python3 library.py $R > $L/lib_$R.log 2>&1 & done
for R in US EU UK DK SC WD; do python3 run_lottery.py $R > $L/rl_$R.log 2>&1 & done; wait
python3 lottery_fix.py > $L/lf.log 2>&1
python3 posthoc_lottery.py > $L/ph.log 2>&1
python3 analyse.py lottery > $L/an.log 2>&1
python3 fix_analysis.py > $L/fa.log 2>&1
python3 neighbourhood.py max > $L/nbmax.log 2>&1 &
python3 neighbourhood.py brk > $L/nbbrk.log 2>&1 &
python3 monkey.py > $L/monkey.log 2>&1 &
python3 analyse_xs.py FS03 FS04 FS06 > $L/ax1.log 2>&1 &
python3 analyse_xs.py FS07 FS08 FS09 > $L/ax2.log 2>&1 &
python3 analyse_xs.py FS10 FS11 FS12 > $L/ax3.log 2>&1 &
wait
python3 nbh_figs.py > $L/nbf.log 2>&1
python3 make_figures.py > $L/mf.log 2>&1
echo ALLDONE > $L/done.log
