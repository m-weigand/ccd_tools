#!/usr/bin/env python
import os
import lib_dd.decomposition.ccd_single as ccd_single
import lib_dd.config.cfg_single as cfg_single

import numpy as np

# import scipy
# import subprocess

frequencies = np.loadtxt('frequencies.dat')
data = np.loadtxt('data.dat')


keys = (
    'rho0',
    'sigma0',
    'm_tot_n',
    'sigma_infty',
)

for model in (0, 1, ):
    for norm_factor in (1, 10, 20, 50, 1000):
        os.environ['DD_COND'] = '{}'.format(model)
        config = cfg_single.cfg_single()
        config['frequency_file'] = frequencies
        config['data_file'] = data
        config['fixed_lambda'] = 10
        config['norm'] = norm_factor
        # generate a ccd object
        ccd_obj = ccd_single.ccd_single(config)

        # commence with the actual fitting
        ccd_obj.fit_data()

        # extract the last iteration
        last_it = ccd_obj.results[0].iterations[-1]

        print('model: {}, norm: {}'.format(model, norm_factor))
        for key in keys:
            if key in last_it.stat_pars:
                print('    {}: {}'.format(key, last_it.stat_pars[key]))

# print(dir(last_it))
# print('fit parameters', last_it.m)
# print('stat_pars', last_it.stat_pars)

# print('raw', last_it.m[0], 10 ** last_it.m[0])
# rho0 = 10 ** last_it.m[0] / last_it.settings['norm_factors']
# print('rho0', rho0)

# save to directory
# ccd_obj.save_to_directory('resultstest3')
# fig = last_it.plot()
