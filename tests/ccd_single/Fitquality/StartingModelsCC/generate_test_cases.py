#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Generate multiple SIP spectra by varying the Cole-Cole parameters m, tau, and c
"""
import os
import numpy as np
import lib_cc.main
frequencies = np.logspace(-2, 4, 20)
cc_obj = lib_cc.main.get('logrho0_m_logtau_c', {'frequencies': frequencies})

data_list = []
for m in (0.1, 0.8):
    for c in np.linspace(0.05, 1.0, 4):
        for tau in np.logspace(np.log10(frequencies.min()),
                               np.log10(frequencies.max()),
                               4):
            pars = [np.log(100), m, np.log(tau), c]

            rlnmag_rpha = cc_obj.forward(pars)
            rmag_rpha = rlnmag_rpha.copy()
            rmag_rpha[:, 0] = np.exp(rmag_rpha[:, 0])
            data_list.append(rmag_rpha.flatten(order='F'))

if not os.path.isdir('data'):
    os.makedirs('data')

np.savetxt('data/frequencies.dat', frequencies)
np.savetxt('data/data.dat', np.array(data_list))
