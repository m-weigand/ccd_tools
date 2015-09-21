#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright 2014,2015 Maximilian Weigand

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
import dd_res_base_rho0_m
import dd_res_base_rho0_log10m
import dd_res_base_log10rho0_log10m
import base_class

"""
Ammend the various parameterisations with a Jacobian function
"""


class dd_resistivity_rho0_m(dd_res_base_rho0_m.dd_res_base,
                            base_class.dd_resistivity_skeleton):
    pass


class dd_resistivity_rho0_log10m(
        dd_res_base_rho0_log10m.dd_res_base, base_class.dd_resistivity_skeleton):
    pass


class dd_resistivity_log10rho0_log10m(
        dd_res_base_log10rho0_log10m.dd_res_base, base_class.dd_resistivity_skeleton):
    pass


def get(parameterisation, settings):
    """
    Helper function which returns a resistivity object with the requested
    parameterisation.

    Parameters
    ----------
    parameterisation : ['rho0m'|'rho0log10m'|'log10rho0log10m']
    settings : setting struct containing various information

    Returns
    -------
    dd_obj: can be used in the inversion module
    """
    if(parameterisation == 'rho0m'):
        return dd_resistivity_rho0_m(settings)
    elif(parameterisation == 'rho0log10m'):
        return dd_resistivity_rho0_log10m(settings)
    elif(parameterisation == 'log10rho0log10m'):
        return dd_resistivity_log10rho0_log10m(settings)
    else:
        print('ERROR: Parameterisation not found.')
        exit()
