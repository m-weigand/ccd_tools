#!/bin/bash
function baseline()
{
    test -d results_no_time && rm -r results_no_time
    dd_time.py -f data/frequencies.dat\
        --times data/times.dat\
        -d data/data.dat\
        -o results_no_time\
        -c 1\
        --tausel data_ext\
        --tm_i_lambda 0\
        --trho0_lambda 0\
        --plot\
		--output_format ascii

    ddpt.py -i results_no_time --plot_stats
}

function rho0_reg()
{
    test -d results && rm -r results
    dd_time.py -f data/frequencies.dat\
        --times data/times.dat\
        -d data/data.dat\
        -o results\
        -c 1\
        --tausel data_ext\
        --tm_i_lambda 0\
        --trho0_lambda 100000\
        --plot\
		--output_format ascii

    ddpt.py -i results/ --plot_stats
}

function rho0_time_diff()
{
    test -d results_tw && rm -r results_tw
    dd_time.py -f data/frequencies.dat\
        --times data/times.dat\
        -d data/data.dat\
        -o results_tw\
        -c 1\
        --tausel data_ext\
        --trho0_first_order\
        --trho0_lambda 600000\
        --plot\
        --tw_rho0\
		--output_format ascii

    ddpt.py -i results_tw/ --plot_stats
}


baseline
rho0_reg
rho0_time_diff
