#!/bin/bash
# this example uses two strategies to determine the starting model:

test -d results && rm -r results
ccd_single -f frequencies.dat -d data.dat\
   	-o results\
    --lambda 1.0\
    -c 1
