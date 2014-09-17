#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
from nose.tools import *
import subprocess
import os
import lib_dd.inversion as DD_RES
import numpy as np

dd_res_inv = DD_RES.dd_res_inversion()


def generate_data():
    """
    Generate the test spectra.

    Call this function only once
    """
    if(os.path.isdir('Data')):
        print('Directory data already exists. ' +
              'Assuming data is already present')
        return

    os.makedirs('Data')

    # generate default values
    nr_taus_decade = 20
    f_default = np.logspace(-3, 5, 30)
    omega_default = 2 * np.pi * f_default
    tau_default, s_default, fx = dd_res_inv.get_tau_values_for_data(
        f_default, nr_taus_decade)

    # generate list of rho0 values
    list_rho0 = []
    for rho0 in np.logspace(1, 5, 10):
        list_rho0.append(rho0)

    # generate different numbers of tau values
    list_s = []
    for nr_tau_decade in (10, ):
        tau, s, fx = dd_res_inv.get_tau_values_for_data(f_default,
                                                        nr_tau_decade)
        list_s.append(s)

    # generate list of m strengths
    list_m_strength = []
    for strength in (0.001, 0.1, 0.2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
        list_m_strength.append(strength)

    # generate data sets
    # rho0, vary tau and m_strength
    generate_dataset(omega_default, lrho0=[10, 100, 100, ], ls=list_s,
                     lm_strength=list_m_strength)


def generate_dataset(omega, lrho0, ls, lm_strength):
    lmag = []
    lpha = []
    for rho0 in lrho0:
        for s in ls:
            for strength in lm_strength:
                p, re, mim = dd_res_inv.get_synthetic_spectrum(
                    omega, s, rho0=rho0, nr_chargeability=len(s),
                    strength=strength, noise=0)
                mag = np.abs(re - 1j * mim)
                pha = np.arctan(-mim / re) * 1000  # mrad
                print('re', re)
                print('mim', mim)
                print('mag', mag)
                print('pha', pha)
                lmag.append(mag)
                lpha.append(pha)

    # save to file
    mmag = np.array(lmag)
    mpha = np.array(lpha)

    magpha = np.hstack((mmag, mpha))
    print(magpha.shape)
    print(omega.shape)

    np.savetxt('Data/frequencies.dat', omega / (2 * np.pi))
    np.savetxt('Data/data.dat', magpha)

    return

    # the keys determine the values:
    # 0 - rho0
    # 1 - nr of tau values per decade
    # 2 - m_level factor

    # second value: nr of items to generate

    # third: default
    axes = {1: ('nr_tau', 3, 10),
            0: ('rho0', 4, 100),
            2: ('m_level', 5, 1)
            }

    exit()
    nr_tests = 4   # number of test values for rho0 and strenght, respectively

    nr_tau = 100
    spectra_orig = []
    pars_orig = []
    s_orig = []
    s = np.log10(np.logspace(-5, 2, nr_tau))

    for rho0 in np.logspace(1, 4, nr_tests):
        for strength in np.linspace(0.01, 1, nr_tests):
            p_orig, re, mim = self.dd_res_inv.get_synthetic_spectrum(
                self.omega, s, rho0=rho0, nr_chargeability=nr_tau,
                strength=strength, noise=noise)
            spectra_orig.append((re, mim))
            s_orig.append(s)
            pars_orig.append(p_orig)


def test_generator():
    test_cases = []
    # find all directories with data.dat and frequencies.dat
    for root, dirs, files in os.walk('.'):
        if('data.dat' in files and 'frequencies.dat' in files):
            test_cases.append((root + os.sep + 'data.dat',
                               root + os.sep + 'frequencies.dat'))

    for datfreq in test_cases:
        yield run_case, datfreq[0], datfreq[1]


def run_case(data_file, frequency_file):
    cmd = 'dd_single.py -o "test_output" '
    cmd += '-f "{0}" -d "{1}"'.format(frequency_file, data_file)
    result = subprocess.call(cmd, shell=True)
    assert_equal(result, 0)


generate_data()
