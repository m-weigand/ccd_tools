#!/bin/bash
rm -r test_dd
debye_decomposition.py -f frequencies.dat -d data.dat -c 2 -o test_dd -n 10 --plot --plot_its
