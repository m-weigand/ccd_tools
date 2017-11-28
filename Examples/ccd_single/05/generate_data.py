#!/usr/bin/python
"""
Generate sample SIP-Spectrum
"""
import numpy as np
import NDimInv.colecole as CC

frequencies = np.logspace(-2, 4, 20)
fin = np.hstack((frequencies, frequencies))

rho0 = 50
m = 0.1
tau = 0.04
c = 1

cc_pars = [np.log(rho0), m, np.log(tau), c, 0.1, np.log(0.00004), 1]

magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

np.savetxt('data.dat', magpha)
np.savetxt('frequencies.dat', frequencies)
