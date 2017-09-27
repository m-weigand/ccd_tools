#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Invert time-lapse SIP data using the Cole-Cole decomposition approach.

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
import os
import logging
logging.basicConfig(level=logging.INFO)
import numpy as np
import NDimInv
import NDimInv.regs as RegFuncs
import NDimInv.reg_pars as LamFuncs
import sip_formats.convert as SC
import lib_dd.interface as lDDi
import lib_dd.plot as lDDp
import lib_dd.conductivity.model as cond_model
from lib_dd.models import ccd_res
import lib_dd.config.cfg_time as cfg_time
import lib_dd.io.io_general as iog


def _get_times(options):
    """
    Read in times
    """
    times = np.loadtxt(options['times'])
    return times


def _get_cr_data(options, data):
    """
    Load complex resistivity data.
    """
    cr_data = np.loadtxt(options.data_file)
    if options.norm_mag is not None:
        # data must me in format 'rmag_rpha'
        if options.data_format != "rmag_rpha":
            cr_data = SC.convert(options.data_format, 'rmag_rpha', cr_data)
            options.data_format = 'rmag_rpha'

        # apply normalization
        index_end = cr_data.shape[1] / 2
        norm_factors = options.norm_mag / cr_data[:, 0]
        norm_factors = np.resize(
            norm_factors.T,
            (index_end, norm_factors.size)
        ).T
        cr_data[:, 0:index_end] *= norm_factors
        data['norm_factors'] = norm_factors[:, 0].squeeze()

    return cr_data, options, data


def get_data_dd_time(options):
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
    data['times'] = _get_times(options)
    data['cr_data'] = data['raw_data']

    prep_opts, inv_opts = options.split_options()
    data['options'] = options
    data['prep_opts'] = prep_opts
    data['inv_opts'] = inv_opts
    return data


def _get_fit_datas(data):

    # add frequencies to inv_opts
    data['inv_opts']['frequencies'] = data['frequencies'].copy()
    data['inv_opts']['global_prefix'] = 'times_'
    if('norm_factors' in data):
        data['inv_opts']['norm_factors'] = data['norm_factors']
    else:
        data['inv_opts']['norm_factors'] = None

    fit_data = {
        'data': data['cr_data'],
        'times': data['times'],
        'frequencies': data['frequencies'],
        'prep_opts': data['prep_opts'],
        'inv_opts': data['inv_opts']
    }

    return fit_data


# @profile
def fit_data(data):
    """
    Call the fit routine for each pixel
    """
    data_struct = _get_fit_datas(data)

    # fit the time-lapse data
    ND = fit_one_time_series(data_struct)

    # results now contains one or more ND objects
    iog.save_fit_results(data, ND)


