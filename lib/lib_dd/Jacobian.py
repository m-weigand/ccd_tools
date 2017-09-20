# -*- coding: utf-8 -*-
""" Copyright 2014-2017 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
Jacobian implementation for a Debye-Decomposition style function
Resistivity formulation
"""
import numpy as np


def Jacobian(omega, pars, s, partials):
    r"""
    Calculate the Jacobian matrix for a given set of parameters m and
    relaxation times s (:math:`s = log_{10}(\tau)`).

    Parameters
    ----------
    omega : Angular frequencies :math:`2 \cdot \pi \cdot f`
    pars : :math:`\rho_0` and :math:`m_i` values in the parmeterisation
          (linear,log10) of the provided partials
    s:  :math:`\tau` values in log10
    partials : List of the four partial derivative functions
               :math:`\frac{\partial Re}{\partial \rho0}, \frac{\partial
               Re}{\partial m_i}, \frac{\partial -Im}{\partial \rho0},
               \frac{\partial -Im}{\partial m_i}`

    Returns
    -------
    The derivatives of d Re(rho)/d g_i and d -Im(rho)d g_i in form of a
    2*K x P matrix (K = number of frequencies), (P = number of model
    parameters)

    """
    K = omega.shape[0]
    P = pars.shape[0]

    Jacobian = np.zeros((K * 2, P))

    # ## Real part ####

    # first column d Re/d rho0; d Im / d rho
    Jacobian[0:K, 0] = partials[0](pars)[:, 0]

    # second to last column d Re/ d g_i where m = chargeability values
    Jacobian[0:K, 1:] = partials[1](pars)

    # ## Imaginary part ###

    # first column d -Im/ d rho0
    Jacobian[K:, 0] = partials[2](pars)[:, 0]

    # second to last column d - Im/d g_i
    Jacobian[K:, 1:] = partials[3](pars)

    return Jacobian
