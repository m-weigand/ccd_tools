#!/usr/bin/python
"""
Generate sample SIP-Spectra for 5 time steps and 9 locations (3x3 tiles)
"""
import os
import numpy as np
import crlab_py.colecole as CC

frequencies = np.logspace(-2, 4, 20)
fin = np.hstack((frequencies, frequencies))

# generate CC parameters
rho0 = np.linspace(10, 1000, 3)
m = np.logspace(-2, -1, 3)
tau = np.logspace(np.log10(0.004), np.log10(0.4), 5)
# note: we keep c constant
c = 0.6

basedir = 'data'
if(not os.path.isdir(basedir)):
    os.makedirs(basedir)
os.chdir(basedir)

time_files = []
for timestep in range(0, 5):
    cr_spectra = []
    for xx in range(0, 18):
        for yy in range(0, 18):
            x = xx % 3
            y = yy % 3
            cc_pars = [np.log(rho0[y]), m[x], np.log(tau[timestep]), c]

            magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
            magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])
            cr_spectra.append(magpha)
    filename = 'time_data_{0}.dat'.format(timestep)
    time_files.append(filename)
    cr_spectra = np.array(cr_spectra).squeeze()
    np.savetxt(filename, cr_spectra)

with open('data_index.dat', 'w') as fid:
    [fid.write(i + '\n') for i in time_files]
np.savetxt('times.dat', range(0, 5))
np.savetxt('frequencies.dat', frequencies)
