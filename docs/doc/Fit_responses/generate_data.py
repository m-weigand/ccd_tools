#!/usr/bin/python
"""
Generate sample SIP-Spectrum
"""
import numpy as np
import lib_dd.colecole as CC

frequencies = np.logspace(-3, 3, 25)
fin = np.hstack((frequencies, frequencies))

# rho0 m1 tau1 c1 m2 tau2 c2
cc_sets = [
    [np.log(50), 0.05, np.log(0.04), 0.5],
    [np.log(50), 0.05, np.log(0.04), 1.0],
    [np.log(50), 0.05, np.log(20), 0.5, 0.15, np.log(0.0008), 0.8],
    [np.log(50), 0.05, np.log(20), 0.7, 0.15, np.log(0.0008), 1.0],
]

magpha_list = []
for cc_pars in cc_sets:
    magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
    magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])
    magpha_list.append(magpha)

magpha_array = np.array(magpha_list).squeeze()
print magpha_array.shape


np.savetxt('data.dat', magpha_array)
np.savetxt('frequencies.dat', frequencies)
