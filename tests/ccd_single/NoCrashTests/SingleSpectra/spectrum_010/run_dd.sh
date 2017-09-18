#!/bin/bash
test -d results && rm -r results
time dd_single.py -f frequencies.dat -d data.dat\
    -n 10 -o results\
    --tausel data_ext\
    --nr_cores=1\
    --plot
#| tee logfile
