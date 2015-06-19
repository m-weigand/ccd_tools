#!/bin/bash

function test_res(){
	outdir="results_resistivity_nonorm"
	test -d "${outdir}" && rm -r "${outdir}"
	DD_COND=0 DD_STARTING_MODEL=3 dd_single.py\
		-f frequencies.dat -d data_rmagrpha.dat -n 20\
		-o "${outdir}" --tausel data_ext\
		--nr_cores=1\
		--tausel data_ext\
		--lambda 1.0
	#    --plot -c 1

	outdir="results_resistivity_norm25"
	test -d "${outdir}" && rm -r "${outdir}"
	DD_COND=0 DD_STARTING_MODEL=3 dd_single.py\
		-f frequencies.dat -d data_rmagrpha.dat -n 20\
		-o "${outdir}" --tausel data_ext\
		--nr_cores=1\
		--tausel data_ext\
		--lambda 1.0\
		--norm 25
		# --plot -c 1

	outdir="results_resistivity_norm50"
	test -d "${outdir}" && rm -r "${outdir}"
	DD_COND=0 DD_STARTING_MODEL=3 dd_single.py\
		-f frequencies.dat -d data_rmagrpha.dat -n 20\
		-o "${outdir}" --tausel data_ext\
		--nr_cores=1\
		--tausel data_ext\
		--lambda 1.0\
		--norm 50
	#   --plot -c 1

	outdir="results_resistivity_norm75"
	test -d "${outdir}" && rm -r "${outdir}"
	DD_COND=0 DD_STARTING_MODEL=3 dd_single.py\
		-f frequencies.dat -d data_rmagrpha.dat -n 20\
		-o "${outdir}" --tausel data_ext\
		--nr_cores=1\
		--tausel data_ext\
		--lambda 1.0\
		--norm 75
	#    --plot -c 1

	for i in `ls -1 | grep results_resistivity`; do cat $i/stats_and_rms/rho0_results.dat; done
	for i in `ls -1 | grep results_resistivity`; do cat $i/data_rmagrpha.dat | cut -f 1 -d ' '; done
	for i in `ls -1 | grep results_resistivity`; do cat $i/data_format.dat; echo ""; done
	for i in `ls -1 | grep results_resistivity`; do cat $i/f.dat | cut -f 1 -d ' '; done
}

function test_cond(){

	pltstr=" --plot "
	# pltdtr=""

	outdir="results_conductivity_nonorm"
	test -d "${outdir}" && rm -r "${outdir}"
	DD_COND=1 DD_STARTING_MODEL=3 dd_single.py\
		-f frequencies.dat -d data_rmagrpha.dat -n 20\
		-o "${outdir}" --tausel data_ext\
		--nr_cores=1\
		--tausel data_ext\
		--lambda 1.0 ${pltstr}

	outdir="results_conductivity_norm25"
	test -d "${outdir}" && rm -r "${outdir}"
	DD_COND=1 DD_STARTING_MODEL=3 dd_single.py\
		-f frequencies.dat -d data_rmagrpha.dat -n 20\
		-o "${outdir}" --tausel data_ext\
		--nr_cores=1\
		--tausel data_ext\
		--lambda 1.0\
		--norm 25 ${pltstr}

	outdir="results_conductivity_norm50"
	test -d "${outdir}" && rm -r "${outdir}"
	DD_COND=1 DD_STARTING_MODEL=3 dd_single.py\
		-f frequencies.dat -d data_rmagrpha.dat -n 20\
		-o "${outdir}" --tausel data_ext\
		--nr_cores=1\
		--tausel data_ext\
		--lambda 1.0\
		--norm 50 ${pltstr}

	outdir="results_conductivity_norm75"
	test -d "${outdir}" && rm -r "${outdir}"
	DD_COND=1 DD_STARTING_MODEL=3 dd_single.py\
		-f frequencies.dat -d data_rmagrpha.dat -n 20\
		-o "${outdir}" --tausel data_ext\
		--nr_cores=1\
		--tausel data_ext\
		--lambda 1.0\
		--norm 75 ${pltstr}
}

function check_cond(){

	for i in `ls -1 | grep results_conductivity`; do echo $i; done
	echo "rho0"
	for i in `ls -1 | grep results_conductivity`; do cat $i/stats_and_rms/rho0_results.dat; done
	echo "data.dat, first col"
	for i in `ls -1 | grep results_conductivity`; do cat $i/data.dat | cut -f 1 -d ' '; done
	echo "data format"
	for i in `ls -1 | grep results_conductivity`; do cat $i/data_format.dat; echo ""; done
	echo "forward, first col"
	for i in `ls -1 | grep results_conductivity`; do cat $i/f.dat | cut -f 1 -d ' '; done
}

# test_cond
check_cond
