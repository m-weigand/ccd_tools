#!/bin/bash

test -d results_starting_model1 && rm -r results_starting_model1
DD_STARTING_MODEL=1 dd_single.py -o results_starting_model1\
	-c 1\
	--plot\
	--plot_its\
	--lambda 300

test -d results_starting_model3 && rm -r results_starting_model3
DD_STARTING_MODEL=3 dd_single.py -o results_starting_model3\
	-c 1\
	--plot\
	--plot_its\
	--lambda 300
