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

Provide simple functions for sample spectrums
"""
import numpy as np
import scipy.stats as stats
import main


class one_peak():

    def __init__(self):
        # init the object
        model_settings = {}
        model_settings['Nd'] = 5
        self.frequencies = np.logspace(-3, 4, 40)
        model_settings['frequencies'] = self.frequencies
        model_settings['tau_sel'] = 'data_ext'
        self.obj = main.get('log10rho0log10m', model_settings)

        # now
        rho0 = np.sqrt(100)
        pol_maximum = self.frequencies.size / 2
        f_max = self.frequencies[pol_maximum]
        tau_max = 1 / (2 * np.pi * f_max)
        s_max = np.log10(tau_max)

        m = stats.norm.pdf(self.obj.s, s_max, 1)
        # normalize
        m /= np.sum(m)

        pars_linear = np.hstack((rho0, m))
        parameters = self.obj.convert_parameters(pars_linear)

        self.rho0 = rho0
        self.m = m
        print 'parsize', parameters.size

        self.re_mim = self.obj.forward(parameters)
