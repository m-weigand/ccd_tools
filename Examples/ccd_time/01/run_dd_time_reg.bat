REM fit with time regularization in rho0
cdd_time -f data/frequencies.dat --times data/times.dat^
    -d data/data.dat^
    -o results_time_rho0^
    -c 1^
    --trho0_lambda 100^
    --plot

pause
