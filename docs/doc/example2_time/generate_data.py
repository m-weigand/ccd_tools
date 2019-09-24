#!/usr/bin/env python
# *-* coding: utf-8 *-*
"""
Generate sample SIP-Spectra for 9 time steps, decreasing linearly tau
"""
import os
import numpy as np
import shutil
from sip_models.res.cc import cc as cc_res

# times = range(0, 10) + range(19, 29)
frequencies = np.logspace(-2, 4, 20)

# generate CC parameters
np.random.seed(6)
rho0 = 50
# variant 1: add noise to CC pars
# m_1 = np.random.uniform(0, 0.01, size=10) + 0.1
# m_2 = np.random.uniform(0, 0.01, size=10) + 0.05

m_raw = np.linspace(0.10, 0.05, 30)

# variant 2: add noise later on data
times = [0, 1, 2, 3, 6, 10, 11, 20, 22, 25, 29]
m = m_raw[times]
print('m_wo_noise', m)

# add noise to m-values
m *= (1 + np.random.normal(-1, 1, size=m.size) * 0.05)
print('m_w_noise', m)
tau = 0.004
c = 0.6

basedir = 'data'
if(os.path.isdir(basedir)):
    shutil.rmtree(basedir)
os.makedirs(basedir)
os.chdir(basedir)

cr_data = []
cr_data_orig = []
cc_list = []
for timestep in range(0, len(times)):
    cc_pars = [rho0, m[timestep], tau, c]
    cc_list.append(cc_pars)

    ccobj = cc_res(frequencies=frequencies)
    response = ccobj.response(cc_pars)
    rmagpha = response.rmag_rpha
    # convert rmag to exp
    rmagpha[:, 0] = np.exp(rmagpha[:, 0])
    rmagpha_nonoise = rmagpha.flatten(order='F')

    cr_data_orig.append(rmagpha_nonoise)
    # add noise to phase data
    # magpha[magpha.size / 2:] *= (1 + np.random.normal(-1, 1, size=1) * 0.10)

    # add a small frequency noise to phase
    rmagpha[:, 1] += np.random.normal(0, 0.5, size=20)
    cr_data.append(rmagpha.flatten(order='F'))

cr_data = np.array(cr_data).squeeze()
cr_data_orig = np.array(cr_data_orig).squeeze()

np.savetxt('data.dat', cr_data)
np.savetxt('data_orig.dat', cr_data_orig)
np.savetxt('frequencies.dat', frequencies)
np.savetxt('times.dat', times)
cc_par_list = np.array(cc_list)
# make rho0 and tau log-again!
cc_par_list[:, 0] = np.log(cc_par_list[:, 0])
cc_par_list[:, 2] = np.log(cc_par_list[:, 2])
np.savetxt('cc_pars.dat', np.array(cc_par_list))
