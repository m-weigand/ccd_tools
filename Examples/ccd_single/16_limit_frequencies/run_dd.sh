#!/bin/bash

odir="results"
test -d "${odir}" && rm -r "${odir}"
test -d results && rm -r results
DD_STARTING_MODEL=3 ccd_single \
	-f frequencies.dat -d data.dat\
   	-n 20 \
	-o "${odir}"\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
	--norm 10\
	--fmax 101
