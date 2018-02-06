#!/bin/bash
# this example uses two strategies to determine the starting model:

test -d results && rm -r results
DD_STARTING_MODEL=1 ccd_single -f frequencies.dat -d data.dat -n 20 -o results --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
    -c 1 --max_it 20

# try again, this should raise an Exception
DD_STARTING_MODEL=1 ccd_single -f frequencies.dat -d data.dat -n 20 -o results --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
    -c 1 --max_it 20 --plot_its
