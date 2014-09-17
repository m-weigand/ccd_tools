#!/usr/bin/python
"""
Generate sample SIP-Spectrum
"""
import numpy as np
import crlab_py.colecole as CC

frequencies = np.logspace(-3, 3, 100)
fin = np.hstack((frequencies, frequencies))

rho0 = 50
m = 0.1
tau = 0.04
c = 1

cc_pars = [np.log(rho0), 0.05, np.log(40), 0.6,
           0.15, np.log(0.0001), 0.6]

magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

magpha = np.resize(magpha, (10, magpha.shape[1]))

np.savetxt('data.dat', magpha)
np.savetxt('frequencies.dat', frequencies)
