set DD_COND=1
set DD_STARTING_MODEL=3

dd_single.py^
	-f frequencies.dat -d data.dat -n 20^
	-o results_conductivity --tausel data_ext^
    --nr_cores=1^
    --tausel data_ext^
    --lambda 1.0^
    --plot -c 1^
	--max_it 20^
	--norm 50
REM  --plot_its

set DD_COND=0
set DD_STARTING_MODEL=3

dd_single.py^
	-f frequencies.dat -d data.dat -n 20^
	-o results_resistivity_norm25 --tausel data_ext^
    --nr_cores=1^
    --tausel data_ext^
    --lambda 1.0^
    --plot -c 1^
	--norm 25

set DD_COND=0
set DD_STARTING_MODEL=3

dd_single.py^
	-f frequencies.dat -d data.dat -n 20^
	-o results_resistivity_no_norm --tausel data_ext^
    --nr_cores=1^
    --tausel data_ext^
    --lambda 1.0^
    --plot -c 1
