
ccd_time -f data/frequencies.dat --times data/times.dat^
    -d data/data.dat^
    -o results_time^
    --data_format "cre_cmim"^
    -c 1^
    --tm_i_lambda 5^
    --plot --plot_lcurve -1

REM plot time evolutation
REM only works with --output_format ascii
REM ddpt.py --plot_stats -i output${outdir}

pause
