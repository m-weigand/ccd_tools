#!/bin/bash


odir="results_norm"
test -d "${odir}" && rm -r "${odir}"
dd_single.py -f frequencies.dat -d data.dat -n 20 -o "${odir}" \
    --nr_cores=1\
    --lambda 1.0\
    --plot
    # --norm_mag 50\

exit
odir="results_no_norm"
test -d "${odir}" && rm -r "${odir}"
dd_single.py -f frequencies.dat -d data.dat -n 20 -o "${odir}" \
    --nr_cores=1\
    --lambda 1.0\
    --plot
