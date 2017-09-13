#!/bin/bash
test -d results && rm -r results
DD_COND=1 dd_single.py -f frequencies.dat -d data.dat -n 20\
   	-o results\
   	--tausel data_ext\
    --nr_cores=1\
	--norm 10\
    --lambda 50

