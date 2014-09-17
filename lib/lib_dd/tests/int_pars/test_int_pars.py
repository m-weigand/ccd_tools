#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests for the lib_dd.int_pars module

Run with

nosetests test_dd_test_function.py -s -v

To run a specific test:

nosetests -s -v test_nt_pars.py:FUNCTION

"""
import numpy as np
from nose.tools import *
import lib_dd.int_pars as int_pars


class test_int_pars_mtot():
    @classmethod
    def teardown(self):
        pass

    def setup(self):
        # generate tau and s values
        self.tau = np.logspace(-2, 4, 300)
        self.s = np.log10(self.tau)
        # set original m_tot
        self.m_tot_original = 1e-2
        self.rho0 = 100
        self.m_tot_n_original = self.m_tot_original / self.rho0

        # generate m_i values
        self.m = np.ones(self.tau.size) * (self.m_tot_original /
                                           self.tau.size)
        # put rho0 in front
        self.pars = np.hstack((self.rho0, self.m))

    def test_mtot(self):
        m_tot_linear = int_pars._m_tot_linear(self.pars, self.tau, self.s)
        assert_almost_equal(m_tot_linear, self.m_tot_original)

        m_tot_log10 = int_pars.m_tot(self.pars, self.tau, self.s)
        assert_almost_equal(m_tot_log10, np.log10(self.m_tot_original))

    def test_mtotn(self):
        m_tot_n_linear = int_pars._m_tot_n_linear(self.pars, self.tau, self.s)
        assert_almost_equal(m_tot_n_linear, self.m_tot_n_original)

        m_tot_n_log10 = int_pars.m_tot_n(self.pars, self.tau, self.s)
        assert_almost_equal(m_tot_n_log10, np.log10(self.m_tot_n_original))
