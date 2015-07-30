#!/usr/bin/python
"""
Generate sample SIP-Spectra for 9 time steps, decreasing linearly tau
"""
import os
import numpy as np
import shutil
import crlab_py.colecole as CC


# times = range(0, 10) + range(19, 29)
frequencies = np.logspace(-2, 4, 20)
fin = np.hstack((frequencies, frequencies))

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
print 'm_wo_noise', m

# add noise to m-values
m *= (1 + np.random.normal(-1, 1, size=m.size) * 0.05)
print 'm_w_noise', m
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
    cc_pars = [np.log(rho0), m[timestep], np.log(tau), c]
    cc_list.append(cc_pars)

    magpha = CC.cole_log(fin, cc_pars).flatten()
    magpha[0:magpha.size / 2] = np.exp(magpha[0:magpha.size / 2])
    magpha_orig = magpha.copy()
    cr_data_orig.append(magpha_orig)
    # add noise to phase data
    # magpha[magpha.size / 2:] *= (1 + np.random.normal(-1, 1, size=1) * 0.10)

    # add a small frequency noise
    magpha[magpha.size / 2:] += np.random.normal(0, 0.5, size=20)
    cr_data.append(magpha)

cr_data = np.array(cr_data).squeeze()
cr_data_orig = np.array(cr_data_orig).squeeze()

np.savetxt('data.dat', cr_data)
np.savetxt('data_orig.dat', cr_data_orig)
np.savetxt('frequencies.dat', frequencies)
np.savetxt('times.dat', times)
np.savetxt('cc_pars.dat', np.array(cc_list))
