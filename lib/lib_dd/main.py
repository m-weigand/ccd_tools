#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright 2014 Maximilian Weigand

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
