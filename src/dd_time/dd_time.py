#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Invert time-lapse SIP data using the Debye Decoposition approach.

Copyright 2014 Maximilian Weigand

Input files
"""
# from memory_profiler import *
import os
import pkg_resources
# import json
import logging
logging.basicConfig(level=logging.INFO)
from optparse import OptionParser
import dd_single as dd
import numpy as np
import NDimInv
import NDimInv.regs as RegFuncs
import NDimInv.reg_pars as LamFuncs
import sip_formats.convert as SC
import sip_formats.convert as sip_converter
import lib_dd.interface as lDDi
import lib_dd.plot as lDDp
import lib_dd.main


def handle_cmd_options():
    """
    Handle command line options
    """
    parser = OptionParser()
    parser = dd.add_base_options(parser)
    parser.add_option("--times", dest="times", type='string',
                      help="Time index (default: times.dat)", metavar="FILE",
                      default='times.dat')
    parser.add_option("-c", "--nr_cores", dest="nr_cores", type='int',
                      help="Number of CPU cores to use (default: 1)",
                      metavar="INT", default=1)
    parser.add_option("--f_lambda", type='float', metavar='FLOAT',
                      help="Use a fixed lambda (float) for the " +
                      "tau-regularization, default=None",
                      default=None, dest="freq_lambda")
    parser.add_option("--trho0_lambda", type='float', metavar='FLOAT',
                      help="Fixed time regularization lambda for rho0, " +
                      "default=0", default=0, dest="time_rho0_lambda")
    parser.add_option("--tm_i_lambda", type='float', metavar='FLOAT',
                      help="Fixed time regularization lambda for the " +
                      "chargeabilities m_i, default=0",
                      default=0, dest="time_m_i_lambda")
    parser.add_option("--ind_lams", action="store_true",
                      dest="individual_lambdas", default=False,
                      help="Use individual lambdas for f-regularization")
    parser.add_option("--lam0", type='float', metavar='FLOAT',
                      help="Initial lambda for f-regularization (default: " +
                      "None - use Easylam", default=None,
                      dest="f_lam0")
    parser.add_option("--trho0_first_order", action="store_true",
                      dest="trho0_first_order", default=False,
                      help="Use first order smoothing for rho_0 " +
                      "(instead of second order smoothing)")
    parser.add_option("--tw_rho0", action="store_true",
                      dest="time_weighting_rho0", default=False,
                      help="Use time-weighting (only in combination with " +
                      "--trho0_first_order)")
    parser.add_option("--tmi_first_order", action="store_true",
                      dest="tmi_first_order", default=False,
                      help="Use first order smoothing for m_i " +
                      "(instead of second order smoothing)")
    parser.add_option("--tw_mi", action="store_true",
                      dest="time_weighting_mi", default=False,
                      help="Use time-weighting (only in combination with " +
                      "--tmi_first_order)")
    (options, args) = parser.parse_args()

    # print version information if requested
    if(options.version):
        print('geccoinv version: ' +
              pkg_resources.require('geccoinv')[0].version)

        print('dd_interface version: ' +
              pkg_resources.require('dd_interface')[0].version)
        exit()

    return options


def _get_times(options):
    """
    Read in times
    """
    times = np.loadtxt(options.times)
    return times


def _get_cr_data(options, data):
    """
    Load complex resistivity data.
    """
    cr_data = np.loadtxt(options.data_file)
    if(options.norm_mag is not None):
        print 'normalizing'
        # data must me in format 'rmag_rpha'
        if(options.data_format != "rmag_rpha"):
            print 'formatting'
            cr_data = SC.convert(options.data_format, 'rmag_rpha', cr_data)
            options.data_format = 'rmag_rpha'

        # apply normalization
        index_end = cr_data.shape[1] / 2
        norm_factors = options.norm_mag / cr_data[:, 0]
        norm_factors = np.resize(norm_factors.T,
                                 (index_end, norm_factors.size)).T
        cr_data[:, 0:index_end] *= norm_factors
        data['norm_factors'] = norm_factors[:, 0].squeeze()

    return cr_data, options, data


def get_data_dd_time(options):
    """
    Read frequencies and data, and apply frequency filters

    options is also returned in case we change some settings, e.g. the data
    """
    data, options = lDDi.load_frequencies_and_data(options)
    data['times'] = _get_times(options)
    data['cr_data'] = data['raw_data']

    return data, options


def split_options(options):
    """
    Extract options for two groups:
    1) prep_opts : these options are used to prepare the actual inversion, i.e.
                   which regularization objects to use
    2) inv_opts : these options are directly passed through to the NDimInv
                  object
    """
    prep_opts, inv_opts = dd.split_options_base(options)

    # prep_opts = {}
    prep_opts['nr_cores'] = options.nr_cores
    # prep_opts['plot_it_spectra'] = options.plot_it_spectra
    # prep_opts['plot'] = options.plot_spectra
    # prep_opts['output_dir'] = options.output_dir
    prep_opts['f_lambda'] = options.freq_lambda
    prep_opts['t_rho0_lambda'] = options.time_rho0_lambda
    prep_opts['t_m_i_lambda'] = options.time_m_i_lambda
    # prep_opts['data_format'] = options.data_format
    prep_opts['individual_lambdas'] = options.individual_lambdas
    prep_opts['f_lam0'] = options.f_lam0
    # prep_opts['max_iterations'] = options.max_iterations
    prep_opts['trho0_first_order'] = options.trho0_first_order
    prep_opts['tmi_first_order'] = options.tmi_first_order
    prep_opts['time_weighting_rho0'] = options.time_weighting_rho0
    prep_opts['time_weighting_mi'] = options.time_weighting_mi
    # prep_opts['plot_lambda'] = options.plot_lambda

    # inv_opts = {}
    # inv_opts['tausel'] = options.tausel
    # inv_opts['Nd'] = options.nr_terms_decade
    return prep_opts, inv_opts


# @profile
def fit_sip_data(data, prep_opts, inv_opts):
    """
    Call the fit routine for each pixel
    """
    # add frequencies to inv_opts
    inv_opts['frequencies'] = data['frequencies']
    inv_opts['global_prefix'] = 'times_'
    if('norm_factors' in data):
        inv_opts['norm_factors'] = data['norm_factors']
    else:
        inv_opts['norm_factors'] = None

    fit_data = {'data': data['cr_data'],
                'times': data['times'],
                'frequencies': data['frequencies'],
                'prep_opts': prep_opts,
                'inv_opts': inv_opts
                }

    # save inversion options
    # with open('inversion_options.json', 'w') as fid:
    # json.dump(inv_opts, fid)

    # fit the time-lapse data
    ND = fit_one_time_series(fit_data)

    final_iteration = ND.iterations[-1]

    # renormalize data
    if('norm_factors' in data):
        parsize = final_iteration.Model.M_base_dims[0][1]
        spectrum_nr = 0
        for index, norm_fac in zip(range(0, final_iteration.m.size, parsize),
                                   data['norm_factors']):
            # add normalization factor to the parameters
            final_iteration.m[index] -= np.log10(norm_fac)
            final_iteration.f = final_iteration.Model.f(final_iteration.m)
            # data
            # note: the normalization factor can be applied either to the
            # magnitude, or to both real and imaginary parts!
            final_iteration.Data.D[:, :, spectrum_nr] /= norm_fac
            spectrum_nr += 1

    if(fit_data['prep_opts']['plot']):
        print('Plotting final iteration')
        final_iteration.plot()
        final_iteration.plot_reg_strengths()

    if(fit_data['prep_opts']['plot_it_spectra']):
        for it in ND.iterations:
            it.plot()

    if(fit_data['prep_opts']['plot_lambda'] is not None):
        ND.iterations[fit_data['prep_opts']['plot_lambda']].plot_lcurve()

    save_fit_results(final_iteration, data)


def save_fit_results(final_iteration, data):
    # note: we don't want to provide the data parameter, but until we really
    # incorporate times into the inversion..just save it
    final_iterations = ((final_iteration, ), )
    dd.save_base_results(final_iterations, data)
    if not os.path.isdir('stats_and_rms'):
        os.makedirs('stats_and_rms')
    os.chdir('stats_and_rms')
    if('norm_factors' in data):
        norm_factors = data['norm_factors']
    else:
        norm_factors = None

    lDDi.save_stat_pars(final_iteration.stat_pars, norm_factors)
    lDDi.save_rms_values(final_iteration.rms_values,
                         final_iteration.RMS.rms_names)

    os.chdir('..')

    # save data
    # we know that the Data array is only 2D
    with open('data.dat', 'w') as fid:
        D = final_iteration.Data.D
        # times to the front
        D = np.swapaxes(D, 0, 2)
        # reshape
        D = D.reshape((D.shape[0], np.prod(D.shape[1:])))
        np.savetxt(fid, D)

    # save model response
    Dsize = np.prod(final_iteration.Data.D_base_size)
    f = final_iteration.Model.f(final_iteration.m)
    f_reshaped = np.reshape(f, (Dsize, f.size / Dsize), order='F').T
    np.savetxt('f.dat', f_reshaped)

    # save times
    with open('times.dat', 'w') as fid:
        for item in data['times']:
            fid.write('{0}'.format(item) + '\n')


def fit_one_time_series(fit_data):
    # init the object
    model = lib_dd.main.get('log10rho0log10m', fit_data['inv_opts'])
    ND = NDimInv.NDimInv(model, fit_data['inv_opts'])

    # add extra dimensions
    nr_timesteps = fit_data['data'].shape[0]
    ND.add_new_dimension('time', nr_timesteps)
    ND.finalize_dimensions()
    ND.Data.data_converter = sip_converter.convert

    # register data
    for index, subdata in enumerate(fit_data['data']):
        print('Importing time step {0}'.format(index))
        subdata = subdata.reshape((2, subdata.size / 2)).T
        ND.Data.add_data(subdata, fit_data['prep_opts']['data_format'],
                         extra=(index, ))

    ND.update_model()

    # add rms types
    ND.RMS.add_rms('rms_re_im',
                   [True, False],
                   ['rms_real_parts', 'rms_imag_parts'])

    ND.RMS.add_rms('rms_times',
                   [True, True, False],
                   ['rms_time_', ])

    # use imaginary part for stopping criteria
    ND.stop_rms_key = 'rms_re_im_noerr'
    ND.stop_rms_index = 1

    ND.set_custom_plot_func(lDDp.plot_iteration())
    # ND.Model.steplength_selector = NDimInv.main.SearchSteplength()
    ND.Model.steplength_selector = NDimInv.main.SearchSteplengthParFit(
        optimize='rms_re_im_noerr', optimize_index=1)

    # get number of tau values
    nr_tau_values = ND.Model.obj.tau.size

    # add a frequency regularization for the DD model
    if fit_data['prep_opts']['f_lambda'] is None:
        print('Frequency lambda search')
        if fit_data['prep_opts']['f_lam0'] is None:
            lam0_obj = LamFuncs.Lam0_Easylam()
        else:
            lam0_obj = LamFuncs.Lam0_Fixed(prep_opts['f_lam0'])

        if(fit_data['prep_opts']['individual_lambdas']):
            lam_obj = LamFuncs.SearchLambdaIndividual(lam0_obj)
        else:
            lam_obj = LamFuncs.SearchLambda(lam0_obj)
        # rms value to optimize
        optimize_rms_key = 'rms_re_im_noerr'
        optimize_rms_index = 1  # imaginary part
        lam_obj.rms_key = optimize_rms_key
        lam_obj.rms_index = optimize_rms_index
    else:
        lam_obj = LamFuncs.FixedLambda(fit_data['prep_opts']['f_lambda'])

    reg_object = RegFuncs.SmoothingFirstOrder(decouple=[0, ])
    ND.Model.add_regularization(0, reg_object, lam_obj)

    # # add time regularization
    # rho0 regularization
    if(fit_data['prep_opts']['time_weighting_rho0'] or
       fit_data['prep_opts']['time_weighting_mi']):
        weighting_obj = RegFuncs.DifferenceWeighting(fit_data['times'])
    else:
        weighting_obj = None

    if(fit_data['prep_opts']['trho0_first_order']):
        reg_obj = RegFuncs.SmoothingFirstOrder(decouple=[],
                                               outside_first_dim=[0, ],
                                               weighting_obj=weighting_obj)
    else:
        reg_obj = RegFuncs.SmoothingSecondOrder(decouple=[],
                                                outside_first_dim=[0, ],
                                                weighting_obj=None)
    ND.Model.add_regularization(1,
                                reg_obj,
                                LamFuncs.FixedLambda(
                                    fit_data['prep_opts']['t_rho0_lambda'])
                                )
    # m regularization
    if(fit_data['prep_opts']['tmi_first_order']):
        reg_obj = RegFuncs.SmoothingFirstOrder(decouple=[],
                                               outside_first_dim=range(
                                                   1, nr_tau_values),
                                               weighting_obj=weighting_obj)
    else:
        reg_obj = RegFuncs.SmoothingSecondOrder(decouple=[],
                                                outside_first_dim=range(
                                                    1, nr_tau_values))
    ND.Model.add_regularization(1, reg_obj,
                                LamFuncs.FixedLambda(
                                    fit_data['prep_opts']['t_m_i_lambda'])
                                )

    # debug start
    """
    ND.start_inversion()
    m = ND.iterations[-1].m
    M = ND.Model.convert_to_M(m)
    f1 = ND.Model.F(M)
    f2 = ND.Model.F_ng(M)
    print f1 - f2
    exit()

    D = ND.Data.D

    f = ND.Model.f(m)
    print 'f', f.shape
    print 'M', M.shape
    print 'D', D.shape
    m1 = M[:, 0]
    f1 = ND.Model.obj.forward(m1)
    print 'f1', f1.shape

    print ND.Model.F(M)

    exit()
    # # debug end
    """

    ND.run_inversion()
    return ND


if __name__ == '__main__':
    options = handle_cmd_options()
    dd.check_input_files(options, ['times', ])
    outdir = dd.get_output_dir(options)
    data, options = get_data_dd_time(options)
    prep_opts, inv_opts = split_options(options)

    # for the fitting process, change to the output_directory
    pwd = os.getcwd()
    os.chdir(outdir)
    fit_sip_data(data, prep_opts, inv_opts)
    # go back to initial working directory
    os.chdir(pwd)
