#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Invert spatial time-lapse complex resistivity data using the Debye Decoposition
approach.

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

Input files
===========

times : text file, one timestep per line
frequencies : text file, one frequency per line, in ascending order
data_index : index file, one file path per line, corresponding to the times.
data_files : files indexed in *data_index*, holds spatial data for one time
             step, one complex restivity spectrum per line
"""
import os
from optparse import OptionParser
import numpy as np
from multiprocessing import Pool
import dd_single as dd
import NDimInv
import NDimInv.regs as RegFuncs
import NDimInv.reg_pars as LamFuncs
import dd_time
import dd_single
import lib_dd.plot as lDDp


def handle_cmd_options():
    """
    Handle command line options
    """
    parser = OptionParser()
    parser.add_option("-f", "--frequency_file", dest="frequency_file",
                      type='string', metavar="FILE", default='frequencies.dat',
                      help="Frequency file (default: frequency.dat)")
    parser.add_option("--ignore", help="Frequency id's to ignore, example:\
                      '12,13,14'. Starts with index 0.", type='string',
                      default=None, dest="ignore_frequencies")
    parser.add_option("-d", "--data_index", dest="data_index", type='string',
                      help="Data index (default: index.dat)", metavar="FILE",
                      default='index.dat')
    parser.add_option('--data_format', dest='data_format', type='string',
                      help='Input data format, possible values are: ' +
                      'rmag_rpha, lnrmag_rpha, log10rmag_rpha, rmag_rpha, ' +
                      ' rre_rim rre_rmim, cmag_cpha, cre_cim, cre_cmim ' +
                      '(default: rmag_rpha). "r" stands for resistance/' +
                      'resistivity, and "c" stands for conductance/' +
                      'conductivity', default='rmag_rpha')
    parser.add_option("--times", dest="times", type='string',
                      help="Time index (default: times.dat)", metavar="FILE",
                      default='times.dat')

    parser.add_option("-n", "--nr_terms", dest="nr_terms_decade", type='int',
                      help="Number of Debye terms per frequency decade " +
                      "(default: 10)", metavar="INT", default=10)
    parser.add_option("-c", "--nr_cores", dest="nr_cores", type='int',
                      help="Number of CPU cores to use (default: 1)",
                      metavar="INT", default=1)
    parser.add_option("-o", "--output", type='string', metavar='DIR',
                      help="Output directory", default=".", dest="output_dir")
    parser.add_option('-p', "--plot", action="store_true", dest="plot_spectra",
                      help="Plot spectra (default: False)", default=False)
    parser.add_option('-i', "--plot_its", action="store_true",
                      dest="plot_it_spectra", default=False,
                      help="Plot spectra of each iteration (default: False)")
    parser.add_option("--silent", action="store_true", dest="silent",
                      help="Do not plot any logs to STDOUT (default: False)",
                      default=False)
    parser.add_option("--tmp", action="store_true", dest="use_tmp",
                      help="Create the output in a temporary directory and " +
                      "later move it later to its destination (default: " +
                      "False)", default=False)
    parser.add_option("--tausel", type='string', metavar='STRATEGY',
                      help="Tau selection strategy:\ndata (default): Use " +
                      "data frequency limits for tau selection\ndata_ext: " +
                      "Extend tau ranges by one frequency decade compared to" +
                      " the 'data' strategy", default="data",
                      dest="tausel")

    parser.add_option("--lambda", type='float', metavar='FLOAT',
                      help="Use a fixed lambda (integer), default=None",
                      default=None, dest="fixed_lambda")
    parser.add_option('-v', "--version", action="store_true",
                      dest="version", default=False,
                      help="Print version information")

    (options, args) = parser.parse_args()

    if(options.version):
        print(dd_single.VV.version)
        exit()
    return options


def _get_cr_data(options):
    """
    Read in the data index file and the import the complex resistivity spectra
    for all time steps
    """
    # # read index

    # the data_index holds relative file paths
    dirname = os.path.dirname(options.data_index)
    if(dirname == ''):
        dirname = '.'

    with open(options.data_index, 'r') as fid:
        data_index = [dirname + os.sep + x.strip() for x in fid.readlines()]

    # read CR data
    time_rmag = []
    time_rpha = []
    for data_file in data_index:
        print('Reading timestep data: ', data_file)
        step_data = np.loadtxt(data_file)
        center = step_data.shape[1] / 2
        rmag = step_data[:, 0:center]
        rpha = step_data[:, center:]
        time_rmag.append(rmag)
        time_rpha.append(rpha)

    trmag = np.array(time_rmag)
    trpha = np.array(time_rpha)
    pixel_data = np.concatenate((trmag, trpha), axis=2)

    return pixel_data, data_index


def get_data(options):
    """
    Read frequencies and data, and apply frequency filters
    """
    data = {}
    frequencies, f_ignore_ids = dd._get_frequencies(options)
    data['frequencies'] = frequencies
    data['times'] = dd_time._get_times(options)

    cr_data, data_index = _get_cr_data(options)
    data['cr_data'] = cr_data
    data['data_index'] = data_index

    return data


def split_options(options):
    """
    Extract options for two groups:
    1) prep_opts : these options are used to prepare the actual inversion, i.e.
                   which regularization objects to use
    2) inv_opts : these options are directly passed through to the NDimInv
                  object
    """
    prep_opts = {}
    prep_opts['f_lambda'] = options.fixed_lambda
    prep_opts['nr_cores'] = options.nr_cores
    prep_opts['plot_it_spectra'] = options.plot_it_spectra
    prep_opts['plot'] = options.plot_spectra
    prep_opts['output_dir'] = options.output_dir

    inv_opts = {}
    inv_opts['tausel'] = options.tausel
    inv_opts['Nd'] = options.nr_terms_decade
    return prep_opts, inv_opts


def save_fit_results(final_iterations, data):
    dd_single.save_base_results(final_iterations)

    # get keys of statistical parameters
    keys = final_iterations[0][0].stat_pars.keys()
    nr_times = len(final_iterations[0][0].stat_pars[keys[0]])

    # # get keys for times
    for time in range(0, nr_times):
        outdir = 'time_{0}'.format(time)
        os.makedirs(outdir)
        os.chdir(outdir)
        # # statistics
        stats = {}
        for key in keys:
            for pixel in final_iterations:
                tmp_stats = pixel[0].stat_pars[key][time]
                if(key not in stats):
                    stats[key] = []
                stats[key] += [tmp_stats, ]
        # save data
        for key in keys:
            values = np.array(stats[key])
            filename = '{0}_results.dat'.format(key)
            np.savetxt(filename, np.atleast_1d(values))

        os.chdir('..')

    # we fit over time, as such RMS values are for each pixel
    # # rms values
    keys = final_iterations[0][0].rms_values().keys()
    rms_stats = {}
    for nr, pixel in enumerate(final_iterations):
        for key in keys:
            rms_value = pixel[0].rms_values()[key]
            if(key not in rms_stats):
                rms_stats[key] = []
            rms_stats[key] += [rms_value, ]
    for key in rms_stats.keys():
        filename = key + '.dat'
        np.savetxt(filename, rms_stats[key])

    # we need to rebuild the data from the iterations (just to make sure that
    # the data we fitted actually is the data we put in - otherwise we could
    # just copy the input files)
    data_list = []
    for it in final_iterations:
        D = it[0].Data.D
        D = np.swapaxes(D, 0, 2)
        D = D.reshape((D.shape[0], np.prod(D.shape[1:3])))
        data_list.append(D)
    D_all = np.array(data_list)
    # swap location and time axes
    D_all = np.swapaxes(D_all, 0, 1)

    with open('data_index.dat', 'w') as fid_index:
        for nr, time_data in enumerate(D_all):
            filename = 'data_t{0}.dat'.format(nr)
            fid_index.write(filename + '\n')
            np.savetxt(filename, time_data)

    # save times
    with open('times.dat', 'w') as fid:
        for item in data['times']:
            fid.write(item + '\n')


def fit_data(data, prep_opts, inv_opts):
    """
    Call the fit routine for each pixel
    """
    # add frequencies to inv_opts
    inv_opts['frequencies'] = data['frequencies']
    inv_opts['max_iterations'] = 20

    # prepare the parameter list for each pixel fit
    fit_datas = []
    for i in range(0, data['cr_data'].shape[1]):
        # change file prefix for each spectrum
        # at the moment we need a copy for this
        inv_opts_i = inv_opts.copy()
        inv_opts_i['global_prefix'] = 'pixel_{0:03}_'.format(i)
        fit_data = {'data': data['cr_data'][:, i, :].squeeze(),
                    'frequencies': data['frequencies'],
                    'prep_opts': prep_opts,
                    'inv_opts': inv_opts_i
                    }
        fit_datas.append(fit_data)

    if(prep_opts['nr_cores'] == 1):
        print('single processing')
        # single processing
        results = map(fit_one_pixel, fit_datas)
    else:
        # multi processing
        print('multi processing')
        p = Pool(prep_opts['nr_cores'])
        results = p.map(fit_one_pixel, fit_datas)

    final_iterations = [(x.iterations[-1], nr) for nr, x in
                        enumerate(results)]
    save_fit_results(final_iterations, data)


def fit_one_pixel(fit_data):
    # init the object
    ND = NDimInv.Inversion('dd_log10rho0log10m', fit_data['inv_opts'])

    # add extra dimensions
    nr_timesteps = fit_data['data'].shape[0]
    ND.add_new_dimension('time', nr_timesteps)
    ND.finalize_dimensions()

    # register data
    for index, subdata in enumerate(fit_data['data']):
        print('Importing time step {0}'.format(index))
        print subdata.shape
        subdata = subdata.reshape((2, subdata.size / 2)).T
        ND.Data.add_data(subdata, 'rmag_rpha', extra=(index, ))

    ND.update_model()
    ND.set_custom_plot_func(lDDp.plot_iteration())
    # ND.Model.steplength_selector = NDimInv.main.SearchSteplength()
    ND.Model.steplength_selector = NDimInv.main.SearchSteplengthParFit()

    # add a frequency regularization for the DD model
    if(prep_opts['f_lambda'] is None):
        lam_obj = LamFuncs.SearchLambda(LamFuncs.Lam0_Easylam())
    else:
        lam_obj = LamFuncs.FixedLambda(prep_opts['f_lambda'])

    reg_object = RegFuncs.SmoothingFirstOrder(decouple=[0, ])
    ND.Model.add_regularization(0, reg_object, lam_obj)

    # # add time regularization
    # rho0 regularization
    reg_obj = RegFuncs.SmoothingSecondOrder(decouple=[],
                                            outside_first_dim=[0, ],
                                            weighting_data=None)
    ND.Model.add_regularization(1,
                                reg_obj,
                                LamFuncs.FixedLambda(1e6)
                                )
    # m regularization
    reg_obj = RegFuncs.SmoothingSecondOrder(decouple=[],
                                            outside_first_dim=range(1, 50),
                                            weighting_data=None)
    ND.Model.add_regularization(1, reg_obj,
                                LamFuncs.FixedLambda(1e2)
                                )

    ND.run_inversion()

    print fit_data['prep_opts']
    if(fit_data['prep_opts']['plot']):
        print('Plotting final iteration')
        ND.iterations[-1].plot()

    if(fit_data['prep_opts']['plot_it_spectra']):
        for it in ND.iterations:
            it.plot()
    return ND


if __name__ == '__main__':
    options = handle_cmd_options()
    outdir = dd.get_output_dir(options)
    prep_opts, inv_opts = split_options(options)
    data = get_data(options)
    # for the fitting process, change to the output_directory
    pwd = os.getcwd()
    os.chdir(outdir)
    fit_data(data, prep_opts, inv_opts)
    # go back to initial working directory
    os.chdir(pwd)
