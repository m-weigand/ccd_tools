#!/bin/bash
test -d results_no_time_reg && rm -r results_no_time_reg
dd_time.py -f frequencies.dat --times times.dat -d data.dat\
    -o results_no_time_reg -c 1 --plot\
    --f_lambda 5\
    --tm_i_lambda 0\
    --trho0_lambda 0 --output_format ascii
ddpt.py -i results_no_time_reg/ --plot_stats


test -d results_time_reg && rm -r results_time_reg
dd_time.py -f frequencies.dat --times times.dat -d data.dat\
    -o results_time_reg -c 1 --plot\
    --f_lambda 5\
    --tm_i_lambda 1\
    --trho0_lambda 10000 --output_format ascii
ddpt.py -i results_time_reg/ --plot_stats
