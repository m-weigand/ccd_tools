#!/usr/bin/python
"""
Generate sample SIP-Spectrum
"""
import numpy as np
import NDimInv.colecole as CC

frequencies = np.logspace(-3, 3, 25)
fin = np.hstack((frequencies, frequencies))

rho0 = 50

cc_pars = [np.log(rho0), 0.05, np.log(40), 0.6,
           0.15, np.log(0.0001), 0.6]

magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

# add noise
np.random.seed(5)

noise_mag_rel = 5  # %
mag_rel = np.abs(magpha[0, 0:magpha.size / 2] * (noise_mag_rel / 100.0))
mag_noise = [np.random.normal(0, x) for x in mag_rel]
magpha[0, 0:magpha.size / 2] += mag_noise

noise_pha_rel = 5  # %
pha_rel = np.abs(magpha[0, magpha.size / 2:] * (noise_pha_rel / 100.0))
pha_noise = [np.random.normal(0, x) for x in pha_rel]
magpha[0, magpha.size / 2:] += pha_noise

np.savetxt('data.dat', magpha)
np.savetxt('frequencies.dat', frequencies)
