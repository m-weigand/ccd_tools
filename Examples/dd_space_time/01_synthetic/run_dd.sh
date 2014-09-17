#!/bin/bash
test -d results && rm -r results
dd_space_time.py -f data/data/frequencies.dat -d data/data/data_index.dat --times data/data/times.dat  -o results/ -c 1
