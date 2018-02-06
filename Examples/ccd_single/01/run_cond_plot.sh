#!/bin/bash
set DD_COND=1
ccd_single -f frequencies.dat -d data.dat -n 20 -o results --plot
