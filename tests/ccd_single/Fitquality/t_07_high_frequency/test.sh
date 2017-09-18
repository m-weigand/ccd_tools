#!/bin/bash
rm -r results_data results_dataext

debye_decomposition.py -f frequencies.dat -d data.dat -n 20 -c 1 -o results_data --plot --silent

debye_decomposition.py -f frequencies.dat -d data.dat -n 20 -c 1 -o results_dataext --plot --silent --tausel data_ext
