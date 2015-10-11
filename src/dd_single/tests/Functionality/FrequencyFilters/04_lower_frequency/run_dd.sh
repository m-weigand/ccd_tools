#!/bin/bash
# filter all frequencies below 1 Hz

test -d results && rm -r results
dd_single.py -f frequencies.dat -d data.dat\
	--fmin 1.0\
   	-o results\
    --lambda 1.0\
    -c 1
