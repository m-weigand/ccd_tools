#!/bin/bash

odir="results"
test -d "${odir}" && rm -r "${odir}"
DD_STARTING_MODEL=3 dd_single.py -f frequencies.dat -d data.dat -n 20\
   	-o "${odir}" \
	--tausel data_ext\
    --nr_cores=1\
    --tausel "100,100"\
    --lambda 1.0\
    --plot -c 1 --max_it 20
