#!/bin/bash
output_dir="results_filtered"
test -d ${output_dir} && rm -r ${output_dir}
ddps.py -i results -o ${output_dir} --filter --log10mtotn "-2.7" --nr_cpus 4
ddps.py --elem GRID/elem.dat --elec GRID/elec.dat -i ${output_dir} --plot_to_grid

# now test if at least one grid was plotted
nr_figures=`ls -1 ${output_dir}/plots_stats_grid/ | wc -l`

if [ ${nr_figures} -eq 0 ]; then
    echo "No figures plotted"
    rm -r "${output_dir}"
    exit 1
else
    rm -r "${output_dir}"
fi
