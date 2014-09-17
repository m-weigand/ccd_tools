#!/bin/bash


odir="results_norm"
test -d "${odir}" && rm -r "${odir}"
dd_time.py --time times.dat -f frequencies.dat -d data.dat -n 20 -o "${odir}" \
    --f_lambda 1.0\
    --norm_mag 50\
    --plot

exit
odir="results_no_norm"
test -d "${odir}" && rm -r "${odir}"
dd_single.py -f frequencies.dat -d data.dat -n 20 -o "${odir}" \
    --nr_cores=1\
    --lambda 1.0\
    --plot
