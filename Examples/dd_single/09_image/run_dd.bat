dd_single.py -f frequencies.dat -d data.dat -n 20 -o results --tausel data_ext^
    -c 2^
    --tausel data_ext^
    --lambda 1.0^
	--output_format ascii

REM plot the results into a grid
ddps.py --plot_to_grid --elem GRID/elem.dat --elec GRID/elec.dat -i results/

pause
