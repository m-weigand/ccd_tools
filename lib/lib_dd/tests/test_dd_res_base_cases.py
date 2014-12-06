#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests for the modules:
    dd_res_base_rho0_0m
    dd_res_base_rho0_log10m
    dd_res_base_log10rho0_log10m

Run with

nosetests test_cc_res_base_cases.py -s -v
"""
import numpy as np
from nose.tools import *
import NDimInv.colecole as colecole
import lib_dd.dd_res_base_rho0_m as dd_res_base_rho0_m
import lib_dd.dd_res_base_rho0_log10m as dd_res_base_rho0_log10m
import lib_dd.dd_res_base_log10rho0_log10m as dd_res_base_log10rho0_log10m

class skeleton():
    """
    This is the basic test class which will only work if the variable
    self.dd_base will be set using the setup(self) function defined in a
    derived class.
    """
    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown(self):
        pass

    def setup_base(self):
        self.frequencies = np.logspace(-2,3,20)
        self.omega = 2 * np.pi * self.frequencies

    def setup(self):
        self.dd_base = None # should be set by child class which inherits this class
        self.setup_base()

    def teardown(self):
        pass

    def check_vs_cc(self, parameters_linear):
        """
        Compares output from Cole-Cole and Debye forward modelling
        """
        # compile Cole-Cole parameters
        # rho0,m in log
        parameters_cc = parameters_linear[:]
        for index in [0, ] + range(2,len(parameters_linear),3):
            parameters_cc[index] = np.log(parameters_cc[index])

        # compile Debye parameters
        parameters_dd_linear = []
        parameters_dd_linear.append(parameters_linear[0]) # rho0
        for index in range(1,len(parameters_linear),3):
            parameters_dd_linear.append(parameters_linear[index])

        parameters_dd = self.dd_base.convert_parameters(parameters_dd_linear)

        s = [parameters_linear[index] for index in range(2,len(parameters_linear),3)]
        s = np.atleast_1d(np.log10(s))

        # calculate Cole-Cole response
        cc_complex = colecole.cole_complex(self.frequencies, parameters_cc)
        re_cc = np.real(cc_complex)
        mim_cc = -np.imag(cc_complex)

        re_dd = self.dd_base.forward_re(self.omega, parameters_dd, s)
        mim_dd = self.dd_base.forward_mim(self.omega, parameters_dd, s)

        # differences
        diff_re = re_cc - re_dd
        diff_mim = mim_cc - mim_dd

        # differences should be close to zero
        for i in list(diff_re) + list(diff_mim):
            assert_almost_equal(i, 0)

    ### tests ###
    def test_calculate_vs_single_cc(self):
        """
        Test output for only one term - equal to a single Cole-Cole model with c=1
        """
        parameters_linear = [100, 0.1, 0.04, 1]
        self.check_vs_cc(parameters_linear)

    def test_calculate_vs_double_cc(self):
        """
        Test output for two terms - equal to a double Cole-Cole model with c=1
        """
        parameters_linear = [100, 0.1, 0.04, 1, 0.2, 0.001, 1]
        self.check_vs_cc(parameters_linear)

#   def test_dRe_drho0_linear(self):
#       r"""
#       Test :math:`\frac{\partial Re(\hat{\rho})}{\partial \rho_0}` against the numerical approximation.

#       """
#       # parameters
#       frequencies = np.loadtxt('files/spectrum3/frequencies.dat')
#       omega = 2 * np.pi * frequencies
#       s = np.array((np.log10(0.0001), np.log10(0.1)))
#       parameters = np.array((100, np.log10(0.15), np.log10(0.08)))

#       # get derivative
#       derivative = self.dd_res.dRe_drho0_linear(omega, parameters, s)

#       # compute a numerical approximation
#       Jac_approx_func = nd.Jacobian(lambda pars: self.dd_res.calculate_response_real(omega, pars, s))
#       Jac_approx = Jac_approx_func(parameters)

#       diff = np.abs(Jac_approx[:,0, np.newaxis] - derivative) / np.abs(derivative)

#       rms = 1/diff.shape[0] * np.sqrt(np.sum(diff**2))

#       print('')
#       print('RMS', rms)
#       print('Min/Max (relative)', np.min(diff), np.max(diff))
#       print('Mean', np.mean(diff))

#       assert_almost_equal(np.max(diff), 0)
#       assert_almost_equal(rms, 0)



class test_dd_res_base_rho0_m(skeleton):
    def setup(self):
        self.dd_base = dd_res_base_rho0_m.dd_res_base()
        self.setup_base()

class test_dd_res_base_rho0_log10m(skeleton):
    def setup(self):
        self.dd_base = dd_res_base_rho0_log10m.dd_res_base()
        self.setup_base()

class test_dd_res_base_log10rho0_log10m(skeleton):
    def setup(self):
        self.dd_base = dd_res_base_log10rho0_log10m.dd_res_base()
        self.setup_base()

