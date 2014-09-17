#!/bin/bash
# Run DD using
# a) no time-regularization
# b) 1st order time-reg.
# c) 1st order time-reg. with time-weighting
# d) 2nd order time-reg

function dd
{
    outdir="$1"
    flam="$2"
    mlam="$3"
    additional_options="$4"
    test -d ${outdir} && rm -r ${outdir}
    dd_time.py -f data/frequencies.dat --times data/times.dat\
        -d data/data.dat\
        -o ${outdir}\
        --f_lambda ${flam}\
        --tm_i_lambda ${mlam}\
        -c 1\
        --plot ${additional_options}
    ddpt.py --plot_stats -i "${outdir}"

}
### a ###
dd "results_time_no_reg" 1 0 ""
dd "results_time_first_order" 1 5 " --tmi_first_order "
dd "results_time_first_order_time_weighting" 1 5 " --tmi_first_order --tw_mi"
dd "results_time_second_order" 1 5 ""
