#!/bin/bash

function time_reg_good
{
    odir="results_good"
    test -d "${odir}" && rm -r "${odir}"
    dd_time.py -f data/frequencies.dat\
        --times data/times.dat\
        -d data/data.dat\
        -o "${odir}"\
        -c 1\
        -n 20\
        --tausel data_ext\
        --f_lambda 1\
        --tm_i_lambda 5\
        --tmi_first_order\
        --plot

    ddpt.py -i "${odir}" --plot_stats
}

function time_reg
{
    odir="$1"
    mlam=$2
    flam=$3
    test -d "${odir}" && rm -r "${odir}"
    dd_time.py -f data/frequencies.dat\
        --times data/times.dat\
        -d data/data.dat\
        -o "${odir}"\
        -n 20\
        -c 1\
        --tausel data_ext\
        --f_lambda ${flam}\
        --tmi_first_order\
        --tm_i_lambda ${mlam}\
        --plot

    ddpt.py -i "${odir}" --plot_stats
}

# time_reg "OUTPUT_FILE" m_lam f_lam
time_reg "results_good" 5 1
# time_reg "results_no_tr" 0 1
# time_reg "results_bad_0" 1 1
# time_reg "results_bad_1" 5 1
# time_reg "results_bad_2" 50 1
time_reg "results_bad_3" 500 1
# time_reg "results_bad_4" 5000 1
# time_reg "results_bad_5" 50000 1
# time_reg "results_bad_6" 100000 1
