#!/bin/bash
# this example uses two strategies to determine the starting model:

test -d results && rm -r results
dd_single.py -f frequencies.dat -d data.dat\
   	-o results\
    --lambda 1.0\
    -c 1
