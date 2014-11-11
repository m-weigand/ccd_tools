#!/bin/bash
test -d results && rm -r results
dd_single.py -f frequencies.dat -d data.dat -n 20 -o results --nr_cores=1\
     --plot --plot_lcurve -1

test -d results_cond && rm -r results_cond
DD_COND=1 dd_single.py -f frequencies.dat -d data.dat -n 20 -o results_cond --nr_cores=1\
    --plot --plot_lcurve -1 --norm 1
