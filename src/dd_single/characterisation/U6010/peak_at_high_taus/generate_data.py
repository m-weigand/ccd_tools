#!/usr/bin/python
"""
Generate sample SIP-Spectrum
"""
import numpy as np
import lib_dd.colecole as CC

frequencies = np.logspace(-3, 3, 25)
fin = np.hstack((frequencies, frequencies))

# rho0 m1 tau1 c1 m2 tau2 c2
cc_pars = [np.log(50), 0.1, np.log(50), 0.6]

magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

np.savetxt('data.dat', magpha)
np.savetxt('frequencies.dat', frequencies)
