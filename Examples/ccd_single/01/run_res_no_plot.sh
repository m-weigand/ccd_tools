#!/bin/bash

export DD_COND=0
dd_single.py -f frequencies.dat -d data.dat -n 20 -o results_res_no_plot
