#!/bin/bash

outdir="results_time"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    --data_format "cre_cmim"\
    -c 1\
    --tm_i_lambda 5\
    --norm 100 --plot --output_format ascii

# plot time evolutation
ddpt.py --plot_stats -i ${outdir}
