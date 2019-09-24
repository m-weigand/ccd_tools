#!/bin/bash

ccd_time \
	-f data/frequencies.dat\
	--times data/times.dat\
	-d data/data.dat\
	-o "results_time"\
	--f_lambda 50\
	--tmi_first_order\
	--tm_i_lambda 5000\
	--plot
