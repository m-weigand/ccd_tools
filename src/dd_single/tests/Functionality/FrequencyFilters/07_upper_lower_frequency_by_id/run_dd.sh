#!/bin/bash
# filter all frequencies below 1 Hz and above 100 Hz
# filter 10 Hz

test -d results && rm -r results
dd_single.py -f frequencies.dat -d data.dat\
	--ignore 16\
	--fmin 1\
	--fmax 100.0\
   	-o results\
    --lambda 1.0\
    -c 1
