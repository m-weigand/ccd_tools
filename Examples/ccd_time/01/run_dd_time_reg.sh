#!/bin/bash

# fit with time regularization in rho0
outdir="results_time_rho0"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    --trho0_lambda 100\
    --plot
