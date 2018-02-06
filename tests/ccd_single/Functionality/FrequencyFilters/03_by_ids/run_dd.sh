#!/bin/bash
# filter frequency id 4 (number 5): 0.01 Hz and id 12 (number 13): 1 Hz

test -d results && rm -r results
ccd_single -f frequencies.dat -d data.dat\
	--ignore "4,12"\
   	-o results\
    --lambda 1.0\
    -c 1
