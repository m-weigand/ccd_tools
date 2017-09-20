#!/bin/bash

export DD_COND=0
ccd_single -f frequencies.dat -d data.dat -n 20 -o results_res_plot --plot
