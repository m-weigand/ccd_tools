#!/usr/bin/python
"""
Generate sample SIP-Spectrum
"""
import numpy as np
import NDimInv.colecole as CC

frequencies = np.logspace(-3, 3, 25)
fin = np.hstack((frequencies, frequencies))

pixel_list = []  # stores the pixel spectra

for m, nr in ((0.05, 100), (0.07, 120)):
    for spec in range(0, nr):
        # rho0 m1 tau1 c1 m2 tau2 c2
        cc_pars = [np.log(50), m, np.log(40), 0.6,
                   0.15, np.log(0.0001), 0.6]
        magpha = CC.cole_log(fin, cc_pars).flatten()
        magpha[0:magpha.size / 2] = np.exp(magpha[0:magpha.size / 2])
        print magpha.shape
        pixel_list.append(magpha)

pixel_list = np.array(pixel_list)
print pixel_list.shape
np.savetxt('data.dat', pixel_list)
np.savetxt('frequencies.dat', frequencies)
