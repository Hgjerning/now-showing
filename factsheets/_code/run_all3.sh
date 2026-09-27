#!/bin/sh
cd "$(dirname "$0")"
L=../results/logs2
rm -f ../results/battery_price.pkl ../results/battery_price_??.pkl
python3 lottery_fix.py > $L/lf.log 2>&1
python3 posthoc_lottery.py > $L/ph.log 2>&1
python3 fix_analysis.py > $L/fa.log 2>&1
python3 analyse_xs.py FS03 FS04 FS06 > $L/ax1.log 2>&1 &
python3 analyse_xs.py FS07 FS08 FS09 > $L/ax2.log 2>&1 &
python3 analyse_xs.py FS10 FS11 FS12 > $L/ax3.log 2>&1 &
python3 battery.py US EU UK > $L/bat1.log 2>&1 &
python3 battery.py DK SC > $L/bat2.log 2>&1 &
wait
python3 battery.py WD > $L/bat3.log 2>&1
python3 financing.py > $L/fin.log 2>&1
python3 common_ground.py > $L/cg.log 2>&1
python3 nbh_figs.py > $L/nbf.log 2>&1
python3 make_figures.py > $L/mf.log 2>&1
echo ALLDONE > $L/done.log
