#!/bin/bash
test -d results_time_reg && rm -r results_time_reg
ccd_time -f frequencies.dat --times times.dat -d data.dat -o results_time_reg -c 1 --tausel data_ext\
    --f_lambda 5\
    --tm_i_lambda 0\
    --trho0_lambda 0\
	--output_format ascii

# test these time regularisation parameters
    #--tm_i_lambda 1\
    #--trho0_lambda 10000
ddpt.py -i results_time_reg/ --plot_stats
