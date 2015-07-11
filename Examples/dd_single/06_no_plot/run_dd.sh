#!/bin/bash
test -d results && rm -r results
python -m memory_profiler `which dd_single.py` -f frequencies.dat -d data.dat -n 20 -o results --tausel data_ext\
    --nr_cores=1\
    --lambda 50\
    --plot #\
    #--plot_lcurve -1
