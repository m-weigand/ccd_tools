#!/usr/bin/env python3
"""
Test the basic normalization procedure by comparing the forward modeling of
the resisitvity and the conductivity formulation for different normalization
factors.
"""
import numpy as np
from nose.tools import *
import lib_dd.main as dd_res
import lib_dd.conductivity.model as dd_cond
from crlab_py.mpl import *


class test_dd_resistivity():
    @classmethod
    def teardown(self):
        pass

    def setup(self):
        self.frequencies = np.logspace(-3, 4, 30)
        settings = {
            'Nd': 20,
            'tausel': 'data_ext',
            'frequencies': self.frequencies
        }
        self.dd_res = dd_res.get('log10rho0log10m', settings)
        self.dd_cond = dd_cond.dd_conductivity(settings)
        # generate a RTD:
        self.m = np.ones_like(self.dd_res.tau)
        center = int(self.m.size / 2)
        length = int(center / 3)

        index = np.arange(0, self.m.size)
        m = np.exp(-(index - center)**2/(2 * length))/np.sqrt(2*np.pi)
        self.m = m / 1e3



    def test_norm_res(self):
        print('test normalization')
        rho0_orig = np.log10(100)
        norm_facs = (1, 10, 100)

        ergs = []
        for norm_fac in norm_facs:
            rho0 = rho0_orig - np.log10(norm_fac)
            pars = np.hstack((rho0, np.log10(self.m)))
            erg = self.dd_res.forward(pars)
            ergs.append(erg)

        # fig, axes = plt.subplots(2, 1, figsize=(5, 4))
        for norm_fac, erg in zip(norm_facs, ergs):
            # renorm results
            erg *= norm_fac
            diff = erg - ergs[0]
            assert(np.sum(diff) <= 1e-14)

            # ax = axes[0]
            # ax.semilogx(self.frequencies, erg[:, 0], '.-')
            # ax = axes[1]
            # ax.loglog(self.frequencies, erg[:, 1], '.-')
        # fig.savefig('norm_res.png')


    def test_norm_cond(self):
        print('test normalisation')
        sigi_orig = np.log10(100)
        norm_facs = (1, 10, 100)

        ergs = []
        for norm_fac in norm_facs:
            sigi = sigi_orig - np.log10(norm_fac)
            pars = np.hstack((sigi, np.log10(self.m)))
            erg = self.dd_cond.forward(pars)
            ergs.append(erg)

        # fig, axes = plt.subplots(2, 1, figsize=(5, 4))
        for norm_fac, erg in zip(norm_facs, ergs):
            # renorm results
            erg *= norm_fac
            diff = erg - ergs[0]
            assert(np.sum(diff) <= 1e-14)

            # ax = axes[0]
            # ax.semilogx(self.frequencies, erg[:, 0], '.-')
            # ax = axes[1]
            # ax.loglog(self.frequencies, erg[:, 1], '.-')
        # fig.savefig('norm_cond.png')
