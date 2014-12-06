#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2014 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.

===============================================================================
This is a really old and naive implementation of the Cole-Cole model. Do not
change or work with it! It's only here until we can adapt lib_cc and/or lib_cc2
as replacements.
===============================================================================
"""
import numpy as np


def cole_real(frequencies, params):
    data_complex = cole_complex(frequencies[0:frequencies.shape[0]/2],
                                params)
    data_real = np.real(data_complex)
    data_imag = np.imag(data_complex)

    mag = np.abs(data_complex)
    # phases, [mrad]
    pha = 1000 * np.arctan(data_imag/data_real)
    data_all = np.hstack((np.log(mag), pha))
    return data_all


def cole_complex(frequencies, params):
    # determine number of Cole-Cole terms
    nr_cc_terms = (len(params) - 1) / 3

    # extract the Cole-Cole parameters
    rho0 = np.exp(params[0])  # DC resistance
    m = params[1:len(params):3]  # chargeability
    tau = np.exp(params[2:len(params):3])  # time constant
    c = params[3:len(params):3]  # cementation exponent

    # extract frequencies
    f = frequencies

    # prepare temporary array which will store the values of all CC-terms,
    # which later will be summed up
    term = np.zeros((f.shape[0], nr_cc_terms), dtype=np.complex128)

    # compute Cole-Cole function, each term separately
    for k in range(0, nr_cc_terms):
        term[:, k] = (m[k]) * (1 - 1 /
                               (1 + ((0+1j) * 2 * np.pi * f * tau[k]) ** c[k]))

    # sum up
    term_g = np.sum(term, 1)

    # multiply rho0
    Zfit = rho0 * (1 - term_g)

    return Zfit


def cole_log(inputdata, params):

    """
    compute impedance values (amplitude and phase) from a given set of
    Cole-Cole parameters at different frequencies.
    ---
    Parameters:
    inputdata   - array containing the frequency values at which the impedance
                  values will be computed twice: [frequencies  frequencies].
    params      - array containg the rho0 and an arbitrary number of (m,tau,c)
    tuples of the parameters: ln(rho0), m, ln(tau), c. The natural logarithm is
    used here! rho0 and tau are always positive (in a physical sense).  Thus
    the length of this vector is L = 1 + 3 * N, where N is the number of
    Cole-Cole terms.  m and c are both limited to the range [0,1]
    ----
    Returns:
    fitdata     - array containing amplitude and phase values for the given
                  frequencies. The first half of the vector contains the
                  amplitudes (in natural logarithm), the second one the phases,
                  in mRad
    """
    # determine number of Cole-Cole terms
    nr_cc_terms = (len(params) - 1) / 3

    # extract the Cole-Cole parameters
    rho0 = np.exp(params[0])  # DC resistance
    m = params[1:len(params):3]  # chargeability
    tau = np.exp(params[2:len(params):3])  # time constant
    c = params[3:len(params):3]  # cementation exponent

    # extract frequencies
    f = inputdata[0:(len(inputdata) / 2)]
    # prepare temporary array which will store the values of all CC-terms,
    # which later will be summed up
    term = np.zeros((len(f), nr_cc_terms), dtype=np.complex128)

    # compute Cole-Cole function, each term separately
    for k in range(0, nr_cc_terms):
        term[:, k] = (m[k]) * (
            1 - 1 / (1 + ((0+1j) * 2 * np.pi * f * tau[k]) ** c[k]))

    # sum up
    term_g = np.sum(term, 1)

    # multiply rho0
    Zfit = rho0 * (1 - term_g)
    # we return magnitude and phase values
    rhoreal = np.real(Zfit)
    rhoimag = np.imag(Zfit)
    try:
        rhofit = np.sqrt(rhoreal ** 2 + rhoimag ** 2)  # Amplitude
    except FloatingPointError:
        # Return NaN values for the whole spectrum!
        rhofit = np.empty_like(rhoreal)
        rhofit[:] = np.nan
        # Developer : Uncomment the following lines to show more info data
        # leading to the error
        print('FloatingPointError')
        print('rhofit', rhofit)
        print('rhoreal', rhoreal)
        print('rhoimag', rhoimag)
        print(rho0, m, tau, c)
        print(params)

    # phases, [mrad]
    phifit = 1000 * np.arctan(rhoimag/rhoreal)

    # Magnitude, Phase
    # returns a 2 x [number of frequencies] ndarray
    # fitdata[0, :] are the magnitudes
    # fitdata[1, :] the phase values

    fitdata = np.vstack((np.log(rhofit), phifit))
    return fitdata


def cc_jac(f, par):
    """
    Wrapper for cc_jac_real which takes a frequency array as large as the
    output of the cole_real function.
    """
    f_red = f[f.shape[0] / 2:]
    return cc_jac_real(f_red, par)


def cc_jac_real(f_red, par):
    """
    d rho^hat/d |R|
    """
    ret = np.vstack((cc_der_lnR(f_red, par), cc_der_phi(f_red, par)))
    return ret


def cc_der_phi(f, par):
    rho = cole_complex(f, par)

    term2 = cc_drhodx_complex(f, par) / np.vstack((rho, rho, rho, rho)).T

    ret = 1j * (cc_der_lnR(f, par) - term2)
    ret = np.real(ret)
    return ret


def cc_drhodx_complex(f_red, par):
    der_lnrho0 = cc_der_lnrho(f_red, par)
    der_m = cc_der_m(f_red, par)
    der_lntau = cc_der_lntau(f_red, par)
    der_c = cc_der_c(f_red, par)

    jac_complex = np.vstack((der_lnrho0, der_m, der_lntau, der_c))
    return jac_complex.T


def cc_der_lnR(f, par):
    rho = cole_complex(f, par)
    crho = rho.conjugate()

    faktor = 1 / (2 * rho * crho)

    sum1 = (crho * rho) + (crho * rho)
    sum2 = (cc_der_m(f, par).conjugate() * rho + crho * cc_der_m(f, par))
    sum3 = (
        cc_der_lntau(f, par).conjugate() * rho + crho * cc_der_lntau(f, par))
    sum4 = (cc_der_c(f, par).conjugate() * rho + crho * cc_der_c(f, par))

    ret = np.vstack(
        (faktor * sum1, faktor * sum2, faktor * sum3, faktor * sum4))
    ret = np.real(ret)
    return ret.T


def cc_der_lnrho(f, par):
    return cole_complex(f, par)


def cc_der_m(f, par):
    ret_complex = np.exp(par[0]) * (
        1 / (1 + (1j * f * 2 * np.pi * np.exp(par[2]))**par[3]) - 1)
    return ret_complex


def cc_der_lntau(f, par):
    a = - (
        np.exp(par[0]) * par[1] * (
            1j * f * 2 * np.pi * np.exp(par[2]))**par[3]) / (1 + (
                1j * f * 2 * np.pi * np.exp(par[2]))**par[3])**2
    ret_komplex = a * par[3]
    return ret_komplex


def cc_der_c(f, par):
    a = - (
        np.exp(par[0]) * par[1] * (
            1j * f * 2 * np.pi * np.exp(par[2]))**par[3]) / (
                1 + (1j * f * 2 * np.pi * np.exp(par[2]))**par[3])**2
    ret_komplex = a * np.log(1j * f * 2 * np.pi * np.exp(par[2]))
    return ret_komplex
