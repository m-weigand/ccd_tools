#!/usr/bin/python
"""
Recreate an inversion
"""
import numpy as np
import debye_decomposition as dd_single
import json
import NDimInv

# get settings
with open('results/inversion_options.json', 'r') as fid:
    opts = json.load(fid)

frequencies = np.loadtxt('results/frequencies.dat')
lambdas = np.atleast_1d(np.loadtxt('results/lambdas.dat'))
lambdas = [x for x in lambdas]
rho0 = np.loadtxt('results/rho0_results.dat')
m_i = np.loadtxt('results/m_i_results.dat')
m = np.hstack((rho0, m_i))
print m.shape
print lambdas
data_format = open('results/data_format.dat').readline().strip()
opts['prep_data_format'] = data_format
# now we need a list with spectra
data_list = []
with open('results/data.dat', 'r') as fid:
    for line in fid.readlines():
        subdata = np.fromstring(line.strip(), sep=' ')
        subdata = subdata.reshape((subdata.size / 2, 2), order='F')
        print subdata
        data_list.append(subdata)

# create data list
fit_datas = dd_single._get_fit_datas(frequencies, data_list, opts)

# create ND object
ND = dd_single._prepare_ND_object(fit_datas[0])

print 'Iterations', ND.iterations
# recreate the last iterations

it = NDimInv.main.Iteration(1, ND.Data, ND.Model)
it.lams = lambdas
it.m = m
it.f = it.Model.obj.convert_parameters(it.Model.f(it.m))

#it.plot()
ND.iterations.append(it)
ND.run_inversion()
for it in ND.iterations:
    it.plot()
