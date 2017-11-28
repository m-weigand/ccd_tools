#!/bin/bash
# extend the frequency range assymetrically: extend the low frequency by a
# factor of 10, and the hight frequencies by a factor of 1000
test -d results && rm -r results
dd_single.py -f frequencies.dat -d data.dat\
    -n 20\
    -o results\
    --tausel "10,1000"\
    --nr_cores=1\
    --plot
