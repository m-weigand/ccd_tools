#!/bin/bash
test -d results && rm -r results
ccd_single -f frequencies.dat -d data.dat -n 20\
	-o results\
   	--tausel data_ext\
    --nr_cores=1\
	--norm 10\
    --lambda 50

