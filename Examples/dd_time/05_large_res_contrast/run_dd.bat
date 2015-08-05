dd_time.py -f data/frequencies.dat --times data/times.dat^
    -d data/data.dat^
    -o results_time^
    --data_format "cre_cmim"^
    -c 1^
    --tm_i_lambda 5^
    --norm 100 --plot --output_format ascii

REM plot time evolutation
ddpt.py --plot_stats -i results_time
