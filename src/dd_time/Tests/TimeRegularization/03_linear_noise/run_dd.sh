#!/bin/bash
# Run DD using
# a) no time-regularization
# b) 1st order time-reg.
# c) 1st order time-reg. with time-weighting
# d) 2nd order time-reg

f_lambda=200
### a ###
outdir="results_time_no_reg"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    --f_lambda ${f_lambda}\
    -c 1\
    --plot
ddpt.py --plot_stats -i "${outdir}"

### b ###
outdir="results_time_first_order"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    -c 1\
    --tmi_first_order\
    --f_lambda ${f_lambda}\
    --tm_i_lambda 5\
    --plot

# plot time evolutation
ddpt.py --plot_stats -i "${outdir}"

### c ###
outdir="results_time_first_order_time_weighting"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    -c 1\
    --tmi_first_order\
    --tm_i_lambda 5\
    --f_lambda ${f_lambda}\
    --tw_mi\
    --plot

# plot time evolutation
ddpt.py --plot_stats -i "${outdir}"

### d ###
outdir="results_time_second_order"
test -d ${outdir} && rm -r ${outdir}
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat\
    -o ${outdir}\
    -c 1\
    --f_lambda ${f_lambda}\
    --tm_i_lambda 5\
    --plot

# plot time evolutation
ddpt.py --plot_stats -i "${outdir}"
