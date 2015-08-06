set DD_STARTING_MODEL=1

dd_single.py -f frequencies.dat -d data.dat -n 20 -o results_1 --tausel data_ext^
    --nr_cores=1^
    --tausel data_ext^
    --lambda 1.0^
    --plot -c 1 --max_it 20 --plot_its
