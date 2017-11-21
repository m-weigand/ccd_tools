#!/bin/bash
test -d results_time_reg && rm -r results_time_reg
dd_time.py -f frequencies.dat --times times.dat -d data.dat\
    -o results_time_reg\
    --f_lambda 5\
    --tm_i_lambda 0\
    --trho0_lambda 0 --plot
