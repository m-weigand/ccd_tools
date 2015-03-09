#!/bin/bash
# this example uses two strategies to determine the starting model:

outdir="results_conductivity"
test -d "${outdir}" && rm -r "${outdir}"
DD_COND=1 DD_STARTING_MODEL=3 dd_single.py\
	-f frequencies.dat -d data.dat -n 20\
	-o "${outdir}" --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
    --plot -c 1\
	--max_it 20\
	--norm 50
	# --plot_its

outdir="results_resistivity"
test -d "${outdir}" && rm -r "${outdir}"
DD_COND=0 DD_STARTING_MODEL=3 dd_single.py\
	-f frequencies.dat -d data.dat -n 20\
	-o "${outdir}" --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
    --plot -c 1\
	--norm 50

outdir="results_resistivity_no_norm"
test -d "${outdir}" && rm -r "${outdir}"
DD_COND=0 DD_STARTING_MODEL=3 dd_single.py\
	-f frequencies.dat -d data.dat -n 20\
	-o "${outdir}" --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
    --plot -c 1
