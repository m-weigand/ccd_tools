#!/bin/bash

function run_dd
{
	ddc="${1}"

	odir="results_ddc_${ddc}"
	test -d "${odir}" && rm -r "${odir}"
	DD_STARTING_MODEL=3 DD_C=${ddc} dd_single.py\
		-o ${odir} \
		--output_format ascii \
		--lambda 5 \
		--plot
}

run_dd 0.3
run_dd 0.5
run_dd 0.7
run_dd 1.0
