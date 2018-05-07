#!/usr/bin/env python3
# *-* coding: utf-8 *-*
# simple example for using the ccd_single module directly with Python
import lib_dd.decomposition.ccd_single as ccd_single
import lib_dd.config.cfg_single as cfg_single
import numpy as np

frequencies = np.loadtxt('data/frequencies.dat')
data = np.loadtxt('data/data.dat')

# set options using this dict-like object
config = cfg_single.cfg_single()
config['frequency_file'] = frequencies
config['data_file'] = data
config['fixed_lambda'] = 10

# generate a ccd object
ccd_obj = ccd_single.ccd_single(config)

# commence with the actual fitting
ccd_obj.fit_data()

# extract the last iteration
last_it = ccd_obj.results[0].iterations[-1]

print(dir(last_it))
print('fit parameters', last_it.m)
print('stat_pars', last_it.stat_pars)

# save to directory
ccd_obj.save_to_directory()

# you need to supply a filename to directly save the figure to file
# Note that at the moment filenames sometimes will be handled wrong.
# For now we suggest to use the method below
last_it.plot(filename='plot.png')
# if you do not supply a filename, a figure object will be returned
fig = last_it.plot()
fig.savefig('plot_v2.png', dpi=300)
# you could also use the figure object to modify the whole figure