def _prepare_ND_object(data):
    # use conductivity or resistivity model?
    if 'DD_COND' in os.environ and os.environ['DD_COND'] == '1':
        # there is only one parameterisation: log10(sigma_i), log10(m)
        model = cond_model.dd_conductivity(data['inv_opts'])
    else:
        # there are multiple parameterisations available, use the log10 one
        if 'DD_C' in os.environ:
            data['inv_opts']['c'] = float(os.environ['DD_C'])
        else:
            data['inv_opts']['c'] = 1.0
        model = ccd_res.decomposition_resistivity(data['inv_opts'])
    ND = NDimInv.NDimInv(model, data['inv_opts'])

    # add extra dimensions
    nr_timesteps = data['data'].shape[0]
    ND.add_new_dimension('time', nr_timesteps)
    ND.finalize_dimensions()
    ND.Data.data_converter = SC.convert

    # register data
    for index, subdata in enumerate(data['data']):
        print('Importing time step {0}'.format(index))
        subdata = subdata.reshape((2, int(subdata.size / 2))).T
        ND.Data.add_data(
            subdata, data['prep_opts']['data_format'],
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
    if data['prep_opts']['f_lambda'] is None:
        print('Frequency lambda search')
        if data['prep_opts']['f_lam0'] is None:
            lam0_obj = LamFuncs.Lam0_Easylam()
        else:
            lam0_obj = LamFuncs.Lam0_Fixed(data['prep_opts']['f_lam0'])

        if(data['prep_opts']['individual_lambdas']):
            lam_obj = LamFuncs.SearchLambdaIndividual(lam0_obj)
        else:
            lam_obj = LamFuncs.SearchLambda(lam0_obj)
        # rms value to optimize
        optimize_rms_key = 'rms_re_im_noerr'
        optimize_rms_index = 1  # imaginary part
        lam_obj.rms_key = optimize_rms_key
        lam_obj.rms_index = optimize_rms_index
    else:
        lam_obj = LamFuncs.FixedLambda(data['prep_opts']['f_lambda'])

    reg_object = RegFuncs.SmoothingFirstOrder(decouple=[0, ])
    ND.Model.add_regularization(0, reg_object, lam_obj)

    # # add time regularization
    # rho0 regularization
    if(data['prep_opts']['time_weighting_rho0'] or
       data['prep_opts']['time_weighting_mi']):
        weighting_obj = RegFuncs.DifferenceWeighting(data['times'])
    else:
        weighting_obj = None

    if(data['prep_opts']['trho0_first_order']):
        reg_obj = RegFuncs.SmoothingFirstOrder(
            decouple=[],
            outside_first_dim=[0, ],
            weighting_obj=weighting_obj)
    else:
        reg_obj = RegFuncs.SmoothingSecondOrder(
            decouple=[],
            outside_first_dim=[0, ],
            weighting_obj=None)

    ND.Model.add_regularization(
        1,
        reg_obj,
        LamFuncs.FixedLambda(
            data['prep_opts']['t_rho0_lambda']
        )
    )

    # m regularization
    if data['prep_opts']['tmi_first_order']:
        reg_obj = RegFuncs.SmoothingFirstOrder(
            decouple=[],
            outside_first_dim=range(
                1, nr_tau_values
            ),
            weighting_obj=weighting_obj
        )
    else:
        reg_obj = RegFuncs.SmoothingSecondOrder(
            decouple=[],
            outside_first_dim=range(
                1, nr_tau_values)
        )
    ND.Model.add_regularization(
        1, reg_obj,
        LamFuncs.FixedLambda(
            data['prep_opts']['t_m_i_lambda']
        )
    )
    return ND


def fit_one_time_series(data):
    ND = _prepare_ND_object(data)
    ND.run_inversion()
    final_iteration = ND.iterations[-1]

    # renormalize data
    if data['inv_opts']['norm_factors'] is not None:
        parsize = final_iteration.Model.M_base_dims[0][1]
        spectrum_nr = 0
        for index, norm_fac in zip(range(0, final_iteration.m.size, parsize),
                                   data['inv_opts']['norm_factors']):
            # add normalization factor to the parameters
            final_iteration.m[index] -= np.log10(norm_fac)
            final_iteration.f = final_iteration.Model.f(final_iteration.m)
            # data
            # note: the normalization factor can be applied either to the
            # magnitude, or to both real and imaginary parts!
            final_iteration.Data.D[:, :, spectrum_nr] /= norm_fac
            spectrum_nr += 1

    call_fit_functions(data, ND)
    return ND


def call_fit_functions(data, ND):
    if data['prep_opts']['plot']:
        print('Plotting final iteration')
        ND.iterations[-1].plot()
        ND.iterations[-1].plot_reg_strengths()

    if data['prep_opts']['plot_it_spectra']:
        for it in ND.iterations:
            it.plot()

    if data['prep_opts']['plot_lambda'] is not None:
        ND.iterations[data['prep_opts']['plot_lambda']].plot_lcurve()


def main():
    options = cfg_time.cfg_time()
    options.parse_cmd_arguments()

    options.check_input_files(['times', ])
    outdir_real, options = lDDi.create_output_dir(options)

    data = get_data_dd_time(options)

    # for the fitting process, change to the output_directory
    pwd = os.getcwd()
    os.chdir(options['output_dir'])
    fit_data(data)
    # go back to initial working directory
    os.chdir(pwd)


if __name__ == '__main__':
    main()
