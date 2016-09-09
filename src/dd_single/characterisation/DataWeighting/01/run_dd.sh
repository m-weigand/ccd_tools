#!/bin/bash

function fit_data(){
	dw=${1}

	odir="results_${dw}"
	test -d "${odir}" && rm -r "${odir}"
	DD_COND=1 DD_STARTING_MODEL=3 dd_single.py \
		-f data/frequencies.dat \
		-d data/data.dat \
		-n 20 \
		--norm 100 \
		--tausel "100,100" \
		-o "${odir}" \
		--lambda 3000 \
		-c 1 \
		--plot\
		--data_weighting ${dw}

	# lambda 6500
}

fit_data re_vs_im
fit_data all_to_one
fit_data one
fit_data avg_im
fit_data avg_im_err
