#!/bin/bash

test -d results_3 && rm -r results_3

DD_STARTING_MODEL=3 dd_single.py -f frequencies.dat -d data.dat -n 20 -o results_3 --tausel data_ext\
    --nr_cores=1\
    --tausel data_ext\
    --lambda 1.0\
    --plot -c 1 --max_it 20 --plot_its\
	--output_format ascii
