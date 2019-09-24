#!/usr/bin/python
"""
Generate sample SIP-Spectra for 9 time steps, decreasing tau linearly
"""
import os
import numpy as np
# import crlab_py.colecole as CC
from sip_models.res.cc import cc as cc_res

frequencies = np.logspace(-2, 4, 20)

# generate CC parameters
np.random.seed(5)
rho0 = 50

m = np.linspace(0.01, 0.15, 20) + np.random.uniform(0, 0.01, size=20)

# m = np.logspace(-2, -1, 3)
# tau = np.logspace(np.log10(0.004), np.log10(0.4), 20)
tau = 0.004
# note: we keep c constant
c = 0.6

basedir = 'data'
if(not os.path.isdir(basedir)):
    os.makedirs(basedir)
os.chdir(basedir)

cr_data = []
cc_list = []
for timestep in range(0, 20):
    cc_pars = [rho0, m[timestep], tau, c]
    cc_list.append(cc_pars)

    ccobj = cc_res(frequencies=frequencies)
    response = ccobj.response(cc_pars)
    rmagpha = response.rmag_rpha
    # convert rmag to exp
    rmagpha[:, 0] = np.exp(rmagpha[:, 0])

    # magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
    # magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

    cr_data.append(rmagpha.flatten(order='F'))
cr_data = np.array(cr_data).squeeze()

np.savetxt('data.dat', cr_data)
np.savetxt('frequencies.dat', frequencies)
# times = range(0, 10) + range(20, 30)
times = range(0, 20)
np.savetxt('times.dat', times)
np.savetxt('cc_pars.dat', np.array(cc_list))
