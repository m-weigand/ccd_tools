REM This is a windows bat file, rename the ending to .bat, and execute

set DD_COND=0
dd_single.py -f frequencies.dat -d data.dat -n 20 -o results --tausel data_ext --nr_cores=1 --plot
