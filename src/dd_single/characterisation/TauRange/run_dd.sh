#!/bin/bash
# apply the debye decomposotion to the generated data using various settings
data_file="data/data.dat"
frequency_file="data/frequencies.dat"

odir='results_tausel_data'
test -d ${odir} && rm -r ${odir}
dd_single.py -f ${frequency_file} -d ${data_file} -n 10 -c 1 -o ${odir} --tausel data --plot --plot_lcurve -1\
    --lambda 1.0

odir='results_tausel_data_ext'
test -d ${odir} && rm -r ${odir}
dd_single.py -f ${frequency_file} -d ${data_file} -n 10 -c 1 --tausel data_ext -o ${odir} --plot --plot_lcurve -1\
    --lambda 1.0
