#!/bin/bash

test -d results && rm -r results
ccd_single -f frequencies.dat -d data.dat -n 20 -o results --tausel data_ext\
    --lambda 1\
    --nr_cores=1\
    --ignore 2\
    --plot\
    #--plot_lcurve -1
