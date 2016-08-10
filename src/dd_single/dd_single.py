#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-wildcard-import,wildcard-import
"""
Cole-Cole decomposition interface for spectral induced polarization data. One
or more spectra can be fitted using a Debye decomposition approach.

Copyright 2014,2015,2016 Maximilian Weigand

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
import logging
logging.basicConfig(level=logging.INFO)
import os
import numpy as np
from multiprocessing import Pool
import shutil

import NDimInv
import NDimInv.regs as RegFuncs
import NDimInv.reg_pars as LamFuncs
from NDimInv.plot_helper import *
import lib_dd.interface as lDDi
import gc
import lib_dd.plot as lDDp
import sip_formats.convert as sip_converter
import lib_dd.conductivity.model as cond_model
import lib_dd.io.ascii as ioascii
import lib_dd.io.ascii_audit as ioascii_audit
from lib_dd.models import ccd_res

import lib_dd.config.cfg_single as cfg_single


def _prepare_ND_object(fit_data):
    # use conductivity or resistivity model?
    if 'DD_COND' in os.environ and os.environ['DD_COND'] == '1':
        # there is only one parameterisation: log10(sigma_i), log10(m)
        model = cond_model.dd_conductivity(fit_data['inv_opts'])
    else:
        # there are multiple parameterisations available, use the log10 one
        # model = lib_dd.main.get('log10rho0log10m', fit_data['inv_opts'])
        if 'DD_C' in os.environ:
            fit_data['inv_opts']['c'] = float(os.environ['DD_C'])
        else:
            fit_data['inv_opts']['c'] = 1.0
        # model = lib_cc2.decomposition_resistivity(fit_data['inv_opts'])
        model = ccd_res.decomposition_resistivity(fit_data['inv_opts'])
    ND = NDimInv.NDimInv(model, fit_data['inv_opts'])
    ND.finalize_dimensions()
    ND.Data.data_converter = sip_converter.convert

    # read in data
    # print fit_data['data'], fit_data['prep_opts']['data_format']
    ND.Data.add_data(fit_data['data'], fit_data['prep_opts']['data_format'],
                     extra=[])

    # now that we know the frequencies we can call the post_frequency handler
    # for the model side
    ND.update_model()

    # add rms types
    ND.RMS.add_rms('rms_re_im',
                   [True, False],
                   ['rms_real_parts', 'rms_imag_parts'])

    # use imaginary part for stopping criteria
    ND.stop_rms_key = 'rms_re_im_noerr'
    ND.stop_rms_index = 1

    ND.set_custom_plot_func(lDDp.plot_iteration())

    # rms value to optimize
    optimize_rms_key = 'rms_re_im_noerr'
    optimize_rms_index = 1  # imaginary part

    # add a frequency regularization for the DD model
    if(fit_data['prep_opts']['lambda'] is None):
        lam_obj = LamFuncs.SearchLambda(LamFuncs.Lam0_Easylam())
        lam_obj.rms_key = optimize_rms_key
        lam_obj.rms_index = optimize_rms_index
    else:
        lam_obj = LamFuncs.FixedLambda(fit_data['prep_opts']['lambda'])

    ND.Model.add_regularization(0,
                                RegFuncs.SmoothingFirstOrder(
                                    decouple=[0, ]),
                                lam_obj
                                )

    # choose from a fixed set of step lengths
    ND.Model.steplength_selector = NDimInv.main.SearchSteplengthParFit(
        optimize_rms_key, optimize_rms_index)
    return ND


# @profile
def fit_one_spectrum(fit_data):
    """
    Fit one spectrum
    """
    print('Fitting spectrum {0} of {1}'.format(fit_data['nr'],
                                               fit_data['nr_of_spectra']))
    ND = _prepare_ND_object(fit_data)

    # run the inversion
    ND.run_inversion()

    # extract the (only) iteration
    final_iteration = ND.iterations[-1]

    # renormalize data (we deal only with one spectrum here)
    if(False and fit_data['inv_opts']['norm_factors'] is not None):
        norm_fac = fit_data['inv_opts']['norm_factors']

        # add normalization factor to the parameters
        final_iteration.m[0] -= np.log10(norm_fac)
        final_iteration.f = final_iteration.Model.f(final_iteration.m)
        # data
        # note: the normalization factor can be applied either to the
        # magnitude, or to both real and imaginary parts!
        final_iteration.Data.D /= norm_fac

    call_fit_functions(fit_data, ND)

    # invoke the garbage collection just to be sure
    gc.collect()
    return ND


def call_fit_functions(fit_data, ND):
    if(fit_data['prep_opts']['plot']):
        print('Plotting final iteration')
        ND.iterations[-1].plot(
            norm_factors=fit_data['inv_opts']['norm_factors'])
        ND.iterations[-1].Model.obj.plot_stats('{0}'.format(fit_data['nr']))

    if(fit_data['prep_opts']['plot_reg_strength']):
        ND.iterations[-1].plot_reg_strengths()

    if(fit_data['prep_opts']['plot_it_spectra']):
        for it in ND.iterations:
            it.plot()

    if(fit_data['prep_opts']['plot_lambda'] is not None):
        ND.iterations[fit_data['prep_opts']['plot_lambda']].plot_lcurve()


def _filter_nan_values(frequencies, cr_spectrum):
    """
        Filter nan values along the frequency axis (we always ne part1 and
        part2).

        Return filtered frequencies, cr_spectrum
    """

    # check for NaN values
    nan_indices = np.isnan(cr_spectrum)
    nan_along_freq = np.any(nan_indices, axis=1)
    to_delete = np.where(nan_along_freq)
    frequencies_cropped = np.delete(frequencies, to_delete)
    cr_spectrum_cropped = np.delete(cr_spectrum, to_delete, axis=0)
    return frequencies_cropped, cr_spectrum_cropped


def _get_fit_datas(data):
    """
    Prepare data for fitting. Prepare a set of variables/objects for each
    spectrum. Also filter nan values

    Parameters
    ----------
    data : dict containing the keys 'frequencies', 'cr_data'
    """
    fit_datas = []

    nr_of_spectra = len(data['cr_data'])
    for i in range(0, nr_of_spectra):
        fit_data = {}
        # change file prefix for each spectrum
        # at the moment we need a copy for this
        frequencies_cropped, cr_data = _filter_nan_values(
            data['frequencies'], data['cr_data'][i])

        fit_data['prep_opts'] = data['prep_opts']
        fit_data['data'] = cr_data
        fit_data['nr'] = i + 1
        fit_data['nr_of_spectra'] = nr_of_spectra
        fit_data['frequencies'] = frequencies_cropped

        # inversion options are changed for each spectrum, so we have to copy
        # it each time
        inv_opts_i = data['inv_opts'].copy()
        inv_opts_i['frequencies'] = frequencies_cropped
        inv_opts_i['global_prefix'] = 'spec_{0:03}_'.format(i)
        if('norm_factors' in data):
            inv_opts_i['norm_factors'] = data['norm_factors'][i]
        else:
            inv_opts_i['norm_factors'] = None

        fit_data['inv_opts'] = inv_opts_i

        fit_datas.append(fit_data)

    return fit_datas


def fit_data(data):
    """This is the central fit function, which prepares the data, fits each
    spectrum, plots (if requested), and then saves the results.
    """
    fit_datas = _get_fit_datas(data)

    # fit
    if(data['prep_opts']['nr_cores'] == 1):
        print('single processing')
        # single processing
        results = list(map(fit_one_spectrum, fit_datas))
    else:
        # multi processing
        print('multi processing')
        p = Pool(data['prep_opts']['nr_cores'])
        results = p.map(fit_one_spectrum, fit_datas)

    # results now contains one or more ND objects
    save_fit_results(data, results)


def _make_list(obj):
    """make sure the provided object is a list, if not, enclose it in one
    """
    if not isinstance(obj, list):
        return [obj, ]
    else:
        return obj


def save_fit_results(data, NDobj):
    """
    Save results of all DD fits to files

    Parameters
    ----------
    data:
    NDobj: one or more ND objects. This is either a ND object, or list of ND
           objects
    """
    NDlist = _make_list(NDobj)
    output_format = data['options']['output_format']
    if output_format == 'ascii':
        ioascii.save_data(data, NDlist)
    elif output_format == 'ascii_audit':
        ioascii_audit.save_results(data, NDlist)
    else:
        raise Exception('Output format "{0}" not recognized!'.format(
            output_format))


def get_data_dd_single(options):
    """
    Load frequencies and data and return a data dict

    Parameters
    ----------

    options: cmd options


    Returns
    -------
    data: dict with entries "raw_data", "cr_data", "options", "inv_opts",
          "prep_opts"
    """
    data, options = lDDi.load_frequencies_and_data(options)

    # we need list of spectra
    size_y = data['raw_data'].shape[1] / 2
    cr_data = [x.reshape((size_y, 2), order='F') for x in data['raw_data']]

    data['cr_data'] = cr_data

    # we distinguish two sets of options:
    # prep_opts : all settings we need to prepare the inversion (i.e. set
    #             regularization objects)
    # inv_opts : options that are directly looped through to the NDimInv object
    prep_opts, inv_opts = options.split_options()

    data['options'] = options
    data['prep_opts'] = prep_opts
    data['inv_opts'] = inv_opts
    return data


# @profile
def main():
    print('Cole-Cole decomposition, no time regularization')

    options = cfg_single.cfg_single()
    options.parse_cmd_arguments()

    options.check_input_files()
    outdir = lDDi.create_output_dir(options)

    # DD_RES_INV.inversion.setup_logger('dd', outdir, options.silent)
    # logger = logging.getLogger('dd.debye decomposition')

    # logger.info('----------------------------------')
    # logger.info('       Debye Decomposition')
    # logger.info('----------------------------------')
    # logger.info('Frequency file: {0}'.format(options.frequency_file))
    # logger.info('Data file: {0}'.format(options.data_file))
    # frequencies, data_list = get_frequencies_and_data(options)
    data = get_data_dd_single(options)

    # for the fitting process, change to the output_directory
    pwd = os.getcwd()
    os.chdir(outdir)

    # fit the data
    fit_data(data)

    # logger.info('=======================================')
    # logger.info('     Debye Decomposition finished!     ')
    # logger.info('=======================================')

    # go back to initial working directory
    os.chdir(pwd)

    # move temp directory to output directory
    if options['use_tmp']:
        if os.path.isdir(options['output_dir']):
            print('WARNING: Output directory already exists')
            print('The new inversion can be found here:')
            print((options['output_dir'] + os.sep + os.path.basename(outdir)))
        shutil.move(outdir, options['output_dir'])


if __name__ == '__main__':
    main()
