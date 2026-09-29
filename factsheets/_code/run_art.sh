#!/bin/sh
cd "$(dirname "$0")"
L=../results/logs_art; mkdir -p $L
for R in US_A EU_A UK_A DK_A; do (python3 signals.py $R > $L/sig_$R.log 2>&1; python3 signals2.py $R > $L/sig2_$R.log 2>&1) & done; wait
python3 signals.py WD_A > $L/sig_WD_A.log 2>&1; python3 signals2.py WD_A > $L/sig2_WD_A.log 2>&1
echo SIGDONE > $L/sigdone.log
