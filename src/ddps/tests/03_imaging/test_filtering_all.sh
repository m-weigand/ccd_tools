#!/bin/bash
test -d results_filtered && rm -r results_filtered
ddps.py -i results -o results_filtered --filter --log10mtotn -2.5 --nr_cpus 4
