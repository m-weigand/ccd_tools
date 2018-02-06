#!/bin/bash
# filter all frequencies above 100 Hz

test -d results && rm -r results
ccd_single -f frequencies.dat -d data.dat\
	--fmax 100.0\
   	-o results\
    --lambda 1.0\
    -c 1
