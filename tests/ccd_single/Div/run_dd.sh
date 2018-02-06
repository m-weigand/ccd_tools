#!/bin/bash
test -d results && rm -r results
ccd_single -f frequencies.dat -d data.dat -c 1 --plot -o results


test -d results1 && rm -r results1
ccd_single -f frequencies.dat -d data.dat -c 1 --plot -o results1 --norm 100
