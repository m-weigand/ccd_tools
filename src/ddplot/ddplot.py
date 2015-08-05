"""
ddplot.py can create plots from plot results created using dd_single.py and
dd_time.py

Copyright 2014,2015 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
# from memory_profiler import *
import json
from multiprocessing import Pool
import shutil
from optparse import OptionParser
import os
import glob
import numpy as np
from NDimInv.plot_helper import *
import NDimInv.elem as elem
import dd_single
import NDimInv
import lib_dd.plot as lDDp


def handle_cmd_options():
    parser = OptionParser()
    parser.add_option("-i", "--dir", type='string', metavar='DIR',
                      help="dd_time result directory default=results",
                      default="results", dest="result_dir")

    parser.add_option("--log10mtot", type='float', metavar='FLOAT',
                      help="Remove all spectra with log10(mtot) below " +
                      "threshold for filter-enabled plots", default=None,
                      dest="filter_log10mtot")
    parser.add_option("--log10mtotn", type='float', metavar='FLOAT',
                      help="Remove all spectra with log10(mtotn) below " +
                      "threshold for filter-enabled plots", default=None,
                      dest="filter_log10mtotn")

    parser.add_option("--statistics", action="store_true",
                      dest="compute_statistics",
                      help="Compute statistics of stats",
                      default=False)
    parser.add_option("--plot_specs", action="store_true",
                      dest="plot_specs", help="Plot specs",
                      default=False)
    parser.add_option("--plot_reg_strengths", action="store_true",
                      dest="plot_reg_strength", default=False,
                      help="Plot regularization strengths")
    parser.add_option("--range", dest="spec_ranges", type="string",
                      help="Pixel range(s) to plot. Separate by ';' and " +
                      "start with 1. For example: \"1;2;4;5\". " +
                      "Also allowed are ranges: \"2-10\", and open ranges: " +
                      "\"5-\" (default: -1 (all))",
                      default=None)

    parser = _add_dd_grid_plot_opts(parser)

    parser.add_option("--filter", action="store_true",
                      dest="apply_filters", default=False,
                      help="Apply filters and save to new directory")
    parser.add_option("--maskfile", type='str', metavar='FILE',
                      help="Mask file for filtering",
                      default=None, dest="maskfile")
    parser.add_option("--nr_cpus", type='int', metavar='NR',
                      help="Output directory", default=1,
                      dest="nr_cpus")
    parser.add_option('-o', "--output", type='str', metavar='DIR',
                      help="Output directory (default: filtered_results)",
                      default='filtered_results',
                      dest="output_dir")

    (options, args) = parser.parse_args()
    return options, args


if __name__ == '__main__':
    pass
