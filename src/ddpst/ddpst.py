"""
ddpst.py is the post-processing tool for dd_space_time.py

Copyright 2014 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.

This tool operates on inversion results created by dd_space_time.py and offers
the following functions:
    -

Planned features:
    - plot (selected) spectra
    - plot (selected) iterations
    - filter spectra based on statistical values
"""
from optparse import OptionParser
from NDimInv.plot_helper import *
import numpy as np
import os
import glob
import shutil
import ddps
import crlab_py.elem as elem


def handle_cmd_options():
    parser = OptionParser()
    parser.add_option("-i", "--dir", type='string', metavar='DIR',
                      help="dd_space_time result directory default=results",
                      default="results", dest="result_dir")

    parser.add_option('-a', "--aggregate", action="store_true",
                      dest="aggregate",
                      help="Aggregate plot results (default: False)",
                      default=False)
    parser = ddps._add_dd_grid_plot_opts(parser)
    (options, args) = parser.parse_args()
    return options, args


def aggregate_results(options):
    """Assemble the fit results for all pixels of each time series
    """
    outdir = os.path.abspath(options.result_dir) + '/stats_and_rms_agg'
    indir = os.path.abspath(options.result_dir) + '/fits'

    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)

    ts_dirs = sorted(glob.glob(indir + '/tmp_ts_*'))
    result_files = [os.path.basename(x) for x in
                    glob.glob(ts_dirs[0] + '/stats_and_rms/*.dat')]

    for filename in result_files:
        data_list = []
        for ts in ts_dirs:
            # open data file
            data = np.loadtxt(ts + '/stats_and_rms/' + filename)
            data_list.append(data)
        data_all = np.array(data_list)
        print filename, data_all.shape
        # for now, save only 1D or 2D results
        if len(data_all.shape) <= 2:
            np.savetxt(outdir + os.sep + filename, data_all)


def plot_to_grids(data, key, options):
    nr_total = data.shape[1]
    nr_x = min(5, nr_total)
    nr_y = int(np.ceil(nr_total / nr_x))
    fig, axes = plt.subplots(nr_y, nr_x, figsize=(nr_x * 2, nr_y * 2))

    global_min = np.nanmin(data)
    global_max = np.nanmax(data)
    elem.plt_opt.cbmin = getattr(options, key + '_min')
    elem.plt_opt.cbmax = getattr(options, key + '_max')
    if elem.plt_opt.cbmin is None:
        elem.plt_opt.cbmin = global_min
    if elem.plt_opt.cbmax is None:
        elem.plt_opt.cbmax = global_max

    for ax, time in zip(axes, xrange(0, nr_total)):
        scale = ddps.dd_stats[key]['scale']
        elem.plt_opt.reverse = ddps.dd_stats[key]['reverse']
        # print 'min/max', elem.plt_opt.cbmin, elem.plt_opt.cbmax
        # print 'scale', scale
        cid = elem.add_to_element_data(data[:, time], True)
        elem.plot_element_data_to_ax(cid, ax, scale=scale, no_electrodes=True)

        ax.set_xlabel('')
        ax.set_ylabel('')

    fig.tight_layout()
    fig.savefig(key + '.png', dpi=200)


def plot_to_grid(options):
    elem.load_elem_file(options.elem_file)
    elem.load_elec_file(options.elec_file)

    result_dir_abs = os.path.abspath(options.result_dir)
    os.chdir(options.result_dir)
    # we use the result definitions from ddps
    for key in ddps.dd_stats.keys():
        print('Plotting {0}'.format(key))
        data = np.loadtxt(result_dir_abs + '/stats_and_rms_agg/' +
                          ddps.dd_stats[key]['filename'])

        plot_to_grids(data, key, options)

if __name__ == '__main__':
    options, args = handle_cmd_options()

    if options.aggregate:
        aggregate_results(options)

    if options.plot_to_grid:
        plot_to_grid(options)
