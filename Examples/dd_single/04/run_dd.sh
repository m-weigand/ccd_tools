#!/bin/bash
test -d results && rm -r results
dd_single.py -f frequencies.dat -d data.dat -n 20 -o results --tausel data_ext\
    --lambda 1\
    --nr_cores=1\
    --ignore 2\
    --plot\
    #--plot_lcurve -1

exit
test -d results_n && rm -r results_n
dd_single.py -f frequencies.dat -d data.dat -n 20 -o results_n --tausel data_ext\
    --lambda 1\
    --nr_cores=1\
    --ignore 2\
    --plot\
    --norm_mag 25
    #--plot_lcurve -1
