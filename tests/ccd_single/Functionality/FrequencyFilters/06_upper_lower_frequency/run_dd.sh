#!/bin/bash
# filter all frequencies below 1 Hz and above 100 Hz

test -d results && rm -r results
ccd_single -f frequencies.dat -d data.dat\
	--fmin 1\
	--fmax 100.0\
   	-o results\
    --lambda 1.0\
    -c 1
