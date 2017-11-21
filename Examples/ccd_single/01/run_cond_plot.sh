#!/bin/bash
set DD_COND=1
dd_single.py -f frequencies.dat -d data.dat -n 20 -o results --plot
