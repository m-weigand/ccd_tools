#!/bin/bash
# this example uses two strategies to determine the starting model:


test -d results3 && rm -r results3
DD_C=0.5 DD_STARTING_MODEL=3 dd_single.py -f frequencies.dat -d data.dat -n 20 -o results3 --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
    -c 2
