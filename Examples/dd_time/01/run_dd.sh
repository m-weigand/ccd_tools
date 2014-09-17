#!/bin/bash

# fit without any time regularization
outdir="results_no_time"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    -c 1\
    --plot

# fit with time regularization in rho0
outdir="results_time_rho0"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    -c 1\
    --trho0_lambda 100\
    --plot

# compare both fits
ddpt.py --plot_stats --compare results_no_time results_time_rho0
