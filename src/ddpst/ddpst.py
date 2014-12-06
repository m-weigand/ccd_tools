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
import NDimInv.elem as elem


def handle_cmd_options():
    parser = OptionParser()
    parser.add_option("-i", "--dir", type='string', metavar='DIR',
                      help="dd_space_time result directory default=results",
                      default="results", dest="result_dir")

    parser.add_option('-a', "--aggregate", action="store_true",
                      dest="aggregate",
                      help="Aggregate plot results (default: False)",
                      default=False)

    parser.add_option("--xmin", type='float', metavar='Depth',
                      help="xmin", default=None, dest="xmin")
    parser.add_option("--xmax", type='float', metavar='Depth',
                      help="xmax", default=None, dest="xmax")
    parser.add_option("--zmin", type='float', metavar='Depth',
                      help="zmin", default=None, dest="zmin")
    parser.add_option("--pixel_mask", type='string', metavar='FILE',
                      help="Pixel mask",
                      default=None, dest="pixel_mask")
    parser.add_option("--mtotn_tau_filter", type='int', metavar='INT',
                      help="Element depth for mtotn filter",
                      default=None, dest="mtotn_filter_depth")
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
        ignore = False
        data_list = []
        for ts in ts_dirs:
            # open data file
            data = np.loadtxt(ts + '/stats_and_rms/' + filename)
            if data.size == 0:
                ignore = True
            data_list.append(data)
        data_all = np.array(data_list)
        # for now, save only 1D or 2D results
        if len(data_all.shape) <= 2 and not ignore:
            np.savetxt(outdir + os.sep + filename, data_all)


def plot_to_grids(data_list, key, options):
    data = data_list[key]
    nr_total = data.shape[1]
    nr_x = min(5, nr_total)
    nr_y = int(np.ceil(nr_total / nr_x))
    fig, axes = plt.subplots(nr_y, nr_x, figsize=(nr_x * 2, nr_y * 2))

    # filter thresholds?
    if options.mtotn_filter_depth is not None:
        # apply thresholds
        for timestep in xrange(0, data.shape[1]):
            data[data_list['mtotn_filter'][timestep], timestep] = np.nan

    data[np.isinf(data)] = np.nan
    data[np.isneginf(data)] = np.nan
    global_min = np.nanmin(data)
    global_max = np.nanmax(data)
    elem.plt_opt.cbmin = getattr(options, key + '_min')
    elem.plt_opt.cbmax = getattr(options, key + '_max')
    if elem.plt_opt.cbmin is None:
        elem.plt_opt.cbmin = global_min
    if elem.plt_opt.cbmax is None:
        elem.plt_opt.cbmax = global_max
    if options.zmin is not None:
        elem.plt_opt.zmin = options.zmin
    if options.xmin is not None:
        elem.plt_opt.xmin = options.xmin
    if options.xmax is not None:
        elem.plt_opt.xmax = options.xmax

    for ax, time in zip(axes.flatten(), xrange(0, nr_total)):
        scale = ddps.dd_stats[key]['scale']
        elem.plt_opt.reverse = ddps.dd_stats[key]['reverse']
        # print 'min/max', elem.plt_opt.cbmin, elem.plt_opt.cbmax
        # print 'scale', scale
        cid = elem.add_to_element_data(data[:, time], True)
        elem.plot_element_data_to_ax(cid, ax, scale=scale, no_electrodes=True)

        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title(ddps.dd_stats[key]['label'])
        ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(3))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(3))

    fig.tight_layout()
    fig.savefig(key + '.png', dpi=200)


def plot_to_grid(options):
    if options.pixel_mask is not None:
        pixel_mask = np.loadtxt(options.pixel_mask, dtype=int)
    else:
        pixel_mask = None

    elem.load_elem_file(options.elem_file)
    elem.load_elec_file(options.elec_file)

    result_dir_abs = os.path.abspath(options.result_dir)
    os.chdir(options.result_dir)

    data_list = {}
    # we use the result definitions from ddps
    for key in reversed(ddps.dd_stats.keys()):
        print('Plotting {0}'.format(key))
        data_file = result_dir_abs + '/stats_and_rms_agg/' + \
            ddps.dd_stats[key]['filename']
        if not os.path.isfile(data_file):
            continue
        data = np.loadtxt(data_file)
        if pixel_mask is not None:
            tmp = np.ones_like(data) * np.nan
            tmp[pixel_mask] = data[pixel_mask]
            data = tmp

        data_list[key] = data

    if options.mtotn_filter_depth is not None:
        # determine depth thresholds
        threshold_elements = options.mtotn_filter_depth
        grid_x = 60
        start_index = grid_x * threshold_elements
        thresholds = data_list['m_tot_n'][start_index:, :].max(axis=0)

        # apply thresholds
        mtotn_filter = []
        for timestep in xrange(0, data.shape[1]):
            indices = np.where(data_list['m_tot_n'][:, timestep] <
                               thresholds[timestep])
            mtotn_filter.append(indices)
        data_list['mtotn_filter'] = mtotn_filter

    for key in reversed(ddps.dd_stats.keys()):
        plot_to_grids(data_list, key, options)

if __name__ == '__main__':
    options, args = handle_cmd_options()

    if options.aggregate:
        aggregate_results(options)

    if options.plot_to_grid:
        plot_to_grid(options)
