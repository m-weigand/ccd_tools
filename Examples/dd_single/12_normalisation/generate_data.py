#!/usr/bin/python
"""
Generate sample SIP-Spectrum
"""
import numpy as np
import lib_dd.colecole as CC
# import sip_formats.convert as sf

frequencies = np.logspace(-3, 3, 25)
fin = np.hstack((frequencies, frequencies))

# rho0 m1 tau1 c1 m2 tau2 c2
cc_pars = [np.log(2), 0.025, np.log(40), 0.6,
           0.75, np.log(0.0001), 0.6]

magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

np.savetxt('data_rmagrpha.dat', magpha)
np.savetxt('frequencies.dat', frequencies)
