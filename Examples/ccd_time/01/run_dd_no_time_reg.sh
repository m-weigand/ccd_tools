#!/bin/bash

# fit without any time regularization
outdir="results_no_time"
test -d ${outdir} && rm -r ${outdir}
DD_STARTING_MODEL=3 dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    -c 1 --plot\
	--f_lambda 1 --output_format ascii_audit
