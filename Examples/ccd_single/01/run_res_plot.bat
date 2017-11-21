REM uncomment the next line to activate Latex support
REM set DD_USE_LATEX=1
set DD_COND=0
dd_single.py -f frequencies.dat -d data.dat -n 20 -o results_res_plot --plot

pause
