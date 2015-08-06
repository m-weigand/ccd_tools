dd_time.py -f frequencies.dat --times times.dat -d data.dat -o results_time_reg -c 1 --tausel data_ext^
    --f_lambda 5^
    --tm_i_lambda 0^
    --trho0_lambda 0^
	--output_format ascii

ddpt.py -i results_time_reg/ --plot_stats

pause
