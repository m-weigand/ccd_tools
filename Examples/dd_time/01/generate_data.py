#!/usr/bin/python
"""
Generate sample SIP-Spectra for 5 time steps
"""
import os
import numpy as np
import crlab_py.colecole as CC

frequencies = np.logspace(-2, 4, 20)
fin = np.hstack((frequencies, frequencies))

# generate CC parameters
rho0 = [10, 20]
m = np.logspace(-2, -1, 3)
tau = np.logspace(np.log10(0.004), np.log10(0.4), 5)
# note: we keep c constant
c = 0.6

basedir = 'data'
if(not os.path.isdir(basedir)):
    os.makedirs(basedir)
os.chdir(basedir)

cr_data = []
cc_list = []
for timestep in range(0, 5):
    cc_pars = [np.log(rho0[timestep % 2]), m[0], np.log(tau[0]), c]
    cc_list.append(cc_pars)

    magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
    magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

    cr_data.append(magpha)
cr_data = np.array(cr_data).squeeze()

np.savetxt('data.dat', cr_data)
np.savetxt('frequencies.dat', frequencies)
np.savetxt('times.dat', range(0, 5))
np.savetxt('cc_pars.dat', np.array(cc_list))
