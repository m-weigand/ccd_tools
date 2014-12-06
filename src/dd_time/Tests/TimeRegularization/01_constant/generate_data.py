#!/usr/bin/python
"""
Generate sample SIP-Spectra for 5 time steps
"""
import os
import numpy as np
import NDimInv.colecole as CC

frequencies = np.logspace(-2, 4, 20)
fin = np.hstack((frequencies, frequencies))

# generate CC parameters
rho0 = 50
m = np.repeat(0.1, 10)
tau = 0.4
c = 0.6

basedir = 'data'
if(not os.path.isdir(basedir)):
    os.makedirs(basedir)
os.chdir(basedir)

cr_data = []
cc_list = []
for timestep in range(0, m.size):
    cc_pars = [np.log(rho0), m[timestep], np.log(tau), c]
    cc_list.append(cc_pars)

    magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
    magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

    cr_data.append(magpha)
cr_data = np.array(cr_data).squeeze()

np.savetxt('data.dat', cr_data)
np.savetxt('frequencies.dat', frequencies)
np.savetxt('times.dat', range(0, m.size))
np.savetxt('cc_pars.dat', np.array(cc_list))
