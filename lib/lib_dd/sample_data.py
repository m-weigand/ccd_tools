"""
Copyright 2014 Maximilian Weigand


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
