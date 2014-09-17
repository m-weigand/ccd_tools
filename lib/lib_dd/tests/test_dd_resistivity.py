#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests for the dd_resistivity module

Run with

nosetests test_dd_resistivity.py -s -v

To run a specific test:

nosetests -s -v test_dd_resistivity.py:test_dd_resistivity

TODO:
    - check log10Re-Jacobian
    - We can not only check against the numerical approximation but also
      against parts of the Cole-Cole Jacobian as implemented in
      crlab_py.colecole
"""
import numpy as np
from nose.tools import *
import numdifftools as nd
#import crlab_py.colecole as colecole
import lib_dd.dd_resistivity

class test_dd_resistivity():
    @classmethod
    def teardown(self):
        pass

    def setup(self):
        pass

    def check_Jacobian_re_mim_vs_numapprox(self, dd_obj):
        """
        Check a Jacobian matrix vs the numerical approximation using just the
        forward functions.
        """
        frequencies = np.logspace(-2,4,40)
        omega = 2 * np.pi * frequencies
        parameters_linear = np.array((100, 0.08)) # rho0 m
        parameters = dd_obj.convert_parameters(parameters_linear)

        s = np.array((np.log10(0.1),)) # log10 tau

        Jac_linear = dd_obj.Jacobian_re_mim(omega, parameters, s)

        # compute a numerical approximation
        Jac_approx_func = nd.Jacobian(lambda pars: np.vstack(dd_obj.forward_re_mim(omega, pars, s)))
        Jac_approx = Jac_approx_func(parameters)

        # check each of the chargeability derivatives
        for index in range(0,parameters.shape[0]):
            analytical = Jac_linear[:, index]
            numerical = Jac_approx[:, index]
            diff = np.abs(analytical - numerical)
            diff_rel = diff / np.abs(analytical)
            rms = 1/diff.shape[0] * np.sqrt(np.sum(diff)**2)
            print('')
            print('Parameter nr: {0}'.format(index+1))
            print('RMS', rms)
            print('Min/Max', np.min(diff), np.max(diff))
            print('Min/Max (relative)', np.min(diff_rel), np.max(diff_rel))
            print('Mean', np.mean(diff))

            assert_almost_equal(np.max(diff), 0)
            assert_almost_equal(rms, 0)

    ## tests ##

    def test_Jacobian_linear(self):
        for parameterisation in ('rho0m', 'rho0log10m', 'log10rho0log10m'):
            dd_obj = lib_dd.dd_resistivity.get(parameterisation)
            self.check_Jacobian_re_mim_vs_numapprox(dd_obj)
