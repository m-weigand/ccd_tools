#!/bin/bash
# test -d results && rm -r results
# for i in `seq 0 4`;
# do
#    mkdir -p results/tmp_ts_`printf %.4i $i`
# done
# echo 'done creating'
dd_space_time.py -f data/data/frequencies.dat\
    -d data/data/data_index.dat\
    --times data/data/times.dat\
    --f_lambda 50\
    -o results/\
    -c 1
