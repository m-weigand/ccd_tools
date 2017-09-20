#!/usr/bin/env python
""" Generate sample SIP-Spectrum
"""
import numpy as np
import NDimInv.colecole as CC

frequencies = np.logspace(-3, 3, 25)
fin = np.hstack((frequencies, frequencies))

data = []
for rho0 in (100000, 1000, 100):
    # rho0 m1 tau1 c1 m2 tau2 c2
    cc_pars = [np.log(rho0), 0.05, np.log(40), 0.6,
               0.15, np.log(0.0001), 0.6]

    magpha = CC.cole_log(fin, cc_pars).flatten()
    magpha[0:magpha.size / 2] = np.exp(magpha[0:magpha.size / 2])
    data.append(magpha)

np.savetxt('data.dat', np.array(data))
np.savetxt('frequencies.dat', frequencies)
