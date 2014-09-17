#!/usr/bin/python
"""
Generate sample SIP-Spectra for 9 time steps, decreasing linearly tau
"""
import os
import numpy as np
import crlab_py.colecole as CC

frequencies = np.logspace(-2, 4, 20)
fin = np.hstack((frequencies, frequencies))

# generate CC parameters
np.random.seed(5)
rho0_1 = np.random.randint(0, 10, size=10) + 70
rho0_2 = np.random.randint(0, 10, size=10) + 30
rho0 = np.hstack((rho0_1, rho0_2))

m = np.logspace(-2, -1, 3)
tau = np.logspace(np.log10(0.004), np.log10(0.4), 20)
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
    cc_pars = [np.log(rho0[timestep]), m[0], np.log(tau), c]
    cc_list.append(cc_pars)

    magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
    magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

    cr_data.append(magpha)
cr_data = np.array(cr_data).squeeze()

np.savetxt('data.dat', cr_data)
np.savetxt('frequencies.dat', frequencies)
times = range(0, 10) + range(20, 30)
np.savetxt('times.dat', times)
np.savetxt('cc_pars.dat', np.array(cc_list))
