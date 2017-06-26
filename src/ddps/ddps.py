#!/usr/bin/env python
# *-* coding: utf-8 *-*
"""
ddpt.py is the post-processing tool for dd_single.py

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

This tool operates on inversion results created by dd_single.py and offers the
following functions:
    -

Planned features:
    - plot (selected) spectra
    - plot (selected) iterations
    - filter spectra based on statistical values
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
import NDimInv
import lib_dd.plot as lDDp
import lib_dd.decomposition.ccd_single_stateless as decomp_single_sl
import lib_dd.io.io_general as iog


# we need to keep track of certain characteristics regarding the output files
# of dd_single.py. These are stored in the dict for later use
# In addition, automatic plot options are produced for the CMD-options from
# this dict.
dd_stats = {}
dd_stats['tau_peak1'] = {'filename': 'tau_peak1_results.dat',
                         'apply_filter': True,
                         'scale': 'linear',
                         'reverse': True,
                         'label': r'$\tau_{peak}^1~[s]$'
                         }
dd_stats['tau_mean'] = {'filename': 'tau_mean_results.dat',
                        'apply_filter': True,
                        'scale': 'linear',
                        'reverse': True,
                        'label': r'$\tau_{mean}~[s]$'
                        }
dd_stats['tau_50'] = {'filename': 'tau_50_results.dat',
                      'apply_filter': True,
                      'scale': 'linear',
                      'reverse': True,
                      'label': r'$\tau_{50}~[s]$'
                      }
dd_stats['rho0'] = {'filename': 'rho0_results.dat',
                    'apply_filter': False,
                    'scale': 'linear',
                    'reverse': False,
                    'label': r'$\rho_0~[\Omega m]$'
                    }
dd_stats['sigma0'] = {
    'filename': 'sigma0_results.dat',
    'apply_filter': False,
    'scale': 'linear',
    'reverse': False,
    'label': r'$\sigma_0~[S/m]$'
}
dd_stats['m_tot_n'] = {'filename': 'm_tot_n_results.dat',
                       'apply_filter': False,
                       'scale': 'linear',
                       'reverse': True,
                       'label': r'$m_{tot}^n~[S/m]$'
                       }
dd_stats['m_tot'] = {'filename': 'm_tot_results.dat',
                     'apply_filter': False,
                     'scale': 'linear',
                     'reverse': True,
                     'label': r'$m_{tot}~[-]$'
                     }
dd_stats['U_tau'] = {'filename': 'U_tau_results.dat',
                     'apply_filter': False,
                     'scale': 'linear',
                     'reverse': True,
                     'label': r'$U_{60/10}$'
                     }

# available filters
filters = {'filter_log10mtot': {'key': 'm_tot',
                                'key_data_is_log10': True,
                                'filter_is_log10': True},
           'filter_log10mtotn': {'key': 'm_tot_n',
                                 'key_data_is_log10': True,
                                 'filter_is_log10': True},
           }


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
    parser.add_option(
        "--maskfile",
        type='str',
        metavar='FILE',
        help="Mask file for filtering: discard all other pixels (start at 0)",
        default=None,
        dest="maskfile",
    )
    parser.add_option("--nr_cpus", type='int', metavar='NR',
                      help="Output directory", default=1,
                      dest="nr_cpus")
    parser.add_option('-o', "--output", type='str', metavar='DIR',
                      help="Output directory (default: filtered_results)",
                      default='filtered_results',
                      dest="output_dir")

    parser.add_option("--output_format", type='string', metavar='TYPE',
                      help="Output format (ascii, ascii_audit)",
                      default='ascii', dest="output_format")
    (options, args) = parser.parse_args()
    return options, args


def _add_dd_grid_plot_opts(parser):
    parser.add_option("--plot_to_grid", action="store_true",
                      dest="plot_to_grid",
                      help="Plot results to grid",
                      default=False)
    parser.add_option("--elem", dest="elem_file", type="string",
                      help="elem.dat file (default: elem.dat)",
                      default="elem.dat")
    parser.add_option("--elec", dest="elec_file", type="string",
                      help="elec.dat file (default: elec.dat)",
                      default="elec.dat")
    # add options for the various DD parameters
    for name in dd_stats.keys():
        opt_name = name + "_min"
        parser.add_option("--" + opt_name, default=None, type="float",
                          dest=opt_name, help="Min value for " + name)
        opt_name = name + "_max"
        parser.add_option("--" + opt_name, default=None, type="float",
                          dest=opt_name, help="Max value for " + name)

    return parser


def load_data(options):
    # load data files
    pwd = os.getcwd()
    os.chdir(options.result_dir + '/stats_and_rms')
    result_files_raw = glob.glob('*.dat')

    result_files_filtered = []
    for filename in result_files_raw:
        if(filename == 'cums_gtau_results.dat'):
            continue
        if(filename == 'm_i_results.dat'):
            continue
        if(filename.startswith('rms_')):
            continue
        result_files_filtered.append(filename)

    data = {}
    for filename in result_files_filtered:
        key = filename[:-12]
        subdata = np.loadtxt(filename)
        data[key] = subdata
    os.chdir(pwd)

    data = filter_data(data, options)
    return data


def filter_data(data, options):
    for key in dd_stats:
        if(dd_stats[key]['apply_filter']):
            data = filter_subdata(data, key, options)
    return data


def filter_subdata(data, key, options):
    """
    Set all values in subdata to np.nan if any filter applies
    """

    # loop through filters
    for filter_key in filters.keys():
        filter_value = getattr(options, filter_key)
        if(filter_value is not None):
            filter_options = filters[filter_key]

            # convert filter to correct representation
            if(filter_options['filter_is_log10'] and
               not filter_options['key_data_is_log10']):
                filter_value = 10 ** filter_value
            # apply this filter
            filter_indices = np.where(
                data[filter_options['key']] <= filter_value)[0]
            data[key][filter_indices] = np.nan

    return data


def plot_to_grid(options):
    """
    Plot statistics to grid
    """
    data = load_data(options)
    pwd = os.getcwd()

    # plot files
    elem.load_elem_file(options.elem_file)
    elem.load_elec_file(options.elec_file)
    outdir = options.result_dir + '/plots_stats_grid'
    if(not os.path.isdir(outdir)):
        os.makedirs(outdir)
    os.chdir(outdir)
    nr_elements = len(elem.element_type_list[0])
    for key in sorted(data.keys()):
        print('Plotting {0}'.format(key))
        # set limits
        if(data[key].size != nr_elements):
            # check if this result dir was previously filtered
            remaining_indices_file = '../remaining_indices.dat'

            if(os.path.isfile(remaining_indices_file)):
                print('Filtered data set')
                remaining_indices = np.loadtxt(
                    remaining_indices_file, dtype=int)
                data_new = np.ones(nr_elements) * np.nan
                data_new[remaining_indices] = data[key]
            else:
                print('Skipping due to wrong array size: {0}'.format(key))
                continue
        else:
            data_new = data[key]

        if(key in dd_stats.keys()):
            elem.plt_opt.cbmin = getattr(options, key + '_min')
            elem.plt_opt.cbmax = getattr(options, key + '_max')
            scale = dd_stats[key]['scale']
            elem.plt_opt.reverse = dd_stats[key]['reverse']
        else:
            # defaults
            elem.plt_opt.cbmin = None
            elem.plt_opt.cbmax = None
            elem.plt_opt.reverse = False
            scale = 'linear'
        print('min/max', elem.plt_opt.cbmin, elem.plt_opt.cbmax)
        print('scale', scale)

        elem.plt_opt.xlabel = 'x'
        elem.plt_opt.ylabel = 'z'
        elem.plt_opt.cb_nr_tiks = 5

        if key in dd_stats:
            elem.plt_opt.title = dd_stats[key]['label']
        else:
            elem.plt_opt.title = ''

        cid = elem.add_to_element_data(data_new)
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        elem.plot_element_data_to_ax(cid, ax, scale=scale)

        fig.savefig(key + '.png', bbox_inches='tight', dpi=300)
        plt.close(fig)
        del(fig)
    os.chdir(pwd)


def _get_ND(subdata):
    nr = subdata['nr']  # the index of this spectrum
    fit_data = subdata['fit_datas'][subdata['nr']]
    # set lambdas
    fit_data['prep_opts']['lambda'] = subdata['lams'][nr]
    # create ND object
    ND = decomp_single_sl._prepare_ND_object(fit_data)

    # recreate the last iteration
    it = NDimInv.main.Iteration(1, ND.Data, ND.Model, ND.RMS, ND.settings)

    # number of iterations
    it.nr = 1
    it.lams = (subdata['lams'][nr], )
    m = np.hstack((subdata['rho0'][nr], subdata['m_i'][nr, :]))
    it.m = m
    it.f = it.Model.obj.convert_parameters(it.Model.f(it.m))
    ND.iterations.append(it)
    ND.set_custom_plot_func(lDDp.plot_iteration())
    return ND


def recreate_ND_obj_list(result_dir, indices=None, nr_cpus=1):
    """
    For a given dd_single.py directory, recreate the ND objects for all spectra
    (final iterations).

    Parameters
    ----------
    result_dir : directory containing the result files/directories of
                 dd_single.py
    indices : None|list, contains indices to load. None loads all spectra
    nr_cpus: use multiple processors to create the inversion objects. nr_cpus =
             1 enables a sequential code path.

    Returns
    -------
    ND_list : list with ND objects
    """
    pwd = os.getcwd()
    os.chdir(result_dir)
    # get settings
    with open('inversion_options.json', 'r') as fid:
        inv_opts = json.load(fid)

    frequencies = np.loadtxt('frequencies.dat')

    data_format = open('data_format.dat').readline().strip()
    prep_opts = {}
    prep_opts['data_format'] = data_format
    # now we need a list with spectra
    pre_data = {}
    data_list = []
    with open('data.dat', 'r') as fid:
        for line in fid.readlines():
            subdata = np.fromstring(line.strip(), sep=' ')
            subdata = subdata.reshape((int(subdata.size / 2), 2), order='F')
            data_list.append(subdata)
    total_nr_spectra = len(data_list)
    pre_data['cr_data'] = data_list
    pre_data['frequencies'] = frequencies

    # create data option list
    data = {}
    data['frequencies'] = frequencies
    data['prep_opts'] = prep_opts
    data['inv_opts'] = inv_opts
    data['cr_data'] = data_list

    data['outdir'] = os.getcwd()

    fit_datas = decomp_single_sl._get_fit_datas(data)

    # # spectrum specific data ##
    lambdas = np.atleast_1d(np.loadtxt('lambdas.dat'))
    # convert to list
    lambdas = [x for x in lambdas]
    rho0 = np.atleast_1d(np.loadtxt('stats_and_rms/rho0_results.dat'))
    m_i = np.atleast_2d(np.loadtxt('stats_and_rms/m_i_results.dat'))
    # #  ##

    ND_list = []
    if(indices is None):
        numbers = range(0, len(fit_datas))
    else:
        numbers = indices

    # prepare a dict with the data
    data = {}
    data['fit_datas'] = fit_datas
    data['lams'] = lambdas
    data['rho0'] = rho0
    data['m_i'] = m_i

    # this is really crappy, but I don't know how to fix it for multiprocessing
    data_list = []

    for nr in numbers:
        new_data = data.copy()
        new_data['nr'] = nr
        data_list.append(new_data)

    # get the required ND objects
    print('Assembling ND objects - this can take a while')
    if(nr_cpus == 1):
        ND_list = [x for x in map(_get_ND, data_list)]
    else:
        p = Pool(nr_cpus)
        ND_list = p.map(_get_ND, data_list)

    os.chdir(pwd)
    return ND_list, total_nr_spectra


def plot_iterations(options):
    """
    Plot various iteration plots
    """

    # we need to get the total nr of spectra
    total_nr_spectra = np.loadtxt(
        options.result_dir + '/nr_iterations.dat').size
    indices = extract_indices_from_range_str(options.spec_ranges,
                                             total_nr_spectra)
    ND_list, _ = recreate_ND_obj_list(options.result_dir, indices)
    pwd = os.getcwd()
    os.chdir(options.result_dir)
    total_nr = len(ND_list)
    for nr, ND in enumerate(ND_list):
        print('Plotting {0} of {1}'.format(nr + 1, total_nr))
        # if(indices is not None and nr not in indices):
        #   continue

        if(options.plot_specs):
            ND.iterations[-1].plot()
        if(options.plot_reg_strength):
            ND.iterations[-1].plot_reg_strengths()
    os.chdir(pwd)


def extract_indices_from_range_str(filter_string, max_index=None):
    """
    Extract indices (e.g. for spectra or pixels) from a range string. The
    string must have the following format: Separate different ranges by ';',
    first index is 1.

    If max_index is provided, open ranges are allowed, as well as "-1" for all.

    Examples:
    "1;2;4;5"
    "2-10"
    "5-"
    "-1"

    Parameters
    ----------
    filter_string : string to be parsed according to the format specifications
                    above
    max_index : (default: None). Provide the maximum index for the ranges to
                allow open ranges and "-1" for all indices
    """
    if(filter_string is None):
        return None

    sections = filter_string.split(';')

    filter_ids = []
    # now look for ranges and expand if necessary
    for section in sections:
        filter_range = section.split('-')
        if(len(filter_range) == 2):
            start = filter_range[0]
            end = filter_range[1]
            # check for an open range, e.g. 4-
            if(end == ''):
                if(max_index is not None):
                    end = max_index
                else:
                    continue
            filter_ids += range(int(start) - 1, int(end))
        else:
            filter_ids.append(int(section) - 1)
    return filter_ids


def filter_result_dir(options):
    """
    Filter the dataset
    """
    # check if we filter using a mask file
    if options.maskfile is not None:
        print('using mask file')
        indices_to_use = np.loadtxt(options.maskfile, dtype=int).tolist()
        # filter_mask = list(np.asarray(filter_mask))
    else:
        indices_to_use = None

    ND_list, total_nr_spectra = recreate_ND_obj_list(
        options.result_dir,
        indices_to_use,
        options.nr_cpus
    )

    # if we use a mask then all indices from here on refer to this smaller set
    # therefore set the list of remaining indices here
    if(indices_to_use is not None):
        remaining_indices = indices_to_use
        deleted_indices = [i for i in range(0, total_nr_spectra) if
                           i not in remaining_indices]
    else:
        remaining_indices = list(range(0, len(ND_list)))
        deleted_indices = []

    # # now we have to apply the various filters
    indices_to_delete = []

    index = 0
    for nr, ND in enumerate(ND_list):
        delete = False
        for filter_key in filters.keys():
            settings = filters[filter_key]
            filter_value = getattr(options, filter_key)
            if(filter_value is None):
                continue

            # convert filter_value if necessary
            if(settings['key_data_is_log10'] and
               not settings['filter_is_log10']):
                filter_value = np.log10(filter_value)

            if(not settings['key_data_is_log10'] and
               settings['filter_is_log10']):
                filter_value = 10 ** (filter_value)

            # the filter process
            it_value = ND.iterations[-1].stat_pars[settings['key']][0]
            if(it_value <= filter_value):
                delete = True
        if delete:
            indices_to_delete.append(index)
        index += 1

    ND_list, remaining_indices, deleted_indices = _delete_indices(
        ND_list,
        indices_to_delete,
        remaining_indices,
        deleted_indices,
    )

    save_filter_results(options, remaining_indices, deleted_indices, ND_list)


def _delete_indices(ND_list, indices_to_delete, remaining_indices,
                    deleted_indices):
    # delete all marked indices
    old_nr_iterations = len(ND_list)
    for i in reversed(sorted(indices_to_delete)):
        del(ND_list[i])
        deleted_indices.append(remaining_indices[i])
        del(remaining_indices[i])

    print('{0} of {1} remaining'.format(
        len(ND_list), old_nr_iterations))

    if(len(ND_list) == 0):
        print('Filter process would remove all spectra! Stopping process.')
        exit()
    return ND_list, remaining_indices, sorted(deleted_indices)


def save_filter_results(options, remaining_indices, deleted_indices, ND_list):
    # # save
    if(not os.path.isdir(options.output_dir)):
        os.makedirs(options.output_dir)
    # copy inversion options files
    shutil.copy(options.result_dir + '/inversion_options.json',
                options.output_dir)
    pwd = os.getcwd()
    os.chdir(options.output_dir)
    # save filter_mask.dat
    np.savetxt('remaining_indices.dat', remaining_indices, fmt='%i')
    np.savetxt('deleted_indices.dat', deleted_indices, fmt='%i')

    # save fit results
    # the data format is kept
    # data_options = {
    # 'raw_format': final_iterations[0][0].Data.obj.data_format
    # }
    #
    prep_opts = {
        'output_format': 'ascii',
    }
    data_options = {
        # 'options': options,
        'options': prep_opts,
        'raw_data': np.atleast_2d(np.array((1))),
        'raw_format': 'None',
        'inv_opts': {},
    }

    iog.save_fit_results(data_options, ND_list)
    os.chdir(pwd)


def _is_log10(filename):
    """Return True if this result file contains log10 data, False otherwise
    """
    # frequencies are usually stored in linear
    if filename.startswith('f_'):
        return False

    files_in_linear_scale = ['decade_loadings_results.dat', ]

    if filename in files_in_linear_scale:
        return False
    return True


def compute_statistics(options):
    """
    Compute various statistics of the stats and store in
    result_dir/statistics.dat
    """
    skip_files = ['decade_bins_results.dat', ]
    stat_files = sorted(glob.glob(options.result_dir + '/stats_and_rms/*.dat'))

    statistics = {}
    for filename in stat_files:
        base_file = os.path.basename(filename)
        key = base_file[:-12]
        # skip rms output files
        if(key.startswith('rms_')):
            continue
        if base_file in skip_files:
            continue

        # load data
        data = np.loadtxt(filename)
        if _is_log10(base_file):
            # integrated parameters are usually stored as log10 values
            data = 10 ** data

        # remove nan-values
        nan_indices = np.where(np.isnan(data))
        data_nonnan = np.delete(data, nan_indices)
        statistics['mean_' + key] = np.mean(data_nonnan)
        statistics['std_' + key] = np.std(np.atleast_1d(data_nonnan))

    # write to json file
    outfile = options.result_dir + '/statistics.json'
    with open(outfile, 'w') as fid:
        json.dump(statistics, fid)

    print('Statistics written to', outfile)


if __name__ == '__main__':
    options, args = handle_cmd_options()
    # call one or more processing steps
    if options.plot_to_grid:
        plot_to_grid(options)

    if options.plot_specs or options.plot_reg_strength:
        plot_iterations(options)

    if options.apply_filters:
        filter_result_dir(options)

    if options.compute_statistics:
        compute_statistics(options)
