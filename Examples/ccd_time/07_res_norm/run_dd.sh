#!/bin/bash

DD_USE_LATEX=0

# fit without any time regularization
outdir="results_no_time"
test -d ${outdir} && rm -r ${outdir}
DD_STARTING_MODEL=3 dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    -c 1 --plot\
	--norm 10\
	--f_lambda 1 --output_format ascii

# fit with time regularization in rho0
outdir="results_time_rho0"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    -c 1\
    --trho0_lambda 100\
    --plot --output_format ascii

# compare both fits
ddpt.py --plot_stats --compare results_no_time results_time_rho0
