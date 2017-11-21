#!/usr/bin/env python
"""
Generate sample SIP-Spectrum
"""
import numpy as np

import sip_models.res.cc as cc_res
# import lib_dd.colecole as CC

frequencies = np.logspace(-3, 3, 30)
fin = np.hstack((frequencies, frequencies))

# rho0 m1 tau1 c1 m2 tau2 c2
cc_pars = [
    np.log(50),
    0.05,
    np.log(40),
    0.6,
    0.15,
    np.log(0.0001),
    0.6
]
cc_pars = [
    # rho0
    50,
    # m
    0.05,
    0.15,
    # tau
    40,
    0.01,
    # c
    0.6,
    0.9
]

obj = cc_res.cc(frequencies)
response = obj.response(cc_pars)
print(response.rmag_rpha)

# magpha = CC.cole_log(fin, cc_pars).flatten()[np.newaxis, :]
# magpha[0, 0:magpha.size / 2] = np.exp(magpha[0, 0:magpha.size / 2])

np.savetxt(
    'data.dat',
    response.rmag_rpha.reshape((1, 2 * frequencies.size), order='F'))
np.savetxt('frequencies.dat', frequencies)
