#!/bin/bash
test -d output && rm -r output
dd_single.py -d data.dat -f frequencies.dat -p -i -n 80 -o output
