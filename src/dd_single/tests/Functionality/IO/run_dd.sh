#!/bin/bash

function fit_data(){
	format=${1}

	odir="results_${format}"
	test -d "${odir}" && rm -r "${odir}"
	DD_COND=1 DD_STARTING_MODEL=3 dd_single.py \
		-f data/frequencies.dat \
		-d data/data.dat \
		--output_format ${format} \
		-n 20 \
		--norm 100 \
		--tausel "100,100" \
		-o "${odir}" \
		--lambda 3000 \
		-c 1
}

fit_data ascii
fit_data ascii_audit
