#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests for the dd_res_inversion module

This module runs some parameter studies to get an overview of the accuracy of the algorithms

Run with

nosetests -s -v test_dd_res_inv_studies.py

To run a specific test:

nosetests -s -v test_dd_res_inv_studies.py:test_dd_res_inv_studies.test_tau_rho0_no_noise
"""
import sys
sys.path.append('..')

from crlab_py.mpl import *
import numpy as np
import scipy.stats as stats
from nose.tools import *
import lib_dd.dd_res_inversion as DD_RES_INV
import numdifftools as nd
from crlab_py.mpl import *
import crlab_py.colecole as colecole

class test_dd_res_inv_studies():
    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown(self):
        pass

    def setup(self):
        self.dd_res_inv = DD_RES_INV.dd_res_inversion('log10rho0log10m')
        self.frequencies = np.logspace(-3, 4, 100)
        self.omega = 2 * np.pi * self.frequencies
        self.nr_tau_fit = 100

    def teardown(self):
        pass


    def test_one_spectrum(self):
        """
        Fit one spectrum
        nosetests -s -v test_dd_res_inv_studies.py:test_dd_res_inv_studies.test_one_spectrum
        """
        s = np.log10(np.logspace(-5,2, 100))
        p_orig,re,mim = self.dd_res_inv.dd_obj.get_synthetic_spectrum(self.omega, s, rho0=100.0, nr_chargeability=100, strength=0.3, noise=0)
        # set tau distribution
        s_fit = np.log10(np.logspace(-5,2,100))

        # now fit the spectra
        opt = {}
        opt['lam0'] = 'user'
        opt['lam0_value'] = 1e2

        self.check_spectra([(re, mim),], s_fit, options=opt, prefix='one_')

    def test_lam0(self):
        """
        Test different lam0 methods
        nosetests -s -v test_dd_res_inv_studies.py:test_dd_res_inv_studies.test_lam0
        """
        s = np.log10(np.logspace(-5,2, 100))
        p_orig,re,mim = self.dd_res_inv.dd_obj.get_synthetic_spectrum(self.omega, s, rho0=500.0, nr_chargeability=100, strength=0.3, noise=0.1)
        # set tau distribution
        s_fit = np.log10(np.logspace(-5,2,100))

        for method in ('easylam', 'jacobian', 'user'):
            # now fit the spectra
            opt = {}
            opt['lam0'] = method
            opt['lam0_value'] = 1e5

            self.check_spectra([(re, mim),], s_fit, options=opt, prefix='lam0_{0}_'.format(method))

    def test_rho0_and_chargeability(self):
        """
        nosetests -s -v test_dd_res_inv_studies.py:test_dd_res_inv_studies.test_rho0_and_chargeability
        """
        self.run_check_rho0_and_chargeability(0, 100)
        self.run_check_rho0_and_chargeability(0.05, 100)
        self.run_check_rho0_and_chargeability(0.1, 100)

    def test_s_fit(self):
        """
        nosetests -s -v test_dd_res_inv_studies.py:test_dd_res_inv_studies.test_s_fit
        """
        self.run_check_rho0_and_chargeability(0, 10)
 #       self.run_test_rho0_and_chargeability(0, 50)
 #       self.run_test_rho0_and_chargeability(0, 100)


    def run_check_rho0_and_chargeability(self, noise, nr_s_fit):
        """
        Vary rho0 and strength (aka chargeability)
        """
        nr_tests = 4   # number of test values for rho0 and strenght, respectively

        nr_tau = 100
        spectra_orig = []
        pars_orig = []
        s_orig = []
        s = np.log10(np.logspace(-5,2, nr_tau))

        for rho0 in np.logspace(1,4,nr_tests):
            for strength in np.linspace(0.01,1,nr_tests):
                p_orig,re,mim = self.dd_res_inv.dd_obj.get_synthetic_spectrum(self.omega, s, rho0=rho0, nr_chargeability=nr_tau, strength=strength, noise=noise)
                spectra_orig.append( (re,mim))
                s_orig.append(s)
                pars_orig.append(p_orig)

        # set tau distribution
        s_fit = np.log10(np.logspace(-5,2,nr_s_fit))

        # now fit the spectra
        opt = {}
        opt['lam0'] = 'jacobian'
        opt['lam0_value'] = 1
        last_it = self.check_spectra(spectra_orig, s_fit, opt, 'rho0_chargeability_noise_{0:03}_sfit_{1}'.format(noise, nr_s_fit), plot=False, rms_threshold=0.2)

#        self.create_matrix_plots(last_it, nr_tests, nr_tests, 'rho0_and_chargeability_noise_{0:03}_sfit_{1}'.format(noise, nr_s_fit))

    def create_matrix_plots(self, last_it, nrx, nry, filename):

        # plot the rms results to an image
        for i in ('rms_re', 'rms_im', 'rms_no_err'):
            values = [getattr(x, i) for x in last_it]
            rms = np.array(values)
            rms = rms.reshape((nrx, nry))

            fig = plt.figure()
            ax = fig.add_subplot(111)
            im = ax.imshow(rms, interpolation='none')
            from mpl_toolkits.axes_grid1 import make_axes_locatable
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size=0.2, pad=0.15)
            cb = plt.colorbar(im, orientation='vertical', cax=cax)
            ax.set_xlabel('rho0')
            ax.set_ylabel('strength')
            ax.set_title(i.replace('_', '\_'))
            y_format = mpl.ticker.FuncFormatter(self.func)  # make formatter
            ax.yaxis.set_major_formatter(y_format)  # set formatter to needed axis

            fig.savefig(filename + '_' + i + '.png')

    def func(self, x, pos):  # formatter function takes tick label and tick position
        s = str(x)
        ind = s.index('.')
        return s[:ind] + ',' + s[ind+1:]   # change dot to comma

    def check_spectra(self, spectra_orig, s_fit, options, prefix='', plot=False, rms_threshold=1):
        """
        Test fitting provided spectra

        Parameters
        ----------
        options : dict containing inversion settings
        rms_threshold : even if plot==False, plot all spectra with an RMS above the threshold
        """
        # recreate inversion object
        self.dd_res_inv = DD_RES_INV.dd_res_inversion('log10rho0log10m')

        last_it = []
        for i in range(0, len(spectra_orig)):
#        for i in (11,):
            print('Fitting spectrum {0} from {1}'.format(i+1, len(spectra_orig)))
            # set initial m values

            # this is a good starting distribution for (rho0, m)
            # m0 = np.zeros(s_fit.shape, dtype=float)

            # this looks like a good starting distribution for (rho0, log10(m))
            # m0 = 1e-4 * np.ones(s_fit.shape, dtype=float)

            # this looks like a good starting distribution for (log10(rho0), log10(m))
            # m0 = 1e-3 * np.ones(s_fit.shape, dtype=float)

            #parameters_start = np.hstack((spectra_orig[i][0][0], m0))

            parameters_start_test = self.dd_res_inv.dd_obj.estimate_starting_parameters_1(spectra_orig[i][0], spectra_orig[i][1], self.omega, s_fit)

            self.dd_res_inv.use_damping = False
            self.dd_res_inv.use_tikhonov = True

            # initial value
            self.dd_res_inv.lambda_set_initial_method(options['lam0'], value=options['lam0_value'])

            # lambda selection for each iteration
#            self.dd_res_inv.lambda_use_l_curve()
 #           self.dd_res_inv.lambda_use_fixed()
            self.dd_res_inv.lambda_use_factor_quotient()

            m,it_infos = self.dd_res_inv.fit_simple_spectrum_reim_linear(self.omega, parameters_start_test, s_fit, spectra_orig[i][0], spectra_orig[i][1])
            #if(plot or it_infos[-1].rms_no_err >= rms_threshold):
            if(plot):
                it_infos[-1].plot_spectrum(suffix='_{0:03}'.format(i+1), prefix=prefix)

#            it_infos[-1].plot_m_diff(pars_orig[i][1:], suffix='_{0:03}'.format(i+1))
#           for j in it_infos:
#               j.plot_spectrum(suffix='_{0:03}'.format(i+1))
            last_it.append(it_infos[-1])

        if(plot and len(last_it) > 1):
            # now create an Nx1 implot of the RMS values
            rms_no_err = [x.rms_no_err for x in last_it]
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(rms_no_err)
            fig.savefig('{0}overview_rms.png'.format(prefix))

        return last_it
