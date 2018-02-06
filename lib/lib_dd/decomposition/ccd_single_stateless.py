"""
stateless code part of the ccd_single decomposition. Everthing else is located
in the ccd_single object
"""
import logging
import os
import gc
import numpy as np

import NDimInv
import NDimInv.regs as RegFuncs
import NDimInv.reg_pars as LamFuncs
import lib_dd.plot as lDDp
import sip_formats.convert as sip_converter
# import lib_dd.conductivity.model as cond_model
from lib_dd.models import ccd_res
from lib_dd.models import ccd_cond


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
        fit_data['outdir'] = data['outdir']
        # change file prefix for each spectrum
        # at the moment we need a copy for this
        frequencies_cropped, cr_data = _filter_nan_values(
            data['frequencies'], data['cr_data'][i]
        )

        fit_data['prep_opts'] = data['prep_opts']
        fit_data['data'] = cr_data
        fit_data['nr'] = i + 1
        fit_data['nr_of_spectra'] = nr_of_spectra
        fit_data['frequencies'] = frequencies_cropped

        # inversion options are changed for each spectrum, so we have to
        # copy it each time
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


def _prepare_ND_object(fit_data):
    # set c parameter for Cole-Cole distribution
    if 'DD_C' in os.environ:
        fit_data['inv_opts']['c'] = float(os.environ['DD_C'])
    else:
        fit_data['inv_opts']['c'] = 1.0

    # use conductivity or resistivity model?
    if 'DD_COND' in os.environ and os.environ['DD_COND'] == '1':
        model = ccd_cond.decomposition_conductivity(fit_data['inv_opts'])
        # Old version:
        # ------------
        # # there is only one parameterisation: log10(sigma_i), log10(m)
        # model = cond_model.dd_conductivity(fit_data['inv_opts'])
    else:
        model = ccd_res.decomposition_resistivity(fit_data['inv_opts'])

    ND = NDimInv.NDimInv(model, fit_data['inv_opts'])
    ND.finalize_dimensions()
    ND.Data.data_converter = sip_converter.convert

    # read in data
    # print fit_data['data'], fit_data['prep_opts']['data_format']
    ND.Data.add_data(
        fit_data['data'],
        fit_data['prep_opts']['data_format'],
        extra=[]
    )

    # now that we know the frequencies we can call the post_frequency
    # handler for the model side
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
    logging.info(
        'Fitting spectrum {0} of {1}'.format(
            fit_data['nr'], fit_data['nr_of_spectra']
        )
    )
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
    # only proceed if one of the plot functions will be called. This makes sure
    # that we can run without an existing output directory, and only fail if we
    # really try to plot...
    keys = (
        'plot',
        'plot_reg_strength',
        'plot_it_spectra',
        'plot_lambda',
    )
    will_activate = [
        fit_data['prep_opts'][key] for key in keys if
        fit_data['prep_opts'][key] is not None
    ]
    if not np.any(np.array(will_activate)):
        return

    # run plot functions in output directory
    pwd = os.getcwd()
    os.chdir(fit_data['outdir'])
    logging.info('Changing to: {0}'.format(fit_data['outdir']))

    if(fit_data['prep_opts']['plot']):
        logging.info('Plotting final iteration')
        ND.iterations[-1].plot(
            filename='_iteration_'.format(fit_data['nr']),
            norm_factors=fit_data['inv_opts']['norm_factors']
        )
        ND.iterations[-1].Model.obj.plot_stats(
            '{0}'.format(fit_data['nr'])
        )

    if(fit_data['prep_opts']['plot_reg_strength']):
        ND.iterations[-1].plot_reg_strengths()

    if(fit_data['prep_opts']['plot_it_spectra']):
        for nr, it in enumerate(ND.iterations[0:-1]):
            it.plot(
                filename='_iteration_',
                norm_factors=fit_data['inv_opts']['norm_factors']
            )

    if(fit_data['prep_opts']['plot_lambda'] is not None):
        ND.iterations[fit_data['prep_opts']['plot_lambda']].plot_lcurve(
            write_output=True
        )
    os.chdir(pwd)
