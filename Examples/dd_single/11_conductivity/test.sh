#!/bin/bash
# this example uses two strategies to determine the starting model:


outdir="results_resistivity_norm25"
test -d "${outdir}" && rm -r "${outdir}"
DD_COND=0 DD_STARTING_MODEL=3 dd_single.py\
	-f frequencies.dat -d data.dat -n 20\
	-o "${outdir}" --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
	--norm 25\
    --plot -c 1

exit

outdir="results_cond_25"
test -d "${outdir}" && rm -r "${outdir}"
DD_COND=1 DD_STARTING_MODEL=3 dd_single.py\
	-f frequencies.dat -d data.dat -n 20\
	-o "${outdir}" --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
	--norm 50\
    --plot -c 1
