#!/bin/bash
test -d results_time && rm -r results_time
dd_time.py -f frequencies.dat -d data.dat --times times.dat -o results_time --plot\
    --ignore 2 --norm_mag 25
