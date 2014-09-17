#!/bin/bash
test -d results/plot_stats_grid && rm -r results/plot_stats_grid
ddps.py --elem GRID/elem.dat --elec GRID/elec.dat -i results/ --plot_to_grid
