#!/bin/bash

DD_STARTING_PARAMETERS=3 dd_single.py \
   	-d data.dat -f frequencies.dat \
	-c 1 -n 20 \
	--output_format ascii \
	-o dd_fit