#!/bin/bash
test -d results && rm -r results
dd_single.py -f frequencies.dat -d data.dat -c 1 --plot -o results


test -d results1 && rm -r results1
dd_single.py -f frequencies.dat -d data.dat -c 1 --plot -o results1 --norm_mag 100
