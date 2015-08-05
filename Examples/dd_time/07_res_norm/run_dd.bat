REM fit without time regularisation
set DD_STARTING_MODEL=3
dd_time.py -f data/frequencies.dat --times data/times.dat\
    -d data/data.dat^
    -o results_no_time^
    -c 1 --plot^
	--norm 10^
	--f_lambda 1 --output_format ascii

REM fit with time regularization in rho0
dd_time.py -f data/frequencies.dat --times data/times.dat^
    -d data/data.dat^
    -o results_time_rho0^
    -c 1^
    --trho0_lambda 100^
    --plot --output_format ascii

REM compare both fits
ddpt.py --plot_stats --compare results_no_time results_time_rho0
