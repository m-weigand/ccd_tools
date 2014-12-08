#!/bin/bash
# unpack data
test -d data || tar xvjf data.tar.bz2

# fit
test -d results && rm -r results
dd_space_time.py -f data/data/frequencies.dat\
    -d data/data/data_index.dat\
    --times data/data/times.dat\
    --f_lambda 50\
    -o results/\
    -c 1
