"""
stateless code part of the ccd_single decomposition. Everthing else is located
in the ccd_single object
"""
import os
import NDimInv
import NDimInv.regs as RegFuncs
import NDimInv.reg_pars as LamFuncs
import gc
import lib_dd.plot as lDDp
import sip_formats.convert as sip_converter
import lib_dd.conductivity.model as cond_model
from lib_dd.models import ccd_res

import numpy as np


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
    # run plot functions in output directory
    pwd = os.getcwd()
    os.chdir(fit_data['outdir'])
    print('Changing to: {0}'.format(fit_data['outdir']))

    if(fit_data['prep_opts']['plot']):
        print('Plotting final iteration')
        ND.iterations[-1].plot(
            norm_factors=fit_data['inv_opts']['norm_factors'])
        ND.iterations[-1].Model.obj.plot_stats(
            '{0}'.format(fit_data['nr'])
        )

    if(fit_data['prep_opts']['plot_reg_strength']):
        ND.iterations[-1].plot_reg_strengths()

    if(fit_data['prep_opts']['plot_it_spectra']):
        for it in ND.iterations:
            it.plot()

    if(fit_data['prep_opts']['plot_lambda'] is not None):
        ND.iterations[fit_data['prep_opts']['plot_lambda']].plot_lcurve()
    os.chdir(pwd)
