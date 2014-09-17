#!/bin/bash
rm -r results
debye_decomposition.py -f frequencies.dat -d data.dat -c 2 -o results -n 10 --plot
